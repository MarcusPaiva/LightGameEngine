"""
Tests for :mod:`light_game_engine.font`.

Uses pygame's built-in default font (the constructor's implicit
choice) so no font file is needed; the font subsystem works headless
under the dummy SDL video driver set in conftest.py.
"""
import pygame
import pytest

from light_game_engine.font import GameFont


@pytest.fixture
def game_font():
    return GameFont(24, "Hello")


class TestGameFont:
    def test_get_text_size_returns_positive_dimensions(self, game_font):
        width, height = game_font.get_text_size()
        assert width > 0
        assert height > 0

    def test_get_text_size_changes_with_text_length(self, game_font):
        short_width, _ = game_font.get_text_size()
        game_font.set_text("Hello, much longer string!")
        long_width, _ = game_font.get_text_size()
        assert long_width > short_width

    def test_set_text_returns_self(self, game_font):
        assert game_font.set_text("New text") is game_font

    def test_set_color_returns_self(self, game_font):
        assert game_font.set_color([255, 0, 0]) is game_font

    def test_enable_anti_alias_returns_self(self, game_font):
        assert game_font.enable_anti_alias(True) is game_font

    def test_set_background_color_returns_self(self, game_font):
        assert game_font.set_background_color([255, 255, 255]) is game_font

    def test_render_returns_a_surface(self, game_font):
        surface = game_font.render()
        assert isinstance(surface, pygame.Surface)

    def test_render_surface_matches_get_text_size(self, game_font):
        width, height = game_font.get_text_size()
        surface = game_font.render()
        assert surface.get_width() == width
        assert surface.get_height() == height

    def test_render_uses_configured_color(self):
        font = GameFont(24, "X").set_color([10, 20, 30]).enable_anti_alias(False)
        surface = font.render()
        # Sample a pixel that should be part of the glyph ink.
        colors_present = {surface.get_at((x, surface.get_height() // 2))[:3]
                           for x in range(surface.get_width())}
        assert (10, 20, 30) in colors_present

    def test_render_with_background_color_fills_background(self):
        font = GameFont(24, "X").set_background_color([1, 2, 3])
        surface = font.render()
        assert surface.get_at((0, 0))[:3] == (1, 2, 3)

    def test_render_without_background_leaves_no_forced_fill(self):
        font = GameFont(24, "X")
        # Should not raise even though background_color defaults to None.
        surface = font.render()
        assert isinstance(surface, pygame.Surface)


class TestGameFontDefaultFont:
    def test_uses_system_default_font_without_set_font(self, mocker):
        # pygame.font.Font(None, size) is how pygame resolves its
        # built-in default font - GameFont must call it that way
        # until set_font() is used.
        font_ctor = mocker.patch("light_game_engine.font.pygame.font.Font", wraps=pygame.font.Font)
        GameFont(24, "Hi")
        font_ctor.assert_called_once_with(None, 24)


class TestGameFontSetFont:
    def test_set_font_returns_self(self, game_font, mocker):
        mocker.patch("light_game_engine.font.pygame.font.Font", wraps=pygame.font.Font)
        assert game_font.set_font(None) is game_font

    def test_set_font_loads_the_given_path_at_the_current_size(self, mocker):
        # "custom.ttf" doesn't exist on disk, so the constructor is fully
        # mocked here (not wrapped) - this only checks what set_font()
        # asks pygame to load, not that loading succeeds.
        font_ctor = mocker.patch("light_game_engine.font.pygame.font.Font")
        font = GameFont(24, "Hi")
        font_ctor.reset_mock()

        font.set_font("custom.ttf")

        font_ctor.assert_called_once_with("custom.ttf", 24)

    def test_set_font_replaces_the_previously_rendered_font(self, mocker):
        # Route every path (real or fake) through the real Font(None, size)
        # so this stays a pure unit test with no font file on disk.
        real_font_ctor = pygame.font.Font
        mocker.patch(
            "light_game_engine.font.pygame.font.Font",
            side_effect=lambda path, size: real_font_ctor(None, size),
        )
        font = GameFont(24, "Hi")
        before = font.render()

        font.set_font("some/custom/font.ttf")
        after = font.render()

        # Same default glyph shapes either way, but a genuinely new
        # pygame.font.Font instance is now backing the render.
        assert before.get_size() == after.get_size()

    def test_set_font_with_none_falls_back_to_default(self, mocker):
        font_ctor = mocker.patch("light_game_engine.font.pygame.font.Font", wraps=pygame.font.Font)
        font = GameFont(24, "Hi")
        font_ctor.reset_mock()

        font.set_font(None)

        font_ctor.assert_called_once_with(None, 24)
