"""This module is responsible for rendering the game's UI. It uses the rich library to create a console-based UI."""

from rich.table import Table
from rich.padding import Padding
from rich.panel import Panel
from rich.align import Align
from rich import box
from rich.rule import Rule
from rich.layout import Layout
from ui.options import (
    CustomRenderable,
    get_selectable_options,
    GridOfChoices,
    GridOfWeapons,
)
from ui.layouts import (
    LayoutInGame,
    LayoutDefault,
    Lsd,
    LayoutStartMenu,
    LayoutLoading,
    LayoutInventory,
)
from rich.console import ConsoleRenderable, group, RichCast
from ui.display_queue import DisplayQueue
from rich.console import group
from typing import TYPE_CHECKING, Tuple, Optional, Literal, List
from enum import Enum

from ui.components import stats_tab

if TYPE_CHECKING:
    from core.core import Core
    from objects.weapon import Weapon


LAYOUTS = {
    "INGAME": LayoutInGame(),
    "SHOP": Layout(),
    "STATS": Layout(),
    "MENU": LayoutStartMenu(),
    "INVENTORY": LayoutInventory(),
    "SCROLL_READING": Layout(),
    "FIGHT": Layout(),
    "SETTINGS": Layout(),
    "AI_STUDIO": Layout(),
    "ABOUT": Layout(),
    "CHARACTER_SELECTION": Lsd(),
    "DEFAULT": LayoutDefault(),
    "LOADING": LayoutLoading(),
}


class Console:
    def __init__(self, core: "Core"):
        self.core = core
        self.table = None
        self._layout = Layout()
        self.right = ""
        self.state: Literal["MAIN", "INVENTORY"] = "MAIN"
        self.left_tab: Optional[ConsoleRenderable] = ""
        self.temp_right_tab: Optional[ConsoleRenderable] = None
        self.current_layout = LayoutDefault()
        self.current_layout.initialize(core=self.core)
        self.renderables = DisplayQueue(console=self)

    def show_weapon(self):
        from rich_pixels import Pixels

 
        self.right = Panel("ds")

    def toggle_command_mode(self):
        if self.core.command_mode:
            self.temp_right_tab = self.right
        else:
            self.right = self.temp_right_tab

    def intitialize_normal_mode(self): ...

    def initialize_fight_mode(self):
        # self.right = self.enemy_tab()
        ...

    def entity(self):
        """Primary Right Tab"""
        grid = Table.grid()
        grid.add_column()
        grid.add_row("in a fight")

        return grid

    def clear_display(self):
        self.renderables.clear()

    def clean(self):
        self.core.chapter_id = "1a"
        self.core.continue_game()

    def print(self, item: any) -> None:
        if isinstance(item, list):
            for i in item:
                self.renderables.append(i)
        else:
            self.renderables.append(item)

    @property
    def layout(self) -> Layout:
        return self._layout

    @layout.setter
    def layout(self, value: str):
        _layout = LAYOUTS.get(value, None)
        if _layout is None:
            raise ValueError("Expected a value, but got None")
        else:
            _layout.initialize(core=self.core)

            self.current_layout = _layout

    def refresh(self) -> None:
        """Refresh the console layout by updating the rich live object with the current layout"""
        _layout: Layout = self.current_layout.update()
        self.core.rich_live_instance.update(_layout)

    def fill_inventory_table(self) -> Table:
        self.clear_display()
        self.print(Panel("weapons"))
        return self.fill_ui_table()

    def fill_ui_table(self) -> Table:
        """returns rich table after filling it with options"""
        _core = self.core
        table = Table(
            expand=True,
            caption=" - ",  # Default caption
            show_edge=False,
            show_lines=False,
            show_header=False,
            style="bold red1",  # Default style
            box=box.ROUNDED,  # Use rounded box characters
        )
        table.add_column(justify="center")

        from rich.rule import Rule

        for option in self.renderables:
            if isinstance(option, (CustomRenderable, GridOfChoices, GridOfWeapons)):
                renderable = option.render(core=_core)
                table.add_row(Align(renderable, align=option.h_allign))
            elif isinstance(option, (Padding, Panel)):
                table.add_row(Align(option))
            else:
                table.add_row(option)

        ary = _core.console.get_selectable_options()
        # if selectable item is selected select the first one
        if ary and all(not i.selected for i in ary):
            a = self.get_last_selectable()
            
     
            a[0].selected = True
            return self.fill_ui_table()

        return table

    def _transtion_layout(self, layout):
        self.core.console.clear_display()
        self.layout = layout

    def show_inventory(self):
        self.layout = "INVENTORY"
        self.options.clear_display()
        self.state = "INVENTORY"

    def show_menu(self):
        self.core.console.clear_display()
        from ui.ad import menu_items

        self.core.console.print(menu_items(self.core))
        self.layout = "MENU"

    def get_selectable_options(self) -> list[CustomRenderable]:
        selectable_list = []
        # Iterate in reverse to maintain visual order when selecting (usually bottom-up)
        for item in reversed(self.renderables):
            # Check if the item is a buffer containing a list of options (ary)
            if isinstance(item, (GridOfChoices, GridOfWeapons)):
                # Add all options from the buffer's list
                selectable_list.extend(item.ary)
            # Check if the item itself is a selectable CustomRenderable subclass
            elif isinstance(item, CustomRenderable) and item.selectable:
                selectable_list.append(item)
            # Add checks for other potential container types if needed
        return selectable_list
    def get_last_selectable(self) -> list[CustomRenderable]:
        selectable_list = []
        # Iterate in reverse to maintain visual order when selecting (usually bottom-up)
        for item in reversed(self.renderables):
            # Check if the item is a buffer containing a list of options (ary)
            if isinstance(item, (GridOfChoices, GridOfWeapons)):
                # Add all options from the buffer's list
                return item.ary
            # Check if the item itself is a selectable CustomRenderable subclass
            elif isinstance(item, CustomRenderable) and item.selectable:
                return [item]
            # Add checks for other potential container types if needed

