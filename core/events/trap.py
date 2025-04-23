from ui.options import Option, choose_me
from util.logger import logger, event_logger


def get_random():
    return 1


@event_logger
def trap(core=None, type: str = None):
    trap = {"name": "fire trap", "damage": 1}
    core.options.append(
        choose_me(
            renderable=Option(
                text="You have been hit by a trap", func=lambda: core.goto_next()
            )
        )
    )
    core.player.contact_with_trap(trap=trap)
