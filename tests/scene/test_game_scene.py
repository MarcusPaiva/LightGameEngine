"""
Tests for :mod:`light_game_engine.scene.game_scene`.
"""
import pytest

from light_game_engine.scene.game_scene import GameScene


class ConcreteScene(GameScene):
    """Minimal concrete implementation used to exercise the contract."""

    def __init__(self, screen):
        self.screen = screen
        self.setup_calls = 0
        self.loop_calls = 0
        self.reset_calls = 0

    def setup(self):
        self.setup_calls += 1

    def loop(self):
        self.loop_calls += 1

    def reset(self):
        self.reset_calls += 1


class TestGameSceneAbstract:
    def test_cannot_instantiate_directly(self):
        with pytest.raises(TypeError):
            GameScene(screen=None)

    def test_subclass_missing_methods_cannot_instantiate(self):
        class Incomplete(GameScene):
            def __init__(self, screen):
                pass

            def setup(self):
                pass

            # loop() and reset() are missing on purpose.

        with pytest.raises(TypeError):
            Incomplete(screen=None)


class TestConcreteGameScene:
    def test_setup_is_callable(self):
        scene = ConcreteScene(screen="fake-screen")
        scene.setup()
        assert scene.setup_calls == 1

    def test_loop_is_callable(self):
        scene = ConcreteScene(screen="fake-screen")
        scene.loop()
        assert scene.loop_calls == 1

    def test_reset_is_callable(self):
        scene = ConcreteScene(screen="fake-screen")
        scene.reset()
        assert scene.reset_calls == 1
