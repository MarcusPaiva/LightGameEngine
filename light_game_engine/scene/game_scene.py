"""
The rule every game scene must follow, so GameManagement can run any
of them the same way.
"""
from abc import ABC, abstractmethod

from light_game_engine.screen import SurfaceScreen


class GameScene(ABC):
    """
    A game scene: a screen or state your game can be in (a menu, a
    level, a splash screen...). Must be able to set itself up, run
    once per frame, and reset back to its starting state.
    """

    @abstractmethod
    def __init__(self, screen: SurfaceScreen):
        """
        :param screen: Screen this scene draws onto.
        """
        pass

    @abstractmethod
    def setup(self) -> None:
        """
        Prepare this scene (load assets, reset state). Called once
        before the scene's first :meth:`loop` call.
        """
        pass

    @abstractmethod
    def loop(self) -> None:
        """
        Update and draw this scene. Called once per frame while it is
        the active scene.
        """

    @abstractmethod
    def reset(self) -> None:
        """
        Reset this scene back to its starting state.
        """
