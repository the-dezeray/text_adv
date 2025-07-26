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
def show_community_stories(core: "Core"):
 
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

