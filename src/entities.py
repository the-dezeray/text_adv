'''handle Entity generation and creation'''
from logger import Log
class Entities():
 
    mapa ={
        
        "snake":"snake"
    }
    class snake():
        def __init__(self,level = 1) -> None:
            
            self.dmg = level * 2
            self.armor = level *1.5
            self.speed = level *3
            self.hp = level * 30
            Log.event()
        def deal_damage(self,player = None):
            pass
    @classmethod
    def generate(cls,type :str = "",lvl :int = 0,entity_id : str = ""):
        entity_class = getattr(cls, cls.mapa.get("snake"), None)
        return entity_class()
        
    
