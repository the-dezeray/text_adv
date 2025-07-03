#!/usr/bin/env python3
"""
Example of how to use the typewriter effect in your text adventure game.
"""

from ui.options import TyperWritter, create_typewriter
from ui.console import Console
from core.core import Core
import time

def example_story_intro():
    """Example of using typewriter effect for story introduction."""
    
    # In your game, you would get the core from your main game loop
    # core = your_game_core_instance
    # console = core.console
    
    # Example usage:
    console = Console(core=Core())  # Replace with your actual core
    
    # Method 1: Direct creation
    intro_text = TyperWritter(
        text="Welcome to the mystical realm of Eldoria...",
        delay=0.05  # 50ms between characters
    )
    
    # Method 2: Using the utility function
    story_text = create_typewriter(
        text="You find yourself standing at the entrance of an ancient dungeon...",
        delay=0.03  # 30ms between characters
    )
    
    # Add them to the console
    console.print(intro_text)
    console.print(story_text)
    
    # In your game loop, you would refresh the console
    # The typewriter effect will automatically progress based on time
    console.refresh()

def example_dialogue():
    """Example of using typewriter effect for character dialogue."""
    
    console = Console(core=Core())  # Replace with your actual core
    
    # Create dialogue with different speeds
    npc_greeting = TyperWritter(
        text="Greetings, brave adventurer! I have been waiting for you...",
        delay=0.04
    )
    
    # Add to console
    console.print(npc_greeting)
    
    # The effect will automatically progress as the console refreshes
    console.refresh()

def example_with_styling():
    """Example of using typewriter effect with rich text styling."""
    
    console = Console(core=Core())  # Replace with your actual core
    
    # Create a typewriter with custom styling
    styled_text = TyperWritter(
        text="[bold red]DANGER![/bold red] The ancient evil has awakened...",
        delay=0.06
    )
    
    console.print(styled_text)
    console.refresh()

# Usage in your game:
"""
# In your main game loop or story system:

def show_story_text(text: str, delay: float = 0.03):
    '''Helper function to show story text with typewriter effect.'''
    typewriter = TyperWritter(text=text, delay=delay)
    self.core.console.print(typewriter)
    self.core.console.refresh()
    
    # Wait for the effect to complete
    while not typewriter.is_finished():
        time.sleep(0.1)  # Small delay
        self.core.console.refresh()

# Example usage:
show_story_text("You enter the dark cave...", delay=0.05)
show_story_text("The air is thick with ancient magic...", delay=0.04)
""" 