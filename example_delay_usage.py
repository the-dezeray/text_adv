#!/usr/bin/env python3
"""
Example showing how to use the Delay class in the game context.
"""

from ui.options import Delay, TyperWritter

def example_story_sequence():
    """Example of using Delay in a story sequence."""
    
    # This would be used in your game's story system
    story_sequence = [
        TyperWritter("You enter the dark cave...", delay=0.03),
        Delay(1.5),  # Pause for dramatic effect
        TyperWritter("The air is thick with ancient magic.", delay=0.03),
        Delay(0.8),  # Short pause
        TyperWritter("Something moves in the shadows...", delay=0.04),
        Delay(2.0),  # Longer pause for suspense
        TyperWritter("A pair of glowing eyes appears!", delay=0.02),
    ]
    
    return story_sequence

def example_combat_sequence():
    """Example of using Delay in combat sequences."""
    
    combat_sequence = [
        TyperWritter("You swing your sword!", delay=0.02),
        Delay(0.5),  # Brief pause for impact
        TyperWritter("The enemy staggers back...", delay=0.03),
        Delay(1.0),  # Pause for enemy reaction
        TyperWritter("Critical hit! 25 damage!", delay=0.02),
        Delay(0.8),  # Pause to let player read damage
    ]
    
    return combat_sequence

def example_menu_transition():
    """Example of using Delay for menu transitions."""
    
    menu_sequence = [
        TyperWritter("Loading inventory...", delay=0.05),
        Delay(1.2),  # Simulate loading time
        TyperWritter("Inventory loaded successfully!", delay=0.03),
        Delay(0.5),  # Brief pause before showing menu
    ]
    
    return menu_sequence

# Usage example:
# In your game code, you would do something like:
#
# def show_story():
#     sequence = example_story_sequence()
#     for item in sequence:
#         core.console.print(item)
#         # The console will automatically handle the timing
#         # and display updates through the fill_ui_table method 