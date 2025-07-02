from rich.align import Align
from rich.panel import Panel
from rich.text import Text
from rich.padding import Padding
from ui.options import CustomRenderable, Option
from util.logger import logger, event_logger
from ui.options import Delay
from typing import TYPE_CHECKING
from ui.options import TyperWritter
if TYPE_CHECKING:
    from core.core import Core
from ui.options import ui_text_panel
def get_random():
    return 1


@event_logger
def trigger_trap(core:"Core", type: str = "None" , lvl = 1,text:str = "You have been hit by a trap"):
    trap = {"name": "fire trap", "damage": 1}
    core.console.print(Align(Panel(renderable="",height=2,width=20),align="center"))
    core.console.print(Align(Padding(renderable="[red]FLAME TRAP[/red]"),align="center"))
    core.console.print(Delay(duration=1))
    core.console.print(Align(Padding(renderable="[dim red]You have been hit by a trap[/dim red]"),align="center"))
    core.console.print(Delay(duration=1))
    text ="[orange_red1]"+"*" * 20+"[/orange_red1]"+ " [red1]- 82[/red1]"
    core.console.print(Align(Padding(renderable=text),align="center"))
    core.console.print(Delay(duration=0.3))
    core.console.print(Align(Padding(renderable="[cyan3]it stings but you try to recover and continue[/cyan3]"),align="center"))
    core.console.print(Delay(duration=0.3))
    core.console.print(TyperWritter(text="You have been hit by a trap"))
    core.console.print(Delay(duration=0.3))
    
    core.player.contact_with_trap(type,lvl)
    core.goto_next()        
