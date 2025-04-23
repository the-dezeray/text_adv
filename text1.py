import time
from rich.console import Console
from rich.text import Text # Keep import just in case
from rich.rule import Rule
from typing import List, Tuple, Optional, Dict, Any # Added Dict and Any for weapon data type hint

# --- Function to display scene content directly to console ---
# (Keep your original display_scene function as it's useful for narrative)
def display_scene(
    console: Console, # Pass the console object
    narrative: str,
    options: Optional[List[str]] = None,
    title: str = "[b yellow]\uf4ad Scene[/b yellow]", # nf-mdi-text_box_outline
    option_icon: str = "\uf105", # nf-fa-angle_right
    option_style: str = "cyan"
):
    """
    Displays game narrative and options directly to the console using Rich,
    separated by a rule, without using a Panel.

    Args:
        console (Console): The Rich Console object to print to.
        narrative (str): The main descriptive text for the scene. Rich markup enabled.
        options (Optional[List[str]]): A list of choices for the player. If None,
                                     a 'continue' prompt is shown. Defaults to None.
        title (str): The title to display in the separator rule. Rich markup enabled.
        option_icon (str): The Nerd Font icon to prefix each option with.
        option_style (str): The Rich style for the options text.
    """
    # Use a Rule as a scene separator with the title
    console.print(Rule(title, style="bright_cyan")) # Use a default style for the rule line
    console.print() # Add some spacing

    # Print the narrative
    console.print(narrative)
    console.print() # Add spacing after narrative

    # Display options if provided
    if options:
        console.print("[bold magenta]--- Choose an Action ---[/bold magenta]")
        for i, option_text in enumerate(options):
            # Print each option with numbering, icon, and style
            console.print(f"  [{option_style}]{i+1}. {option_icon} {option_text}[/{option_style}]")
    else:
        # Handle cases with no specific options
        console.print("[dim][italic](Press Enter to continue...)[/italic][/dim]")

    console.print() # Add blank line at the end of the scene display

# --- NEW Function specifically for detailed choice lists like weapon selection ---
def display_detailed_choices(
    console: Console,
    narrative: str,
    choices: List[Dict[str, str]], # Expects a list of dictionaries with 'icon', 'name', 'desc', 'style'
    title: str = "[b yellow]\uf044 Make a Choice[/b yellow]", # nf-fa-edit
    prompt: str = "[bold magenta]--- Choose an Item ---[/bold magenta]"
):
    """
    Displays narrative and a detailed list of choices, each with an icon,
    name, description, and style.

    Args:
        console (Console): The Rich Console object to print to.
        narrative (str): The introductory text for the choice. Rich markup enabled.
        choices (List[Dict[str, str]]): A list of dictionaries. Each dict should have:
                                          'icon': Nerd Font character (str)
                                          'name': Name of the choice (str)
                                          'desc': Description (str)
                                          'style': Rich style for the name/icon (str)
        title (str): The title to display in the separator rule. Rich markup enabled.
        prompt (str): The text to display above the numbered list. Rich markup enabled.
    """
    console.print(Rule(title, style="bright_cyan"))
    console.print()
    console.print(narrative)
    console.print()

    if choices:
        console.print(prompt)
        for i, choice_data in enumerate(choices):
            # Format each choice line
            icon = choice_data.get('icon', '?') # Default icon if missing
            name = choice_data.get('name', 'Unknown Choice')
            desc = choice_data.get('desc', 'No description.')
            style = choice_data.get('style', 'white') # Default style

            # Print formatted choice: Number. [style]Icon Name[/style] - [dim]Description[/dim]
            console.print(
                f"  {i+1}. [{style}]{icon} {name}[/{style}] - [dim italic]{desc}[/dim italic]"
            )
    else:
        console.print("[dim italic](No choices available...)[/dim italic]")

    console.print() # Add blank line at the end

# ---------------------------------------------

# --- Weapon Definitions ---
# Using a list of dictionaries to store weapon data
# Icons from Nerd Fonts (ensure your terminal supports them!)
# nf-mdi-sword: \uf53a
# nf-mdi-axe: \uf6b3
# nf-mdi-bow-arrow: \uf51e
# nf-mdi-knife: \uf51c (for dagger)
# nf-mdi-magic-staff: \uf6f0
# nf-mdi-bat: \uf6b8 (for club)
# nf-mdi-shield-cross: \uf794 (maybe shield bash?)
# nf-mdi-hand-back-left: \ufc99 (unarmed)

WEAPONS = [
    {
        "icon": "\uf53a", # nf-mdi-sword
        "name": "Iron Sword",
        "desc": "A standard blade. Reliable and balanced.",
        "style": "bright_white"
    },
    {
        "icon": "\uf6b3", # nf-mdi-axe
        "name": "Woodsman's Axe",
        "desc": "Heavy and sharp. Good for chopping wood... or foes.",
        "style": "yellow" # brown isn't a standard rich color, use yellow/orange
    },
    {
        "icon": "\uf51c", # nf-mdi-knife
        "name": "Swift Dagger",
        "desc": "Small, fast, and easy to conceal. Favors quick strikes.",
        "style": "cyan"
    },
    {
        "icon": "\uf51e", # nf-mdi-bow-arrow
        "name": "Hunter's Bow",
        "desc": "Keeps enemies at a distance. Requires arrows (sold separately!).",
        "style": "green"
    },
    {
        "icon": "\uf6f0", # nf-mdi-magic-staff
        "name": "Apprentice Staff",
        "desc": "Focuses arcane energy. Feels warm to the touch.",
        "style": "bright_blue"
    },
    {
        "icon": "\uf6b8", # nf-mdi-bat
        "name": "Sturdy Club",
        "desc": "A simple piece of heavy wood. Surprisingly effective.",
        "style": "bold orange"
    },
    {
        "icon": "\ufc99", # nf-mdi-hand-back-left
        "name": "Bare Fists",
        "desc": "Sometimes the best tools are the ones you were born with.",
        "style": "dim"
    }
]


# --- Main Game Simulation ---
if __name__ == "__main__":
    console = Console()

    # --- Example Scene: Finding an Armoury ---
    narrative_armoury = ("You push open a creaking wooden door and find yourself in a small, dusty armoury. "
                         "Racks line the walls, holding a variety of basic weapons. It seems you can choose one "
                         "to aid you on your journey.")

    display_scene(
        console,
        narrative_armoury,
        title="[b white]\uf6a0 The Armoury[/b white]" # nf-mdi-shield-sword
    )
    # Simulate pressing Enter before showing choices
    # console.print("\n[dim](Simulating pressing Enter...)[/dim]")
    # time.sleep(1.5) # Pause if needed

    # --- Weapon Selection Scene ---
    narrative_choose = "The faint light glints off metal and wood. Which weapon will you take?"
    display_detailed_choices(
        console,
        narrative_choose,
        WEAPONS, # Pass the list of weapon dictionaries
        title="[b yellow]\uf0ad Choose Your Weapon[/b yellow]", # nf-fa-wrench
        prompt="[bold green]--- Select Your Armament ---[/bold green]"
    )

    # --- Simulate Player Choice ---
    # In a real game, you would get input here, e.g., input("Enter the number of your choice: ")
    # For demonstration, let's pretend the player chooses the Dagger (option 3)
    player_choice_index = 2 # (Index is number - 1)
    chosen_weapon = WEAPONS[player_choice_index]

    console.print(f"\n[dim](Simulating choice: {player_choice_index + 1}. {chosen_weapon['name']}...)[/dim]")
    time.sleep(2)

    # --- Confirmation Scene ---
    narrative_confirm = (f"You grip the [{chosen_weapon['style']}]{chosen_weapon['name']}[/{chosen_weapon['style']}] {chosen_weapon['icon']}. "
                         f"It feels { 'light' if 'Dagger' in chosen_weapon['name'] else 'solid' if 'Sword' in chosen_weapon['name'] else 'heavy' if 'Axe' in chosen_weapon['name'] or 'Club' in chosen_weapon['name'] else 'balanced' if 'Bow' in chosen_weapon['name'] else 'strangely warm' if 'Staff' in chosen_weapon['name'] else 'familiar' } in your hand. " # Example flavor text based on choice
                         "You are now better equipped for the dangers ahead.")

    display_scene(
        console,
        narrative_confirm,
        title="[b bright_green]\uf00c Weapon Acquired[/b bright_green]" # nf-fa-check
    )

    console.print(Rule(style="blue"))
    console.print("\n[bold blue]--- Ready for Adventure ---[/bold blue]")
    from rich.table import Table 
    a Table()