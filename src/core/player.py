from items.inventory import Inventory
from items.weapon import Weapon
class Player():
    def __init__(self):
        self.hp = 100
        self.max_hp = 100
        self.attack = 10
        self.defense = 10
        self.speed = 10
        self.luck = 10
        self.turn = False
        self.inventory = Inventory()
        self.add_basic_weapons()
        
    def add_basic_weapons(self):
        self.inventory.add(Weapon.generate(name ="bat",level = 1))
    
        self.inventory.add(Weapon.generate(name ="sword",level = 1))

    def is_revivable(self):
        return False
    