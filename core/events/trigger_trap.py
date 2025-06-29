from ui.options import CustomRenderable, Option
from util.logger import logger, event_logger
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from core.core import Core
from ui.options import ui_text_panel
def get_random():
    return 1


@event_logger
def trigger_trap(core:"Core", type: str = "None" , lvl = 1,text:str = "You have been hit by a trap"):
    trap = {"name": "fire trap", "damage": 1}
    core.console.print(
        ui_text_panel(text="You have been hit by a trap")
        )
    
    core.player.contact_with_trap(type,lvl)
    core.goto_next()        
