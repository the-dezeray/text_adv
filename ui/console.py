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
from ui.components import player_tab
from rich.console import ConsoleRenderable, group, RichCast
from ui.display_queue import DisplayQueue
from rich.console import group
from typing import TYPE_CHECKING, Tuple, Optional, Literal, List
from enum import Enum
from ui.options import Option ,WeaponOption
from ui.components import stats_tab

if TYPE_CHECKING:
    from core.core import Core
    from objects.weapon import Weapon
from ui.layouts import CustomLayout

LAYOUTS: dict [str, type[CustomLayout]] = {
    
    "INGAME": LayoutInGame,
    "SHOP": LayoutDefault,
    "STATS": LayoutDefault,
    "MENU": LayoutStartMenu,
    "INVENTORY": LayoutInventory,
    "SCROLL_READING": LayoutDefault,
    "FIGHT": LayoutDefault,
    "SETTINGS": LayoutDefault,
    "AI_STUDIO": LayoutDefault,
    "ABOUT": LayoutDefault,
    "CHARACTER_SELECTION": Lsd,
    "DEFAULT": LayoutDefault,
    "LOADING": LayoutLoading,
}


class Console:
    def __init__(self, core: "Core"):
        self.core = core
        self.table = None
        self._layout  : CustomLayout = LayoutDefault(core=self.core)
        self.right :Optional[ConsoleRenderable] = None
        self.state: Literal["MAIN", "INVENTORY"] = "MAIN"
        self.left_tab: Optional[ConsoleRenderable] = None
        self.temp_right_tab: Optional[ConsoleRenderable] =None
        self.current_layout : CustomLayout = LayoutDefault(core=self.core)
        self.renderables = DisplayQueue(console=self)
        self.selected_option = 0;
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
        self.core.chapter_id = "0"
        self.core.continue_game()

    def print(self, item) -> None:
        if isinstance(item, list):
            self.renderables.extend(item)
        else:
            self.renderables.append(item)

    @property
    def layout(self) -> CustomLayout:
        return self._layout

    @layout.setter
    def layout(self, value: str):
        _layout  = LAYOUTS.get(value, LayoutDefault)
     
        if _layout is None:
            raise ValueError("Expected a value, but got None")
        else:


            self.current_layout =  _layout(core=self.core)

    def refresh(self) -> None:
        """Refresh the console layout by updating the rich live object with the current layout"""
        _layout: Layout= self.current_layout.update()
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

        # First pass: render all options
        for option in self.renderables:
            if isinstance(option, (CustomRenderable, GridOfChoices, GridOfWeapons)):
                renderable = option.render(core=_core)

                table.add_row(Align(renderable, align=option.h_allign))
            elif isinstance(option, (Padding, Panel)):
                table.add_row(Align(option))
            else:
                from rich.console import RenderableType
                
                table.add_row(option)

        # Second pass: handle selection state
        selectable_options = self.get_selectable_options()
        if selectable_options and not any(opt.selected for opt in selectable_options):
            # Get the last group of selectable options
            last_selectable = self.get_last_selectable()
            if last_selectable:
                index, options = last_selectable
                # Select the first option in the last group
                options[0].selected = True
                self.selected_option = index

        return table

    def get_last_selectable(self) -> Optional[Tuple[int, List[CustomRenderable] | List[Option] | list[WeaponOption]]]:
        """Get the last group of selectable options.
        
        Returns:
            Optional[Tuple[int, List[CustomRenderable]]]: A tuple containing the index and list of options,
            or None if no selectable options are found.
        """
        for i, item in enumerate(reversed(self.renderables)):
            if isinstance(item, (GridOfChoices, GridOfWeapons)):
                return (i, item.ary)
            elif isinstance(item, CustomRenderable) and item.selectable:
                return (i, [item])
        return None

    def _transtion_layout(self, layout):
        self.core.console.clear_display()
        self.layout = layout

    def show_inventory(self):
        self.layout = "INVENTORY"
        self.state = "INVENTORY"

    def show_menu(self):
        self.core.console.clear_display()
        from ui.ad import menu_items

        self.core.console.print(menu_items(self.core))
        self.layout = "MENU"

    def get_selectable_options(self) -> list[CustomRenderable]:
  
        selectable_list :list[CustomRenderable] = []
        # Iterate in reverse to maintain visual order when selecting (usually bottom-up)
        for item in reversed(self.renderables):
            # Check if the item is a buffer containing a list of options (ary)
            if isinstance(item, (GridOfChoices, GridOfWeapons)):
                # Add all options from the buffer's list
                for i in item.ary:
                    if i.selectable:
                        selectable_list.append(i)
                #selectable_list.extend(item.ary)
            # Check if the item itself is a selectable CustomRenderable subclass
            elif isinstance(item, CustomRenderable) and item.selectable:
                selectable_list.append(item)
            # Add checks for other potential container types if needed
        return selectable_list

