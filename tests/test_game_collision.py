"""
Tests for :mod:`light_game_engine.game_collision`.
"""
from light_game_engine.bounding_box import CircleBoundingBox, RectBoundingBox
from light_game_engine.game_collision import (
    circle_collision_detections,
    circle_rect_collision_detection,
    rect_collision_detection,
)


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


class TestRectCollisionDetection:
    def test_overlapping_rects_collide(self):
        rect1 = RectBoundingBox(0, 0, 10, 10)
        rect2 = RectBoundingBox(5, 5, 15, 15)
        assert rect_collision_detection(rect1, rect2) is True

    def test_far_apart_rects_do_not_collide(self):
        rect1 = RectBoundingBox(0, 0, 10, 10)
        rect2 = RectBoundingBox(20, 20, 30, 30)
        assert rect_collision_detection(rect1, rect2) is False

    def test_one_rect_fully_inside_another_collides(self):
        outer = RectBoundingBox(0, 0, 10, 10)
        inner = RectBoundingBox(2, 2, 8, 8)
        assert rect_collision_detection(outer, inner) is True
        assert rect_collision_detection(inner, outer) is True

    def test_exactly_touching_edges_collide(self):
        rect1 = RectBoundingBox(0, 0, 10, 10)
        rect2 = RectBoundingBox(10, 0, 20, 10)
        assert rect_collision_detection(rect1, rect2) is True

    def test_just_beyond_touching_edges_does_not_collide(self):
        rect1 = RectBoundingBox(0, 0, 10, 10)
        rect2 = RectBoundingBox(10.01, 0, 20, 10)
        assert rect_collision_detection(rect1, rect2) is False

    def test_touching_only_at_a_corner_collides(self):
        rect1 = RectBoundingBox(0, 0, 10, 10)
        rect2 = RectBoundingBox(10, 10, 20, 20)
        assert rect_collision_detection(rect1, rect2) is True

    def test_order_of_arguments_does_not_matter(self):
        rect1 = RectBoundingBox(0, 0, 10, 10)
        rect2 = RectBoundingBox(5, 5, 15, 15)
        assert rect_collision_detection(rect1, rect2) == rect_collision_detection(rect2, rect1)


class TestCircleRectCollisionDetection:
    def test_circle_center_inside_rect_collides(self):
        rect = RectBoundingBox(0, 0, 10, 10)
        circle = CircleBoundingBox(5, 5, 1)
        assert circle_rect_collision_detection(circle, 1, rect) is True

    def test_far_apart_does_not_collide(self):
        rect = RectBoundingBox(0, 0, 10, 10)
        circle = CircleBoundingBox(100, 100, 1)
        assert circle_rect_collision_detection(circle, 1, rect) is False

    def test_circle_overlapping_an_edge_collides(self):
        rect = RectBoundingBox(0, 0, 10, 10)
        circle = CircleBoundingBox(13, 5, 5)  # closest point is (10, 5), distance 3
        assert circle_rect_collision_detection(circle, 5, rect) is True

    def test_circle_exactly_touching_an_edge_collides(self):
        rect = RectBoundingBox(0, 0, 10, 10)
        circle = CircleBoundingBox(15, 5, 0)  # closest point is (10, 5), distance 5
        assert circle_rect_collision_detection(circle, 5, rect) is True

    def test_circle_just_beyond_an_edge_does_not_collide(self):
        rect = RectBoundingBox(0, 0, 10, 10)
        circle = CircleBoundingBox(15.01, 5, 0)
        assert circle_rect_collision_detection(circle, 5, rect) is False

    def test_circle_exactly_touching_a_corner_collides(self):
        # closest point is the corner (10, 10); distance is exactly 5 (3-4-5 triangle)
        rect = RectBoundingBox(0, 0, 10, 10)
        circle = CircleBoundingBox(13, 14, 0)
        assert circle_rect_collision_detection(circle, 5, rect) is True

    def test_circle_just_beyond_a_corner_does_not_collide(self):
        rect = RectBoundingBox(0, 0, 10, 10)
        circle = CircleBoundingBox(13, 14, 0)
        assert circle_rect_collision_detection(circle, 4.99, rect) is False

    def test_zero_radius_circle_on_the_boundary_collides(self):
        rect = RectBoundingBox(0, 0, 10, 10)
        circle = CircleBoundingBox(10, 5, 0)  # sitting exactly on the edge
        assert circle_rect_collision_detection(circle, 0, rect) is True
