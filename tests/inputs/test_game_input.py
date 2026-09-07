"""
Tests for :mod:`light_game_engine.inputs.game_input`.

All pygame key/mouse polling calls are mocked, so these tests never
depend on real keyboard/mouse hardware state. Joystick tests mock
pygame._sdl2.controller the same way, so they never depend on a real
controller being plugged in either.
"""
from collections import defaultdict

import pygame
import pytest

from light_game_engine.inputs.game_input import (
    Axes,
    Buttons,
    Joystick,
    Keys,
    Keyboard,
    list_connected_joysticks,
    set_reapeat,
    mouse_click_detection,
    mouse_position,
)


class FakeController:
    """Stand-in for pygame._sdl2.controller.Controller."""

    def __init__(self, name="Fake Pad", attached=True, buttons=None, axes=None):
        self.name = name
        self._attached = attached
        self._buttons = buttons or {}
        self._axes = axes or {}

    def attached(self):
        return self._attached

    def get_button(self, button_id):
        return self._buttons.get(button_id, False)

    def get_axis(self, axis_id):
        return self._axes.get(axis_id, 0)


class TestKeysEnum:
    def test_has_one_member_per_pygame_key_constant(self):
        assert Keys.escape.value == pygame.K_ESCAPE
        assert Keys.a.value == pygame.K_a
        assert Keys.f1.value == pygame.K_F1
        assert Keys.space.value == pygame.K_SPACE

    def test_directional_aliases_match_canonical_arrow_keys(self):
        assert Keys.key_up is Keys.up
        assert Keys.key_down is Keys.down
        assert Keys.key_left is Keys.left
        assert Keys.key_right is Keys.right

    def test_aliases_share_pygame_key_codes(self):
        assert Keys.key_up.value == pygame.K_UP
        assert Keys.key_down.value == pygame.K_DOWN
        assert Keys.key_left.value == pygame.K_LEFT
        assert Keys.key_right.value == pygame.K_RIGHT


class TestSetReapeat:
    def test_delegates_to_pygame_key_set_repeat(self, mocker):
        set_repeat = mocker.patch("light_game_engine.inputs.game_input.pygame.key.set_repeat")
        set_reapeat(300, 50)
        set_repeat.assert_called_once_with(300, 50)


class TestKeyboard:
    def test_no_keys_pressed_initially(self):
        keyboard = Keyboard()
        assert keyboard.user_is_pressing is False
        assert keyboard.current_keys_pressing == []

    def _fake_pressed_array(self, *pressed_keys: Keys):
        # pygame's real key constants span a huge range (extended keys use
        # the SDL scancode mask, values over 2**30), so a plain list sized
        # to the max value would try to allocate over a billion entries.
        # A dict indexed the same way as pygame's ScancodeWrapper avoids that.
        pressed = defaultdict(bool)
        for key in pressed_keys:
            pressed[key.value] = True
        return pressed

    def test_detect_buttons_with_no_keys_pressed(self, mocker):
        mocker.patch(
            "light_game_engine.inputs.game_input.pygame.key.get_pressed",
            return_value=self._fake_pressed_array(),
        )
        keyboard = Keyboard()
        keyboard.detect_buttons()
        assert keyboard.user_is_pressing is False
        assert keyboard.current_keys_pressing == []

    def test_detect_buttons_with_one_key_pressed(self, mocker):
        mocker.patch(
            "light_game_engine.inputs.game_input.pygame.key.get_pressed",
            return_value=self._fake_pressed_array(Keys.a),
        )
        keyboard = Keyboard()
        keyboard.detect_buttons()
        assert keyboard.user_is_pressing is True
        assert keyboard.current_keys_pressing == [Keys.a]

    def test_detect_buttons_with_multiple_keys_pressed(self, mocker):
        mocker.patch(
            "light_game_engine.inputs.game_input.pygame.key.get_pressed",
            return_value=self._fake_pressed_array(Keys.a, Keys.key_up),
        )
        keyboard = Keyboard()
        keyboard.detect_buttons()
        assert keyboard.user_is_pressing is True
        assert set(keyboard.current_keys_pressing) == {Keys.a, Keys.up}

    def test_detect_buttons_refreshes_state_each_call(self, mocker):
        get_pressed = mocker.patch("light_game_engine.inputs.game_input.pygame.key.get_pressed")
        keyboard = Keyboard()

        get_pressed.return_value = self._fake_pressed_array(Keys.a)
        keyboard.detect_buttons()
        assert keyboard.current_keys_pressing == [Keys.a]

        get_pressed.return_value = self._fake_pressed_array()
        keyboard.detect_buttons()
        assert keyboard.current_keys_pressing == []
        assert keyboard.user_is_pressing is False


class TestMouseClickDetection:
    def test_returns_none_when_left_button_not_pressed(self, mocker):
        mocker.patch(
            "light_game_engine.inputs.game_input.pygame.mouse.get_pressed",
            return_value=(False, False, False),
        )
        assert mouse_click_detection() is None

    def test_returns_position_when_left_button_pressed(self, mocker):
        mocker.patch(
            "light_game_engine.inputs.game_input.pygame.mouse.get_pressed",
            return_value=(True, False, False),
        )
        mocker.patch(
            "light_game_engine.inputs.game_input.pygame.mouse.get_pos",
            return_value=(42, 24),
        )
        assert mouse_click_detection() == (42, 24)

    def test_ignores_right_and_middle_buttons(self, mocker):
        mocker.patch(
            "light_game_engine.inputs.game_input.pygame.mouse.get_pressed",
            return_value=(False, True, True),
        )
        assert mouse_click_detection() is None


class TestMousePosition:
    def test_returns_current_mouse_position(self, mocker):
        mocker.patch(
            "light_game_engine.inputs.game_input.pygame.mouse.get_pos",
            return_value=(10, 20),
        )
        assert mouse_position() == (10, 20)


class TestButtonsEnum:
    def test_has_one_member_per_pygame_controller_button_constant(self):
        assert Buttons.a.value == pygame.CONTROLLER_BUTTON_A
        assert Buttons.b.value == pygame.CONTROLLER_BUTTON_B
        assert Buttons.dpad_up.value == pygame.CONTROLLER_BUTTON_DPAD_UP
        assert Buttons.leftshoulder.value == pygame.CONTROLLER_BUTTON_LEFTSHOULDER

    def test_excludes_invalid_and_max_sentinels(self):
        assert not hasattr(Buttons, "invalid")
        assert not hasattr(Buttons, "max")


class TestAxesEnum:
    def test_has_one_member_per_pygame_controller_axis_constant(self):
        assert Axes.leftx.value == pygame.CONTROLLER_AXIS_LEFTX
        assert Axes.lefty.value == pygame.CONTROLLER_AXIS_LEFTY
        assert Axes.triggerleft.value == pygame.CONTROLLER_AXIS_TRIGGERLEFT

    def test_excludes_invalid_and_max_sentinels(self):
        assert not hasattr(Axes, "invalid")
        assert not hasattr(Axes, "max")


class TestListConnectedJoysticks:
    def _mock_devices(self, mocker, devices):
        """
        :param devices: (is_controller, name) per SDL joystick index.
        """
        mocker.patch("light_game_engine.inputs.game_input.controller.init")
        mocker.patch("light_game_engine.inputs.game_input.controller.get_count", return_value=len(devices))
        mocker.patch(
            "light_game_engine.inputs.game_input.controller.is_controller",
            side_effect=lambda index: devices[index][0],
        )
        mocker.patch(
            "light_game_engine.inputs.game_input.controller.name_forindex",
            side_effect=lambda index: devices[index][1],
        )

    def test_no_devices_returns_an_empty_list(self, mocker):
        self._mock_devices(mocker, [])
        assert list_connected_joysticks() == []

    def test_one_connected_controller(self, mocker):
        self._mock_devices(mocker, [(True, "Xbox Series X Controller")])
        assert list_connected_joysticks() == [(0, "Xbox Series X Controller")]

    def test_multiple_connected_controllers_keep_their_index(self, mocker):
        self._mock_devices(mocker, [
            (True, "Xbox Series X Controller"),
            (True, "PS5 Controller"),
        ])
        assert list_connected_joysticks() == [(0, "Xbox Series X Controller"), (1, "PS5 Controller")]

    def test_non_controller_joysticks_are_excluded(self, mocker):
        # SDL may see a joystick device it has no game-controller mapping
        # for; is_controller(index) is False for those and they should
        # be left out.
        self._mock_devices(mocker, [
            (True, "Xbox Series X Controller"),
            (False, "Some Unmapped Joystick"),
        ])
        assert list_connected_joysticks() == [(0, "Xbox Series X Controller")]

    def test_initializes_the_controller_subsystem(self, mocker):
        self._mock_devices(mocker, [])
        init = mocker.patch("light_game_engine.inputs.game_input.controller.init")

        list_connected_joysticks()

        init.assert_called_once()


class TestJoystickConnection:
    def test_no_controller_at_index_is_not_connected(self, mocker):
        mocker.patch("light_game_engine.inputs.game_input.controller.init")
        mocker.patch("light_game_engine.inputs.game_input.controller.is_controller", return_value=False)

        joystick = Joystick()

        assert joystick.connected is False
        assert joystick.name is None

    def test_controller_at_index_is_connected(self, mocker):
        mocker.patch("light_game_engine.inputs.game_input.controller.init")
        mocker.patch("light_game_engine.inputs.game_input.controller.is_controller", return_value=True)
        mocker.patch(
            "light_game_engine.inputs.game_input.controller.Controller",
            return_value=FakeController(name="Xbox Series X Controller"),
        )

        joystick = Joystick()

        assert joystick.connected is True
        assert joystick.name == "Xbox Series X Controller"

    def test_opens_the_requested_device_index(self, mocker):
        mocker.patch("light_game_engine.inputs.game_input.controller.init")
        mocker.patch("light_game_engine.inputs.game_input.controller.is_controller", return_value=True)
        controller_ctor = mocker.patch(
            "light_game_engine.inputs.game_input.controller.Controller",
            return_value=FakeController(),
        )

        Joystick(device_index=2)

        controller_ctor.assert_called_once_with(2)

    def test_detached_controller_is_not_connected(self, mocker):
        mocker.patch("light_game_engine.inputs.game_input.controller.init")
        mocker.patch("light_game_engine.inputs.game_input.controller.is_controller", return_value=True)
        mocker.patch(
            "light_game_engine.inputs.game_input.controller.Controller",
            return_value=FakeController(attached=False),
        )

        assert Joystick().connected is False


class TestJoystickDetectButtons:
    def _joystick_with(self, mocker, **fake_controller_kwargs):
        mocker.patch("light_game_engine.inputs.game_input.controller.init")
        mocker.patch("light_game_engine.inputs.game_input.controller.is_controller", return_value=True)
        mocker.patch(
            "light_game_engine.inputs.game_input.controller.Controller",
            return_value=FakeController(**fake_controller_kwargs),
        )
        return Joystick()

    def test_no_controller_reports_nothing_pressed(self, mocker):
        mocker.patch("light_game_engine.inputs.game_input.controller.init")
        mocker.patch("light_game_engine.inputs.game_input.controller.is_controller", return_value=False)
        joystick = Joystick()

        joystick.detect_buttons()

        assert joystick.current_buttons_pressing == []
        assert joystick.user_is_pressing is False

    def test_no_buttons_pressed(self, mocker):
        joystick = self._joystick_with(mocker, buttons={})
        joystick.detect_buttons()
        assert joystick.current_buttons_pressing == []
        assert joystick.user_is_pressing is False

    def test_one_button_pressed(self, mocker):
        joystick = self._joystick_with(mocker, buttons={Buttons.a.value: True})
        joystick.detect_buttons()
        assert joystick.current_buttons_pressing == [Buttons.a]
        assert joystick.user_is_pressing is True

    def test_multiple_buttons_pressed(self, mocker):
        joystick = self._joystick_with(
            mocker, buttons={Buttons.a.value: True, Buttons.dpad_up.value: True}
        )
        joystick.detect_buttons()
        assert set(joystick.current_buttons_pressing) == {Buttons.a, Buttons.dpad_up}

    def test_detect_buttons_refreshes_state_each_call(self, mocker):
        joystick = self._joystick_with(mocker, buttons={Buttons.a.value: True})
        joystick.detect_buttons()
        assert joystick.current_buttons_pressing == [Buttons.a]

        joystick._controller._buttons = {}
        joystick.detect_buttons()
        assert joystick.current_buttons_pressing == []
        assert joystick.user_is_pressing is False


class TestJoystickGetAxis:
    def _joystick_with(self, mocker, **fake_controller_kwargs):
        mocker.patch("light_game_engine.inputs.game_input.controller.init")
        mocker.patch("light_game_engine.inputs.game_input.controller.is_controller", return_value=True)
        mocker.patch(
            "light_game_engine.inputs.game_input.controller.Controller",
            return_value=FakeController(**fake_controller_kwargs),
        )
        return Joystick()

    def test_no_controller_returns_zero(self, mocker):
        mocker.patch("light_game_engine.inputs.game_input.controller.init")
        mocker.patch("light_game_engine.inputs.game_input.controller.is_controller", return_value=False)
        joystick = Joystick()
        assert joystick.get_axis(Axes.leftx) == 0.0

    def test_full_deflection_normalizes_to_one(self, mocker):
        joystick = self._joystick_with(mocker, axes={Axes.leftx.value: 32767})
        assert joystick.get_axis(Axes.leftx) == pytest.approx(1.0)

    def test_full_negative_deflection_normalizes_to_minus_one(self, mocker):
        joystick = self._joystick_with(mocker, axes={Axes.leftx.value: -32767})
        assert joystick.get_axis(Axes.leftx) == pytest.approx(-1.0)

    def test_out_of_range_value_is_clamped(self, mocker):
        joystick = self._joystick_with(mocker, axes={Axes.leftx.value: -32768})
        assert joystick.get_axis(Axes.leftx) >= -1.0

    def test_value_within_default_deadzone_is_zero(self, mocker):
        joystick = self._joystick_with(mocker, axes={Axes.leftx.value: 1000})  # ~0.03
        assert joystick.get_axis(Axes.leftx) == 0.0

    def test_value_outside_default_deadzone_is_reported(self, mocker):
        joystick = self._joystick_with(mocker, axes={Axes.leftx.value: 16000})  # ~0.49
        assert joystick.get_axis(Axes.leftx) == pytest.approx(16000 / 32767)

    def test_custom_deadzone_overrides_default(self, mocker):
        joystick = self._joystick_with(mocker, axes={Axes.leftx.value: 16000})
        assert joystick.get_axis(Axes.leftx, deadzone=0.9) == 0.0

    def test_untouched_axis_defaults_to_zero(self, mocker):
        joystick = self._joystick_with(mocker, axes={})
        assert joystick.get_axis(Axes.rightx) == 0.0
