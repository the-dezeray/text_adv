from rich.padding import Padding
from typing import TYPE_CHECKING
from rich.style import Style
from rich.align import Align
if TYPE_CHECKING:
    from core.core import Core

def modify_player_attribute(core: 'Core',property:str,amount : int,text:str )-> None:
    style = Style(bgcolor="dark_olive_green3",color="black")
    core.player.modify_attribute(property,amount,text)      
    core.console.print(Align.center(Padding(text,style=style)))
    core.goto_next()

