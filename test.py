import time
from rich.console import Console
from rich.text import Text
from rich.rule import Rule
from rich.panel import Panel  # Import Panel for selected options
from typing import List, Tuple, Optional

# --- Function to display scene content directly to console ---
def display_scene(
    console: Console,
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
    console.print(Rule(title, style="bright_cyan"))
    console.print()  # Add some spacing

    # Print the narrative
    console.print(narrative)
    console.print()  # Add spacing after narrative

    # Display options if provided, using Panel for the selected one
    if options:
        console.print("[bold magenta]--- Choose an Action ---[/bold magenta]")

        # Define style for unselected options
        style_unselected = f"dim {option_style}"  # Dim the unselected options

        for i, option_text in enumerate(options):
            if selected_index is not None and i == selected_index:
                # Create a Panel for the selected option, including the icon
                selected_text = f"{option_icon} {option_text}"
                panel = Panel(
                    selected_text,
                    style=f"bold {option_style}",
                    padding=(0, 1),  # Minimal padding (vertical, horizontal)
                    expand=False     # Don't expand to fill width
                )
                console.print(panel)
            else:
                # Print unselected options normally with icon
                console.print(f"[{style_unselected}]{option_icon} {option_text}[/{style_unselected}]")

    else:
        # Handle cases with no specific options
        console.print("[dim][italic](Press Enter to continue...)[/italic][/dim]")

    console.print()  # Add blank line at the end of the scene display

# ---------------------------------------------

# --- Main Game Simulation ---
# IMPORTANT: This simulation just SHOWS the selected option.
# It does NOT implement actual arrow key input or selection logic.
if __name__ == "__main__":
    console = Console(force_terminal=True)  # Ensure Rich uses colors even if piped

    # Check if the terminal likely supports Nerd Fonts (basic check)
    # In a real app, you might have better detection or configuration.
    try:
        # Try printing a known Nerd Font character - this might still render
        # incorrectly if the font isn't installed, but it avoids errors.
        console.print(f"Testing Nerd Font: \uf1bb", end="\r")
        time.sleep(0.1)  # Tiny pause
        console.print(" " * 20, end="\r")  # Clear the test line
    except Exception as e:
        console.print(f"[bold red]Warning: Could not render Nerd Font character. Icons might not display correctly.[/bold red]")
        console.print(f"[dim]Ensure you have a Nerd Font installed and configured in your terminal.[/dim]")

    # --- Scene 1: The Awakening ---
    narrative1 = ("Sunlight streams through the dense canopy above. "
                  "You slowly open your eyes, the smell of damp earth filling your nostrils. "
                  "A throbbing pain echoes in your skull. You appear to be in a [green]forest[/green]. "
                  "Paths lead left and right, and something glints nearby.")
    options1 = [
        "Go Left towards the darker woods",
        "Go Right towards a faint sound of water",
        "Investigate the glinting object"
    ]
    display_scene(
        console,
        narrative1,
        options1,
        selected_index=0,  # Show first option highlighted initially
        title="[b green]\uf1bb Deep Forest[/b green]",  # nf-fa-tree
        option_icon="\uf0da",  # nf-fa-caret_right (from original code)
        option_style="green"
    )
    console.print("\n[dim](Simulating choice: 2. Go Right towards water...)[/dim]")
    time.sleep(2)  # Slightly longer pause for readability

    # --- Scene 2: The Stream ---
    narrative2 = ("Following the faint sound, you push through some ferns and arrive "
                  "at the bank of a small, clear [blue]stream[/blue]. Tiny fish dart between smooth stones. "
                  "The water looks refreshingly cool. The stream flows gently downhill.")
    options2 = [
        "Drink from the stream",
        "Follow the stream downhill",
        "Head back into the forest"  # Option to return
    ]
    display_scene(
        console,
        narrative2,
        options2,
        selected_index=0,  # Show first option highlighted
        title="[b cyan]\uf773 Babbling Stream[/b cyan]",  # nf-mdi-water
        option_icon="\uf0da",  # nf-fa-caret_right
        option_style="cyan"
    )
    console.print("\n[dim](Simulating choice: 1. Drink from the stream...)[/dim]")
    time.sleep(2)

    # --- Scene 3: Refreshment ---
    narrative3 = ("You kneel and cup your hands, scooping up the cold water. It tastes pure and "
                  "instantly quenches your thirst. The throbbing in your head lessens slightly. "
                  "You feel a bit revitalized. \uf004")  # nf-fa-heart
    # No specific choices here
    display_scene(
        console,
        narrative3,
        options=None,  # Pass None for options to show continue prompt
        # selected_index is irrelevant here as there are no options
        title="[b bright_green]\uf79f Refreshed[/b bright_green]",  # nf-mdi-cup_water
    )
    console.print("\n[dim](Simulating pressing Enter...)[/dim]")
    time.sleep(2)

    # --- Scene 4: Following Downstream ---
    narrative4 = ("Deciding to follow the water's path, you walk alongside the stream as it "
                  "widens slightly. The trees thin out ahead, revealing a small, dilapidated "
                  "[grey]wooden shack[/grey] nestled near the bank. Smoke trickles from its chimney.")
    options4 = [
        "Approach the shack cautiously",
        "Hide and observe the shack",
        "Continue following the stream, ignoring the shack"
    ]
    display_scene(
        console,
        narrative4,
        options4,
        selected_index=0,  # Show first option highlighted
        title="[b yellow]\uf6e4 Downstream Path[/b yellow]",  # nf-mdi-home_variant_outline
        option_icon="\uf0da",  # nf-fa-caret_right
        option_style="yellow"
    )
    console.print("\n[dim](Simulating choice: 1. Approach the shack cautiously...)[/dim]")
    time.sleep(2)

    # --- Scene 5: The Shack Door ---
    narrative5 = ("You move quietly towards the shack. The wood is old and weathered. A faint, "
                  "savory smell emanates from within, mixed with woodsmoke. The door is slightly ajar. "
                  "You hear a low humming sound from inside.")
    options5 = [
        "Knock on the door \uf52a",  # nf-mdi-door_open
        "Peek through the opening",
        "Back away slowly"
    ]
    display_scene(
        console,
        narrative5,
        options5,
        selected_index=0,  # Show first option highlighted
        title="[b default]\uf6ea The Old Shack[/b default]",  # nf-mdi-hut
        option_icon="\uf0da",  # nf-fa-caret_right
        option_style="white"  # Using white as base style
    )
    console.print("\n[dim](Simulating choice: 2. Peek through the opening...)[/dim]")
    time.sleep(2)

    # --- Scene 6: Inside the Shack ---
    narrative6 = ("You carefully peer through the crack in the door. Inside, an old woman with "
                  "kind eyes hums as she stirs a pot over a small hearth. Shelves lined with herbs "
                  "and strange roots cover the walls. She hasn't noticed you yet.")
    options6 = [
        "Clear your throat to announce yourself",
        "Push the door open fully",
        "Quietly retreat"
    ]
    display_scene(
        console,
        narrative6,
        options6,
        selected_index=0,  # Show first option highlighted
        title="[b magenta]\uf500 Peeking Inside[/b magenta]",  # nf-mdi-eye_outline
        option_icon="\uf0da",  # nf-fa-caret_right
        option_style="magenta"
    )
    console.print("\n[dim](Simulating choice: 1. Clear your throat...)[/dim]")
    time.sleep(2)

    # --- Scene 7: Encounter ---
    narrative7 = ("You make a soft 'ahem' sound. The old woman startles slightly, turning towards "
                  "the door. Her eyes widen a fraction, but then soften into a curious gaze. "
                  "'Well now,' she says, her voice raspy but gentle. 'Lost, are we? Come in, come in out of the woods.'")
    # End of this sequence example
    display_scene(
        console,
        narrative7,
        options=None,  # No options here
        title="[b bright_blue]\uf58b Encounter[/b bright_blue]",  # nf-mdi-human_greeting
    )
    console.print("\n[dim](Simulating pressing Enter...)[/dim]")
    time.sleep(2)

    console.print(Rule(style="green"))  # Final rule
    console.print("\n[bold green]--- End of Demo Sequence ---[/bold green]")