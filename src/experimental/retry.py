
import threading 
from rich.live import Live
from pynput.keyboard  import Listener
from rich.console import Console
from core.core import Core
from input.keyboard import Keyboard_control
from rich.traceback import install
from rich.layout import Layout
from rich.table import Table
import time 
import random

install(show_locals=True)
def update_gui():
    
    table = Table()
    table.add_column("ID")
    table.add_column("Value")
    table.add_column("Status")

    for row in range(random.randint(2, 6)):
        value = random.random() * 100
        table.add_row(
            f"{row}", f"{value:3.2f}", "[red]ERROR" if value < 50 else "[green]SUCCESS"
        )
    return table


def main():
    a = Layout(name="main")
    
    threading.Thread(target = update_gui,daemon=True).start()
    with Live(a, refresh_per_second=4) as live:
        while True:
            live.update()


            
if __name__ == "__main__":

    main()

