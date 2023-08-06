'''upgrades.py - defines the behaviour of upgrades.'''

import logging
from enum import Enum

import pygame

from trosnoth.model.shot import GrenadeShot

log = logging.getLogger(__name__)

upgradeOfType = {}
allUpgrades = set()


class Categories(Enum):
    ITEM = ('Items', 'category-item.png')
    WEAPON = ('Guns', 'category-weapon.png')

    def __init__(self, name, icon_filename):
        self.display_name = name
        self.icon_filename = icon_filename
        self.upgrades = []

    def get_icon(self, sprites):
        return sprites.categoryImage(self.icon_filename)


def registerUpgrade(upgradeClass):
    '''
    Marks the given upgrade class to be used in the game.
    '''
    recordUpgradeClassString(upgradeClass)
    allUpgrades.add(upgradeClass)
    upgradeClass.category.upgrades.append(upgradeClass)

    return upgradeClass


def specialUpgrade(upgradeClass):
    '''
    Marks the given upgrade class as a special upgrade that can be used only
    via the console.
    '''
    recordUpgradeClassString(upgradeClass)
    return upgradeClass


def recordUpgradeClassString(upgradeClass):
    '''
    Records the type string of the given upgrade class for use in network
    communication.
    '''
    if upgradeClass.upgradeType in upgradeOfType:
        raise KeyError('2 upgrades with %r' % (upgradeClass.upgradeType,))
    upgradeOfType[upgradeClass.upgradeType] = upgradeClass


class ItemManager(object):
    '''
    Keeps track of which items are currently active for a given player.
    '''

    def __init__(self, player):
        self.player = player
        self.world = player.world
        self.active = {}

        # Only used server-side. Set of upgrade classes for which the server
        # has sent UpgradeApprovedMsg, but has not yet received
        # PlayerHasUpgradeMsg from the client.
        self.serverApproved = set()

    def dump(self):
        return [item.dump() for item in list(self.active.values())]

    def restore(self, data):
        self.clear()

        for itemData in data:
            itemClass = self.world.getUpgradeType(itemData['kind'])
            self.active[itemClass] = itemClass.restore(self.player, itemData)

    def get(self, upgradeKind):
        '''
        :param upgradeKind: A subclass of :class Upgrade:
        :return: An instance of the given subclass, if this player has an
            active item of that type, else None.
        '''
        return self.active.get(upgradeKind)

    def has(self, upgradeKind):
        '''
        :param upgradeKind: A subclass of :class Upgrade:
        :return: True iff this player has an active item of the given type.
        '''
        return upgradeKind in self.active

    def hasAny(self):
        return bool(self.active)

    def activate(self, upgradeKind, local):
        item = self.get(upgradeKind)
        if not item:
            self.active[upgradeKind] = item = upgradeKind(self.player)
        self.serverApproved.discard(upgradeKind)

        if local:
            if item.doNotWaitForServer:
                local.addUnverifiedItem(item)
            item.localUse(local)
        else:
            item.use()
        self.player.onUsedUpgrade(item)
        return item

    def clear(self):
        '''
        Clears the player's upgrades, performing any finalisation needed.
        '''
        for item in list(self.active.values()):
            item.delete()

        self.active = {}
        self.serverApproved = set()

    def delete(self, activeItem):
        '''
        Deletes the item, assuming that the item's tear-down has already
        been done.
        '''
        upgradeKind = activeItem.__class__
        if self.get(upgradeKind) == activeItem:
            del self.active[upgradeKind]

    def server_approve(self, upgradeKind):
        assert self.world.isServer
        self.serverApproved.add(upgradeKind)

    def server_isApproved(self, upgradeKind):
        assert self.world.isServer
        return upgradeKind in self.serverApproved

    def tick(self):
        for item in list(self.active.values()):
            if item.timeRemaining:
                item.timeRemaining -= self.world.tickPeriod
                if item.timeRemaining <= 0:
                    item.delete()
                    item.timeRanOut()

        for item in list(self.active.values()):
            item.tick()

    def getActiveKinds(self):
        '''
        :return: A new list of the Upgrade classes that are currently active.
        '''
        return list(self.active.keys())

    def getAll(self):
        return list(self.active.values())


class Upgrade(object):
    '''Represents an upgrade that can be bought.'''
    requiredCoins = None
    goneWhenDie = True
    defaultKey = None
    defaultPygameKey = None
    iconPath = 'upgrade-unknown.png'
    enabled = True
    applyLocally = False
    aggressive = False

    category = Categories.ITEM

    # If this flag is set, instead of waiting for a verdict from the server,
    # the client will guess whether a purchase of this upgrade will be allowed,
    # and go on that assumption until it finds out otherwise. This exists so
    # that grenades can feel responsive even if there's high latency.
    doNotWaitForServer = False

    # Upgrades have an upgradeType: this must be a unique, single-character
    # value.
    upgradeType = NotImplemented
    totalTimeLimit = NotImplemented
    name = NotImplemented

    def __init__(self, player):
        self.world = player.world
        self.player = player
        self.timeRemaining = self.totalTimeLimit

    def __str__(self):
        return self.name

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        cls.display_name = cls.name

    @classmethod
    def get_icon(cls, sprites):
        return sprites.upgradeImage(cls)

    @classmethod
    def pre_buy_check(cls, player):
        '''
        If this method returns False, the given player will not attempt
        to buy this upgrade.
        '''
        if cls.aggressive:
            if not player.abilities.aggression:
                return False
            if player.team and not player.team.abilities.aggression:
                return False
        return True

    def dump(self):
        return {
            'kind': self.upgradeType,
            'time': self.timeRemaining,
        }

    @classmethod
    def restore(cls, player, data):
        item = cls(player)
        item.timeRemaining = data['time']
        return item

    def tick(self):
        pass

    def getReactivateCost(self):
        '''
        :return: The cost required to activate the upgrade again before it's
            run out, or None if that's impossible.
        '''
        return None

    @classmethod
    def getActivateNotification(cls, nick):
        return '{} is using a {}'.format(nick, cls.name)

    def use(self):
        '''Initiate the upgrade (server-side)'''
        pass

    def localUse(self, localState):
        '''Initiate the upgrade (client-side)'''
        if self.applyLocally:
            self.use()

    def serverVerified(self, localState):
        '''
        Called client-side when the server has confirmed that this upgrade is
        allowed. This is most useful as a hook for upgrade classes which set
        the doNotWaitForServer flag.
        '''
        if self.doNotWaitForServer:
            localState.discardUnverifiedItem(self)

    def deniedByServer(self, localState):
        '''
        Called client-side when a doNotWaitForServer upgrade needs to be
        canceled because the server did not approve it.
        '''
        self.delete()

    def delete(self):
        '''
        Performs any necessary tasks to remove this upgrade from the game.
        '''
        self.player.items.delete(self)

    def timeRanOut(self):
        '''
        Called by the universe when the upgrade's time has run out.
        '''
        pass

    def cancelOthers(self, others):
        '''
        Helper function to cancel other incompatible items.

        :param others: the Upgrade classes to cancel
        '''
        for upgradeClass in others:
            item = self.player.items.get(upgradeClass)
            if item:
                item.delete()


@registerUpgrade
class Shield(Upgrade):
    '''
    shield: protects player from one shot
    '''
    upgradeType = b's'
    requiredCoins = 500
    totalTimeLimit = 30
    name = 'Shield'
    action = 'shield'
    order = 20
    defaultKey = '2'
    defaultPygameKey = pygame.K_2
    iconPath = 'upgrade-shield.png'
    category = Categories.ITEM

    def __init__(self, player):
        super(Shield, self).__init__(player)
        self.maxProtections = self.world.physics.playerRespawnHealth
        self.protections = self.maxProtections

    def hit(self, hitpoints, hitter, hitKind):
        '''
        Called when this shield is hit for the given number of hitpoints.

        :return: zero if the hit was entirely absorbed by the shield,
            otherwise returns the remainder of the hit that was not absorbed.
        '''
        self.protections -= hitpoints
        if self.protections <= 0:
            result = -self.protections
            self.delete()

            self.player.onShieldDestroyed(hitter, hitKind)
            if self.player.isCanonicalPlayer() and hitter:
                hitter.onDestroyedShield(self.player, hitKind)
        else:
            result = 0
        return result


@registerUpgrade
class MinimapDisruption(Upgrade):
    upgradeType = b'm'
    requiredCoins = 1500
    totalTimeLimit = 20
    name = 'Minimap Disruption'
    action = 'minimap disruption'
    order = 30
    defaultKey = '3'
    defaultPygameKey = pygame.K_3
    iconPath = 'upgrade-minimap.png'
    category = Categories.ITEM

    def __init__(self, *args, **kwargs):
        super(MinimapDisruption, self).__init__(*args, **kwargs)
        self.team = self.player.team

    def use(self):
        if self.team is not None:
            self.team.usingMinimapDisruption = True

    def delete(self):
        if self.team is not None:
            if not any(
                    p for p in self.world.players
                    if p.team == self.team
                    and p.disruptive
                    and p.id != self.player.id):
                self.team.usingMinimapDisruption = False
        super(MinimapDisruption, self).delete()


@registerUpgrade
class Grenade(Upgrade):
    upgradeType = b'g'
    requiredCoins = 450
    totalTimeLimit = 2.5
    goneWhenDie = False
    name = 'Grenade'
    action = 'grenade'
    order = 50
    defaultKey = '5'
    defaultPygameKey = pygame.K_5
    iconPath = 'upgrade-grenade.png'
    doNotWaitForServer = True
    category = Categories.ITEM
    aggressive = True

    @classmethod
    def getActivateNotification(cls, nick):
        return '{} has thrown a {}'.format(nick, cls.name)

    def localUse(self, localState):
        localState.grenadeLaunched()

    def serverVerified(self, localState):
        super(Grenade, self).serverVerified(localState)
        localState.matchGrenade()

    def deniedByServer(self, localState):
        super(Grenade, self).deniedByServer(localState)
        localState.grenadeRemoved()

    def use(self):
        '''Initiate the upgrade.'''
        self.player.world.addGrenade(
            GrenadeShot(self.player.world, self.player, self.totalTimeLimit))


@registerUpgrade
class Ricochet(Upgrade):
    upgradeType = b'r'
    requiredCoins = 150
    totalTimeLimit = 20
    name = 'Ricochet'
    action = 'ricochet'
    order = 60
    defaultKey = '6'
    defaultPygameKey = pygame.K_6
    iconPath = 'upgrade-ricochet.png'
    applyLocally = True
    category = Categories.WEAPON
    aggressive = True

    @classmethod
    def getActivateNotification(cls, nick):
        return '{} is using {}'.format(nick, cls.name)

    def use(self):
        self.cancelOthers([Shoxwave, MachineGun])


@registerUpgrade
class Ninja (Upgrade):
    '''allows you to become invisible to all players on the opposing team'''
    upgradeType = b'n'
    requiredCoins = 325
    totalTimeLimit = 25
    name = 'Ninja'
    action = 'phase shift'  # So old phase shift hotkeys trigger ninja.
    order = 40
    defaultKey = '4'
    defaultPygameKey = pygame.K_4
    iconPath = 'upgrade-ninja.png'
    category = Categories.ITEM

    @classmethod
    def getActivateNotification(cls, nick):
        return '{} has become a {}'.format(nick, cls.name)


@registerUpgrade
class Shoxwave(Upgrade):
    '''
    shockwave: upgrade that will replace shots with a shockwave like that of
    the grenade vaporising all enemies and enemy shots in the radius of blast.
    '''
    upgradeType = b'w'
    requiredCoins = 250
    totalTimeLimit = 45
    name = 'Shoxwave'
    action = 'shoxwave'
    order = 80
    defaultKey = '7'
    defaultPygameKey = pygame.K_7
    iconPath = 'upgrade-shoxwave.png'
    applyLocally = True
    category = Categories.WEAPON
    aggressive = True

    @classmethod
    def getActivateNotification(cls, nick):
        return '{} is using {}'.format(nick, cls.name)

    def use(self):
        self.cancelOthers([Ricochet, MachineGun])


@registerUpgrade
class MachineGun(Upgrade):
    upgradeType = b'x'
    requiredCoins = 500
    totalTimeLimit = 30
    name = 'Machine Gun'
    action = 'turret'   # So that old turret hotkeys trigger machine gun.
    order = 10
    defaultKey = '1'
    defaultPygameKey = pygame.K_1
    iconPath = 'upgrade-machinegun.png'
    applyLocally = True
    category = Categories.WEAPON
    aggressive = True

    BULLETS_BEFORE_OVERHEATING = 16

    def __init__(self, *args, **kwargs):
        super(MachineGun, self).__init__(*args, **kwargs)
        self.overheat_ratio = 0
        self.overheated = False
        self.firing = False

    def dump(self):
        result = super().dump()
        result['heat'] = self.overheat_ratio
        result['overheated'] = self.overheated
        result['firing'] = self.firing
        return result

    @classmethod
    def restore(cls, player, data):
        result = super().restore(player, data)
        result.overheat_ratio = data['heat']
        result.overheated = data['overheated']
        result.firing = data['firing']
        return result

    def weaponDischarged(self):
        reload_rate = self.world.physics.playerMachineGunReloadRate
        reload_time = reload_rate * self.player.standard_reload_time
        self.overheat_ratio += 1 / self.BULLETS_BEFORE_OVERHEATING
        self.overheat_ratio += self.world.tickPeriod / reload_time

        if self.overheat_ratio > 1:
            self.overheat_ratio = 0
            self.overheated = True
            return reload_time
        return self.world.physics.playerMachineGunFireRate

    def cool_one_frame(self):
        normal_reload_amount = self.world.tickPeriod / self.player.standard_reload_time
        reload_amount = normal_reload_amount / self.world.physics.playerMachineGunReloadRate
        self.overheat_ratio = max(0, self.overheat_ratio - reload_amount)
        if self.overheated and self.player.reloadTime <= 0:
            self.overheated = False

    def use(self):
        self.cancelOthers([Shoxwave, Ricochet])


@registerUpgrade
class Bomber(Upgrade):
    upgradeType = b'b'
    requiredCoins = 50
    totalTimeLimit = 6
    name = 'Bomber'
    action = 'bomber'
    order = 90
    defaultKey = '8'
    defaultPygameKey = pygame.K_8
    iconPath = 'upgrade-bomber.png'
    applyLocally = True
    category = Categories.ITEM

    def __init__(self, *args, **kwargs):
        super(Bomber, self).__init__(*args, **kwargs)
        self.firstUse = True

    def timeRanOut(self):
        self.cancelOthers([Shield])

        if self.player.isCanonicalPlayer():
            self.world.bomberExploded(self.player)

    def getReactivateCost(self):
        return 0

    def use(self):
        if self.firstUse:
            self.firstUse = False
        else:
            # Hitting "use" a second time cancels bomber
            self.delete()


@specialUpgrade
class RespawnFreezer(Upgrade):
    '''
    Respawn freezer: upgrade that will render spawn points unusable.
    '''
    upgradeType = b'f'
    requiredCoins = 400
    totalTimeLimit = 30
    name = 'Respawn Freezer'
    action = 'respawn freezer'
    order = 100
    defaultKey = '9'
    defaultPygameKey = pygame.K_9
    category = Categories.ITEM

    def use(self):
        '''Initiate the upgrade'''
        self.zone = self.player.getZone()
        self.zone.frozen = True

    def delete(self):
        '''Performs any necessary tasks to remove this upgrade from the game'''
        super(RespawnFreezer, self).delete()
        if self.zone:
            self.zone.frozen = False
