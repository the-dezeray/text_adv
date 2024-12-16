from util.logger import Log
from ui.options import Option, WeaponOption
from core.player import Player

def deal_damage(core, weapon):
    """
    Deals damage to the entity and updates the options list with the damage dealt.

    Args:
        core: The core game object containing game state.
        weapon: The weapon used to deal damage.
    """
    core.entity.hp -= weapon.damage
    core.options.append(Option(text=f"[yellow]dealt[/yellow] {weapon.damage} damage", type="header", func=lambda: None, selectable=False))
    _fight(core)

def fight(entity=None, core=None):
    """
    Initiates a fight sequence.

    Args:
        entity: The entity to fight against.
        core: The core game object containing game state.
    """
    if entity is None:
        print("entity is required")
        Log.error("entity is required")
    else:
        core.options = []
        core.console.refresh()
        core.move_on = False
        core.entity = entity
        core.player.turn = True
        core.in_fight = True
        _fight(core)

def get_head_count(array):
    """
    Counts the number of header options in the given array.

    Args:
        array: The array of options.

    Returns:
        int: The count of header options.
    """
    return sum(1 for i in array if i.type == "header")

def _fight(core):
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
    core.options.append(Option(type="entity_profile", text=f"Player ❤ {player.hp}/50     ⚔ 5      🛡 100 "))
    core.options.append(Option(type="entity_profile", text=f"SNAKE ❤ {entity.hp}/50     ⚔ 5      🛡 100 "))

    if player.turn:
        core.options += core.ant
        core.ant = []
        for weapon in player.inventory.weapons(type = "attack"):
            core.options.append(WeaponOption(weapon=weapon, func=lambda w=weapon: deal_damage(core, w)))
        player.turn = False
        entity.turn = True
    else:
        core.options.append(last)
        core.options.append(Option(type="header", text="You prepare to defend "))
        for weapon in player.inventory.weapons(type="defence"):
            core.options.append(WeaponOption(weapon=weapon, func=lambda w=weapon: deal_damage(core, w)))
        entity.deal_damage(player)
        entity.turn = False
        player.turn = True

    if player.hp <= 0:
        if player.is_revivable():
            player.revive()
        else:
            pass  # console.print("you lose")

    if entity.hp <= 0:
        print("you win")
        core.move_on = True
        if core.next_node is not None and core.move_on:
            core.chapter_id = core.next_node
            for option in core.options:
                option.selectable = False
            core.game_loop()

    core.console.refresh()
