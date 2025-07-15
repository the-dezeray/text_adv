from numpy.lib._function_base_impl import iterable
from util.logger import logger
from typing import Literal, TYPE_CHECKING


if TYPE_CHECKING:
    from objects.item import Item

from typing import Iterable
from objects.weapon import WeaponFactory
from objects.item import ItemFactory
class Inventory:
    def __init__(self, items: list["Item"] = []):
        self.items: list["Item"] = []
        if items:
            for item in items:
                if item["type"] =="weapon":
                    self.items.append(WeaponFactory.create_weapon(item))
                else:
                    self.items.append(ItemFactory.create_item(item))

       

    def add(self, item: "Item"):
        self.items.append(item)
        logger.info(f"Added {item.name} to inventory")
    def __iter__(self) -> Iterable["Item"]:
        return iter(self.items)
    def weapons(self, type: Literal["defence", "attack", "none"] = "none"):
        if type == "defence":
            list_of_weapons = [
                item
                for item in self.items
                if item.type == "weapon" and item.defence > 0
            ]
        elif type == "attack":
            list_of_weapons = [
                item for item in self.items if item.type == "weapon" and item.damage > 0
            ]
        else:
            list_of_weapons = [item for item in self.items if item.type == "weapon"]
        return list_of_weapons
