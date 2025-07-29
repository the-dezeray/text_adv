from __future__ import annotations
from enum import Enum
from rich.table import Table
from rich.padding import Padding
from rich.panel import Panel
from rich.align import Align
from rich.rule import Rule
from rich import box
from ui.components import player_tab,command_mode_layout
from ui.options import CustomRenderable
from rich.layout import Layout
from typing import TYPE_CHECKING, Tuple
from abc import ABC , abstractmethod 
if TYPE_CHECKING:
    from core.core import Core

from ui.layouts.custom_layout import CustomLayout


class LayoutSelectStory(CustomLayout):
    def __init__(self, core:"Core"):
        self.core = core
        self.layout = Layout()
    
    def setup(self)->None:
  
        self.layout = Layout()
        self.layout.split_row(Layout(name="left"), Layout(visible=False,name="right"))        
    def update(self):
        
        table: Table = self.core.console.fill_ui_table()
        content = table
        


        def top_bar():
            ui = "Home Inventory Settings "
            return ui

 

        ui = self.core.console.fill_ui_table(show_lines=True,show_edge = True)
        self.layout.update(Align(ui,align="center"))

        return self.layout

