from PIL.ImageMath import lambda_eval
from typing import TYPE_CHECKING , List
if TYPE_CHECKING:
    from ui.console import Console
def get_user_stories():
    #TODO implement get user stories from path 
    return ["story 1","story 2","story 3","story 132","story 232","story 323"]
def generate_new_game_menu_options(core):   
    console:"Console" = core.console
    from art import text2art
    from ui.options import MenuOption,Option,MinimalMenuOption,MinimalTextOption
    # Define menu options with ASCII text
    def transition_to_story_select(console:"Console"):
        console._transtion_layout("SELECTSTORY")
        stories = get_user_stories()
        items = []
        for story in stories:
            items.append(MinimalTextOption(
                text=story,
                func=lambda: console._transtion_layout("INGAME"),
                next_node=None,
                type="menu"
            ))
        console.clear_display()
        core.console.print(items)
    def ds():   
        console._transtion_layout("AI_STUDIO")
    
        console.refresh()
        core.ai.fake_prompt('d')
    list_of_options = {
        "enter the library of stories": lambda: transition_to_story_select(console),
        "generate your own story with with ai": lambda: ds(),
        "load a personal story ": lambda: console.TERMINATE(),
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
def generate_settings_menu_options(core):
    console = core.console
    from ui.options import MinimalMenuOption
    list_of_options = {
        "keybindings and shorcuts": lambda: generate_keybindings_menu_options(core),
        "language preference": lambda: console._transtion_layout("LANGUAGE"),
        "set api keys": lambda: generate_api_keys_menu_options(core),
        "visuals": lambda: generate_visuals_menu_options(core),
        "clear data": lambda: generate_clear_data_menu_options(core),
        "back": lambda: console._transtion_layout("CREDITS"),
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
        "shorcuts": lambda: console._transtion_layout("MENU"),
    }

def generate_api_keys_menu_options(core):
    console = core
    from ui.options import MinimalMenuOption
    list_of_options = {
        "api keys": lambda: console._transtion_layout("MENU"),
    }
    menu: List[MinimalMenuOption] = []
    for key,value in list_of_options.items():
        menu.append(MinimalMenuOption(
            text=key,
            func=value,
            next_node=None,
            type="menu"
        ))
def generate_visuals_menu_options(core):
    console = core.console
    from ui.options import MinimalMenuOption
    list_of_options = {
        "visuals": lambda: console._transtion_layout("MENU"),
    }
    menu: List[MinimalMenuOption] = []
    for key,value in list_of_options.items():
        menu.append(MinimalMenuOption(
            text=key,
            func=value,
            next_node=None,
            type="menu"
        ))
def generate_about_us_menu_options(core):
    console = core.console
    from ui.options import MinimalMenuOption
    list_of_options = {
        "about us": lambda: console._transtion_layout("MENU"),
    }
    menu: List[MinimalMenuOption] = []
    for key,value in list_of_options.items():
        menu.append(MinimalMenuOption(
            text=key,
            func=value,
            next_node=None,
            type="menu"
        ))
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
def generate_main_menu_options(core):
    console = core.console
    from art import text2art
    from ui.options import MenuOption,Option,MinimalMenuOption
    # Define menu options with ASCII text

    List_of_options = {
        "continue": lambda: console._transtion_layout("INGAME"),
        "new game": lambda: generate_new_game_menu_options(core),
        "settings": lambda: generate_settings_menu_options(core),
        "about us": lambda: generate_about_us_menu_options(core),
        "leave": lambda: console.TERMINATE(),
    }
    menu: List[MinimalMenuOption] =[]
    for key,value in  List_of_options.items():
        menu.append(MinimalMenuOption(
            text=key,
            func=value,
            next_node=None,
            type="menu"
        ))
    return menu
   