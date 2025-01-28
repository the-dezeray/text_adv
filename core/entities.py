'''handle Entity generation and creation'''

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
            self.hp = level * 40
            self.turn = False
          
        def deal_damage(self,player = None):
       
            if player != None :
                 player.hp -= self.dmg
        def heal_self(self,player = None):
            self.hp += 100 
            self.turn = False
    @classmethod
    def generate(cls,type :str = "",lvl :int = 0,entity_id : str = ""):
        entity_class = getattr(cls, cls.mapa.get("snake"), None)
        return entity_class()
        
    
