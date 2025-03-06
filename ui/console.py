"""This module is responsible for rendering the game's UI. It uses the rich library to create a console-based UI."""

from rich.table import Table
from rich.padding import Padding
from rich.panel import Panel
from rich.align import Align
from rich.rule import Rule
from rich.layout import Layout
from ui.options import richTable
from ui.options import Option
from ui.layouts import LayoutInGame, LayoutDefault,Lsd
from rich.console import ConsoleRenderable, Group, RichCast

from typing import TYPE_CHECKING, Tuple, Optional
from enum import Enum

if TYPE_CHECKING:
    from core.core import Core
    
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

def command_mode_layout():
    from rich.table import Table
    grid = Table.grid()
    grid.add_column()
    grid.add_row(Panle("core.command_handler.input"))
    return grid
class Console:
    def __init__(self, core: "Core"):
        self.core = core
        self.table = None
        self._layout = Layout()
        self.right = ""
        self.left_tab :Optional[ConsoleRenderable] = ""
        self.temp_right_tab : Optional[ConsoleRenderable] = None
    def initialize_command_mode(self):
        self.temp_right_tab = self.right
        self.right = command_mode_layout(core = self.core)

    def s(self):
        grid = Table.grid(expand=True)
        grid.add_column()
        stat_grid =  Table.grid(expand=True)
        
        stat_grid.add_row("[bright_yellow]> vitality[/bright_yellow] [bold yellow1]1[/bold yellow1]")
        stat_grid.add_row("[bright_yellow]> strength[/bright_yellow] 2")
        stat_grid.add_row("[bright_yellow]> speed[/bright_yellow] 2")
        stat_grid.add_row("[bright_yellow]> mana[/bright_yellow] 6")
        stat_grid.add_row("[bright_yellow]> luck[/bright_yellow] 2")
        stat_grid.add_row("[bright_yellow]> exp [/bright_yellow] 232/1000")
        stat_grid.add_row("[bright_yellow]> LEVEL[/bright_yellow] 5")
        grid.add_row(Panel(renderable="",title="HP",title_align="right",border_style="bold bright_green"))
        grid.add_row(Panel(renderable=stat_grid,title="Stats",title_align="right",border_style="bold bright_yellow"))
        grid.add_row(self.core.job_progress)
        grid.add_row(Panel(renderable="",title="inventory",title_align="right"))
        grid.add_row(r"""
            .____     _______________   _______________.____       ____ 
            |    |    \_   _____/\   \ /   /\_   _____/|    |     /_   |
            |    |     |    __)_  \   Y   /  |    __)_ |    |      |   |
            |    |___  |        \  \     /   |        \|    |___   |   |
            |_______ \/_______  /   \___/   /_______  /|_______ \  |___|
                    \/        \/                    \/         \/       
        """)
        return grid
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
                renderable = option.build_renderable( style="none", left_padding=0,core = _core)
                table.add_row(Align(renderable, align="center"))
  
            elif isinstance(option,Padding):
                table.add_row(Align(option, align="center"))
            else:
                grid = option.build_renderable()
                table.add_row(Align(grid, align="center"))
        return table
