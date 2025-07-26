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
def  show_personal_story_instructions(core:"Core"):
        core.console.clear_display()
        instructions: str = "if you find a story place it in the storie files you can even manually type you own story out as long "

        core.console.print(Panel(renderable=instructions))
        core.console.print(
            StoryTextOption(text= "back",func = lambda:core.console.back() )
            )
