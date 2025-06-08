from core.core import Core
from core.events import *
from util.logger import logger
import traceback
from rich.live import Live
from rich.console import Console
from rich.layout import Layout

def test_event_string(event_string: str, core: Core) -> bool:
    """Test a single event string from the story."""
    try:
        logger.info(f"Testing event string: {event_string}")
        # Initialize rich live display for this test
        layout = Layout()
        with Live(layout, console=core.rich_console, auto_refresh=True) as live:
            core.rich_live_instance = live
            # Execute the event string using core's execute_yaml_function
            core.execute_yaml_function(event_string)
        logger.info(f"✓ Event string executed successfully")
        return True
    except Exception as e:
        logger.error(f"✗ Event string failed with error: {str(e)}")
        logger.error(traceback.format_exc())
        return False

def main():
    # Initialize core with proper console setup
    core = Core()
    core.rich_console = Console(color_system="truecolor", style="bold black")
    
    # Get all event strings from the story
    event_strings = core.game_engine.get_all_events()
    
    if not event_strings:
        logger.error("No event strings found in the story!")
        return
    
    # Test each event string
    results = {}
    for i, event_string in enumerate(event_strings, 1):
        results[f"Event {i}"] = test_event_string(event_string, core)
    
    # Print summary
    print("\n=== Story Event Test Summary ===")
    successful = sum(1 for result in results.values() if result)
    total = len(results)
    print(f"Successfully tested: {successful}/{total} events")
    
    if successful < total:
        print("\nFailed events:")
        for event_name, success in results.items():
            if not success:
                print(f"- {event_name}")
                print(f"  Event string: {event_strings[int(event_name.split()[1]) - 1]}")

if __name__ == "__main__":
    main()
