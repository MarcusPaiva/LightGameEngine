"""
Loading images, and the fade-in/fade-out splash effect.
"""
import pygame

from light_game_engine.image_effects import fade_image


class Image:
    """
    A loaded image that can fade in and then fade out on screen.
    """

    def __init__(self, file: str):
        """
        :param file: Path to the image file to load.
        """
        self.__image = pygame.image.load(file)

    def fade(self, screen, duration):
        """
        Fade this image in, then out, in the middle of the screen.

        :param screen: The :class:`light_game_engine.screen.SurfaceScreen`
            to show the image on.
        :param duration: How long the whole effect lasts, in
            milliseconds.
        :return: None
        """
        self.__image.convert_alpha()
        logo_rect = self.__image.get_rect(center=(screen.width() // 2, screen.height() // 2))
        fade_image(screen, self.__image.convert_alpha(), logo_rect, duration)
