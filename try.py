from rich.live import Live
from rich.layout import Layout
from rich.table import Table
from time import sleep
import random

# Create a shared mutable table
table = Table(title="📊 Temperature Logs")
table.add_column("Time", style="bold cyan")
table.add_column("Temperature (°C)", style="bold green")

# Create a layout and assign table to a visible area
layout = Layout()
layout.split_column(
    Layout(name="header", size=3),
    Layout(name="body"),
)

layout["header"].update("[bold magenta]Live System Monitor")
layout["body"].update(table)
def a():
    b = Table(title="📊 Temperature Logs")
    b.add_column("Time", style="bold cyan")
    b.add_column("Temperature (°C)", style="bold green")
    for i in range(1):
        temp = round(random.uniform(20.0, 30.0), 2)
        b.add_row(f"{i+1}s", f"{temp}")
        yield b
# Start live auto-refresh
with Live(layout, refresh_per_second=5, auto_refresh=True):
    for i in range(10):
        # Add a new row to the table (mutating in-place)
        temp = round(random.uniform(20.0, 30.0), 2)
        table.add_row(f"{i+1}s", f"{temp}")
        sleep(1)
