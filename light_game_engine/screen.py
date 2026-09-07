"""
The application's window, wrapping pygame's display module and owning
pygame's init/quit lifecycle.
"""
from typing import List

import pygame


class SurfaceScreen:
    """
    The game's window: opens the display surface and exposes only the
    small set of drawing and timing operations the game needs, so
    callers never have to touch pygame's display/time APIs directly.
    """

    def __init__(self, width: int, height: int, title: str):
        """
        Initialize pygame and open the application window.

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
        Blit a surface onto the screen.

        :param artfact: Surface to draw.
        :param position: ``[x, y]`` position to draw it at.
        :return: This instance, for chaining.
        :rtype: SurfaceScreen
        """
        self.__screen.blit(artfact, position)
        return self

    def fill(self, color: "str|List[int]"):
        """
        Fill the entire screen with a color.

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
        Present the current frame to the display.

        :return: This instance, for chaining.
        :rtype: SurfaceScreen
        """
        pygame.display.flip()
        return self

    def set_clock(self, value: int):
        """
        Cap the frame rate, sleeping as needed.

        :param value: Target frames per second.
        :return: This instance, for chaining.
        :rtype: SurfaceScreen
        """
        self._clock.tick(value)
        return self

    def get_screen(self):
        """
        :return: The underlying pygame display surface.
        :rtype: pygame.Surface
        """
        return self.__screen

    def quit(self):
        """
        Shut pygame down.

        :return: This instance, for chaining.
        :rtype: SurfaceScreen
        """
        pygame.quit()
        return self
