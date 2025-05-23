from ui.options import CustomRenderable
from util.logger import logger, event_logger
from ui.options import ui_text_panel,Option
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from core.core import Core
@event_logger
def navigate(core:"Core" , location="treasure"):
    core.console.clear_display()
    text = "you have enter a treasure room now there is a chance death awaits y ou in the chest or great wealth"
    core.console.print(
        ui_text_panel(text="you step closer wandering if you should open the treasure chest")
    )

             
    core.console.print(Option(text="pick up", func=lambda: core.goto_next() ))
    core.console.print(Option(text="leave", func=lambda: core.goto_next(),))