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
def show_inventory(core):
    core.console.clear_display()

    
    from ui.options import MinimalMenuOption
    menu: List[MinimalMenuOption] = []
    core.console._transtion_layout("INVENTORY")

    core.console.print(menu)
    core.console.layout = "INVENTORY"