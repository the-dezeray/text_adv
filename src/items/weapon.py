from util.logger import Log 
from util.file_handler import load_json_file
from items.item import Item

class WeaponItem(Item):
    def __init__(self, **kwargs) -> None:
        super().__init__(type="weapon")
        
        self.name = kwargs.pop("name", None)  # Extract 'name' from kwargs
        self.effects = kwargs.pop("effects", [])  # Extract 'effects' from kwargs 
        self.defence =  kwargs.pop("defence", 0)  # Extract 'defence' from kwargs
        self.damage =  kwargs.pop("damage", 0)  # Extract 'damage' from kwargs
        self.condition = kwargs.pop("condition", None)  # Extract 'condition' from kwargs
        self.crit = kwargs.pop("crit", 0)  # Extract 'crit' from kwargs
        self.img = kwargs.pop("img", None)  # Extract 'img' from kwargs
        self.cursed = kwargs.pop("cursed", None)  # Extract 'cursed' from kwargs
        self.description =kwargs.pop("description", None)  # Extract 'description' from kwargs
        self.type =  "weapon"
        self.rarity = kwargs.pop("rarity", None)  # Extract 'rarity' from kwargs 
        self.area_of_effect = kwargs.pop("area_of_effect", None)  # Extract 'area_of_effect' from kwargs
        self.skill_req =kwargs.pop("skill_req", None)  # Extract 'skill_req' from kwargs
        self.noise = kwargs.pop("noise", None)  # Extract 'noise' from kwargs
        self.effect = kwargs.pop("effect", None)  # Extract 'effect' from kwargs
    
        Log.event()  # log the create event to the logger

    def deal_damage(self, player=None) -> None:
        pass


    
class Weapon:
    WEAPON_DICT = load_json_file("config/weapons.json")

    @classmethod
    def generate(cls, name) -> WeaponItem:
        return WeaponItem(**cls.WEAPON_DICT[name])
