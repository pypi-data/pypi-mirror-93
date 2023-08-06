import logging

from trosnoth.const import TICK_PERIOD
from trosnoth.model.hub import Hub, Node
from trosnoth.messages import TickMsg
from trosnoth.utils import globaldebug
from trosnoth.utils.utils import timeNow

log = logging.getLogger(__name__)


class UIMsgThrottler(Hub, Node):
    '''
    This class is used for RemoteGames which are connected to the UI. It delays
    messages a little bit, in order that the UI can smoothly display what is
    happening even if there is some variation in network round trip time.
    '''

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.smoother = LagSmoothingCalculator()
        self.agent_event_groups = [[]]

    def stop(self):
        pass

    def disconnectNode(self):
        super().disconnectNode()
        self.hub.disconnectNode()

    def connectNewAgent(self, authTag=0):
        return self.hub.connectNewAgent(authTag=authTag)

    def disconnectAgent(self, agentId):
        if self.hub:
            self.hub.disconnectAgent(agentId)

    def sendRequestToGame(self, agentId, msg):
        if self.hub:
            self.hub.sendRequestToGame(agentId, msg)

    def gotServerCommand(self, msg):
        msg.tracePoint(self, 'gotServerCommand')
        if isinstance(msg, TickMsg):
            self.agent_event_groups[-1].append((self.node.gotServerCommand, msg))
            self.agent_event_groups.append([])

            self.smoother.got_tick()
            if globaldebug.enabled:
                globaldebug.tick_logger.ui_throttler_saw_tick(msg.tickId)
        elif msg.pumpAllEvents:
            self.agent_event_groups[-1].append((self.node.gotServerCommand, msg))
            self.pump_events()
        elif msg.isControl:
            self.node.gotServerCommand(msg)
        else:
            self.agent_event_groups[-1].append((self.node.gotServerCommand, msg))

    def gotMessageToAgent(self, agentId, msg):
        if msg.isControl:
            self.node.gotMessageToAgent(agentId, msg)
        else:
            self.agent_event_groups[-1].append((self.node.gotMessageToAgent, agentId, msg))

    def agentDisconnected(self, agentId):
        self.node.agentDisconnected(agentId)

    def release_event_group(self):
        if not self.has_groups_to_release():
            # No complete event groups to release
            return
        group = self.agent_event_groups.pop(0)
        for event in group:
            event[-1].tracePoint(self, 'release_event_group')
            event[0](*event[1:])

    def uiTick(self, deltaT):
        '''
        Called to indicate that the UI has advanced by the given time delta.
        Returns the tween fraction to use in the UI.
        '''
        ticks_to_release, tween_fraction = self.smoother.get_ticks_and_fraction(deltaT)
        for i in range(ticks_to_release):
            self.release_event_group()
        return tween_fraction

    def has_groups_to_release(self):
        return len(self.agent_event_groups) >= 2

    def pump_events(self):
        '''
        Causes us to immediately release all event groups.
        '''
        self.agent_event_groups.append([])
        while self.has_groups_to_release():
            self.release_event_group()
        self.smoother.reset()


class LocalGameTweener(object):
    '''
    Used in place of a UIMsgThrottler for a local game to simply get the
    current tween fraction.
    '''
    def __init__(self, game):
        self.game = game
        self.tweenFraction = 0
        game.onServerCommand.addListener(self.gotServerCommand)

    def stop(self):
        self.game.onServerCommand.removeListener(self.gotServerCommand)

    def gotServerCommand(self, msg):
        if isinstance(msg, TickMsg):
            self.tweenFraction -= 1

    def uiTick(self, deltaT):
        self.tweenFraction += deltaT / TICK_PERIOD
        if self.tweenFraction < 0:
            self.tweenFraction = 0
        elif self.tweenFraction > 2:
            # Could be just after a pause, so a jump's ok as we catch up
            self.tweenFraction = 1
        elif self.tweenFraction >= 1:
            self.game.world.requestTickNow()
            if self.tweenFraction > 1:
                # Game is still paused / AI data is still loading
                self.tweenFraction = 1
        return self.tweenFraction


class LagSmoothingCalculator(object):
    STEP_TIME = 2               # seconds
    CATCH_UP_RATE = 1.5         # speed multiplier
    ACCELERATION_TIME = 1.5     # seconds

    # v = u + at
    ACCELERATION = (CATCH_UP_RATE - 1) / ACCELERATION_TIME
    # s = ½(u + v)t
    ACCEL_RATE_CHANGE = (1 + CATCH_UP_RATE) * ACCELERATION_TIME / 2

    def __init__(self):
        self.steps = []
        self.last_offset = 0
        self.last_sequence_number = -1
        self.released_offset = 0
        self.released_sequence_number = -1
        self.last_release_time = timeNow()

        self.relative_time = self.last_release_time - self.last_offset
        self.rate = 1

    def reset(self):
        self.steps = []
        self.last_offset = 0
        self.last_sequence_number = -1
        self.released_offset = 0
        self.released_sequence_number = -1

    def got_tick(self):
        self.last_offset += TICK_PERIOD
        self.last_sequence_number += 1
        now = timeNow()
        relative_time = now - self.last_offset
        sequence_number = self.last_sequence_number

        if self.steps:
            seq, rel = self.steps[-1]

            while rel < relative_time:
                # This new step is larger than the previous step
                self.steps.pop(-1)
                if not self.steps:
                    break
                seq, rel = self.steps[-1]

        self.steps.append((sequence_number, relative_time))

    def get_ticks_and_fraction(self, delta_t):
        if not self.steps:
            return 0, 1
        seq, rel = self.steps[0]

        if rel >= self.relative_time:
            # Ticks message was late (or perfectly timed).
            # Release immediately.
            self.relative_time = rel
            self.rate = 1
        else:
            if self.relative_time - rel <= self.ACCEL_RATE_CHANGE:
                # Slow the playback rate down again until we hit normal
                # v² = u² + 2as
                self.rate = (1 + 2 * self.ACCELERATION * (self.relative_time - rel)) ** 0.5
            else:
                # Speed playback up until we hit CATCH_UP_RATE
                self.rate = min(self.CATCH_UP_RATE, self.rate + self.ACCELERATION * delta_t)
            self.relative_time = max(rel, self.relative_time - TICK_PERIOD * (self.rate - 1))

        ticks = (timeNow() - self.relative_time - self.released_offset) / TICK_PERIOD
        ticks, fraction = divmod(ticks, 1)

        if ticks > self.last_sequence_number - self.released_sequence_number:
            # No more ticks to release
            ticks = self.last_sequence_number - self.released_sequence_number
            fraction = 1

        # Clear out steps older than STEP_TIME
        self.released_sequence_number += ticks
        self.released_offset += TICK_PERIOD * ticks
        clear_steps_before = self.released_sequence_number - round(self.STEP_TIME / TICK_PERIOD)
        while self.steps and clear_steps_before >= self.steps[0][0]:
            self.steps.pop(0)

        return round(ticks), fraction
