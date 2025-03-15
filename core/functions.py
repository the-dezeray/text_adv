from util.logger import logger


def receive(item, core):
    core.player.inventory.add(item)
    logger.info(f"Player Received {item.name}")
    core.goto_next()
