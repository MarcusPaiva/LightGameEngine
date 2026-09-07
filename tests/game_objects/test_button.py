"""
Tests for :mod:`light_game_engine.game_objects.button`.

Button's font defaults to pygame's built-in font (via GameFont), so no
font file is needed on disk unless a test exercises set_font() with a
custom path, in which case pygame.font.Font is patched locally. Mouse
polling and pygame.draw.rect are mocked per-test so behavior is
deterministic.
"""
from unittest.mock import MagicMock

import pygame
import pytest

from light_game_engine.bounding_box import RectBoundingBox
from light_game_engine.font import GameFont
from light_game_engine.game_objects.button import Button


def make_button(screen, x=100, y=100, text="Hi", **kwargs):
    button = Button(screen, x, y, text, **kwargs)
    button.setup()
    return button


def mock_mouse(mocker, click=None, position=(0, 0)):
    mocker.patch("light_game_engine.game_objects.button.mouse_click_detection", return_value=click)
    mocker.patch("light_game_engine.game_objects.button.mouse_position", return_value=position)


class TestButtonInit:
    def test_default_margin(self, screen):
        button = Button(screen, 0, 0, "Hi")
        assert button.margin == 10

    def test_custom_margin(self, screen):
        button = Button(screen, 0, 0, "Hi", margin=5)
        assert button.margin == 5


class TestButtonContentSize:
    def test_content_size_matches_text_plus_margins(self, screen):
        button = make_button(screen, text="Hi", margin=10, font_size=40)
        text_width, text_height = GameFont(40, "Hi").get_text_size()

        size = button.content_size()

        assert isinstance(size, RectBoundingBox)
        assert size.initial_position == [0, 0]
        assert size.width == text_width + 20
        assert size.height == text_height + 20

    def test_content_size_grows_with_longer_text(self, screen):
        short = make_button(screen, text="Hi").content_size().width
        long = make_button(screen, text="Hello, world!").content_size().width
        assert long > short

    def test_content_size_is_position_independent(self, screen):
        a = make_button(screen, x=0, y=0, text="Hi").content_size()
        b = make_button(screen, x=500, y=500, text="Hi").content_size()
        assert a.bounds == b.bounds


class TestButtonSetPosition:
    def test_update_places_box_around_new_position(self, mocker, screen):
        mock_mouse(mocker)
        button = make_button(screen, x=0, y=0, text="Hi", margin=10)
        button.set_position(200, 300)
        button.update()

        assert button._main_bounding_box.x0 == 190  # 200 - margin
        assert button._main_bounding_box.y0 == 290  # 300 - margin

    def test_set_position_does_not_change_text_or_margin(self, mocker, screen):
        mock_mouse(mocker)
        button = make_button(screen, text="Hi", margin=10)
        button.set_position(50, 50)
        assert button.margin == 10


class TestButtonClick:
    def test_click_inside_box_triggers_on_click(self, mocker, screen):
        on_click = MagicMock()
        button = make_button(screen, x=100, y=100, text="Hi", on_click=on_click)
        mock_mouse(mocker, click=(105, 105))

        button.update()

        on_click.assert_called_once()

    def test_click_outside_box_does_not_trigger_on_click(self, mocker, screen):
        on_click = MagicMock()
        button = make_button(screen, x=100, y=100, text="Hi", on_click=on_click)
        mock_mouse(mocker, click=(0, 0))

        button.update()

        on_click.assert_not_called()

    def test_no_click_does_not_trigger_on_click(self, mocker, screen):
        on_click = MagicMock()
        button = make_button(screen, x=100, y=100, text="Hi", on_click=on_click)
        mock_mouse(mocker, click=None)

        button.update()

        on_click.assert_not_called()

    def test_disabled_button_ignores_clicks(self, mocker, screen):
        on_click = MagicMock()
        button = make_button(screen, x=100, y=100, text="Hi", on_click=on_click)
        button.disable(True)
        mock_mouse(mocker, click=(105, 105))

        button.update()

        on_click.assert_not_called()

    def test_re_enabling_restores_click_handling(self, mocker, screen):
        on_click = MagicMock()
        button = make_button(screen, x=100, y=100, text="Hi", on_click=on_click)
        button.disable(True)
        button.disable(False)
        mock_mouse(mocker, click=(105, 105))

        button.update()

        on_click.assert_called_once()

    def test_no_on_click_callback_does_not_raise(self, mocker, screen):
        button = make_button(screen, x=100, y=100, text="Hi")
        mock_mouse(mocker, click=(105, 105))
        button.update()  # should not raise


class TestButtonHover:
    def test_hovering_inside_box_sets_hover_true(self, mocker, screen):
        button = make_button(screen, x=100, y=100, text="Hi")
        mock_mouse(mocker, position=(105, 105))
        button.update()
        assert button._hover

    def test_not_hovering_outside_box_sets_hover_falsy(self, mocker, screen):
        button = make_button(screen, x=100, y=100, text="Hi")
        mock_mouse(mocker, position=(0, 0))
        button.update()
        assert not button._hover


class TestButtonDraw:
    def test_draw_uses_background_color_when_not_hovering(self, mocker, screen):
        draw_rect = mocker.patch("light_game_engine.game_artfacts_2d.pygame.draw.rect")
        button = make_button(screen, x=100, y=100, text="Hi")
        button.background_color("#111111")
        mock_mouse(mocker, position=(0, 0))
        button.update()
        button.draw()
        assert draw_rect.call_args[0][1] == "#111111"

    def test_draw_uses_hover_color_when_hovering(self, mocker, screen):
        draw_rect = mocker.patch("light_game_engine.game_artfacts_2d.pygame.draw.rect")
        button = make_button(screen, x=100, y=100, text="Hi")
        button.hover_color("#222222")
        mock_mouse(mocker, position=(105, 105))
        button.update()
        button.draw()
        assert draw_rect.call_args[0][1] == "#222222"

    def test_default_background_color(self, mocker, screen):
        draw_rect = mocker.patch("light_game_engine.game_artfacts_2d.pygame.draw.rect")
        button = make_button(screen, x=100, y=100, text="Hi")
        mock_mouse(mocker, position=(0, 0))
        button.update()
        button.draw()
        assert draw_rect.call_args[0][1] == "#cccccc"

    def test_draw_blits_the_rendered_text_onto_the_screen(self, mocker, screen):
        mocker.patch("light_game_engine.game_artfacts_2d.pygame.draw.rect")
        button = make_button(screen, x=100, y=100, text="Hi")
        mock_mouse(mocker, position=(0, 0))
        button.update()
        button.draw()

        assert len(screen.draw_calls) == 1
        drawn_surface, drawn_position = screen.draw_calls[0]
        assert isinstance(drawn_surface, pygame.Surface)
        assert len(drawn_position) == 2

    def test_draw_centers_text_within_the_button_box(self, mocker, screen):
        mocker.patch("light_game_engine.game_artfacts_2d.pygame.draw.rect")
        button = make_button(screen, x=100, y=100, text="Hi", margin=10)
        mock_mouse(mocker, position=(0, 0))
        button.update()
        button.draw()

        _, (text_x, text_y) = screen.draw_calls[0]
        box = button._main_bounding_box
        assert box.x0 < text_x < box.x1
        assert box.y0 < text_y < box.y1


class TestButtonSetFont:
    def test_set_font_returns_self(self, screen):
        button = Button(screen, 0, 0, "Hi")
        assert button.set_font("custom.ttf") is button

    def test_without_set_font_setup_uses_the_system_default(self, mocker, screen):
        font_ctor = mocker.patch("light_game_engine.font.pygame.font.Font", wraps=pygame.font.Font)
        make_button(screen, text="Hi", font_size=40)
        font_ctor.assert_called_once_with(None, 40)

    def test_set_font_makes_setup_load_the_given_path(self, mocker, screen):
        # "custom.ttf" doesn't exist on disk, so pygame.font.Font itself is
        # mocked out here (not wrapped) - this only checks what setup()
        # asks pygame to load, not that loading succeeds. setup() builds
        # the default font first and then swaps in the custom one, so the
        # custom path should be the *last* call, not the only one.
        font_ctor = mocker.patch("light_game_engine.font.pygame.font.Font")
        button = Button(screen, 0, 0, "Hi", font_size=40)
        button.set_font("custom.ttf")

        button.setup()

        font_ctor.assert_called_with("custom.ttf", 40)
