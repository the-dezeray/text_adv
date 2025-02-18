from util.logger import logger,event_logger
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    # Import only for type checking (not at runtime)
    from core.core import Core

@event_logger
def investigate(core : 'Core' = None,source : str = None)->None:
    if core is None:
        raise ValueError("Core is None")
    core.goto_next()