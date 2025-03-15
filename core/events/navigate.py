from ui.options import Option, Choices
from util.logger import logger, event_logger


@event_logger
def navigate(core=None, location="treasure"):
    core.options = []
    text = "you have enter a treasure room now there is a chance death awaits y ou in the chest or great wealth"
    core.options.append(
        Option(
            text="you step closer wandering if you should open the treasure chest",
            type="header",
            func=lambda: None,
            selectable=False,
        )
    )
    ary = [
        Option(text="Open", func=lambda: core.goto_next(), selectable=False),
        Option(text="Leave", func=lambda: core.goto_next(), selectable=False),
    ]
    core.options.append(Choices(core=core, ary=ary, do_list_build=True))
