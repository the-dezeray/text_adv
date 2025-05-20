"""Main entry point for the text adventure game."""

from logging import raiseExceptions
from rich.live import Live
from rich.layout import Layout
from rich.console import Console
from rich.traceback import install
from readchar import readkey
from util.logger import logger
from core.core import Core
from core.keyboard import KeyboardControl
from rich.progress import Progress
import sys
import select
import threading
import queue
from typing import Optional, Dict, Any


class NonBlockingInput:
    def __init__(self):
        self.input_queue = queue.Queue()
        self.running = True
        self.thread = threading.Thread(target=self._input_thread, daemon=True)
        self.thread.start()

    def _input_thread(self):
        while self.running:
            try:
                key = readkey()
                if key:
                    self.input_queue.put(key)
            except Exception as e:
                logger.error(f"Error in input thread: {e}")
                self.running = False

    def stop(self):
        self.running = False
        self.thread.join(timeout=1.0)

    def get_key(self) -> Optional[str]:
        try:
            return self.input_queue.get_nowait()
        except queue.Empty:
            return None


def non_blocking_readkey() -> Optional[str]:
    """Check if a key is available without blocking.
    
    Returns:
        Optional[str]: The key pressed or None if no key was pressed.
    """
    try:
        if sys.stdin in select.select([sys.stdin], [], [], 0)[0]:
            key = sys.stdin.read(1)

            # Check if it's an escape sequence (for arrow keys)
            if key == "\x1b":  # The beginning of an escape sequence
                key += sys.stdin.read(2)  # Read the rest of the escape sequence
                if key == "\x1b[A":
                    return "UP"  # Up arrow key
                elif key == "\x1b[B":
                    return "DOWN"  # Down arrow key
                elif key == "\x1b[C":
                    return "RIGHT"  # Right arrow key
                elif key == "\x1b[D":
                    return "LEFT"  # Left arrow key
            elif key == "q":
                return "q"  # 'q' key
            elif key == "a":
                return "a"  # 'a' key

            return None  # No relevant key pressed
        return None
    except Exception as e:
        logger.error(f"Error reading key: {e}")
        return None


def main(**kwargs) -> None:
    """Main entry point for the game.
    
    Args:
        **kwargs: Optional keyword arguments:
            - chapter_id (str): Starting chapter ID (default: "1a")
            - story (str): Story file path (default: "story.yaml")
            - mute (bool): Whether to mute sound (default: False)
            - tank (bool): Tank mode flag (default: False)
            - subchapter (str): Subchapter file path (default: "areas_to_explore.yaml")
    """
    try:
        # Initialize configuration
        config = {
            "chapter_id": kwargs.get("chapter_id", "1a"),
            "story": kwargs.get("story", "story.yaml"),
            "mute": kwargs.get("mute", False),
            "tank": kwargs.get("tank", False),
            "subchapter": kwargs.get("subchapter", "areas_to_explore.yaml")
        }
        
        logger.info(f"Starting game with config: {config}")

        # Initialize core components
        core = Core()
        core.rich_console = Console(color_system="truecolor", style="bold black", quiet=True)
        install(show_locals=True, console=core.rich_console)
        core.chapter_id = config["chapter_id"]
        core.rich_console.force_terminal = True
        core.rich_console.force_interactive = True
        core.rich_console.stderr = True
        core.rich_console.quiet = False
        
        keyboard_controller = KeyboardControl(core=core)
        core.input_block = NonBlockingInput()

        try:
            with Live(
                Layout(),
                auto_refresh=True,
                screen=True,
                console=core.rich_console,
            ) as core.rich_live_instance:
                #core.console.show_menu()
                core.console._transtion_layout("INGAME")
                
                while core.running:
                    try:
                        key = core.input_block.get_key()
                        if key:
                            keyboard_controller.execute_on_key(key)
                        
                        # Update progress bars
                        for job in core.job_progress.tasks:
                            if not job.finished:
                                core.job_progress.advance(job.id)
                    except Exception as e:
                        logger.error(f"Error in main game loop: {e}")
                        continue

        except Exception as e:
            logger.error(f"Error in Live display: {e}")
            raise

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
