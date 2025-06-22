from util.file_handler import load_yaml_file
from util.logger import logger
from typing import Optional

class Item:
    def __init__(self, **kwargs):
        self.type = kwargs.pop("type", None)
        self.amount = 0
        self.name = kwargs.pop("name", None)


class ItemFactory:
    ITEM_DICT = load_yaml_file("data/items.yaml")

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

