"""Core game engine for the text adventure game."""

from util.file_handler import load_yaml_file
from ui.options import CustomRenderable, GridOfChoices
from rich.layout import Layout
from objects.entities import Entities
from objects.item import Items
from objects.player import Player
from util.logger import logger
from rich.padding import Padding
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn
from typing import TYPE_CHECKING, Dict, Any, Optional, List, cast
import datetime
import sys
import yaml
from pathlib import Path
from core.story import GameEngine

if TYPE_CHECKING:
    from ui.console import Console
    from rich.live import Live
    from rich.console import Console as RichConsole

# Import event handlers
from core.events.navigate import navigate
from core.events.explore import explore
from core.functions import receive
from core.events.fight import fight
from core.events.rest import rest
from core.events.read import read
from core.events.meditate import meditate
from core.events.run import run
from core.events.search import search
from core.events.trap import trap
from core.events.sneak import sneak
from core.events.encounter import encounter

from core.events.haverst import harvest
from core.events.interact import interact
from core.events.investigate import investigate
from core.events.place import place
from core.events.shop import shop
from core.events.search_in import search_in
from core.events.skill_check import skill_check
from core.events.receive_item import receive_item
from core.events.escape import attempt_escape
from rich.live import Live

from core.non_blocking_input import NonBlockingInput


class Core:
    """Core game engine that manages the game state and coordinates between components."""

    def __init__(self) -> None:
        """Initialize the core game engine."""
        # UI Components
        self.rich_console: "RichConsole"
        self.rich_live_instance: "Live"
        self._layout = Layout()
        
        # Game State
        self.running: bool = True
        self.in_fight: bool = False
        self.in_game: bool = True
        self.move_on: bool = True
        self._state: str = "INGAME"
        self._command_mode: bool = False
        self._disable_command_mode: bool = False
        
        # Story and Progress
        self.game_engine = GameEngine()
        self.next_node: Optional[str] = None
        self.current_entry_text: str = ""
        
        # Player and Entities
        self.player = Player()
        self.entity: Optional[Entities] = None
        self.others: List[Any] = []
        
        # Input and Control
        self.input_block = NonBlockingInput()
        self.key_listener = None
        self.selected_option: int = 0
        self.s: str = "options"
        
        # Progress Tracking
        self.job_progress = Progress(
            "{task.description}",
            SpinnerColumn(),
            BarColumn(),
            TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
        )
        self.overall_progress = Progress()
        self.overall_task = self.overall_progress.add_task("All Jobs", total=1000)
        
        # Initialize console
        from ui.console import Console
        self.console = cast("Console", Console(core=self))
        
        # Post-initialization
        self._post_initialize()
        
        logger.info("Core game engine initialized")

    def _post_initialize(self) -> None:
        """Perform post-initialization tasks."""
        current_time = datetime.datetime.now()
        logger.info(f"New game instance {current_time}")
        self.game_engine.validate_story()

    @property
    def chapter_id(self) -> str:
        """Get the current chapter ID."""
        return str(self.game_engine.current_node_id)

    @chapter_id.setter
    def chapter_id(self, value: str) -> None:
        """Set the current chapter ID.
        
        Args:
            value: The chapter ID to set
        """
        if value == "-1" or value == -1:
            self.game_engine.current_node_id = "-1"
        else:
            self.game_engine.set_current_node(str(value))

    def execute_yaml_function(self, func: str) -> Any:
        """Execute a function defined in YAML.
        
        Args:
            func: The function to execute
            
        Returns:
            Any: The result of the function execution
        """
        logger.info(f"Executing function: {func}")
        local_scope = {"core": self}
        
        try:
            return exec(func, globals(), local_scope)
        except Exception as e:
            logger.error(f"Error executing function {func}: {e}")
            raise

    @property
    def command_mode(self) -> bool:
        """Get the command mode state."""
        return self._command_mode

    @command_mode.setter
    def command_mode(self, value: bool) -> None:
        """Set the command mode state.
        
        Args:
            value: The new command mode state
        """
        if not self._disable_command_mode:
            self._command_mode = bool(value)
            self.console.toggle_command_mode()
            self.chapter_id = "1"
            self.console.layout = "INGAME"

    def TERMINATE(self) -> None:
        """Terminate the game and clean up resources."""
        logger.info("Terminating game")
        self.running = False
        if self.rich_live_instance:
            self.rich_live_instance.stop()
        if self.input_block:
            self.input_block.stop()
        sys.exit(0)

    def continue_game(self) -> None:
        """Continue the game from the current state."""
        if self.chapter_id == "-1":
            self.chapter_id = 0
            return

        current_node = self.game_engine.get_current_node()
        if not current_node:
            logger.error(f"Current node {self.chapter_id} not found")
            # Reset to a valid starting point
            self.chapter_id = "0"
            current_node = self.game_engine.get_current_node()
            if not current_node:
                logger.critical("Failed to load starting node")
                return
        
        # Display chapter title
        from rich.rule import Rule
        title = "[b green]\uf1bb Deep Forest[/b green]"
        self.console.print(Rule(title=title, align="left", style="cyan"))
        
        # Display chapter text
        from rich.text import Text
        ui_text = Text(text=current_node.text, justify="full")
        self.console.print(Padding(ui_text))
        
        # Display choices
        self.console.print(GridOfChoices(current_node.choices))
        
        self.console.refresh()

    def goto_next(self) -> None:
        """Go to the next node in the story."""
        if not self.next_node:
            logger.error("No next node specified")
            return
            
        logger.info(f"Going to next node: {self.next_node}")
        self.chapter_id = self.next_node
        self.continue_game()

    def execute_command(self, command: str) -> None:
        """Execute a game command.
        
        Args:
            command: The command to execute
        """
        try:
            match command.lower():
                case "kill":
                    self.TERMINATE()
                case _:
                    logger.warning(f"Unknown command: {command}")
        except Exception as e:
            logger.error(f"Error executing command {command}: {e}")

    def show_settings(self) -> None:
        """Show the game settings menu."""
        logger.info("Showing settings menu")
        self._state = "SETTINGS"
        self.console.layout = "SETTINGS"
        self.console.refresh()

    def show_stats(self) -> None:
        """Show the player's statistics."""
        logger.info("Showing player stats")
        self._state = "STATS"
        self.console.layout = "STATS"
        self.console.refresh()
