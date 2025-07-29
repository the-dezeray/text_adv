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


class LayoutCharacterSelection(CustomLayout):
    def setup(self):
        self.core.console.renderables[0].ary[0].selected = True

    def update(self) -> Layout:
        table = self.core.console.fill_ui_table()
        content = Padding(table, pad=(0, 0, 0, 0))
        layout = Layout("des")
        layout.update(content)
        return layout

