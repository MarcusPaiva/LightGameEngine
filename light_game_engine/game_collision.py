"""
Collision detection: circle-vs-circle, rect-vs-rect and circle-vs-rect.
"""
import math

from light_game_engine.bounding_box import BoundingBox, RectBoundingBox


def circle_collision_detections(position1: BoundingBox, radius1: int, position2: BoundingBox, radius2: int) -> bool:
    """
    Euclidean circle-vs-circle collision detection.

    :param position1: First object's bounding box position.
    :param radius1: First object's radius distance.
    :param position2: Second object's bounding box position.
    :param radius2: Second object's radius distance.
    :return: Whether the two circles overlap.
    :rtype: bool
    """
    distance = math.sqrt(
        (position1.center_x - position2.center_x) ** 2 + (position1.center_y - position2.center_y) ** 2)
    if distance <= radius1 + radius2:
        return True
    return False


def rect_collision_detection(rect1: RectBoundingBox, rect2: RectBoundingBox) -> bool:
    """
    Axis-aligned rectangle-vs-rectangle collision detection.

    :param rect1: First rectangle.
    :param rect2: Second rectangle.
    :return: Whether the two rectangles overlap.
    :rtype: bool
    """
    x0_1, y0_1, x1_1, y1_1 = rect1.bounds
    x0_2, y0_2, x1_2, y1_2 = rect2.bounds
    return x0_1 <= x1_2 and x1_1 >= x0_2 and y0_1 <= y1_2 and y1_1 >= y0_2


def circle_rect_collision_detection(circle_position: BoundingBox, radius: int, rect: RectBoundingBox) -> bool:
    """
    Circle-vs-axis-aligned-rectangle collision detection.

    Finds the point on the rectangle closest to the circle's center and
    checks whether that point is within the circle's radius.

    :param circle_position: Circle's bounding box position (its center is used).
    :param radius: Circle's radius distance.
    :param rect: Rectangle to test against.
    :return: Whether the circle and the rectangle overlap.
    :rtype: bool
    """
    x0, y0, x1, y1 = rect.bounds
    closest_x = min(max(circle_position.center_x, x0), x1)
    closest_y = min(max(circle_position.center_y, y0), y1)
    distance = math.sqrt(
        (circle_position.center_x - closest_x) ** 2 + (circle_position.center_y - closest_y) ** 2)
    return distance <= radius
