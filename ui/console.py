"""This module is responsible for rendering the game's UI. It uses the rich library to create a console-based UI."""

from rich.table import Table
from rich.padding import Padding
from rich.panel import Panel
from rich.align import Align
from rich.rule import Rule
from rich.layout import Layout
from ui.options import ui_table
from ui.options import Option,Choices, get_selectable_options
from ui.layouts import LayoutInGame, LayoutDefault, Lsd, LayoutStartMenu, LayoutLoading,LayoutInventory
from rich.console import ConsoleRenderable, group, RichCast

from rich.console import group
from typing import TYPE_CHECKING, Tuple, Optional,Literal
from enum import Enum

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
    def show_weapon(self, weapon: "Weapon"):
        grid = Table.grid(expand=True)
        grid.add_column()
        grid.add_row(Panel(f"[bold green]{weapon.name}[/bold green]"))

        self.right = grid

    def toggle_command_mode(self):
        if self.core.command_mode:
            self.temp_right_tab = self.right
        else:
            self.right = self.temp_right_tab

    def intitialize_normal_mode(self): ...
    def command_mode_layout(self):
        from rich.table import Table

        grid = Table.grid(expand=True)
        grid.add_column()
        stext = "t"
        try:
            stext = self.core.current_entry_text
        except Exception:
            stext = "hehe"
        grid.add_row(
            Panel(
                f"> + {stext}",
                title="input",
                title_align="right",
                border_style="green",
                expand=True,
            )
        )

        hgrid = Table.grid(expand=True)
        hgrid.add_column()
        instructions = "goto \[chapter\] \nreload \nkill \nheal \nrestart"
        grid.add_row(
            Panel(
                instructions,
                title="input",
                title_align="right",
                border_style="yellow",
                expand=True,
            )
        )

        @group()
        def layout():
            yield grid
            yield hgrid

        return layout()

    def initialize_fight_mode(self):
        self.right = self.entity()

    def entity(self):
        """Primary Right Tab"""
        grid = Table.grid()
        grid.add_column()

        return grid

    def s(self):
        grid = Table.grid(expand=True)
        grid.add_column()
        stat_grid = Table.grid(expand=True)

        stat_grid.add_row(
            "[bright_yellow]> vitality[/bright_yellow] [bold yellow1]1[/bold yellow1]"
        )
        stat_grid.add_row(
            "[bright_yellow]> strength[/bright_yellow] [red3]\uf111 \uf111 \uf111 \uf111 \uf111[red3] "
        )
        stat_grid.add_row("[bright_yellow]> speed[/bright_yellow] 2")
        stat_grid.add_row("[bright_yellow]> mana[/bright_yellow] 6")
        stat_grid.add_row("[bright_yellow]> luck[/bright_yellow] 2")
        stat_grid.add_row("[bright_yellow]> exp [/bright_yellow] 232/1000")
        stat_grid.add_row("[bright_yellow]> LEVEL[/bright_yellow] 5")

        def get_vitals():
            """Vitals Panel"""
            c = "green_yellow"
            c2 = "dark_orange3"
            d1 = "bright_cyan"
            ui = f"[{c}]HP ////////////[/{c}][{c2}]//////[/{c2}]  \n[{d1}]MP /////[/{d1}][{c2}]/////[/{c2}] "
            return ui

        grid.add_row(
            Panel(
                renderable=get_vitals(),
                title="Vitals",
                title_align="right",
                border_style="bold light_slate_grey",
            )
        )
        grid.add_row(
            Panel(
                renderable=stat_grid,
                title="Stats",
                title_align="right",
                border_style="bold light_slate_grey",
            )
        )
        # grid.add_row(self.core.job_progress)
        

        from art import text2art
        grid.add_row(
            Panel(
                renderable=f"ARMOR \n [grey]leather jacker[/grey]\n [red1]Hat of death[/red1]\n [red1]bots of truth[/red1] \nWeapons\n sword \n shield \n rusty axe",
                title="[green]inventory[/green]",
                title_align="right",
            )
        )

        @group()
        def get_panels():
            """Instruction Panel"""
            yield "[bright_yellow]Controls[/bright_yellow] Q - [bright_yellow]quit[/bright_yellow]"
            yield "I - [bright_yellow]inventory[/bright_yellow] A - [bright_yellow]stats[/bright_yellow]"
            yield "M - [bright_yellow]menu[/bright_yellow]  S - [bright_yellow]settins[/bright_yellow]"

        instruction_panel = get_panels()
        task_panel = Padding(
            renderable="Taks :\nkill 3 snakes \n Make it alive \n Kill the great snake"
        )
        grid.add_row(task_panel)
        grid.add_row(instruction_panel)
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
        self.core.options.append(Choices(ary=self.core.player.inventory.weapons(),core=self.core))
        return self.fill_ui_table()
    def fill_ui_table(self) -> Table:
        """returns rich table after filling it with options"""
        _core = self.core
        table = ui_table()
        options = _core.options
        from ui.options import Choices

        for option in options:
            if isinstance(option, (Option, Choices)):
                renderable = option.render(core=_core)
                table.add_row(Align(renderable, align=option.h_allign))
            elif isinstance(option, (Padding, Panel)):
                table.add_row(Align(option))

        ary = get_selectable_options(_core.options)
        # if selectable item is selected select the first one
        if ary and all(not i.selected for i in ary):
            ary[0].selected = True
            return self.fill_ui_table()

        return table
    def _transtion_layout(self,layout):
            self.layout = layout
    def show_inventory(self):
        self.layout = "INVENTORY"
        self.options = []
        self.state = "INVENTORY"
    def show_menu(self):
        self.core.options = []
        from art import text2art

        # Define menu options with ASCII text
        menu_items = [
        Option(
            text="Continue",
            func=lambda: self._transtion_layout("INGAME"),
            next_node=None,
            type="menu",
           
        ),
        Option(
            text="New game",
            func=lambda: self._transtion_layout("NEWGAME"),
            next_node=None,
            type="menu"
        ),
        Option(
            text="Settings",
            func=lambda: self._transtion_layout("SETTINGS"),
            next_node=None,
            type="menu"
        ),
        Option(
            text="About us",
            func=lambda:self._transtion_layout("ABOUTUS"),
            next_node=None,
            type="menu"
        ),
        Option(
            text="Leave",
            func=lambda: self.TERMINATE(),
            next_node=None,
            type="menu"
        ),
        ]       
    
        self.core.options.append(Choices(ary=menu_items, menu_type="menu"))
        self.layout = "MENU"
