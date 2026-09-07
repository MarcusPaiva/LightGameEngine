"""
Abstract base class every drawable, movable game entity implements.
"""
from abc import ABC, abstractmethod
from typing import Optional

from light_game_engine.bounding_box import BoundingBox


class GameObject(ABC):
    """
    Contract for a game entity that has a position, can be updated once
    per frame, drawn to the screen, and optionally exposes the bounding
    box of what it last drew (its "sprite").
    """

    @abstractmethod
    def update(self):
        """
        Advance this object's state by one frame (movement, animation, etc).

        :return: None
        """
        pass

    @property
    @abstractmethod
    def position(self) -> BoundingBox:
        """
        This object's current position.

        :return: The object's bounding box.
        :rtype: BoundingBox
        """
        pass

    @abstractmethod
    def draw(self) -> None:
        """
        Draw this object onto its screen.

        :return: None
        """
        pass

    @property
    @abstractmethod
    def sprite(self) -> Optional[BoundingBox]:
        """
        The bounding box of the shape last drawn for this object, if any.

        :return: The last-drawn bounding box, or None if nothing has been
            drawn yet.
        :rtype: Optional[BoundingBox]
        """
        pass
