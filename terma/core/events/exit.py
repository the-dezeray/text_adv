
from terma.util.logger import logger, event_logger
from typing import TYPE_CHECKING

def exit_story(core, text:str = "") -> None:
    """Exit the story and show the player's statistics."""
    if not core.test_mode:
        logger.info("Exiting story" )
        core.console.print(text)

        #self._state = "STATS"
        #self.console.layout = "STATS"
        core.TERMINATE()
    else: 
        core.console.print(text)