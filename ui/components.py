import time
from rich.console import Console
from rich.text import Text
from rich.rule import Rule
from rich.panel import Panel  # Import Panel for selected options
from typing import List, Tuple, Optional
from rich.padding import Padding
from ui.options import Option


def display_scene(
    narrative: str,
    options: Optional[List[str]] = None,
    selected_index: Optional[int] = 0,
    title: str = "[b yellow]\uf4ad Scene[/b yellow]",
    option_icon: str = "\uf101",  # Default icon for options (nf-fa-angle_right)
    option_style: str = "cyan"  # Base style color for options
):
    """
    Displays game narrative and options directly to the console using Rich,
    highlighting one option using a Panel.

    Args:
        console (Console): The Rich Console object to print to.
        narrative (str): The main descriptive text for the scene. Rich markup enabled.
        options (Optional[List[str]]): A list of choices for the player. If None,
                                     a 'continue' prompt is shown. Defaults to None.
        selected_index (Optional[int]): The 0-based index of the option to visually
                                        highlight with a Panel. Defaults to 0 (first option).
                                        If None or out of range, nothing is highlighted.
        title (str): The title to display in the separator rule. Rich markup enabled.
        option_icon (str): Icon prefix for options.
        option_style (str): The base Rich style color for the options.
    """

    # Use a Rule as a scene separator with the title

    from rich.table import Table
    a = Table.grid()
    a.add_column()
    a.add_row(Rule(title, style="bright_cyan"))
    a.add_row()
        # Print the narrative
    a.add_row(narrative)
    a.add_row()  # Add spacing after narrative

    # Display options if provided, using Panel for the selected one
    if options:
        a.add_row("[bold magenta]--- Choose an Action ---[/bold magenta]")

        # Define style for unselected options
        #style_unselected = f"dim {option_style}"  # Dim the unselected options

        for i, option_text in enumerate(options):
            
            a.add_row[option_text]
