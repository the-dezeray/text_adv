from rich import print
from rich.console import group
from rich.panel import Panel

@group()
def get_panels():
    yield Panel("Hello", style="bold blue")
    yield Panel("World", style="bold  red")

print(Panel(get_panels()))