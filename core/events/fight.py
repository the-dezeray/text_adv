from ui.options import Option, WeaponOption
from objects.player import Player
from ui.options import Reward,buffer_create_weapons
from util.logger import logger, event_logger
from typing import TYPE_CHECKING, Literal
from ui.options import ui_text_panel,choose_me
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
    core.options.append(
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
        core.options = []
        core.console.refresh()
        core.move_on = False
        core.entity = entity
        core.player.turn = True
        core.in_fight = True
        core.console.initialize_fight_mode()
        _fight(core)





def _fight(core: "Core") -> None:
    """
    Handles the fight logic, alternating turns between the player and the entity.

    Args:
        core: The core game object containing game state.
    """
    for option in core.options:
        option.selectable = False

    player: Player = core.player
    entity = core.entity

    if len(core.options) > 1:
        last = core.options[-1]

    core.options = []


    if player.turn:
        core.options += core.ant
        core.ant = []
        ary = player.inventory.weapons(type="attack")
        core.options.append(ui_text_panel(text="You prepare to attack"))
        core.options.append(buffer_create_weapons(ary, core))
        player.turn = False
        entity.turn = True
    else:
        core.options.append(last)


        core.options.append(ui_text_panel( text="You prepare to defend "))
        ary = player.inventory.weapons(type="defence")
        core.options.append(buffer_create_weapons(ary, core))
        entity.deal_damage(player)
        entity.turn = False
        player.turn = True

    if player.hp <= 0:
        if player.is_revivable():
            player.revive()
        else:
            pass  # console.print("you lose")

    if entity.hp <= 0:
        core.options = []
        core.options.append(ui_text_panel(text="you attained the [red]sword of death![/]"))
        from objects.weapon import Weapon

        w = Weapon.generate(name="sword")
   
        a = choose_me(text="You win!", func=core.goto_next)
        core.options.append(choose_me(text="You win!", func=core.goto_next) )
        core.options.append(buffer_create_weapons(ary=[w, w], core=core,extra=True))

