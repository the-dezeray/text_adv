     
from util.logger import logger, event_logger
from ui.options import CustomRenderable,ui_text_panel,Option
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from core.core import Core


@event_logger
def chance_event( core:"Core", on_success = None,on_fail = None,probability = 0):
    
    logger.info("You rest for a while")
    core.console.clear_display()
    core.console.print(ui_text_panel(text="You rest for a while"))
  
    core.console.print(
  Option(
                text="Proceed", func=lambda: core.goto_next()
    
        )
    )
 
