#!/usr/bin/env python3
"""
Test script to demonstrate the Delay functionality.
"""

import time
from ui.options import Delay, TyperWritter

def test_delay():
    """Test the Delay class functionality."""
    print("Testing Delay functionality...")
    
    # Create a delay of 2 seconds
    delay = Delay(duration=2.0)
    
    print("Starting 2-second delay...")
    start_time = time.time()
    
    # Simulate the update loop
    while delay.update():
        print(f"Delaying... {time.time() - start_time:.1f}s elapsed")
        time.sleep(0.1)  # Small sleep to prevent busy waiting
    
    print(f"Delay complete! Total time: {time.time() - start_time:.1f}s")

def test_delay_with_typing():
    """Test Delay combined with TyperWritter."""
    print("\nTesting Delay with TyperWritter...")
    
    # Create a typing animation
    typer = TyperWritter("Hello, this is a test message!", delay=0.05)
    
    # Create a delay
    delay = Delay(duration=1.0)
    
    print("Starting combined test...")
    
    # Simulate the update loop
    while typer.update() or delay.update():
        if typer.is_typing:
            print(f"Typing: {typer.typed}")
        if delay.is_delaying:
            print("Delaying...")
        time.sleep(0.05)
    
    print("Combined test complete!")

if __name__ == "__main__":
    test_delay()
    test_delay_with_typing() 