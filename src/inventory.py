class Inventory():
    def __init__(self):
        self.items = []
    
    def add(self,item):
        self.items.append(item)
    
    def weapons(self):
   
        list_of_weapons = [item for item in self.items if item.type == "weapon"]

        return list_of_weapons