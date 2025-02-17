"""This module is responsible for rendering the game's UI. It uses the rich library to create a console-based UI."""

from __future__ import annotations
from enum import Enum
from rich.table import Table
from rich.padding import Padding
from rich.panel import Panel
from rich.align import Align
from rich.rule import Rule
from rich import box
from rich.console import Group, group
from rich.spinner import Spinner
from ui.options import Option, Choices
from rich.layout import Layout
from typing import TYPE_CHECKING, Tuple


class Op:
    def __init__(self):
        self.selected = False
        self.next_node = "1a"
        self.func = "core.clean()"
        self.preview = None
        self.type = None
        self.text = "d"


def get_grid(colomuns: int = 1) -> Table:
    grid = Table.grid()
    for _ in range(colomuns):
        grid.add_column()
    return grid


class LayoutCharacterSelection:
    def initialize(self, core):
        self.core = core
        core.options = [Choices(ary=[Op() for _ in range(4)], do_build=False)]
        core.options[0].ary[0].selected = True

    def update(self):
        table = self.core.console.build_table()
        content = Padding(table, pad=(0, 0, 0, 0))
        layout = Layout("des")
        layout.update(content)
        return layout


class LayoutDefault:
    def initialize(self, core): ...
    def update(self):
        return Layout("des")


class Lsd:
    def initialize(self, core):
        self.core = core
        core.options = [Choices(ary=[Op() for _ in range(4)], do_build=False)]
        core.options[0].ary[0].selected = True

    def update(self):
        layout = Layout()
        layout.split(Layout(name="View", ratio=10), Layout(name="control"))
        layout["View"].split_row(Layout(name="Picture"), Layout(name="Stats"))

        grid = [Panel("") for _ in range(4)]
        grid[self.core.selected_option] = Panel(
            renderable="", style="bold red", height=2, width=7
        )

        from rich.columns import Columns

        layout["control"].update(Columns(renderables=grid, align="center"))
        return layout


class LayoutInGame:
    def initialize(self, core):
        self.core = core

    def update(self):
        table = self.core.console.build_table()
        content = table
        layout = Layout()   
        layout.split_row(
            Layout(name= "left",ratio= 1,visible=True),
            Layout(name= "middle",ratio= 3),
            Layout(name= "right",ratio= 1,visible=True)
            )
        layout["left"].update("")
        layout["right"].update("")
        layout["middle"].update(Panel(content,padding = (0,0)))
        layout.update(content)
        return layout


LAYOUTS = {
    "INGAME": LayoutInGame(),
    "SHOP": Layout(),
    "STATS": Layout(),
    "INVENTORY": Layout(),
    "SCROLL_READING": Layout(),
    "FIGHT": Layout(),
    "SETTINGS": Layout(),
    "AI_STUDIO": Layout(),
    "ABOUT": Layout(),
    "CHARACTER_SELECTION": Lsd(),
    "DEFAULT": LayoutDefault(),
}


class Console:
    def __init__(self, core):
        self.core = core

        self.table = None

        self._layout = Layout()

    def clean(self):
        self.core.chapter_id = "1a"
        self.core.continue_game()

    def show_error():
        pass

    @property
    def layout(self):
        return self._layout

    @layout.setter
    def layout(self, value: str):
        lay = LAYOUTS.get(value, LAYOUTS["DEFAULT"])

        if lay == None:
            print("layout is not defined")

        else:
            lay.initialize(core=self.core)
            self.current_layout = lay

    def refresh(self):
        layout = self.current_layout.update()
        self.core.love.update(layout)
        """
        layout = Layout()
        layout.split(Layout(name="View",ratio=10),Layout(name="control"))
        layout["View"].split_row(Layout(name="Picture"),Layout(name="Stats"))
        
        grid = [Panel("") for _ in range(4)]
        grid[self.core.selected_option] = Panel(renderable="",style="bold red",height=2,width=7)
        
        from rich.columns import Columns
        layout["control"].update(Columns( renderables=grid,align="center"))
        self.core.love.update(layout)"""

    def build_table(self) -> Table:
        core = self.core
        table = Table(
            
            expand=True,
            caption=" -",
            show_edge=False,
            show_header=False,
            style="bold red1",
            box=box.ROUNDED,
        )
        table.add_column(justify="center")
        options = core.options

        for option in options:
            if not isinstance(option, Choices):
                renderable = self.get_renderable(option, style="none", left_padding=0)
                table.add_row(Align(renderable, align="center"))
            else:
                ch = False
                for i in option.ary:
                    if i.selected:
                        ch = True
                if ch is False:
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

                    renderable = self.get_renderable(option, style, left_padding)
                    renderables.append(renderable)
                for i in range(0, len(renderables), 2):
                    grid = get_grid(colomuns=2)

                    # Check if there's a "next" item in the list
                    if i + 1 < len(renderables):
                        grid.add_row(
                            Align(renderables[i], align="center"),
                            Align(renderables[i + 1], align="center"),
                        )
                    else:
                        # Handle the case where there's only one item left
                        grid.add_row(Align(renderables[i], align="center"))

                    table.add_row(Align(grid, align="center"))
        return table

    def get_renderable(self, option, style, left_padding) -> Padding:
        if option.type == "header":
            return _dialogue_text(option.text, style)
        elif option.type == "entity_profile":
            return get_player_display(option)
        else:
            return _option_button(option.text, style, left_padding=left_padding)


@group()
def get_player_display(option):
    yield _dialogue_text(option.text, "none")
    yield Rule(style="bold red")


def _dialogue_text(text, style) -> Padding:
    return Padding(Panel(text,border_style=style), pad=(2, 0, 0, 0))


def _option_button(
    text, style, top_padding=0, right_padding=0, bottom_padding=0, left_padding=0
) -> Padding:
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


def load_shop(): ...

