from core.core import Core
from core.events import *
from util.logger import logger
import traceback
from rich.live import Live
from rich.console import Console
from rich.layout import Layout
from typing import Dict, List, Optional, NamedTuple

class EventTestResult(NamedTuple):
    """Structured result for event testing."""
    success: bool
    event_index: int
    event_string: str
    node_id: Optional[str] = None
    function_name: Optional[str] = None
    error_message: Optional[str] = None
    full_traceback: Optional[str] = None

def test_event_string(event_string: str, core: Core, event_index: int) -> EventTestResult:
    """Test a single event string and return detailed results."""
    try:
        logger.info(f"Testing event string {event_index}: {event_string}")
        
        # Initialize rich live display for this test
        layout = Layout()
        with Live(layout, console=core.rich_console, auto_refresh=True) as live:
            core.rich_live_instance = live
            
            # Execute the event string using core's execute_yaml_function
            core.execute_yaml_function(event_string)
            logger.info(f"✓ Event string {event_index} executed successfully")
        
        return EventTestResult(
            success=True,
            event_index=event_index,
            event_string=event_string
        )
        
    except Exception as e:
        logger.error(f"✗ Event string {event_index} failed with error: {str(e)}")
        
        # Extract function name from event string if possible
        function_name = extract_function_name(event_string)
        
        return EventTestResult(
            success=False,
            event_index=event_index,
            event_string=event_string,
            function_name=function_name,
            error_message=str(e),
            full_traceback=traceback.format_exc()
        )

def extract_function_name(event_string: str) -> Optional[str]:
    """Extract function name from YAML event string."""
    try:
        # Simple extraction - look for function name after 'function:' or similar
        lines = event_string.strip().split('\n')
        for line in lines:
            if 'function:' in line.lower():
                return line.split(':')[-1].strip()
            # Also check for direct function calls
            if line.strip() and not line.startswith('#') and not line.startswith('-'):
                return line.strip().split('(')[0] if '(' in line else line.strip()
    except:
        pass
    return None

def get_failed_events_summary(results: List[EventTestResult]) -> Dict:
    """Get a structured summary of failed events."""
    failed_events = [r for r in results if not r.success]
    
    summary = {
        'total_events': len(results),
        'successful_events': len(results) - len(failed_events),
        'failed_events': len(failed_events),
        'failures': []
    }
    
    for failure in failed_events:
        failure_info = {
            'event_index': failure.event_index,
            'function_name': failure.function_name,
            'event_string': failure.event_string,
            'error_message': failure.error_message,
            'error_type': type(eval(f"Exception('{failure.error_message}')")).__name__ if failure.error_message else None
        }
        summary['failures'].append(failure_info)
    
    return summary

def analyze_node_failures(results: List[EventTestResult], core: Core) -> Dict:
    """Analyze which nodes/functions are causing failures."""
    failed_results = [r for r in results if not r.success]
    
    analysis = {
        'failed_functions': {},
        'error_patterns': {},
        'node_analysis': []
    }
    
    # Group by function name
    for result in failed_results:
        func_name = result.function_name or 'unknown'
        if func_name not in analysis['failed_functions']:
            analysis['failed_functions'][func_name] = []
        analysis['failed_functions'][func_name].append(result)
    
    # Group by error type
    for result in failed_results:
        error_type = result.error_message.split(':')[0] if result.error_message else 'unknown'
        if error_type not in analysis['error_patterns']:
            analysis['error_patterns'][error_type] = []
        analysis['error_patterns'][error_type].append(result)
    
    return analysis

def main():
    """Main function that returns structured results instead of just printing."""
    # Initialize core with proper console setup
    core = Core()
    core.rich_console = Console(color_system="truecolor", style="bold black")
    
    # Get all event strings from the story
    event_strings = core.game_engine.get_all_events()
    
    if not event_strings:
        logger.error("No event strings found in the story!")
        return None
    
    # Test each event string
    results = []
    for i, event_string in enumerate(event_strings, 1):
        result = test_event_string(event_string, core, i)
        results.append(result)
    
    # Generate summary
    summary = get_failed_events_summary(results)
    analysis = analyze_node_failures(results, core)

    # Print concise summary
    core.console.print(f"\n=== Story Event Test Results ===")
    core.rich_console.log(f"Total: {summary['total_events']} | Success: {summary['successful_events']} | Failed: {summary['failed_events']}")
    
    if summary['failed_events'] > 0:
        print(f"\nFailed Events:")
        for failure in summary['failures']:
            print(f"Event {failure['event_index']}: {failure['function_name']} - {failure['error_message'][:50]}...")
    
    # Return structured data for further processing
    ad ={
        'results': results,
        'summary': summary,
        'analysis': analysis
    }
    test_data = ad
    
    # You can now access specific failure information:
    if test_data and test_data['summary']['failed_events'] > 0:
        core.console.print("\nDetailed failure analysis available in test_data variable")
        # Example: Get all failed function names
        failed_functions = list(test_data['analysis']['failed_functions'].keys())
        core.console.print(f"Functions that failed: {failed_functions}")

# Alternative: Just get the failure data without printing
def get_failure_data_only():
    """Get only the failure data without any console output."""
    core = Core()
    core.rich_console = Console(color_system="truecolor", style="bold black")
    
    event_strings = core.game_engine.get_all_events()
    if not event_strings:
        return None
    
    failures = []
    for i, event_string in enumerate(event_strings, 1):
        try:
            layout = Layout()
            with Live(layout, console=core.rich_console, auto_refresh=True) as live:
                core.rich_live_instance = live
                core.execute_yaml_function(event_string)
        except Exception as e:
            failures.append({yout()
                'event_index': i,
                'event_string': event_string,
                'function_name': extract_function_name(event_string),
                'error': str(e),
                'traceback': traceback.format_exc()
            })
    
    return failures

if __name__ == "__main__":
    # Use main() for full analysis or get_failure_data_only() for just failures
    test_data = main()
    from rich.console import Console
    from rich.style import Style
    console = Console()

    base_style = Style.parse("cyan")
    console.log("Hello, World", style = base_style + Style(underline=True))
    # You can now access specific failure information:
    if test_data and test_data['summary']['failed_events'] > 0:
        print("\nDetailed failure analysis available in test_data variable")
        # Example: Get all failed function names
        failed_functions = list(test_data['analysis']['failed_functions'].keys())
        print(f"Functions that failed: {failed_functions}")