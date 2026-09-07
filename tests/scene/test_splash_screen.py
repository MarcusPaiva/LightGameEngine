"""
Tests for :mod:`light_game_engine.scene.SplashScreen`.

``pygame.image.load`` is mocked so no real image file is needed. The
fade effect itself (``Image.fade``) is already covered by
test_image.py/test_image_effects.py, so here it's mocked too - these
tests only check that SplashScreen calls it correctly.
"""
from unittest.mock import MagicMock

from light_game_engine.scene.SplashScreen import SplashScreen


class TestSplashScreenSetup:
    def test_loads_the_logo_image(self, mocker):
        load = mocker.patch("light_game_engine.image.pygame.image.load")
        splash = SplashScreen(MagicMock(), "logo.png")

        splash.setup()

        load.assert_called_once_with("logo.png")

    def test_plays_the_intro_sound_when_given(self, mocker):
        mocker.patch("light_game_engine.image.pygame.image.load")
        sound_effect = mocker.patch("light_game_engine.scene.SplashScreen.SoundEffect")
        splash = SplashScreen(MagicMock(), "logo.png", "intro.wav")

        splash.setup()

        sound_effect.assert_called_once_with("intro.wav")
        sound_effect.return_value.play.assert_called_once()

    def test_does_not_touch_sound_when_none(self, mocker):
        mocker.patch("light_game_engine.image.pygame.image.load")
        sound_effect = mocker.patch("light_game_engine.scene.SplashScreen.SoundEffect")
        splash = SplashScreen(MagicMock(), "logo.png")  # no sound_intro_effect

        splash.setup()  # must not raise

        sound_effect.assert_not_called()


class TestSplashScreenLoop:
    def test_fades_the_logo_for_2500ms(self, mocker):
        mocker.patch("light_game_engine.image.pygame.image.load")
        fade = mocker.patch("light_game_engine.image.Image.fade")
        screen = MagicMock()
        splash = SplashScreen(screen, "logo.png")
        splash.setup()

        splash.loop()

        fade.assert_called_once_with(screen, 2500)


class TestSplashScreenReset:
    def test_reset_does_not_raise(self, mocker):
        mocker.patch("light_game_engine.image.pygame.image.load")
        splash = SplashScreen(MagicMock(), "logo.png")
        splash.setup()

        splash.reset()  # nothing to assert - just must not raise
