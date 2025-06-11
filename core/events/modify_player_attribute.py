from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from core.core import Core

def modify_player_attribute(core: 'Core',property:str,amount : int,text:str )-> None:
    core.player.modify_attribute(property,amount,text)      
    core.goto_next()

