from ui.options import VolumeOption
from numpy._core.defchararray import title
from rich.padding import Padding
from PIL.ImageMath import lambda_eval
from typing import TYPE_CHECKING , List
from ui.options import Option
from rich.panel import Panel
from ui.options import MenuOption,Option,MinimalMenuOption,MinimalTextOption, StoryTextOption,MinimalKeyboardOption
from ui.window import window
from ui.menus.select_stories import  show_story_selection_menu
from ui.menus.community_stories import show_community_stories
from ui.menus.personal_story import  show_personal_story_instructions
if TYPE_CHECKING:
    from ui.console import Console
    from core.core import Core


@window
def show_new_game_menu(core):   
    console:"Console" = core.console
    from art import text2art
  
    # Define menu options with ASCII text1
    
    def ds():   
        if core.ai.setup():
            console._transtion_layout("AI_STUDIO")
    
            console.refresh()
            core.ai.fake_prompt('d')

    list_of_options = {
        "enter the library of stories": lambda: show_story_selection_menu(core),
        "community stories": lambda: show_community_stories(core),
        "generate your own story with with ai": lambda: ds(),
        "load a personal story ": lambda: show_personal_story_instructions(core),
           "back": lambda: core.console.back(),
    }
    menu: List[MinimalMenuOption] = []
    for key,value in list_of_options.items():
        menu.append(MinimalMenuOption(
            text=key,
            func=value,
            next_node=None,
            type="menu"
        ))


    console.clear_display()
    menu[0].selected = True
    core.console.print(menu)
