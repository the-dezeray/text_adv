import threading
import time
from rich.live import Live
from rich.layout import Layout
from rich.table import Table

# Shared variable (Rich Layout)
shared_variable = Layout(name="main")

# Lock for synchronization
lock = threading.Lock()

# Function for the thread
def update_gui():
    global shared_variable
    table = Table()
    table.add_column("Data")
    
    while True:
        with lock:  # Lock while modifying the variable
            table.add_row("New Row Added")
            shared_variable.update(table)  # Update the layout with the table
        
        time.sleep(1)  # Simulate work

# Main function
def main():
    global shared_variable
    
    # Start the thread
    thread = threading.Thread(target=update_gui, daemon=True)
    thread.start()

    # Live display of the layout
    with Live(shared_variable, refresh_per_second=4) as live:
        while True:
            time.sleep(0.1)  # Avoid CPU overuse

if __name__ == "__main__":
    main()
