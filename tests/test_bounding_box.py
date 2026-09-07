"""
Tests for :mod:`light_game_engine.bounding_box`.
"""
import pytest

from light_game_engine.bounding_box import BoundingBox, RectBoundingBox, CircleBoundingBox


class TestBoundingBoxAbstract:
    def test_cannot_instantiate_directly(self):
        with pytest.raises(TypeError):
            BoundingBox()


class TestRectBoundingBox:
    @pytest.fixture
    def rect(self):
        # x0=10, y0=20, x1=50, y1=80 -> width 40, height 60
        return RectBoundingBox(10, 20, 50, 80)

    def test_initial_position(self, rect):
        assert rect.initial_position == [10, 20]

    def test_final_position(self, rect):
        assert rect.final_position == [50, 80]

    def test_bounds(self, rect):
        assert rect.bounds == (10, 20, 50, 80)

    def test_size(self, rect):
        assert rect.size == [40, 60]

    def test_x0_y0_x1_y1(self, rect):
        assert rect.x0 == 10
        assert rect.y0 == 20
        assert rect.x1 == 50
        assert rect.y1 == 80

    def test_center(self, rect):
        assert rect.center == [30, 50]

    def test_center_x_center_y(self, rect):
        assert rect.center_x == 30
        assert rect.center_y == 50

    def test_center_matches_center_x_center_y(self, rect):
        assert rect.center == [rect.center_x, rect.center_y]

    def test_width_height(self, rect):
        assert rect.width == 40
        assert rect.height == 60

    def test_copy_returns_equal_but_distinct_instance(self, rect):
        copy = rect.copy()
        assert copy is not rect
        assert isinstance(copy, RectBoundingBox)
        assert copy.bounds == rect.bounds

    def test_copy_is_independent(self, rect):
        copy = rect.copy()
        copy._RectBoundingBox__x0 = 999
        assert rect.x0 == 10

    def test_degenerate_zero_size_rect(self):
        zero = RectBoundingBox(5, 5, 5, 5)
        assert zero.size == [0, 0]
        assert zero.center == [5, 5]
        assert zero.width == 0
        assert zero.height == 0


class TestCircleBoundingBox:
    @pytest.fixture
    def circle(self):
        return CircleBoundingBox(100, 100, 25)

    def test_center(self, circle):
        assert circle.center == [100, 100]

    def test_initial_position(self, circle):
        assert circle.initial_position == [75, 75]

    def test_final_position(self, circle):
        assert circle.final_position == [125, 125]

    def test_bounds(self, circle):
        assert circle.bounds == (75, 75, 125, 125)

    def test_size(self, circle):
        assert circle.size == [50, 50]

    def test_radius(self, circle):
        assert circle.radius == 25

    def test_x0_y0_x1_y1(self, circle):
        assert circle.x0 == 75
        assert circle.y0 == 75
        assert circle.x1 == 125
        assert circle.y1 == 125

    def test_center_x_center_y(self, circle):
        assert circle.center_x == 100
        assert circle.center_y == 100

    def test_width_height(self, circle):
        assert circle.width == 50
        assert circle.height == 50

    def test_copy_returns_equal_but_distinct_instance(self, circle):
        copy = circle.copy()
        assert copy is not circle
        assert copy == circle

    def test_copy_is_independent(self, circle):
        copy = circle.copy()
        copy.set_position(0, 0)
        assert circle.center == [100, 100]

    def test_set_position_mutates_and_returns_self(self, circle):
        result = circle.set_position(1, 2)
        assert result is circle
        assert circle.center == [1, 2]

    def test_move_by_offsets_and_returns_self(self, circle):
        result = circle.move_by(5, -5)
        assert result is circle
        assert circle.center == [105, 95]

    def test_move_by_is_cumulative(self, circle):
        circle.move_by(1, 1).move_by(2, 2)
        assert circle.center == [103, 103]

    def test_eq_true_for_same_center_and_radius(self):
        a = CircleBoundingBox(1, 2, 3)
        b = CircleBoundingBox(1, 2, 3)
        assert a == b

    def test_eq_false_for_different_center_or_radius(self, circle):
        assert circle != CircleBoundingBox(101, 100, 25)
        assert circle != CircleBoundingBox(100, 100, 26)

    def test_eq_not_implemented_for_other_types(self, circle):
        assert circle.__eq__(object()) is NotImplemented
        assert circle != "not a circle"

    def test_hash_consistent_with_eq(self):
        a = CircleBoundingBox(1, 2, 3)
        b = CircleBoundingBox(1, 2, 3)
        assert hash(a) == hash(b)

    def test_hash_changes_after_move(self, circle):
        original_hash = hash(circle)
        circle.move_by(1, 1)
        assert hash(circle) != original_hash
