from objects.inventory import Inventory
from objects.weapon import Weapon
from util.logger import logger


class Player:
    def __init__(self):
        self.hp = 100
        self.max_hp = 43
        self.exp = 70
        self.level = 0
        self.max_exp =100
        self.attack = 10
        self.defense = 10
        self.speed = 10
        self.name = "default-name"
        self.luck = 10
        self.crit = 0
        self.max_mp = 100
        self.mp = 50
        self.faith = 0
        self.turn = False
        self.agility = 0  
        self.armor = 0
        self.description = ""
        self.skills = {}
        self.resistance = {}
        self.inventory = Inventory()
        self.add_basic_weapons()
        self.add_basic_skills()
        self.add_basic_resistance()
        logger.info("Player created")
    def trap_interaction(self, trap: dict):
        # attempt escape
        if trap != None:
            logger.info(f"trap invalid -CURRENT CHAPTER - {self.chapter_id}")
        pass

    def add_basic_resistance(self):
        pass

    def add_basic_skills(self):
        pass

    def add_basic_weapons(self):
        self.inventory.add(Weapon.generate(name="shield"))
        self.inventory.add(Weapon.generate(name="sword"))
        self.inventory.add(Weapon.generate(name="oblivion_dagger"))
        

    def is_revivable(self):
        return False
