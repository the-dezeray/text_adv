from ui.options import CustomRenderable, ui_text_panel, Option
from util.logger import logger, event_logger
from util.file_handler import load_yaml_file
import random

import random

def creek(core, depth=0) -> None:
    """Creak event: Player might get hit by a boulder, taking HP damage."""
    if random.choice([True, False]):
        core.console.print(ui_text_panel(text="A boulder has fallen on you!"))
        core.player.hp -= 10

        if core.player.hp <= 0:
            core.console.print(ui_text_panel(text="You have been crushed."))
            core.console.print(Option(text="proceed", func=lambda: core.goto_next()))
            return

        if random.choice([True, False]) and depth < 3:
            # Continue deeper into danger
            creek(core, depth + 1)
            return
        else:
            # Survived all attacks, but still needs resolution
            core.console.print(ui_text_panel(text="You barely made it through the creaky terrain."))
            core.console.print(Option(text="proceed", func=lambda: core.goto_next()))
            return
    else:
        core.console.print(ui_text_panel(text="You make it safely across the creaky terrain."))
        core.console.print(Option(text="proceed", func=lambda: core.goto_next()))


def swamp(core):
    """Swamp event: Player loses experience."""
    loss = random.randint(5, 15)
    core.player.exp = max(0, core.player.exp - loss)
    core.console.print(ui_text_panel(text=f"The swamp drains your energy... you lose {loss} EXP!"))

def webs(core):
    """Webs event: Player loses some gold."""
    if hasattr(core.player, "gold"):
        loss = random.randint(1, 20)
        core.player.gold = max(0, core.player.gold - loss)
        core.console.print(ui_text_panel(text=f"Sticky webs slow you down! You drop {loss} gold."))
    else:
        core.console.print(ui_text_panel(text="The webs tangle you, but you have no gold to lose."))

def bolders(core):
    """Boulders event: Player loses a random attribute."""
    possible_attrs = ['hp', 'dmg', 'mp']
    attr = random.choice(possible_attrs)
    if hasattr(core.player, attr):
        val = getattr(core.player, attr)
        reduction = random.randint(1, 3)
        setattr(core.player, attr, max(0, val - reduction))
        core.console.print(ui_text_panel(text=f"A falling rock hits your {attr}! You lose {reduction} {attr}."))
    else:
        core.console.print(ui_text_panel(text="A boulder crashes nearby, but you're unharmed... for now."))

@event_logger
def explore(core=None, area=None):
    """Handles exploration logic for different areas."""
    areas = {
        "creek": lambda: creek(core),
        "swamp": lambda: swamp(core),
        "webs": lambda: webs(core),
        "bolders": lambda: bolders(core)
    }

    if area in areas:
        areas[area]()
    else:
        logger.error(f"story: '{area}' not defined.")
        core.console.print(ui_text_panel(text=f"'{area}' is an unknown area."))

