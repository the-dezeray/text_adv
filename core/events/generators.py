from util.logger import logger, event_logger
from objects.weapon import WeaponFactory
from objects.item import ItemFactory
from ui.options import CustomRenderable,ui_text_panel,Option,MinimalMenuOption
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from core.core import Core


@event_logger
def rest( core:"Core", event = None,probability = 0):
    
    logger.info("You rest for a while")
    core.console.clear_display()
    core.console.print(ui_text_panel(text="You rest for a while"))
    
    core.console.print(  Option(
                text="Proceed", func=lambda: core.goto_next()
    
        )
    )


def randomly_generate_weapons(core:"Core", count=1, level="low"):
    """
    Generate a list of random weapons based on the specified level.
    """
    weapons = WeaponFactory.generate_randomly(level=level, count=count)
    if not weapons:
        logger.warning(f"No weapons found for level '{level}'.")
        return []

  
    core.console.print(ui_text_panel(text="You find some weapons:"))
    menu = []

    def pick_weapon(index):
        # weapon = weapons[index]
        #core.player.inventory.add(weapon)
        #core.console.print(ui_text_panel(text=f"You have selected the {weapon.name}."))
        del core.console.renderables[index]

    for i, weapon in enumerate(weapons):
        index = len(core.console.renderables)
        core.console.print(Option(text = index))
        core.console.print(Option(text=weapon.name, func=lambda index=index: pick_weapon(index),disable_others=False))
        
def randomly_generate_items(core:"Core", count=1, level="low"):
    """
    Generate a list of random items based on the specified level.
    """
    items = ItemFactory.generate_randomly(level=level, count=count)
    if not items:
        logger.warning(f"No items found for level '{level}'.")
        return []

  
    core.console.print(ui_text_panel(text="You find some items:"))
    menu = []
    for item in items:
        menu.append(Option(text=item.name, func=lambda w=item: core.player.inventory.add(w)))
    core.console.print(menu)


