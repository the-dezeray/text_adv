from ui.options import Option, WeaponOption
from objects.player import Player
from ui.options import Choices, Reward
from util.logger import logger, event_logger
from typing import TYPE_CHECKING, Literal

if TYPE_CHECKING:
    from objects.item import Item
    from core.core import Core
    from objects.entities import entity


def deal_damage(core, weapon) -> None:
    """
    Deals damage to the entity and updates the options list with the damage dealt.

    Args:
        core: The core game object containing game state.
        weapon: The weapon used to deal damage.
    """
    core.entity.hp -= weapon.damage
    core.options.append(
        Option(
            text=f"[yellow]dealt[/yellow] {weapon.damage} damage",
            type="header",
            func=lambda: None,
            selectable=False,
        )
    )
    _fight(core)


@event_logger
def fight(
    entity: "entity" = None,
    core: "Core" = None,
    repeat: int = 0,
    reward: Literal["auto", None, "Item"] = None,
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


def get_head_count(array: list):
    """
    Counts the number of header options in the given array.
    Args:
        array: The array of options.

    Returns:
        int: The count of header options.
    """
    return sum(1 for i in array if i.type == "header")


def _fight(core) -> None:
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
    core.options.append(
        Option(
            type="entity_profile", text=f"Player ❤ {player.hp}/50     ⚔ 5      🛡 100 "
        )
    )
    core.options.append(
        Option(
            type="entity_profile", text=f"SNAKE ❤ {entity.hp}/50     ⚔ 5      🛡 100 "
        )
    )

    if player.turn:
        core.options += core.ant
        core.ant = []
        ary = player.inventory.weapons(type="attack")

        core.options.append(Choices(ary, core))
        player.turn = False
        entity.turn = True
    else:
        core.options.append(last)
        core.options.append(Option(type="header", text="You prepare to defend "))
        ary = player.inventory.weapons(type="defence")
        core.options.append(Choices(ary, core))
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
        core.options.append(
            Option(
                type="header",
                text="you attained the [red]sword of death![/]",
                selectable=False,
            )
        )
        from objects.weapon import Weapon

        w = Weapon.generate(name="sword")
        from ui.options import Selectables

        core.options.append(Choices(ary=[w, w], core=core))
        core.options.append(
            Choices(
                renderable=Option(text="You win!", selectable=True, func=core.goto_next)
            )
        )
