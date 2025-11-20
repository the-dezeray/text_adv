import threading
import queue
import time
from typing import Optional

"""class Timer():
    def __init__(self):
        self._thread : Optional[threading.Thread] = None
    
    def create_timer(self,time:float ,func: callable):
        if not func:
            raise ValueError("function cannot be null")
        self._thread = threading.Thread(target=self.timer,args=(time,func),daemon=True)
    def _timer(self,time:float,func:callable):
        ...
    def close():
        ...
"""
class Timer():
    def __init__(self,time:float = 0 ,func:callable= None):
        self.time= time

        self.func = func
    def is_finished(self):
        return self.time <= 0
    