from logging import disable
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
        
        core.console.print(Option(text=weapon.name, func=lambda index=index: pick_weapon(index),disable_others=False))
    core.console.print(Option(text="leave and proceed"))
def randomly_generate_items(core:"Core", count=1, level="low"):
    """
    Generate a list of random items based on the specified level.
    """
    items = ItemFactory.generate_randomly(level=level, count=count)
    if not items:
        logger.warning(f"No items found for level '{level}'.")
        return []
    def pick_item(index):
        #item = items[index]
        #core.player.inventory.add(item)
        #core.console.print(ui_text_panel(text=f"You have selected the {item.name}."))
        del core.console.renderables[index]
  
    core.console.print(ui_text_panel(text="You find some items:"))
    menu = []
    for index,item in enumerate (items):
        i = len(core.console.renderables)
        menu.append(Option(text=item.name, func=lambda index=i: pick_item(index),disable_others=False))
    core.console.print(menu)

from typing import Union
def show_items(core :"Core", items = list[tuple]|tuple)->None:
    def generate(core=core,name :str = "",count:int =1 )->None:
        if (item_instance :=ItemFactory.generate(name = name,amount=count)) is not None:
          
            core.player.inventory.add(item_instance)
            core.console.print(ui_text_panel(text=f"You have added {count} {name}(s) to your inventory."))
        elif (weapon_instance := WeaponFactory.generate(name=name, amount=count)) is not None:
            core.player.inventory.add(weapon_instance)
            core.console.print(ui_text_panel(text=f"You have added {count} {name}(s) to your inventory."))
        else:
            logger.warning(f"Failed to generate item or weapon with name '{name}' and count {count}.")
            core.console.print(ui_text_panel(text=f"no items where found "))
    if not items:
        logger.warning("No items to display.")
        core.console.print(ui_text_panel(text="No items to display."))
        return
    
    if isinstance(items, tuple):
        name = items[0]
        count = items[1]
        generate(core=core, name=name, count=count)
    elif isinstance(items, list):
        for item in items:
            generate(core=core, name=item[0], count=item[1])
    core.console.print(Option(text="You can now proceed with your adventure."))