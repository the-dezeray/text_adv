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

def link(link:str):
    ...
@window
def show_about_us_menu(core: "Core"):

    from ui.options import MinimalMenuOption
    list_of_options = {
        "sponsor project": lambda:link("https://ko-fi.com/desiree"),
        "more about me ": lambda: link("https://www.dezeray.me"),
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