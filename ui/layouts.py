from __future__ import annotations
from enum import Enum
from rich.table import Table
from rich.padding import Padding
from rich.panel import Panel
from rich.align import Align
from rich.rule import Rule
from rich import box
from ui.options import Op
from ui.options import Option, Choices
from rich.layout import Layout
from typing import TYPE_CHECKING, Tuple
if TYPE_CHECKING:
    from core.core import Core
class CustomLayout:
    def initialize(self, core):
        ...
    def update(self):
        ...
class LayoutCharacterSelection(CustomLayout):
    def initialize(self, core: "Core"):
        self.core = core
        core.options = [Choices(ary=[Op() for _ in range(4)], do_build=False)]
        core.options[0].ary[0].selected = True

    def update(self)->Layout:
        table = self.core.console.fill_richTable()
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
    def initialize(self, core : "Core"):
        self.core = core

    def update(self):
        table : Table = self.core.console.fill_richTable()
        content = table
        layout = Layout()   
        layout.split_row(
            Layout(name= "left",ratio= 1,visible=True),
            Layout(name= "middle",ratio= 3),
            Layout(name= "right",ratio= 1,visible=True)
            )
        layout["left"].update(self.core.console.left_tab)
        layout["right"].update(self.core.console.right)
        layout["middle"].update(Panel(content,padding = (0,0)))
        layout.update(content)
        return layout