"""
Circle-based collision detection.
"""
import math

from light_game_engine.bounding_box import BoundingBox


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
