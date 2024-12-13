from util.logger import Log
from ui.options import Option,WeaponOption


def deal_damage(core,weapon):
    core.entity.hp -= weapon.damage
    core.options.append(Option(text = f"dealt {weapon.damage} damage",type = "header",func=lambda : None,selectable = False))
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
        core.player.turn = True
        core.in_fight = True
        _fight(core)
def get_head_count(array):
    count = 0
    for i in array:
        if i.type == "header":
            count += 1
    return count
def _fight(core):
  
    for option in core.options:
        option.selectable = False
    player = core.player
    console = core.console
    entity  = core.entity
    if len(core.options) > 1:
        last = core.options[-1]
    core.options = []
    core.options.append(Option(type= "header",text= f"❤ {player.hp}/50     ⚔ 5      🛡 100 "))
    core.options.append(Option(type= "header",text= f"❤ {entity.hp}/50     ⚔ 5      🛡 100 "))    

    if player.turn == True:
     

        core.options += core.ant
        core.ant = []
        for weapon in player.inventory.weapons():
            core.options.append(WeaponOption(weapon = weapon,func=lambda : deal_damage(core,weapon)))
          
        
        #player.show_actions(entity)
        player.turn = False
        entity.turn = True
    else:
        core.options.append(last)
        core.options.append(Option(type= "header",text= "You prepare to defend "))
        for weapon in player.inventory.weapons():
           core.options.append(WeaponOption(weapon = weapon,func=lambda : deal_damage(core,weapon)))
        entity.deal_damage(player)
        entity.turn = False
        player.turn = True
    if player.hp <= 0:
        if player.is_revivable():
            player.revive()
        else:
            pass
            #console.print("you lose")
    core.console.refresh()

    if entity.hp <= 0:
        
        print("you win")
        core.move_on = True
        if core.next_node != None and core.move_on != False :
            core.chapter_id = core.next_node
            for option in core.options:
                option.selectable = False
            core.game_loop()

        
