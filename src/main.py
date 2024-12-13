"""handles program launch"""

from rich.live import Live
from pynput.keyboard  import Listener
from rich.console import Console
from core.core import Core
from input.keyboard import Keyboard_control
from rich.traceback import install
install(show_locals=True)
def main():

    core = Core()
    keyboard_controller = Keyboard_control(core = core)
    
   # console.color_system =None
    with Listener(on_press= keyboard_controller.execute_on_key) as core.key_listener:
        with Live(core.interface, refresh_per_second=10) as core.love:
           
       
            core.continue_game()
            while core.running:
                pass
        core.key_listener.join()
             
if __name__ == "__main__":

    main()


