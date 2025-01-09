class Option():
    def __init__(self,text :str ="",func = None,preview =None,next_node = None,selectable = True ,type :str = "",h_allign = "center",v_allign = "middle") -> None:
        self.text = text
        self.func = func
        self.preview = preview
        self.next_node = next_node
        self.selectable = selectable
        self.selected = False
        self.type = type
        self.v_allign = v_allign
        self.h_allign = v_allign
class Choices():
    def __init__(self,ary :list = None ,core = None,renderable = None,selectable = True):
        self.ary = ary
        self.build(core,renderable)
    def build(self,core,renderable ):
        from core.fight import deal_damage
        array = []
        from items.weapon import WeaponItem
        if renderable != None:
                
            array.append(renderable)
        elif isinstance(self.ary[0],WeaponItem):
            for weapon in self.ary:    
                array.append(WeaponOption(weapon=weapon, func=lambda w=weapon: deal_damage(core, w)))
        else:
            for choice in self.ary:    
        
                array.append(Option(text = choice['text'],func=choice['function'],next_node = choice['next_node'],selectable = True))
        self.ary = array
from rich.padding import Padding

def _dialogue_text(text,style):
    instance : Padding = Padding (
            
                text,
            #pad = (0,0,0,0),
            pad =(4,0,0,0)
    )
    return instance

def WeaponOption(weapon,func):
    return Option(text = weapon.name,func= func,selectable=True,type="weapon")
