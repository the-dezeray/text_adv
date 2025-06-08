from typing import TYPE_CHECKING
from util.logger import logger, event_logger
from ui.options import CustomRenderable,ui_text_panel,Option


if TYPE_CHECKING:
    from core.core import Core

if TYPE_CHECKING:
    # Import only for type checking (not at runtime)
    from core.core import Core


def attempt_steal(core: "Core" ,item="",stealth_check  =0,on_success = None,on_fail = None):
    core.console.clear_display()
    text = "you have obtained"
    core.console.print(
        ui_text_panel(text=text)
    )

    core.console.print(Option(text="pick up", func=lambda: core.goto_next() ))
    core.console.print(Option(text="leave", func=lambda: core.goto_next(),))