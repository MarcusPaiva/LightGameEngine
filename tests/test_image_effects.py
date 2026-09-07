"""
Tests for :mod:`light_game_engine.image_effects`.

``pygame.time.Clock.tick`` is mocked to return a fixed, large delta so
the fade loop completes in exactly two iterations instead of racing a
real clock.
"""
import sys
from unittest.mock import MagicMock

import pygame
import pytest

from light_game_engine.image_effects import fade_image


@pytest.fixture
def fast_clock(mocker):
    """Make every Clock.tick() advance the fade loop by a full duration."""
    clock = MagicMock()
    clock.tick.return_value = 2000
    mocker.patch("light_game_engine.image_effects.pygame.time.Clock", return_value=clock)
    return clock


@pytest.fixture
def no_events(mocker):
    mocker.patch("light_game_engine.image_effects.pygame.event.get", return_value=[])


class TestFadeImage:
    def test_runs_to_completion_and_flips_screen(self, fast_clock, no_events):
        screen = MagicMock()
        image = pygame.Surface((10, 10), pygame.SRCALPHA)
        rect = image.get_rect()

        fade_image(screen, image, rect, duration=2000)

        assert screen.fill.called
        assert screen.draw.called
        assert screen.flip.called

    def test_draws_once_per_clock_tick(self, fast_clock, no_events):
        screen = MagicMock()
        image = pygame.Surface((10, 10), pygame.SRCALPHA)
        rect = image.get_rect()

        fade_image(screen, image, rect, duration=2000)

        # One fade-in tick + one fade-out tick, at 2000ms/tick.
        assert screen.flip.call_count == 2

    def test_draw_receives_an_alpha_surface_matching_image_size(self, fast_clock, no_events):
        screen = MagicMock()
        image = pygame.Surface((32, 16), pygame.SRCALPHA)
        rect = image.get_rect()

        fade_image(screen, image, rect, duration=2000)

        drawn_surface, drawn_rect = screen.draw.call_args_list[0][0]
        assert isinstance(drawn_surface, pygame.Surface)
        assert drawn_surface.get_size() == (32, 16)
        assert drawn_rect is rect

    def test_quits_on_pygame_quit_event(self, fast_clock, mocker):
        quit_event = MagicMock()
        quit_event.type = pygame.QUIT
        mocker.patch("light_game_engine.image_effects.pygame.event.get", return_value=[quit_event])
        pygame_quit = mocker.patch("light_game_engine.image_effects.pygame.quit")
        mocker.patch("light_game_engine.image_effects.sys.exit", side_effect=SystemExit)

        screen = MagicMock()
        image = pygame.Surface((10, 10), pygame.SRCALPHA)
        rect = image.get_rect()

        with pytest.raises(SystemExit):
            fade_image(screen, image, rect, duration=2000)

        pygame_quit.assert_called_once()

    def test_default_duration_is_2000ms(self, fast_clock, no_events):
        # With the mocked 2000ms-per-tick clock, the default duration
        # should also resolve in exactly two ticks.
        screen = MagicMock()
        image = pygame.Surface((10, 10), pygame.SRCALPHA)
        rect = image.get_rect()

        fade_image(screen, image, rect)

        assert screen.flip.call_count == 2
