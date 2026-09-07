"""
A splash-screen scene: shows a logo that fades in and out, with an
optional sound effect.
"""
from light_game_engine.image import Image
from light_game_engine.screen import SurfaceScreen
from light_game_engine.sound import SoundEffect
from light_game_engine.scene.game_scene import GameScene


class SplashScreen(GameScene):
    """
    A scene that fades a logo image in and out, optionally playing a
    sound effect when it starts.
    """

    def __init__(self, screen: SurfaceScreen, logo_file:str, sound_intro_effect:str = None):
        """
        :param screen: Screen to show the splash screen on.
        :param logo_file: Path to the logo image file.
        :param sound_intro_effect: Path to a sound file to play once,
            when the splash screen starts. Optional - pass None (the
            default) for no sound.
        """
        self._screen = screen
        self._logo = None
        self._logo_file = logo_file
        self._sound_intro_effect = sound_intro_effect

    def setup(self) -> None:
        """
        Load the logo image, and play the intro sound if one was
        given.
        """
        self._logo = Image(self._logo_file)
        if self._sound_intro_effect is not None:
            SoundEffect(self._sound_intro_effect).play()

    def loop(self) -> None:
        """
        Fade the logo in, then out.
        """
        self._logo.fade(self._screen, 2500)

    def reset(self) -> None:
        """
        Nothing to reset - this scene has no state that changes after
        setup().
        """
        pass
