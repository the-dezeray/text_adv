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
def show_keybindings_menu_options(core):
    console = core.console
    @window
    def set_key_bindings(core :"Core" = core,key:str = ""):
        core.console.clear_display()
        core.keyboard_controller.refresh_on_key = True
        core.keyboard_controller.setting_key_type = value
        from ui.options import KeyboardStr
        console.print(KeyboardStr(str=322))

        
    list_of_options = {}
    menu: List[MinimalKeyboardOption] = []
    for key,value in core.config["keymaps"].items():
        func = lambda: set_key_bindings(core=core,key=key)

        from readchar import readkey
        from readchar import key as KEY
        map = core.config["keymaps"]
        map = {
            KEY.UP: "up"  # Nerd Font: Arrow Up (nf-md-arrow_up)
            ,KEY.DOWN: "down"  # Nerd Font: Arrow Down (nf-md-arrow_down)
            ,KEY.LEFT: "left"  # Nerd Font: Arrow Left (nf-md-arrow_left)
            ,KEY.RIGHT: "right"  # Nerd Font: Arrow Right (nf-md-arrow_right)
            ,KEY.ENTER: "enter"  # Nerd Font: Enter (nf-md-enter)
            ,KEY.BACKSPACE: "backspace"  # Nerd Font: Backspace (nf-md-backspace)
            ,KEY.ESC: "esc"  # Nerd Font: Escape (nf-md-escape)

        }
        if value in map:
            value = map[value]
        menu.append(MinimalKeyboardOption(
            text=key,
            func=func,
            next_node=None,
            key=value,
            type="menu"
        ))
    #list_of_options["back"] = lambda: core.console.back()

    console.clear_display()
    console.print(menu)