
from PIL.PngImagePlugin import logger
from gc import disable
from typing import Callable, Optional, Literal, TYPE_CHECKING
from rich.padding import Padding
from rich.panel import Panel
from rich.table import Table
from rich.align import Align
from rich.layout import Layout
from rich.text import Text
import time
from typing import Generator,Union
from rich.console import ConsoleRenderable
from dataclasses import dataclass, field
from typing import Callable, Optional, Literal, Any


if TYPE_CHECKING:
    from core.core import Core
    from objects.weapon import Weapon


def yy():
    """Placeholder function"""
    pass

@dataclass
class RenderConfig:
    """Configuration for rendering UI components."""
    style: str = ""
    left_padding: int = 0
    top_padding: int = 0
    right_padding: int = 0
    bottom_padding: int = 0
    width: Optional[int] = None
    height: Optional[int] = None



def default_on_select():
    pass  # Your fallback action


AlignMethod = Literal["left", "center", "right"]
VerticalAlign = Literal["top", "middle", "bottom"]

@dataclass
class CustomRenderable:
    text: str = ""
    disable_others: bool = True
    func: Optional[Callable[[], Any]] = None
    preview: Optional[Callable[[], Any]] = None
    next_node: Optional[str] = None
    selectable: bool = True
    sound: str = ""
    type: str = ""
    h_allign: AlignMethod = "center"
    v_allign: VerticalAlign = "middle"
    on_select: Callable[[], Any] = field(default_factory=lambda: default_on_select)
    core: Optional["Core"] = None

    # These are excluded from __init__, set internally
    left_padding: int = field(default=0, init=False)
    style: str = field(default="", init=False)
    _selected: bool = field(default=False, init=False)

    @property
    def selected(self) -> bool:
        return self._selected

    @selected.setter
    def selected(self, value: bool) -> None:

        self._selected = value
        # Trigger preview only if selected, preview function exists, and core is available
        if self._selected and self.preview and self.core and self.core.console:
            self.preview()
            self.core.console.refresh() # Refresh console to show preview

    def render(self, config: RenderConfig) -> ConsoleRenderable:
        raise NotImplementedError("Subclasses must implement the render method.")


def CHOICE(core,data):
                   return Option(     text=data.get("text", "Missing text"),
                    func=data.get("function"),
                    next_node=data.get("next_node"),
                    selectable=True,
                    sound=data.get("sound", ""))
def WEAPON(core,data):
    """Creates a weapon option from provided data."""
    from core.events.fight import deal_damage # Local import to prevent circular dependency
    weapon = data
    return create_weapon_option(
                    name=weapon.name,
                    # Pass the specific weapon to deal_damage
                    func=lambda w=weapon: deal_damage(core, w),
                    preview=core.console.show_weapon ,
                    core=core
    )
def WEAPON2(core,data):
    """Creates a weapon option from provided data."""
    from core.events.fight import deal_damage # Local import to prevent circular dependency
    weapon = data
    return create_mini_weapon_option(
                    weapon=weapon,
                    # Pass the specific weapon to deal_damage
                    func=lambda w=weapon: core.player.inventory.add( w),
                    preview=core.console.show_weapon ,
                    core=core
    )    
            
class GRID():
    """Creates a buffer for displaying generic choice options."""
    def __init__(
        self,
        core =None,
        renderItem: Callable= CHOICE,
        ary: list[dict] = [], # Expects a list of dictionaries
        title: str = "",
        extra: bool = False,
        icon: str = "" # Icon parameter seems unused in render
    ):

        self.raw_choices = ary 
        from typing import Literal
        self.h_allign :AlignMethod = 'left'
        self.title = title
        self.weapons = ary or []
        self.extra=extra
        self.renderItem = renderItem
        self.selectable = True # Buffer contains selectable items
        self.core = core
        self.ary = self._build_choice_options() # Store generated CustomRenderable objects

    def _build_choice_options(self) -> list["Option"]:
        """Builds a list of Option options from the choice data."""
        options_list = []
        for data in self.raw_choices:
            # Create a Option option for each dictionary in the list
            options_list.append(
                self.renderItem(core=self.core ,data=data)
            )
        return options_list

    def render(self, core: Optional["Core"] = None) -> Table:
        """
        Renders the list of choice options within a grid.

        Args:
            core (Optional["Core"]): Reference to the core object. Defaults to None.

        Returns:
            Table: A Table (grid) containing the rendered choice options.
        """
        renderables = [option.render() for option in self.ary]

        grid = create_grid(colomuns=1)
        for r in renderables:
            grid.add_row(r)
        return grid




def create_grid(colomuns: int = 1) -> Table:

    grid = Table.grid(expand=True) # Expand grid to fill available space
    for _ in range(colomuns):
        grid.add_column()
    return grid


def ui_text_panel(option: Optional[CustomRenderable] = None, text: str = "") -> Padding:

    display_text = text
    style = "" # Default style

    if not display_text:
        if option:
            display_text = option.text
            if option.selected:
                style = "bold green"
                # Preview is handled by the CustomRenderable's selected setter, not here.
        else:
            # Raise error if there's nothing to display
            raise ValueError("ui_text_panel requires either an 'option' or 'text'.")

    # Return text wrapped in Padding, potentially with a style
    return Padding(display_text, style=style)
class WeaponOption(CustomRenderable):
    """UI representation for a weapon option."""
    def __init__(self, **kwargs):
        """Initializes a weapon UI element, forwarding arguments to CustomRenderable."""
        super().__init__(**kwargs)
        self.type  : str = "weapon" # Ensure type is set

    def render(self, style: str = "", left_padding: int = 0, core: Optional["Core"] = None) -> ConsoleRenderable:
        # Use a Unicode arrow or similar indicator
        indicator = "\uf0da" # Example: Right-pointing arrow
        display_text = f"{indicator} {self.text} "
        style = "dim green"
        if self.selected:
            style = "bold green" # Internal style tracking
            # Preview is handled by the setter
            return Panel(display_text, style=style, expand=False) # Wrap selected in Panel
        else:
            style = "dim green" # Internal style tracking
            # Non-selected items are padded Text
            return Padding(Text(display_text, style=style), (0, 0, 0, 0)) # No extra padding here

class MiniWeaponOption(CustomRenderable):
    """UI representation for a weapon option."""
    def __init__(self, **kwargs):
        """Initializes a weapon UI element, forwarding arguments to CustomRenderable."""
        super().__init__(**kwargs)
        self.type  : str = "weapon" # Ensure type is set

    def render(self, style: str = "", left_padding: int = 0, core: Optional["Core"] = None) -> ConsoleRenderable:

        indicator = "\uf0da" 
        display_text = f"{indicator} {self.text} "
        from rich.style import Style
        style = "dim green"
        if self.selected:
            style = "bold green" # Internal style tracking
            style = Style(bgcolor="green",color="black")
        else:
            style = "dim green" # Internal style tracking
        return Padding(display_text, style=style,expand=True) # No extra padding here






def create_weapon_option(
    name: "Weapon",
    func: Callable,
    preview: Optional[Callable] = None,
    core: Optional["Core"] = None
) -> "WeaponOption":
    return WeaponOption(
        text=name,
        func=func,
        selectable=True,
        type="weapon", # Set type explicitly
        preview=preview,
        core=core
    )
def create_mini_weapon_option(
    weapon: "Weapon",
    func: Callable,
    preview: Optional[Callable] = None,
    core: Optional["Core"] = None
) -> "MiniWeaponOption":

    return MiniWeaponOption(
        text=f"{weapon.name}                        [red]{weapon.damage}[/red] [cyan]{weapon.defence}[/cyan]  {weapon.rarity} {weapon.condition})",
        func=func,
        selectable=True,
        type="weapon", # Set type explicitly
        preview=preview,
        core=core
    )


def new_ui_button(
    option: CustomRenderable,
    # style: str = "", # Style is determined by selection state
    # selected: bool = False, # Selection is determined by option.selected
    top_padding: int = 0,
    right_padding: int = 0,
    bottom_padding: int = 0,
    left_padding: int = 0, # This seems overridden based on selection state
) -> Padding:

    button_height = 3
    current_left_padding = left_padding # Use the provided base padding
    border_style = "" # Default border style

    if option.selected:
        border_style = "bold green" # Highlight border when selected
        current_left_padding += 5 # Indent when selected
        # Preview is handled by the CustomRenderable's selected setter, not here.

    # Create the Panel for the button appearance
    button_panel = Panel(
        Align.center(option.text), # Center text inside the panel
        width=15,
        height=button_height,
        border_style=border_style
    )

    # Wrap the panel in Padding
    return Padding(
        button_panel,
        pad=(top_padding, right_padding, bottom_padding, current_left_padding),
    )

# --- Placeholder/Utility Functions ---

def load_shop():
    """Placeholder function for loading shop data or UI."""
    print("DEBUG: load_shop called")
    pass



def Loader() -> Padding:
    return Padding(Panel("Loading..."), pad=(2, 4, 0, 4), expand=False)


def Reward(ary: list[str] = []) -> Panel:

    rewards = ary or []
    grid = Table.grid(expand=True) # Use a grid to list rewards
    grid.add_column()
    for reward_text in rewards:
        grid.add_row(Text(reward_text, style="yellow")) # Style rewards text
    return Panel(grid, title="[bold green]Rewards![/bold green]", expand=False)
class Option(CustomRenderable):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    def render(self, style: str =   "", left_padding: int = 0, core: Optional["Core"] = None) -> ConsoleRenderable:
        indicator = "\uf0da"
        display_text = f"{indicator} {self.text} "
        style :str = "dim green"
        if self.selected:
            style = "bold green"
            # Preview handled by setter
            return Panel(display_text, style=style, expand=False)
        else:
            style = "dim green"
             # Add space before indicator for alignment?
            return Padding(Text(f" {display_text}", style=style), (0, 0, 0, 0))

# --- Placeholder Functions (Likely for future implementation) ---

def shop():
    """Placeholder function for shop interaction."""
    print("DEBUG: shop called")
    pass

def card():
    """Placeholder function for card-related actions."""
    print("DEBUG: card called")
    pass

def sound():
    """Placeholder function for sound control."""
    print("DEBUG: sound called")
    pass

def long_button():
    """Placeholder function for a different button type."""
    print("DEBUG: long_button called")
    pass

def lister():
    """Placeholder function for a listing mechanism."""
    print("DEBUG: lister called")
    pass

def inventory_button():
    """Placeholder function for an inventory button."""
    print("DEBUG: inventory_button called")
    pass


# --- CustomRenderable Subclasses ---





class MenuOption(CustomRenderable):
    def __init__(self, **kwargs):
        if 'h_allign' not in kwargs:
            kwargs['h_allign'] = "left"
        super().__init__(**kwargs)
        self.type = "menu" # Ensure type is set

    def render(self, style: str = "", left_padding: int = 0, core: Optional["Core"] = None) -> ConsoleRenderable:

        ctext = self.text # Example font

        style = "dim grey93"
        if self.selected:
            style = "bold green"
            core.console.current_layout.layout["right"].update(Panel("new selection"))
            ctext = "> " + self.text
        else:
            style = "dim grey93" #
        return Panel(Align.center(f"[{style}]{ctext}[/{style}]"), width=20)

class MinimalMenuOption(CustomRenderable):
    def __init__(self, **kwargs):
        if 'h_allign' not in kwargs:
            kwargs['h_allign'] = "left"
        super().__init__(**kwargs)
        self.type = "menu" # Ensure type is set

    def render(self, style: str = "", left_padding: int = 0, core: Optional["Core"] = None) -> ConsoleRenderable:

        ctext = self.text # Example font

        style = "dim grey93"
        if self.selected:
            style = "bold green"
        
            core.console.current_layout.layout["right"].update(Panel("new selection"))
            ctext ="> " + self.text 

        else:
            style = "dim grey93" #
        return Padding(Align.center(f"[{style}]{ctext}[/{style}]"))

class MinimalTextOption(CustomRenderable):
    def __init__(self, **kwargs):
        if 'h_allign' not in kwargs:
            kwargs['h_allign'] = "left"
        super().__init__(**kwargs)
        self.type = "menu" # Ensure type is set

    def render(self, style: str = "", left_padding: int = 0, core: Optional["Core"] = None) -> ConsoleRenderable:

        ctext = self.text # Example font

        style = "dim grey93"
        if self.selected:
            style = "bold green"
            ctext = "> " + self.text

        else:
            style = "dim grey93" #
        return Padding(Align.center(f"[{style}]{ctext}[/{style}]"))
        

class TyperWritter():
    def __init__(self,text:str,delay:float = 0.05):
        self.text = text
        self.delay = delay
        self.typed = ""
        self.is_typing = True
        self.current_index = 0
        self.last_update_time = time.time()
        
    def update(self) -> bool:
        """Update the typing animation. Returns True if still typing, False if done."""
        current_time = time.time()
        if current_time - self.last_update_time >= self.delay:
            if self.current_index < len(self.text):
                self.typed += self.text[self.current_index]
                self.current_index += 1
                self.last_update_time = current_time
            else:
                self.is_typing = False
        return self.is_typing
        
    def render(self,style:str = "",left_padding:int = 0,core:Optional["Core"] = None):
        return self.typed

class Delay:
    """Creates a delay/pause for a specified duration when rendered."""
    def __init__(self, duration: float = 1.0):
        self.duration = duration
        self.renderable = ""
        self.start_time = None
        self.is_delaying = True
        
    def update(self) -> bool:
        """Update the delay. Returns True if still delaying, False if done."""
        if self.start_time is None:
            self.start_time = time.time()
            
        current_time = time.time()
        if current_time - self.start_time >= self.duration:
            self.is_delaying = False
            return False
        return True
        
    def render(self, style: str = "", left_padding: int = 0, core: Optional["Core"] = None):
        """Render an empty string during delay."""
        return ""


class StoryTextOption(CustomRenderable):
    def __init__(self, **kwargs):
        if 'h_allign' not in kwargs:
            kwargs['h_allign'] = "left"
        super().__init__(**kwargs)
        self.type = "menu" # Ensure type is set

    def render(self, style: str = "", left_padding: int = 0, core: Optional["Core"] = None) -> ConsoleRenderable:

        ctext = self.text # Example font
        style = "dim grey93"
        if self.selected:
            from rich.style import Style
            style = Style(bold=True,bgcolor="green",color="black")
            ctext ="> " + self.text
        else:
            style = "dim grey93" #
        
        return Padding(Align.center(f"[{style}]{ctext}[/{style}]"),pad=(0,0,0,0))
        



class MinimalKeyboardOption(CustomRenderable):
    def __init__(self, **kwargs,):
        if 'h_allign' not in kwargs:
            kwargs['h_allign'] = "left"
        self.key = kwargs.pop("key", None)
        super().__init__(**kwargs)
        self.key = "[cyan1]"+str(self.key)+"[/cyan1]"
        self.text = str(self.text) + (" "* 10) + str(self.key)
        self.type = "menu" # Ensure type is set

    def render(self, style: str = "", left_padding: int = 0, core: Optional["Core"] = None) -> ConsoleRenderable:

        ctext = self.text # Example font
        style = "dim grey93"
        if self.selected:
            style = "bold green"
            s = "> " + self.text 
            core.console.current_layout.layout["right"].update(Panel("new selection"))
            ctext = s
        else:
            style = "dim grey93" #
        return Padding(Align.center(f"[{style}]{ctext}[/{style}]"))



class KeyboardStr:
    """Creates a delay/pause for a specified duration when rendered."""
    def __init__(self,str):
        self.str = str

    def render(self, style: str = "", left_padding: int = 0, core: Optional["Core"] = None):
        """Render an empty string during delay."""
        return self.str


class VolumeOption(CustomRenderable):
    def __init__(self, **kwargs):
        if 'h_allign' not in kwargs:
            kwargs['h_allign'] = "left"
        self.volume_type = kwargs.pop("volume_type", "sound")
        super().__init__(**kwargs)

        self.type = "menu" # Ensure type is set
    def volume(self,value:int):
        if self.volume_type == "sound":
            self.core.volume = max(0, min(10, self.core.volume + value))
        elif self.volume_type == "music":
            self.core.music_volume = max(0, min(10, self.core.music_volume + value))
        logger.info(f"Volume changed by {value}. Current volume: {self.core.volume}")

    def render(self, style: str = "", left_padding: int = 0, core: Optional["Core"] = None) -> ConsoleRenderable:
        try:
            from art import text2art 
            ctext = self.text # Example font
        except ImportError:
            ctext = self.text 
        except Exception: 
             ctext = f"[italic] {self.text} (art error) [/italic]"
        
        if self.volume_type == "sound":
            volume_count = int(self.core.volume)
        elif self.volume_type == "music":
            volume_count = self.core.music_volume
        style = "dim grey93"


        filled_bar_char = "■"
        empty_bar_char = "□"
         # Add space before indicator for alignment?
        if self.selected:
            style = "bold green"
            bar = filled_bar_char * volume_count
            bar = f"        [bold green]{bar}[/bold green]"

            mbar = f"[grey]{empty_bar_char * (10 - volume_count)}[/grey]"
            s = "[bold green]> " + self.text +"[/bold green] "+ bar+mbar
            
            core.console.current_layout.layout["right"].update(Panel("new selection"))
            ctext = s
            return Padding(Align.center(f"{ctext}"))
        else:

            bar = filled_bar_char * volume_count
            bar = f"        [bold green]{bar}[/bold green]"
            mbar = f"[grey]{empty_bar_char * (10 - volume_count)}[/grey]"
            s =  "[dim]"+self.text +"[/dim]" + bar+mbar
            ctext = s
            style = "dim grey93" #
            return Padding(Align.center(f"{ctext}"))
