"""handles program launch"""
import queue
import time

from main_layout import character_preview_layout,gameplay_layout,character_selection_layout
from pynput.keyboard  import Listener
from game import Game
from rich.console import Console
from rich.live import Live
console = Console()

def main():
    """Program Launch"""
    
    core = Game()

    with Listener(on_press= core.save_key) as core.key_listener:
        with Live(core.interface, refresh_per_second=10) as core.love:  # update 10  times a second to feel fluid
            
            while core.running: #if program has not been terminated
                pass
        core.key_listener.join()
    
                
if __name__ == "__main__":

    main()

