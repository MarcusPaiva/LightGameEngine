"""
Checks for when two shapes touch or overlap: circle-vs-circle,
rect-vs-rect, and circle-vs-rect.
"""
import math

from light_game_engine.bounding_box import BoundingBox, RectBoundingBox


def circle_collision_detections(position1: BoundingBox, radius1: int, position2: BoundingBox, radius2: int) -> bool:
    """
    Check if two circles touch or overlap.

    :param position1: First circle's position (its center is used).
    :param radius1: First circle's radius.
    :param position2: Second circle's position (its center is used).
    :param radius2: Second circle's radius.
    :return: True if the two circles touch or overlap.
    :rtype: bool
    """
    distance = math.sqrt(
        (position1.center_x - position2.center_x) ** 2 + (position1.center_y - position2.center_y) ** 2)
    if distance <= radius1 + radius2:
        return True
    return False


def rect_collision_detection(rect1: RectBoundingBox, rect2: RectBoundingBox) -> bool:
    """
    Check if two rectangles (not tilted) touch or overlap.

    :param rect1: First rectangle.
    :param rect2: Second rectangle.
    :return: True if the two rectangles touch or overlap.
    :rtype: bool
    """
    x0_1, y0_1, x1_1, y1_1 = rect1.bounds
    x0_2, y0_2, x1_2, y1_2 = rect2.bounds
    return x0_1 <= x1_2 and x1_1 >= x0_2 and y0_1 <= y1_2 and y1_1 >= y0_2


def circle_rect_collision_detection(circle_position: BoundingBox, radius: int, rect: RectBoundingBox) -> bool:
    """
    Check if a circle touches or overlaps a rectangle (not tilted).

    Finds the point on the rectangle that is closest to the circle's
    center, then checks if that point is close enough to be inside the
    circle.

    :param circle_position: Circle's position (its center is used).
    :param radius: Circle's radius.
    :param rect: The rectangle to check against.
    :return: True if the circle and the rectangle touch or overlap.
    :rtype: bool
    """
    x0, y0, x1, y1 = rect.bounds
    closest_x = min(max(circle_position.center_x, x0), x1)
    closest_y = min(max(circle_position.center_y, y0), y1)
    distance = math.sqrt(
        (circle_position.center_x - closest_x) ** 2 + (circle_position.center_y - closest_y) ** 2)
    return distance <= radius
