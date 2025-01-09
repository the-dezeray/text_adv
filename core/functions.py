
def receive(item,core ):
    core.player.inventory.add(item)
    core.goto_next()