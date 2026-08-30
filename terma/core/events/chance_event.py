     
from terma.util.logger import logger, event_logger
from terma.ui.options import CustomRenderable,ui_text_panel,Option
from typing import TYPE_CHECKING
import random 
if TYPE_CHECKING:
    from terma.core.core import Core


@event_logger
def chance_event( core:"Core", on_success = None,on_fail = None,probability = 0.0):
    
    roll = random.random()
    logger.info("You rest for a while")
    
    if roll < probability:
        next_func = on_success if on_success else core.goto_next
    else:
         next_func = on_fail if on_fail else core.goto_next

    core.console.clear_display()
    
    core.console.print(ui_text_panel(text="You rest for a while"))
  
    core.console.print(
        Option(
            text="Proceed", 
            func=next_func,
            next_node=core.next_node
        )
    )
 
