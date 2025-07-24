"""Main entry point for the text adventure game."""

from logging import raiseExceptions
from rich.live import Live
from rich.layout import Layout

from rich.traceback import install

from util.logger import logger
from core.core import Core

from rich.progress import Progress
import sys

from typing import Optional, Dict, Any



def main(**kwargs) -> None:
    """Main entry point for the game.
    
    Args:
        **kwargs: Optional keyword arguments:
            - chapter_id (str): Starting chapter ID (default: 0)
            - story (str): Story file path (default: "gemini_story.yaml")
            - mute (bool): Whether to mute sound (default: False)
            - tank (bool): Tank mode flag (default: False)
            - subchapter (str): Subchapter file path (default: "areas_to_explore.yaml")
    """
    try:
        # Initialize configuration
        config = {
            "chapter_id": kwargs.get("chapter_id", 9),
            "story": kwargs.get("story", "data/gemini_story.yaml"),
            "mute": kwargs.get("mute", False),
            "tank": kwargs.get("tank", False),
            "subchapter": kwargs.get("subchapter", "areas_to_explore.yaml"),
            "menu": kwargs.get("menu",True),
            "mute": kwargs.get("mute",False),
        }
        
        sound_enabled = not config["mute"]
        logger.info(f"Starting game with config: {config}")
        # Initialize core components
        core = Core(sound_enabled=True)
        core.menu = config["menu"]
       
        
        install(show_locals=True, console=core.rich_console)
        core.chapter_id = config["chapter_id"]
        #core.rich_console.force_terminal = True
        # core.rich_console.force_interactive = True
        core.run()
      
    except Exception as error:
        logger.error(f"Fatal error: {error}")
        raise
    finally:
        # Cleanup
        if 'core' in locals() and hasattr(core, 'input_block'):
            core.input_block.stop()


if __name__ == "__main__":
    try:
        main()
        print("Game completed successfully")
    except Exception as e:
        print(f"Game terminated with error: {e}")
        sys.exit(1)
    
