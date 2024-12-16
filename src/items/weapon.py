from util.logger import Log
from items.item import Item

class WeaponItem(Item):
    def __init__(self) -> None:
        super().__init__(type = "weapon")
        
        self.name = "----"
        self.effects = []
    
        self.defence :int = 0
        self.damage :int = 0
        self.condition :int = 0
        self.crit :int = 0
        self.img  :str = None
        self.cursed :bool = False
        self.description :str = ""
        self.type :str = "weapon"
        self.rarity :str = ""
        self.a :bool = False
        self.area_of_effect :int = 0
        self.skill_req :int = ""
        self.noise :int  = 0
        self.effect :list = []
    
        Log.event()#log the create event to the logger
    def deal_damage(self,player = None)-> None:
        pass


class sword(WeaponItem):
    def __init__(self,level = 0) -> None:
        super().__init__()
        self.name = "sword"
        self.damage = 10
        self.crit = 23
        self.description = "simple sword "
    
class shield(WeaponItem):
    def __init__(self,level = 0) -> None:
        super().__init__()
        self.name = "shield"
        self.damage = 0
        self.crit = 0
        self.defence = 10
        self.description = "a simple shield"    
class bat(WeaponItem):

    def __init__(self,level = 0 ) -> None:
        super().__init__()
        self.name = "bat"
        self.damage = 10
        self.condition = 10
        self.crit = 10
        self.defence = -1;
        self.img = "bat"
        self.cursed = False
        self.description = "bat"
        Log.event()
    
    
    
class Weapon:
    @classmethod
    def generate(cls, **kwargs) -> WeaponItem:
        name = kwargs.pop("name", None)  # Extract 'name' from kwargs
        if not name:
            #log.event()
            raise ValueError("Weapon name must be specified.")
        entity_class = globals().get(name, None)  # Retrieve the class dynamically
        if not entity_class:
            raise ValueError(f"Weapon '{name}' does not exist.")
        return entity_class(**kwargs)
