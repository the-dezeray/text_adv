"""Handles Keyboard key"""

from __future__ import annotations

from ui.options import Choices
from core.core import Core
from util.logger import logger


def get_selectable_options(options: list):
    for i in reversed(options):
        if isinstance(i, Choices):
            return i.ary


class KeyboardControl:
    def __init__(self, core: Core):
        self.core = core
        self.current_entry_text = ""
        # logger insert here

    def execute_on_key(self, key):
        """
        all keyboard commands must be handled through here
        """

        class MyException(Exception):
            pass

        core = self.core
        from readchar import readkey
        from readchar import key as KEY
      
        key_actions = {
            KEY.BACKSPACE: self.handle_backspace,
            KEY.LEFT : lambda: self.scroll_options(1),
            KEY.RIGHT: lambda: self.scroll_options(-1),
            KEY.UP: lambda: self.scroll_options(1),
            KEY.BACKSPACE: self.handle_backspace,
            KEY.DOWN: lambda: self.scroll_options(-1),
            KEY.ENTER: self.handle_enter,
            "q": self.handle_escape,
            ":": self.handle_command_mode,
        }
        try:
            action = key_actions.get(key, lambda: None)
            action()
        except Exception:
            logger.error(f"Unhandled exception in execute_on_key: {Exception}")
        core.console.refresh()

    def handle_command_mode(self):
        self.core.command_mode = True
        

    def handle_escape(self):
        self.core.TERMINATE()
        # self.core.end_game()

    def handle_tab():
        # TODO handle tab related functions
        ...

    def handle_space(self):
        self.current_entry_text += " "

    def handle_backspace(self):
        self.current_entry_text = self.current_entry_text[:-1]

    def handle_enter(self):
        self.core.selected_option = 1
        self.execute_selected_option()

    def scroll_options(self, value: int):
        selectable_options = get_selectable_options(self.core.options)
        options_len = len(selectable_options)

        if options_len == 0:  # No selectable options; return early.
            return

        # Update selected option using modulo arithmetic for circular behavior.
        self.core.selected_option = (self.core.selected_option - value) % options_len

        # Update the selected status of each option.
        for i, option in enumerate(selectable_options):
            option.selected = i == self.core.selected_option

    def execute_selected_option(self):
        core: Core = self.core

        for option in get_selectable_options(core.options):
            if option.selected == True:
                if isinstance(option.func, str):
                    core.next_node = option.next_node
                    core.execute_yaml_function(option.func)
                elif callable(option.func):
                    if option.next_node is not None:
                        core.next_node = option.next_node
                    option.func()
                else:
                    core.chapter_id = (
                        option.next_node
                        if option.next_node is not None
                        else core.next_node
                    )
                    core.continue_game()
