from rich.panel import Panel
from rich.table import Table
from rich.padding import Padding
from rich.layout import Layout
from rich.console import Console
from file_handler import load_yaml_file
from options import Option
from main_layout import character_selection_layout,character_preview_layout,gameplay_layout
class Game():
    def __init__(self,interface = None) -> None:
        self.running = True
        
        self.story = load_yaml_file("story.yaml")
        self.chapter_id = "1a"
        self.interface =character_selection_layout()
        self.options_displayed = True
        self.in_game = True
        self.love = None
        self.key_listener = None

        self.options = [Option(text = "new journey",func=self.continue_game)
        ,Option("exsiting journey",self.continue_game,lambda a = "desiree":self.display_preview(value = a)),
        Option("exit",self.exit_game)]

        #other = [Option(text ="Desiree",preview= self.preview_character(name = "Desiree"))]
        #self.options = other
        self.selected_option = 0
        self.table = Table()
        self.refresh()
    def preview_character(self):
        pass
    def display_preview(self,value = None):
        layout = character_preview_layout()
        self.interface["preview"].update(layout)
    def load_new_game(self):
        
        self.layout = character_selection_layout()
    def start_game(self):pass
    def continue_game(self):
        print("working")
        self.in_game = True
        self.interface   = gameplay_layout()
        self.game_loop()
    def option_table(self):
        self.table = Table(expand=True,show_edge=False,show_header=False)
        self.table.add_column()
                
        for i ,option in enumerate(self.options):    
            style = "none"
            x = 5
            if i == self.selected_option:
                if self.options[i].preview:
                    self.options[i].preview()
                style = "bold green"
                x += 5
            #self.table.add_row(Padding(Panel(option.text,border_style=style),pad =(0,0,0,x))) 
            self.table.add_row(self.menu_button(text = option.text,style = style,x=x))
    def menu_button(self,text,style,x):
        instance : Padding = Padding (
                Panel(
                    text,
                    border_style = style
                    ),
                pad = (0,0,0,x)
        )
        return instance
    def exit_game(self):pass
    def refresh(self):
        self.option_table()
        self.interface["options"].update(self.table)
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
                from main_layout import make_layout
   

                self.refresh()
            #RUN COMMAND
            case "Key.enter":
            
                if self.options_displayed:
                    self.options[self.selected_option].func()

            #default
            case _:
                pass   
    def game_loop(self):
            
            current_chapter = self.story[self.chapter_id]
            table = Table(expand=True,show_header = False,show_edge=False)
            table.add_column()
            table.add_row(Padding(Panel(current_chapter["text"]),pad =(0,20,0,0)))
            #interface.display(current_chapter["text"])
            self.options = []
            for index,choice in enumerate(current_chapter["choices"]):
                
                table.add_row(Padding(Panel(f"{index}.{choice['text']}"),pad=(0,100,0,0)))
                self.options.append(choice['function'])
            
            self.interface["preview"].update(table)
            self.love.update(self.interface)
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


