from PIL.ImageMath import lambda_eval
from typing import TYPE_CHECKING , List
from ui.options import Option
from rich.panel import Panel
from ui.options import MenuOption,Option,MinimalMenuOption,MinimalTextOption, StoryTextOption
if TYPE_CHECKING:
    from ui.console import Console
    from core.core import Core
def get_user_stories():
    #TODO implement get user stories from path 
    return ["the story of the lost city"," A Lost city","Dying Angel","The dungeaon of death","Solace"," Missing the rage"]
def  generate_load_personal_story_pane(core:"Core"):
        core.console.clear_display()
        instructions: str = "if you find a story place it in the storie files you can even manually type you own story out as long "

        core.console.print(Panel(renderable=instructions))
        core.console.print(
            StoryTextOption(text= "back",func = lambda:generate_previous_menu_options(core) )
            )
        
def generate_new_game_menu_options(core):   
    console:"Console" = core.console
    from art import text2art
  
    # Define menu options with ASCII text
    def transition_to_story_select(console:"Console"):
        console.table.show_lines = False
    
        stories = get_user_stories()
        menu = []
        for story in stories:
            menu.append(StoryTextOption(
                text=story,
                func=lambda: console._transtion_layout("INGAME"),
                next_node=None,
                type="menu"
            ))
        console.clear_display()
        menu[0].selected = True
        core.console.print(menu)
    def ds():   
        console._transtion_layout("AI_STUDIO")
    
        console.refresh()
        core.ai.fake_prompt('d')

    list_of_options = {
        "enter the library of stories": lambda: transition_to_story_select(console),
        "generate your own story with with ai": lambda: ds(),
        "load a personal story ": lambda: generate_load_personal_story_pane(core),
           "back": lambda: generate_previous_menu_options(core),
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
def generate_settings_menu_options(core):
    console = core.console
    from ui.options import MinimalMenuOption
    list_of_options = {
        "keybindings and shorcuts": lambda: generate_keybindings_menu_options(core),
        "language preference": lambda: console._transtion_layout("LANGUAGE"),
        "set api keys": lambda: generate_api_keys_menu_options(core),
        "visuals": lambda: generate_visuals_menu_options(core),
        "clear data": lambda: generate_clear_data_menu_options(core),
        "back": lambda: generate_previous_menu_options(core),
    }
    menu: List[MinimalMenuOption] = []
    for key,value in list_of_options.items():
        menu.append(MinimalMenuOption(
            text=key,
            func=value,
            next_node=None,
            type="menu"
        ))
    menu.append(MinimalMenuOption(
        text="sound volume",
        func=lambda: console._transtion_layout("MUSIC"),
        next_node=None,
        type="menu"
    ))
    menu.append(MinimalMenuOption(
        text="efffect volume",
        func=lambda: console._transtion_layout("SOUND"),
        next_node=None,
        type="menu"
    ))
    console.clear_display()
    core.console.print(menu)
def generate_keybindings_menu_options(core):
    console = core.console
    from ui.options import MinimalMenuOption
    list_of_options = {
        "keybindings": lambda: console._transtion_layout("MENU"),
           "back": lambda: generate_previous_menu_options(core),
        "shorcuts": lambda: console._transtion_layout("MENU"),
    }

def generate_api_keys_menu_options(core):
    console = core.console
    from ui.options import MinimalMenuOption
    list_of_options = {
        "api keys": lambda: print("d"),
           "back": lambda: generate_previous_menu_options(core),
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
    core.console.print(menu)
def generate_visuals_menu_options(core):
    console = core.console
    from ui.options import MinimalMenuOption
    list_of_options = {
        "visuals": lambda: console._transtion_layout("MENU"),
           "back": lambda: generate_previous_menu_options(core),
    }
    menu: List[MinimalMenuOption] = []
    for key,value in list_of_options.items():
        menu.append(MinimalMenuOption(
            text=key,
            func=value,
            next_node=None,
            type="menu"
        ))
def generate_about_us_menu_options(core: "Core"):

    from ui.options import MinimalMenuOption
    list_of_options = {
        "sponsor project": lambda: generate_about_us_menu_options(core),
        "more about me ": lambda: generate_about_us_menu_options(core),
        "back": lambda: generate_previous_menu_options(core),
    }
    menu: List[MinimalMenuOption] = []
    for key,value in list_of_options.items():
        menu.append(MinimalMenuOption(
            text=key,
            func=value,
            next_node=None,
            type="menu"
        ))
    
    about_me_text  = "I am desiree creator of this project feel free to by me a coffe PS:saving to get a decent laptop"
    core.console._transtion_layout("ABOUT_US")
    core.console.clear_display()
    core.console.print(Panel("image to be rended"))
    core.console.print(Panel(about_me_text))
    core.console.print(menu)
def generate_clear_data_menu_options(core):
    console = core.console
    from ui.options import MinimalMenuOption
    list_of_options = {
        "clear data": lambda: console._transtion_layout("MENU"),
    }
    menu: List[MinimalMenuOption] = []
    for key,value in list_of_options.items():
        menu.append(MinimalMenuOption(
            text=key,
            func=value,
            next_node=None,
            type="menu"
        ))
def generate_main_menu_options(core: "Core"):
    console = core.console
    from art import text2art
    
    from ui.options import MenuOption,Option,MinimalMenuOption
    # Define menu options with ASCII text

    List_of_options = {
        "continue": lambda: console._transtion_layout("INGAME"),
        "new game": lambda: generate_new_game_menu_options(core),
        "settings": lambda: generate_settings_menu_options(core),
        "about us": lambda: generate_about_us_menu_options(core),
        "leave": lambda: core.TERMINATE(),
    }
    if not core.saved_game:
        del List_of_options["continue"]
    menu: List[MinimalMenuOption] =[]
    for key,value in  List_of_options.items():
        menu.append(MinimalMenuOption(
            text=key,
            func=value,
            next_node=None,
            type="menu"
        ))
    menu[0].selected = True
    return menu
def generate_previous_menu_options(core:"Core")->None:
    if core.current_pane:
        core.console.clear_display()
        core.current_pane()
    