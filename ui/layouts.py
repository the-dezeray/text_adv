from __future__ import annotations
from enum import Enum
from rich.table import Table
from rich.padding import Padding
from rich.panel import Panel
from rich.align import Align
from rich.rule import Rule
from rich import box
from ui.components import player_tab,command_mode_layout
from ui.options import Option
from rich.layout import Layout
from typing import TYPE_CHECKING, Tuple

if TYPE_CHECKING:
    from core.core import Core


class CustomLayout:
    def initialize(self, core):
        self.core = core

    def update(self): ...


class LayoutCharacterSelection(CustomLayout):
    def initialize(self, core: "Core"):
        self.core = core
        #core.options = [Choices(ary=[Op() for _ in range(4)], do_build=False)]
        core.options[0].ary[0].selected = True

    def update(self) -> Layout:
        table = self.core.console.fill_ui_table()
        content = Padding(table, pad=(0, 0, 0, 0))
        layout = Layout("des")
        layout.update(content)
        return layout


class LayoutDefault(CustomLayout):
    def initialize(self, core): ...
    def update(self) -> Layout:
        return Layout("des")


class Lsd(CustomLayout):
    def initialize(self, core):
        self.core = core
        # TODO
        # core.options = [Choices(ary=[Op() for _ in range(4)], do_list_build=False)]
        core.options[0].ary[0].selected = True

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


class LayoutInGame(CustomLayout):
    def initialize(self, core: "Core"):
        self.core = core


        self.core.continue_game()
    def update(self):

        layout = Layout()
        layout.split_column(
            Layout(name="up", size=1),
            Layout(name="down"),

        )

        def top_bar():
            ui = "Home Inventory Settings "
            return ui

        layout["up"].update(top_bar())
        layout["down"].split_row(
            Layout(name="left", ratio=1, visible=True),
            Layout(name="middle", ratio=3),
            Layout(name="right", ratio=1, visible=True),
        )

        if self.core.command_mode:
            self.core.console.right = command_mode_layout(self.core)
        layout["left"].update(player_tab(self.core))
        #layout["right"].update(self.core.console.right)
        table = None
        if self.core.console.state == "MAIN":
            table: Table = self.core.console.fill_ui_table()
            
        elif self.core.console.state == "INVENTORY":
            table = self.core.console.fill_inventory_table()
        content = table
        layout["middle"].update(
            Panel(
                content,
                padding=(0, 0),
                title="A fallen room",
                title_align="right",
                box=box.ROUNDED,
                subtitle=": [red1]5%[/red1]",
                subtitle_align="right",
                style="",
                border_style="bold light_slate_grey",
            )
        )

        return layout


class LayoutInventory(CustomLayout):
    def initialize(self, core: "Core"):
        self.core = core


class LayoutSettings(CustomLayout):
    def initialize(self, core: "Core"):
        self.core = core


class LayoutPreGame(CustomLayout):
    def initialize(self, core: "Core"):
        self.core = core


class LayoutStartMenu(CustomLayout):
    def initialize(self, core: "Core"):
        self.core = core

    def update(self):
        table: Table = self.core.console.fill_ui_table()
        content = table
        layout = Layout()
        layout.split_column(Layout(name="up", size=1), Layout(name="down"))

        def top_bar():
            ui = "Home Inventory Settings "
            return ui

        layout["up"].update(top_bar())
        layout["down"].split_row(
            Layout(name="menus", ratio=3),
        )


        ui = self.core.console.fill_ui_table()
        layout["menus"].update(Panel(ui))

        return layout


class LayoutLoading(CustomLayout):
    def initialize(self, core: "Core"):
        self.core = core
        self.core.options = ["dsiree"]
        from core.timer import Timer
        self.core.timer = Timer(time = 3,func =core.from_loading_to_start_menu)
    def update(self):
        from rich.align import Align
        lines = "/////////////////////////////////////////////////////////////"
     
        from rich.console import Group
        panel_group = Group(
        lines,
        f"{self.core.timer.time}",
        )
        ui = Layout(renderable=panel_group)
        return Padding(renderable=ui,pad = (10,))
class LayoutInventory(CustomLayout):
    def initialize(self, core: "Core"):
        self.core = core

    def update(self):
        

        layout = Layout()

        #ui = self.core.console.fill_ui_table()
        #weapons = Choices()
        renderable = self.core.console.fill_inventory_table()
        layout.update(Align(Panel(renderable=renderable,height=32,width=100),align="center"))

        return layout

