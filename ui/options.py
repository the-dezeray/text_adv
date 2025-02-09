'''This module contains the Option class and Choices class. The Option class is used to create an option object that can be used in the Choices class. The Choices class is used to create a list of options that can be used in the UI. The WeaponOption function is used to create an option object for weapons. The _dialogue_text function is used to create a text object for the UI.'''
from rich.padding import Padding

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
    def __init__(self,ary :list = None ,core = None,renderable = None,selectable = True,do_build=True):
        self.ary = ary
        if do_build == True:
            self.build(core,renderable)

    def build(self,core,renderable ):
        
        from core.events.fight import deal_damage # dont remove this prevents circular import
        
        array = []
        from objects.weapon import WeaponItem
        if renderable != None:
            array.append(renderable)
        elif isinstance(self.ary[0],WeaponItem):
            for weapon in self.ary:    
                array.append(WeaponOption(weapon=weapon, func=lambda w=weapon: deal_damage(core, w)))
        else:
            for choice in self.ary:     
                array.append(Option(text = choice['text'],func=choice['function'],next_node = choice['next_node'],selectable = True))
        self.ary = array

def _dialogue_text(text,style):
    instance : Padding = Padding (
        text,
        pad =(4,0,0,0)
    )
    return instance

def WeaponOption(weapon,func):
    return Option(text = weapon.name,func= func,selectable=True,type="weapon")
