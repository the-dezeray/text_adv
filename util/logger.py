"""This module is used to log the messages in the log file."""
import logging

logging.basicConfig(level=logging.DEBUG,filename="log.log",filemode="w",format="%(filename)s - %(levelname)s - %(message)s")
logger= logging.getLogger("central")
