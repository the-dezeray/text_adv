class Inventory():
    def __init__(self):
        self.items = []
    
    def add(self,item):
        self.items.append(item)
    
    def weapons(self,type = "none"):
        if type == "defence":
            list_of_weapons = [item for item in self.items if item.type == "weapon" and item.defence > 0]
        elif type == "attack":
            list_of_weapons = [item for item in self.items if item.type == "weapon" and item.damage > 0]
        else:
          list_of_weapons = [item for item in self.items if item.type == "weapon"]

        return list_of_weapons