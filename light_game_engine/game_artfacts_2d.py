"""
Filled 2D shapes (rectangles and circles) that draw themselves onto a
:class:`light_game_engine.screen.SurfaceScreen`.
"""
from typing import List

import pygame

from light_game_engine.bounding_box import RectBoundingBox, CircleBoundingBox


class Rect:
    """
    A filled, axis-aligned rectangle.
    """

    def __init__(self, position_x: int, position_y: int, width: int, height: int):
        """
        :param position_x: X of the top-left corner.
        :param position_y: Y of the top-left corner.
        :param width: Rectangle width.
        :param height: Rectangle height.
        """
        self.__bounding_box = RectBoundingBox(position_x, position_y, position_x + width, position_y + height)
        self.__fill_color = "red"

    def set_fill_color(self, color: "str|List[int]"):
        """
        Set the fill color.

        :param color: Color name/hex string, or ``[r, g, b]`` triplet.
        :return: This instance, for chaining.
        :rtype: Rect
        """
        self.__fill_color = color
        return self

    def render(self, screen) -> RectBoundingBox:
        """
        Draw this rectangle onto a screen.

        :param screen: Target :class:`light_game_engine.screen.SurfaceScreen`.
        :return: A copy of this rectangle's bounding box.
        :rtype: RectBoundingBox
        """
        initial = self.__bounding_box.initial_position
        size = self.__bounding_box.size
        pygame.draw.rect(screen.get_screen(), self.__fill_color, [initial[0], initial[1], size[0], size[1]], 0)
        return self.__bounding_box.copy()


class Circle:
    """
    A filled circle.
    """

    def __init__(self, position_x: int, position_y: int, radius):
        """
        :param position_x: X coordinate of the circle's center.
        :param position_y: Y coordinate of the circle's center.
        :param radius: Circle radius.
        """
        self.__bounding_box = CircleBoundingBox(position_x, position_y, radius)
        self.__fill_color = "red"

    def set_fill_color(self, color: "str|List[int]"):
        """
        Set the fill color.

        :param color: Color name/hex string, or ``[r, g, b]`` triplet.
        :return: This instance, for chaining.
        :rtype: Circle
        """
        self.__fill_color = color
        return self

    def render(self, screen) -> CircleBoundingBox:
        """
        Draw this circle onto a screen.

        :param screen: Target :class:`light_game_engine.screen.SurfaceScreen`.
        :return: A copy of this circle's bounding box.
        :rtype: CircleBoundingBox
        """
        pygame.draw.circle(screen.get_screen(), self.__fill_color, self.__bounding_box.center, self.__bounding_box.radius)
        return self.__bounding_box.copy()
