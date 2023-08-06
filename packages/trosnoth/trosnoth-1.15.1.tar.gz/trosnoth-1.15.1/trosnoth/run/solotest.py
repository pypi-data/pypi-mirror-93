import asyncio
import functools
import logging
import sys

from twisted.internet import defer, reactor

from trosnoth.const import DEFAULT_BOT_DIFFICULTY
from trosnoth.game import LocalGame, RemoteGame
from trosnoth.gamerecording.replays import ReplayPlayer
from trosnoth.gui.app import get_pygame_runner, UserClosedPygameWindow
from trosnoth.manholehelper import LocalManholeHelper
from trosnoth.model import mapLayout
from trosnoth.model.agenthub import LocalHub
from trosnoth.model.hub import Hub, Node
from trosnoth.model.uithrottler import UIMsgThrottler, LocalGameTweener
from trosnoth.run.common import initialise_trosnoth_app
from trosnoth.settings import ClientSettings
from trosnoth.trosnothgui.ingame.gameInterface import GameInterface
from trosnoth.utils.utils import console_locals, run_in_pygame, new_console_context

log = logging.getLogger(__name__)


class SoloGameClosed(Exception):
    pass


def launch_solo_game(**kwargs):
    with new_console_context():
        size, full_screen = ClientSettings.get().display.get_size_and_full_screen()
        try:
            get_pygame_runner().launch_application(
                functools.partial(
                    launch_solo_game_async, return_when_level_completes=False, **kwargs),
                size=size,
                full_screen=full_screen,
            )
        except (UserClosedPygameWindow, SoloGameClosed):
            pass


@run_in_pygame
async def launch_solo_game_async(*, return_when_level_completes=True, **kwargs):
    with initialise_trosnoth_app() as app:
        game, game_interface = build_game(app, **kwargs)
        return_value = None
        try:
            tasks = [asyncio.ensure_future(app.runner.run())]
            if return_when_level_completes:
                level_task = asyncio.ensure_future(game.wait_for_level_to_complete())
                tasks.append(level_task)
            else:
                level_task = None

            done, pending = await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)
            if level_task and level_task.done():
                return_value = level_task.result()

            for task in pending:
                task.cancel()
        finally:
            game.stop()
            game_interface.stop()
    if return_value is None:
        raise SoloGameClosed()
    return return_value


def build_game(
        app, level=None,
        isolate=False, bot_count=0, bot_class='ranger',
        map_blocks=(), test_mode=False, stack_teams=False,
        delay=None, bots_only=False, no_auto_balance=False,
        game_prefix='unnamed',
        bot_difficulty=DEFAULT_BOT_DIFFICULTY,
        add_bots=(),
        save_replay=False,
):
    db = mapLayout.LayoutDatabase(blocks=map_blocks)
    game_type = 'solo'
    game = LocalGame(
        db, onceOnly=True,
        level=level,
        gameType=game_type,
        gamePrefix=game_prefix,
        botProcess=True,
        bots_only=bots_only,
        no_auto_balance=no_auto_balance,
        saveReplay=save_replay,
    )
    if test_mode:
        game.world.setTestMode()

    bots = []

    try:
        for i in range(bot_count):
            if stack_teams:
                bot = game.addBot(
                    bot_class, team=game.world.teams[0], difficulty=bot_difficulty)
            else:
                bot = game.addBot(bot_class, difficulty=bot_difficulty)
            bots.append(bot)
    except ImportError:
        print('AI module not found: %s' % (bot_class,), file=sys.stderr)
        sys.exit(1)
    except AttributeError:
        print((
                'AI module does not define BotClass: %s' % (bot_class,)), file=sys.stderr)
        sys.exit(1)

    console_locals_dict = console_locals.get()

    # Create a client and an interface.
    if isolate:
        rgame = RemoteGame(db)
        console_locals_dict['rgame'] = rgame
        hub = LocalHub(game)
        app.tweener = UIMsgThrottler()
        if delay:
            delayer = DelayNodeHub(delay)
            hub.connectNode(delayer)
            delayer.connectNode(app.tweener)
        else:
            hub.connectNode(app.tweener)
        app.tweener.connectNode(rgame)
        gi = GameInterface(app, rgame, spectate=bots_only)
        rgame.connected(game.world.dumpEverything())
    else:
        app.tweener = LocalGameTweener(game)
        gi = GameInterface(app, game, spectate=bots_only)
    console_locals_dict['game_interface'] = gi
    gi.onDisconnectRequest.addListener(app.stop)
    gi.onConnectionLost.addListener(app.stop)
    app.interface.elements.append(gi)

    for team_index, bot_specs in enumerate(add_bots):
        for bot_class, difficulty in bot_specs:
            bot = game.addBot(
                bot_class, team=game.world.teams[team_index], difficulty=difficulty)
            bots.append(bot)

    console_locals_dict.update({
        'game': game,
        'bots': bots,
        'helper': LocalManholeHelper(lambda: game),
    })
    return game, gi


class DelayNodeHub(Hub, Node):
    def __init__(self, delay, *args, **kwargs):
        super(DelayNodeHub, self).__init__(*args, **kwargs)
        self.delay = delay

    @defer.inlineCallbacks
    def connectNewAgent(self, authTag=0):
        result = yield self.hub.connectNewAgent(authTag=authTag)

        d = defer.Deferred()
        reactor.callLater(self.delay, d.callback, None)
        yield d

        defer.returnValue(result)

    def disconnectAgent(self, agentId):
        reactor.callLater(self.delay, self.hub.disconnectAgent, agentId)

    def sendRequestToGame(self, agentId, msg):
        msg.tracePoint(self, 'sendRequestToGame')
        reactor.callLater(self.delay, self.hub.sendRequestToGame, agentId, msg)

    def gotServerCommand(self, msg):
        msg.tracePoint(self, 'gotServerCommand')
        reactor.callLater(self.delay, self.node.gotServerCommand, msg)

    def gotMessageToAgent(self, agentId, msg):
        msg.tracePoint(self, 'gotMessageToAgent')
        reactor.callLater(
            self.delay, self.node.gotMessageToAgent, agentId, msg)

    def agentDisconnected(self, agentId):
        reactor.callLater(self.delay, self.node.agentDisconnected, agentId)


@run_in_pygame
async def launch_replay(filename):
    replayer = ReplayPlayer(filename)
    game = RemoteGame()

    with initialise_trosnoth_app() as app:
        app.tweener = UIMsgThrottler()

        replayer.connectNode(app.tweener)
        app.tweener.connectNode(game)

        game.connected(replayer.popSettings())
        game_interface = GameInterface(
            app, game, replay=True,
            onDisconnectRequest=app.stop, onConnectionLost=app.stop)
        replayer.start()

        app.interface.elements = [game_interface]
        try:
            await app.runner.run()
        finally:
            replayer.stop()
            game_interface.stop()
