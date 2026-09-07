"""
Tests for :mod:`light_game_engine.inputs.alias`.

Uses a minimal InputModel implementation instead of a real
Keyboard/Joystick, so these tests exercise Alias's own logic without
depending on pygame's key/controller polling at all.
"""
import pytest

from light_game_engine.inputs.alias import Alias
from light_game_engine.inputs.game_input import Buttons, InputModel, Keys


class FakeInput(InputModel):
    """Minimal InputModel: caller sets what's "pressed" directly."""

    def __init__(self, pressed=None, is_pressing=None):
        self.detect_buttons_calls = 0
        self._pressed = list(pressed or [])
        self._is_pressing = is_pressing if is_pressing is not None else bool(self._pressed)

    def detect_buttons(self):
        self.detect_buttons_calls += 1

    @property
    def user_is_pressing(self):
        return self._is_pressing

    @property
    def get_user_interaction(self):
        return self._pressed


class TestAliasInputManagement:
    def test_add_input_returns_self(self):
        alias = Alias()
        assert alias.add_input(FakeInput()) is alias

    def test_remove_input_returns_self(self):
        alias = Alias()
        fake = FakeInput()
        alias.add_input(fake)
        assert alias.remove_input(fake) is alias

    def test_removed_input_no_longer_contributes(self):
        alias = Alias()
        fake = FakeInput(pressed=[Keys.space])
        alias.add_input(fake).add_alias("jump", Keys.space)
        alias.remove_input(fake)
        assert alias.get_alias_triggered() == []

    def test_remove_input_never_added_raises(self):
        alias = Alias()
        with pytest.raises(ValueError):
            alias.remove_input(FakeInput())


class TestAliasAliasManagement:
    def test_add_alias_returns_self(self):
        alias = Alias()
        assert alias.add_alias("jump", Keys.space) is alias

    def test_remove_alias_returns_self(self):
        alias = Alias()
        alias.add_alias("jump", Keys.space)
        assert alias.remove_alias("jump") is alias

    def test_remove_alias_never_added_raises(self):
        alias = Alias()
        with pytest.raises(KeyError):
            alias.remove_alias("jump")

    def test_remove_key_in_alias_returns_self(self):
        alias = Alias()
        alias.add_alias("jump", Keys.space)
        assert alias.remove_key_in_alias("jump", Keys.space) is alias

    def test_remove_key_in_alias_keeps_other_keys(self):
        alias = Alias()
        fake = FakeInput(pressed=[Keys.up])
        alias.add_input(fake)
        alias.add_alias("jump", Keys.space)
        alias.add_alias("jump", Keys.up)

        alias.remove_key_in_alias("jump", Keys.space)

        assert alias.get_alias_triggered() == ["jump"]

    def test_remove_key_not_in_alias_raises(self):
        alias = Alias()
        alias.add_alias("jump", Keys.space)
        with pytest.raises(ValueError):
            alias.remove_key_in_alias("jump", Keys.up)


class TestAliasGetTriggered:
    def test_no_inputs_returns_empty_list(self):
        alias = Alias()
        alias.add_alias("jump", Keys.space)
        assert alias.get_alias_triggered() == []

    def test_no_aliases_returns_empty_list(self):
        alias = Alias()
        alias.add_input(FakeInput(pressed=[Keys.space]))
        assert alias.get_alias_triggered() == []

    def test_mapped_key_pressed_triggers_its_alias(self):
        alias = Alias()
        alias.add_input(FakeInput(pressed=[Keys.space]))
        alias.add_alias("jump", Keys.space)
        assert alias.get_alias_triggered() == ["jump"]

    def test_unmapped_key_pressed_triggers_nothing(self):
        alias = Alias()
        alias.add_input(FakeInput(pressed=[Keys.escape]))
        alias.add_alias("jump", Keys.space)
        assert alias.get_alias_triggered() == []

    def test_input_not_pressing_anything_triggers_nothing(self):
        alias = Alias()
        alias.add_input(FakeInput(is_pressing=False))
        alias.add_alias("jump", Keys.space)
        assert alias.get_alias_triggered() == []

    def test_only_the_matching_alias_is_reported(self):
        alias = Alias()
        alias.add_input(FakeInput(pressed=[Keys.space]))
        alias.add_alias("jump", Keys.space)
        alias.add_alias("crouch", Keys.down)
        assert alias.get_alias_triggered() == ["jump"]

    def test_alias_with_multiple_keys_triggers_on_any_of_them(self):
        alias = Alias()
        alias.add_input(FakeInput(pressed=[Keys.up]))
        alias.add_alias("jump", Keys.space)
        alias.add_alias("jump", Keys.up)
        assert alias.get_alias_triggered() == ["jump"]

    def test_keyboard_and_joystick_can_share_the_same_alias(self):
        # Mixing Keys and Buttons under one alias is the whole point of
        # Alias - both input types are read the same way (InputModel).
        alias = Alias()
        alias.add_input(FakeInput(pressed=[Keys.space]))
        alias.add_input(FakeInput(pressed=[Buttons.a]))
        alias.add_alias("confirm", Keys.space)
        alias.add_alias("confirm", Buttons.a)
        assert alias.get_alias_triggered() == ["confirm", "confirm"]

    def test_does_not_refresh_inputs_itself(self):
        # Alias must read already-refreshed state - detect_buttons() is
        # the caller's responsibility, once per frame, the same as when
        # reading an input directly (and critically, so it doesn't eat
        # a Joystick's just-pressed edge from under Button/Modal).
        fake = FakeInput(pressed=[Keys.space])
        alias = Alias()
        alias.add_input(fake)
        alias.add_alias("jump", Keys.space)

        alias.get_alias_triggered()

        assert fake.detect_buttons_calls == 0
