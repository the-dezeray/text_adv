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


class LayoutLoading(CustomLayout):


    def setup(self ):

        self.core.console.renderables= ["dsiree"]
        from core.timer import Timer
        self.core.timer = Timer(time = 3,func =self.core.from_loading_to_start_menu)
    def update(self):
        from rich.align import Align
        lines = "/////////////////////////////////////////////////////////////"
     
        from rich.console import Group
        panel_group = Group(
        lines,
        f"{self.core.timer.time}",
        )
        ui = Layout(renderable=panel_group)
        return Layout(Padding(renderable=ui,pad = (10,)))
