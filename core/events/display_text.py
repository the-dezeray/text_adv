from util.logger import logger, event_logger
from ui.options import CustomRenderable,ui_text_panel,Option
from rich.panel import Panel
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from core.core import Core


@event_logger
def display_text( core:"Core",  text = ""):
    
    logger.info("You rest for a while")
    core.console.clear_display()
    core.console.print(Panel(text="You rest for a while"))
  
    core.console.print(
  Option(
                text="Proceed", func=lambda: core.goto_next()
    
        )
    )
 
