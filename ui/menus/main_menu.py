from ui.options import VolumeOption
from numpy._core.defchararray import title
from rich.padding import Padding
from PIL.ImageMath import lambda_eval
from typing import TYPE_CHECKING , List
from ui.options import Option
from rich.panel import Panel
from ui.options import MenuOption,Option,MinimalMenuOption,MinimalTextOption, StoryTextOption,MinimalKeyboardOption
from ui.window import window
from ui.menus.continue_menu import show_continue_menu
from ui.menus.new_game import show_new_game_menu
from ui.menus.settings import show_settings_menu
from ui.menus.about_us import show_about_us_menu
if TYPE_CHECKING:
    from ui.console import Console
    from core.core import Core


@window
def show_main_menu(core: "Core"):
    console = core.console
    from art import text2art
    
    from ui.options import MenuOption,Option,MinimalMenuOption
    # Define menu options with ASCII text
    from ui.layouts.factory import LayoutType
    core.console._transtion_layout(LayoutType.MENU)
    List_of_options = {
        "continue": lambda: show_continue_menu(core),
        "new game": lambda: show_new_game_menu(core),
        "settings": lambda: show_settings_menu(core),
        "about us": lambda: show_about_us_menu(core),
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