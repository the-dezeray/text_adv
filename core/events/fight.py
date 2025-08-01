from ui.options import CustomRenderable, create_weapon_option
from objects.player import Player
from ui.options import Reward,GRID,WEAPON
from util.logger import logger, event_logger
from typing import TYPE_CHECKING, Literal
from ui.options import ui_text_panel,Option
if TYPE_CHECKING:
    from objects.item import Item
    from core.core import Core
    from objects.entities import entity
    from objects.weapon import Weapon

REWARDS = Literal["auto", None, "Item"]
def deal_damage(core:"Core", weapon:"Weapon") -> None:
    """Deals damage to the entity and updates the options list with the damage dealt.

    Args:
        core: The core game object containing game state.
        weapon: The weapon used to deal damage.
    Returns:
        None
    """
    core.entity.hp -= weapon.damage
    core.console.print(
        ui_text_panel(text=f"[yellow]dealt[/yellow] {weapon.damage} damage")
    )
    _fight(core)


@event_logger
def fight(
    core: "Core",
    entity: "entity",
    repeat: int = 0,
    reward: REWARDS = None,
) -> None:
    """
    Initiates a fight sequence.

    Args:
        entity: The entity to fight against.
        core: The core game object containing game state.
    """
    if entity is None:
        logger.info("entity is not defined in fight")

    else:
        core.console.clear_display()
        core.console.refresh()
        core.move_on = False
        core.entity = entity
        core.player.turn = True
        core.in_fight = True
        core.console.initialize_fight_mode()
        core.console.clear_display()
        _fight(core)


status_effect_styles = {
    # Positive/Utility
    "extra_turn": {"icon": "\U000F051F", "style": "bold grey"},      # 󰔟 nf-mdi-timelapse
    "haste":      {"icon": "\U000F08FE", "style": "bold cyan"},       # 󰣾 nf-mdi-run_fast
    "regen":      {"icon": "\U000F02D8", "style": "bold green"},      # 󰋘 nf-mdi-heart_pulse

    # Negative/Damage Over Time
    "burnt":     {"icon": "\U000F0238", "style": "red1"},    # 󰈸 nf-mdi-fire
    "poisoned":  {"icon": "\U000F10DB", "style": "green"},        # 󱃛 nf-mdi-flask_poison
    "bleeding":  {"icon": "\U000F1B87", "style": "red"},      # 󱮇 nf-mdi-water_opacity (looks like a drop)
    "frost":     {"icon": "\U000F072A", "style": "cyan"},         # 󰜪 nf-mdi-snowflake (can be DoT or slow)

    # Negative/Control & Debuff
    "stunned":   {"icon": "\U000F07A6", "style": "blue"}, # 󰞦 nf-mdi-flash
    "paralyzed": {"icon": "\U000F141E", "style": "blue"},         # 󱐞 nf-mdi-cancel
    "blinded":   {"icon": "\U000F06D0", "style": "grey70"},         # 󰛐 nf-mdi-eye_off
    "chilled":   {"icon": "\U000F005C", "style": "red1"},# 󰁜 nf-mdi-arrow_down_bold (representing slowness)
    "shock":     {"icon": "\U000F07A6", "style": "yellow"}       # 󰞦 nf-mdi-flash (reusing flash for shock trigger)
}


# Helper function (optional, place outside the main logic if preferred)
def _get_damage_color(damage_amount):
    """ Returns a Rich color style based on damage amount. """
    if damage_amount > 75:
        return "bold bright_red"
    elif damage_amount > 40:
        return "red"
    elif damage_amount > 20:
        return "orange_red1"
    else:
        return "dark_orange"

# --- End of code block to paste back ---
def hhhh(core):

    # Import necessary Rich components
    from rich.rule import Rule
    from rich.text import Text
    from rich.panel import Panel # Optional: for framing output

    # --- Player Action ---
    # nf-fa-user (U+F007)  | nf-mdi-sword (U+F04E9) 󰓩 | nf-mdi-skull (U+F04B4) 󰒴 (Goblin)
    player_icon = "\uf007"
    attack_icon = "\U000F04E9"
    target_icon = "\U000F04B4" # Assuming Goblin is represented by skull
    target_name = "Goblin"
    damage_amount = 45

    # 1. Rule to start the player's action sequence
    core.console.print(Rule(f"[bold sky_blue1]{player_icon} Player Turn[/]", style="sky_blue1", align="left"))

    # 2. Descriptive Attack Text
    attack_text = ui_text_panel(text = f"You lunge, {attack_icon} striking the {target_icon}[bold red]{target_name}[/bold red]!")
    core.console.print(attack_text)

    # 3. Damage Report - With Visual Bar
    #    Adjust the number of blocks based on damage or target HP%
    #    Here, we'll use a fixed number for simplicity, but you could scale it.
    damage_bar_char = "/" # U+2588 Full Block
    bar_length = 15 # Example length
    damage_bar = damage_bar_char * bar_length
    # nf-mdi-heart_broken (U+F0ECF) 󰻏
    damage_icon = "\U000F0ECF"
    core.console.print(
        ui_text_panel(text = f"{damage_icon} Dealt [bold bright_red]{damage_amount}[/] damage! [{_get_damage_color(damage_amount)}]{damage_bar}[/]")
    )
    # --- Start of section to replace ---

    # 4. Effects Applied - Displayed in one row within a panel using a Table
    effects_applied = {"frost": 1, "stunned": 2, "blinded": 1, "bleeding": 1, "chilled": 1}  # Example effects
    g =[]
    if effects_applied:
        from rich.table import Table
        from rich.panel import Panel

        # Create a table with no headers and no borders
        effects_table = Table.grid(padding=(0, 2))  # Slight horizontal padding between effects
        effects_table.expand = False

        # Add each effect as a column cell
        for effect, value in effects_applied.items():
            details = status_effect_styles.get(effect)
            if details:
                icon = details["icon"]
                style = details["style"]
                effect_text = Text(f"{icon} {effect.capitalize()} ({value})", style=style)
            else:
                # Fallback style for unknown effects
                effect_text = Text(f"{effect.capitalize()} ({value})", style="dim")
            effects_table.add_column(justify="left")
            effects_table.columns[-1].header = ""
            g.append(effect_text)
        effects_table.add_row(*g)
        # Create a header text with icon
        effects_header_icon = "\U000F025B"
        header = Text(f"{effects_header_icon} Effects Inflicted:", style="dim italic")

        # Wrap the row of effects in a panel
        effects_panel = Panel(effects_table, title=header, title_align="left", border_style="dim")

        # Append the panel to the core options
        core.console.print(effects_panel)


        # --- End of section to replace ---
        # 5. Special Events - Like Extra Turn from Shock
        shock_details = status_effect_styles.get("shock")
        extra_turn_details = status_effect_styles.get("extra_turn")

        # Example: Assume shock always grants an extra turn for this demo
        shock_triggered = True # Set this based on actual game logic

        if shock_triggered and shock_details and extra_turn_details:
            shock_icon = shock_details["icon"]
            shock_style = shock_details["style"]
            extra_turn_icon = extra_turn_details["icon"]
            extra_turn_style = extra_turn_details["style"]

            # Combine Shock trigger and Extra Turn result
            # nf-mdi-lightning_bolt (U+F0341) 󰍡 (alternative to flash)
            event_icon = "\U000F0341"
            extra_turn_line = ui_text_panel(text = f"{event_icon} [{shock_style}]Shock[/] ripples through the enemy! You gain an {extra_turn_icon}[{extra_turn_style}] Extra Turn![/]")
        
            line =  f"{event_icon} [{shock_style}]Impact[/] Skull Fructure  INCAPABLE OF CASTING MAGICAL SPELLS FOR 2 TURNS  [red1]BLEED [/red1]"
            core.console.print(Panel(renderable=line, title="Shock Triggered", border_style="yellow",title_align="left"))

            core.console.print(extra_turn_line)
        # Add elif/else for other potential special events (crits, misses, etc.)

        # 6. End of Player Action Rule
        core.console.print(Rule(style="sky_blue1"))    
def _fight(core: "Core") -> None:
    """
    Handles the fight logic, alternating turns between the player and the entity.

    Args:
        core: The core game object containing game state.
    """
    player: Player = core.player
    entity = core.entity

    # Clear previous renderables but keep the layout structure
    core.console.clear_display()
    
    # Display fight status
    from rich.rule import Rule
    from rich.text import Text
    
    # Show player and entity status
    status_text = f"[bold green]Player HP: {player.hp}[/bold green] | [bold red]Enemy HP: {entity.hp}[/bold red]"
    core.console.print(Rule(status_text, style="bold white"))
    
    # Display turn information
    turn_text = "[bold blue]Your Turn[/bold blue]" if player.turn else "[bold red]Enemy Turn[/bold red]"
    core.console.print(ui_text_panel(text=turn_text))

    if player.turn:
        # Player's turn
        core.console.print(ui_text_panel(text="Choose your weapon:"))
        ary = player.inventory.weapons(type="attack")
        from ui.options import GRID,WEAPON

        core.console.print(GRID(ary=ary, core=core,renderItem=WEAPON))
        
        # End player's turn
        player.turn = False
        entity.turn = True

    else:
        # Enemy's turn
        core.console.print(ui_text_panel(text="You prepare to defend"))
        ary = player.inventory.weapons(type="defence")
        core.console.print(GRID(ary=ary, core=core, renderItem=WEAPON))

        # Enemy attacks
        entity.deal_damage(player)
        entity.turn = False
        player.turn = True

    # Check for game over conditions
    if player.hp <= 0:
        if player.is_revivable():
            player.revive()
        else:
            core.console.print(ui_text_panel(text="[bold red]You have been defeated![/bold red]"))
            core.in_fight = False
            return

    if entity.hp <= 0:
        core.console.clear_display()
        core.console.print(ui_text_panel(text="[bold green]Victory![/bold green] You attained the [red]sword of death![/red]"))
        from objects.weapon import Weapon
        w = Weapon.generate(name="sword")
        core.console.print(Option(text="Continue your journey", func=core.goto_next))
        core.in_fight = False

