from util.logger import logger
from typing import Literal, TYPE_CHECKING


if TYPE_CHECKING:
    from objects.item import Item
class Inventory():
    def __init__(self):
        self.items = []
    
    def add(self,item: "Item"):
        self.items.append(item)
        logger.info(f"Added {item.name} to inventory")
         
    def weapons(self,type : Literal["defence","attack","none"] = "none"):
        if type == "defence":
            list_of_weapons = [item for item in self.items if item.type == "weapon" and item.defence > 0]
        elif type == "attack":
            list_of_weapons = [item for item in self.items if item.type == "weapon" and item.damage > 0]
        else:
          list_of_weapons = [item for item in self.items if item.type == "weapon"]
        return list_of_weapons