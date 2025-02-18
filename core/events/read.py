from ui.options import Option, Choices
from util.logger import logger,event_logger
scrolls= {"ancient_scroll":"you see things"}

@event_logger
def read(core ,scroll :str = ""):
    string = scrolls.get(scroll,None)
    if string != None:
        core.options.append(Option(text=string, type="header", func=lambda: None, selectable=False))
        core.options.append(Choices(renderable = Option(text="Proceed", func=lambda: core.goto_next(), selectable=False)))
    