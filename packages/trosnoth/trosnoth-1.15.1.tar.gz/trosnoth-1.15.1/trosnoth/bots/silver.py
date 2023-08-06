if __name__ == '__main__':
    import os
    import sys
    sys.path.insert(0, os.path.join(
        os.path.abspath(os.path.dirname(__file__)), '..', '..'))

    # Install the asyncio reactor as early as possible
    from trosnoth.qtreactor import declare_this_module_requires_qt_reactor
    declare_this_module_requires_qt_reactor()


import enum
import logging
import math
import random

from trosnoth.bots.goalsetter import GoalSetterBot, Goal, ZoneMixin
from trosnoth.bots import ranger
from trosnoth.const import (
    BOT_GOAL_CAPTURE_MAP, BOT_GOAL_SCORE_TROSBALL_POINT, BOT_GOAL_HUNT_RABBITS,
    BOT_GOAL_KILL_THINGS,
)
from trosnoth.messages import AimPlayerAtMsg
from trosnoth.model import upgrades
from trosnoth.model.shot import PredictedGrenadeTrajectory, GRENADE_BLAST_RADIUS
from trosnoth.utils.math import distance

log = logging.getLogger(__name__)


class DecideBetweenSilverOrRangerAlgorithm(Goal):
    '''
    If this is not a regular Trosnoth match, fall back to RangerBot
    algorithm.
    '''
    def __eq__(self, other):
        if type(self) != type(other):
            return False
        return (self.bot, self.parent) == (other.bot, other.parent)

    def __hash__(self):
        return hash(type(self))

    def start(self):
        self.bot.player.onRemovedFromGame.addListener(self.removed_from_game)
        self.bot.agent.localState.onGameInfoChanged.addListener(self.reevaluate)

    def stop(self):
        super().stop()
        self.bot.agent.localState.onGameInfoChanged.removeListener(self.reevaluate)
        self.bot.player.onRemovedFromGame.removeListener(self.removed_from_game)

    def removed_from_game(self, playerId):
        self.returnToParent()

    def reevaluate(self):
        self.bot.setUpgradePolicy(None)
        bot_goal = self.bot.agent.localState.botGoal
        if bot_goal == BOT_GOAL_CAPTURE_MAP:
            self.setSubGoal(WinSoloTrosnothGame(self.bot, self))
        elif bot_goal == BOT_GOAL_SCORE_TROSBALL_POINT:
            self.setSubGoal(ranger.ScoreTrosballPoint(self.bot, self))
        elif bot_goal == BOT_GOAL_HUNT_RABBITS:
            self.setSubGoal(ranger.HuntTheRabbits(self.bot, self))
        elif bot_goal == BOT_GOAL_KILL_THINGS:
            self.setSubGoal(ranger.HuntEnemies(self.bot, self))
        else:
            self.setSubGoal(ranger.RunAroundKillingHumans(self.bot, self))


class Location(enum.Enum):
    FRONT_LINE = 1
    NEAR_FRONT_LINE = 2
    FAR_AWAY = 3


class UpgradeSelector:
    def __init__(self, bot):
        self.bot = bot
        self.choice = None
        self.use_function = {
            upgrades.Grenade: self.use_grenade,
        }

    def make_decision(self):
        player = self.bot.player
        choices = [upgrades.Grenade]
        if not player.items.has(upgrades.Shield):
            choices.append(upgrades.Shield)
        if not player.team.usingMinimapDisruption:
            choices.append(upgrades.MinimapDisruption)
        if not (player.shoxwave or player.machineGunner or player.hasRicochet):
            choices.extend([upgrades.MachineGun, upgrades.Ricochet])
        if not player.ninja:
            choices.append(upgrades.Ninja)

        self.choice = random.choice(choices)
        cost = upgrades.Bomber.requiredCoins + self.choice.requiredCoins

        self.bot.set_upgrade_callback(cost, self.upgrade_available, delay=0.5)

    def upgrade_available(self):
        # This method is called every tick until it's no longer
        # available.
        self.use_function.get(self.choice, self.use_upgrade)()

    def use_upgrade(self):
        self.bot.buy_upgrade(self.choice)
        self.make_decision()

    def use_grenade(self):
        player = self.bot.player
        trajectory = PredictedGrenadeTrajectory(
            self.bot.world, player, upgrades.Grenade.totalTimeLimit)

        best_angle = None
        max_enemies_hit = 0
        for i in range(5):
            angle = random.random() * 2 * math.pi
            self.bot.sendRequest(AimPlayerAtMsg(angle, 1, self.bot.world.lastTickId))
            final_pos = list(trajectory.predictedTrajectoryPoints())[-1]
            enemies_hit = len([
                p for p in self.bot.world.players
                if not (p.dead or player.isFriendsWith(p))
                and distance(p.pos, player.pos) < GRENADE_BLAST_RADIUS])
            if enemies_hit > max_enemies_hit:
                max_enemies_hit = enemies_hit
                best_angle = angle

        if best_angle is not None:
            self.bot.sendRequest(AimPlayerAtMsg(best_angle, 1, self.bot.world.lastTickId))
            self.use_upgrade()


class WinSoloTrosnothGame(Goal):
    '''
    The aim of SilverBot is to win a 1v1 Trosnoth game on a map that's
    only one zone high at all points.
    '''

    def __init__(self, bot, parent):
        super().__init__(bot, parent)
        self.zone_live_player_counts = []
        self.zone_ownerships = []
        self.dead = False
        self.upgrade_selector = UpgradeSelector(bot)

    def __eq__(self, other):
        if type(self) != type(other):
            return False
        return (self.bot, self.parent) == (other.bot, other.parent)

    def __hash__(self):
        return hash(type(self))

    def start(self):
        self.dead = self.bot.player.dead
        self.upgrade_selector.make_decision()
        self.bot.onTick.addListener(self.tick)
        self.bot.onOrderFinished.addListener(self.reevaluate)
        super().start()

    def stop(self):
        super().stop()
        self.bot.onTick.removeListener(self.tick)
        self.bot.onOrderFinished.removeListener(self.reevaluate)

    def tick(self):
        # Whenever any player except me changes zones, or a zone changes
        # hands,or I die or respawn, reevaluate what I'm doing
        player_counts = []
        zone_ownerships = []
        for zone in self.bot.zone_order:
            zone_ownerships.append(zone.owner)
            count = {}
            player_counts.append(count)
            for player in zone.players:
                if not player.dead and player.id != self.bot.player.id:
                    count[player.team] = count.get(player.team, 0) + 1

        if (
                player_counts != self.zone_live_player_counts
                or self.bot.player.dead != self.dead
                or zone_ownerships != self.zone_ownerships):

            if self.dead and not self.bot.player.dead:
                self.upgrade_selector.make_decision()

            self.zone_live_player_counts = player_counts
            self.dead = self.bot.player.dead
            self.zone_ownerships = zone_ownerships
            self.reevaluate()

    def reevaluate(self):
        '''
        Decide whether to stay in the current zone, or move to another.
        '''

        player = self.bot.player

        # 1. If we're dead, respawn
        if player.dead:
            self.setSubGoal(RespawnInBestZone(self.bot, self))
            return

        # # 2. If we're bombing, let it run its course
        # if self.subGoal and isinstance(self.subGoal, Explode):
        #     return

        my_zone = player.getZone()

        # 2. If we're alive but outside the map, move towards the
        # nearest zone.
        if not my_zone:
            self.setSubGoal(MoveIntoMap(self.bot, self))
            return

        if my_zone.owner == player.team:
            location = self.evaluate_friendly_location(my_zone)
            if location == Location.FRONT_LINE:
                if friendly_zone_is_threatened(
                        player.team, my_zone, i_am_there=True, sub_player=player):
                    self.setSubGoal(EngageWithEnemiesInZones(self.bot, self, {my_zone}))
                else:
                    self.setSubGoal(AdvanceToCapturableZone(self.bot, self))
            elif location == Location.NEAR_FRONT_LINE:
                self.setSubGoal(AdvanceToFrontLine(self.bot, self))
            else:
                self.setSubGoal(Explode(self.bot, self))
        else:
            location, friendly_neighbours = self.evaluate_unfriendly_location(my_zone)
            if location == Location.FAR_AWAY:
                self.setSubGoal(Explode(self.bot, self))
            else:
                focus_zones = {my_zone}
                if friendly_neighbours:
                    zone_to_defend = min(
                        friendly_neighbours, key=lambda n: distance(n.defn.pos, player.pos))
                    focus_zones.add(zone_to_defend)
                else:
                    zone_to_defend = None

                if zone_to_defend and friendly_zone_is_threatened(
                        player.team, zone_to_defend, sub_player=player):
                    if not my_zone.isCapturableBy(player.team, sub_player=player):
                        # Just head back and defend as there's no point trying to capture
                        self.setSubGoal(MoveToZone(self.bot, self, zone_to_defend, sprint=True))
                    elif not self.will_returning_help(zone_to_defend):
                        # Just try to capture as there's no point trying to defend
                        self.setSubGoal(CaptureCurrentZone(self.bot, self, sprint=True))
                    elif self.estimate_ticks_to_zone(zone_to_defend) \
                            <= self.estimate_ticks_to_orb():
                        self.setSubGoal(MoveToZone(self.bot, self, zone_to_defend, sprint=True))
                    else:
                        self.setSubGoal(CaptureCurrentZone(self.bot, self, sprint=True))
                elif my_zone.isCapturableBy(player.team, sub_player=player):
                    self.setSubGoal(CaptureCurrentZone(self.bot, self))
                else:
                    self.setSubGoal(EngageWithEnemiesInZones(self.bot, self, focus_zones))

    def will_returning_help(self, zone):
        '''
        :param zone: a threatened zone that this player is not in
        :return: true iff adding this player to the zone would stop it
            from being capturable.
        '''
        player_counts = zone.getPlayerCounts(sub_player=self.bot.player)
        if not player_counts:
            # Zone is not actually threatened
            return False

        my_team = self.bot.player.team
        count, teams = player_counts.pop(0)
        if my_team in teams:
            # Zone is not actually threatened
            return False

        if not player_counts:
            # Zone has enemies and no friendlies
            return count == 1

        count2, teams2 = player_counts.pop(0)
        if count - count2 > 1:
            # One player won't make a difference
            return False

        return my_team in teams2

    def evaluate_friendly_location(self, zone):
        my_team = self.bot.player.team
        seen = {zone}
        neighbours = set()
        for neighbour in zone.getUnblockedNeighbours():
            if neighbour.owner not in (my_team, None):
                return Location.FRONT_LINE
            neighbours.add(neighbour)
            seen.add(neighbour)

        for neighbour in neighbours:
            for next_zone in neighbour.getUnblockedNeighbours():
                if next_zone in seen:
                    continue
                seen.add(next_zone)
                if next_zone.owner not in (my_team, None):
                    return Location.NEAR_FRONT_LINE

        return Location.FAR_AWAY

    def evaluate_unfriendly_location(self, zone):
        my_team = self.bot.player.team
        if not zone.adjacentToAnotherZoneOwnedBy(my_team):
            return Location.FAR_AWAY, set()

        friendly_neighbours = {
            neighbour for neighbour in zone.getUnblockedNeighbours() if neighbour.owner == my_team}
        return Location.FRONT_LINE, friendly_neighbours

    def estimate_ticks_to_zone(self, zone):
        route = self.bot.create_hypothetical_route()
        if route.end is None:
            # We won't know exactly where we are until we land
            return 500
        if not route.attemptPathToOrb(zone.defn):
            # Can't find path
            return 10000
        result = 0
        for step in route.steps:
            result += step.get_estimated_ticks()
            if self.bot.world.map.getZoneAtPoint(step.end.pos) == zone:
                break
        return result

    def estimate_ticks_to_orb(self):
        route = self.bot.create_hypothetical_route()
        if route.end is None:
            # We won't know exactly where we are until we land
            return 500
        if not route.attemptPathToOrb(self.bot.player.getZone().defn):
            # Can't find path
            return 10000
        return sum(step.get_estimated_ticks() for step in route.steps)


def friendly_zone_is_threatened(my_team, zone, i_am_there=False, sub_player=None):
    '''
    :param my_team: the team of this bot
    :param zone: a zone
    :param i_am_there: true if I am already there
    :param sub_player: see sub_player docs in DynamicZoneLogic.getCountedPlayersByTeam
    :return: true iff I need to be in this zone to stop it being
             capturable
    '''
    player_counts = zone.getPlayerCounts(sub_player=sub_player)
    if not player_counts:
        # No players in the zone
        return False

    count, teams = player_counts[0]
    teams = set(teams)
    if teams == {my_team}:
        # My team has strictly more players than any other team
        return False
    if my_team in teams and not i_am_there:
        # My team has just enough defenders without me
        return False

    # I am needed
    return True


class RespawnInBestZone(Goal):
    def __eq__(self, other):
        if type(self) != type(other):
            return False
        return (self.bot, self.parent) == (other.bot, other.parent)

    def __hash__(self):
        return hash(type(self))

    def start(self):
        self.bot.world.onZoneTagged.addListener(self.zone_tagged)
        self.bot.player.onRespawned.addListener(self.reevaluate)
        super().start()

    def stop(self):
        self.bot.world.onZoneTagged.removeListener(self.zone_tagged)
        self.bot.player.onRespawned.removeListener(self.reevaluate)
        super().stop()

    def zone_tagged(self, *args, **kwargs):
        self.reevaluate()

    def reevaluate(self):
        player = self.bot.player
        if not player.dead:
            self.returnToParent()
            return

        good_zones = [
            zone for zone in self.bot.world.zones
            if player.isZoneRespawnable(zone)
            and any(
                not player.isZoneRespawnable(neighbour)
                for neighbour in zone.getUnblockedNeighbours())]

        if not good_zones:
            self.returnToParent()
            return

        best_zone = min(good_zones, key=lambda zone: distance(zone.defn.pos, player.pos))
        self.bot.respawn(zone=best_zone)


class MoveIntoMap(Goal):
    def __eq__(self, other):
        if type(self) != type(other):
            return False
        return (self.bot, self.parent) == (other.bot, other.parent)

    def __hash__(self):
        return hash(type(self))

    def start(self):
        self.bot.onOrderFinished.addListener(self.order_finished)
        self.bot.onTick.addListener(self.tick)
        super().start()

    def stop(self):
        super().stop()
        self.bot.onOrderFinished.removeListener(self.order_finished)
        self.bot.onTick.removeListener(self.tick)

    def order_finished(self):
        self.returnToParent()

    def tick(self):
        if self.bot.player.getZone():
            self.returnToParent()

    def reevaluate(self):
        target = min(self.bot.world.zones, key=lambda z: distance(z.defn.pos, self.bot.player.pos))
        self.bot.moveToZone(target)


class Explode(Goal):
    def __eq__(self, other):
        if type(self) != type(other):
            return False
        return (self.bot, self.parent) == (other.bot, other.parent)

    def __hash__(self):
        return hash(type(self))

    def start(self):
        self.bot.onTick.addListener(self.tick)
        super().start()

    def stop(self):
        super().stop()
        self.bot.onTick.removeListener(self.tick)

    def reevaluate(self):
        if self.bot.player.dead:
            self.returnToParent()
            return

        if not self.bot.player.bomber:
            self.bot.standStill()
            self.bot.buy_upgrade(upgrades.Bomber)

    def tick(self):
        if self.bot.player.dead:
            self.returnToParent()


class CaptureCurrentZone(Goal):
    '''
    Captures the zone the bot is currently in. Assumes that the parent
    goal already has triggers in place that will notice when the zone
    changes hands or the bot dies.
    '''

    def __init__(self, bot, parent, sprint=False):
        super().__init__(bot, parent)
        self.sprint = sprint

    def __eq__(self, other):
        if type(self) != type(other):
            return False
        return (self.bot, self.parent, self.sprint) == (other.bot, other.parent, other.sprint)

    def __hash__(self):
        return hash((type(self), self.sprint))

    def reevaluate(self):
        self.bot.moveToOrb(self.bot.player.getZone(), sprint=self.sprint)


class AdvanceToCapturableZone(Goal):
    '''
    Selects a neighbour of the bot's current zone which is not owned by
    the bot's team and moves to it. Gives preference to zones which are
    owned by enemy teams over neutral zones.
    '''

    def __eq__(self, other):
        if type(self) != type(other):
            return False
        return (self.bot, self.parent) == (other.bot, other.parent)

    def __hash__(self):
        return hash(type(self))

    def start(self):
        self.bot.onOrderFinished.addListener(self.order_finished)
        super().start()

    def stop(self):
        super().stop()
        self.bot.onOrderFinished.removeListener(self.order_finished)

    def order_finished(self):
        self.returnToParent()

    def reevaluate(self):
        my_zone = self.bot.player.getZone()
        my_team = self.bot.player.team
        enemy_neighbours = []
        neutral_neighbours = []
        for neighbour in my_zone.getUnblockedNeighbours():
            if neighbour.owner is None:
                neutral_neighbours.append(neighbour)
            elif neighbour.owner != my_team:
                enemy_neighbours.append(neighbour)

        if enemy_neighbours:
            target_zone = random.choice(enemy_neighbours)
        else:
            target_zone = random.choice(neutral_neighbours)

        self.bot.moveToZone(target_zone)


class AdvanceToFrontLine(Goal):
    '''
    Selects a neighbour of the bot's current zone which is on the front
    line. That is, it is not owned by an enemy team, but is adjacent to
    a zone which is. Gives preference to zones which are contested.
    '''

    def __eq__(self, other):
        if type(self) != type(other):
            return False
        return (self.bot, self.parent) == (other.bot, other.parent)

    def __hash__(self):
        return hash(type(self))

    def start(self):
        self.bot.onOrderFinished.addListener(self.order_finished)
        super().start()

    def stop(self):
        super().stop()
        self.bot.onOrderFinished.removeListener(self.order_finished)

    def order_finished(self):
        self.returnToParent()

    def reevaluate(self):
        my_zone = self.bot.player.getZone()
        my_team = self.bot.player.team

        candidates = [
            neighbour for neighbour in my_zone.getUnblockedNeighbours()
            if neighbour.owner in (my_team, None) and any(
                next_zone.owner not in (my_team, None)
                for next_zone in neighbour.getUnblockedNeighbours()
            )]

        contested = [
            z for z in candidates
            if friendly_zone_is_threatened(my_team, z, sub_player=self.bot.player)]
        if contested:
            target_zone = random.choice(contested)
        else:
            target_zone = random.choice(candidates)

        self.bot.moveToZone(target_zone)


class MoveToZone(ZoneMixin, Goal):
    '''
    Moves to the given zone.
    '''

    def __init__(self, bot, parent, zone, sprint=False):
        super().__init__(bot, parent)
        self.zone = zone
        self.sprint = sprint

    def start(self):
        self.bot.onOrderFinished.addListener(self.order_finished)
        super().start()

    def stop(self):
        super().stop()
        self.bot.onOrderFinished.removeListener(self.order_finished)

    def order_finished(self):
        self.returnToParent()

    def reevaluate(self):
        self.bot.moveToZone(self.zone, sprint=self.sprint)


class EngageWithEnemiesInZones(Goal):
    '''
    Tries to kill enemies without leaving the specified zones. Assumes
    that the parent goal has triggers to notice when the player dies
    or succeeds in killing enough enemies.
    '''

    def __init__(self, bot, parent, zones):
        super().__init__(bot, parent)
        self.zones = frozenset(zones)
        self.bot_zone = bot.player.getZone()
        self.avoiding = False

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        return (other.bot, other.parent, other.zones, other.bot_zone) \
            == (self.bot, self.parent, self.zones, self.bot_zone)

    def __hash__(self):
        return hash((self.zones, self.bot_zone))

    def start(self):
        self.bot.onTick.addListener(self.tick)
        super().start()

    def stop(self):
        super().stop()
        self.bot.onTick.removeListener(self.tick)

    def tick(self):
        if self.bot.player.reloadTime > 0:
            if not self.avoiding:
                self.reevaluate()
        elif self.avoiding:
            self.reevaluate()

    def reevaluate(self):
        zone = self.bot.player.getZone()
        if zone not in self.zones:
            self.returnToParent()
            return

        if self.bot.player.reloadTime > 0:
            self.avoiding = True
            self.setSubGoal(AvoidEnemiesInZones(self.bot, self, self.zones))
        else:
            target = self.select_enemy()
            if not target:
                self.returnToParent()
                return
            self.avoiding = False
            self.setSubGoal(MoveTowardsEnemy(self.bot, self, target))

    def select_enemy(self):
        enemies = [
            p for p in self.bot_zone.players
            if not p.dead and not p.isFriendsWith(self.bot.player)]

        if not enemies:
            # No enemies left in this bot's starting zone. Expand search
            # to all allowed zones.
            enemies = [
                p for p in self.bot.world.players
                if not p.dead and p.getZone() in self.zones
                and not p.isFriendsWith(self.bot.player)]
            if not enemies:
                return None

        target = min(
            enemies, key=lambda p: distance(p.pos, self.bot.player.pos))
        return target


class MoveTowardsEnemy(Goal):
    '''
    Moves towards the given player. Assumes that the parent goal has
    triggers to check when either player dies.
    '''

    def __init__(self, bot, parent, enemy):
        super().__init__(bot, parent)
        self.target = enemy

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        return (other.bot, other.parent, other.target) == (self.bot, self.parent, self.target)

    def __hash__(self):
        return hash(self.target)

    def reevaluate(self):
        self.bot.attackPlayer(self.target)


class AvoidEnemiesInZones(Goal):
    '''
    Moves around, trying to avoid being within firing range of enemies,
    while staying in the given zones.
    '''

    def __init__(self, bot, parent, zones):
        super().__init__(bot, parent)
        self.zones = frozenset(zones)

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        return (other.bot, other.parent, other.zones) == (self.bot, self.parent, self.zones)

    def __hash__(self):
        return hash(self.zones)

    def start(self):
        self.bot.onTick.addListener(self.tick)
        self.bot.standStill()
        super().start()

    def stop(self):
        super().stop()
        self.bot.onTick.removeListener(self.tick)

    def tick(self):
        if self.bot.player.dead:
            self.returnToParent()
            return

        if not self.bot.hasUnfinishedRoute():
            self.reevaluate()

    def reevaluate(self):
        if self.bot.hasUnfinishedRoute():
            return

        zone = self.bot.player.getZone()
        if zone not in self.zones:
            self.returnToParent()
            return

        path_finder = self.bot.world.map.layout.pathFinder

        # Limit to actions that stay in the zones
        routes = [
            r for r in path_finder.getPossibleActions(self.bot.player)
            if r.finishPoint and self.bot.world.map.getZoneAtPoint(r.finishPoint) in self.zones]

        if not routes:
            self.returnToParent()
            return

        # The best route is the route that ends where the fewest number
        # of enemies can shoot this bot, and which is furthest from the
        # nearest enemy.
        best_route = None
        best_route_key = None
        for route in routes:
            enemies_in_view = 0
            nearest_enemy_distance = None
            for player in self.bot.world.players:
                if player.dead or self.bot.player.isFriendsWith(player):
                    continue
                if self.bot.canHitPlayer(player):
                    enemies_in_view += 1
                    enemy_distance = distance(player.pos, self.bot.player.pos)
                    if nearest_enemy_distance is None or enemy_distance < nearest_enemy_distance:
                        nearest_enemy_distance = enemy_distance

            route_key = (enemies_in_view, nearest_enemy_distance)
            if best_route is None or route_key < best_route_key:
                best_route = route
                best_route_key = route_key

        # Make sure there's no other order that might be competing
        self.bot.standStill()
        self.bot.setRoute(best_route)


class SilverBot(GoalSetterBot):
    nick = 'SilverBot'
    generic = True

    MainGoalClass = DecideBetweenSilverOrRangerAlgorithm

    def __init__(self, *args, **kwargs):
        self.zone_order = []
        super().__init__(*args, **kwargs)

    def worldReset(self):
        super().worldReset()
        self.recalculate_zone_order()

    def start(self):
        self.recalculate_zone_order()
        super().start()

    def recalculate_zone_order(self):
        self.zone_order = list(self.world.zones)


BotClass = SilverBot


if __name__ == '__main__':
    from trosnoth.levels.base import play_level, LevelOptions
    from trosnoth.levels.standard import StandardRandomLevel
    level = StandardRandomLevel(level_options=LevelOptions(map_index=1))
    level.countdown_time = 2

    play_level(level, bot_count=1, bot_class='silver')

    # from trosnoth.levels.base import run_bot_match
    # run_bot_match(level, 'silver', 'ranger', team_size=1)
