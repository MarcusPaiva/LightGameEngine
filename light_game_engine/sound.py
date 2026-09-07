"""
Playing sound: short sound effects, and looping background music.
"""
import pygame


class SoundEffect:
    """
    A short sound that plays once, like a jump or a hit sound.
    """

    def __init__(self, file: str):
        """
        :param file: Path to the sound file to load.
        """
        self.__sound = pygame.mixer.Sound(file)

    def set_volume(self, value: float):
        """
        Set how loud this sound effect plays.

        :param value: Volume, from 0.0 (silent) to 1.0 (full volume).
        :return: This instance, for chaining.
        :rtype: SoundEffect
        """
        self.__sound.set_volume(value)
        return self

    def play(self):
        """
        Play this sound effect once.

        :return: This instance, for chaining.
        :rtype: SoundEffect
        """
        self.__sound.play(0)
        return self


class Music:
    """
    The one shared background-music channel for the whole game.
    """

    def __init__(self, file: str):
        """
        Load a music track, but do not start playing it yet.

        :param file: Path to the music file to load.
        """
        self.__sound = pygame.mixer.music
        self.__sound.load(file)

    def set_volume(self, value: float):
        """
        Set how loud the music plays.

        :param value: Volume, from 0.0 (silent) to 1.0 (full volume).
        :return: This instance, for chaining.
        :rtype: Music
        """
        self.__sound.set_volume(value)
        return self

    def play_loop(self):
        """
        Start playing the loaded track, and keep repeating it forever.

        :return: This instance, for chaining.
        :rtype: Music
        """
        self.__sound.play(-1, 0.0)
        return self

    def stop_loop(self):
        """
        Stop the music completely.

        :return: This instance, for chaining.
        :rtype: Music
        """
        self.__sound.stop()
        return self

    def pause_loop(self):
        """
        Pause the music. It stays at the same spot until resumed.

        :return: This instance, for chaining.
        :rtype: Music
        """
        self.__sound.pause()
        return self

    def resume_loop(self):
        """
        Continue playing the music from where it was paused.

        :return: This instance, for chaining.
        :rtype: Music
        """
        self.__sound.unpause()
        return self
