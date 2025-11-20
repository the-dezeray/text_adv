from ui.options import VolumeOption
from numpy._core.defchararray import title
from rich.padding import Padding
from PIL.ImageMath import lambda_eval
from typing import TYPE_CHECKING , List
from ui.options import Option
from rich.panel import Panel
from ui.options import MenuOption,Option,MinimalMenuOption,MinimalTextOption, StoryTextOption,MinimalKeyboardOption
from ui.window import window
from ui.menus.keybindings_menu import show_keybindings_menu_options
from ui.menus.languagues import show_language_menu
from ui.menus.api_keys  import show_api_keys_settings
from ui.menus.visuals_options import show_visuals_settings
from ui.menus.clear_data import show_clear_data_menu
if TYPE_CHECKING:
    from ui.console import Console
    from core.core import Core


@window
def show_settings_menu(core):
    console = core.console
    from ui.options import MinimalMenuOption
    list_of_options = {
        "keybindings and shorcuts": lambda: show_keybindings_menu_options(core),
        "language preference": lambda: show_language_menu(core),
        "set api keys": lambda: show_api_keys_settings(core),
        "visuals": lambda: show_visuals_settings(core),
        "clear data": lambda: show_clear_data_menu(core),
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
    menu.append(VolumeOption(
        core=core,
        text="music volume",
        func=lambda: console._transtion_layout("MUSIC"),
        next_node=None,
        type="menu",
        volume_type="music"
    ))
    menu.append(VolumeOption(
        core=core,
        text="efffect volume",
        func=lambda: console._transtion_layout("SOUND"),
        next_node=None,
        type="menu",
        volume_type="sound"
    ))
    console.clear_display()
    core.console.print(menu)