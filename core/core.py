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
from ui.console import Op
from util.logger import logger

import datetime

def get_selectable_options(options: list):
    a =[]
    for i in options:
        if isinstance(i, Op):
            a.append(i)
    if len(a) == 0:
        for i in options:
            if isinstance(i, Choices):
                return i.ary
            
class Core():
    def __init__(self) -> None:
        self.rich_console = None
        self.running = True
        self.ant =[]
        self.in_fight = False
        self.story = load_yaml_file("config/story.yaml")
        self._chapter_id = "1a" #default value
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
        self.post_initialize()
    def post_initialize(self):
        current_time = datetime.datetime.now()
        logger.info(f"New game instance {current_time}")
        self.check_story()


    
    def check_story(self):
        print("Checking story")
    @property
    def chapter_id(self):
        return self._chapter_id
    
    @chapter_id.setter
    def chapter_id(self,value):
        if value not in self.story:
            raise ValueError(f"The chapter '{value}' is not defined.")
        self._chapter_id = value


    def execute_yaml_function(self, func: str):
        core = self
        logger.info(f"Executing function: {func}")

        local_scope = {"core": core}  # Define the scope where 'core' is available
        
        try:
            exec(func, globals(), local_scope)
        except Exception as e:
            logger.error(f"Error executing function: {func} - {e}")

    def clean(self):
        self.console.current_layout =None
        self.chapter_id = "1a"

        self.continue_game()
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