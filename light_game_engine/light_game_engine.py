import pygame

__all__ = ["LightGameEngine"]

from light_game_engine.engines.core.game_screen import GameScene
from light_game_engine.engines.core.scene_management import SceneManagement


class LightGameEngine:
    def __init__(self, window_width: int, window_height: int, window_caption: str = "Light Game Engine"):
        """
        Light Game Engine initializer.
        :param window_width: Game Window width.
        :param window_height: Game Window height.
        :param window_caption: Game Window Caption.
        """

        pygame.init()
        self.__screen = pygame.display.set_mode((window_width, window_height))
        pygame.display.set_caption(window_caption)
        self.__screen_management = SceneManagement()
        pygame.font.init()
        pygame.mixer.init()

    def add_screen_game(self, screen_name: str, screen: GameScene) -> None:
        """
        Add game screen.
        :param screen_name: Game Screen's name.
        :param screen: Game Screen.
        """
        self.__screen_management.register_screen(screen_name, screen)

    def start(self):
        """
        Start game.
        """
        self.__screen_management.start()
