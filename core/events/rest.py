from util.logger import logger,event_logger
from ui.options import Option, Choices

@event_logger
def rest(core= None):
    logger.info("You rest for a while")
    core.options.append(Choices(renderable = Option(text="Proceed", func=lambda: core.goto_next, selectable=False)))

