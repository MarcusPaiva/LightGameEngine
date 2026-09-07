"""
Global game state: which scene is active, and whether the game is
running or paused. GameStatus and SceneManagement are singletons on
purpose, so any part of the game can read or change them without
having to pass an instance around.
"""
from typing import Dict, List

import pygame

from light_game_engine.screen import SurfaceScreen
from light_game_engine.scene.game_scene import GameScene

class GameStatus:
    """
    Whether the game is running and whether it's paused. This is a
    singleton: every call to GameStatus() returns the very same
    instance, so any part of the game sees the same state.
    """
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(GameStatus, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        # __init__ runs on every GameStatus() call, even when __new__
        # returns the existing instance - so without this guard, every
        # call would silently reset _paused and _game_is_running back
        # to their starting values.
        if self._initialized:
            return
        self._initialized = True
        self._paused = False
        self._game_is_running = True

    def set_game_is_running(self, value: bool):
        """
        Set whether the game should keep running.

        :param value: False to stop the main loop.
        """
        self._game_is_running = value

    def set_pause_game(self, value: bool):
        """
        Pause or unpause the game.

        :param value: True to pause, False to unpause.
        """
        self._paused = value

    @property
    def game_paused(self) -> bool:
        """
        :return: Whether the game is currently paused.
        :rtype: bool
        """
        return self._paused

    @property
    def game_is_running(self) -> bool:
        """
        :return: Whether the main loop should keep running.
        :rtype: bool
        """
        return self._game_is_running


class SceneManagement:
    """
    Holds every registered scene and tracks which one is active. This
    is a singleton: every call to SceneManagement() returns the very
    same instance, so any part of the game can register or switch
    scenes without needing a reference passed around.
    """
    _instance = None  # Class variable to hold the single instance

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(SceneManagement, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        # Same reason as GameStatus.__init__: without this guard, every
        # SceneManagement() call would wipe out every scene already
        # registered.
        if self._initialized:
            return
        self._initialized = True
        self._scenes: Dict[str, GameScene] = {}
        self._current_scene = ""

    def add_scene(self, scene_name:str, screen:GameScene):
        """
        Register a scene under a name. The first scene ever added
        becomes the active one automatically.

        :param scene_name: Name to register this scene under.
        :param screen: The scene itself.
        :return: This instance, for chaining.
        """
        if self._current_scene == "":
            self._current_scene = scene_name
        self._scenes[scene_name] = screen
        return self

    def set_current_scene(self, scene_name):
        """
        Switch to a different registered scene.

        :param scene_name: Name of the scene to switch to.
        :return: This instance, for chaining.
        """
        self._current_scene = scene_name
        return self

    def reset_current_scene(self):
        """
        Reset the active scene back to its starting state.

        :return: This instance, for chaining.
        """
        self._scenes[self._current_scene].reset()
        return self

    def get_current_scene(self) -> GameScene:
        """
        :return: The currently active scene.
        :rtype: GameScene
        """
        return self._scenes[self._current_scene]

    @property
    def get_current_scene_name(self) ->str:
        """
        :return: The name the active scene was registered under.
        :rtype: str
        """
        return self._current_scene

    def get_scene(self, scene_name:str) -> GameScene:
        """
        Look up a registered scene by name.

        :param scene_name: Name the scene was registered under.
        :return: The scene, or None if no scene was registered under
            that name.
        :rtype: GameScene
        """
        if scene_name in self._scenes.keys():
            return self._scenes[scene_name]

    def list_scene(self) -> List[str]:
        """
        :return: The names of every registered scene.
        :rtype: List[str]
        """
        return list(self._scenes.keys())

    def setup_scenes(self):
        """
        Call setup() on every registered scene.

        :return: This instance, for chaining.
        """
        for _, screen in self._scenes.items():
            screen.setup()
        return self



class GameManagement:
    """
    Runs the main game loop: pumps pygame events, updates and draws
    the active scene, and stops cleanly when the game is closed.
    """

    def __init__(self, screen: SurfaceScreen):
        """
        :param screen: Game window.
        """
        self._screen = screen
        self._game_status = GameStatus()
        self._scene_management = SceneManagement()

    def setup(self):
        """
        Call setup() on every registered scene. Call this once before
        :meth:`loop`.

        :return: This instance, for chaining.
        """
        self._scene_management.setup_scenes()
        return self

    @property
    def current_screen(self) -> str:
        """
        :return: The name of the currently active scene.
        :rtype: str
        """
        return self._scene_management.get_current_scene_name

    def exit_game(self):
        """
        Ask the main loop to stop. The window is closed once the loop
        actually exits, not immediately when this is called.
        """
        self._game_status.set_game_is_running(False)

    def loop(self):
        """
        The main game loop. Runs until the window is closed or
        :meth:`exit_game` is called, updating and drawing the active
        scene every frame it isn't paused.
        """
        while self._game_status.game_is_running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.exit_game()
            if not self._game_status.game_paused:
                self._scene_management.get_current_scene().loop()
                self._screen.flip()
        self._screen.quit()
