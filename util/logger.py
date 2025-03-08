"""This module is used to log the messages in the log file."""
import logging

logging.basicConfig(level=logging.DEBUG,filename="log.log",filemode="w",format="%(filename)s - %(levelname)s - %(message)s")
logger= logging.getLogger("central")

def event_logger(func)->callable:
    '''log the call of a cution'''
    def wrapper(*args, **kwargs):
        logger.info(f"Calling function: {func.__name__} with args: {args} and kwargs: {kwargs}")
        result = func(*args, **kwargs)
        print(f"Function {func.__name__} returned: {result}")
        return result
    return wrapper

