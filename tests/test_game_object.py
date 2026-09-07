"""
Tests for :mod:`light_game_engine.GameObject`.
"""
import pytest

from light_game_engine.game_objects.GameObject import GameObject
from light_game_engine.bounding_box import RectBoundingBox


class ConcreteGameObject(GameObject):
    """Minimal concrete implementation used to exercise the contract."""

    def __init__(self):
        self.update_calls = 0
        self.draw_calls = 0
        self._position = RectBoundingBox(0, 0, 10, 10)
        self._sprite = None

    def update(self):
        self.update_calls += 1

    @property
    def position(self):
        return self._position

    def draw(self):
        self.draw_calls += 1
        self._sprite = self._position.copy()

    @property
    def sprite(self):
        return self._sprite


class TestGameObjectAbstract:
    def test_cannot_instantiate_directly(self):
        with pytest.raises(TypeError):
            GameObject()

    def test_subclass_missing_methods_cannot_instantiate(self):
        class Incomplete(GameObject):
            def update(self):
                pass

        with pytest.raises(TypeError):
            Incomplete()


class TestConcreteGameObject:
    def test_update_is_callable(self):
        obj = ConcreteGameObject()
        obj.update()
        assert obj.update_calls == 1

    def test_position_returns_bounding_box(self):
        obj = ConcreteGameObject()
        assert isinstance(obj.position, RectBoundingBox)

    def test_sprite_is_none_before_draw(self):
        obj = ConcreteGameObject()
        assert obj.sprite is None

    def test_draw_sets_sprite(self):
        obj = ConcreteGameObject()
        obj.draw()
        assert obj.draw_calls == 1
        assert obj.sprite is not None
        assert obj.sprite.bounds == obj.position.bounds
