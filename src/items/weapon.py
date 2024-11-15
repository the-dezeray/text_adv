from util.logger import Log
from items.item import Item
class Weapon():
    
    class weapon(Item):
        def __init__(self) -> None:
            super().__init__(type = "weapon")
            
            self.name = "----"
            self.effects = []
            self.type = "weapon"
            self.damage :int = 0
            self.condition :int = 0
            self.crit :int = 0
            self.img  = None
            self.cursed :bool = False
            self.description :str = ""
            self.type :str = ""
            self.rarity :str = ""
            self.a :bool = False
            self.area_of_effect :int = 0
            self.skill_req :int = ""
            self.noise = 0
            self.effect = []
            self.type = 'weapon'
            Log.event()
        def deal_damage(self,player = None):
            pass
    class sword(weapon):
        def __init__(self) -> None:
            super().__init__()
            self.name = "sword"
            self.damage = 10
            self.crit = 23
            self.description = "simple sword "
    class bat(weapon):
        def __init__(self,level = 0 ) -> None:
            super().__init__()
            self.name = "bat"
            self.damage = 10
            self.condition = 10
            self.crit = 10
            self.img = "bat"
            self.cursed = False
            self.description = "bat"
   
            

            Log.event()
     
    @classmethod
    def generate(cls,name:str = "",**kwargs):
        entity_class = getattr(cls, name, None)
        return entity_class(**kwargs)
        
    
