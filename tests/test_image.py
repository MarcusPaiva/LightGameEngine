"""
Tests for :mod:`light_game_engine.image`.

``pygame.image.load`` and the ``fade_image`` effect are mocked out so
these tests need neither a real image file nor a real render loop.
"""
from unittest.mock import MagicMock

from light_game_engine.image import Image


class TestImage:
    def test_init_loads_the_given_file(self, mocker):
        load = mocker.patch("light_game_engine.image.pygame.image.load")
        Image("logo.png")
        load.assert_called_once_with("logo.png")

    def test_fade_converts_alpha_and_delegates_to_fade_image(self, mocker):
        loaded_image = MagicMock(name="loaded_image")
        loaded_image.convert_alpha.return_value = loaded_image
        loaded_image.get_rect.return_value = MagicMock(name="logo_rect")
        mocker.patch("light_game_engine.image.pygame.image.load", return_value=loaded_image)
        fade_image = mocker.patch("light_game_engine.image.fade_image")

        screen = MagicMock()
        screen.width.return_value = 800
        screen.height.return_value = 600

        image = Image("logo.png")
        image.fade(screen, duration=1500)

        loaded_image.get_rect.assert_called_once_with(center=(400, 300))
        fade_image.assert_called_once_with(screen, loaded_image, loaded_image.get_rect.return_value, 1500)

    def test_fade_calls_convert_alpha(self, mocker):
        loaded_image = MagicMock(name="loaded_image")
        mocker.patch("light_game_engine.image.pygame.image.load", return_value=loaded_image)
        mocker.patch("light_game_engine.image.fade_image")

        screen = MagicMock()
        screen.width.return_value = 100
        screen.height.return_value = 100

        Image("logo.png").fade(screen, duration=500)

        assert loaded_image.convert_alpha.called
