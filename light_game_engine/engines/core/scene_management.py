from typing import Dict

import pygame

from light_game_engine.engines.core.game_screen import GameScene

__all__ = ["SceneManagement","SceneEvent"]

from light_game_engine.engines.core.game_status import GameStatus


class SceneEvent:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(SceneEvent, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        self._current_screen:str = None

    @property
    def current_screen(self) -> str:
        return self._current_screen

    def set_current_screen(self, current_screen:str):
        self._current_screen = current_screen


class SceneManagement:
    def __init__(self):
        """
        Screen management's initializer.
        """
        self.__screens: Dict[str, GameScene] = {}
        self.__game_status = GameStatus()
        self._clock = pygame.time.Clock()
        self.__screen_event = SceneEvent()

    def register_screen(self, screen_name: str, screen: GameScene) -> None:
        """
        Register game screen.
        :param screen_name: Game Screen's name.
        :param screen: Game Screen.
        """
        if screen_name not in self.__screens.keys():
            self.__screens[screen_name] = screen
            if len(self.__screens) == 1:
                self.__screen_event.set_current_screen(screen_name)

    def start(self):
        """
        Game start.
        """
        for screen in self.__screens.keys():
            self.__screens[screen].setup()

        self.__game_loop()

    def exit_game(self):
        """
        Exit game.
        """
        self.__game_status.close_game()

    def __game_loop(self):
        """
        Main Game's loop.
        """
        current_screen = self.__screens[self.__screen_event.current_screen]
        while self.__game_status.game_running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.exit_game()
            current_screen.update()
            current_screen.draw()
            pygame.display.flip()
            self._clock.tick(self.__game_status.game_clock)
