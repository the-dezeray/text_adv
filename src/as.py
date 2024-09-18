"""handles program launch"""
import queue
import time

from pynput.keyboard  import Listener
from rich.live import Live
from rich.table import Table
from rich.layout import Layout
from rich.panel import Panel
from rich.padding import Padding
from rich.console import Console,Group
from rich.spinner import Spinner

console = Console()


def make_layout() -> Layout:
    """return a structured Layout object

    Returns:
        Layout: Layout object
    """
    layout = Layout(name="root") 
    layout.split(
        Layout(name = "header",size =2),
        Layout(name="main", size = 3),
        Layout(name = "suggestion",size=3),
        
        Layout(name = "view",ratio=2),

    )
    
    layout["header"].update(Padding(pad=(0,70),renderable=Spinner(name="dots12")))
    
    return layout
class Core():
    def __init__(self,interface) -> None:
        self.running = True
    def save_key(self,key):
        pass
def main():

    """Program Launch"""
    layout = make_layout()
    core = Core(interface = layout)
    core.table =  Table(expand=True,show_edge=False)
    core.table.add_column()
    layout["view"].update(Padding(core.table,pad =(0,40),expand=True))

    #listens for keyboard key press
    with Listener(on_press= core.save_key) as L:
        #Renders an auto-updating terminal
        with Live(layout, refresh_per_second=10):  # update 10  times a second to feel fluid
            
            while core.running: #if program has not been terminated
                layout["main"].update(Padding(Panel("hello"),pad =(0,20)))
                layout["suggestion"].update(Padding("hi hi",pad =(0,20),expand=True))

        L.join()
    
                
if __name__ == "__main__":

    main()
