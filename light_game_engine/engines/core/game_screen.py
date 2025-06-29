from abc import ABC, abstractmethod

__all__ = ["GameScene"]

class GameScene(ABC):

    def __init__(self):
        self.__geometry = []

    @abstractmethod
    def setup(self) -> None:
        """
        Screen's setup.
        """
        pass

    @abstractmethod
    def update(self) -> None:
        """
        Screen's update process.
        """
        pass

    def draw(self):
        """
        Screen's draw event.
        """
        return self.__geometry