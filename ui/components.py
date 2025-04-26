from rich.table import Table
from rich.panel import Panel
from rich.padding import Padding
from rich.align import Align
from rich.console import group
from typing import List

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
    instructions = "goto \[chapter\] \nreload \nkill \nheal \nrestart"
    grid.add_row(
        Panel(
            instructions,
            title="input",
            title_align="right",
            border_style="yellow",
            expand=True,
        )
    )

    @group()
    def layout():
        yield grid
        yield hgrid

    return layout()
