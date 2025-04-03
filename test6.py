from rich.live import Live
from rich.layout import Layout
from rich.panel import Panel
from rich.console import Console
from rich.text import Text
from rich import box
from time import sleep
import random
import os

# Define temp functions to simulate actual work
def check_music_files():
    """Simulate checking music files."""
    sleep(0.1)
    return f"Found {random.randint(10, 200)} music files"

def check_pictures():
    """Simulate checking pictures."""
    sleep(0.1)
    return f"Found {random.randint(50, 500)} pictures"

def check_config():
    """Simulate checking configuration."""
    sleep(0.1)
    return "Configuration verified"

def check_updates():
    """Simulate checking for updates."""
    sleep(0.1)
    return f"Found {random.randint(0, 5)} updates"

def test_sound():
    """Simulate testing sound."""
    sleep(0.1)
    return "Sound system working"

def check_nerd_font():
    """Simulate checking nerd font."""
    sleep(0.1)
    return f"{random.randint(3, 10)} nerd fonts installed"
def test():
    # Map function names to actual functions
    functions = {
        "checking music files": check_music_files,
        "checking pictures": check_pictures,
        "checking config": check_config,
        "checking updates": check_updates,
        "testing sound": test_sound,
        "checking nerd font": check_nerd_font
    }

    # Function results storage
    results = {}

    # Create the layout
    layout = Layout(name="main",size=7)


    # Run the process with live display
    with Live(layout, auto_refresh=True,) as live:
        for i, (func_name, func) in enumerate(functions.items()):
            # Create status list with current function marked as processing
            status_lines = []
            for j, (name, _) in enumerate(functions.items()):
                if j < i:
                    # Completed functions with checkmark and result
                    status_lines.append(f"[green]✓[/green] {name}: [green]{results[name]}[/green]")
                elif j == i:
                    # Current function being processed
                    status_lines.append(f"[yellow]⟳[/yellow] [bold yellow]{name}[/bold yellow] [yellow]processing...[/yellow]")
                else:
                    # Pending functions
                    status_lines.append(f"[grey]□[/grey] {name}")
            
            # Update the layout with current status
            status_text = "\n".join(status_lines)
            layout.update(status_text)
            
            # Actually run the function
            result = func()
            results[func_name] = result

        
        # All tasks completed
        status_lines = [f"[green]✓[/green] {name}: [green]{results[name]}[/green]" for name in functions.keys()]
        status_text = "\n".join(status_lines)
        layout.update(status_text)
        live.stop()
