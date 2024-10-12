from logger import Log
from options import Option,WeaponOption
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
            core.options.append(WeaponOption(weapon = weapon,func=lambda : _fight(core)))
          
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

        
