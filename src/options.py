class Option():
    def __init__(self,text :str ="",func = None,preview =None,next_node = None,selectable = True ,type :str = "") -> None:
        self.text = text
        self.func = func
        self.preview = preview
        self.next_node = next_node
        self.selectable = selectable
        self.selected = False
        self.type = type
def WeaponOption(weapon,func):
    return Option(text = weapon.name,func= func,selectable=True,type="weapon")
