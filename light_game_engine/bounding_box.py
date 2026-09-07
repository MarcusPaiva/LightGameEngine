"""
Pure geometry: 2D bounding boxes with no pygame dependency.

Every position/size accessor returns plain numbers or ``[x, y]``
pairs - never a ``pygame.Vector2`` - so game code built on top of
this module never needs to import pygame itself.
"""
from abc import ABC, abstractmethod
from typing import List, Tuple


class BoundingBox(ABC):
    """
    Abstract 2D bounding box: something with a position and a size,
    describable by its corners, center and dimensions.
    """

    @property
    @abstractmethod
    def center(self) -> List[float]:
        """
        This box's center position.

        :return: ``[x, y]`` pair.
        :rtype: List[float]
        """
        pass

    @property
    @abstractmethod
    def initial_position(self) -> List[float]:
        """
        This box's top-left corner (or, for a circle, the top-left
        corner of its bounding square).

        :return: ``[x0, y0]`` pair.
        :rtype: List[float]
        """
        pass

    @property
    @abstractmethod
    def final_position(self) -> List[float]:
        """
        This box's bottom-right corner (or, for a circle, the
        bottom-right corner of its bounding square).

        :return: ``[x1, y1]`` pair.
        :rtype: List[float]
        """
        pass

    @property
    @abstractmethod
    def bounds(self) -> Tuple[int, int, int, int]:
        """
        This box's corners as a flat tuple.

        :return: ``(x0, y0, x1, y1)`` tuple.
        :rtype: Tuple[int, int, int, int]
        """
        pass

    @property
    @abstractmethod
    def size(self) -> List[float]:
        """
        This box's dimensions.

        :return: ``[width, height]`` pair.
        :rtype: List[float]
        """
        pass

    @property
    @abstractmethod
    def x0(self) -> float:
        """
        Left edge (or bounding-square left, for a circle).

        :return: X coordinate of the left edge.
        :rtype: float
        """
        pass

    @property
    @abstractmethod
    def y0(self) -> float:
        """
        Top edge (or bounding-square top, for a circle).

        :return: Y coordinate of the top edge.
        :rtype: float
        """
        pass

    @property
    @abstractmethod
    def x1(self) -> float:
        """
        Right edge (or bounding-square right, for a circle).

        :return: X coordinate of the right edge.
        :rtype: float
        """
        pass

    @property
    @abstractmethod
    def y1(self) -> float:
        """
        Bottom edge (or bounding-square bottom, for a circle).

        :return: Y coordinate of the bottom edge.
        :rtype: float
        """
        pass

    @property
    @abstractmethod
    def center_x(self) -> float:
        """
        Center x coordinate.

        :return: X coordinate of the center.
        :rtype: float
        """
        pass

    @property
    @abstractmethod
    def center_y(self) -> float:
        """
        Center y coordinate.

        :return: Y coordinate of the center.
        :rtype: float
        """
        pass

    @property
    @abstractmethod
    def width(self) -> float:
        """
        This box's width.

        :return: Width.
        :rtype: float
        """
        pass

    @property
    @abstractmethod
    def height(self) -> float:
        """
        This box's height.

        :return: Height.
        :rtype: float
        """
        pass

    @abstractmethod
    def copy(self) -> "BoundingBox":
        """
        Build an independent copy of this bounding box.

        :return: A new bounding box with the same geometry.
        :rtype: BoundingBox
        """
        pass


class RectBoundingBox(BoundingBox):
    """
    Axis-aligned rectangular bounding box, defined by its two corners.
    """

    def __init__(self, x0, y0, x, y):
        """
        :param x0: X of the initial (top-left) corner.
        :param y0: Y of the initial (top-left) corner.
        :param x: X of the final (bottom-right) corner.
        :param y: Y of the final (bottom-right) corner.
        """
        self._x0 = x0
        self._y0 = y0
        self._x = x
        self._y = y

    @property
    def center(self) -> List[float]:
        """
        :return: ``[x, y]`` pair for this rectangle's center.
        :rtype: List[float]
        """
        x_center = (self._x - self._x0) / 2
        y_center = (self._y - self._y0) / 2
        return [x_center + self._x0, y_center + self._y0]

    @property
    def initial_position(self) -> List[float]:
        """
        :return: ``[x0, y0]`` pair for the top-left corner.
        :rtype: List[float]
        """
        return [self._x0, self._y0]

    @property
    def final_position(self) -> List[float]:
        """
        :return: ``[x1, y1]`` pair for the bottom-right corner.
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
    Circular bounding box, defined by its center and radius. Corner-
    based properties describe the square that bounds the circle.
    """

    def __init__(self, x_center: int, y_center: int, radius: int):
        """
        :param x_center: X coordinate of the circle's center.
        :param y_center: Y coordinate of the circle's center.
        :param radius: Circle radius.
        """
        self.__x = x_center
        self.__y = y_center
        self.__radius = radius

    @property
    def center(self) -> List[float]:
        """
        :return: ``[x, y]`` pair for the circle's center.
        :rtype: List[float]
        """
        return [self.__x, self.__y]

    @property
    def initial_position(self) -> List[float]:
        """
        :return: ``[x0, y0]`` pair for the bounding square's top-left corner.
        :rtype: List[float]
        """
        return [self.__x - self.__radius, self.__y - self.__radius]

    @property
    def final_position(self) -> List[float]:
        """
        :return: ``[x1, y1]`` pair for the bounding square's bottom-right corner.
        :rtype: List[float]
        """
        return [self.__x + self.__radius, self.__y + self.__radius]

    @property
    def bounds(self) -> Tuple[int, int, int, int]:
        """
        :return: ``(x0, y0, x1, y1)`` tuple for the bounding square.
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
        :return: X coordinate of the bounding square's left edge.
        :rtype: float
        """
        return self.__x - self.__radius

    @property
    def y0(self) -> float:
        """
        :return: Y coordinate of the bounding square's top edge.
        :rtype: float
        """
        return self.__y - self.__radius

    @property
    def x1(self) -> float:
        """
        :return: X coordinate of the bounding square's right edge.
        :rtype: float
        """
        return self.__x + self.__radius

    @property
    def y1(self) -> float:
        """
        :return: Y coordinate of the bounding square's bottom edge.
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
        :return: Diameter (used as the bounding square's width).
        :rtype: float
        """
        return self.__radius * 2

    @property
    def height(self) -> float:
        """
        :return: Diameter (used as the bounding square's height).
        :rtype: float
        """
        return self.__radius * 2

    def copy(self) -> "CircleBoundingBox":
        """
        :return: A new :class:`CircleBoundingBox` with the same center and radius.
        :rtype: CircleBoundingBox
        """
        return CircleBoundingBox(self.__x, self.__y, self.__radius)

    def set_position(self, x: float, y: float) -> "CircleBoundingBox":
        """
        Move this circle's center to an absolute position.

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
        Move this circle's center by a relative offset.

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
        Two circles are equal when their center and radius match.

        :param other: Object to compare against.
        :return: Whether ``other`` is an equal :class:`CircleBoundingBox`.
        :rtype: bool
        """
        if not isinstance(other, CircleBoundingBox):
            return NotImplemented
        return (self.__x, self.__y, self.__radius) == (other.center_x, other.center_y, other.radius)

    def __hash__(self):
        """
        :return: Hash consistent with :meth:`__eq__`.
        :rtype: int
        """
        return hash((self.__x, self.__y, self.__radius))
