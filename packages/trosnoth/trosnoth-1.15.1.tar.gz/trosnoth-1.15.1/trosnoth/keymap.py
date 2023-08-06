import pygame

from trosnoth.const import (
    ACTION_SHOW_TRAJECTORY, ACTION_DEBUGKEY, ACTION_EMOTE, ACTION_LEFT,
    ACTION_DOWN, ACTION_RIGHT, ACTION_JUMP, ACTION_HOOK, ACTION_FOLLOW,
    ACTION_RADIAL_UPGRADE_MENU, ACTION_USE_UPGRADE,
    ACTION_RESPAWN,
    ACTION_READY, ACTION_CLEAR_UPGRADE, ACTION_CHAT,
    ACTION_PAUSE_GAME, ACTION_TERMINAL_TOGGLE,
)
from trosnoth.gui.keyboard import VirtualKeySet, mouseButton

# Define virtual keys and their default bindings.
default_game_keys = VirtualKeySet((
    # Movement keys.
    (ACTION_LEFT, pygame.K_a),
    (ACTION_DOWN, pygame.K_s),
    (ACTION_RIGHT, pygame.K_d),
    (ACTION_JUMP, pygame.K_w),
    (ACTION_HOOK, mouseButton(3)),
    (ACTION_SHOW_TRAJECTORY, pygame.K_LSHIFT),
    (ACTION_DEBUGKEY, mouseButton(2)),

    # Used in replay mode.
    (ACTION_FOLLOW, pygame.K_EQUALS),

    (ACTION_RADIAL_UPGRADE_MENU, pygame.K_TAB),
    (ACTION_USE_UPGRADE, pygame.K_SPACE),
    (ACTION_RESPAWN, pygame.K_r),
    (ACTION_READY, pygame.K_y),
    (ACTION_EMOTE, pygame.K_t),

    (ACTION_CLEAR_UPGRADE, pygame.K_0),

    (ACTION_CHAT, pygame.K_RETURN),
    (ACTION_PAUSE_GAME, pygame.K_PAUSE),

    (ACTION_TERMINAL_TOGGLE, pygame.K_SCROLLOCK),
))

from trosnoth.model.upgrades import allUpgrades

for upgradeClass in allUpgrades:
    if upgradeClass.defaultPygameKey is not None:
        default_game_keys[upgradeClass.action] = upgradeClass.defaultPygameKey
del upgradeClass
