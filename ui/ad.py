from rich.padding import Padding
from PIL.ImageMath import lambda_eval
from typing import TYPE_CHECKING , List
from ui.options import Option
from rich.panel import Panel
from ui.options import MenuOption,Option,MinimalMenuOption,MinimalTextOption, StoryTextOption,MinimalKeyboardOption
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
        if core.ai.setup():
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
    def set_key_bindings(core = core,key:str = ""):
        core.console.clear_display()
        core.console.print(Panel(width=40,renderable = "",style="cyan1",subtitle=f"set key binding for {key}"))
      
        core.config["keymaps"]
    list_of_options = {}
    menu: List[MinimalKeyboardOption] = []
    for key,value in core.config["keymaps"].items():
        func = lambda: set_key_bindings(core=core,key=key)

        from readchar import readkey
        from readchar import key as KEY

        map = {
            KEY.UP: "󰁝  up"  # Nerd Font: Arrow Up (nf-md-arrow_up)
            ,KEY.DOWN: "󰁞 down"  # Nerd Font: Arrow Down (nf-md-arrow_down)
            ,KEY.LEFT: "󰁜 left"  # Nerd Font: Arrow Left (nf-md-arrow_left)
            ,KEY.RIGHT: "󰁟 right"  # Nerd Font: Arrow Right (nf-md-arrow_right)
            ,KEY.ENTER: "󰁠 enter"  # Nerd Font: Enter (nf-md-enter)
            ,KEY.BACKSPACE: "󰁡 backspace"  # Nerd Font: Backspace (nf-md-backspace)
            ,KEY.ESC: "󰁢 esc"  # Nerd Font: Escape (nf-md-escape)

        }
        if value in map:
            value = map[value]
        menu.append(MinimalKeyboardOption(
            text=key,
            func=func,
            next_node=None,
            key=value,
            type="menu"
        ))
    #list_of_options["back"] = lambda: generate_previous_menu_options(core)

    console.clear_display()
    console.print(menu)

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

def genereate_continue_game_menu_options(core: "Core"):

    console = core.console
    from ui.options import MinimalMenuOption
    list_of_options = {

    }
    
    menu: List[MinimalMenuOption] = []
    from core.atypes import Story
    stories: list[Story] =core.config["current_stories"]
    def load_and_play_story(story:Story)->None:
        core.game_engine.load_story(story)
        core.menu = False
        core.console._transtion_layout("INGAME")
    for story in stories:
        import datetime
        last_accessed = story.get("last_accessed", 0)
        last_accessed_time = datetime.datetime.fromtimestamp(last_accessed)
        menu.append(MinimalMenuOption(
            text=f"{story["id"]}               [red]{last_accessed_time}[/red]",
            func=lambda: load_and_play_story(story),
            next_node=None,
            type="menu"
        ))
        console.clear_display()
        console.print(menu)
def generate_main_menu_options(core: "Core"):
    console = core.console
    from art import text2art
    
    from ui.options import MenuOption,Option,MinimalMenuOption
    # Define menu options with ASCII text

    List_of_options = {
        "continue": lambda: genereate_continue_game_menu_options(core),
        "new game": lambda: generate_new_game_menu_options(core),
        "settings": lambda: generate_settings_menu_options(core),
        "about us": lambda: generate_about_us_menu_options(core),
        "leave": lambda: core.TERMINATE(),
    }
    if not core.config["current_stories"]:
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
    