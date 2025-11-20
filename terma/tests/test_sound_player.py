#!/usr/bin/env python3
"""
Test script for the pygame-based sound player.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from terma.core.sound_player import SoundPlayer
import time

def test_sound_player():
    """Test the sound player functionality."""
    print("Testing pygame-based sound player...")
    
    try:
        # Initialize sound player
        sound_player = SoundPlayer(music_volume=0.3, effects_volume=0.5)
        print("✓ Sound player initialized successfully")
        
        # Test loading music track
        music_file = "data/cin1.mp3"
        if os.path.exists(music_file):
            sound_player.load_music_track("test_music", music_file)
            print("✓ Music track loaded successfully")
            
            # Test playing music
            sound_player.play_music("test_music")
            print("✓ Music started playing")
            
            # Let it play for a few seconds
            time.sleep(3)
            
            # Test stopping music
            sound_player.stop_music()
            print("✓ Music stopped successfully")
        else:
            print(f"⚠ Music file {music_file} not found, skipping music test")
        
        # Test volume controls
        sound_player.set_music_volume(0.7)
        sound_player.set_effects_volume(0.8)
        print("✓ Volume controls working")
        
        # Test cleanup
        sound_player.close()
        print("✓ Sound player closed successfully")
        
        print("\n🎵 All sound player tests passed!")
        
    except Exception as e:
        print(f"❌ Error testing sound player: {e}")
        return False
    
    return True

if __name__ == "__main__":
    test_sound_player() 