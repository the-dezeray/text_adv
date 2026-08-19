from terma.ui.options import VolumeOption
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
def show_help(core):
    core.console.clear_display()
    from terma.ui.options import MinimalMenuOption
    menu: List[MinimalMenuOption] = []
    core.console._transtion_layout("INVENTORY")
    
    core.console.print(menu)
    core.console.layout = "INVENTORY"
