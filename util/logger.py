import logging


logging.basicConfig(level=logging.DEBUG,filename="log.log",filemode="w",format="%(levelname)s - %(message)s")

logger= logging.getLogger("central")
