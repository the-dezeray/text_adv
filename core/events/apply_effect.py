from ui.options import ui_text_panel
from rich.panel import Panel
from rich.text import Text
from rich.align import Align
from rich.padding import Padding
from rich.table import Table
def apply_effect( effect=None, duration=None, core=None, str=None) -> None:

    # Effect data
    effect_name = "Frost"
    target = "You"
    description = "are frozen in place, limbs stiff with cold."
    icon = ""  # Nerd Font: nf-weather-snowflake
    color = "cyan1"
    duration = 3
    damage = -35


    # Create stylized content
    title_text = Text(f"{icon} {effect_name.upper()}", style=f"bold {color}")
    description_text = Text(f"{target} {description}", style="white")
    damage_text = Text(f" {damage} HP", style="bold red")  # Nerd Font: nf-md-heart_broken

    # Optional extra info (like duration)
    duration_text = Text(f" {duration} turns", style="dim")  # Nerd Font: nf-fa-hourglass_half

    # Table layout for clean structure
    table = Table.grid(padding=(0, 1))
    table.add_row(description_text)
    table.add_row(damage_text, duration_text)

    # Build the final panel
    panel = Panel(
        Align.center(table),
        title=title_text,
        title_align="left",
        subtitle="Status Effect",
        subtitle_align="right",
        border_style=color,
        expand=True,
        width=60
    )

    # Apply padding for vertical spacing
    pretty_output = Align(Padding(panel,pad=(2,0,0,0)),align="center")

    # Display

    core.console.print(pretty_output)

    
    core.goto_next()

def remove_effect( effect=None, duration=None, core=None, str=None) -> None:
    core.console.print(ui_text_panel(text=str))
    core.goto_next()