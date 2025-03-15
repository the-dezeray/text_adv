"""This module contains the run event."""

from ui.options import Option, Choices, Loader
from util.logger import logger, event_logger
from random import randint
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    # Import only for type checking (not at runtime)
    from core.core import Core


@event_logger
def run(
    core: "Core", fail: Optional[bool] = None, decision: Optional[bool] = None
) -> None:
    if decision is None:
        core.options.append(
            Loader(
                "attempting escape",
                function=lambda: run(core=core, decision=True, fail=fail),
            )
        )
        return 0
    if fail:
        ...
    else:
        chance = randint(1, 10)
        success: bool = chance % 2 == 0

    if success:
        core.goto_next()
    else:
        ...
