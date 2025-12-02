from rich.layout import Layout
from terma.ui.options import VolumeOption
from numpy._core.defchararray import title
from rich.padding import Padding
from PIL.ImageMath import lambda_eval
from typing import TYPE_CHECKING , List
from terma.ui.options import Option
from terma.ui.layouts.factory import LayoutType
from rich.panel import Panel
from terma.ui.options import MenuOption,Option,MinimalMenuOption,MinimalTextOption, StoryTextOption,MinimalKeyboardOption
from terma.ui.window import window
from terma.core.story import get_user_stories
if TYPE_CHECKING:
    from terma.ui.console import Console
    from terma.core.core import Core



@window
def show_story_selection_menu(core):
    console = core.console
    console.table.show_lines = False

    stories = get_user_stories()
    menu = []
    for story in stories:
        menu.append(StoryTextOption(
            text=story,
            func=lambda: console._transtion_layout(LayoutType.MENU),
            next_node=None,
            type="menu"
        ))
    console.clear_display()
    menu[0].selected = True
    core.console.print(menu)
