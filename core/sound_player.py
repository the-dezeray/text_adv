import pygame
import threading
import time
from typing import Dict, Optional
from util.logger import logger

class SoundPlayer:
    def __init__(self, music_volume: float = 0.5, effects_volume: float = 0.7):
        """
        Initialize the sound player with separate volume controls.
        
        :param music_volume: Volume for background music (0.0 to 1.0)
        :param effects_volume: Volume for sound effects (0.0 to 1.0)
        """
        # Initialize pygame mixer
        try:
            pygame.mixer.init()
            logger.info("Pygame mixer initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize pygame mixer: {e}")
            raise
        
        # Sound collections
        self._music_tracks: Dict[str, str] = {}
        self._sound_effects: Dict[str, pygame.mixer.Sound] = {}
        
        # Volume settings
        self._music_volume = max(0.0, min(1.0, music_volume))
        self._effects_volume = max(0.0, min(1.0, effects_volume))
        
        # Music playback management
        self._current_music: Optional[str] = None
        
    def load_music_track(self, track_name: str, file_path: str):
        """
        Load a music track into the player's collection.
        
        :param track_name: Identifier for the track
        :param file_path: Path to the music file
        """
        try:
            # Verify file can be opened by pygame
            pygame.mixer.music.load(file_path)
            self._music_tracks[track_name] = file_path
            logger.info(f"Music track loaded: {track_name} -> {file_path}")
        except Exception as e:
            logger.critical(f"Music file error: {file_path} - {e}")
            raise FileNotFoundError(f"Music file error: {file_path} - {e}")

    def load_sound_effect(self, effect_name: str, file_path: str):
        """
        Load a sound effect into the player's collection.
        
        :param effect_name: Identifier for the sound effect
        :param file_path: Path to the sound effect file
        """
        try:
            # Load sound effect with pygame
            sound = pygame.mixer.Sound(file_path)
            self._sound_effects[effect_name] = sound
            logger.info(f"Sound effect loaded: {effect_name} -> {file_path}")
        except Exception as e:
            logger.error(f"Sound effect file error: {file_path} - {e}")
            raise FileNotFoundError(f"Sound effect file error: {file_path} - {e}")

    def play_music(self, track_name: str, loops: int = -1):
        """
        Play background music track.
        
        :param track_name: Name of the track to play
        :param loops: Number of times to repeat (-1 for infinite)
        """
        if track_name not in self._music_tracks:
            raise ValueError(f"Music track '{track_name}' not loaded")
        
        try:
            # Stop current music if playing
            self.stop_music()
            
            # Load and play the music track
            music_path = self._music_tracks[track_name]
            pygame.mixer.music.load(music_path)
            pygame.mixer.music.set_volume(self._music_volume)
            pygame.mixer.music.play(loops)
            
            self._current_music = track_name
            logger.info(f"Playing music: {track_name}")
        except Exception as e:
            logger.error(f"Error playing music {track_name}: {e}")
            raise

    def play_sound_effect(self, effect_name: str):
        """
        Play a sound effect.
        
        :param effect_name: Name of the sound effect to play
        """
        if effect_name not in self._sound_effects:
            raise ValueError(f"Sound effect '{effect_name}' not loaded")
        
        try:
            # Get the sound effect and play it
            sound = self._sound_effects[effect_name]
            sound.set_volume(self._effects_volume)
            sound.play()
            logger.info(f"Playing sound effect: {effect_name}")
        except Exception as e:
            logger.error(f"Error playing sound effect {effect_name}: {e}")
            raise

    def set_music_volume(self, volume: float):
        """
        Set the volume for background music.
        
        :param volume: Volume level (0.0 to 1.0)
        """
        self._music_volume = max(0.0, min(1.0, volume))
        pygame.mixer.music.set_volume(self._music_volume)
        logger.info(f"Music volume set to: {self._music_volume}")

    def set_effects_volume(self, volume: float):
        """
        Set the volume for sound effects.
        
        :param volume: Volume level (0.0 to 1.0)
        """
        self._effects_volume = max(0.0, min(1.0, volume))
        # Update volume for all loaded sound effects
        for sound in self._sound_effects.values():
            sound.set_volume(self._effects_volume)
        logger.info(f"Effects volume set to: {self._effects_volume}")

    def stop_music(self):
        """Stop the current music track."""
        try:
            pygame.mixer.music.stop()
            self._current_music = None
            logger.info("Music stopped")
        except Exception as e:
            logger.error(f"Error stopping music: {e}")

    def pause_music(self):
        """Pause the current music track."""
        try:
            pygame.mixer.music.pause()
            logger.info("Music paused")
        except Exception as e:
            logger.error(f"Error pausing music: {e}")

    def unpause_music(self):
        """Unpause the current music track."""
        try:
            pygame.mixer.music.unpause()
            logger.info("Music unpaused")
        except Exception as e:
            logger.error(f"Error unpausing music: {e}")

    def close(self):
        """
        Clean up and stop all sound playback.
        Call this when closing the game.
        """
        try:
            self.stop_music()
            pygame.mixer.quit()
            logger.info("Sound player closed")
        except Exception as e:
            logger.error(f"Error closing sound player: {e}")



