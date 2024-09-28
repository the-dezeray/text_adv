
from rich.panel import Panel
from rich.table import Table
from rich.padding import Padding
from rich.layout import Layout
from rich.console import Console
from file_handler import load_yaml_file
from options import Option
from main_layout import character_selection_layout,character_preview_layout,gameplay_layout
class Player():
    def __init__(self):
        self.turn = False
    def show_actions(entity = False):
        pass
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
        self.s = 'options'
        self.table = Table()
        self.selected_option = 0
        self.others = []
        self.player = Player()
        self.player_turn = False
        self.options = [Option(text = "new journey",func=self.continue_game,)
        ,Option("exsiting journey",self.continue_game,lambda a = "desiree":self.display_preview(value = a)),
        Option("exit",self.exit_game)]


        self.refresh()
    def fight(self,entity):
        self.options = []
        self.player.turn = False
        
        while True:
            if self.player.turn == False:
                enitity.deal_damage(self.player)
            else : 
                player.show_actions(self.entity)
        # "fight(entity =Entities.generate(type = 'snake',lvl =3 ))"
    def preview_character(self):
        pass
    def display_preview(self,value = None):
        layout = character_preview_layout()
        self.interface["preview"].update(layout)
    def load_new_game(self):
        
        self.layout = character_selection_layout()
    def start_game(self):pass
    def continue_game(self):
        self.options = []
        print("working")
        self.in_game = True
        self.interface   = gameplay_layout()
        self.game_loop()
    def option_table(self):
        
        self.table = Table(expand=True,show_edge=False,show_header=False)
        self.table.add_column()
        for others in self.others:
            self.table.add_row(others)
        if len(self.options) > 9 : self.options = self.options[9:]
        for i ,option in enumerate(self.options):    
            style = "none"
            x = 5
            if option.selected:
                if self.options[i].preview:
                    self.options[i].preview()
                style = "bold green"
                x += 5
            #self.table.add_row(Padding(Panel(option.text,border_style=style),pad =(0,0,0,x)))
            if option.type == 'header' :
                item = self.header_option(text = option.text,style = style)
            else: 
                item = self.menu_button(text = option.text,style = style,x=x)
            self.table.add_row(item)
    def header_option(self,text,style):
        instance : Padding = Padding (
                
                    text,
                pad = (0,0,0,0)
        )
        return instance

    def menu_button(self,text,style,x):
        instance : Padding = Padding (
                Panel(
                    text,
                    width= 20,
                    border_style = style,
                    ),
                pad = (0,10,0,x)
        )
        return instance
    def exit_game(self):pass
    def refresh(self):
        self.option_table()

        self.interface[self.s].update(self.table)
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
                selectable_options = len([option for option in self.options  if option.selectable == True ])
             
                if self.selected_option < 0 : self.selected_option = selectable_options-1
                if self.selected_option > selectable_options : self.selected_option = 0
                a= [option for option in self.options if option.selectable == True]
                for i,option in enumerate (a) :
                    option.selected =False
                    if i == self.selected_option :
                        option.selected=True
                        
                        
                    
            case "Key.down":
                self.selected_option += 1
        
            #RUN COMMAND
            case "Key.enter":
            
                if self.options_displayed:
                    for option in self.options:
                        if option.selected == True:
                            function = option
                    if isinstance(function.func, str):
                        if len(function.func) > 1 and function.func != None:
                            exec(function.func)

                    elif callable(function.func):
                        function.func()
        
                    if function.next_node != None:
                        self.chapter_id = function.next_node
                        for option in self.options:
                            option.selectable = False
                        self.game_loop()
            #default
            case _:
                pass 
        self.refresh() 
    def game_loop(self):
            
        current_chapter = self.story[self.chapter_id]

        self.s = 'preview'
                        

        #interface.display(current_chapter["text"])
        #self.options.append(Padding(Panel(current_chapter['text']),pad=(0,20)))

        self.options.append(Option(text = current_chapter['text'],selectable = False,type ="header"))
        for index,choice in enumerate(current_chapter["choices"]):
            
            
            self.options.append(Option(text = choice['text'],func=choice['function'],next_node = choice['next_node'],selectable = True))
            

        self.refresh()
        # self.interface["preview"].update(table)
        self.love.update(self.interface)


    def fight(self):
        self.interface.fight()
        self.interface.show_health_bar()
        self.interface.show_user_options()
        a = 1
           


