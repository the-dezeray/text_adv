

from __future__ import annotations

"""Handles keyboard input and control for the game."""

from util.logger import logger
from ui.options import get_selectable_options, CustomRenderable
from typing import TYPE_CHECKING, Dict, Callable, Optional, Any
from readchar import readkey
from readchar import key as KEY
from ui.ad import  generate_main_menu_options
if TYPE_CHECKING:
    from core.core import Core


class KeyboardControl:
    """Handles all keyboard input and control for the game.
    
    This class manages keyboard input, command mode, and option selection.
    It provides a centralized way to handle all keyboard interactions.
    """
    
    def __init__(self, core:"Core"):
        """Initialize the keyboard controller.
        
        Args:
            core: The game's core instance
        """
        self.core = core
        self.current_entry_text = ""
        self._setup_key_actions()
        self.nkey = ""
        self.refresh_on_key = False
        logger.info("Keyboard controller initialized")
        self.setting_key_type: Optional[str] = None  # Type of key being set, if any
    def _setup_key_actions(self) -> None:
        """Setup the key action mappings."""
        config = self.core.config["keymaps"]
        reach_key = {
            "up": KEY.UP,
            "down": KEY.DOWN,
            "left": KEY.LEFT,
            "right": KEY.RIGHT,
            "enter": KEY.ENTER,
            "backspace": KEY.BACKSPACE,
            
                    }
        for key, value in config.items():
            value =reach_key.get(value, None)
            if value is not None:
                config[key] = value
            
        if config is None:
            logger.error("Configuration not found, using default key mappings")
            config =None 
            KEY.BACKSPACE
        self.key_actions: Dict[str, Callable] = config
        self.function_map: Dict[str, Callable] = {
            "backspace": self.handle_backspace,
            "move_left": lambda: self.scroll_options(1),
            "move_right": lambda: self.scroll_options(-1),
            "move_up": lambda: self.scroll_options(1),
            "move_down": lambda: self.scroll_options(-1),
            "enter": self.handle_enter,
            "help": self.core.console.show_help,
            "log": self.core.console.show_log,
            "restart_app": self.core.restart_app,
            "reload_files": self.core.reload_files,
            "keybindings": self.show_keybindings,
            "stats": self._handle_stats,
            "show_settings": self._handle_settings,
            "menu": lambda:  generate_main_menu_options(self.core),
            "show_inventory": self.core.console.show_inventory,
            'quit': self.handle_escape,
            "command_mode": self.handle_command_mode,
            "go_back": self.core.console.back
        }

    def show_keybindings(self):
        from ui.ad import generate_keybindings_menu_options
        console = self.core.console
        console._transtion_layout("MENU")
        generate_keybindings_menu_options(self.core)


    def execute_on_key(self, key: str) -> None:
        """Execute the appropriate action for the given key.
        
        Args:
            key: The key that was pressed
        """
        logger.debug(f"Key pressed: {key}")
        try: 
            if key != KEY.ESC and key != KEY.ENTER:
                self.nkey = key
            if self.refresh_on_key:
                if key == KEY.ESC:
                    self.refresh_on_key = False 
                    self.core.console.back()
                if  key==KEY.ENTER :
                    self.refresh_on_key = False
                    self.core.config["keymaps"][self.setting_key_type] = self.nkey

                    self.core.console.refresh()
                    self.core.console.back()
                self.core.console.refresh()
            else:
                if self.core.command_mode:
                    self._handle_command_mode_input(key)
                else:
                    def get_key_by_value(d: dict, value):
                        for key, val in d.items():
                            if val == value:
                                return key
                        return None  # or raise an error if not found
                    function_id = get_key_by_value(self.key_actions, key)
                    logger.debug(f"Function ID for key '{key}': {function_id}")
                    action: Callable|None = self.function_map.get(function_id,None)
                    if action:
                        logger.debug(f"Executing action for key '{key}': {action}")
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
        if key == "q":
            self.handle_escape()
        elif key == ":":
            self.handle_command_mode()
        elif key == KEY.ENTER:
            if not self.core.ai_studio:
                self._execute_command()
            else:
                self.core.ai.prompt(self.core.current_entry_text)
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
            selectable_options = core.console.get_selectable_options()
            
            # Find the selected option
            selected_option = next((opt for opt in selectable_options if opt.selected), None)
            
            if selected_option:
                # Clear selection state
                selected_option.selected = False
                # Disable all other selectable options
                if hasattr(selected_option, 'disable_others') and selected_option.disable_others:
                    for option in selectable_options:
                        option.selectable = False
                
                # Execute the appropriate function based on type
                if isinstance(selected_option.func, str):
                    self._execute_yaml_function(selected_option)
                elif callable(selected_option.func):
                    self._execute_callable_function(selected_option)
                else:
                    self._execute_default_function(selected_option)
                    
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