"""This module is responsible for rendering the game's UI. It uses the rich library to create a console-based UI."""


from rich.table import Table
from rich.padding import Padding
from rich.panel import Panel
from rich.align import Align
from rich.rule import Rule

from rich.layout import Layout

from ui.options import Op
from ui.options import richTable
from ui.options import Option
from ui.layouts import LayoutInGame, LayoutDefault,Lsd

from typing import TYPE_CHECKING, Tuple

from enum import Enum


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

    @property
    def layout(self)->Layout:
        return self._layout
    @layout.setter
    def layout(self, value: str):
    
        _layout = LAYOUTS.get(value,None)
        if _layout is None:
            raise ValueError("Expected a value, but got None")
        else:
            _layout.initialize(core=self.core)
            self.current_layout = _layout

    def refresh(self)->None:
        '''Refresh the console layout by updating the rich live object with the current layout'''
        _layout : Layout = self.current_layout.update()
        self.core.rich_live_instance.update(_layout)

    def fill_richTable(self) -> Table:
        '''returns rich table after filling it with options'''
        _core = self.core
        table = richTable()
        options = _core.options
        
        for option in options:
            if  isinstance(option, Option):
                renderable = option.build_renderable( style="none", left_padding=0)
                table.add_row(Align(renderable, align="center"))
            elif isinstance(option,Padding):
                table.add_row(Align(option, align="center"))
            else:
                grid = option.build_renderable()
                table.add_row(Align(grid, align="center"))
        return table
