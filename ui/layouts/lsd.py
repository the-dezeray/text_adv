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


class Lsd(CustomLayout):
    def setup(self):
        self.core.console.renderables[0].ary[0].selected = True

    def update(self) -> Layout:
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

