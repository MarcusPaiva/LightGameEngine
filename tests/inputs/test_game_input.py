"""
Tests for :mod:`light_game_engine.inputs.game_input`.

All pygame key/mouse polling calls are mocked, so these tests never
depend on real keyboard/mouse hardware state.
"""
from collections import defaultdict

import pygame
import pytest

from light_game_engine.inputs.game_input import (
    Keys,
    Keyboard,
    set_reapeat,
    mouse_click_detection,
    mouse_position,
)


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
