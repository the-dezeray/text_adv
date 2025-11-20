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


class LayoutAIStudio(CustomLayout):
    def setup(self)  :
        self.core.command_mode = True
        self.core.console.clear_display()
        self.core.ai.setup()
     
    def update(self) -> Layout:
        from  ui.components import input_mode_layout
        layout = Layout()
        
        layout.split_row(
            Layout(name="left", ratio=1, visible=True),
            Layout(name="middle", ratio=3),
            Layout(name="right", ratio=1, visible=True),
        )

        layout["middle"].split_column(
            Layout(name="top", ratio=4),
            Layout(name="bottom", ratio=1),
        )
        layout["left"].update("")
        layout["right"].update("")
        layout["top"].update(self.core.console.fill_ui_table())
        layout["bottom"].update(Align(input_mode_layout(self.core),align="center",vertical="middle"))
        return layout
