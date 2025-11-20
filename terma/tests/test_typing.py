#!/usr/bin/env python3
"""Test script for the typing feature"""

from ui.options import TyperWritter
import time

def test_typing():
    """Test the TyperWritter class"""
    print("Testing TyperWritter...")
    
    # Create a TyperWritter instance
    typer = TyperWritter("Hello, this is a test of the typing feature!", delay=0.1)
    
    print("Starting typing animation...")
    print("=" * 50)
    
    # Simulate the typing animation
    while typer.is_typing:
        typer.update()
        print(f"\rTyped: '{typer.typed}'", end="", flush=True)
        time.sleep(0.05)  # Small delay to see the animation
    
    print(f"\n\nFinal result: '{typer.typed}'")
    print("=" * 50)
    print("Typing test completed!")

if __name__ == "__main__":
    test_typing() 