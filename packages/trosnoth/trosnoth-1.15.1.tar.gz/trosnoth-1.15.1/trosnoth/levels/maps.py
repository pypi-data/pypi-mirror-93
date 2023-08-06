from trosnoth.model.map import ZoneLayout, ZoneStep
from trosnoth.triggers.deathmatch import make_small_circles_layout, makeCirclesLayout


class MapAPI:
    name: str

    def build(self, layout_database):
        raise NotImplementedError

    def apply(self, level):
        layout = self.build(level.world.layoutDatabase)
        level.world.setLayout(layout)

    @property
    def code(self):
        return type(self).__name__


class StandardMap(MapAPI):
    name = 'Regulation Standard'

    def build(self, layout_database):
        zones = ZoneLayout.generate(3, 2, 0.95)
        return zones.createMapLayout(layout_database)


class DefaultLobbyMap(MapAPI):
    name = 'Diamond'

    def build(self, layout_database):
        zones = ZoneLayout.generate(2, 1, 0.5)
        return zones.createMapLayout(layout_database)


class SmallMap(MapAPI):
    name = 'Regulation 1v1'

    def build(self, layout_database):
        zones = ZoneLayout.generate(3, 0, 0.95)
        return zones.createMapLayout(layout_database)


class WideMap(MapAPI):
    name = 'Wide'

    def build(self, layout_database):
        zones = ZoneLayout.generate(5, 1, 0.95)
        return zones.createMapLayout(layout_database)


class CorridorMap(MapAPI):
    name = 'Corridor'

    def build(self, layout_database):
        zones = ZoneLayout.generate(5, 0, 0.95)
        return zones.createMapLayout(layout_database)


class LargeMap(MapAPI):
    name = 'Large'

    def build(self, layout_database):
        zones = ZoneLayout.generate(5, 3, 0.95)
        return zones.createMapLayout(layout_database)


class CustomStandardMap(MapAPI):
    name = 'Custom'

    def __init__(self, half_width, height):
        self.half_width = half_width
        self.height = height

    def build(self, layout_database):
        zones = ZoneLayout.generate(self.half_width, self.height, 0.95)
        return zones.createMapLayout(layout_database)


class SmallStackMap(MapAPI):
    name = 'Small Stack'

    def build(self, layout_database):
        zones = ZoneLayout()

        zones.setZoneOwner(zones.firstLocation, 0, dark=True)
        zones.connectZone(zones.firstLocation, ZoneStep.SOUTH, ownerIndex=1, dark=False)

        return zones.createMapLayout(layout_database, autoOwner=False)


class SmallRingMap(MapAPI):
    name = 'Small Ring'

    def build(self, layout_database):
        return make_small_circles_layout(layout_database)


class LargeRingsMap(MapAPI):
    name = 'Large Rings'

    def build(self, layout_database):
        return makeCirclesLayout(layout_database)


class LabyrinthMap(MapAPI):
    name = 'Labyrinth'

    def build(self, layout_database):
        zones = ZoneLayout()

        # Outer ring
        north_spawn_zone = zone = zones.firstLocation
        zone = zones.connectZone(zone, ZoneStep.SOUTHEAST)
        zone = zones.connectZone(zone, ZoneStep.SOUTHEAST)
        east_zone = zone = zones.connectZone(zone, ZoneStep.SOUTH)
        east_spawn_zone = zone = zones.connectZone(zone, ZoneStep.SOUTH)
        zone = zones.connectZone(zone, ZoneStep.SOUTHWEST)
        zone = zones.connectZone(zone, ZoneStep.SOUTHWEST)
        south_west_zone = zone = zones.connectZone(zone, ZoneStep.NORTHWEST)
        west_spawn_zone = zone = zones.connectZone(zone, ZoneStep.NORTHWEST)
        zone = zones.connectZone(zone, ZoneStep.NORTH)
        zone = zones.connectZone(zone, ZoneStep.NORTH)
        north_west_zone = zone = zones.connectZone(zone, ZoneStep.NORTHEAST)
        zone = zones.connectZone(zone, ZoneStep.NORTHEAST)

        # Inner swirl
        zone = zones.connectZone(east_zone, ZoneStep.NORTHWEST)
        zone = zones.connectZone(zone, ZoneStep.NORTHWEST)
        zones.connectZone(zone, ZoneStep.SOUTH, ownerIndex=0, dark=True)
        zone = zones.connectZone(south_west_zone, ZoneStep.NORTHEAST)
        zone = zones.connectZone(zone, ZoneStep.NORTHEAST)
        zones.connectZone(zone, ZoneStep.NORTHWEST)
        zone = zones.connectZone(north_west_zone, ZoneStep.SOUTH)
        zone = zones.connectZone(zone, ZoneStep.SOUTH)
        zones.connectZone(zone, ZoneStep.NORTHEAST)

        # Outer spawn zones
        zones.connectZone(north_spawn_zone, ZoneStep.NORTH, ownerIndex=0, dark=True)
        zones.connectZone(east_spawn_zone, ZoneStep.SOUTHEAST, ownerIndex=0, dark=True)
        zones.connectZone(west_spawn_zone, ZoneStep.SOUTHWEST, ownerIndex=0, dark=True)

        return zones.createMapLayout(layout_database, autoOwner=False)
