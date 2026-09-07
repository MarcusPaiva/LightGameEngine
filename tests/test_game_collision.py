"""
Tests for :mod:`light_game_engine.game_collision`.
"""
from light_game_engine.bounding_box import CircleBoundingBox
from light_game_engine.game_collision import circle_collision_detections


class TestCircleCollisionDetections:
    def test_overlapping_circles_collide(self):
        pos1 = CircleBoundingBox(0, 0, 0)
        pos2 = CircleBoundingBox(5, 0, 0)
        assert circle_collision_detections(pos1, 5, pos2, 5) is True

    def test_far_apart_circles_do_not_collide(self):
        pos1 = CircleBoundingBox(0, 0, 0)
        pos2 = CircleBoundingBox(100, 0, 0)
        assert circle_collision_detections(pos1, 5, pos2, 5) is False

    def test_exactly_touching_circles_collide(self):
        # distance between centers == sum of radii -> boundary counts as a collision
        pos1 = CircleBoundingBox(0, 0, 0)
        pos2 = CircleBoundingBox(10, 0, 0)
        assert circle_collision_detections(pos1, 5, pos2, 5) is True

    def test_just_beyond_touching_does_not_collide(self):
        pos1 = CircleBoundingBox(0, 0, 0)
        pos2 = CircleBoundingBox(10.01, 0, 0)
        assert circle_collision_detections(pos1, 5, pos2, 5) is False

    def test_diagonal_distance(self):
        # 3-4-5 triangle: distance is exactly 5
        pos1 = CircleBoundingBox(0, 0, 0)
        pos2 = CircleBoundingBox(3, 4, 0)
        assert circle_collision_detections(pos1, 2, pos2, 3) is True
        assert circle_collision_detections(pos1, 2, pos2, 2) is False

    def test_same_position_always_collides(self):
        pos1 = CircleBoundingBox(7, 7, 0)
        pos2 = CircleBoundingBox(7, 7, 0)
        assert circle_collision_detections(pos1, 0, pos2, 0) is True
