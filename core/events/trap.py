from ui.options import CustomRenderable, Option
from util.logger import logger, event_logger


def get_random():
    return 1


@event_logger
def trap(core=None, type: str = None , lvl = 1):
    trap = {"name": "fire trap", "damage": 1}
    core.console.print(
        Option(
            renderable=CustomRenderable(
                text="You have been hit by a trap", func=lambda: core.goto_next()
            )
        )
    )
    core.player.contact_with_trap(trap=trap)
