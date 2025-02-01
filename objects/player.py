from objects.inventory import Inventory
from objects.weapon import Weapon
from util.logger import logger
class Player():
    def __init__(self):
        self.hp = 100
        self.max_hp = 100
        self.attack = 10
        self.defense = 10
        self.speed = 10
        self.name = "default-name"
        self.luck = 10
        self.crit = 0
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
        

    def add_basic_weapons(self):
        self.inventory.add(Weapon.generate(name ="shield"))
        self.inventory.add(Weapon.generate(name ="sword"))

    def is_revivable(self):
        return False
    