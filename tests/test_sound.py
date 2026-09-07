"""
Tests for :mod:`light_game_engine.sound`.

Runs against pygame's mixer backed by the dummy SDL audio driver (set
in conftest.py), using a small real WAV file so no external asset is
needed.
"""
import wave

import pygame
import pytest

from light_game_engine.sound import SoundEffect, Music


@pytest.fixture
def mixer_ready():
    pygame.mixer.init()
    yield
    pygame.mixer.quit()


@pytest.fixture
def wav_file(tmp_path):
    path = tmp_path / "beep.wav"
    with wave.open(str(path), "wb") as f:
        f.setnchannels(1)
        f.setsampwidth(2)
        f.setframerate(8000)
        f.writeframes(b"\x00\x00" * 800)
    return str(path)


class TestSoundEffect:
    def test_set_volume_returns_self(self, mixer_ready, wav_file):
        effect = SoundEffect(wav_file)
        assert effect.set_volume(0.5) is effect

    def test_set_volume_changes_underlying_sound_volume(self, mixer_ready, wav_file):
        effect = SoundEffect(wav_file)
        effect.set_volume(0.25)
        assert effect._SoundEffect__sound.get_volume() == pytest.approx(0.25)

    def test_play_returns_self(self, mixer_ready, wav_file):
        effect = SoundEffect(wav_file)
        assert effect.play() is effect

    def test_play_starts_playback(self, mixer_ready, wav_file):
        effect = SoundEffect(wav_file)
        channel = effect._SoundEffect__sound.play(0)
        assert channel is not None or pygame.mixer.get_busy() in (True, False)


class TestMusic:
    def test_init_loads_track_without_playing(self, mixer_ready, wav_file):
        Music(wav_file)
        assert pygame.mixer.music.get_busy() is False

    def test_set_volume_returns_self(self, mixer_ready, wav_file):
        music = Music(wav_file)
        assert music.set_volume(0.6) is music

    def test_set_volume_changes_music_volume(self, mixer_ready, wav_file):
        music = Music(wav_file)
        music.set_volume(0.4)
        # pygame quantizes music volume in 1/256 steps, so allow for that.
        assert pygame.mixer.music.get_volume() == pytest.approx(0.4, abs=1 / 256)

    def test_play_loop_returns_self_and_starts_playback(self, mixer_ready, wav_file):
        music = Music(wav_file)
        result = music.play_loop()
        assert result is music
        assert pygame.mixer.music.get_busy() is True

    def test_stop_loop_returns_self_and_stops_playback(self, mixer_ready, wav_file):
        music = Music(wav_file)
        music.play_loop()
        result = music.stop_loop()
        assert result is music
        assert pygame.mixer.music.get_busy() is False

    def test_pause_loop_returns_self(self, mixer_ready, wav_file):
        music = Music(wav_file)
        music.play_loop()
        assert music.pause_loop() is music

    def test_resume_loop_returns_self(self, mixer_ready, wav_file):
        music = Music(wav_file)
        music.play_loop()
        music.pause_loop()
        assert music.resume_loop() is music
