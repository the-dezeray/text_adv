"""Handles Keyboard key"""

from __future__ import annotations

from core.core import Core
from util.logger import logger
from ui.options import get_selectable_options
from typing import TYPE_CHECKING

from ui.options import CustomRenderable

if TYPE_CHECKING:
    ...


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
            KEY.LEFT: lambda: self.scroll_options(1),
            KEY.RIGHT: lambda: self.scroll_options(-1),
            KEY.UP: lambda: self.scroll_options(1),
            KEY.BACKSPACE: self.handle_backspace,
            KEY.DOWN: lambda: self.scroll_options(-1),
            KEY.ENTER: self.handle_enter,
            "A": self.core.show_stats,
            "S": self.core.show_settings,
            "M": self.core.console.show_menu,
            "I": self.core.console.show_inventory,
            'q': self.handle_escape,
            ":": self.handle_command_mode,
        }

        if core.command_mode:
            if key == "Q":
                self.handle_escape()
            if key == ":":
                self.handle_command_mode()

            if key == KEY.ENTER:
                core.execute_command(core.current_entry_text)
                core.current_entry_text = ""
            elif key == KEY.BACKSPACE:
                core.current_entry_text = core.current_entry_text[:-1]
            else:
                core.current_entry_text += key

        else:
            action = key_actions.get(key, lambda: None)
            action()

        core.console.refresh()

    def handle_command_mode(self):
        self.core.command_mode = not self.core.command_mode

    def show_stats(self): ...





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
        selectable_options: list["CustomRenderable"] = self.core.console.get_selectable_options()
        options_len: int = len(selectable_options)

        if options_len == 0:  # No selectable options; return early.
            return

        # Update selected option using modulo arithmetic for circular behavior.
        self.core.selected_option = (self.core.selected_option - value) % options_len

        # Update the selected status of each option.
        for i, option in enumerate(selectable_options):
            option.selected = i == self.core.selected_option
        

    def execute_selected_option(self):
        core: Core = self.core

        for option in core.console.get_selectable_options():
            if option.selected == True:
                option.selected = False
                if isinstance(option.func, str):
                    core.next_node = option.next_node
                    core.execute_yaml_function(option.func)
                    option.selectable = False
                elif callable(option.func):
                    if option.next_node is not None:
                        core.next_node = option.next_node
                    option.func()
                    option.selectable = False
                else:
                    core.chapter_id = (
                        option.next_node
                        if option.next_node is not None
                        else core.next_node
                    )
                    option.selectable = False
                    core.continue_game()
         