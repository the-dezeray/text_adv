'''core of the game'''
from rich.panel import Panel
from rich.table import Table
from rich.padding import Padding
from rich.layout import Layout
from rich.console import Console
from file_handler import load_yaml_file
from options import Option
from main_layout import character_selection_layout,character_preview_layout,gameplay_layout, make_layout
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
        from console import Console
      
        self.options = [Option(text = "new journey",func=self.continue_game,)
        ,Option("exsiting journey",self.continue_game,lambda a = "desiree":self.display_preview(value = a)),
        Option("exit",self.exit_game)]

        self.console = Console(core = self)
        self.console.refresh()
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

    def exit_game(self):pass

    def game_loop(self):
            
        current_chapter = self.story[self.chapter_id]

        self.s = 'preview'
                        

        #interface.display(current_chapter["text"])
        #self.options.append(Padding(Panel(current_chapter['text']),pad=(0,20)))

        self.options.append(Option(text = current_chapter['text'],selectable = False,type ="header"))
        for index,choice in enumerate(current_chapter["choices"]):
            
            
            self.options.append(Option(text = choice['text'],func=choice['function'],next_node = choice['next_node'],selectable = True))
            
        #self.console.refresh()
        #self.refresh()
        # self.interface["preview"].update(table)
        self.love.update(self.interface)



           


