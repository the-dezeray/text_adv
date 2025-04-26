from util.logger import logger, event_logger
from ui.options import Option,ui_text_panel,choose_me
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from core.core import Core


@event_logger
def rest(core: "Core" = None):
    logger.info("You rest for a while")
    core.options.clear()
    core.options(ui_text_panel(text="You rest for a while"))
    core.options(ui_text_panel())
    core.options.append(
  choose_me(
                text="Proceed", func=lambda: core.goto_next(), selectable=False
    
        )
    )
 
