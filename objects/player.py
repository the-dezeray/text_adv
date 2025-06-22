from objects.inventory import Inventory
from objects.weapon import WeaponFactory
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
        self.cash = 0
        self.charm = 0
        self.dmg = 0
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
    def modify_attribute(self,property:str,amount: int,text:str)-> None:
        property_map: dict[str,int]     = {
            "hp": self.hp,
            "max_hp": self.max_hp,
            "exp": self.exp,
            "level": self.level,
            "max_exp": self.max_exp,
            "luck": self.luck,
            "crit": self.crit,
            "mp": self.mp,
            "max_mp": self.max_mp,
            "faith": self.faith,
            "agility": self.agility,
            "armor": self.armor,
        }
        if property in property_map:
            property_map[property] += amount
            logger.info(f"Player {property} modified by {amount} to {property_map[property]}")
        else:
            logger.error(f"Player {property} not found")
            
    def add_basic_resistance(self):
        pass

    def add_basic_skills(self):
        pass
    def contact_with_trap(self, type: str, lvl: int)->None:
        ...
    def add_basic_weapons(self):
        self.inventory.add(WeaponFactory.generate(name="shield"))
        self.inventory.add(WeaponFactory.generate(name="sword"))
        self.inventory.add(WeaponFactory.generate(name="rusted_shiv"))
        self.inventory.add(WeaponFactory.generate(name="bone_club"))
        self.inventory.add(WeaponFactory.generate(name="gate_shield"))
        self.inventory.add(WeaponFactory.generate(name="whip"))
        self.inventory.add(WeaponFactory.generate(name="barbed_flail"))
        self.inventory.add(WeaponFactory.generate(name="furnace_poker"))
  
  
    def is_revivable(self):
        return False
