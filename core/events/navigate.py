from ui.options import Option
from util.logger import logger, event_logger
from ui.options import ui_text_panel,choose_me
@event_logger
def navigate(core=None, location="treasure"):
    core.options.clear()
    text = "you have enter a treasure room now there is a chance death awaits y ou in the chest or great wealth"
    core.options.append(
        ui_text_panel(text="you step closer wandering if you should open the treasure chest")
    )

             
    core.options.append(choose_me(text="Open", func=lambda: core.goto_next(), ))
    core.options.append(choose_me(text="Leave", func=lambda: core.goto_next(),))

