"""
Example AI Agent Usage for Text Adventure Game
Demonstrates how an AI agent can use the generation rules and helper functions.
"""

from core.ai_agent_helpers import EventFunctionInspector, AIStoryValidator, AIStoryGenerator
from util.logger import logger
from typing import List, Dict, Any


class ExampleAIAgent:
    """Example AI agent that generates story content using the helper functions."""
    
    def __init__(self, core):
        self.core = core
        self.inspector = EventFunctionInspector()
        self.validator = AIStoryValidator(core)
        self.generator = AIStoryGenerator(core)
    
    def generate_story_sequence(self, theme: str = "exploration") -> List[Dict[str, Any]]:
        """Generate a sequence of story events based on a theme."""
        
        if theme == "exploration":
            return self._generate_exploration_sequence()
        elif theme == "combat":
            return self._generate_combat_sequence()
        elif theme == "mystery":
            return self._generate_mystery_sequence()
        else:
            return self._generate_general_sequence()
    
    def _generate_exploration_sequence(self) -> List[Dict[str, Any]]:
        """Generate an exploration-focused story sequence."""
        sequence = [
            {
                'function': 'display_text',
                'parameters': {
                    'text': 'You find yourself at the edge of an ancient forest. The trees whisper secrets in a language forgotten by time.'
                },
                'description': 'Opening scene description'
            },
            {
                'function': 'explore',
                'parameters': {},
                'description': 'Player explores the forest'
            },
            {
                'function': 'investigate',
                'parameters': {},
                'description': 'Player investigates something interesting'
            },
            {
                'function': 'skill_check',
                'parameters': {
                    'skill': 'intelligence',
                    'limit': 8,
                    'on_success': lambda: logger.info("Successfully deciphered ancient markings"),
                    'on_fail': lambda: logger.info("The markings remain mysterious")
                },
                'description': 'Intelligence check to understand ancient markings'
            },
            {
                'function': 'receive_item',
                'parameters': {
                    'item': 'gold'
                },
                'description': 'Reward for successful exploration'
            }
        ]
        
        return sequence
    
    def _generate_combat_sequence(self) -> List[Dict[str, Any]]:
        """Generate a combat-focused story sequence."""
        sequence = [
            {
                'function': 'display_text',
                'parameters': {
                    'text': 'A menacing creature emerges from the shadows, blocking your path forward.'
                },
                'description': 'Combat introduction'
            },
            {
                'function': 'fight',
                'parameters': {
                    'entity': 'snake',
                    'reward': 'auto'
                },
                'description': 'Combat encounter with snake'
            },
            {
                'function': 'rest',
                'parameters': {},
                'description': 'Rest and recovery after combat'
            },
            {
                'function': 'receive_item',
                'parameters': {
                    'item': 'heal_potion'
                },
                'description': 'Healing reward for victory'
            }
        ]
        
        return sequence
    
    def _generate_mystery_sequence(self) -> List[Dict[str, Any]]:
        """Generate a mystery-focused story sequence."""
        sequence = [
            {
                'function': 'display_text',
                'parameters': {
                    'text': 'You discover a dusty tome lying open on an ancient pedestal. Its pages seem to glow with an inner light.'
                },
                'description': 'Mystery setup'
            },
            {
                'function': 'read',
                'parameters': {},
                'description': 'Player reads the mysterious book'
            },
            {
                'function': 'skill_check',
                'parameters': {
                    'skill': 'intelligence',
                    'limit': 12,
                    'on_success': lambda: logger.info("Unlocked ancient knowledge"),
                    'on_fail': lambda: logger.info("The knowledge remains hidden")
                },
                'description': 'High-difficulty intelligence check'
            },
            {
                'function': 'investigate',
                'parameters': {},
                'description': 'Further investigation of the area'
            }
        ]
        
        return sequence
    
    def _generate_general_sequence(self) -> List[Dict[str, Any]]:
        """Generate a general story sequence."""
        # Use the generator to suggest appropriate events
        suggested_events = self.generator.suggest_next_events({})
        
        sequence = []
        for event_name in suggested_events[:3]:  # Take first 3 suggestions
            if event_name == 'display_text':
                sequence.append({
                    'function': 'display_text',
                    'parameters': {
                        'text': 'You continue your journey through this mysterious land.'
                    },
                    'description': 'General narrative text'
                })
            elif event_name == 'explore':
                sequence.append({
                    'function': 'explore',
                    'parameters': {},
                    'description': 'General exploration'
                })
            elif event_name == 'investigate':
                sequence.append({
                    'function': 'investigate',
                    'parameters': {},
                    'description': 'General investigation'
                })
        
        return sequence
    
    def validate_and_execute_sequence(self, sequence: List[Dict[str, Any]]) -> bool:
        """Validate a story sequence and execute it if valid."""
        
        # Validate the sequence
        validation_result = self.validator.validate_event_sequence(sequence)
        
        if not validation_result['valid']:
            logger.error("Story sequence validation failed:")
            for error in validation_result['errors']:
                logger.error(f"  - {error}")
            return False
        
        # Log any warnings
        for warning in validation_result['warnings']:
            logger.warning(warning)
        
        # Execute the sequence (in a real implementation)
        logger.info("Executing validated story sequence...")
        for i, event in enumerate(sequence):
            logger.info(f"Step {i+1}: {event['description']}")
            # Here you would actually call the event function
            # e.g., getattr(events, event['function'])(self.core, **event['parameters'])
        
        return True
    
    def demonstrate_function_inspection(self):
        """Demonstrate how to inspect available functions."""
        
        print("=== FUNCTION INSPECTION DEMO ===\n")
        
        # List all available functions
        all_functions = self.inspector.list_all_functions()
        print(f"Available functions: {', '.join(all_functions)}\n")
        
        # Get categorized functions
        categories = self.inspector.get_functions_by_category()
        for category, functions in categories.items():
            if functions:
                print(f"{category.upper()}: {', '.join(functions)}")
        print()
        
        # Inspect specific functions
        for func_name in ['fight', 'skill_check', 'display_text']:
            info = self.inspector.get_function_info(func_name)
            if info:
                print(f"Function: {func_name}")
                print(f"  Signature: {info['signature']}")
                print(f"  Docstring: {info['docstring']}")
                print(f"  Parameters:")
                for param in info['parameters']:
                    default_info = f" (default: {param['default']})" if param['has_default'] else ""
                    print(f"    - {param['name']}: {param['annotation']}{default_info}")
                print()


def demo_ai_agent_usage():
    """Demonstrate how an AI agent would use the system."""
    
    # This would normally be passed from the game core
    class MockCore:
        def __init__(self):
            self.player = MockPlayer()
            self.in_fight = False
    
    class MockPlayer:
        def __init__(self):
            self.hp = 75
            self.level = 1
            self.strength = 10
    
    # Create mock core and AI agent
    core = MockCore()
    ai_agent = ExampleAIAgent(core)
    
    print("=== AI AGENT DEMO ===\n")
    
    # Demonstrate function inspection
    ai_agent.demonstrate_function_inspection()
    
    # Generate different types of story sequences
    themes = ['exploration', 'combat', 'mystery']
    
    for theme in themes:
        print(f"=== {theme.upper()} SEQUENCE ===")
        sequence = ai_agent.generate_story_sequence(theme)
        
        # Print the sequence
        for i, event in enumerate(sequence):
            print(f"Step {i+1}: {event['function']}() - {event['description']}")
        
        # Validate and "execute" the sequence
        success = ai_agent.validate_and_execute_sequence(sequence)
        print(f"Execution {'successful' if success else 'failed'}\n")


if __name__ == "__main__":
    demo_ai_agent_usage()
