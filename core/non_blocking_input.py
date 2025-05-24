
from readchar import readkey
from util.logger import logger

import threading
import queue
from typing import Optional

class NonBlockingInput:
    def __init__(self):
        self.input_queue = queue.Queue()
        self.running = True
        self.thread = threading.Thread(target=self._input_thread, daemon=True)
        self.thread.start()

    def _input_thread(self):
        while self.running:
            try:
                key = readkey()
                if key:
                    self.input_queue.put(key)
            except Exception as e:
                logger.error(f"Error in input thread: {e}")
                self.running = False

    def stop(self):
        self.running = False
        self.thread.join(timeout=1.0)

    def get_key(self) -> Optional[str]:
        try:
            return self.input_queue.get_nowait()
        except queue.Empty:
            return None

