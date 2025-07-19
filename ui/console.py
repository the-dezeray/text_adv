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
    GridOfWeaponsShop,
    TyperWritter,
    Delay,
)
from ui.layouts import (
    LayoutInGame,
    LayoutDefault,
    Lsd,
    LayoutStartMenu,
    LayoutLoading,
    LayoutInventory,
    LayoutSelectStory,
    LayoutAIStudio,
    LayoutAboutUs
)
from ui.components import player_tab
from rich.console import ConsoleRenderable, group, RichCast
from ui.display_queue import DisplayQueue
from rich.console import group
from typing import TYPE_CHECKING, Tuple, Optional, Literal, List
from enum import Enum
from ui.options import Option ,WeaponOption
from ui.components import stats_tab
import time
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
 
    "ABOUT_US": LayoutAboutUs,
    "CHARACTER_SELECTION": Lsd,
    "DEFAULT": LayoutDefault,
    "LOADING": LayoutLoading,
    "SELECTSTORY": LayoutSelectStory,
    "AI_STUDIO": LayoutAIStudio,
}
class DummyTable(Table):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.border_style = None
        self.caption = None
        self.title = None
        self.style = None
        self.show_edge = None
        self.show_lines = None
        self.show_header = None
        self.expand = None

class Console:
    def __init__(self, core: "Core"):
        self.core = core
        self.table_count = 0
        self.table: DummyTable = DummyTable()
        self._layout  : CustomLayout = LayoutDefault(core=self.core)
        self.right :Optional[ConsoleRenderable] = ""
        self.state: Literal["MAIN", "INVENTORY"] = "MAIN"
        self.left_tab: Optional[ConsoleRenderable] = None
        self.temp_right_tab: Optional[ConsoleRenderable] =None
        self.current_layout : CustomLayout = LayoutDefault(core=self.core)
        self.renderables = DisplayQueue(console=self)
        self.selected_option = 0
        self.left_ratio =1
        self.right_ratio = 1
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
        
        if self.table_count >5:
            self.renderables._data = self.renderables._data[-9:]

  
        self.refresh()
    @property
    def layout(self) -> CustomLayout:
        return self._layout

    @layout.setter
    def layout(self, value: str)->None:
        _layout:type[CustomLayout]  = LAYOUTS.get(value, LayoutDefault)
     
        if _layout is None:
            raise ValueError("Expected a value, but got None")
        else:


            self.current_layout =  _layout(core=self.core)

    def refresh(self) -> None:
        """Refresh the console layout by updating the rich live object with the current layout"""
        _layout: Layout = self.current_layout.update()
        self.core.rich_live_instance.update(_layout)

    def fill_inventory_table(self) -> Table:
        self.clear_display()
        self.print(Panel("weapons"))
        
        return self.fill_ui_table()

    def fill_ui_table(self,expand:bool = True,title:str = "",caption:str = " - ",border_style:str = "",show_edge:bool = False,show_lines:bool = False,show_header:bool = False,style:str = "",box:box.Box = box.ROUNDED) -> Table:
        """returns rich table after filling it with options"""
        border_style = border_style if not self.table.border_style else self.table.border_style
        caption = caption if not self.table.caption else self.table.caption
        title = title if not self.table.title else self.table.title
        style = style if not self.table.style else self.table.style
        box = box if not self.table.box else self.table.box
        show_edge = show_edge if not self.table.show_edge else self.table.show_edge
        show_lines = show_lines if not self.table.show_lines else self.table.show_lines
        show_header = show_header if not self.table.show_header else self.table.show_header
        expand = expand if not self.table.expand else self.table.expand
        _core = self.core
        table = Table(
            expand=expand,
            
            border_style=border_style,
            caption=caption,  # Default caption
            show_edge=show_edge,
            show_lines=show_lines,
            title = title,

            show_header=show_header,
            style=style,  # Default style
            box=box  # Use rounded box characters
        )
        table.add_column(justify="center")

        # Update typing animations and delays first
        any_typing = False
        any_delaying = False
        for option in self.renderables:
            if isinstance(option, TyperWritter):
                if option.update():  # Update the typing animation
                    any_typing = True
                    _core.is_typing = True
                    break
            elif isinstance(option, Delay):
                if option.update():  # Update the delay
                    any_delaying = True
                    _core.is_typing = True
                    break
        # First pass: render all options
        for option in self.renderables:

            if isinstance(option, (CustomRenderable, GridOfChoices, GridOfWeapons,GridOfWeaponsShop)):
                renderable = option.render(core=_core)

                table.add_row(Align(renderable, align=option.h_allign))
            elif isinstance(option,TyperWritter):
                if option.is_typing:
                    table.add_row(Align(option.typed))
                else:
                    table.add_row(Align(option.text))
            elif isinstance(option, Delay):
                if option.is_delaying:
                    
                    return table
                else:
                    # Delay is complete, don't add anything
                    pass

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
        self.table_count = table.row_count
        
        # If no typing or delaying is happening, clear the typing flag
        if not any_typing and not any_delaying:
            _core.is_typing = False
            
        return table

    def get_last_selectable(self) -> Optional[Tuple[int, List[CustomRenderable] | List[Option] | list[WeaponOption]]]:
        """Get the last group of selectable options.
        
        Returns:
            Optional[Tuple[int, List[CustomRenderable]]]: A tuple containing the index and list of options,
            or None if no selectable options are found.
        """
        for i, item in enumerate(reversed(self.renderables)):
            if isinstance(item, (GridOfChoices, GridOfWeapons,GridOfWeaponsShop)):
                return (i, item.ary)
            elif isinstance(item, CustomRenderable) and item.selectable:
                return (i, [item])
        return None
    layout_list =Literal["MENU","ABOUT_US","AI_STUDIO","INGAME","SHOP","STATS","INVENTORY","SCROLL_READING","FIGHT","SETTINGS","AI_STUDY","ABOUT","CHARACTER_SELECTION","DEFAULT","LOADING","SELECTSTORY"]
    def _transtion_layout(self, layout:layout_list):
        self.core.console.clear_display()
        self.layout = layout
    def show_help(self):
        self.core.console.clear_display()
        
        # TODO: Implement proper back navigation must be implemented
        self.core.current_pane = lambda: self.core.console.show_menu()

        from ui.ad import generate_main_menu_options
        from ui.options import MinimalMenuOption
        menu: List[MinimalMenuOption] = generate_main_menu_options(self.core)
        self.core.console._transtion_layout("INVENTORY")
        
        self.core.console.print(menu)
        self.layout = "INVENTORY"
    def show_log(self):
        self.core.console.clear_display()
        
        # TODO: Implement proper back navigation must be implemented
        self.core.current_pane = lambda: self.core.console.show_menu()

        from ui.ad import generate_main_menu_options
        from ui.options import MinimalMenuOption
        menu: List[MinimalMenuOption] = generate_main_menu_options(self.core)
        self.core.console._transtion_layout("INVENTORY")
        
        self.core.console.print(menu)
        self.layout = "INVENTORY"

    def show_inventory(self):
        self.core.console.clear_display()
        
        # TODO: Implement proper back navigation must be implemented
        self.core.current_pane = lambda: self.core.console.show_menu()

        from ui.ad import generate_main_menu_options
        from ui.options import MinimalMenuOption
        menu: List[MinimalMenuOption] = generate_main_menu_options(self.core)
        self.core.console._transtion_layout("INVENTORY")
        
        self.core.console.print(menu)
        self.layout = "INVENTORY"

    def show_menu(self):
        self.core.console.clear_display()

        # TODO: Implement proper back navigation must be implemented
        self.core.current_pane = lambda: self.core.console.show_menu()

        from ui.ad import generate_main_menu_options
        from ui.options import MinimalMenuOption
        menu: List[MinimalMenuOption] = generate_main_menu_options(self.core)
        self.core.console._transtion_layout("MENU")
        
        self.core.console.print(menu)
        self.layout = "MENU"

    def get_selectable_options(self) -> list[CustomRenderable]:
  
        selectable_list :list[CustomRenderable] = []
        # Iterate in reverse to maintain visual order when selecting (usually bottom-up)
        for item in self.renderables:
            # Check if the item is a buffer containing a list of options (ary)
            if isinstance(item, (GridOfChoices, GridOfWeapons,GridOfWeaponsShop)):
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

