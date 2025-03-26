import sounddevice as sd
import soundfile as sf
import threading
import queue
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
        # Sound collections
        self._music_tracks: Dict[str, str] = {}
        self._sound_effects: Dict[str, str] = {}
        
        # Volume settings
        self._music_volume = max(0.0, min(1.0, music_volume))
        self._effects_volume = max(0.0, min(1.0, effects_volume))
        
        # Music playback management
        self._current_music: Optional[str] = None
        self._music_stop_event = threading.Event()
        self._music_thread: Optional[threading.Thread] = None
        
    def load_music_track(self, track_name: str, file_path: str):
        """
        Load a music track into the player's collection.
        
        :param track_name: Identifier for the track
        :param file_path: Path to the music file
        """
        try:
            # Verify file can be opened
            with sf.SoundFile(file_path) as f:
                pass
            self._music_tracks[track_name] = file_path
        except Exception as e:
            logger.critical(e)
            raise FileNotFoundError(f"Music file error: {file_path} - {e}")

    def load_sound_effect(self, effect_name: str, file_path: str):
        """
        Load a sound effect into the player's collection.
        
        :param effect_name: Identifier for the sound effect
        :param file_path: Path to the sound effect file
        """
        try:
            # Verify file can be opened
            with sf.SoundFile(file_path) as f:
                pass
            self._sound_effects[effect_name] = file_path
        except Exception as e:
            raise FileNotFoundError(f"Sound effect file error: {file_path} - {e}")

    def _play_music_loop(self, file_path: str):
        """
        Internal method to continuously play music in a thread.
        
        :param file_path: Path to the music file
        """
        while not self._music_stop_event.is_set():
            data, samplerate = sf.read(file_path)
            # Apply volume scaling
            data = data * self._music_volume
            
            try:
                sd.play(data, samplerate)
                sd.wait()
            except sd.PortAudioError:
                # Handle potential playback interruptions
                break

    def play_music(self, track_name: str, loops: int = -1):
        """
        Play background music track.
        
        :param track_name: Name of the track to play
        :param loops: Number of times to repeat (-1 for infinite)
        """
        if track_name not in self._music_tracks:
            raise ValueError(f"Music track '{track_name}' not loaded")
        
        # Stop current music if playing
        self.stop_music()
        
        # Reset stop event
        self._music_stop_event.clear()
        
        # Start new music thread
        music_path = self._music_tracks[track_name]
        self._music_thread = threading.Thread(
            target=self._play_music_loop, 
            args=(music_path,), 
            daemon=True
        )
        self._music_thread.start()
        
        self._current_music = track_name

    def play_sound_effect(self, effect_name: str):
        """
        Play a sound effect.
        
        :param effect_name: Name of the sound effect to play
        """
        if effect_name not in self._sound_effects:
            raise ValueError(f"Sound effect '{effect_name}' not loaded")
        
        # Read and play sound effect
        effect_path = self._sound_effects[effect_name]
        data, samplerate = sf.read(effect_path)
        
        # Apply volume scaling
        data = data * self._effects_volume
        
        # Play in a separate thread to avoid blocking
        def play_effect():
            sd.play(data, samplerate)
            sd.wait()
        
        threading.Thread(target=play_effect, daemon=True).start()

    def set_music_volume(self, volume: float):
        """
        Set the volume for background music.
        
        :param volume: Volume level (0.0 to 1.0)
        """
        self._music_volume = max(0.0, min(1.0, volume))

    def set_effects_volume(self, volume: float):
        """
        Set the volume for sound effects.
        
        :param volume: Volume level (0.0 to 1.0)
        """
        self._effects_volume = max(0.0, min(1.0, volume))

    def stop_music(self):
        """Stop the current music track."""
        if self._music_thread:
            # Signal the music thread to stop
            self._music_stop_event.set()
            
            # Wait a short time for the thread to terminate
            self._music_thread.join(timeout=1)
            
            # Stop any ongoing sound playback
            sd.stop()
            
            self._current_music = None
            self._music_thread = None

    def close(self):
        """
        Clean up and stop all sound playback.
        Call this when closing the game.
        """
        self.stop_music()
        sd.stop()



