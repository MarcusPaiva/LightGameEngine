"""
The game's window. Wraps pygame's display module, and owns starting
and stopping pygame itself.
"""
from typing import List

import pygame


class SurfaceScreen:
    """
    The game's window: opens it, and offers only the small set of
    drawing and timing actions a game needs. Callers never have to
    touch pygame's display/time code directly.
    """

    def __init__(self, width: int, height: int, title: str):
        """
        Start pygame and open the game's window.

        :param width: Window width, in pixels.
        :param height: Window height, in pixels.
        :param title: Window title.
        """
        pygame.init()
        self.__screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption(title)
        self._clock = pygame.time.Clock()

    def draw(self, artfact, position: List[int]):
        """
        Draw an image onto the screen.

        :param artfact: The image to draw.
        :param position: ``[x, y]`` position to draw it at.
        :return: This instance, for chaining.
        :rtype: SurfaceScreen
        """
        self.__screen.blit(artfact, position)
        return self

    def fill(self, color: "str|List[int]"):
        """
        Fill the whole screen with one color.

        :param color: Color name/hex string, or ``[r, g, b]`` triplet.
        :return: This instance, for chaining.
        :rtype: SurfaceScreen
        """
        self.__screen.fill(color)
        return self

    def height(self):
        """
        :return: Window height, in pixels.
        :rtype: int
        """
        return self.__screen.get_height()

    def width(self):
        """
        :return: Window width, in pixels.
        :rtype: int
        """
        return self.__screen.get_width()

    def flip(self):
        """
        Show everything drawn so far on screen.

        :return: This instance, for chaining.
        :rtype: SurfaceScreen
        """
        pygame.display.flip()
        return self

    def set_clock(self, value: int):
        """
        Limit how many frames run per second, pausing as needed.

        :param value: Target frames per second.
        :return: This instance, for chaining.
        :rtype: SurfaceScreen
        """
        self._clock.tick(value)
        return self

    def get_screen(self):
        """
        :return: The pygame surface behind this screen, for code that
            needs direct pygame access.
        :rtype: pygame.Surface
        """
        return self.__screen

    def quit(self):
        """
        Stop pygame.

        :return: This instance, for chaining.
        :rtype: SurfaceScreen
        """
        pygame.quit()
        return self
