"""
Shared fixtures for the scene test package.

GameStatus and SceneManagement are singletons by design (see
game_management.py), so their state would otherwise leak between
tests. This fixture forces a fresh instance for every test.
"""
import pytest

from light_game_engine.scene.game_management import GameStatus, SceneManagement


@pytest.fixture(autouse=True)
def reset_singletons():
    GameStatus._instance = None
    SceneManagement._instance = None
    yield
    GameStatus._instance = None
    SceneManagement._instance = None
