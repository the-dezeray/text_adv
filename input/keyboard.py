'''Handles Keyboard key'''
from __future__ import annotations

from ui.options import Choices, Option
from core.core import Core

#this are referenced in the exec function
from core.fight import fight
from core.entities import Entities
from ui.console import Op
def get_selectable_options(options: list):

        for i in options:
            if isinstance(i, Choices):
                return i.ary

def execute_yaml_function(func: dict, core):
    if isinstance(func, dict):
        target = func.get("target")
        args = func.get("args", "")
        if target:
            exec(f"{target}({args}, core=core)")

class KeyboardControl:
    def __init__(self, core : Core):
        self.core = core

        self.current_entry_text = ""


    def execute_on_key(self, key):
        core = self.core
        input_string = str(key).replace("'", "")
        
        key_actions = {
            "Key.space": self.handle_space,
            "Key.backspace": self.handle_backspace,
            "Key.up": lambda: self.scroll_options(1),
            "Key.down": lambda: self.scroll_options(-1),
            "Key.enter": self.handle_enter
        }
        
        action = key_actions.get(input_string, lambda: None)
        action()
        core.console.refresh()

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
            option.selected = (i == self.core.selected_option)


    def execute_selected_option(self):
        
        core: Core = self.core

        for option in get_selectable_options(core.options):
            if option.selected:
                if isinstance(option.func, str):
                    core.next_node = option.next_node
                    core.execute_yaml_function(option.func)
                elif callable(option.func):
                    if option.next_node is not None:
                        core.next_node = option.next_node
                    option.func()
                else:
                    core.chapter_id = option.next_node if option.next_node is not None else core.next_node
                    core.continue_game()
