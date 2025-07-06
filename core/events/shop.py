from ui.options import CustomRenderable,Option
from rich.panel import Panel
from ui.options import GridOfWeaponsShop,GridOfWeapons
from rich.rule import Rule
from rich.text import Text
from rich.style import Style
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from core.core import Core

def shop(core:"Core", level="normal", items=[], prices=[],text=''):
    core.console.clear_display()
    core.console.print(
        Rule(title="shop",style="cyan1")
    )
    
    
    core.console.table.border_style = "green"
    core.console.print(Text("a strange man approaches you and say welcome to my cavern",style="bold green"))
    core.console.print((GridOfWeaponsShop(core=core,ary=core.player.inventory.weapons(type="attack"))))
    core.console.print((GridOfWeaponsShop(core=core,ary=core.player.inventory.weapons(type="attack"))))
    def go_to_shop():
        core.console.clear_display()
        core.goto_next()
        core.console.table.border_style = None
        


    core.console.print(

        Option(text="shop", func=go_to_shop)
    )
    
