"""
Tests for :mod:`light_game_engine.screen`.

Runs against a real pygame display surface backed by the dummy SDL
video driver (set in conftest.py), so no actual window is opened.
"""
import pygame
import pytest

from light_game_engine.screen import SurfaceScreen


@pytest.fixture
def screen():
    s = SurfaceScreen(320, 240, "Test Window")
    yield s
    s.quit()


class TestSurfaceScreen:
    def test_init_sets_window_size(self, screen):
        assert screen.width() == 320
        assert screen.height() == 240

    def test_init_sets_window_title(self, screen):
        assert pygame.display.get_caption()[0] == "Test Window"

    def test_get_screen_returns_a_surface(self, screen):
        assert isinstance(screen.get_screen(), pygame.Surface)

    def test_fill_returns_self(self, screen):
        assert screen.fill("black") is screen

    def test_fill_actually_fills_the_surface(self, screen):
        screen.fill((10, 20, 30))
        assert screen.get_screen().get_at((0, 0))[:3] == (10, 20, 30)

    def test_draw_returns_self(self, screen):
        artifact = pygame.Surface((10, 10))
        assert screen.draw(artifact, [0, 0]) is screen

    def test_draw_blits_onto_the_screen(self, screen):
        artifact = pygame.Surface((10, 10))
        artifact.fill((255, 0, 0))
        screen.draw(artifact, [5, 5])
        assert screen.get_screen().get_at((5, 5))[:3] == (255, 0, 0)

    def test_flip_returns_self(self, screen):
        assert screen.flip() is screen

    def test_set_clock_returns_self(self, screen):
        assert screen.set_clock(60) is screen

    def test_quit_returns_self(self):
        s = SurfaceScreen(100, 100, "Quit Test")
        assert s.quit() is s
