from typing import Callable, TypeVar, Any
from util.logger import logger

T = TypeVar('T')

def window(window_generator: Callable[..., T]) -> Callable[..., T]:
    """Decorator that wraps window generation functions to handle UI state management.
    
    Args:
        window_generator: The function that generates the window content
        
    Returns:
        A wrapper function that handles adding the window to the navigation stack
    """
    def wrapper(core, *args: Any, **kwargs: Any) -> T:
        logger.info(f"Creating window with generator function {window_generator.__name__}")
        if not core.current_pane or core.current_pane[-1] != window_generator:
            core.current_pane.append(window_generator)
        return window_generator(core)
    return wrapper