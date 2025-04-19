"""handle Entity generation and creation"""

from util.file_handler import load_yaml_file
from util.logger import logger


class entity:
    def __init__(self, **kwargs) -> None:
        level = kwargs.pop("level")
        self.level = level
        self.name = ""
        self.weapon = None
        self.intelligence = 3
        self.luck = 0
        self.crit = 0
        self.profile_art = ""
        self.description = ""
        self.agility = 0
        self.resitant = {}
        self.droppable_items = {}
        self.flee = 0
        self.dmg = level * 30
        self.armor = level * 1.5
        self.speed = level * 3
        self.hp = level * 40
        self.turn = False
        self.rank = ""

    def drop():
        pass

    def escape():
        pass

    def deal_damage(self, player=None):
        if player != None:
            player.hp -= self.dmg

    def heal_self(self, player=None):
        self.hp += 100
        self.turn = False


class Entities:
    ENTITIES_DICT = load_yaml_file("data/entities.yaml")

    @classmethod
    def generate(cls, **kwargs):
        type = kwargs.pop("type", None)
        if type != None:
            instance_attributes: dict = cls.ENTITIES_DICT[type]
            instance = entity(**instance_attributes)
            logger.info(f"Generated entity {type}")
            return instance
