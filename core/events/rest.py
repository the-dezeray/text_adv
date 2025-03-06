from util.logger import logger,event_logger
from ui.options import Option, Choices
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from core.core import Core
@event_logger
def rest(core : "Core"= None):
    logger.info("You rest for a while")
    core.options.append(Choices(renderable = Option(text="Proceed", func=lambda: core.goto_next, selectable=False)))
    core.goto_next()
