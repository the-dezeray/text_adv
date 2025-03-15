from util.file_handler import load_yaml_file
from util.logger import logger


class Item:
    def __init__(self, **kwargs):
        self.type = kwargs.pop("type", None)
        self.amount = 0
        self.name = kwargs.pop("name", None)


class Items:
    ITEM_DICT = load_yaml_file("data/items.yaml")

    @classmethod
    def generate(cls, **kwargs):
        name = kwargs.pop("name", None)
        amount = kwargs.pop("amount", 1)
        item: dict = cls.ITEM_DICT[name]
        item_instance = Item(**item)
        item_instance.amount = amount
        logger.info(f"Item {item_instance.name} generated")
        return item_instance
