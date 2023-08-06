# Trosnoth (Ubertweak Platform Game)
# Copyright (C) Joshua D Bartlett
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# version 2 as published by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA
# 02110-1301, USA.
import asyncio
import contextlib
import functools
import logging

import pygame
from PySide2.QtCore import QFile, QObject, Qt
from PySide2.QtGui import QFontDatabase, QWindow, QIcon
from PySide2.QtWidgets import QApplication, QMessageBox
from PySide2.QtUiTools import QUiLoader

from trosnoth import data
from trosnoth.utils.utils import UIScreenRunner
from trosnoth.welcome.aspectwidget import AspectWidget, ScalingPushButton
from trosnoth.welcome.nonqt import ICON_FILE


log = logging.getLogger(__name__)

FONTS_PATH = data.base_path / 'fonts'


def initialise_qt_application():
    QApplication.setQuitOnLastWindowClosed(False)
    QApplication.setApplicationName('Trosnoth')
    QApplication.setStyle('Fusion')

    font_db = QFontDatabase()
    font_db.addApplicationFont(str(FONTS_PATH / 'Junction.ttf'))
    font_db.addApplicationFont(str(FONTS_PATH / 'KLEPTOCR.TTF'))


class QtMessageBoxRunner:
    def __init__(self, message_type, buttons, text, title='', extra_text='', parent_window=None):
        self.msg_box = QMessageBox(message_type, title, text, buttons, parent_window)
        self.msg_box.setInformativeText(extra_text)
        self.runner = UIScreenRunner(self.msg_box.show)
        self.msg_box.finished.connect(run_callback_in_async_loop(self.finished))

    def finished(self, result):
        self.runner.done(self.msg_box.standardButton(self.msg_box.clickedButton()))

    async def run(self):
        self.msg_box.show()
        result = await self.runner.run()
        self.msg_box.hide()
        return result


async def message_box(message_type, buttons, text, title='', extra_text='', parent_window=None):
    return await QtMessageBoxRunner(
        message_type, buttons, text, title, extra_text, parent_window).run()


class CustomLoader(QUiLoader):
    '''
    Loads the .ui file created by Qt Designer, with two additions:

     1. Locates custom widget classes such as AspectWidget,
        ScalingPushButton, and anything specified in custom_widgets.
     2. Installs any event handlers provided in event_filters.
    '''

    def __init__(self, parent=None, *, event_filters=None, custom_widgets=None):
        super().__init__(parent)
        self.widget_classes = {
            'AspectWidget': AspectWidget,
            'ScalingPushButton': ScalingPushButton,
        }
        if custom_widgets:
            self.widget_classes.update(custom_widgets)

        if event_filters is None:
            event_filters = {}
        self.event_filters = {k: EventFilter(v) for k, v in event_filters.items()}
        self.unused_event_filters = set(event_filters)

        # If we don't maintain a reference to the installed event
        # filters, they will be garbage collected and will not apply.
        self.do_not_garbage_collect = set()

    def createWidget(self, class_name, parent=None, name='', *args, **kwargs):
        custom_class = self.widget_classes.get(class_name)
        if custom_class:
            result = custom_class(parent)
            result.setObjectName(name)
        else:
            result = super().createWidget(class_name, parent, name, *args, **kwargs)

        filters = None
        if name:
            filters = self.event_filters.get(name)
            self.unused_event_filters.discard(name)
        if filters is None:
            filters = self.event_filters.get(class_name)
            self.unused_event_filters.discard(class_name)
        if filters:
            result.installEventFilter(filters)
            self.do_not_garbage_collect.add(filters)

        return result

    def load(self, *args, **kwargs):
        result = super().load(*args, **kwargs)
        if self.unused_event_filters:
            raise RuntimeError(
                'Event filters specified but never used for '
                + ', '.join(repr(f) for f in sorted(self.unused_event_filters)))
        result._do_not_garbage_collect = self.do_not_garbage_collect
        return result


class EventFilter(QObject):
    def __init__(self, event_map):
        super().__init__()
        self.event_map = event_map

    def eventFilter(self, obj, event):
        callback = self.event_map.get(event.type())
        if callback:
            return callback(obj, event)
        return False


def load_ui_file(filename, event_filters=None, parent=None):
    ui_file = QFile(str(filename))
    if not ui_file.open(QFile.ReadOnly):
        raise IOError('Could not open UI file')

    try:
        loader = CustomLoader(event_filters=event_filters)
        window = loader.load(ui_file, parentWidget=parent)
    finally:
        ui_file.close()

    if not window:
        raise RuntimeError(loader.errorString())

    window.setWindowIcon(QIcon(str(ICON_FILE)))
    return window


@contextlib.contextmanager
def hide_qt_windows():
    try:
        window_handle = pygame.display.get_wm_info()['window']
    except pygame.error:
        qt_window = None
    else:
        qt_window = QWindow.fromWinId(window_handle) if window_handle else None

    hidden = set()
    if qt_window:
        # By getting Qt to show the Pygame window, we ensure the Pygame
        # window gets the same task bar application name and group as
        # the Qt windows had.
        qt_window.setModality(Qt.WindowModality.ApplicationModal)
        qt_window.show()
    try:
        for toplevel in QApplication.topLevelWidgets():
            if not toplevel.isHidden():
                hidden.add(toplevel)
                toplevel.hide()

        yield
    finally:
        if qt_window:
            qt_window.hide()
        for toplevel in hidden:
            toplevel.show()


class AsyncCallbackManager:
    def __init__(self):
        self.tasks = set()

    def start_coroutine(self, coro):
        task = asyncio.create_task(coro)
        self.tasks.add(task)
        task.add_done_callback(self.task_done)
        return task

    def task_done(self, future):
        self.tasks.remove(future)
        try:
            future.result()
        except asyncio.CancelledError:
            pass
        except Exception:
            log.exception('Exception in async task')

    def cancel_all(self):
        for task in list(self.tasks):
            if not task.done():
                task.cancel()


class HasAsyncCallbacks:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.async_manager = AsyncCallbackManager()


def async_callback(fn):
    @functools.wraps(fn)
    def wrapper(self: HasAsyncCallbacks, *args, **kwargs):
        return self.async_manager.start_coroutine(fn(self, *args, **kwargs))
    return wrapper


def run_callback_in_async_loop(fn, *fixed_args):
    # Sometimes on Windows, Qt events interrupt running code. To fix
    # this, we wrap callbacks in this function.
    try:
        initial_loop = asyncio.get_running_loop()
    except RuntimeError:
        initial_loop = None

    def callback(*args):
        loop = initial_loop or asyncio.get_running_loop()
        loop.call_soon_threadsafe(fn, *(fixed_args + args))

    return callback
