"""This module contains the Option class and Choices class. The Option class is used to create an option object that can be used in the Choices class. The Choices class is used to create a list of options that can be used in the UI. The WeaponOption function is used to create an option object for weapons. The ui_text_panel function is used to create a text object for the UI."""

from typing import Callable, Optional, Literal
from rich.padding import Padding
from rich.panel import Panel
from rich.table import Table
from rich.align import Align
from rich.layout import Layout
from rich.console import group
from rich.rule import Rule
from rich.text import Text
from rich import box
from rich.console import ConsoleRenderable
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from core import Core
    from objects.weapon import Weapon


def yy(): ...


class Option:
    def __init__(
        self,
        text: str = "",
        func: Optional[Callable] = None,
        preview: Optional[str] = None,
        next_node: Optional[str] = None,
        selectable: bool = True,
        type: Literal["header", "entity_profile", "note", "choices", "menu"] = "",
        h_allign: str = "center",
        v_allign: str = "middle",
        on_select: Optional[Callable] = lambda: yy(),
    ) -> None:
        self.left_padding = 0
        self.style = ""
        self.core = None
        self.text = text
        self.func = func
        self.preview = preview
        self.next_node = next_node
        self.selectable = selectable
        self.selected = False
        self.type = type
        self.v_allign = v_allign
        self.h_allign = h_allign  # Fixed incorrect assignment from v_allign

    def on_selecta(self):
        self.style = "bold green"
        self.left_padding += 5

    def render(
        self, style: str = "", left_padding: int = 0, core=None
    ) -> Padding | ConsoleRenderable:
        option: Option = self
        option.core = core
        _dict = {
            "header": ui_text_panel,
            "entity_profile": ui_player_display,
            "note": ui_note,
            "menu": ui_menu_btn,
            "default": ui_button,
        }

        if option.type in _dict:
            return _dict[option.type](option)
        else:
            return _dict["default"](option)


class Choices:
    def __init__(
        self,
        ary: list = None,
        core: "Core" = None,
        renderable: Optional[ConsoleRenderable] = None,
        selectable: bool = True,
        do_list_build: bool = True,
        menu_type: Literal["grid", "menu"] = "grid",
    ):
        self.ary = ary
        self.h_allign = "center"
        self.core = core
        self.renderable = renderable
        self.menu_type = menu_type
        if do_list_build:
            self.list_builder()


    def render(self, core=None) -> Padding:
        renderables = []
        for option in self.ary:
            style = "none"
            left_padding = 0

            renderable: Option = option.render(style, left_padding)
            renderables.append(renderable)
        if self.menu_type == "grid":
            grid = ui_grid(colomuns=2)
            for i in range(0, len(renderables), 2):
                if i + 1 < len(renderables):
                    grid.add_row(
                        Align(renderables[i], align="center"),
                        Align(renderables[i + 1], align="center"),
                    )
                else:
                    grid.add_row(Align(renderables[i], align="center"))

            return Padding(grid, pad=(1, 0, 0, 0))
        elif self.menu_type == "menu":
            self.h_allign = "left"
            grid = Table.grid()
            grid.add_column()
            for renderable in renderables:
                grid.add_row(Align(renderable, align="center"))

            return Padding(grid, pad=(1, 0, 0, 0))

    def list_builder(self) -> None:
        from core.events.fight import (
            deal_damage,
        )  # don't remove this prevents circular import

        array = []
        from objects.weapon import WeaponItem

        if self.renderable is not None:
            array.append(self.renderable)
        elif isinstance(self.ary[0], WeaponItem):
            if self.core.console is None:
                raise ValueError(
                    "Core must be set if weapon instance is being called, but got None"
                )
            for weapon in self.ary:
                array.append(
                    WeaponOption(
                        weapon=weapon,
                        func=lambda w=weapon: deal_damage(self.core, w),
                        preview=lambda: self.core.console.show_weapon(weapon),
                    )
                )
        elif isinstance(self.ary[0], dict):
            for choice in self.ary:
                array.append(
                    Option(
                        text=choice["text"],
                        func=choice["function"],
                        next_node=choice["next_node"],
                        selectable=True,
                    )
                )
        elif isinstance(self.ary[0], (Panel, Padding, Option)):
            for option in self.ary:
                array.append(option)

        self.ary = array


def ui_grid(colomuns: int = 1) -> Table:
    grid = Table.grid()
    for _ in range(colomuns):
        grid.add_column()
    return grid


def ui_text_panel(option=None, text="") -> Padding:
    style = ""
    if text == "":
        if option:
            text = option.text
            if option.selected:
                style = "bold green"
                if option.preview:
                    option.preview()
        else:
            raise ValueError("no string provided")
    return Padding(Panel(text, border_style=style), pad=(2, 0, 0, 0))


def WeaponOption(
    weapon: "Weapon", func: str, preview: Optional[callable] = None
) -> Option:
    return Option(
        text=weapon.name, func=func, selectable=True, type="weapon", preview=preview
    )


def ui_menu_btn(
    option,
    text: str,
    style: str,
    selected=True,
    top_padding: int = 0,
    right_padding: int = 0,
    bottom_padding: int = 0,
    left_padding: int = 0,
) -> Padding:
    height = 6
    if left_padding != 0:
        height = 8
    left_padding = 0
    if option.selected:
        style = "bold green"
        left_padding = 8

        if option.preview:
            option.preview()

    return Padding(
        option.text,
        pad=(top_padding, right_padding, bottom_padding, left_padding),
    )


def ui_button(
    option: Option,
    style: str = "",
    selected=False,
    top_padding: int = 0,
    right_padding: int = 0,
    bottom_padding: int = 0,
    left_padding: int = 0,
) -> Padding:
    height = 3
    if left_padding != 0:
        height = 4
    left_padding = 0

    if option.selected:
        style = "bold green"
        left_padding = 5
        if option.preview:
            option.preview()
    return Padding(
        Panel(option.text, width=15, height=height, border_style=style),
        pad=(top_padding, right_padding, bottom_padding, left_padding),
    )


def _display_weapon(weapon: "Weapon"):
    pass


def _display_player_weapons(player):
    pass


def _display_alternative():
    pass


def show_player_actions(player):
    _display_player_weapons(player)
    _display_alternative()


def load_shop():
    pass


def ui_player_display(text):
    return ui_text_panel(text=text)


class Op:
    def __init__(self):
        self.selected: bool = False
        self.next_node: str = "1a"
        self.func: str = "core.clean()"
        self.preview: Layout = None
        self.type: str = None
        self.text: str = "d"


def ui_table() -> Table:
    """This function creates a rich Table object with the specified properties."""
    table: Table = Table(
        expand=True,
        caption=" -",
        show_edge=False,
        show_lines=False,
        show_header=False,
        style="bold red1",
        box=box.ROUNDED,
    )
    table.add_column(justify="center")
    return table


def Loader() -> Padding:
    return Padding(Panel("Loading..."), pad=(2, 4, 0, 4), expand=False)


def ui_note(option) -> Padding:
    text_renderable = Text(option.text, no_wrap=False)
    return Padding(Panel(text_renderable), pad=(2, 4, 0, 4), expand=False)


def Reward(ary: list = []) -> Panel:
    # chances this might not work due to the choices thing
    grid = Table.grid()
    grid.add_column()
    for reward in ary:
        grid.add_row(reward)
    return Panel(grid)


def get_selectable_options(options: list) -> list[Option]:
    array = []
    for i in reversed(options):
        if isinstance(i, (Choices)):
            array.extend(i.ary)
    return array


def shop(): ...


def card(): ...


def sound(): ...


def long_button(): ...


def lister(): ...


def inventory_button(): ...
