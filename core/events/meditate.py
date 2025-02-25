from ui.options import Option, Choices
from util.logger import event_logger
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    # Import only for type checking (not at runtime)
    from core.core import Core

@event_logger
def meditate(core: "Core" ,value :str = ""):
    core.goto_next()
    