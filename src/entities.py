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
            #log.event()
    @classmethod
    def generate(cls,type :str = "",lvl :int = 0,entity_id : str = ""):
        entity_class = getattr(cls, cls.mapa.get("snake"), None)
        entity_class()
    
