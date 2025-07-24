from ui.options import VolumeOption
from numpy._core.defchararray import title
from rich.padding import Padding
from PIL.ImageMath import lambda_eval
from typing import TYPE_CHECKING , List
from ui.options import Option
from rich.panel import Panel
from ui.options import MenuOption,Option,MinimalMenuOption,MinimalTextOption, StoryTextOption,MinimalKeyboardOption
from ui.window import window
if TYPE_CHECKING:
    from ui.console import Console
    from core.core import Core
def get_user_stories():
    #TODO implement get user stories from path 
    return ["the story of the lost city"," A Lost city","Dying Angel","The dungeaon of death","Solace"," Missing the rage"]
@window
def  generate_load_personal_story_pane(core:"Core"):
        core.console.clear_display()
        instructions: str = "if you find a story place it in the storie files you can even manually type you own story out as long "

        core.console.print(Panel(renderable=instructions))
        core.console.print(
            StoryTextOption(text= "back",func = lambda:core.console.back() )
            )
@window
def transition_to_community_stories(core: "Core"):
 
    console:"Console" = core.console
    from art import text2art
  

    console.table.show_lines = False
    try:
        stories = core.get_community_stories()
    except Exception as e:
        console.clear_display()
        console.print(Panel(renderable=f"Error fetching community stories: {e}", style="red",title="Error"))  
        console.print(Padding("back"))
        return
    if len(stories) == 0:
        console.clear_display()
        console.print(Panel(renderable="No community stories available", style="yellow", title="Community Stories"))
        console.print(Padding("back"))
        return

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
@window
def transition_to_story_select(core):
    console = core.console
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
@window
def generate_new_game_menu_options(core):   
    console:"Console" = core.console
    from art import text2art
  
    # Define menu options with ASCII text1
    
    def ds():   
        if core.ai.setup():
            console._transtion_layout("AI_STUDIO")
    
            console.refresh()
            core.ai.fake_prompt('d')

    list_of_options = {
        "enter the library of stories": lambda: transition_to_story_select(core),
        "community stories": lambda: transition_to_community_stories(core),
        "generate your own story with with ai": lambda: ds(),
        "load a personal story ": lambda: generate_load_personal_story_pane(core),
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
@window
def generate_langnage_menu_options(core):
    console = core.console
    from ui.options import MinimalMenuOption
    def set_language(lang:str):
        if core.set_language(lang)  :
            console.back()
        else:
            
            console.print(Padding("[red]Failed to set language. Please try again later."))
            console.print(MinimalMenuOption(
            text="back  ",
            func=lambda: console.back(),
            next_node=None,
            type="menu"
        ))
    list_of_options = {
        "english": lambda: set_language("english"),
        "french": lambda: set_language("french"),
        "spanish": lambda: set_language("spanish"),
        "back": lambda:console.back(),
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
@window
def generate_settings_menu_options(core):
    console = core.console
    from ui.options import MinimalMenuOption
    list_of_options = {
        "keybindings and shorcuts": lambda: generate_keybindings_menu_options(core),
        "language preference": lambda: generate_langnage_menu_options(core),
        "set api keys": lambda: generate_api_keys_menu_options(core),
        "visuals": lambda: generate_visuals_menu_options(core),
        "clear data": lambda: generate_clear_data_menu_options(core),
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
    menu.append(VolumeOption(
        core=core,
        text="music volume",
        func=lambda: console._transtion_layout("MUSIC"),
        next_node=None,
        type="menu",
        volume_type="music"
    ))
    menu.append(VolumeOption(
        core=core,
        text="efffect volume",
        func=lambda: console._transtion_layout("SOUND"),
        next_node=None,
        type="menu",
        volume_type="sound"
    ))
    console.clear_display()
    core.console.print(menu)
@window
def generate_keybindings_menu_options(core):
    console = core.console
    @window
    def set_key_bindings(core :"Core" = core,key:str = ""):
        core.console.clear_display()
        core.keyboard_controller.refresh_on_key = True
        core.keyboard_controller.setting_key_type = value
        from ui.options import KeyboardStr
        console.print(KeyboardStr(str=322))

        
    list_of_options = {}
    menu: List[MinimalKeyboardOption] = []
    for key,value in core.config["keymaps"].items():
        func = lambda: set_key_bindings(core=core,key=key)

        from readchar import readkey
        from readchar import key as KEY
        map = core.config["keymaps"]
        map = {
            KEY.UP: "up"  # Nerd Font: Arrow Up (nf-md-arrow_up)
            ,KEY.DOWN: "down"  # Nerd Font: Arrow Down (nf-md-arrow_down)
            ,KEY.LEFT: "left"  # Nerd Font: Arrow Left (nf-md-arrow_left)
            ,KEY.RIGHT: "right"  # Nerd Font: Arrow Right (nf-md-arrow_right)
            ,KEY.ENTER: "enter"  # Nerd Font: Enter (nf-md-enter)
            ,KEY.BACKSPACE: "backspace"  # Nerd Font: Backspace (nf-md-backspace)
            ,KEY.ESC: "esc"  # Nerd Font: Escape (nf-md-escape)

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
    #list_of_options["back"] = lambda: core.console.back()

    console.clear_display()
    console.print(menu)
@window
def generate_api_keys_menu_options(core):
    console = core.console
    from ui.options import MinimalMenuOption
    list_of_options = {
        "api keys": lambda: print("d"),
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
    core.console.print(menu)
@window
def generate_visuals_menu_options(core):
    console = core.console
    from ui.options import MinimalMenuOption
    list_of_options = {
        
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
    console.print(Padding("[cyan1]Visuals settings will be here soon![/cyan1]"))
    core.console.print(menu)
@window
def generate_about_us_menu_options(core: "Core"):

    from ui.options import MinimalMenuOption
    list_of_options = {
        "sponsor project": lambda: generate_about_us_menu_options(core),
        "more about me ": lambda: generate_about_us_menu_options(core),
        "back": lambda: core.console.back() ,
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
@window
def generate_clear_data_menu_options(core):
    console = core.console
    from ui.options import MinimalMenuOption
    def attempt_delete():
        core.console.clear_display()
        console.print(Padding("Clearing all data..."))
        if core.clear_data():
            console.print(Padding("[green]All data cleared successfully!"))
            console.print(MinimalMenuOption(
            text="back  ",
            func=lambda: console.back(),
            next_node=None,
            type="menu"
        ))
        else:
            console.print(Padding("[red]Failed to clear data. Please try again later."))    
            console.print(MinimalMenuOption(
            text="back  ",
            func=lambda: console.back(),
            next_node=None,
            type="menu"
        ))
        
    list_of_options = {
        "yes": lambda: attempt_delete(),
        "no": lambda:console.back(),
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
    from rich.style import Style
    from rich.panel import Panel
    style = Style( color="white")
    console.print(Panel("Are you sure you want to clear all data?",border_style = "red1", style=style))
    core.console.print(menu)

@window
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
def generate_inventory_menu(core):
    player = core.player
    console = core.console
@window
def generate_main_menu_options(core: "Core"):
    console = core.console
    from art import text2art
    
    from ui.options import MenuOption,Option,MinimalMenuOption
    # Define menu options with ASCII text
    core.console._transtion_layout("MENU")
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
    console.clear_display()

    console.print(menu)
def generate_previous_menu_options(core:"Core")->None:
    if core.current_pane:
        core.console.clear_display()
        core.current_pane()


