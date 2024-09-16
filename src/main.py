from file_handler import load_yaml_file
from rich.style import Style

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
    def __init__(self,interface = None) -> None:
        self.running = True
        self.story = load_yaml_file("story.yaml")
        self.chapter_id = "1a"
        self.interface =interface

        self.options = ["new journey ","exsiting journey","exit",]
        self.selected_option = 0
        self.table = Table()
        self.refresh()

    
    def refresh(self):
        self.table = Table(expand=True,show_edge=False,show_header=False)
        self.table.add_column()
                
        for i ,text in enumerate(self.options):    
            style = "none"
            x = 40
            if i == self.selected_option:
                style = "bold green"
                x -= 5
            self.table.add_row(Padding(Panel(text,border_style=style),pad =(0,x))) 
                
        self.interface["main"].update(self.table)
    def save_key(self,key):
        """handles keyboard input"""
        input_string :str= str(key)
        input_string = input_string.replace("'","")
        
        match input_string:
            case "Key.space":
                input_string = " "
            
            case "Key.backspace":
                input_string = ""
                self.current_entry_text =  self.current_entry_text[:-1]
            case "Key.up":
                self.selected_option -=1
                self.refresh() 
            case "Key.down":
                self.selected_option += 1
                self.refresh()
            #RUN COMMAND
            case "Key.enter":
                self.run_command()
                self.current_entry_text = ""
            #default
            case _:
                pass   
    def fight(self):
        self.interface.fight()
        self.interface.show_health_bar()
        self.interface.show_user_options()
        a = 1
           
        
    def main_loop(self):
        interface = self.interface
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



"""handles program launch"""
import queue
import time

from pynput.keyboard  import Listener
from rich.live import Live
from rich.table import Table
from rich.layout import Layout
from rich.panel import Panel
from rich.padding import Padding
from rich.console import Console,Group
from rich.spinner import Spinner

console = Console()


def make_layout() -> Layout:
    """return a structured Layout object

    Returns:
        Layout: Layout object
    """
    layout = Layout(name="root") 
    layout.split(
    
        Layout(name="main", ratio = 3),
        

    )
    
    
    return layout

def main():

    """Program Launch"""
    layout = make_layout()
    core = Game(interface = layout)

    #listens for keyboard key press
    with Listener(on_press= core.save_key) as L:
        #Renders an auto-updating terminal
        with Live(layout, refresh_per_second=10):  # update 10  times a second to feel fluid
            
            while core.running: #if program has not been terminated
                pass
        L.join()
    
                
if __name__ == "__main__":

    main()

