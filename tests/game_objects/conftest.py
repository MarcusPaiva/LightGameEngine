"""
Shared fixtures for the game_objects test package.

Button and Modal build a GameFont via setup(), which now defaults to
pygame's built-in font and only touches disk if set_font() is used, so
no font-file patching is needed here.
"""
from unittest.mock import MagicMock

import pytest


class FakeScreen:
    """Stand-in for SurfaceScreen: records draw() calls, no real display."""

    def __init__(self, width=800, height=600):
        self._width = width
        self._height = height
        self.surface = MagicMock(name="pygame.Surface")
        self.draw_calls = []

    def get_screen(self):
        return self.surface

    def width(self):
        return self._width

    def height(self):
        return self._height

    def draw(self, artifact, position):
        self.draw_calls.append((artifact, position))
        return self


@pytest.fixture
def make_screen():
    return FakeScreen


@pytest.fixture
def screen():
    return FakeScreen()
