'''Handles Keyboard key'''
from core.fight import fight
from core.entities import Entities

def get_selectable_options(options: list):
    return [option for option in options if option.selectable]

def execute_yaml_function(func: dict, core):
    if isinstance(func, dict):
        target = func.get("target")
        args = func.get("args", "")
        if target:
            exec(f"{target}({args}, core=core)")

class KeyboardControl:
    def __init__(self, core):
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
        core = self.core
        core.selected_option -= value
        selectable_options = get_selectable_options(core.options)
        options_len = len(selectable_options)
        
        if core.selected_option < 0:
            core.selected_option = options_len - 1
        elif core.selected_option >= options_len:
            core.selected_option = 0
        
        for i, option in enumerate(selectable_options):
            option.selected = (i == core.selected_option)

    def execute_selected_option(self):
        from core.core import Core
        core: Core = self.core

        for option in core.options:
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
