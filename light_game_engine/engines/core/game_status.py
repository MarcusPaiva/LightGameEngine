class GameStatus:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(GameStatus, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        self._running = True
        self._game_clock = 30

    @classmethod
    def reset_instance(cls):
        cls._instance = None

    def close_game(self):
        self._running = False

    @property
    def game_running(self):
        return self._running

    @property
    def game_clock(self):
        return self._game_clock

    @game_clock.setter
    def game_clock(self, value:int):
        self._game_clock = value