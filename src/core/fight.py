from util.logger import Log
from ui.options import Option,WeaponOption
def deal_damage(core,weapon):
    core.entity.hp -= weapon.damage
    core.options.append(Option(text = f"dealt {weapon.damage} damage",func=lambda : None,selectable = False))
    _fight(core)
def fight(entity = None,core = None):
    if entity == None:
        print("entity is required")
        Log.error("entity is required")
    else:
        core.options = []
        core.console.refresh()
        core.move_on = False
        core.entity = entity
        _fight(core)
def _fight(core):
  
    for option in core.options:
        option.selectable = False
    player = core.player
    console = core.console
    entity = core.entity
    player.turn = True
    
    if player.turn == True:
        for weapon in player.inventory.weapons():
            core.options.append(WeaponOption(weapon = weapon,func=lambda : deal_damage(core,weapon)))
          
        core.console.refresh()
        #player.show_actions(entity)
        player.turn = False
    else:
        entity.deal_damage(player)
        
    if player.hp <= 0:
        if player.is_revivable():
            player.revive()
        else:
            console.print("you lose")
            
    if entity.hp <= 0:
        console.print("you win")
        core.move_on = True
        if core.next_node != None and core.move_on != False :
            core.chapter_id = core.next_node
            for option in core.options:
                option.selectable = False
            core.game_loop()

        
