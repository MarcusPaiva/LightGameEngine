"""
Keyboard, mouse and controller input - the only place in the engine
that talks to pygame's key/mouse/controller code.
"""
from abc import ABC, abstractmethod
from enum import Enum
from typing import List, Optional, Tuple

import pygame
import pygame._sdl2.controller as controller

class InputModel(ABC):
    """
    The shared rule every input source (Keyboard, Joystick, ...) must
    follow: refresh its state once per frame, then say whether
    anything is pressed, and what.
    """

    @abstractmethod
    def detect_buttons(self):
        """
        Refresh this input's currently pressed keys/buttons.

        :return: None
        """
        pass

    @property
    @abstractmethod
    def user_is_pressing(self) -> bool:
        """
        :return: True if anything was pressed the last time
            :meth:`detect_buttons` was called.
        :rtype: bool
        """
        pass

    @property
    @abstractmethod
    def get_user_interaction(self) -> 'Keys | Buttons':
        """
        :return: The keys/buttons currently pressed.
        :rtype: List[Keys] or List[Buttons]
        """
        pass

def _build_keys_enum() -> type[Enum]:
    """
    Build one Keys member for every key pygame knows about. Each name
    comes from pygame's own K_* constant, made lowercase and with the
    "K_" removed - for example, K_ESCAPE becomes Keys.escape, K_a
    becomes Keys.a, and K_F1 becomes Keys.f1.

    A few easier-to-read names are added on top, for the arrow keys.
    They use the same key code as the normal name, so both spellings
    point to the same member (Keys.key_up is the same as Keys.up).

    :return: The Keys enum, built at import time.
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
    Set up keyboard key-repeat: how a held key sends more key-presses.

    :param delay: Milliseconds to wait before the key starts repeating.
    :param interval: Milliseconds between each repeat after that.
    :return: None
    """
    pygame.key.set_repeat(delay, interval)


class Keyboard(InputModel):
    """
    Checks which keys are pressed, once per frame, and turns them into
    :class:`Keys` members.
    """

    def __init__(self):
        """
        Start with no keys marked as pressed.
        """
        self._current_keys_pressed = []
        self._user_is_pressing = False

    def detect_buttons(self):
        """
        Ask pygame which keys are pressed right now, and store them.

        :return: None
        """
        pressed = pygame.key.get_pressed()
        self._current_keys_pressed = [key for key in Keys if pressed[key.value]]
        self._user_is_pressing = len(self._current_keys_pressed) > 0

    @property
    def user_is_pressing(self):
        """
        :return: True if any key was pressed the last time
            :meth:`detect_buttons` was called.
        :rtype: bool
        """
        return self._user_is_pressing

    @property
    def get_user_interaction(self):
        """
        :return: The :class:`Keys` members currently pressed.
        :rtype: List[Keys]
        """
        return self._current_keys_pressed


def _build_buttons_enum() -> type[Enum]:
    """
    Build one Buttons member for every SDL game-controller button
    pygame knows about. Each name comes from pygame's own
    CONTROLLER_BUTTON_* constant, made lowercase and with the
    "CONTROLLER_BUTTON_" part removed - for example,
    CONTROLLER_BUTTON_A becomes Buttons.a, and CONTROLLER_BUTTON_DPAD_UP
    becomes Buttons.dpad_up.

    This uses SDL's GameController code (through
    pygame._sdl2.controller) instead of the older pygame.joystick code.
    That means button names stay the same no matter which controller
    brand is plugged in - SDL already knows how to read Xbox,
    PlayStation, Switch, and most other controllers, and maps them all
    onto this same set of names.

    :return: The Buttons enum, built at import time.
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
    Build one Axes member for every SDL game-controller stick/trigger
    axis pygame knows about. Each name comes from pygame's own
    CONTROLLER_AXIS_* constant - for example, CONTROLLER_AXIS_LEFTX
    becomes Axes.leftx.

    :return: The Axes enum, built at import time.
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


class Joystick(InputModel):
    """
    Checks the state of one connected game controller, once per frame,
    and turns it into :class:`Buttons`/:class:`Axes` members. Works
    the same way as :class:`Keyboard`.
    """

    #: If a stick/trigger reading is smaller than this, it counts as
    #: 0.0. This stops small, natural stick drift from being read as
    #: real input.
    DEFAULT_DEADZONE = 0.1

    def __init__(self, device_index: int = 0):
        """
        Open a controller. Start with no buttons marked as pressed.

        :param device_index: Which controller to open (0 is the first
            one connected).
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
        :return: True if a controller was found at this index, and it
            is still plugged in.
        :rtype: bool
        """
        return self._controller is not None and self._controller.attached()

    @property
    def name(self) -> Optional[str]:
        """
        :return: The controller's name, as reported by SDL (for
            example "Xbox Series X Controller", "PS5 Controller",
            "Nintendo Switch Pro Controller"). None if nothing is
            connected.
        :rtype: Optional[str]
        """
        return self._controller.name if self._controller is not None else None

    def detect_buttons(self):
        """
        Ask the controller which buttons are pressed right now, and
        store them.

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
        :return: True if any button was pressed the last time
            :meth:`detect_buttons` was called.
        :rtype: bool
        """
        return self._user_is_pressing

    @property
    def get_user_interaction(self):
        """
        :return: The :class:`Buttons` members currently pressed.
        :rtype: List[Buttons]
        """
        return self._current_buttons_pressed

    def button_just_pressed(self, button: "Buttons") -> bool:
        """
        Check if a button went from not-pressed to pressed on the last
        :meth:`detect_buttons` call. This is useful for menu actions
        (like confirm or move) that should happen once per press, not
        once per frame while the button stays held down.

        :param button: The button to check.
        :return: True if it was just pressed.
        :rtype: bool
        """
        return button in self._current_buttons_pressed and button not in self._previous_buttons_pressed

    def get_axis(self, axis: "Axes", deadzone: float = DEFAULT_DEADZONE) -> float:
        """
        Read one stick or trigger. The result is scaled to fit between
        -1.0 and 1.0.

        :param axis: Which axis to read.
        :param deadzone: Any reading smaller than this (as a positive
            or negative amount) counts as 0.0.
        :return: The axis' current value.
        :rtype: float
        """
        if self._controller is None:
            return 0.0
        value = max(-1.0, min(1.0, self._controller.get_axis(axis.value) / 32767))
        return value if abs(value) > deadzone else 0.0


def list_connected_joysticks() -> List[Tuple[int, str]]:
    """
    List every controller SDL currently sees as plugged in.

    :return: ``(device_index, name)`` pairs, one for each connected
        controller. Each ``device_index`` is the same number you would
        pass to :class:`Joystick`.
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
    Check if the left mouse button is being clicked right now.

    :return: The mouse position if the left button is pressed, or None
        if it is not.
    :rtype: Optional[Tuple[int, int]]
    """
    if pygame.mouse.get_pressed()[0]:
        return pygame.mouse.get_pos()
    return None


def mouse_position() -> Tuple[int, int]:
    """
    Get where the mouse is right now, whether or not any button is
    pressed.

    :return: Mouse position.
    :rtype: Tuple[int, int]
    """
    return pygame.mouse.get_pos()
