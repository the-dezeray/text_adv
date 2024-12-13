'''handle Entity generation and creation'''
from util.logger import Log
class Entities():
 
    mapa ={
        
      "snake":"snake",
        "mob": "mob"
    }
    class snake():
        def __init__(self,level = 1) -> None:
            
            self.dmg = level * 2
            self.armor = level *1.5
            self.speed = level *3
            self.hp = level * 30
            self.turn = False
            Log.event()
        def deal_damage(self,player = None):
            print("in fight")
            if player != None :
                 player.hp -= self.dmg
        def heal_self(self,player = None):
            self.hp += 100 
            self.turn = False
    @classmethod
    def generate(cls,type :str = "",lvl :int = 0,entity_id : str = ""):
        entity_class = getattr(cls, cls.mapa.get("snake"), None)
        return entity_class()
        
    
