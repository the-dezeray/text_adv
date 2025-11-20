from terma.ui.options import VolumeOption
from numpy._core.defchararray import title
from rich.padding import Padding
from PIL.ImageMath import lambda_eval
from typing import TYPE_CHECKING , List
from terma.ui.options import Option
from rich.panel import Panel
from terma.ui.options import MenuOption,Option,MinimalMenuOption,MinimalTextOption, StoryTextOption,MinimalKeyboardOption
from terma.ui.window import window
if TYPE_CHECKING:
    from terma.ui.console import Console
    from terma.core.core import Core



@window
def show_visuals_settings(core):
    console = core.console
    from terma.ui.options import MinimalMenuOption
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