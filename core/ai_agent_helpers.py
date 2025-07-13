"""
AI Agent Helper Functions for Text Adventure Game
Provides utility functions for AI agents to dynamically discover and call game events.
"""

import inspect
from typing import Dict, List, Callable, Any, Optional, Union
from core import events
from util.logger import logger


class EventFunctionInspector:
    """Utility class to help AI agents discover and call event functions."""
    
    def __init__(self):
        self.event_functions = self._discover_event_functions()
    
    def _discover_event_functions(self) -> Dict[str, Callable]:
        """Discover all available event functions from the events module."""
        functions = {}
        
        # Get all functions from the events module
        for name in dir(events):
            if not name.startswith('_'):  # Skip private functions
                attr = getattr(events, name)
                if callable(attr) and hasattr(attr, '__module__'):
                    functions[name] = attr
        
        return functions
    
    def get_function_signature(self, function_name: str) -> Optional[str]:
        """Get the signature of a specific event function."""
        if function_name not in self.event_functions:
            return None
        
        func = self.event_functions[function_name]
        return str(inspect.signature(func))
    
    def get_function_docstring(self, function_name: str) -> Optional[str]:
        """Get the docstring of a specific event function."""
        if function_name not in self.event_functions:
            return None
        
        func = self.event_functions[function_name]
        return inspect.getdoc(func)
    
    def get_function_info(self, function_name: str) -> Optional[Dict[str, Any]]:
        """Get comprehensive information about a function."""
        if function_name not in self.event_functions:
            return None
        
        func = self.event_functions[function_name]
        
        try:
            source_file = inspect.getfile(func)
        except (TypeError, OSError):
            source_file = None
            
        return {
            'name': function_name,
            'signature': str(inspect.signature(func)),
            'docstring': inspect.getdoc(func),
            'parameters': self._get_parameter_info(func),
            'source_file': source_file
        }
    
    def _get_parameter_info(self, func: Callable) -> List[Dict[str, Any]]:
        """Extract detailed parameter information from a function."""
        sig = inspect.signature(func)
        params = []
        
        for param_name, param in sig.parameters.items():
            param_info = {
                'name': param_name,
                'kind': param.kind.name,
                'has_default': param.default != inspect.Parameter.empty,
                'default': param.default if param.default != inspect.Parameter.empty else None,
                'annotation': param.annotation if param.annotation != inspect.Parameter.empty else None
            }
            params.append(param_info)
        
        return params
    
    def list_all_functions(self) -> List[str]:
        """Get a list of all available event function names."""
        return list(self.event_functions.keys())
    
    def get_functions_by_category(self) -> Dict[str, List[str]]:
        """Categorize functions based on their names and docstrings."""
        categories = {
            'combat': [],
            'exploration': [],
            'interaction': [],
            'narrative': [],
            'player_modification': [],
            'utility': []
        }
        
        for name, func in self.event_functions.items():
            docstring = inspect.getdoc(func) or ""
            name_lower = name.lower()
            
            # Categorize based on function name and docstring content
            if any(keyword in name_lower for keyword in ['fight', 'combat', 'damage', 'escape']):
                categories['combat'].append(name)
            elif any(keyword in name_lower for keyword in ['explore', 'investigate', 'search']):
                categories['exploration'].append(name)
            elif any(keyword in name_lower for keyword in ['interact', 'shop', 'steal', 'sneak']):
                categories['interaction'].append(name)
            elif any(keyword in name_lower for keyword in ['display', 'text', 'read']):
                categories['narrative'].append(name)
            elif any(keyword in name_lower for keyword in ['modify', 'effect', 'attribute', 'receive']):
                categories['player_modification'].append(name)
            else:
                categories['utility'].append(name)
        
        return categories


class ValidationResult:
    """Represents the result of event validation."""
    
    def __init__(self):
        self.valid: bool = True
        self.errors: List[str] = []
        self.warnings: List[str] = []
        self.suggestions: List[str] = []


class AIStoryValidator:
    """Validates AI-generated story sequences for consistency and feasibility."""
    
    def __init__(self, core):
        self.core = core
        self.inspector = EventFunctionInspector()
    
    def validate_event_sequence(self, events: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Validate a sequence of events for feasibility."""
        validation_result = ValidationResult()
        
        for i, event in enumerate(events):
            event_validation = self.validate_single_event(event, i)
            
            if not event_validation.valid:
                validation_result.valid = False
            
            validation_result.errors.extend(event_validation.errors)
            validation_result.warnings.extend(event_validation.warnings)
            validation_result.suggestions.extend(event_validation.suggestions)
        
        return {
            'valid': validation_result.valid,
            'errors': validation_result.errors,
            'warnings': validation_result.warnings,
            'suggestions': validation_result.suggestions
        }
    
    def validate_single_event(self, event: Dict[str, Any], position: int) -> ValidationResult:
        """Validate a single event for correctness."""
        result = ValidationResult()
        
        function_name = event.get('function')
        if not function_name:
            result.valid = False
            result.errors.append(f"Event {position}: Missing function name")
            return result
        
        if function_name not in self.inspector.event_functions:
            result.valid = False
            result.errors.append(f"Event {position}: Unknown function '{function_name}'")
            return result
        
        # Validate parameters
        func_info = self.inspector.get_function_info(function_name)
        if func_info:
            required_params = [p for p in func_info['parameters'] 
                             if p['name'] != 'core' and not p['has_default']]
            provided_params = event.get('parameters', {})
            
            for param in required_params:
                if param['name'] not in provided_params:
                    result.valid = False
                    result.errors.append(
                        f"Event {position}: Missing required parameter '{param['name']}' for {function_name}"
                    )
        
        # Context-specific validations
        if function_name == 'fight':
            entity = event.get('parameters', {}).get('entity')
            if entity and not self._entity_exists(entity):
                result.warnings.append(
                    f"Event {position}: Entity '{entity}' may not exist"
                )
        
        if function_name == 'receive_item':
            item = event.get('parameters', {}).get('item')
            if item and not self._item_exists(item):
                result.warnings.append(
                    f"Event {position}: Item '{item}' may not exist"
                )
        
        return result
    
    def _entity_exists(self, entity_name: str) -> bool:
        """Check if an entity exists in the game data."""
        try:
            from util.file_handler import load_yaml_file
            entities = load_yaml_file("data/entities.yaml")
            return entity_name in entities
        except:
            return False
    
    def _item_exists(self, item_name: str) -> bool:
        """Check if an item exists in the game data."""
        try:
            from util.file_handler import load_yaml_file
            items = load_yaml_file("data/items.yaml")
            return item_name in items
        except:
            return False


class AIStoryGenerator:
    """Helper class for AI agents to generate story content."""
    
    def __init__(self, core):
        self.core = core
        self.inspector = EventFunctionInspector()
        self.validator = AIStoryValidator(core)
    
    def suggest_next_events(self, current_context: Dict[str, Any]) -> List[str]:
        """Suggest appropriate next events based on current game context."""
        suggestions = []
        
        player_hp = getattr(self.core.player, 'hp', 100)
        player_level = getattr(self.core.player, 'level', 1)
        in_combat = getattr(self.core, 'in_fight', False)
        
        if in_combat:
            suggestions.extend(['fight', 'attempt_escape', 'skill_check'])
        elif player_hp < 30:
            suggestions.extend(['rest', 'receive_item', 'shop'])
        else:
            suggestions.extend(['explore', 'investigate', 'interact', 'display_text'])
        
        return suggestions
    
    def generate_balanced_encounter(self, difficulty: str = "normal") -> Dict[str, Any]:
        """Generate a balanced encounter based on difficulty level."""
        difficulty_mapping = {
            "easy": {"entity": "snake", "reward": "auto"},
            "normal": {"entity": "starlight_guardian", "reward": "auto"},
            "hard": {"entity": "starlight_guardian", "reward": None}
        }
        
        encounter = difficulty_mapping.get(difficulty, difficulty_mapping["normal"])
        
        return {
            'function': 'fight',
            'parameters': encounter,
            'description': f"A {difficulty} combat encounter"
        }
    
    def create_skill_challenge(self, skill: str, difficulty: str = "normal") -> Dict[str, Any]:
        """Create a skill-based challenge."""
        difficulty_limits = {
            "easy": 5,
            "normal": 10,
            "hard": 15
        }
        
        limit = difficulty_limits.get(difficulty, 10)
        
        return {
            'function': 'skill_check',
            'parameters': {
                'skill': skill,
                'limit': limit,
                'on_success': lambda: logger.info(f"Player succeeded {skill} check"),
                'on_fail': lambda: logger.info(f"Player failed {skill} check")
            },
            'description': f"A {difficulty} {skill} challenge"
        }


def print_all_event_functions():
    """Utility function to print all available event functions and their signatures."""
    inspector = EventFunctionInspector()
    
    print("=== AVAILABLE EVENT FUNCTIONS ===\n")
    
    categories = inspector.get_functions_by_category()
    
    for category, functions in categories.items():
        if functions:
            print(f"## {category.upper()} FUNCTIONS:")
            for func_name in functions:
                info = inspector.get_function_info(func_name)
                if info:
                    print(f"  {func_name}{info['signature']}")
                    if info['docstring']:
                        print(f"    {info['docstring']}")
                    print()
            print()


if __name__ == "__main__":
    # Print all available functions when run directly
    print_all_event_functions()
