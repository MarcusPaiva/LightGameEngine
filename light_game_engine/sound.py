"""
Audio playback: short sound effects and looping background music.
"""
import pygame


class SoundEffect:
    """
    A short, one-shot sound effect.
    """

    def __init__(self, file: str):
        """
        :param file: Path to the sound file to load.
        """
        self.__sound = pygame.mixer.Sound(file)

    def set_volume(self, value: float):
        """
        Set this effect's playback volume.

        :param value: Volume, from 0.0 (silent) to 1.0 (full).
        :return: This instance, for chaining.
        :rtype: SoundEffect
        """
        self.__sound.set_volume(value)
        return self

    def play(self):
        """
        Play this effect once.

        :return: This instance, for chaining.
        :rtype: SoundEffect
        """
        self.__sound.play(0)
        return self


class Music:
    """
    The single, shared background-music channel.
    """

    def __init__(self, file: str):
        """
        Load a music track without starting playback.

        :param file: Path to the music file to load.
        """
        self.__sound = pygame.mixer.music
        self.__sound.load(file)

    def set_volume(self, value: float):
        """
        Set the music playback volume.

        :param value: Volume, from 0.0 (silent) to 1.0 (full).
        :return: This instance, for chaining.
        :rtype: Music
        """
        self.__sound.set_volume(value)
        return self

    def play_loop(self):
        """
        Start playing the loaded track on an infinite loop.

        :return: This instance, for chaining.
        :rtype: Music
        """
        self.__sound.play(-1, 0.0)
        return self

    def stop_loop(self):
        """
        Stop playback entirely.

        :return: This instance, for chaining.
        :rtype: Music
        """
        self.__sound.stop()
        return self

    def pause_loop(self):
        """
        Pause playback, keeping the current position.

        :return: This instance, for chaining.
        :rtype: Music
        """
        self.__sound.pause()
        return self

    def resume_loop(self):
        """
        Resume playback from where it was paused.

        :return: This instance, for chaining.
        :rtype: Music
        """
        self.__sound.unpause()
        return self
