"""
Keyboard, mouse and controller input - the only place in the engine
that talks to pygame's key/mouse/controller polling APIs.
"""
from enum import Enum
from typing import List, Optional, Tuple

import pygame
import pygame._sdl2.controller as controller


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


def _build_buttons_enum() -> type[Enum]:
    """
    Build one Buttons member per SDL game-controller button pygame
    knows about, named after pygame's own CONTROLLER_BUTTON_* constant
    (lowercased, without the "CONTROLLER_BUTTON_" prefix) - e.g.
    CONTROLLER_BUTTON_A becomes Buttons.a, CONTROLLER_BUTTON_DPAD_UP
    becomes Buttons.dpad_up.

    This uses SDL's GameController API (via pygame._sdl2.controller)
    instead of the older, per-device pygame.joystick API, so button
    names are the same regardless of which controller brand is plugged
    in - SDL's built-in mapping database already recognizes Xbox,
    PlayStation, Switch and most third-party controllers and maps them
    all onto this same standardized layout.

    :return: The dynamically built ``Buttons`` enum.
    :rtype: type[Enum]
    """
    prefix = "CONTROLLER_BUTTON_"
    members = {
        name[len(prefix):].lower(): getattr(pygame, name)
        for name in dir(pygame)
        if name.startswith(prefix) and not name.endswith(("_INVALID", "_MAX"))
    }
    return Enum("Buttons", members)


def _build_axes_enum() -> type[Enum]:
    """
    Build one Axes member per SDL game-controller axis pygame knows
    about (the two sticks and the two triggers), named after pygame's
    own CONTROLLER_AXIS_* constant - e.g. CONTROLLER_AXIS_LEFTX becomes
    Axes.leftx.

    :return: The dynamically built ``Axes`` enum.
    :rtype: type[Enum]
    """
    prefix = "CONTROLLER_AXIS_"
    members = {
        name[len(prefix):].lower(): getattr(pygame, name)
        for name in dir(pygame)
        if name.startswith(prefix) and not name.endswith(("_INVALID", "_MAX"))
    }
    return Enum("Axes", members)


Buttons = _build_buttons_enum()
Axes = _build_axes_enum()


class Joystick:
    """
    Polls one connected game controller once per frame and translates
    its state into :class:`Buttons`/:class:`Axes` members, mirroring
    :class:`Keyboard`'s interface.
    """

    #: Raw axis readings below this magnitude are reported as 0.0, so a
    #: controller's natural stick drift doesn't register as input.
    DEFAULT_DEADZONE = 0.1

    def __init__(self, device_index: int = 0):
        """
        Open a controller and start with no buttons recorded as pressed.

        :param device_index: Index of the controller to open (0 for the
            first one connected).
        """
        controller.init()
        self._device_index = device_index
        self._controller = (
            controller.Controller(device_index) if controller.is_controller(device_index) else None
        )
        self._current_buttons_pressed = []
        self._previous_buttons_pressed = []
        self._user_is_pressing = False

    @property
    def connected(self) -> bool:
        """
        :return: Whether a controller was found at this index and is
            still attached.
        :rtype: bool
        """
        return self._controller is not None and self._controller.attached()

    @property
    def name(self) -> Optional[str]:
        """
        :return: The controller's SDL-reported name (e.g. "Xbox Series X
            Controller", "PS5 Controller", "Nintendo Switch Pro
            Controller"), or None if nothing is connected.
        :rtype: Optional[str]
        """
        return self._controller.name if self._controller is not None else None

    def detect_buttons(self):
        """
        Refresh the set of currently pressed buttons from the controller.

        :return: None
        """
        self._previous_buttons_pressed = self._current_buttons_pressed
        if self._controller is None:
            self._current_buttons_pressed = []
            self._user_is_pressing = False
            return
        self._current_buttons_pressed = [
            button for button in Buttons if self._controller.get_button(button.value)
        ]
        self._user_is_pressing = len(self._current_buttons_pressed) > 0

    @property
    def user_is_pressing(self):
        """
        :return: Whether any button was pressed on the last
            :meth:`detect_buttons` call.
        :rtype: bool
        """
        return self._user_is_pressing

    @property
    def current_buttons_pressing(self):
        """
        :return: The :class:`Buttons` members currently pressed.
        :rtype: List[Buttons]
        """
        return self._current_buttons_pressed

    def button_just_pressed(self, button: "Buttons") -> bool:
        """
        Whether a button transitioned from not-pressed to pressed on the
        last :meth:`detect_buttons` call - useful for menu actions
        (confirm, navigate) that should fire once per press instead of
        once per frame while held.

        :param button: The button to check.
        :return: Whether it was just pressed.
        :rtype: bool
        """
        return button in self._current_buttons_pressed and button not in self._previous_buttons_pressed

    def get_axis(self, axis: "Axes", deadzone: float = DEFAULT_DEADZONE) -> float:
        """
        Read one stick/trigger axis, normalized to the [-1.0, 1.0] range.

        :param axis: Which axis to read.
        :param deadzone: Values with an absolute magnitude below this
            are reported as 0.0.
        :return: The axis' current value.
        :rtype: float
        """
        if self._controller is None:
            return 0.0
        value = max(-1.0, min(1.0, self._controller.get_axis(axis.value) / 32767))
        return value if abs(value) > deadzone else 0.0


def list_connected_joysticks() -> List[Tuple[int, str]]:
    """
    List every connected controller SDL currently recognizes.

    :return: ``(device_index, name)`` pairs, one per connected
        controller - each ``device_index`` is what :class:`Joystick`
        expects.
    :rtype: List[Tuple[int, str]]
    """
    controller.init()
    return [
        (index, controller.name_forindex(index))
        for index in range(controller.get_count())
        if controller.is_controller(index)
    ]


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
