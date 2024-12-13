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
