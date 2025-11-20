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
def show_clear_data_menu(core):
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