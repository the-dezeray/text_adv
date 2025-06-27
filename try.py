from rich.console import Console
from rich.text import Text
import time

console = Console()

def display_status_effect(
    effect_name: str,
    target: str,
    description: str,
    icon: str,
    color: str,
    duration: int = 0
):
    """
    Displays a minimal, one-line status effect notification.
    """
    
    # The '»' character (U+00BB) acts as a clean separator
    separator = Text(" » ", style="dim")
    
    # Build the text components
    icon_text = Text(f"{icon} {effect_name}", style=f"bold {color}")
    target_text = Text(target, style="bold white")
    description_text = Text(f" {description}", style="italic")
    
    # Assemble the final line
    output_text = Text.assemble(
        icon_text,
        separator,
        target_text,
        description_text
    )

    # Add duration if provided
    if duration > 0:
        duration_text = f" ({duration} turns)"
        output_text.append(duration_text)
        from rich.panel import Panel
        output_text = Panel(" you have  been fozen \n [red]|||[/red]||||  [bold]-35#[/bold] ",border_style = f"{color}",title=icon_text,title_align="left",expand=False,width=40 ,subtitle="-35HP",subtitle_align="right")

    console.print(output_text)
    time.sleep(0.5) # A shorter sleep for a quick effect


# --- Example Usage ---

# 1. The requested "Frost" effect
display_status_effect(
    effect_name="Frost",
    target="You",
    description="are slowed.",
    icon="",  # Nerd Font: nf-weather-snowflake
    color="bright_cyan",
    duration=3
)

# 2. A "Poison" debuff example
display_status_effect(
    effect_name="Poison",
    target="Goblin",
    description="is taking damage over time.",
    icon="",  # Nerd Font: nf-md-skull_crossbones
    color="bright_green",
    duration=5
)

# 3. A "Haste" buff example
display_status_effect(
    effect_name="Haste",
    target="You",
    description="feel faster!",
    icon="ﯙ",  # Nerd Font: nf-fa-bolt
    color="yellow",
    duration=4
)