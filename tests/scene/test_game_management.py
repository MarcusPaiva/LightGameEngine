"""
Tests for :mod:`light_game_engine.scene.game_management`.

Several tests here are regression tests for two bugs found in review:
GameStatus/SceneManagement silently resetting their state on every
call (defeating the whole point of being a singleton), and
GameManagement.loop() crashing after a pygame.QUIT event instead of
exiting cleanly.
"""
from unittest.mock import MagicMock

import pygame
import pytest

from light_game_engine.scene.game_scene import GameScene
from light_game_engine.scene.game_management import GameManagement, GameStatus, SceneManagement


class FakeScene(GameScene):
    """Minimal scene that counts how many times each method is called."""

    def __init__(self, screen=None):
        self._screen = screen
        self.setup_calls = 0
        self.loop_calls = 0
        self.reset_calls = 0

    def setup(self):
        self.setup_calls += 1

    def loop(self):
        self.loop_calls += 1

    def reset(self):
        self.reset_calls += 1


class TestGameStatusSingleton:
    def test_repeated_calls_return_the_same_instance(self):
        assert GameStatus() is GameStatus()

    def test_defaults(self):
        status = GameStatus()
        assert status.game_is_running is True
        assert status.game_paused is False

    def test_state_survives_across_separate_lookups(self):
        # Regression test: __init__ used to re-run on every GameStatus()
        # call - even though __new__ returns the same object - silently
        # resetting _paused/_game_is_running back to their defaults.
        GameStatus().set_pause_game(True)
        assert GameStatus().game_paused is True

    def test_set_game_is_running(self):
        GameStatus().set_game_is_running(False)
        assert GameStatus().game_is_running is False

    def test_set_pause_game(self):
        GameStatus().set_pause_game(True)
        assert GameStatus().game_paused is True
        GameStatus().set_pause_game(False)
        assert GameStatus().game_paused is False


class TestSceneManagementSingleton:
    def test_repeated_calls_return_the_same_instance(self):
        assert SceneManagement() is SceneManagement()

    def test_starts_with_no_scenes(self):
        assert SceneManagement().list_scene() == []
        assert SceneManagement().get_current_scene_name == ""

    def test_scenes_survive_across_separate_lookups(self):
        # Regression test: __init__ used to re-run on every
        # SceneManagement() call, silently wiping _scenes and
        # _current_scene back to empty.
        scene = FakeScene()
        SceneManagement().add_scene("menu", scene)

        assert SceneManagement().list_scene() == ["menu"]
        assert SceneManagement().get_current_scene() is scene


class TestSceneManagementAddScene:
    def test_add_scene_returns_self(self):
        sm = SceneManagement()
        assert sm.add_scene("menu", FakeScene()) is sm

    def test_first_scene_added_becomes_current(self):
        sm = SceneManagement()
        sm.add_scene("menu", FakeScene())
        assert sm.get_current_scene_name == "menu"

    def test_second_scene_added_does_not_change_current(self):
        sm = SceneManagement()
        sm.add_scene("menu", FakeScene())
        sm.add_scene("level1", FakeScene())
        assert sm.get_current_scene_name == "menu"

    def test_list_scene_lists_every_registered_name(self):
        sm = SceneManagement()
        sm.add_scene("menu", FakeScene())
        sm.add_scene("level1", FakeScene())
        assert set(sm.list_scene()) == {"menu", "level1"}


class TestSceneManagementSwitching:
    def test_set_current_scene_returns_self(self):
        sm = SceneManagement()
        sm.add_scene("menu", FakeScene())
        assert sm.set_current_scene("menu") is sm

    def test_set_current_scene_switches(self):
        sm = SceneManagement()
        sm.add_scene("menu", FakeScene())
        level = FakeScene()
        sm.add_scene("level1", level)

        sm.set_current_scene("level1")

        assert sm.get_current_scene_name == "level1"
        assert sm.get_current_scene() is level

    def test_get_scene_by_name(self):
        sm = SceneManagement()
        menu = FakeScene()
        sm.add_scene("menu", menu)
        assert sm.get_scene("menu") is menu

    def test_get_scene_unknown_name_returns_none(self):
        assert SceneManagement().get_scene("does-not-exist") is None

    def test_reset_current_scene_returns_self(self):
        sm = SceneManagement()
        sm.add_scene("menu", FakeScene())
        assert sm.reset_current_scene() is sm

    def test_reset_current_scene_calls_reset_on_the_active_scene_only(self):
        sm = SceneManagement()
        menu = FakeScene()
        level = FakeScene()
        sm.add_scene("menu", menu)
        sm.add_scene("level1", level)
        sm.set_current_scene("level1")

        sm.reset_current_scene()

        assert level.reset_calls == 1
        assert menu.reset_calls == 0


class TestSceneManagementSetup:
    def test_setup_scenes_returns_self(self):
        sm = SceneManagement()
        assert sm.setup_scenes() is sm

    def test_setup_scenes_calls_setup_on_every_scene(self):
        sm = SceneManagement()
        menu = FakeScene()
        level = FakeScene()
        sm.add_scene("menu", menu)
        sm.add_scene("level1", level)

        sm.setup_scenes()

        assert menu.setup_calls == 1
        assert level.setup_calls == 1


class TestGameManagementSetup:
    def test_setup_delegates_to_scene_management_and_returns_self(self):
        screen = MagicMock()
        scene = FakeScene(screen)
        SceneManagement().add_scene("main", scene)
        gm = GameManagement(screen)

        result = gm.setup()

        assert result is gm
        assert scene.setup_calls == 1

    def test_current_screen_returns_the_active_scene_name(self):
        screen = MagicMock()
        SceneManagement().add_scene("main", FakeScene(screen))
        gm = GameManagement(screen)

        assert gm.current_screen == "main"

    def test_registering_scenes_before_construction_still_works(self):
        # Regression test: GameManagement.__init__() calls
        # SceneManagement() again internally - before the singleton fix,
        # that wiped out any scene registered beforehand.
        screen = MagicMock()
        scene = FakeScene(screen)
        SceneManagement().add_scene("main", scene)

        gm = GameManagement(screen)

        assert SceneManagement().get_current_scene() is scene
        assert gm.current_screen == "main"


class TestGameManagementExitGame:
    def test_exit_game_flags_the_status_without_touching_the_screen(self):
        screen = MagicMock()
        SceneManagement().add_scene("main", FakeScene(screen))
        gm = GameManagement(screen)

        gm.exit_game()

        assert GameStatus().game_is_running is False
        screen.quit.assert_not_called()


class TestGameManagementLoop:
    def test_runs_the_active_scene_once_per_frame_until_stopped(self, mocker):
        mocker.patch("light_game_engine.scene.game_management.pygame.event.get", return_value=[])
        screen = MagicMock()
        scene = FakeScene(screen)
        SceneManagement().add_scene("main", scene)
        gm = GameManagement(screen)

        # Stop the otherwise-infinite loop after 3 frames.
        calls = {"n": 0}
        real_loop = scene.loop

        def loop_then_maybe_stop():
            real_loop()
            calls["n"] += 1
            if calls["n"] >= 3:
                gm.exit_game()

        scene.loop = loop_then_maybe_stop

        gm.loop()

        assert scene.loop_calls == 3
        assert screen.flip.call_count == 3
        screen.quit.assert_called_once()

    def test_never_updates_the_scene_while_paused(self, mocker):
        screen = MagicMock()
        scene = FakeScene(screen)
        SceneManagement().add_scene("main", scene)
        gm = GameManagement(screen)
        GameStatus().set_pause_game(True)

        # Stop after 2 paused frames - only pygame.event.get() runs
        # while paused, so that's where we inject the exit.
        ticks = {"n": 0}

        def fake_events():
            ticks["n"] += 1
            if ticks["n"] >= 2:
                gm.exit_game()
            return []

        mocker.patch(
            "light_game_engine.scene.game_management.pygame.event.get",
            side_effect=fake_events,
        )

        gm.loop()

        assert scene.loop_calls == 0
        screen.flip.assert_not_called()
        screen.quit.assert_called_once()

    def test_stops_cleanly_on_pygame_quit_event(self, mocker):
        # Regression test: exit_game() used to call screen.quit()
        # (pygame.quit()) immediately, but the while loop kept running
        # since nothing set game_is_running to False - the next pygame
        # call then crashed with "video system not initialized".
        quit_event = MagicMock()
        quit_event.type = pygame.QUIT
        mocker.patch(
            "light_game_engine.scene.game_management.pygame.event.get",
            return_value=[quit_event],
        )
        screen = MagicMock()
        scene = FakeScene(screen)
        SceneManagement().add_scene("main", scene)
        gm = GameManagement(screen)

        gm.loop()  # must return normally, not raise

        assert GameStatus().game_is_running is False
        assert scene.loop_calls == 1  # the frame already in progress still finishes
        screen.quit.assert_called_once()
