#!/usr/bin/env python3
if __name__ == '__main__':
    import os
    import sys
    sys.path.insert(0, os.path.join(
        os.path.abspath(os.path.dirname(__file__)), '..', '..'))

    # Install the asyncio reactor as early as possible
    from trosnoth.qtreactor import declare_this_module_requires_qt_reactor
    declare_this_module_requires_qt_reactor()

import random

from trosnoth.const import BOT_GOAL_CAPTURE_MAP, ACHIEVEMENT_TACTICAL
from trosnoth.levels.base import play_level, Level
from trosnoth.levels.maps import (
    LabyrinthMap, LargeRingsMap, SmallRingMap,
    StandardMap, WideMap, LargeMap, SmallMap,
)
from trosnoth.messages import AwardPlayerCoinMsg, ZoneStateMsg
from trosnoth.model.universe import OrbRegion
from trosnoth.model.universe_base import NEUTRAL_TEAM_ID
from trosnoth.triggers.coins import SlowlyIncrementLivePlayerCoinsTrigger
from trosnoth.utils.event import waitForEvents
from trosnoth.utils.math import distance

BONUS_COINS_FOR_WINNER = 500


class OrbChaseLevel(Level):
    allowAutoTeams = False
    levelName = 'Orb Chase'
    default_duration = 6 * 60
    map_selection = (
        LabyrinthMap(),
        LargeRingsMap(),
        SmallRingMap(),
        StandardMap(),
        SmallMap(),
        WideMap(),
        LargeMap(),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.duration = self.level_options.get_duration(self)

        self.team = None
        self.targetZone = None
        self.targetTeamId = None

    def getTeamToJoin(self, preferredTeam, user, bot):
        return self.team

    def pre_sync_setup(self):
        self.team, _ = self.pre_sync_create_teams([
            ('Racers', self.world.players),
            ('Targets', ()),
        ])
        self.targetTeamId = self.world.teams[1].id
        self.level_options.apply_map_layout(self)
        for zone in self.world.zones:
            if zone.owner != self.team:
                zone.owner = None
        self.world.uiOptions.team_ids_humans_can_join = [b'A']

    async def run(self):
        SlowlyIncrementLivePlayerCoinsTrigger(self).activate()
        self.world.setActiveAchievementCategories({ACHIEVEMENT_TACTICAL})
        self.world.scoreboard.setMode(players=True)
        self.world.abilities.set(zoneCaps=False, balanceTeams=False)

        await self.pregameCountdownPhase()
        await self.mainPhase()

        # Game over!
        playerScores = self.world.scoreboard.playerScores
        max_score = max(playerScores.values())
        winners = [
            p for p, score in list(playerScores.items())
            if score == max_score
        ]

        self.set_winners(winners)
        for winner in winners:
            self.world.sendServerCommand(
                AwardPlayerCoinMsg(winner.id, BONUS_COINS_FOR_WINNER))

        return (max_score > 0), max_score

    async def pregameCountdownPhase(self, delay=10):
        self.setUserInfo('Get Ready...', (
            '* Game will begin soon',
            '* Score points by touching the red orb',
        ), BOT_GOAL_CAPTURE_MAP)
        self.world.clock.startCountDown(delay, flashBelow=0)
        self.world.clock.propagateToClients()

        self.world.pauseStats()
        self.world.abilities.set(respawn=False)
        await self.world.clock.onZero.wait_future()

    async def mainPhase(self):
        self.setUserInfo('Orb Chase', (
            '* Score points by touching the red orb',
            '* Don’t forget you have a grappling hook (R.Click by default)',
        ), BOT_GOAL_CAPTURE_MAP)
        self.notifyAll('The game is now on!!')
        self.playSound('startGame.ogg')
        self.world.resumeStats()
        self.world.abilities.set(respawn=True)

        if self.duration:
            self.world.clock.startCountDown(self.duration)
        else:
            self.world.clock.stop()
        self.world.clock.propagateToClients()

        onClockZero = self.world.clock.onZero

        while True:
            zone = self.selectZone()
            region = OrbRegion(self.world, zone.defn)
            self.world.addRegion(region)
            try:
                event, args = await waitForEvents(
                    [onClockZero, region.onEnter])

                if event == onClockZero:
                    break

                self.playSound('short-whistle.ogg')
                self.world.scoreboard.playerScored(args['player'], 1)
            finally:
                self.world.removeRegion(region)

    def selectZone(self):
        if self.targetZone:
            self.world.sendServerCommand(
                ZoneStateMsg(self.targetZone.id, NEUTRAL_TEAM_ID, True))

        allZones = [z for z in self.world.zones if z.owner is None]
        options = [z for z in allZones if not z.players]
        if options:
            zone = random.choice(options)
        else:
            zone = min(
                allZones,
                key=lambda z: min(
                    distance(z.defn.pos, p.pos) for p in z.players))

        self.world.sendServerCommand(
            ZoneStateMsg(zone.id, self.targetTeamId, True))
        self.targetZone = zone
        return zone


if __name__ == '__main__':
    play_level(OrbChaseLevel())
