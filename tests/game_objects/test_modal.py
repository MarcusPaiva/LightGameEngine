"""
Tests for :mod:`light_game_engine.game_objects.modal`.

Modal's font defaults to pygame's built-in font (via GameFont), so no
font file is needed on disk unless a test exercises set_font(). Modal
builds real Button instances internally, so mouse polling is mocked
the same way the button tests mock it (Button.update() is called by
Modal.__process_options()).
"""
from unittest.mock import MagicMock

import pygame
import pytest

from light_game_engine.bounding_box import RectBoundingBox
from light_game_engine.game_objects.modal import Modal, Options


def mock_mouse(mocker, click=None, position=(0, 0)):
    mocker.patch("light_game_engine.game_objects.button.mouse_click_detection", return_value=click)
    mocker.patch("light_game_engine.game_objects.button.mouse_position", return_value=position)


class TestOptions:
    def test_required_fields(self):
        on_click = MagicMock()
        option = Options(text="OK", on_click=on_click)
        assert option.text == "OK"
        assert option.on_click is on_click

    def test_default_colors(self):
        option = Options(text="OK", on_click=MagicMock())
        assert option.background_color == "#cccccc"
        assert option.hover_color == "#cccccc"

    def test_custom_colors(self):
        option = Options(text="OK", on_click=MagicMock(), background_color="#ff0000", hover_color="#00ff00")
        assert option.background_color == "#ff0000"
        assert option.hover_color == "#00ff00"


class TestModalInit:
    def test_bounding_box_is_centered_and_proportional(self, make_screen):
        screen = make_screen(800, 600)
        modal = Modal(screen, "Are you sure?", width_ratio=0.6, height_ratio=0.5)

        box = modal._main_bounding_box

        assert isinstance(box, RectBoundingBox)
        assert box.width == pytest.approx(800 * 0.6)
        assert box.height == pytest.approx(600 * 0.5)
        assert box.center_x == pytest.approx(400)
        assert box.center_y == pytest.approx(300)

    def test_default_show_is_true(self, screen):
        modal = Modal(screen, "Hi")
        assert modal._show is True

    def test_show_flag_can_start_hidden(self, screen):
        modal = Modal(screen, "Hi", show=False)
        assert modal._show is False

    def test_no_options_initially(self, screen):
        modal = Modal(screen, "Hi")
        assert modal._options == []


class TestModalShow:
    def test_show_true_sets_flag(self, screen):
        modal = Modal(screen, "Hi", show=False)
        modal.show(True)
        assert modal._show is True

    def test_show_false_sets_flag(self, screen):
        modal = Modal(screen, "Hi", show=True)
        modal.show(False)
        assert modal._show is False


class TestModalAddOptions:
    def test_add_options_appends(self, screen):
        modal = Modal(screen, "Hi")
        opt1 = Options(text="OK", on_click=MagicMock())
        opt2 = Options(text="Cancel", on_click=MagicMock())

        modal.add_options([opt1])
        modal.add_options([opt2])

        assert modal._options == [opt1, opt2]


class TestModalUpdate:
    def test_update_without_options_renders_text_and_no_buttons(self, mocker, screen):
        mock_mouse(mocker)
        modal = Modal(screen, "Hello")
        modal.setup()

        modal.update()

        assert modal._button_text is not None
        assert modal._options_buttons == []

    def test_update_recomputes_bounding_box(self, mocker, make_screen):
        mock_mouse(mocker)
        screen = make_screen(800, 600)
        modal = Modal(screen, "Hi")
        modal.setup()
        first_box = modal._main_bounding_box

        modal.update()

        assert modal._main_bounding_box.bounds == first_box.bounds

    def test_update_creates_one_button_per_option(self, mocker, screen):
        mock_mouse(mocker)
        modal = Modal(screen, "Hi")
        modal.setup()
        modal.add_options([
            Options(text="OK", on_click=MagicMock()),
            Options(text="Cancel", on_click=MagicMock()),
        ])

        modal.update()

        assert len(modal._options_buttons) == 2

    def test_option_buttons_are_laid_out_left_to_right(self, mocker, screen):
        mock_mouse(mocker)
        modal = Modal(screen, "Hi")
        modal.setup()
        modal.add_options([
            Options(text="OK", on_click=MagicMock()),
            Options(text="Cancel", on_click=MagicMock()),
        ])

        modal.update()

        first, second = modal._options_buttons
        assert first._x < second._x

    def test_option_buttons_stay_within_modal_width(self, mocker, screen):
        mock_mouse(mocker)
        modal = Modal(screen, "Hi")
        modal.setup()
        modal.add_options([
            Options(text="OK", on_click=MagicMock()),
            Options(text="Cancel", on_click=MagicMock()),
        ])

        modal.update()

        box = modal._main_bounding_box
        for button in modal._options_buttons:
            content = button.content_size()
            assert button._x >= box.x0
            assert button._x + content.width <= box.x1 + 1  # tolerate rounding

    def test_option_buttons_use_their_own_colors(self, mocker, screen):
        mock_mouse(mocker)
        modal = Modal(screen, "Hi")
        modal.setup()
        modal.add_options([
            Options(text="OK", on_click=MagicMock(), background_color="#ff0000", hover_color="#00ff00"),
        ])

        modal.update()

        button = modal._options_buttons[0]
        assert button._background_color == "#ff0000"
        assert button._hover_color == "#00ff00"

    def test_option_buttons_disabled_when_modal_hidden(self, mocker, screen):
        mock_mouse(mocker)
        modal = Modal(screen, "Hi", show=False)
        modal.setup()
        on_click = MagicMock()
        modal.add_options([Options(text="OK", on_click=on_click)])

        modal.update()
        # A disabled button must not fire its callback even on a direct click.
        mock_mouse(mocker, click=(modal._options_buttons[0]._x + 1,
                                   modal._options_buttons[0]._y + 1))
        modal._options_buttons[0].update()

        on_click.assert_not_called()

    def test_option_buttons_enabled_when_modal_shown(self, mocker, screen):
        mock_mouse(mocker)
        modal = Modal(screen, "Hi", show=True)
        modal.setup()
        on_click = MagicMock()
        modal.add_options([Options(text="OK", on_click=on_click)])

        modal.update()
        button = modal._options_buttons[0]
        content = button.content_size()
        inside_point = (button._x + content.width / 2, button._y + content.height / 2)
        mock_mouse(mocker, click=inside_point)
        button.update()

        on_click.assert_called_once()

    def test_update_called_twice_replaces_buttons(self, mocker, screen):
        mock_mouse(mocker)
        modal = Modal(screen, "Hi")
        modal.setup()
        modal.add_options([Options(text="OK", on_click=MagicMock())])

        modal.update()
        first_buttons = modal._options_buttons
        modal.update()
        second_buttons = modal._options_buttons

        assert first_buttons is not second_buttons
        assert len(second_buttons) == 1


class TestModalDraw:
    def test_draw_when_shown_draws_box_and_text(self, mocker, screen):
        mock_mouse(mocker)
        draw_rect = mocker.patch("light_game_engine.game_artfacts_2d.pygame.draw.rect")
        modal = Modal(screen, "Hi", show=True)
        modal.setup()
        modal.update()

        modal.draw()

        assert draw_rect.call_count == 2  # margin rect + background rect
        assert len(screen.draw_calls) == 1  # modal text

    def test_draw_when_hidden_draws_nothing(self, mocker, screen):
        mock_mouse(mocker)
        draw_rect = mocker.patch("light_game_engine.game_artfacts_2d.pygame.draw.rect")
        modal = Modal(screen, "Hi", show=False)
        modal.setup()
        modal.update()

        modal.draw()

        draw_rect.assert_not_called()
        assert screen.draw_calls == []

    def test_draw_also_draws_each_option_button(self, mocker, screen):
        mock_mouse(mocker)
        draw_rect = mocker.patch("light_game_engine.game_artfacts_2d.pygame.draw.rect")
        modal = Modal(screen, "Hi", show=True)
        modal.setup()
        modal.add_options([
            Options(text="OK", on_click=MagicMock()),
            Options(text="Cancel", on_click=MagicMock()),
        ])
        modal.update()

        modal.draw()

        # 2 modal rects + 1 rect per option button
        assert draw_rect.call_count == 2 + 2
        # 1 modal text blit + 1 text blit per option button
        assert len(screen.draw_calls) == 1 + 2


class TestModalSetFont:
    def test_set_font_returns_self(self, screen):
        modal = Modal(screen, "Hi")
        assert modal.set_font("custom.ttf") is modal

    def test_without_set_font_setup_uses_the_system_default(self, mocker, screen):
        font_ctor = mocker.patch("light_game_engine.font.pygame.font.Font", wraps=pygame.font.Font)
        modal = Modal(screen, "Hi", font_size=40)
        modal.setup()
        font_ctor.assert_called_once_with(None, 40)

    def test_set_font_makes_setup_load_the_given_path(self, mocker, screen):
        # "custom.ttf" doesn't exist on disk, so pygame.font.Font itself is
        # mocked out here (not wrapped). setup() builds the default font
        # first and then swaps in the custom one, so the custom path
        # should be the *last* call, not the only one.
        font_ctor = mocker.patch("light_game_engine.font.pygame.font.Font")
        modal = Modal(screen, "Hi", font_size=40)
        modal.set_font("custom.ttf")

        modal.setup()

        font_ctor.assert_called_with("custom.ttf", 40)
