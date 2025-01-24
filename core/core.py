'''core of the game'''
from rich.table import Table
from rich.console import Console
from util.file_handler import load_yaml_file
from ui.options import Option ,Choices
from rich.layout import Layout
from core.entities import Entities
from items.item import Items
from core.functions import receive
from core.fight import fight
from core.player import Player
from ui.console import Console
from core.read import read

def get_selectable_options(options: list):
    for i in options:
        if isinstance(i, Choices):
            return i.ary
        
class Core():
    def __init__(self,interface = None) -> None:
        self.running = True
        self.ant =[]
        self.in_fight = False
        self.story = load_yaml_file("config/story.yaml")
        self.chapter_id = -1
        self.interface =Layout("des")
        self.in_game = True
        self.love = None
        self.move_on = True
        self.entity = None
        self.key_listener = None
        self.s = 'options'
        self.table = Table()
        self.selected_option = 0
        self.others = []
        self.player = Player()
        self.player_turn = False
        self.next_node = None
        self.options = []
        self.console = Console(core = self)

    def execute_yaml_function(self,func: callable):
        core = self
        exec(func)
    def clean(self):
        self.console.clean()
    def continue_game(self):
        #set the selected option to 0
        self.selected_option = 0
        if self.chapter_id == -1:
            self.console.refresh(layout="charactor")
        else:
            current_chapter = self.story[self.chapter_id]
            self.options = []
            self.options.append(Option(text = current_chapter['text'],selectable = False,type ="header"))
            #or index,choice in enumerate(current_chapter["choices"]):    
            self.options.append(Choices(current_chapter["choices"]))    
            self.love.update(self.interface)
            self.console.refresh()

    def goto_next(self):
        self.chapter_id = self.next_node
        self.continue_game()