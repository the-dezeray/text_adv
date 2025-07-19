from rich.padding import Padding
from rich.table import Table
from rich.panel import Panel
from rich.padding import Padding
from rich.align import Align
from rich.console import group
from typing import List,TYPE_CHECKING

if TYPE_CHECKING:
    from core.core import Core
def stats_tab(player)-> Table:
    stat_grid = Table.grid(padding=(0, 2))
    stat_grid.add_column(justify="left", style="bold yellow")
    stat_grid.add_column(justify="right", style="cyan")

    stats = {
        "󰛨 Health": player.hp,      # nf-md-heart
        "󰦝 Damage": player.attack,   # nf-md-sword
        " Defence": player.defense, # nf-md-shield
        "󰄽 Speed": player.speed,     # nf-md-run
        "󰔚 Luck": player.luck,       # nf-fa-clover
        "󰫍 EXP": player.exp         # nf-md-star_three_points
    }

    for key, value in stats.items():
        stat_grid.add_row(key, str(value))

    return stat_grid

def player_tab(core):
    grid = Table.grid(expand=True)
    grid.add_column()
    stat_grid = Table.grid(expand=True)
    ch = {"health":   core.player.hp,"damage":   core.player.attack,"defence":   core.player.defense,"speed":   core.player.speed,"luck":   core.player.luck,"exp":   core.player.exp} 
    #for key, value in ch.items():
    #    stat_grid.add_row(f"[bright_yellow]{key}[/bright_yellow]\t\t [blue]{value}[/blue]")
    stat_grid.add_row(stats_tab(   core.player))
    
    from rich.text import Text

    def draw_bar(label: str, value: int, max_value: int, symbol: str = "█", 
                fill_color: str = "green", background_color: str = "grey23", width: int = 20) -> str:
        """Draws a progress bar with custom label, colors, and symbol."""
        filled_length = int((value / max_value) * width)
        bar = (
            f"[{fill_color}]{symbol * filled_length}[/{fill_color}]"
            f"[{background_color}]{symbol * (width - filled_length)}[/{background_color}]"
        )
        return f"[bold]{label}[/bold] {value}/{max_value} {bar}"


    def get_vitals(hp: int, max_hp: int, mp: int, max_mp: int, exp: int, max_exp: int) -> str:
        """Vitals Panel using custom bars for HP, MP, and EXP"""
        hp_bar = draw_bar("󰛨 HP", hp, max_hp, symbol="/", fill_color="green_yellow", background_color="dark_orange3")
        mp_bar = draw_bar(" MP", mp, max_mp, symbol="/", fill_color="bright_cyan", background_color="dark_orange3")
        exp_bar = draw_bar("󰫍 EXP", exp, max_exp, symbol="|", fill_color="gold1", background_color="grey37")
        return f"{hp_bar}\n{mp_bar}\n{exp_bar}"
    grid.add_row(
        Panel(
            renderable=get_vitals(   core.player.hp,    core.player.max_hp,    core.player.mp,    core.player.max_mp,    core.player.exp, 1000),
            title="Vitals",
            title_align="right",
            border_style="bold light_slate_grey",
        )
    )
    grid.add_row(
        Panel(
            renderable=stat_grid,
            title="Stats",
            title_align="right",
            border_style="bold light_slate_grey",
        )
    )
    # grid.add_row(   core.job_progress)
    

    from art import text2art
    


    from typing import Dict, Tuple

    def create_inventory_panel(
        armor_items: Dict[str, Dict[str, str]],
        weapon_items: Dict[str, Dict[str, str]],
        title: str = "[b green]\uf0b1 Inventory[/b green]",
        title_align: str = "right",
        border_style: str = "dim blue",
        padding: Tuple[int, int] = (0, 1)
    ) -> Panel:
        inventory_lines = []

        if armor_items:
            inventory_lines.append("[bold yellow]\uf132 Armor[/bold yellow]")
            for name, data in armor_items.items():
                icon = data.get("icon", "?")
                style = data.get("style", "default")
                inventory_lines.append(f"  [{style}]{icon} {name}[/{style}]")

        if armor_items and weapon_items:
            inventory_lines.append("")

        if weapon_items:
            inventory_lines.append("[bold bright_red]\uea0e Weapons[/bold bright_red]")
            for name, data in weapon_items.items():
                icon = data.get("icon", "?")
                style = data.get("style", "default")
                inventory_lines.append(f"  [{style}]{icon} {name}[/{style}]")

        if not inventory_lines:
            inventory_lines.append("[dim]Empty[/dim]")

        inventory_renderable = "\n".join(inventory_lines)

        return Panel(
            inventory_renderable,
            title=title,
            title_align=title_align,
            border_style=border_style,
            padding=padding
        )
    current_armor = {
            "Leather Jacket": {"icon": "\uea8d", "style": "grey"},
            "Hat of Death": {"icon": "\uf6e5", "style": "red1"},
            "Boots of Truth": {"icon": "\uf54c", "style": "red1"}
        }

    current_weapons = {
            "Sword": {"icon": "\uf530", "style": "default"},
            "Shield": {"icon": "\uf132", "style": "default"},
            "Rusty Axe": {"icon": "\uea0b", "style": "bright_black"}
        }
    grid.add_row( create_inventory_panel(current_armor, current_weapons) )


    def create_task_panel(
        tasks: List[str],
        title: str = "[b yellow]\uf0ae Tasks[/b yellow]",
        title_align: str = "left",
        border_style: str = "dim green",
        padding: Tuple[int, int] = (0, 1),
        task_icon: str = "\uf10c"
    ) -> Panel:
        task_lines = [f"  {task_icon} {task}" for task in tasks] if tasks else ["[dim i]No active tasks.[/dim i]"]
        return Panel(
            "\n".join(task_lines),
            title=title,
            title_align=title_align,
            border_style=border_style,
            padding=padding
        )
    current_tasks = [
        "Kill 3 Slimes",
        "Collect 5 Herbs",
        "Report back to the Guild Master",
        "Investigate the Whispering Cave"
    ]
    task_panel = Padding(
        renderable="Taks :\nkill 3 snakes \n Make it alive \n Kill the great snake"
    )
    grid.add_row(create_task_panel(current_tasks))
    
    return grid

def command_mode_layout(core):
    from rich.table import Table

    grid = Table.grid(expand=True)
    grid.add_column()
    stext = "t"
    try:
        stext = core.current_entry_text
    except Exception:
        stext = "hehe"
    grid.add_row(
        Panel(
            f"> + {stext}",
            title="input",
            title_align="right",
            border_style="green",
            expand=True,
        )
    )

    hgrid = Table.grid(expand=True)
    hgrid.add_column()
    instructions = "just running "
    grid.add_row(
        Padding(
            instructions,
 
            expand=True,
        )
    )

    @group()
    def layout():
        yield grid
        yield hgrid

    return Panel(layout(),border_style="dim cyan1")
def input_mode_layout(core:"Core"):
    from rich.table import Table

    grid = Table.grid(expand=True)
    grid.add_column()
    stext = "t"
    try:
        stext = core.current_entry_text
    except Exception:
        stext = "hehe"
    grid.add_row(
        Panel(
            f"> + {stext}",
            title="input",
            title_align="right",
            border_style="green",
            expand=True,
           
        )
    )

    return grid


import random
from typing import List, Dict, Tuple # Added Tuple for consistency

from rich.panel import Panel
from rich.table import Table
from rich.text import Text # Included for consistency, though not directly used for new Text objects
from rich_pixels import Pixels # Assuming rich_pixels is installed

from rich.console import Console
from rich.layout import Layout
from rich.padding import Padding # For the main layout example
# It's good practice to have the draw_bar function accessible if it's not globally defined
# or passed around. Assuming it's available in the same scope or imported.
# If not, you'd redefine it here or in a shared utility module.
# For this example, I'll copy it here for completeness of the enemy_tab section.

def draw_enemy_bar(label: str, value: int, max_value: int, symbol: str = "█",
             fill_color: str = "green", background_color: str = "grey23", width: int = 20) -> str:
    """Draws a progress bar with custom label, colors, and symbol."""
    # Ensure value does not exceed max_value for bar calculation
    value = min(value, max_value)
    if max_value == 0: # Avoid division by zero
        filled_length = 0
    else:
        filled_length = int((value / max_value) * width)
    
    bar_fill = symbol * filled_length
    bar_empty = symbol * (width - filled_length)
    
    # Applying colors separately to fill and empty parts
    return f"[bold]{label}[/bold] {value}/{max_value} [{fill_color}]{bar_fill}[/{fill_color}][{background_color}]{bar_empty}[/{background_color}]"


# Define a placeholder Enemy class for demonstration
class Enemy:
    def __init__(self, name: str, hp: int, max_hp: int, attack: int, defense: int, speed: int,
                 image_paths: List[str], description: str = "A fearsome foe.",
                 loot: List[str] = [], abilities: List[str] = [],
                 icon_resize: Tuple[int, int] = (16, 16),
                 xp_value: int = 0, level: int = 1):
        self.name = name
        self.hp = hp
        self.max_hp = max_hp
        self.attack = attack
        self.defense = defense
        self.speed = speed
        self.image_paths = image_paths
        self.description = description
        self.loot = loot if loot else []
        self.abilities = abilities if abilities else []
        self.icon_resize = icon_resize
        self.xp_value = xp_value
        self.level = level
        # For draw_bar, an enemy might have a 'fury' or 'stamina' bar instead of MP/EXP
        # For simplicity, we'll focus on HP for the enemy vitals bar.


def enemy_tab(enemy: Enemy):
    """
    Creates a Rich renderable tab for displaying enemy information,
    including a pixel art image, vitals, stats, and other details.
    """
    grid = Table.grid(expand=True)
    grid.add_column() # Single column layout for the main grid

    # --- Enemy Image Panel ---
    if enemy.image_paths:
        icon_path = random.choice(enemy.image_paths)
        try:
            # Attempt to load pixels, ensure image path is valid and accessible
            pixels = Pixels.from_image_path(icon_path, resize=enemy.icon_resize)
            # The user's example used a sub-grid for the image panel, which is fine.
            # Alternatively, the Panel can directly contain the Pixels object.
            image_panel_content = pixels
        except Exception as e: # Catch potential errors like FileNotFoundError
            # Fallback text if image loading fails
            image_panel_content = Text(f"Error loading image:\n{icon_path}\n{e}", style="bold red")
    else:
        image_panel_content = Text("No Image", style="dim_italic")

    # Panel for the image itself, styled for an enemy
    # The user's snippet mentioned width=23 for the image panel
    image_display_panel = Panel(
        image_panel_content,
        title=f"[b white on red]\uf071 {enemy.name} (Lvl {enemy.level}) \uf071[/b white on red]", # Using a skull icon or similar for enemy
        title_align="center",
        border_style="bold red",
        expand=False, # As per user's example for the image panel part
        width=(enemy.icon_resize[0] * 2) + 7 if enemy.image_paths else 23 # Adjust width based on image, or fixed
    )
    grid.add_row(image_display_panel)


    # --- Enemy Vitals Panel ---
    # Simplified vitals for enemy, focusing on HP
    # Using different colors and symbols for the enemy HP bar
    enemy_hp_bar = draw_enemy_bar(
        label="HP", # Simpler label for enemy
        value=enemy.hp,
        max_value=enemy.max_hp,
        symbol="=", # Different symbol
        fill_color="bright_red",
        background_color="rgb(50,0,0)", # Dark red background
        width=25 # Slightly wider bar
    )
    vitals_panel = Panel(
        enemy_hp_bar,
        title="[b red]\uf21e Vitals[/b red]", # Heartbeat icon
        title_align="left",
        border_style="red"
    )
    grid.add_row(vitals_panel)

    # --- Enemy Stats Panel ---
    stat_grid = Table.grid(expand=True, padding=(0,1))
    stat_grid.add_column(style="bright_yellow", justify="right", width=10) # Stat name
    stat_grid.add_column(style="white", justify="left") # Stat value

    # Defining enemy stats to display
    enemy_stats_display = {
        "Attack": enemy.attack,
        "Defense": enemy.defense,
        "Speed": enemy.speed,
        "XP Value": enemy.xp_value,
    }
    for key, value in enemy_stats_display.items():
        stat_grid.add_row(f"{key}:", str(value))

    stats_panel = Panel(
        stat_grid,
        title="[b red1]Estadísticas[/b red1]", # Using a generic stats/monster icon (placeholder)
        title_align="left",
        border_style="orange_red1"
    )
    grid.add_row(stats_panel)

    # --- Enemy Description/Abilities Panel ---
    info_lines = []
    if enemy.description:
        info_lines.append(f"[i grey70]{enemy.description}[/i grey70]")
        info_lines.append("") # Spacer

    if enemy.abilities:
        info_lines.append("[bold bright_red]Abilities:[/bold bright_red]")
        for ability in enemy.abilities:
            info_lines.append(f"  \uf118 {ability}") # Using a generic "skill" or "action" icon

    if enemy.loot:
        info_lines.append("") # Spacer
        info_lines.append("[bold gold1]Potential Loot:[/bold gold1]")
        for item in enemy.loot:
            info_lines.append(f"  \uf0b0 {item}") # Gem icon for loot

    if not info_lines:
        info_lines.append("[dim]No additional intel.[/dim]")

    intel_renderable = "\n".join(info_lines)
    intel_panel = Panel(
        intel_renderable,
        title="[b grey50]\uf21b Intel[/b grey50]", # Scroll icon for intel/description
        title_align="left",
        border_style="grey37",
        padding=(1, 2)
    )
    grid.add_row(intel_panel)

    return grid



# --- Player Tab (for context, slightly modified from your original) ---
# Assuming 'stats_tab' would be a function similar to the stat display logic
# For now, I'll inline a simple stat display for the player as well.



from PIL import Image
import os





goblin_enemy = Enemy(
    name="Cave Goblin",
    hp=30,
    max_hp=30,
    attack=8,
    defense=3,
    speed=10,
    image_paths="2.png", # Reusing dummy images
    description="A small, vicious creature lurking in the dark.",
    abilities=["Rusty Shiv", "Throw Rock"],
    loot=["Rupees", "Goblin Ear"],
    icon_resize=(16,16),
    xp_value=50,
    level=3
)





