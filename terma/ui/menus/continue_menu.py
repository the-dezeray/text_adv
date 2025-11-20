from terma.ui.options import VolumeOption
from numpy._core.defchararray import title
from rich.padding import Padding
from PIL.ImageMath import lambda_eval
from typing import TYPE_CHECKING , List
from terma.ui.options import Option
from rich.panel import Panel
from terma.ui.options import MenuOption,Option,MinimalMenuOption,MinimalTextOption, StoryTextOption,MinimalKeyboardOption
from terma.ui.window import window
from terma.core.atypes import Story
if TYPE_CHECKING:
    from terma.ui.console import Console
    from terma.core.core import Core


@window
def show_continue_menu(core: "Core"):

    console = core.console
    from terma.ui.options import MinimalMenuOption
    list_of_options = {}
    
    menu: List[MinimalMenuOption] = []
   
    stories: list[Story] =core.config["current_stories"]
    def load_and_play_story(save:Story)->None:
        core.game_engine.load_save(save)
        core.menu = False
        core.console._transtion_layout("INGAME")
    for story in stories:
        import datetime
        last_accessed = story.get("last_accessed", 0)
        last_accessed_time = datetime.datetime.fromtimestamp(last_accessed)
        menu.append(MinimalMenuOption(
            text=f"{story["id"]}               [red]{last_accessed_time}[/red]",
            func=lambda: load_and_play_story(story),
            next_node=None,
            type="menu"
        ))
        console.clear_display()
        console.print(menu)