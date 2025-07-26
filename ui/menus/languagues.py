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


@window
def show_language_menu(core):
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