"""
A simple wrapper around :mod:`pygame.font`, for drawing text.
"""
from typing import List, Optional

import pygame


class GameFont:
    """
    A loaded font tied to one piece of text. You can set its color,
    turn anti-aliasing on or off, and set a background color. Call
    render() any time to draw the text with the current settings.

    Uses pygame's built-in font by default. Call :meth:`set_font` to
    use your own font file instead.
    """

    def __init__(self, size: int, text: str):
        """
        :param size: Font size, in points.
        :param text: The text to show at first.
        """
        pygame.font.init()
        self.__text = text
        self.__size = size
        self.__font = pygame.font.Font(None, size)
        self.__color = [0, 0, 0]
        self.__anti_alias = False
        self.__background_color = None

    def set_font(self, path: Optional[str]):
        """
        Load your own ``.ttf`` font file, at the same size as before.
        This replaces the font currently in use.

        :param path: Path to a ``.ttf`` font file. Pass None to go back
            to pygame's built-in font.
        :return: This instance, for chaining.
        :rtype: GameFont
        """
        self.__font = pygame.font.Font(path, self.__size)
        return self

    def get_text_size(self):
        """
        Measure how big the text would look once drawn, without
        actually drawing it.

        :return: ``(width, height)`` of the text, in pixels.
        :rtype: Tuple[int, int]
        """
        return self.__font.size(self.__text)

    def set_text(self, text: str):
        """
        Change the text this font shows.

        :param text: The new text.
        :return: This instance, for chaining.
        :rtype: GameFont
        """
        self.__text = text
        return self

    def set_color(self, color: List[int]):
        """
        Set the color of the text.

        :param color: ``[r, g, b]`` (or ``[r, g, b, a]``) color.
        :return: This instance, for chaining.
        :rtype: GameFont
        """
        self.__color = color
        return self

    def enable_anti_alias(self, value: bool):
        """
        Turn anti-aliasing on or off for the next time you render.
        Anti-aliasing makes text edges look smoother, but a bit softer.

        :param value: True to smooth the text edges, False for sharp,
            blocky edges.
        :return: This instance, for chaining.
        :rtype: GameFont
        """
        self.__anti_alias = value
        return self

    def set_background_color(self, value: "None|List[int]"):
        """
        Set (or remove) the color drawn behind the text.

        :param value: ``[r, g, b]`` background color, or None for no
            background (the text stays see-through behind).
        :return: This instance, for chaining.
        :rtype: GameFont
        """
        self.__background_color = value
        return self

    def render(self):
        """
        Draw the current text using the current color, anti-alias, and
        background settings, and return the result as an image.

        :return: The rendered text.
        :rtype: pygame.Surface
        """
        return self.__font.render(self.__text, self.__anti_alias, self.__color, self.__background_color)
