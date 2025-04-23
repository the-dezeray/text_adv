from typing import Callable, Optional, Literal, TYPE_CHECKING
from rich.padding import Padding
from rich.panel import Panel
from rich.table import Table
from rich.align import Align
from rich.layout import Layout
from rich.text import Text
from rich import box
from rich.console import ConsoleRenderable

if TYPE_CHECKING:
    from core import Core
    from objects.weapon import Weapon


def yy():
    """Placeholder function"""
    pass


class Option:
    """Represents a selectable or non-selectable item in the UI."""
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
        """
        Initializes an Option object.

        Args:
            text (str): The text displayed for the option. Defaults to "".
            func (Optional[Callable]): The function executed when the option is selected. Defaults to None.
            preview (Optional[Callable]): A function to generate a preview when the option is highlighted. Defaults to None.
            next_node (Optional[str]): The identifier of the next node in a sequence or flow. Defaults to None.
            selectable (bool): Determines if the option can be selected by the user. Defaults to True.
            type (Literal[...] "" ): The category or type of the option. Defaults to "".
            h_allign (str): Horizontal alignment of the option's text. Defaults to "center".
            v_allign (str): Vertical alignment of the option's text. Defaults to "middle".
            on_select (Optional[Callable]): A function called immediately upon selection. Defaults to a placeholder.
            core (Optional["Core"]): A reference to the main application core object. Defaults to None.
        """
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
        """Gets the selection state of the option."""
        return self._selected

    @selected.setter
    def selected(self, value: bool) -> None:
        """
        Sets the selection state and triggers the preview function if selected.
        Requires the 'core' attribute to be set for refreshing the console.
        """
        self._selected = value
        # Trigger preview only if selected, preview function exists, and core is available
        if self._selected and self.preview and self.core and self.core.console:
            self.preview()
            self.core.console.refresh() # Refresh console to show preview

    def render(
        self, style: str = "", left_padding: int = 0, core: Optional["Core"] = None
    ) -> ConsoleRenderable:
        """
        Abstract render method to be implemented by subclasses.

        Args:
            style (str): The style string for rendering. Defaults to "".
            left_padding (int): The amount of left padding. Defaults to 0.
            core (Optional["Core"]): Reference to the core object. Defaults to None.

        Returns:
            ConsoleRenderable: The Rich renderable object for this option.

        Raises:
            NotImplementedError: If the subclass does not implement this method.
        """
        # Subclasses should implement how they render based on their state
        raise NotImplementedError("Subclasses must implement the render method.")


class buffer_create_weapons:
    """Creates a buffer specifically for displaying weapon options."""
    def __init__(
        self,
        ary: list["Weapon"] = None, # Specify list contains Weapon objects
        core: "Core" = None,
        extra: bool = False
    ):
        """
        Initializes the weapon buffer.

        Args:
            ary (list["Weapon"], optional): A list of Weapon objects. Defaults to None.
            core ("Core", optional): Reference to the main application core. Defaults to None.
            extra (bool): Flag for potentially different display modes. Defaults to False.

        Raises:
            ValueError: If core is None when initializing.
        """
        if core is None:
            raise ValueError("Core must be provided for buffer_create_weapons.")
        self.extra = extra
        # Initialize with an empty list if ary is None
        self.weapons = ary or []
        self.h_allign = "left"
        self.core = core
        self.selectable = True # This buffer itself isn't selectable, but its contents are
        self.ary = self._build_weapon_options() # Store the generated Option objects

    def _build_weapon_options(self) -> list["wep__ui"]:
        """Builds a list of wep__ui options from the weapon data."""
        from core.events.fight import deal_damage # Local import to prevent circular dependency

        options_list = []
        # Determine the preview function based on the 'extra' flag
        preview_func = self.core.console.show_weapon if self.extra and hasattr(self.core, 'console') and hasattr(self.core.console, 'show_weapon') else None

        for weapon in self.weapons:
            # Create a WeaponOption for each weapon
            # Use a lambda with a default argument to capture the current weapon
            options_list.append(
                WeaponOption(
                    weapon=weapon,
                    # Pass the specific weapon to deal_damage
                    func=lambda w=weapon: deal_damage(self.core, w),
                    preview=preview_func,
                    core=self.core
                )
            )
        return options_list

    def render(self, core: Optional["Core"] = None) -> ConsoleRenderable:
        """
        Renders the list of weapon options within a layout or grid.

        Args:
            core (Optional["Core"]): Reference to the core object (can override instance core). Defaults to None.

        Returns:
            ConsoleRenderable: A Panel or Table containing the rendered weapon options.
        """
        renderables = [option.render() for option in self.ary] # Render each weapon option

        grid = ui_grid(colomuns=1)
        for r in renderables:
            grid.add_row(r)

        # Different layout based on the 'extra' flag
        if not self.extra:
            from rich_pixels import Pixels # Local import for optional dependency
            layout = Layout()
            layout.split_row(Layout(name="options"), Layout(name="preview"))
            try:
                # Attempt to load and display an icon
                pixels = Pixels.from_image_path("icon1.png")
                layout["preview"].update(Panel(pixels, height=28))
            except Exception: # Catch potential file not found or loading errors
                 layout["preview"].update(Panel("[dim]No preview[/dim]", height=28)) # Fallback text

            layout["options"].update(grid)
            return Panel(layout, expand=False, height=32)
        else:
            # If 'extra' is true, just return the grid
            return grid


class buffer_display_choices:
    """Creates a buffer for displaying generic choice options."""
    def __init__(
        self,
        ary: list[dict] = None, # Expects a list of dictionaries
        title: str = "",
        icon: str = "" # Icon parameter seems unused in render
    ):
        """
        Initializes the choices buffer.

        Args:
            ary (list[dict], optional): List of choice dictionaries. Each dict should have 'text', 'function', 'next_node'. Defaults to None.
            title (str): Title for the choice section (unused in render). Defaults to "".
            icon (str): Icon identifier (unused in render). Defaults to "".
        """
        self.raw_choices = ary or []
        self.h_allign = "left"
        self.title = title
        self.selectable = True # Buffer contains selectable items
        self.ary = self._build_choice_options() # Store generated Option objects

    def _build_choice_options(self) -> list["new__ui"]:
        """Builds a list of new__ui options from the choice data."""
        options_list = []
        for choice_data in self.raw_choices:
            # Create a new__ui option for each dictionary in the list
            options_list.append(
                new__ui(
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

        grid = ui_grid(colomuns=1)
        for r in renderables:
            grid.add_row(r)
        return grid


class buffer_display_menu_items:
    """Creates a buffer for displaying menu items (similar to choices)."""
    def __init__(
        self,
        ary: list[dict] = None, # Expects a list of dictionaries
        title: str = "",
        icon: str = "" # Icon parameter seems unused in render
    ):
        """
        Initializes the menu items buffer.

        Args:
            ary (list[dict], optional): List of menu item dictionaries. Each dict should have 'text', 'function', 'next_node'. Defaults to None.
            title (str): Title for the menu section (unused in render). Defaults to "".
            icon (str): Icon identifier (unused in render). Defaults to "".
        """
        self.raw_items = ary or []
        self.h_allign = "left"
        self.title = title
        # Menu items are typically selectable
        self.ary = self._build_menu_item_options() # Store generated Option objects

    def _build_menu_item_options(self) -> list["new__ui"]:
        """Builds a list of new__ui options from the menu item data."""
        options_list = []
        for item_data in self.raw_items:
            # Create a new__ui option for each dictionary
            options_list.append(
                new__ui(
                    text=item_data.get("text", "Menu Item"), # Provide default
                    func=item_data.get("function"),
                    next_node=item_data.get("next_node"),
                    selectable=True,
                )
            )
        return options_list

    def render(self, core: Optional["Core"] = None) -> Table:
        """
        Renders the list of menu items within a grid.

        Args:
            core (Optional["Core"]): Reference to the core object. Defaults to None.

        Returns:
            Table: A Table (grid) containing the rendered menu item options.
        """
        renderables = [option.render() for option in self.ary]

        grid = ui_grid(colomuns=1)
        for r in renderables:
            grid.add_row(r)
        return grid


def ui_grid(colomuns: int = 1) -> Table:
    """
    Creates a simple Rich Table configured as a borderless grid.

    Args:
        colomuns (int): The number of columns for the grid. Defaults to 1.

    Returns:
        Table: A Rich Table object ready for rows to be added.
    """
    grid = Table.grid(expand=True) # Expand grid to fill available space
    for _ in range(colomuns):
        grid.add_column()
    return grid


def ui_text_panel(option: Optional[Option] = None, text: str = "") -> Padding:
    """
    Creates a simple text element wrapped in Padding. If an option is provided
    and selected, applies a specific style.

    Args:
        option (Optional[Option]): An Option object whose text and state might be used. Defaults to None.
        text (str): Explicit text to display. If empty, uses option's text. Defaults to "".

    Returns:
        Padding: A Padding object containing the text.

    Raises:
        ValueError: If both `option` and `text` are not provided.
    """
    display_text = text
    style = "" # Default style

    if not display_text:
        if option:
            display_text = option.text
            if option.selected:
                style = "bold green"
                # Preview is handled by the Option's selected setter, not here.
        else:
            # Raise error if there's nothing to display
            raise ValueError("ui_text_panel requires either an 'option' or 'text'.")

    # Return text wrapped in Padding, potentially with a style
    return Padding(Text(display_text, style=style))


def WeaponOption(
    weapon: "Weapon",
    func: Callable,
    preview: Optional[Callable] = None,
    core: Optional["Core"] = None
) -> "wep__ui":
    """
    Factory function to create a 'wep__ui' instance for a weapon.

    Args:
        weapon ("Weapon"): The weapon object.
        func (Callable): The function to execute when this weapon option is selected.
        preview (Optional[Callable]): Function to generate a preview. Defaults to None.
        core (Optional["Core"]): Reference to the core application object. Defaults to None.

    Returns:
        wep__ui: An initialized weapon UI option.
    """
    return wep__ui(
        text=weapon.name,
        func=func,
        selectable=True,
        type="weapon", # Set type explicitly
        preview=preview,
        core=core
    )


def new_ui_button(
    option: Option,
    # style: str = "", # Style is determined by selection state
    # selected: bool = False, # Selection is determined by option.selected
    top_padding: int = 0,
    right_padding: int = 0,
    bottom_padding: int = 0,
    left_padding: int = 0, # This seems overridden based on selection state
) -> Padding:
    """
    Creates a UI element resembling a button using Rich Panel and Padding.
    Highlights the button when the associated option is selected.

    Args:
        option (Option): The Option object associated with this button.
        top_padding (int): Top padding units. Defaults to 0.
        right_padding (int): Right padding units. Defaults to 0.
        bottom_padding (int): Bottom padding units. Defaults to 0.
        left_padding (int): Base left padding units (modified when selected). Defaults to 0.

    Returns:
        Padding: A Padding object containing the styled Panel.
    """
    button_height = 3
    current_left_padding = left_padding # Use the provided base padding
    border_style = "" # Default border style

    if option.selected:
        border_style = "bold green" # Highlight border when selected
        current_left_padding += 5 # Indent when selected
        # Preview is handled by the Option's selected setter, not here.

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


def ui_table() -> Table:
    """
    Creates a predefined Rich Table suitable for displaying options or data.

    Returns:
        Table: A configured Rich Table object.
    """
    table = Table(
        expand=True,
        caption=" - ", # Default caption
        show_edge=False,
        show_lines=False,
        show_header=False,
        style="bold red1", # Default style
        box=box.ROUNDED, # Use rounded box characters
    )
    table.add_column(justify="center") # Add a single centered column
    return table


def Loader() -> Padding:
    """
    Creates a simple "Loading..." indicator panel wrapped in Padding.

    Returns:
        Padding: A Padding object containing the loading Panel.
    """
    return Padding(Panel("Loading..."), pad=(2, 4, 0, 4), expand=False)


def Reward(ary: list[str] = None) -> Panel:
    """
    Displays a list of reward strings in a Panel.

    Args:
        ary (list[str], optional): A list of strings representing rewards. Defaults to None.

    Returns:
        Panel: A Panel containing the list of rewards.
    """
    rewards = ary or []
    grid = Table.grid(expand=True) # Use a grid to list rewards
    grid.add_column()
    for reward_text in rewards:
        grid.add_row(Text(reward_text, style="yellow")) # Style rewards text
    return Panel(grid, title="[bold green]Rewards![/bold green]", expand=False)


def get_selectable_options(options: list) -> list[Option]:
    """
    Filters a list of UI elements and extracts all selectable Option objects.
    It handles nested options within buffer objects.

    Args:
        options (list): A list potentially containing Option objects or buffer objects.

    Returns:
        list[Option]: A flattened list containing only the selectable Option instances.
    """
    selectable_list = []
    # Iterate in reverse to maintain visual order when selecting (usually bottom-up)
    for item in reversed(options):
        # Check if the item is a buffer containing a list of options (ary)
        if isinstance(item, (buffer_display_choices, buffer_create_weapons, buffer_display_menu_items)):
             # Add all options from the buffer's list
            selectable_list.extend(item.ary)
        # Check if the item itself is a selectable Option subclass
        elif isinstance(item, Option) and item.selectable:
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


# --- Option Subclasses ---

class wep__ui(Option):
    """UI representation for a weapon option."""
    def __init__(self, **kwargs):
        """Initializes a weapon UI element, forwarding arguments to Option."""
        super().__init__(**kwargs)
        self.type = "weapon" # Ensure type is set

    def render(self, style: str = "", left_padding: int = 0, core: Optional["Core"] = None) -> ConsoleRenderable:
        """
        Renders the weapon option, highlighting it when selected.

        Args:
            style (str): Base style (unused, determined by selection). Defaults to "".
            left_padding (int): Base padding (unused). Defaults to 0.
            core (Optional["Core"]): Core reference. Defaults to None.

        Returns:
            ConsoleRenderable: A Panel (if selected) or Padding (if not).
        """
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


class new__ui(Option):
    """General purpose UI option, often used for choices or simple actions."""
    def __init__(self, **kwargs):
        """Initializes a general UI element, forwarding arguments to Option."""
        super().__init__(**kwargs)
        # Type might be set via kwargs or defaults to ""

    def render(self, style: str = "", left_padding: int = 0, core: Optional["Core"] = None) -> ConsoleRenderable:
        """
        Renders the general UI option, highlighting it when selected.

        Args:
            style (str): Base style (unused). Defaults to "".
            left_padding (int): Base padding (unused). Defaults to 0.
            core (Optional["Core"]): Core reference. Defaults to None.

        Returns:
            ConsoleRenderable: A Panel (if selected) or Padding (if not).
        """
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


class choose_me(Option):
    """A distinct UI option type, possibly for confirmation or special choices."""
    def __init__(self, **kwargs):
        """Initializes a 'choose_me' UI element, forwarding arguments to Option."""
        super().__init__(**kwargs)
        # Type might be set via kwargs

    def render(self, style: str = "", left_padding: int = 0, core: Optional["Core"] = None) -> Panel:
        """
        Renders the 'choose_me' option as a Panel, highlighting border when selected.

        Args:
            style (str): Base style (unused). Defaults to "".
            left_padding (int): Base padding (potentially modified internally). Defaults to 0.
            core (Optional["Core"]): Core reference. Defaults to None.

        Returns:
            Panel: A Panel representing the option.
        """
        current_style = "" # Default empty style
        # Padding is handled externally if needed, not added here directly.
        # self.left_padding modification removed as it's not standard practice in render

        if self.selected:
            current_style = "bold green"
            # Preview handled by setter

        # Always render as a Panel, change style based on selection
        return Panel(Align.center(self.text), style=current_style, expand=False)


class menu__ui(Option):
    """UI representation for a main menu item, often using ASCII art."""
    def __init__(self, **kwargs):
        """Initializes a menu UI element, forwarding arguments to Option."""
        # Default horizontal alignment to left for menu items
        if 'h_allign' not in kwargs:
            kwargs['h_allign'] = "left"
        super().__init__(**kwargs)
        self.type = "menu" # Ensure type is set

    def render(self, style: str = "", left_padding: int = 0, core: Optional["Core"] = None) -> ConsoleRenderable:
        """
        Renders the menu item using ASCII art text, highlighting when selected.

        Args:
            style (str): Base style (unused). Defaults to "".
            left_padding (int): Base padding (unused). Defaults to 0.
            core (Optional["Core"]): Core reference. Defaults to None.

        Returns:
            ConsoleRenderable: A Panel or Padding containing the ASCII art text.
        """
        try:
            from art import text2art # Optional dependency
            # Generate ASCII art, fallback to plain text if 'art' fails
            ctext = text2art(self.text, font="tarty2") # Example font
        except ImportError:
            ctext = self.text # Fallback to plain text
        except Exception: # Catch errors during text2art generation
             ctext = f"[italic] {self.text} (art error) [/italic]"

        if self.selected:
            self.style = "bold green"
            # Preview handled by setter
            # Wrap selected ASCII art in a Panel for potential border/background
            return Panel(Align.center(f"[{self.style}]{ctext}[/{self.style}]"), border_style=self.style, expand=False)
        else:
            self.style = "dim grey93" # Dim style for non-selected
            # Non-selected is just padded text
            return Padding(Align.center(f"[{self.style}]{ctext}[/{self.style}]"), (0,0,0,0))