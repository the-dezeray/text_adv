from terma.util.logger import logger, event_logger
from typing import TYPE_CHECKING 
from terma.ui.options import Option

def challenge(core,quest='LabyrinthHeart' ,text:str = "", status = "active") -> None:
    """Challenge event that requires the player to make a choice."""
    logger.info("Challenge event triggered")
    core.console.clear_display()
    core.console.print(text)

    if status == "active":
        core.console.print(
            Option(
                text="Accept the challenge", func=lambda: core.goto_next()
            )
        )
              
    if status == "failed":
        core.console.print(
            Option(
                text="Decline the challenge", func=lambda:core.goto_next()
            )
        )