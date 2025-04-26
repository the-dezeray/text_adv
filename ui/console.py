"""This module is responsible for rendering the game's UI. It uses the rich library to create a console-based UI."""

from rich.table import Table
from rich.padding import Padding
from rich.panel import Panel
from rich.align import Align
from rich.rule import Rule
from rich.layout import Layout
from ui.options import ui_table
from ui.options import Option, get_selectable_options,buffer_display_choices,buffer_create_weapons
from ui.layouts import LayoutInGame, LayoutDefault, Lsd, LayoutStartMenu, LayoutLoading,LayoutInventory
from rich.console import ConsoleRenderable, group, RichCast

from rich.console import group
from typing import TYPE_CHECKING, Tuple, Optional,Literal,List
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
        self.state:Literal["MAIN","INVENTORY"] = "MAIN"
        self.left_tab: Optional[ConsoleRenderable] = ""
        self.temp_right_tab: Optional[ConsoleRenderable] = None
        self.current_layout = LayoutDefault()
        self.current_layout.initialize(core=self.core)

    def show_weapon(self):
        from rich_pixels import Pixels
        pixels = Pixels.from_image_path("icon1.png",)
        self.right=  Panel('ds')       

    def toggle_command_mode(self):
        if self.core.command_mode:
            self.temp_right_tab = self.right
        else:
            self.right = self.temp_right_tab

    def intitialize_normal_mode(self): ...

    def initialize_fight_mode(self):
        #self.right = self.enemy_tab()
        ...

    def entity(self):
        """Primary Right Tab"""
        grid = Table.grid()
        grid.add_column()
        grid.add_row("in a fight")

        return grid



    def clean(self):
        self.core.chapter_id = "1a"
        self.core.continue_game()

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
    def fill_inventory_table(self)->Table:
        self.core.options = []
        self.core.options.append(Panel("weapons"))
        #self.core.options.append(Choices(ary=self.core.player.inventory.weapons(),core=self.core))
        return self.fill_ui_table()
    def fill_ui_table(self) -> Table:
        """returns rich table after filling it with options"""
        _core = self.core
        table = ui_table()
        options = _core.options
      
        from rich.rule import Rule
        
        for option in options:
            if isinstance(option, (Option, buffer_display_choices,buffer_create_weapons)):
                renderable = option.render(core=_core)
                table.add_row(Align(renderable, align=option.h_allign))
            elif isinstance(option, (Padding, Panel)):
                table.add_row(Align(option))
            else:
                table.add_row(option)

        ary = get_selectable_options(_core.options)
        # if selectable item is selected select the first one
        if ary and all(not i.selected for i in ary):
            _core.selected_option = 0
            ary[0].selected = True
            return self.fill_ui_table() 

        return table
    def _transtion_layout(self,layout):
            self.core.options = []
            self.layout = layout
           
    def show_inventory(self):
        self.layout = "INVENTORY"
        self.options = []
        self.state = "INVENTORY"
    def show_menu(self):
        self.core.options = []
        from ui.ad import menu_items
        self.core.options.extend(menu_items(self.core))
        self.layout = "MENU"
