'''This module contains the Option class and Choices class. The Option class is used to create an option object that can be used in the Choices class. The Choices class is used to create a list of options that can be used in the UI. The WeaponOption function is used to create an option object for weapons. The _dialogue_text function is used to create a text object for the UI.'''

from rich.padding import Padding
from rich.panel import Panel
from rich.table import Table
from rich.align import Align
from rich.console import Group, group
from rich.rule import Rule

class Option():
    def __init__(self, text: str = "", func=None, preview=None, next_node=None, selectable=True, type: str = "", h_allign="center", v_allign="middle") -> None:
        self.text = text
        self.func = func
        self.preview = preview
        self.next_node = next_node
        self.selectable = selectable
        self.selected = False
        self.type = type
        self.v_allign = v_allign
        self.h_allign = v_allign

    def build_renderable(self, style, left_padding) -> Padding:
        option = self
        if option.type == "header":
            return _dialogue_text(option.text, style)
        elif option.type == "entity_profile":
            return get_player_display(option)
        else:
            return _option_button(option.text, style, left_padding=left_padding)

class Choices():
    def __init__(self, ary: list = None, core=None, renderable=None, selectable=True, do_build=True):
        self.ary = ary
        if do_build:
            self.build(core, renderable)

    def build_renderable(option):
        ch = False
        for i in option.ary:
            if i.selected:
                ch = True
        if not ch:
            option.ary[0].selected = True
        renderables = []
        for option in option.ary:
            style = "none"
            left_padding = 0

            if option.selected:
                if option.preview:
                    option.preview()
                style = "bold green"
                left_padding += 5

            renderable = option.build_renderable(style, left_padding)
            renderables.append(renderable)
        grid = get_grid(colomuns=2)
        for i in range(0, len(renderables), 2):
            if i + 1 < len(renderables):
                grid.add_row(
                    Align(renderables[i], align="center"),
                    Align(renderables[i + 1], align="center"),
                )
            else:
                grid.add_row(Align(renderables[i], align="center"))
        return grid

    def build(self, core, renderable):
        from core.events.fight import deal_damage  # don't remove this prevents circular import
        array = []
        from objects.weapon import WeaponItem
        if renderable is not None:
            array.append(renderable)
        elif isinstance(self.ary[0], WeaponItem):
            for weapon in self.ary:
                array.append(WeaponOption(weapon=weapon, func=lambda w=weapon: deal_damage(core, w)))
        elif isinstance(self.ary[0], dict):
            for choice in self.ary:
                array.append(Option(text=choice['text'], func=choice['function'], next_node=choice['next_node'], selectable=True))
        elif isinstance(self.ary[0], (Panel, Padding, Option)):
            for option in self.ary:
                array.append(option)
        self.ary = array

def get_grid(colomuns: int = 1) -> Table:
    grid = Table()
    for _ in range(colomuns):
        grid.add_column()
    return grid

def _dialogue_text(text, style) -> Padding:
    return Padding(Panel(text, border_style=style), pad=(2, 0, 0, 0))

def WeaponOption(weapon, func):
    return Option(text=weapon.name, func=func, selectable=True, type="weapon")

@group()
def get_player_display(option):
    yield _dialogue_text(option.text, "none")
    yield Rule(style="bold red")

def _option_button(text, style, top_padding=0, right_padding=0, bottom_padding=0, left_padding=0) -> Padding:
    return Padding(
        Panel(text, width=15, border_style=style),
        pad=(top_padding, right_padding, bottom_padding, left_padding),
    )

def _display_player_weapons(player):
    pass

def _display_alternative():
    pass

def show_player_actions(player):
    _display_player_weapons(player)
    _display_alternative()

def load_shop():
    pass

class Op:
    def __init__(self):
        self.selected = False
        self.next_node = "1a"
        self.func = "core.clean()"
        self.preview = None
        self.type = None
        self.text = "d"
