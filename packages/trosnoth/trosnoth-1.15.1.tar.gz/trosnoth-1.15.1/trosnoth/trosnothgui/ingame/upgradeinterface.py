import logging
import math

import pygame.gfxdraw
import pygame.surface

from trosnoth.gui.framework.framework import Element
from trosnoth.model.upgrades import Categories
from trosnoth.utils.math import distance

log = logging.getLogger(__name__)


VERTICES_IN_FULL_CIRCLE = 36


class RadialUpgradeMenu(Element):
    def __init__(self, app, detailsInterface):
        super().__init__(app)
        self.app = app
        self.detailsInterface = detailsInterface
        self.surface = pygame.surface.Surface(self.app.screenManager.size, pygame.SRCALPHA)

        self.maxDepth = 1
        self.screenCentre = (
            round(self.app.screenManager.size[0] / 2),
            round(self.app.screenManager.size[1] / 2))
        self.displayRadiusMax = min(self.app.screenManager.size) / 4
        self.displayRadiusMin = self.displayRadiusMax * 0.5
        self.outlineOffset = 0.05
        self.outlineColour = (125, 125, 125, 225)
        self.colours = [(170, 170, 170, 225), (170, 170, 170, 225)]
        self.hvrColour = (255, 255, 100, 225)
        self.degreesInGap = 5

        self.enabled = False
        self.optionIndexes = []
        self.currentSelection = -1
        self.currentOptions = []
        self.polygonCoordinates = []
        self.imageCoordinates = []
        self.degreesPerOption = 0

        self.item_label = ItemLabel(self.app, self.app.fonts.gameMenuFont)

    def start(self):
        self.app.screenManager.onResize.addListener(self.screen_resized)

    def stop(self):
        self.app.screenManager.onResize.removeListener(self.screen_resized)

    def screen_resized(self):
        self.surface = pygame.surface.Surface(self.app.screenManager.size, pygame.SRCALPHA)
        self.screenCentre = (
            round(self.app.screenManager.size[0] / 2),
            round(self.app.screenManager.size[1] / 2))
        self.displayRadiusMax = min(self.app.screenManager.size) / 4
        self.displayRadiusMin = self.displayRadiusMax * 0.5
        self.calculateDisplayCoordinates()

    def toggle(self):
        self.enabled = not self.enabled
        if self.enabled:
            self.optionIndexes.clear()
            self.calculateDisplayCoordinates()

    def get_current_options(self):
        options = list(Categories)
        for index in self.optionIndexes:
            options = options[index].upgrades
        return options

    def calculateDisplayCoordinates(self):
        self.currentOptions = self.get_current_options()
        self.polygonCoordinates.clear()
        self.imageCoordinates.clear()
        options = len(self.currentOptions)
        self.degreesPerOption = 360 / options
        vertexCount = VERTICES_IN_FULL_CIRCLE // options
        degreesOffset = {0: self.degreesInGap * 0.5, vertexCount: -self.degreesInGap * 0.5}
        for optionIndex in range(options):
            self.polygonCoordinates.append([])
            arcCoordinates = []
            for vertexIndex in range(vertexCount + 1):
                offset = degreesOffset.get(vertexIndex, 0)

                arcCoordinates.append(self.getPosition(
                    optionIndex * self.degreesPerOption + offset
                    + vertexIndex * self.degreesPerOption / vertexCount, 1))
            for vertexCoordinate in arcCoordinates:
                self.polygonCoordinates[-1].append((
                    vertexCoordinate[0] * self.displayRadiusMax + self.screenCentre[0],
                    vertexCoordinate[1] * self.displayRadiusMax + self.screenCentre[1]))
            arcCoordinates.reverse()
            for vertexCoordinate in arcCoordinates:
                self.polygonCoordinates[-1].append((
                    vertexCoordinate[0] * self.displayRadiusMin + self.screenCentre[0],
                    vertexCoordinate[1] * self.displayRadiusMin + self.screenCentre[1]))
            imagePosition = self.getPosition(
                (optionIndex + 0.5) * self.degreesPerOption, self.displayRadiusMax * 0.75)
            imagePosition = (
                imagePosition[0] + self.screenCentre[0], imagePosition[1] + self.screenCentre[1])
            self.imageCoordinates.append(imagePosition)
        self.currentSelection = self.selection_from_position(pygame.mouse.get_pos())

    def getPosition(self, angle, magnitude):
        radians = math.radians(angle)
        x = magnitude * math.sin(radians)
        y = -magnitude * math.cos(radians)
        return (x, y)

    def processEvent(self, event):
        if self.enabled:
            if event.type == pygame.MOUSEMOTION:
                self.currentSelection = self.selection_from_position(event.pos)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1 and self.currentSelection != -1:
                    if len(self.optionIndexes) == self.maxDepth:
                        self.detailsInterface._setCurrentUpgrade(
                            self.currentOptions[self.currentSelection])
                        self.toggle()
                    else:
                        self.optionIndexes.append(self.currentSelection)
                        self.calculateDisplayCoordinates()
                    return None
        return event

    def selection_from_position(self, givenPos):
        magnitude = distance(givenPos, self.screenCentre)
        if self.displayRadiusMax > magnitude > self.displayRadiusMin:
            return math.floor(
                math.degrees(math.atan2(
                    givenPos[0] - self.screenCentre[0],
                    -givenPos[1] + self.screenCentre[1])) % 360 / self.degreesPerOption)
        return -1

    def draw(self, screen):
        if self.enabled:
            self.surface.fill((0, 0, 0, 0))
            draw_circle(self.surface, self.outlineColour, self.screenCentre, math.floor(
                self.displayRadiusMax * (1 + self.outlineOffset)))
            draw_circle(self.surface, (0, 0, 0, 0), self.screenCentre, math.floor(
                self.displayRadiusMin * (1 - self.outlineOffset)))
            for optionIndex in range(len(self.polygonCoordinates)):
                colourAdjusted = self.colours[optionIndex % len(self.colours)]
                if self.currentSelection == optionIndex:
                    colourAdjusted = self.hvrColour
                draw_polygon(self.surface, colourAdjusted, self.polygonCoordinates[optionIndex])

                image = self.currentOptions[optionIndex].get_icon(self.app.theme.sprites)
                self.surface.blit(image, (
                    self.imageCoordinates[optionIndex][0] - image.get_rect().size[0] / 2,
                    self.imageCoordinates[optionIndex][1] - image.get_rect().size[1] / 2))
            screen.blit(self.surface, (0, 0))

            if self.currentSelection >= 0:
                self.item_label.set_text(self.currentOptions[self.currentSelection].display_name)
                x, y = pygame.mouse.get_pos()
                self.item_label.blit_to(screen, (x, y + 30))


def draw_circle(surface, colour, centre, radius):
    pygame.gfxdraw.aacircle(surface, *centre, radius, colour)
    pygame.gfxdraw.filled_circle(surface, *centre, radius, colour)


def draw_polygon(surface, colour, points):
    pygame.gfxdraw.aapolygon(surface, points, colour)
    pygame.gfxdraw.filled_polygon(surface, points, colour)


class ItemLabel:
    def __init__(self, app, font, colour=(200, 200, 200), shadow=(50, 50, 50)):
        self.app = app
        self.font = font
        self.colour = colour
        self.shadow = shadow
        self.text = None
        self.main_surface = None
        self.shadow_surface = None

    def set_text(self, text):
        if text == self.text:
            return
        self.text = text
        self.main_surface = self.font.render(self.app, text, True, self.colour)
        self.shadow_surface = self.font.render(self.app, text, True, self.shadow)

    def blit_to(self, screen, position):
        r = self.main_surface.get_rect()
        r.center = position
        x, y = r.topleft
        screen.blit(self.shadow_surface, (x + 2, y + 2))
        screen.blit(self.main_surface, r)
