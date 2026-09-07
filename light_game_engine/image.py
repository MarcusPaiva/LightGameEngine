"""
Image loading and the fade-in/fade-out splash effect.
"""
import pygame

from light_game_engine.image_effects import fade_image


class Image:
    """
    A loaded image that can fade in and out on screen.
    """

    def __init__(self, file: str):
        """
        :param file: Path to the image file to load.
        """
        self.__image = pygame.image.load(file)

    def fade(self, screen, duration):
        """
        Fade this image in, then out, centered on the screen.

        :param screen: Target :class:`light_game_engine.screen.SurfaceScreen`.
        :param duration: Total effect duration, in milliseconds.
        :return: None
        """
        self.__image.convert_alpha()
        logo_rect = self.__image.get_rect(center=(screen.width() // 2, screen.height() // 2))
        fade_image(screen, self.__image.convert_alpha(), logo_rect, duration)
