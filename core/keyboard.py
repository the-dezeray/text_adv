"""Handles keyboard input and control for the game."""

from __future__ import annotations

from core.core import Core
from util.logger import logger
from ui.options import get_selectable_options, CustomRenderable
from typing import TYPE_CHECKING, Dict, Callable, Optional, Any
from readchar import readkey
from readchar import key as KEY

if TYPE_CHECKING:
    from core.core import Core


class KeyboardControl:
    """Handles all keyboard input and control for the game.
    
    This class manages keyboard input, command mode, and option selection.
    It provides a centralized way to handle all keyboard interactions.
    """
    
    def __init__(self, core: Core):
        """Initialize the keyboard controller.
        
        Args:
            core: The game's core instance
        """
        self.core = core
        self.current_entry_text = ""
        self._setup_key_actions()
        logger.info("Keyboard controller initialized")

    def _setup_key_actions(self) -> None:
        """Setup the key action mappings."""
        self.key_actions: Dict[str, Callable] = {
            KEY.BACKSPACE: self.handle_backspace,
            KEY.LEFT: lambda: self.scroll_options(1),
            KEY.RIGHT: lambda: self.scroll_options(-1),
            KEY.UP: lambda: self.scroll_options(1),
            KEY.DOWN: lambda: self.scroll_options(-1),
            KEY.ENTER: self.handle_enter,
            "A": self._handle_stats,
            "S": self._handle_settings,
            "M": self.core.console.show_menu,
            "I": self.core.console.show_inventory,
            'q': self.handle_escape,
            ":": self.handle_command_mode,
        }

    def execute_on_key(self, key: str) -> None:
        """Execute the appropriate action for the given key.
        
        Args:
            key: The key that was pressed
        """
        try:
            if self.core.command_mode:
                self._handle_command_mode_input(key)
            else:
                action = self.key_actions.get(key)
                if action:
                    action()
                else:
                    logger.debug(f"Unhandled key: {key}")

            self.core.console.refresh()
        except Exception as e:
            logger.error(f"Error executing key action: {e}")

    def _handle_command_mode_input(self, key: str) -> None:
        """Handle input while in command mode.
        
        Args:
            key: The key that was pressed
        """
        if key == "Q":
            self.handle_escape()
        elif key == ":":
            self.handle_command_mode()
        elif key == KEY.ENTER:
            self._execute_command()
        elif key == KEY.BACKSPACE:
            self.handle_backspace()
        else:
            self.core.current_entry_text += key

    def _execute_command(self) -> None:
        """Execute the current command and clear the input."""
        try:
            self.core.execute_command(self.core.current_entry_text)
            self.core.current_entry_text = ""
        except Exception as e:
            logger.error(f"Error executing command: {e}")

    def handle_command_mode(self) -> None:
        """Toggle command mode on/off."""
        self.core.command_mode = not self.core.command_mode
        logger.debug(f"Command mode {'enabled' if self.core.command_mode else 'disabled'}")

    def handle_escape(self) -> None:
        """Handle escape key press."""
        logger.info("Game termination requested")
        self.core.TERMINATE()

    def handle_backspace(self) -> None:
        """Handle backspace key press."""
        if self.core.current_entry_text:
            self.core.current_entry_text = self.core.current_entry_text[:-1]

    def handle_enter(self) -> None:
        """Handle enter key press."""
        self.core.selected_option = 1
        self.execute_selected_option()

    def scroll_options(self, value: int) -> None:
        """Scroll through available options.
        
        Args:
            value: Direction to scroll (1 for up/left, -1 for down/right)
        """
        try:
            selectable_options: list[CustomRenderable] = self.core.console.get_selectable_options()
            options_len: int = len(selectable_options)

            if options_len == 0:
                return

            # Find the currently selected option's index
            current_index = next((i for i, opt in enumerate(selectable_options) if opt.selected), 0)
            
            # Calculate new index with modulo arithmetic for circular behavior
            new_index = (current_index - value) % options_len
            
            # Update selected status for all options
            for i, option in enumerate(selectable_options):
                option.selected = (i == new_index)
            
            # Update the core's selected_option to match
            self.core.selected_option = new_index
            
        except Exception as e:
            logger.error(f"Error scrolling options: {e}")

    def execute_selected_option(self) -> None:
        """Execute the currently selected option."""
        try:
            core: Core = self.core
            for option in core.console.get_selectable_options():
                if option.selected:
                    option.selected = False
                    for option in core.console.get_selectable_options():
                        option.selectable = False
                    if isinstance(option.func, str):
                        self._execute_yaml_function(option)
                    elif callable(option.func):
                        self._execute_callable_function(option)
                    else:
                        self._execute_default_function(option)

                    break
        except Exception as e:
            logger.error(f"Error executing selected option: {e}")

    def _execute_yaml_function(self, option: CustomRenderable) -> None:
        """Execute a YAML function.
        
        Args:
            option: The selected option containing the function
        """
        self.core.next_node = option.next_node
        self.core.execute_yaml_function(option.func)

    def _execute_callable_function(self, option: CustomRenderable) -> None:
        """Execute a callable function.
        
        Args:
            option: The selected option containing the function
        """
        if option.next_node is not None:
            self.core.next_node = option.next_node
        option.func()

    def _execute_default_function(self, option: CustomRenderable) -> None:
        """Execute the default function behavior.
        
        Args:
            option: The selected option
        """
        self.core.chapter_id = (
            option.next_node
            if option.next_node is not None
            else self.core.next_node
        )
        self.core.continue_game()

    def _handle_stats(self) -> None:
        """Handle stats menu display."""
        try:
            self.core.show_stats()
        except Exception as e:
            logger.error(f"Error showing stats: {e}")

    def _handle_settings(self) -> None:
        """Handle settings menu display."""
        try:
            self.core.show_settings()
        except Exception as e:
            logger.error(f"Error showing settings: {e}")