'''core of the game'''
'''random temp comment'''
import datetime
import sys

from util.file_handler import load_yaml_file
from ui.options import Option ,Choices
from rich.layout import Layout
from objects.entities import Entities
from objects.item import Items
from objects.player import Player
from ui.console import Console
from ui.console import Op

from util.logger import logger
from core.events.navigate import navigate
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
from core.events.shop import shop
from core.events.search_in import search_in

from rich.padding import Padding
from rich.panel import Panel
def _dialogue_text(text, style) -> Padding:
    return Padding(Panel(text,border_style=style), pad=(2, 0, 0, 0))
            
class Core():
    def __init__(self) -> None:
        self.rich_console = None
        self.running = True
        self.ant =[]
        self.in_fight = False
        self.story = load_yaml_file("data/story.yaml")
        self._chapter_id = -1 #default value
 
        self.in_game = True
        self.rich_live_instance = None
        self.temp_story = None
        self.move_on = True
        self.entity = None
        self.key_listener = None
        self.s = 'options'
        self.selected_option = 0
        self.others = []
        self._layout = Layout()
        self.player = Player()
        self.player_turn = False
        self.next_node = None
        self.options = []
        self.console = Console(core = self)
        self._post_initialize()
        
    def exit():
        sys.exit()
    def _post_initialize(self):
        current_time = datetime.datetime.now()
        logger.info(f"New game instance {current_time}")
        self.check_story()

    def check_story(self):
        print("Checking story")

    @property
    def chapter_id(self):
        return self._chapter_id
    @chapter_id.getter
    def chapter_id(self):
        return self._chapter_id
    @chapter_id.setter
    def chapter_id(self,value):
        story = self.story if self.temp_story == None else self.temp_story
        if value == "-1"or value == -1:
            value = -1
        elif value not in story:
            logger.critical(f"The chapter '{value}' is not defined in the default yaml file. check if defined in yaml")
            raise ValueError(f"The chapter '{value}' is not defined in the default yaml file. check if defined in yaml")

        self._chapter_id = value

    def execute_yaml_function(self, func: str):
        core = self
        logger.info(f"Executing function: {func}")
        local_scope = {"core": core}  # Define the scope where 'core' is available
        try:
            exec(func, globals(), local_scope)
        except Exception as e:
            logger.error(f"chapter : {self.chapter_id}")
            logger.error(f"Error executing function: {func} - {e} : function exists in yaml file however execution failed mostly likely to the function not defined as  a local or global variable")

    def clean(self):
        self.chapter_id = "1a"
        self.console.layout = "INGAME"
    def TERMINATE(self):
        self.running = False
        self.console.options = []
        quit()


        self.continue_game()
    def continue_game(self):
        #set the selected option to 0
        self.selected_option = 0
        if self.chapter_id == -1:
            self.console.layout =  "CHARACTER_SELECTION"
        
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
        self.console.refresh()

    def goto_next(self)->None:
        '''Go to the next node in the story'''
        logger.info("Going to next node")

        self.chapter_id = self.next_node
        self.continue_game()
    def clear_logs():
        ...
    def restart():
        ...
    def raw_exec():
        ...