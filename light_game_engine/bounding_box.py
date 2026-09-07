"""
Simple 2D shapes: boxes and circles, with no pygame code inside.

Every method here returns plain numbers or ``[x, y]`` pairs, never a
``pygame.Vector2``. This means game code that uses this module does
not need to import pygame at all.
"""
from abc import ABC, abstractmethod
from typing import List, Tuple


class BoundingBox(ABC):
    """
    A shape with a position and a size. You can ask it for its
    corners, its center, and its width and height.
    """

    @property
    @abstractmethod
    def center(self) -> List[float]:
        """
        The center point of this box.

        :return: ``[x, y]`` pair.
        :rtype: List[float]
        """
        pass

    @property
    @abstractmethod
    def initial_position(self) -> List[float]:
        """
        The top-left corner of this box. For a circle, this is the
        top-left corner of the square drawn around it.

        :return: ``[x0, y0]`` pair.
        :rtype: List[float]
        """
        pass

    @property
    @abstractmethod
    def final_position(self) -> List[float]:
        """
        The bottom-right corner of this box. For a circle, this is the
        bottom-right corner of the square drawn around it.

        :return: ``[x1, y1]`` pair.
        :rtype: List[float]
        """
        pass

    @property
    @abstractmethod
    def bounds(self) -> Tuple[int, int, int, int]:
        """
        All four corners of this box, in one tuple.

        :return: ``(x0, y0, x1, y1)`` tuple.
        :rtype: Tuple[int, int, int, int]
        """
        pass

    @property
    @abstractmethod
    def size(self) -> List[float]:
        """
        The width and height of this box.

        :return: ``[width, height]`` pair.
        :rtype: List[float]
        """
        pass

    @property
    @abstractmethod
    def x0(self) -> float:
        """
        The left edge of this box. For a circle, this is the left edge
        of the square drawn around it.

        :return: X coordinate of the left edge.
        :rtype: float
        """
        pass

    @property
    @abstractmethod
    def y0(self) -> float:
        """
        The top edge of this box. For a circle, this is the top edge
        of the square drawn around it.

        :return: Y coordinate of the top edge.
        :rtype: float
        """
        pass

    @property
    @abstractmethod
    def x1(self) -> float:
        """
        The right edge of this box. For a circle, this is the right
        edge of the square drawn around it.

        :return: X coordinate of the right edge.
        :rtype: float
        """
        pass

    @property
    @abstractmethod
    def y1(self) -> float:
        """
        The bottom edge of this box. For a circle, this is the bottom
        edge of the square drawn around it.

        :return: Y coordinate of the bottom edge.
        :rtype: float
        """
        pass

    @property
    @abstractmethod
    def center_x(self) -> float:
        """
        The x position of the center.

        :return: X coordinate of the center.
        :rtype: float
        """
        pass

    @property
    @abstractmethod
    def center_y(self) -> float:
        """
        The y position of the center.

        :return: Y coordinate of the center.
        :rtype: float
        """
        pass

    @property
    @abstractmethod
    def width(self) -> float:
        """
        The width of this box.

        :return: Width.
        :rtype: float
        """
        pass

    @property
    @abstractmethod
    def height(self) -> float:
        """
        The height of this box.

        :return: Height.
        :rtype: float
        """
        pass

    @abstractmethod
    def copy(self) -> "BoundingBox":
        """
        Make a new copy of this box. Changing the copy will not change
        the original.

        :return: A new bounding box with the same shape and position.
        :rtype: BoundingBox
        """
        pass


class RectBoundingBox(BoundingBox):
    """
    A rectangle that is not tilted (its sides are flat: up-down and
    left-right). It is defined by its two corners.
    """

    def __init__(self, x0, y0, x, y):
        """
        :param x0: X position of the top-left corner.
        :param y0: Y position of the top-left corner.
        :param x: X position of the bottom-right corner.
        :param y: Y position of the bottom-right corner.
        """
        self._x0 = x0
        self._y0 = y0
        self._x = x
        self._y = y

    @property
    def center(self) -> List[float]:
        """
        :return: ``[x, y]`` position of the center of this rectangle.
        :rtype: List[float]
        """
        x_center = (self._x - self._x0) / 2
        y_center = (self._y - self._y0) / 2
        return [x_center + self._x0, y_center + self._y0]

    @property
    def initial_position(self) -> List[float]:
        """
        :return: ``[x0, y0]`` position of the top-left corner.
        :rtype: List[float]
        """
        return [self._x0, self._y0]

    @property
    def final_position(self) -> List[float]:
        """
        :return: ``[x1, y1]`` position of the bottom-right corner.
        :rtype: List[float]
        """
        return [self._x, self._y]

    @property
    def bounds(self) -> Tuple[int, int, int, int]:
        """
        :return: ``(x0, y0, x1, y1)`` tuple.
        :rtype: Tuple[int, int, int, int]
        """
        return self._x0, self._y0, self._x, self._y

    @property
    def size(self) -> List[float]:
        """
        :return: ``[width, height]`` pair.
        :rtype: List[float]
        """
        return [self._x - self._x0, self._y - self._y0]

    @property
    def x0(self) -> float:
        """
        :return: X coordinate of the left edge.
        :rtype: float
        """
        return self._x0

    @property
    def y0(self) -> float:
        """
        :return: Y coordinate of the top edge.
        :rtype: float
        """
        return self._y0

    @property
    def x1(self) -> float:
        """
        :return: X coordinate of the right edge.
        :rtype: float
        """
        return self._x

    @property
    def y1(self) -> float:
        """
        :return: Y coordinate of the bottom edge.
        :rtype: float
        """
        return self._y

    @property
    def center_x(self) -> float:
        """
        :return: X coordinate of the center.
        :rtype: float
        """
        return self._x0 + (self._x - self._x0) / 2

    @property
    def center_y(self) -> float:
        """
        :return: Y coordinate of the center.
        :rtype: float
        """
        return self._y0 + (self._y - self._y0) / 2

    @property
    def width(self) -> float:
        """
        :return: Width.
        :rtype: float
        """
        return self._x - self._x0

    @property
    def height(self) -> float:
        """
        :return: Height.
        :rtype: float
        """
        return self._y - self._y0

    def copy(self) -> "RectBoundingBox":
        """
        :return: A new :class:`RectBoundingBox` with the same corners.
        :rtype: RectBoundingBox
        """
        return RectBoundingBox(self._x0, self._y0, self._x, self._y)


class CircleBoundingBox(BoundingBox):
    """
    A circle, defined by its center point and its radius. The
    corner-style properties (like x0 and x1) describe the square drawn
    around this circle.
    """

    def __init__(self, x_center: int, y_center: int, radius: int):
        """
        :param x_center: X position of the circle's center.
        :param y_center: Y position of the circle's center.
        :param radius: Circle radius.
        """
        self.__x = x_center
        self.__y = y_center
        self.__radius = radius

    @property
    def center(self) -> List[float]:
        """
        :return: ``[x, y]`` position of the circle's center.
        :rtype: List[float]
        """
        return [self.__x, self.__y]

    @property
    def initial_position(self) -> List[float]:
        """
        :return: ``[x0, y0]`` position of the top-left corner of the
            square drawn around this circle.
        :rtype: List[float]
        """
        return [self.__x - self.__radius, self.__y - self.__radius]

    @property
    def final_position(self) -> List[float]:
        """
        :return: ``[x1, y1]`` position of the bottom-right corner of
            the square drawn around this circle.
        :rtype: List[float]
        """
        return [self.__x + self.__radius, self.__y + self.__radius]

    @property
    def bounds(self) -> Tuple[int, int, int, int]:
        """
        :return: ``(x0, y0, x1, y1)`` tuple for the square drawn around
            this circle.
        :rtype: Tuple[int, int, int, int]
        """
        return self.__x - self.__radius, self.__y - self.__radius, self.__x + self.__radius, self.__y + self.__radius

    @property
    def size(self) -> List[float]:
        """
        :return: ``[diameter, diameter]`` pair.
        :rtype: List[float]
        """
        return [self.__radius * 2, self.__radius * 2]

    @property
    def radius(self):
        """
        :return: This circle's radius.
        :rtype: float
        """
        return self.__radius

    @property
    def x0(self) -> float:
        """
        :return: X coordinate of the left edge of the square drawn
            around this circle.
        :rtype: float
        """
        return self.__x - self.__radius

    @property
    def y0(self) -> float:
        """
        :return: Y coordinate of the top edge of the square drawn
            around this circle.
        :rtype: float
        """
        return self.__y - self.__radius

    @property
    def x1(self) -> float:
        """
        :return: X coordinate of the right edge of the square drawn
            around this circle.
        :rtype: float
        """
        return self.__x + self.__radius

    @property
    def y1(self) -> float:
        """
        :return: Y coordinate of the bottom edge of the square drawn
            around this circle.
        :rtype: float
        """
        return self.__y + self.__radius

    @property
    def center_x(self) -> float:
        """
        :return: X coordinate of the center.
        :rtype: float
        """
        return self.__x

    @property
    def center_y(self) -> float:
        """
        :return: Y coordinate of the center.
        :rtype: float
        """
        return self.__y

    @property
    def width(self) -> float:
        """
        :return: Diameter (used as the width of the square drawn around
            this circle).
        :rtype: float
        """
        return self.__radius * 2

    @property
    def height(self) -> float:
        """
        :return: Diameter (used as the height of the square drawn
            around this circle).
        :rtype: float
        """
        return self.__radius * 2

    def copy(self) -> "CircleBoundingBox":
        """
        :return: A new :class:`CircleBoundingBox` with the same center
            and radius.
        :rtype: CircleBoundingBox
        """
        return CircleBoundingBox(self.__x, self.__y, self.__radius)

    def set_position(self, x: float, y: float) -> "CircleBoundingBox":
        """
        Move this circle to a new position. You give the exact x and y
        position (not an offset).

        :param x: New center x.
        :param y: New center y.
        :return: This instance, for chaining.
        :rtype: CircleBoundingBox
        """
        self.__x = x
        self.__y = y
        return self

    def move_by(self, dx: float, dy: float) -> "CircleBoundingBox":
        """
        Move this circle by an amount, added to its current position.

        :param dx: X offset.
        :param dy: Y offset.
        :return: This instance, for chaining.
        :rtype: CircleBoundingBox
        """
        self.__x += dx
        self.__y += dy
        return self

    def __eq__(self, other) -> bool:
        """
        Two circles are equal when they have the same center and the
        same radius.

        :param other: The other object to compare with.
        :return: True if ``other`` is a :class:`CircleBoundingBox` with
            the same center and radius.
        :rtype: bool
        """
        if not isinstance(other, CircleBoundingBox):
            return NotImplemented
        return (self.__x, self.__y, self.__radius) == (other.center_x, other.center_y, other.radius)

    def __hash__(self):
        """
        :return: A hash value that matches :meth:`__eq__`, so equal
            circles always give the same hash.
        :rtype: int
        """
        return hash((self.__x, self.__y, self.__radius))
