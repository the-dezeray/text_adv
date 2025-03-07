'''This module contains the Option class and Choices class. The Option class is used to create an option object that can be used in the Choices class. The Choices class is used to create a list of options that can be used in the UI. The WeaponOption function is used to create an option object for weapons. The _dialogue_text function is used to create a text object for the UI.'''
from typing import Callable, Optional ,Literal
from rich.padding import Padding
from rich.panel import Panel
from rich.table import Table
from rich.align import Align
from rich.layout import Layout
from rich.console import  group
from rich.rule import Rule
from rich.text import Text 
from rich import box
from rich.console import ConsoleRenderable
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING :
    from core import Core
    from objects.weapon import Weapon
class Option:
    def __init__(
        self, 
        text: str = "", 
        func: Optional[Callable] = None, 
        preview: Optional[str] = None, 
        next_node: Optional[str] = None, 
        selectable: bool = True, 
        type: Literal ["header","entity_profile","note"] = "", 
        h_allign: str = "center", 
        v_allign: str = "middle"
    ) -> None:
        self.text = text
        self.func = func
        self.preview = preview
        self.next_node = next_node
        self.selectable = selectable
        self.selected = False
        self.type = type
        self.v_allign= v_allign
        self.h_allign = h_allign  # Fixed incorrect assignment from v_allign


    def build_renderable(self, style: str= "", left_padding: int= 0,core = None) -> Padding | ConsoleRenderable:
        option : Option = self
        
        if option.type == "header":
            return _dialogue_text(option.text, style)
        elif option.type == "entity_profile":
            return get_player_display(option)
        elif option.type == "note":
            return richNote(option.text,core)
        else:
            return _option_button(option.text, style, left_padding=left_padding, )

class Choices():
    def __init__(self, ary: list = None, core: "Core"=None, renderable: Optional[ConsoleRenderable] =None, selectable : bool =True, do_build:bool=True):
        self.ary = ary
        if do_build:
            self.build(core, renderable)

    def build_renderable(option:Option)->Padding:

        renderables = []
        for option in option.ary:
            style = "none"
            left_padding = 0

            if option.selected:
                if option.preview:
                    option.preview()
                style = "bold green"
                left_padding += 5

            renderable = option.build_renderable(style, left_padding)
            renderables.append(renderable)
        grid = get_grid(colomuns=2)
        for i in range(0, len(renderables), 2):
            if i + 1 < len(renderables):
                grid.add_row(
                    Align(renderables[i], align="center"),
                    Align(renderables[i + 1], align="center"),
                )
            else:
                grid.add_row(Align(renderables[i], align="center"))
        return Padding(grid,pad=(1,0,0,0))

    def build(self, core: "Core", renderable: ConsoleRenderable )->None:
        from core.events.fight import deal_damage  # don't remove this prevents circular import
        array = []
        from objects.weapon import WeaponItem
        if renderable is not None:
            array.append(renderable)
        elif isinstance(self.ary[0], WeaponItem):
            for weapon in self.ary:
                array.append(WeaponOption(weapon=weapon, func=lambda w=weapon: deal_damage(core, w)))
        elif isinstance(self.ary[0], dict):
            for choice in self.ary:
                array.append(Option(text=choice['text'], func=choice['function'], next_node=choice['next_node'], selectable=True))
        elif isinstance(self.ary[0], (Panel, Padding, Option)):
            for option in self.ary:
                array.append(option)
        self.ary = array

def get_grid(colomuns: int = 1) -> Table:
    grid = Table.grid()
    for _ in range(colomuns):
        grid.add_column()
    return grid

def _dialogue_text(text:str, style:str) -> Padding:
    return Padding(Panel(text, border_style=style), pad=(2, 0, 0, 0))

def WeaponOption(weapon : "Weapon", func:str):
    return Option(text=weapon.name, func=func, selectable=True, type="weapon")

@group()
def get_player_display(option: Option):
    yield _dialogue_text(option.text, "none")
    yield Rule(style="bold red")

def _option_button(text :str, style: str, top_padding:int=0, right_padding:int =0, bottom_padding:int =0, left_padding:int =0) -> Padding:
    height = 3
    if left_padding !=0 :
        height = 4 
    left_padding = 0

    return Padding(
        Panel(text, width=15,height=height , border_style=style),
        pad=(top_padding, right_padding, bottom_padding, left_padding),
    )

def _display_player_weapons(player):
    pass

def _display_alternative():
    pass

def show_player_actions(player):
    _display_player_weapons(player)
    _display_alternative()

def load_shop():
    pass

class Op:
    def __init__(self):
        self.selected : bool= False
        self.next_node : str = "1a"
        self.func : str = "core.clean()"
        self.preview : Layout = None
        self.type : str = None
        self.text : str= "d"


def richTable()->Table:
    '''This function creates a rich Table object with the specified properties.'''
    table : Table = Table(
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

def Loader():
    return Padding(Panel("Loading..."), pad=(2, 4, 0, 4),expand=False)
def richNote(text:str,core: "Core")->Padding:

    text_renderable = Text(text ,no_wrap=False)
    return Padding(Panel(text_renderable), pad=(2, 4, 0, 4),expand=False)

def Reward(ary :list = []):
    #chances this might not work due to the choices thing
    grid = Table.grid()
    grid.add_column()
    for reward in ary:
        grid.add_row(reward)
    return Panel(grid)


def get_selectable_options(options: list):
    array = []
    for i in reversed(options):
        if isinstance(i, Choices):
            array.extend(i.ary)
    return array