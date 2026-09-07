"""
Shared pytest configuration.

Forces pygame onto dummy video/audio drivers so the whole suite runs
headless (no real window or sound device needed), and does it before
pygame is ever imported by test code.
"""
import os

os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
os.environ.setdefault("SDL_AUDIODRIVER", "dummy")
