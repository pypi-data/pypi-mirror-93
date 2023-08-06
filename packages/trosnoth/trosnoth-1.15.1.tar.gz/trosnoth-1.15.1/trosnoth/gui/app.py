import asyncio
import functools
import logging
import os
import time
from typing import Tuple, Optional, TypeVar, Awaitable, Callable
try:
    from typing import Protocol
except ImportError:
    from typing_extensions import Protocol

import pygame
import pygame.surface

from trosnoth.gui.sound.soundPlayer import SoundPlayer
from trosnoth.utils.event import Event
from trosnoth.utils.lifespan import LifeSpan
from trosnoth.utils.utils import timeNow, run_async_main_function, UIScreenRunner
from trosnoth.welcome.nonqt import hide_qt_windows, ICON_FILE

log = logging.getLogger(__name__)

TARGET_FRAME_RATE = 60.


class JitterLogger(object):
    def __init__(self, cycle):
        self.cycle = cycle
        self.lastTime = None
        self.thisCount = 0
        self.thisMax = 0
        self.jitter = None

    def noteGap(self):
        '''
        Called to tell the JitterLogger that there is currently a gap,
        so the timing of the next observation should be discarded.
        '''
        self.lastTime = None

    def observation(self, expectedTime, resume=False):
        if resume:
            self.noteGap()

        now = timeNow()
        if self.lastTime:
            value = now - self.lastTime - expectedTime
            self.thisMax = max(self.thisMax, value)
            self.thisCount += 1

            if self.thisCount >= self.cycle:
                self.jitter = self.thisMax
                self.thisCount = 0
                self.thisMax = 0

        self.lastTime = now


class FocusManager:
    def __init__(self):
        self.focused_element = None

    def clear_focus(self):
        self.set_focus(None)

    def set_focus(self, element):
        if self.focused_element is element:
            return
        if self.focused_element:
            previous_focus = self.focused_element
            self.focused_element = None
            previous_focus.hasFocus = False
            previous_focus.lostFocus()

        self.focused_element = element
        if element:
            element.hasFocus = True
            element.gotFocus()


class MultiWindowApplication:
    '''Instantiating the Main class will set up a ui. Calling the run()
    method will run the application.'''

    def __init__(self):
        '''Initialise the application.'''
        from .screenManager import windowManager

        self.focus = FocusManager()
        self._running = False
        self._top_level = None
        self.jitterLogger = JitterLogger(cycle=60)

        self.targetFrameInterval = 1. / TARGET_FRAME_RATE
        self.soundPlayer = SoundPlayer()
        self.screenManager = windowManager.WindowManager(self)
        self.fonts = self.screenManager.fonts

        self.runner = UIScreenRunner(self.start)

    @property
    def interface(self):
        return self.screenManager.interface

    def start(self):
        self.jitterLogger.noteGap()
        self._running = True
        self._top_level = AppTopLevel(self)

    def stop(self):
        if self._running:
            self._top_level.stop()
            if self.runner.running:
                self.runner.done(None)
            self._running = False


class AppTopLevel:
    def __init__(self, app):
        self.app = app
        self.lifespan = LifeSpan()
        pygame_runner = get_pygame_runner()
        pygame_runner.on_pygame_event.addListener(self.process_event, lifespan=self.lifespan)
        pygame_runner.on_tick.addListener(self.tick, lifespan=self.lifespan)
        pygame_runner.on_draw.addListener(self.draw, lifespan=self.lifespan)

    def stop(self):
        self.lifespan.stop()

    def process_event(self, event):
        self.app.screenManager.processEvent(event)

    def tick(self, delta_t):
        self.app.jitterLogger.observation(self.app.targetFrameInterval)
        self.app.screenManager.tick(delta_t)

    def draw(self, screen):
        self.app.screenManager.draw(screen)


class PygameWindowNotOpen(RuntimeError):
    pass


class UserClosedPygameWindow(asyncio.CancelledError):
    pass


class PygameWindowAlreadyOpen(RuntimeError):
    pass


T = TypeVar('T')


class PygameRunnerAPI(Protocol):
    '''
    Defines the methods and attributes of the pygame runner which should
    be used outside of the class itself.
    '''
    on_resize: Event            # ()
    on_tick: Event              # (delta_t)
    on_pygame_event: Event      # (event)
    on_draw: Event              # (surface)

    def is_showing(self) -> bool:
        '''
        :return: true iff a Pygame window is open
        '''
        raise NotImplementedError

    def is_full_screen(self) -> bool:
        '''
        :return: true iff Pygame is running in full screen mode
        '''
        raise NotImplementedError

    def get_window_size(self) -> Tuple[int, int]:
        '''
        :return: the size of the Pygame window
        :raises:
            PygameWindowNotOpen: if no Pygame window is open
        '''
        raise NotImplementedError

    async def show_window(
            self,
            coroutine: Callable[[], Awaitable[T]],
            size: Optional[Tuple[int, int]] = None,
            full_screen: Optional[bool] = None,
            target_frame_rate: float = 60,
            hide_qt: bool = True,
    ) -> T:
        '''
        Shows a Pygame window, and runs an asynchronous Pygame event
        loop until either the given coroutine completes, or the Pygame
        window is closed by the user.

        :param coroutine: This will be called once the Pygame window is
            shown. Once this coroutine completes, the Pygame window will
            be closed. If the Pygame window is closed by the user before
            this coroutine completes, the coroutine will be cancelled.
        :param size: If provided, this specifies the size of the Pygame
            window. If not provided and a Pygame window has been
            previously opened by this Pygame runner, uses the previous
            window size.
        :param full_screen: If provided, controls whether the window
            will be shown in full-screen mode. Note that if full_screen
            is True and size is not a supported full-screen size, a
            suitable size will be automatically chosen.
        :param target_frame_rate: This value controls the length of
            delay between each frame of the event loop. Expressed in
            units of frames per second.
        :param hide_qt: If true, hides all Qt windows until the
            Pygame window is closed.
        :return: the result of coroutine, if it completed.
        :raises:
            UserClosedPygameWindow: if the Pygame window was closed
            WindowAlreadyOpen: if a Pygame window is already open when
                this is called.
        '''
        raise NotImplementedError

    def resize_window(
            self, window_size: Tuple[int, int], full_screen: Optional[bool] = None) -> None:
        '''
        Resizes the currently showing Pygame window.

        :param window_size: The new size of the window.
        :param full_screen: If provided, controls whether the window
            will be shown in full-screen mode. If not provided, the
            current value will be used.
        :raises:
            PygameWindowNotOpen: if the Pygame window is not open
        '''
        raise NotImplementedError

    def launch_application(
            self,
            coroutine: Callable[[], Awaitable[T]],
            *,
            size: Tuple[int, int],
            full_screen: bool,
            target_frame_rate: float = 60,
    ) -> T:
        '''
        Shows a Pygame window, and synchronously runs the Pygame event
        loop until either the given coroutine completes, or the Pygame
        window is closed by the user.

        :param coroutine: this will be called once the Pygame window is
            shown. Once this coroutine completes, the Pygame window will
            be closed. If the Pygame window is closed by the user before
            this coroutine completes, the coroutine will be cancelled.
        :param size: the size of the Pygame window.
        :param full_screen: controls whether the window will be shown in
            full-screen mode. Note that if full_screen is true and size
            is not a supported full-screen size, a suitable size will be
            automatically chosen.
        :param target_frame_rate: This value controls the length of
            delay between each frame of the event loop. Expressed in
            units of frames per second.
        :return: the result of coroutine, if it completed.
        :raises:
            UserClosedPygameWindow: if the Pygame window was closed
            WindowAlreadyOpen: if a Pygame window is already open when
                this is called.
        '''
        raise NotImplementedError


class PygameRunner(PygameRunnerAPI):
    instance = None

    def __init__(self):
        self.full_screen_requested = False
        self.last_screen_size = (800, 600)
        self.on_resize = Event([])
        self.on_tick = Event(['delta_t'])
        self.on_pygame_event = Event(['event'])
        self.on_draw = Event(['surface'])
        pygame.init()
        pygame.display.init()

    def is_showing(self) -> bool:
        return bool(pygame.display.get_surface())

    def is_full_screen(self) -> bool:
        if not self.is_showing():
            return False
        return self.full_screen_requested

    def get_window_size(self) -> Tuple[int, int]:
        surface = pygame.display.get_surface()
        if not surface:
            raise PygameWindowNotOpen('No Pygame window currently open')
        return surface.get_size()

    def resize_window(
            self, window_size: Tuple[int, int], full_screen: Optional[bool] = None) -> None:
        if not self.is_showing():
            raise PygameWindowNotOpen('No pygame window currently open')
        if full_screen is None:
            full_screen = self.full_screen_requested
        self.set_display_mode(window_size, full_screen)
        self.on_resize()

    def set_display_mode(self, size, full_screen):
        self.last_screen_size = size
        self.full_screen_requested = full_screen

        if full_screen:
            flags = pygame.FULLSCREEN | pygame.DOUBLEBUF | pygame.HWSURFACE
        else:
            flags = pygame.RESIZABLE

        pygame.display.init()
        self.set_default_icon()
        return pygame.display.set_mode(size, flags)

    def set_default_icon(self):
        icon = pygame.image.load(str(ICON_FILE))
        if os.name == 'nt':
            # On Windows, icon transparency does not work unless the
            # icon is an approved Windows icon size.
            icon = pygame.transform.smoothscale(icon, (96, 96))
        pygame.display.set_icon(icon)

    async def show_window(
            self, coroutine: Callable[[], Awaitable[T]], size: Optional[Tuple[int, int]] = None,
            full_screen: Optional[bool] = None, target_frame_rate: float = 60,
            hide_qt: bool = True) -> T:

        if self.is_showing():
            raise PygameWindowAlreadyOpen('Pygame window is already showing')

        if size is None:
            size = self.last_screen_size
        if full_screen is None:
            full_screen = self.full_screen_requested
        screen = self.set_display_mode(size, full_screen)

        try:
            if hide_qt:
                with hide_qt_windows():
                    return await self._run_body(coroutine, screen, target_frame_rate)
            else:
                return await self._run_body(coroutine, screen, target_frame_rate)
        finally:
            pygame.display.quit()

    async def _run_body(self, coroutine, screen, target_frame_rate):
        task_from_caller = asyncio.create_task(coroutine())
        event_loop_task = asyncio.create_task(
            self.pygame_event_loop(screen, 1 / target_frame_rate))

        done, pending = await asyncio.wait(
            [task_from_caller, event_loop_task],
            return_when=asyncio.FIRST_COMPLETED)

        for task in pending:
            task.cancel()

        if task_from_caller in done:
            return task_from_caller.result()

        raise UserClosedPygameWindow('The user closed the Pygame window')

    async def pygame_event_loop(self, screen, target_frame_interval):
        last_time = time.monotonic()

        while True:
            now = time.monotonic()
            for event in pygame.event.get():
                try:
                    self.on_pygame_event(event)
                except Exception:
                    log.exception('Error during Pygame event processing')

                if event.type == pygame.QUIT:
                    return
                if event.type == pygame.VIDEORESIZE:
                    self.resize_window(event.size)

            try:
                self.on_tick(now - last_time)
            except Exception:
                log.exception('Error in tick() method')
            last_time = now

            if pygame.display.get_active():
                try:
                    self.on_draw(screen)
                except pygame.error:
                    log.exception('Error in draw()')

                pygame.display.flip()

            processing_time = time.monotonic() - now
            await asyncio.sleep(max(0.001, target_frame_interval - processing_time))

    def launch_application(
            self, coroutine: Callable[[], Awaitable[T]], *,
            size: Tuple[int, int], full_screen: bool, target_frame_rate: float = 60) -> T:
        pygame.init()
        pygame.display.init()
        try:
            return run_async_main_function(functools.partial(
                self.show_window, coroutine, size=size, full_screen=full_screen,
                target_frame_rate=target_frame_rate, hide_qt=False))
        finally:
            pygame.quit()


def get_pygame_runner() -> PygameRunnerAPI:
    '''
    :return: the global pygame runner which can be used to query or
        control the open Pygame window.
    '''
    if PygameRunner.instance is None:
        PygameRunner.instance = PygameRunner()
    return PygameRunner.instance
