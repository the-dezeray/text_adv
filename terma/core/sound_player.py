from typing import Dict, Optional
from pathlib import Path
from terma.util.logger import logger

class SoundPlayer:
    def __init__(self, enable: bool = True, music_volume: float = 0.5, effects_volume: float = 0.7):
        self.enabled = enable
        self._music_tracks: Dict[str, str] = {}
        self._sound_effects = {}

        self._music_volume = max(0.0, min(1.0, music_volume))
        self._effects_volume = max(0.0, min(1.0, effects_volume))
        self._current_music: Optional[str] = None

        self._pygame_loaded = False  # Track whether pygame is initialized

        if not enable:
            logger.info("Sound disabled — skipping pygame initialization")
            return

        self._init_pygame()

    def _init_pygame(self):
        """Import and initialize pygame mixer only once."""
        if self._pygame_loaded:
            return

        try:
            import pygame
            pygame.mixer.init()
            self.pygame = pygame
            self._pygame_loaded = True
            logger.info("Pygame mixer initialized")
        except Exception as e:
            logger.error(f"Failed to initialize audio: {e}")
            self.enabled = False

    def load_music_track(self, track_name: str, file_path: str | Path):
        if not self.enabled:
            return

        self._init_pygame()

        file_path = str(file_path)
        self.pygame.mixer.music.load(file_path)
        self._music_tracks[track_name] = file_path

    def load_sound_effect(self, effect_name: str, file_path: str | Path):
        if not self.enabled:
            return

        self._init_pygame()

        sound = self.pygame.mixer.Sound(str(file_path))
        self._sound_effects[effect_name] = sound

    def play_music(self, track_name: str, loops: int = -1):
        if not self.enabled:
            return

        self._init_pygame()

        self.stop_music()
        path = self._music_tracks[track_name]
        self.pygame.mixer.music.load(path)
        self.pygame.mixer.music.set_volume(self._music_volume)
        self.pygame.mixer.music.play(loops)

    def play_sound_effect(self, effect_name: str):
        if not self.enabled:
            return

        self._init_pygame()

        sound = self._sound_effects[effect_name]
        sound.set_volume(self._effects_volume)
        sound.play()

    def stop_music(self):
        if self.enabled and self._pygame_loaded:
            self.pygame.mixer.music.stop()

    def close(self):
        if self.enabled and self._pygame_loaded:
            self.pygame.mixer.quit()
            logger.info("Sound player closed")
