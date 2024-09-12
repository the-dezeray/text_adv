from file_handler import load_yaml_file

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
    

    
    
def fight(entity = None,player= None):
    pass
    
    
class Game():
    def __init__(self,) -> None:
        self.running = True
        self.story = load_yaml_file("story.yaml")
        self.chapter_id = "1a"
        self.interface = None
       
    def fight(self):
        self.interface.fight()
        self.interface.show_health_bar()
        self.interface.show_user_options()
        a = 1
           
        
    def main_loop(self,interface):
        
        current_chapter = self.story[self.chapter_id]
        
        interface.display(current_chapter["text"])

        for index,choice in enumerate(current_chapter["choices"]):
            print(f"{index}.{choice['text']}")

        user_input =interface.get_user_input(restriction= len(current_chapter["choices"]))
        selected_choice = int(user_input)

        function_as_string = current_chapter["choices"][selected_choice]["function"]
        interface.display(function_as_string)
        exec(function_as_string)


class Display():
    @classmethod 
    def display(cls,string = ""):
        print(string)
        pass       
    
          
    @classmethod
    def get_user_input(cls,restriction = None): 
        return input("enter choice: ")

if __name__ == "__main__":
    core = Game()
    display = Display()
    core.main_loop(interface= display)



