from typing import Callable, Optional, Literal, TYPE_CHECKING
from rich.padding import Padding
from rich.panel import Panel
from rich.table import Table
from rich.align import Align
from rich.layout import Layout
from rich.text import Text

from rich.console import ConsoleRenderable

if TYPE_CHECKING:
    from core import Core
    from objects.weapon import Weapon


def yy():
    """Placeholder function"""
    pass


class CustomRenderable:
    def __init__(
        self,
        text: str = "",
        func: Optional[Callable] = None,
        preview: Optional[Callable] = None, # Changed from str to Callable based on usage
        next_node: Optional[str] = None,
        selectable: bool = True,
        type: Literal["header", "entity_profile", "note", "choices", "menu", "weapon", ""] = "", # Added "weapon"
        h_allign: str = "center",
        v_allign: str = "middle",
        on_select: Optional[Callable] = None,
        core: Optional["Core"] = None, # Added type hint
    ) -> None:
        self.left_padding = 0
        self.style = ""
        self.core = core
        self.text = text
        self.func = func
        self.preview = preview # Function to call for preview
        self.next_node = next_node
        self.selectable = selectable
        self._selected = False
        self.type = type
        self.v_allign = v_allign
        self.h_allign = h_allign
        # Ensure on_select is always callable
        self.on_select = on_select if on_select is not None else yy

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

    def render(
        self, style: str = "", left_padding: int = 0, core: Optional["Core"] = None
    ) -> ConsoleRenderable:
        # Subclasses should implement how they render based on their state
        raise NotImplementedError("Subclasses must implement the render method.")


class GridOfWeapons:
    """Creates a buffer specifically for displaying weapon options."""
    def __init__(
        self,
        ary: list["Weapon"] = None, # Specify list contains Weapon objects
        core: "Core" = None,
        extra: bool = False
    ):
        if core is None:
            raise ValueError("Core must be provided for GridOfWeapons.")
        self.extra = extra
        # Initialize with an empty list if ary is None
        self.weapons = ary or []
        self.h_allign = "left"
        self.core = core
        self.selectable = True # This buffer itself isn't selectable, but its contents are
        self.ary = self._build_weapon_options() # Store the generated CustomRenderable objects

    def _build_weapon_options(self) -> list["WeaponOption"]:
        """Builds a list of WeaponOption options from the weapon data."""
        from core.events.fight import deal_damage # Local import to prevent circular dependency

        options_list = []
        # Determine the preview function based on the 'extra' flag
        preview_func = self.core.console.show_weapon if self.extra and hasattr(self.core, 'console') and hasattr(self.core.console, 'show_weapon') else None

        for weapon in self.weapons:
            # Create a create_weapon_option for each weapon
            # Use a lambda with a default argument to capture the current weapon
            options_list.append(
                create_weapon_option(
                    weapon=weapon,
                    # Pass the specific weapon to deal_damage
                    func=lambda w=weapon: deal_damage(self.core, w),
                    preview=preview_func,
                    core=self.core
                )
            )
        return options_list

    def render(self, core: Optional["Core"] = None) -> ConsoleRenderable:
        renderables = [option.render() for option in self.ary] # Render each weapon option

        grid = create_grid(colomuns=1)
        for r in renderables:
            grid.add_row(r)

        # Different layout based on the 'extra' flag
        if not self.extra:
            from rich_pixels import Pixels # Local import for optional dependency
            layout = Layout()
            layout.split_row(Layout(name="options"), Layout(name="preview"))
            try:
                # Attempt to load and display an icon
                cc =[]
                for i in range(0,49):
                    cc.append(f"a/{i}.png")
                cc =["1.png","2.png","3.png"]
                import random
                icon = random.choice(cc)
                from rich_pixels import FullcellRenderer
                pixels = Pixels.from_image_path(icon,resize=(16,16))
                a = Table.grid(expand=False)
                a.add_column()
                a.add_row(Panel(pixels,border_style="cyan",subtitle="reaper",subtitle_align="right",expand=False,width=23))

                a.add_row("󰦝 dmg [ [bold red1]43[/bold red1] ]")
                a.add_row("󰄽 spd 23")
                a.add_row("[white]EFFECTS[/white]\n [red]bleed 1[/red][cyan]frost[/cyan]\n slow and blinding")
                layout["preview"].update(Padding(a, expand=False))
            except Exception: # Catch potential file not found or loading errors
                 layout["preview"].update(Panel("[dim]No preview[/dim]", height=28)) # Fallback text

            layout["options"].update(grid)
            return Padding(layout, expand=False,)
        else:
            # If 'extra' is true, just return the grid
            return grid


class GridOfChoices:
    """Creates a buffer for displaying generic choice options."""
    def __init__(
        self,
        ary: list[dict] = None, # Expects a list of dictionaries
        title: str = "",
        icon: str = "" # Icon parameter seems unused in render
    ):

        self.raw_choices = ary or []
        self.h_allign = "left"
        self.title = title
        self.selectable = True # Buffer contains selectable items
        self.ary = self._build_choice_options() # Store generated CustomRenderable objects

    def _build_choice_options(self) -> list["Option"]:
        """Builds a list of Option options from the choice data."""
        options_list = []
        for choice_data in self.raw_choices:
            # Create a Option option for each dictionary in the list
            options_list.append(
                Option(
                    text=choice_data.get("text", "Missing text"), # Provide default
                    func=choice_data.get("function"), # Function can be None
                    next_node=choice_data.get("next_node"), # next_node can be None
                    selectable=True, # Assume choices are selectable
                )
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


def create_weapon_option(
    weapon: "Weapon",
    func: Callable,
    preview: Optional[Callable] = None,
    core: Optional["Core"] = None
) -> "WeaponOption":
    return WeaponOption(
        text=weapon.name,
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


def Reward(ary: list[str] = None) -> Panel:

    rewards = ary or []
    grid = Table.grid(expand=True) # Use a grid to list rewards
    grid.add_column()
    for reward_text in rewards:
        grid.add_row(Text(reward_text, style="yellow")) # Style rewards text
    return Panel(grid, title="[bold green]Rewards![/bold green]", expand=False)


def get_selectable_options(options: list) -> list[CustomRenderable]:

    selectable_list = []
    # Iterate in reverse to maintain visual order when selecting (usually bottom-up)
    for item in reversed(options):
        # Check if the item is a buffer containing a list of options (ary)
        if isinstance(item, (GridOfChoices, GridOfWeapons)):
             # Add all options from the buffer's list
            selectable_list.extend(item.ary)
        # Check if the item itself is a selectable CustomRenderable subclass
        elif isinstance(item, CustomRenderable) and item.selectable:
            selectable_list.append(item)
        # Add checks for other potential container types if needed
    return selectable_list


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

class WeaponOption(CustomRenderable):
    """UI representation for a weapon option."""
    def __init__(self, **kwargs):
        """Initializes a weapon UI element, forwarding arguments to CustomRenderable."""
        super().__init__(**kwargs)
        self.type = "weapon" # Ensure type is set

    def render(self, style: str = "", left_padding: int = 0, core: Optional["Core"] = None) -> ConsoleRenderable:
        # Use a Unicode arrow or similar indicator
        indicator = "\uf0da" # Example: Right-pointing arrow
        display_text = f"{indicator} {self.text} "

        if self.selected:
            self.style = "bold green" # Internal style tracking
            # Preview is handled by the setter
            return Panel(display_text, style=self.style, expand=False) # Wrap selected in Panel
        else:
            self.style = "dim green" # Internal style tracking
            # Non-selected items are padded Text
            return Padding(Text(display_text, style=self.style), (0, 0, 0, 0)) # No extra padding here






class Option(CustomRenderable):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    def render(self, style: str = "", left_padding: int = 0, core: Optional["Core"] = None) -> ConsoleRenderable:
        indicator = "\uf0da"
        display_text = f"{indicator} {self.text} "

        if self.selected:
            self.style = "bold green"
            # Preview handled by setter
            return Panel(display_text, style=self.style, expand=False)
        else:
            self.style = "dim green"
             # Add space before indicator for alignment?
            return Padding(Text(f" {display_text}", style=self.style), (0, 0, 0, 0))
class MenuOption(CustomRenderable):
    def __init__(self, **kwargs):
        if 'h_allign' not in kwargs:
            kwargs['h_allign'] = "left"
        super().__init__(**kwargs)
        self.type = "menu" # Ensure type is set

    def render(self, style: str = "", left_padding: int = 0, core: Optional["Core"] = None) -> ConsoleRenderable:
        try:
            from art import text2art 
            ctext = text2art(self.text, font="tarty2") # Example font
        except ImportError:
            ctext = self.text 
        except Exception: 
             ctext = f"[italic] {self.text} (art error) [/italic]"

        if self.selected:
            self.style = "bold green"

            return Panel(Align.center(f"[{self.style}]{ctext}[/{self.style}]"), border_style=self.style, expand=False)
        else:
            self.style = "dim grey93" #
            return Padding(Align.center(f"[{self.style}]{ctext}[/{self.style}]"), (0,0,0,0))