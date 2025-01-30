'''core of the game'''

import datetime

from util.file_handler import load_yaml_file
from ui.options import Option ,Choices
from rich.layout import Layout
from objects.entities import Entities
from objects.item import Items
from objects.player import Player
from ui.console import Console
from ui.console import Op
from util.logger import logger

from core.events.explore import explore
from core.events.read import read
from core.functions import receive
from core.events.fight import fight
from core.events.rest import rest
from core.events.read import read
from core.events.meditate import meditate
from core.events.run import run
from core.events.search import search
from core.events.trap import trap
from core.events.sneak import sneak
from core.events.encounter import encounter
from core.events.goto import goto
from core.events.haverst import harvest
from core.events.interact import interact
from core.events.investigate import investigate
from core.events.place import place 

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
        self.story = load_yaml_file("data/story.yaml")

        self._chapter_id = "1a" #default value
        self.interface =Layout("des")
        self.in_game = True
        self.love = None
        self.temp_story = None
        self.move_on = True
        self.entity = None
        self.key_listener = None
        self.s = 'options'

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
        story = self.story if self.temp_story == None else self.temp_story
        if value not in story:
            raise ValueError(f"The chapter '{value}' is not defined in the default yaml file. check if defined in yaml")
        self._chapter_id = value


    def execute_yaml_function(self, func: str):
        core = self
        logger.info(f"Executing function: {func}")

        local_scope = {"core": core}  # Define the scope where 'core' is available
        
        try:
            exec(func, globals(), local_scope)
        except Exception as e:
            logger.error(f"Error executing function: {func} - {e} : function exists in yaml file however execution failed mostly likely to the function not defined as  a local or global variable")

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
            if  self.temp_story != None:
                story = self.story
            else:
                story = self.temp_story
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