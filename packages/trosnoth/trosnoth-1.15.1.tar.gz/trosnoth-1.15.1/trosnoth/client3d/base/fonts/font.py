import logging
from pathlib import Path

from direct.gui.OnscreenText import OnscreenText

from trosnoth.data import get_overridable_path

log = logging.getLogger(__name__)

PANDA_SCALE = 400.


class Font(object):
    def __init__(self, name, size, bold = False):
        self._name = name
        self._size = size
        self._bold = bold
        self._filename = None
        self.pandaFont = None

    def _initFilename(self, app):
        if self._filename is None:
            self._filename = str(get_overridable_path(Path('fonts') / self._name))
            self.pandaFont = app.panda.loader.loadFont(self._filename)
        else:
            filename = self._filename
        return filename

    def __repr__(self):
        return 'Font: %s size %d' % (self._name, self._size)

    def getPandaFont(self, app):
        if self.pandaFont is None:
            filename = self._initFilename(app)
        return self.pandaFont

    def getPandaScale(self, scale=1):
        return scale * self._size / PANDA_SCALE

    def makeOnscreenText(self, app, text, scale=1, **kwargs):
        '''
        Creates a panda3d OnscreenText object with the given arguments.
        '''
        font = self.getPandaFont(app)
        scale = self.getPandaScale(scale)
        return OnscreenText(
            font=font, text=text, scale=scale, **kwargs)

    def getPandaLineHeight(self, app, scale=1):
        height = self.getPandaFont(app).getLineHeight()
        return height * self.getPandaScale(scale)
