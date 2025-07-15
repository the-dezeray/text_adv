from rich.console import Console
from rich.layout import Layout
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

def create_rpg_inventory_layout():
    """Creates a Rich layout for an RPG inventory screen."""
    layout = Layout()

    # Split the layout into a header for the title and a main content area
    layout.split(
        Layout(name="header", size=3),
        Layout(ratio=1, name="main"),
    )

    # Split the main area into a side panel for character stats and a primary area
    layout["main"].split_row(Layout(name="side"), Layout(name="body", ratio=2))

    # Split the body into the inventory grid and an item description footer
    layout["body"].split(Layout(name="inventory"), Layout(name="footer", size=7))

    return layout

def make_character_panel() -> Panel:
    """Creates a panel displaying character stats."""
    character_stats = Table.grid(padding=1)
    character_stats.add_column(style="cyan", justify="right")
    character_stats.add_column(no_wrap=True)
    character_stats.add_row("Name:", "Gandalf")
    character_stats.add_row("Level:", "99")
    character_stats.add_row("HP:", "[bold red]100/100[/bold red]")
    character_stats.add_row("MP:", "[bold blue]80/80[/bold blue]")
    character_stats.add_row("Strength:", "75")
    character_stats.add_row("Magic:", "95")
    character_stats.add_row("Defense:", "60")

    return Panel(character_stats, title="[bold yellow]Character[/bold yellow]", border_style="green")

def make_inventory_panel() -> Panel:
    """Creates a panel for the inventory grid."""
    inventory_table = Table(
        show_header=True, header_style="bold magenta", expand=True
    )
    inventory_table.add_column("Item", style="dim")
    inventory_table.add_column("Quantity", justify="right")
    inventory_table.add_column("Value", justify="right")

    # --- Sample Inventory Items ---
    inventory_table.add_row("Health Potion", "5", "50g")
    inventory_table.add_row("Mana Potion", "3", "75g")
    inventory_table.add_row("Sword of Slaying", "1", "1200g")
    inventory_table.add_row("Elven Cloak", "1", "800g")
    inventory_table.add_row("Lembas Bread", "10", "10g")
    inventory_table.add_row("Key to the West Gate", "1", "N/A")

    return Panel(inventory_table, title="[bold yellow]Inventory[/bold yellow]", border_style="green")

def make_item_description_panel() -> Panel:
    """Creates a panel for the selected item's description."""
    description = Text(
        "A finely crafted blade, rumored to be of ancient make. It glows faintly in the presence of orcs.",
        justify="left",
    )
    return Panel(description, title="[bold yellow]Sword of Slaying[/bold yellow]", border_style="green")


if __name__ == "__main__":
    console = Console()
    layout = create_rpg_inventory_layout()

    # Update the layout with the generated panels
    layout["header"].update(
        Panel(Text("RPG INVENTORY", justify="center", style="bold white on blue"))
    )
    layout["side"].update(make_character_panel())
    layout["body"]["inventory"].update(make_inventory_panel())
    layout["body"]["footer"].update(make_item_description_panel())

    console.print(layout)