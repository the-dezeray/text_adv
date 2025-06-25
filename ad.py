from core.core import Core
from core.events import *
from util.logger import logger
import traceback
from rich.live import Live
from rich.console import Console
from rich.layout import Layout

def test_event(event_name, event_func, core):
    """Test a single event and log the results."""
    try:
        logger.info(f"Testing event: {event_name}")
        # Initialize rich live display for this test
        layout = Layout()
        with Live(layout, console=core.rich_console, auto_refresh=True) as live:
            core.rich_live_instance = live
            event_func(core)
        logger.info(f"✓ {event_name} completed successfully")
        return True
    except Exception as e:
        logger.error(f"✗ {event_name} failed with error: {str(e)}")
        logger.error(traceback.format_exc())
        return False

def main():
    # Initialize core with proper console setup
    core = Core()
    core.rich_console = Console(color_system="truecolor", style="bold black")
    
    # Get all available events
    events = {
        'explore': explore,
        'fight': fight,
        'rest': rest,
        'read': read,
        'run': run,
        'trap': trap,
        'sneak': sneak,
        'apply_effect': apply_effect,
        'attempt_steal': attempt_steal,
        'interact': interact,
        'investigate': investigate,
        'shop': shop,
        'skill_check': skill_check,
        'receive_item': receive_item,
        'attempt_escape': attempt_escape
    }
    
    # Test each event
    results = {}
    for event_name, event_func in events.items():
        results[event_name] = test_event(event_name, event_func, core)
    
    # Print summary
    print("\n=== Event Test Summary ===")
    successful = sum(1 for result in results.values() if result)
    total = len(results)
    print(f"Successfully tested: {successful}/{total} events")
    
    if successful < total:
        print("\nFailed events:")
        for event_name, success in results.items():
            if not success:
                print(f"- {event_name}")
                print(f"  Function: {event_func}")

if __name__ == "__main__":
    main()



