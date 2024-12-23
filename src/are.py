from rich.console import Console
from rich.spinner import Spinner
console = Console()
console.input("What is [i]your[/i] [bold red]name[/]? :smiley: ")
console.rule("[bold red]Chapter 1")
spinner = Spinner("dots", text="Loading...")
