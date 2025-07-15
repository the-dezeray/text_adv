from util.file_handler import load_yaml_file
from util.logger import logger
from typing import Optional

class Item:
    def __init__(self, **kwargs):
        self.type = kwargs.pop("type", None)
        self.amount = 0
        self.name = kwargs.pop("name", None)

    def to_dict(self) -> dict:
        return {
            "type": self.type,
            "amount": self.amount,
            "name": self.name
        }   

class ItemFactory:
    ITEM_DICT = load_yaml_file("data/items.yaml")
    low_level_items = [name for name, data in ITEM_DICT.items() if data.get("lvl") == "low"]
    mid_level_items = [name for name, data in ITEM_DICT.items() if data.get("lvl") == "mid"]
    high_level_items = [name for name, data in ITEM_DICT.items() if data.get("lvl") == "high"]
    @classmethod
    def generate_randomly(cls,type:str ="potion",level:str = "low",count:int=1 ):

        """
        Generate a list of random items based on the specified level.
        """
        if level == "mid":
            item_names = cls.mid_level_items
        elif level == "high":
            item_names = cls.high_level_items
        else:
            item_names = cls.low_level_items

        if not item_names:
            logger.warning(f"No items found for level '{level}'.")
            return []

        from random import sample
        selected_names = sample(item_names, min(count, len(item_names)))
        return [item for name in selected_names if (item := cls.generate(name)) is not None]
    @classmethod
    def create_item(cls, item: dict) -> Optional[Item]:
        """
        Create an Item from a dictionary.
        """
        if item.get("type") == "item":
            item_instance = Item(**item)
            if item_instance:
                return item_instance
            else:
                logger.warning(f"Item '{item['name']}' not found in item data.")
    @classmethod
    def generate(cls, name: str,amount:int=1) -> Optional[Item]:
        args = cls.ITEM_DICT.get(name)
        if args:
  
            item_instance= Item(**args)
            item_instance.amount = amount
            logger.info(f"Item {item_instance.name} generated")
            return item_instance
        else:
            logger.warning(f"item  '{name}' not found in item data.")
            return None

