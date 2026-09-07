"""
Tests for :mod:`light_game_engine.game_artfacts_2d`.

``pygame.draw.rect``/``pygame.draw.circle`` are mocked out so these tests
never need a real display surface.
"""
from unittest.mock import MagicMock

from light_game_engine.bounding_box import RectBoundingBox, CircleBoundingBox
from light_game_engine.game_artfacts_2d import Rect, Circle


class FakeScreen:
    """Stand-in for SurfaceScreen exposing only get_screen()."""

    def __init__(self):
        self.surface = MagicMock(name="pygame.Surface")

    def get_screen(self):
        return self.surface


class TestRect:
    def test_default_fill_color(self, mocker):
        draw_rect = mocker.patch("light_game_engine.game_artfacts_2d.pygame.draw.rect")
        rect = Rect(0, 0, 10, 10)
        screen = FakeScreen()
        rect.render(screen)
        assert draw_rect.call_args[0][1] == "red"

    def test_set_fill_color_returns_self_and_is_used_on_render(self, mocker):
        draw_rect = mocker.patch("light_game_engine.game_artfacts_2d.pygame.draw.rect")
        rect = Rect(0, 0, 10, 10)
        result = rect.set_fill_color("blue")
        assert result is rect
        rect.render(FakeScreen())
        assert draw_rect.call_args[0][1] == "blue"

    def test_render_draws_on_given_screen_surface(self, mocker):
        draw_rect = mocker.patch("light_game_engine.game_artfacts_2d.pygame.draw.rect")
        screen = FakeScreen()
        Rect(5, 10, 20, 30).render(screen)
        args = draw_rect.call_args[0]
        assert args[0] is screen.surface
        assert args[2] == [5, 10, 20, 30]
        assert args[3] == 0

    def test_render_returns_a_copy_of_the_bounding_box(self, mocker):
        mocker.patch("light_game_engine.game_artfacts_2d.pygame.draw.rect")
        rect = Rect(5, 10, 20, 30)
        result = rect.render(FakeScreen())
        assert isinstance(result, RectBoundingBox)
        assert result.bounds == (5, 10, 25, 40)

    def test_render_returns_different_instance_each_call(self, mocker):
        mocker.patch("light_game_engine.game_artfacts_2d.pygame.draw.rect")
        rect = Rect(0, 0, 1, 1)
        screen = FakeScreen()
        first = rect.render(screen)
        second = rect.render(screen)
        assert first is not second
        assert first.bounds == second.bounds


class TestCircle:
    def test_default_fill_color(self, mocker):
        draw_circle = mocker.patch("light_game_engine.game_artfacts_2d.pygame.draw.circle")
        Circle(50, 50, 10).render(FakeScreen())
        assert draw_circle.call_args[0][1] == "red"

    def test_set_fill_color_returns_self_and_is_used_on_render(self, mocker):
        draw_circle = mocker.patch("light_game_engine.game_artfacts_2d.pygame.draw.circle")
        circle = Circle(50, 50, 10)
        result = circle.set_fill_color("green")
        assert result is circle
        circle.render(FakeScreen())
        assert draw_circle.call_args[0][1] == "green"

    def test_render_draws_on_given_screen_surface_with_center_and_radius(self, mocker):
        draw_circle = mocker.patch("light_game_engine.game_artfacts_2d.pygame.draw.circle")
        screen = FakeScreen()
        Circle(50, 60, 10).render(screen)
        args = draw_circle.call_args[0]
        assert args[0] is screen.surface
        assert args[2] == [50, 60]
        assert args[3] == 10

    def test_render_returns_a_copy_of_the_bounding_box(self, mocker):
        mocker.patch("light_game_engine.game_artfacts_2d.pygame.draw.circle")
        circle = Circle(50, 60, 10)
        result = circle.render(FakeScreen())
        assert isinstance(result, CircleBoundingBox)
        assert result.center == [50, 60]
        assert result.radius == 10
