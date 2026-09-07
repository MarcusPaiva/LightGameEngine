"""
The base rule every drawable, movable game thing must follow.
"""
from abc import ABC, abstractmethod
from typing import Optional

from light_game_engine.bounding_box import BoundingBox


class GameObject(ABC):
    """
    Any game object that follows this rule must have a position, must
    be able to update itself once per frame, must be able to draw
    itself, and may show the box of what it last drew (its "sprite").
    """

    @abstractmethod
    def update(self):
        """
        Move this object forward by one frame (for example: movement,
        animation).

        :return: None
        """
        pass

    @property
    @abstractmethod
    def position(self) -> BoundingBox:
        """
        This object's current position.

        :return: The object's box.
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
        The box of the shape this object last drew, if any.

        :return: The last-drawn box, or None if nothing has been drawn
            yet.
        :rtype: Optional[BoundingBox]
        """
        pass
