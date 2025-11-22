from terma.util.logger import logger
from typing import Any
def execute_string(core, string: str) -> Any:
    """Execute a function defined in YAML.
    
    Args:
        func: The function to execute
        
    Returns:
        Any: The result of the function execution
    """
    logger.info(f"Executing function: {string}")
    local_scope = {"core": core}
    
    try:
        return exec(string, globals(), local_scope)
    except Exception as e:
        logger.error(f"Error executing function {string}: {e}")
        raise