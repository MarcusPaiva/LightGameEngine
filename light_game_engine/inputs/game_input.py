"""
Keyboard and mouse input - the only place in the engine that talks to
pygame's key/mouse polling APIs.
"""
from enum import Enum
from typing import Optional, Tuple

import pygame


def _build_keys_enum() -> type[Enum]:
    """
    Build one Keys member per key pygame knows about, named after pygame's
    own K_* constant (lowercased, without the "K_" prefix) - e.g. K_ESCAPE
    becomes Keys.escape, K_a becomes Keys.a, K_F1 becomes Keys.f1.

    A few friendlier aliases used by the game are added on top for
    readability; since they share the same underlying key code as their
    canonical name, they resolve to the very same member (Keys.key_up is
    Keys.up), so both spellings work everywhere.

    :return: The dynamically built ``Keys`` enum.
    :rtype: type[Enum]
    """
    members = {name[2:].lower(): getattr(pygame, name) for name in dir(pygame) if name.startswith("K_")}
    members.update({
        "key_up": pygame.K_UP,
        "key_down": pygame.K_DOWN,
        "key_left": pygame.K_LEFT,
        "key_right": pygame.K_RIGHT,
    })
    return Enum("Keys", members)


Keys = _build_keys_enum()


def set_reapeat(delay, interval):
    """
    Configure keyboard key-repeat.

    :param delay: Milliseconds before the first repeat fires.
    :param interval: Milliseconds between subsequent repeats.
    :return: None
    """
    pygame.key.set_repeat(delay, interval)


class Keyboard:
    """
    Polls pygame for currently pressed keys once per frame and
    translates them into :class:`Keys` members.
    """

    def __init__(self):
        """
        Start with no keys recorded as pressed.
        """
        self._current_keys_pressed = []
        self._user_is_pressing = False

    def detect_buttons(self):
        """
        Refresh the set of currently pressed keys from pygame.

        :return: None
        """
        pressed = pygame.key.get_pressed()
        self._current_keys_pressed = [key for key in Keys if pressed[key.value]]
        self._user_is_pressing = len(self._current_keys_pressed) > 0

    @property
    def user_is_pressing(self):
        """
        :return: Whether any key was pressed on the last
            :meth:`detect_buttons` call.
        :rtype: bool
        """
        return self._user_is_pressing

    @property
    def current_keys_pressing(self):
        """
        :return: The :class:`Keys` members currently pressed.
        :rtype: List[Keys]
        """
        return self._current_keys_pressed


def mouse_click_detection() -> Optional[Tuple[int, int]]:
    """
    Mouse click detection.

    :return: Mouse click position, or None if the left button isn't pressed.
    :rtype: Optional[Tuple[int, int]]
    """
    if pygame.mouse.get_pressed()[0]:
        return pygame.mouse.get_pos()
    return None


def mouse_position() -> Tuple[int, int]:
    """
    Current mouse cursor position, regardless of any button being pressed.

    :return: Mouse position.
    :rtype: Tuple[int, int]
    """
    return pygame.mouse.get_pos()
