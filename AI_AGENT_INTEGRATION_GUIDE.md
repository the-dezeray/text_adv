# AI Agent Integration Guide for Text Adventure Game

This document provides a complete guide for integrating AI agents into the text adventure game system, including rules for story generation and function calling.

## Overview

The AI agent system consists of three main components:

1. **Generation Rules** (`data/ai_generation_rules.txt`) - Comprehensive guidelines for story creation
2. **Helper Functions** (`core/ai_agent_helpers.py`) - Utility classes for function discovery and validation
3. **Example Implementation** (`example_ai_agent_usage.py`) - Demonstration of how to use the system

## Quick Start

### 1. Basic AI Agent Setup

```python
from core.ai_agent_helpers import EventFunctionInspector, AIStoryValidator, AIStoryGenerator

class MyAIAgent:
    def __init__(self, core):
        self.core = core
        self.inspector = EventFunctionInspector()
        self.validator = AIStoryValidator(core)
        self.generator = AIStoryGenerator(core)
```

### 2. Function Discovery

```python
# List all available event functions
functions = inspector.list_all_functions()

# Get categorized functions
categories = inspector.get_functions_by_category()

# Get detailed info about a specific function
info = inspector.get_function_info('fight')
print(f"Signature: {info['signature']}")
print(f"Docstring: {info['docstring']}")
```

### 3. Story Generation

```python
# Generate a story event sequence
sequence = [
    {
        'function': 'display_text',
        'parameters': {'text': 'You enter a dark cave...'},
        'description': 'Opening scene'
    },
    {
        'function': 'explore',
        'parameters': {},
        'description': 'Cave exploration'
    },
    {
        'function': 'fight',
        'parameters': {'entity': 'snake', 'reward': 'auto'},
        'description': 'Combat encounter'
    }
]
```

### 4. Validation and Execution

```python
# Validate the sequence
validation = validator.validate_event_sequence(sequence)

if validation['valid']:
    # Execute events
    for event in sequence:
        func = getattr(events, event['function'])
        func(core, **event['parameters'])
else:
    print("Validation errors:", validation['errors'])
```

## Available Event Functions

### Combat Functions
- `fight(entity, reward=None)` - Initiate combat with an entity
- `attempt_escape()` - Try to flee from danger
- `deal_damage(weapon)` - Deal damage with a weapon

### Exploration Functions
- `explore()` - General area exploration
- `investigate()` - Detailed examination
- `sneak()` - Stealth-based movement

### Narrative Functions
- `display_text(text)` - Show story text to player
- `read()` - Read books, scrolls, signs

### Player Interaction Functions
- `skill_check(skill, limit, on_success, on_fail)` - Ability tests
- `receive_item(item)` - Give items to player
- `modify_player_attribute(attribute, value)` - Change player stats
- `apply_effect(effect)` - Apply status effects
- `remove_effect(effect)` - Remove status effects

### Environmental Functions
- `rest()` - Recovery and healing
- `shop()` - Trading interface
- `interact()` - NPC/object interactions
- `trigger_trap()` - Activate hazards
- `chance_event()` - Random occurrences

## Story Generation Guidelines

### Core Principles
1. **Narrative Flow** - Create engaging, logical progressions
2. **Player Agency** - Provide meaningful choices
3. **Balanced Difficulty** - Scale appropriately to player level
4. **Immersive Description** - Use vivid, descriptive language
5. **Consequence System** - Actions have clear outcomes

### Event Sequencing Rules
- Start with scene-setting (`display_text`)
- Provide exploration opportunities (`explore`, `investigate`)
- Include challenges (`skill_check`, `fight`)
- Offer recovery periods (`rest`)
- Reward progression (`receive_item`)

### Difficulty Scaling
```python
# Easy encounter
easy_fight = generator.generate_balanced_encounter("easy")

# Skill check based on player stats
skill_challenge = generator.create_skill_challenge("strength", "normal")
```

## Advanced Features

### Dynamic Content Generation
The system can suggest appropriate events based on current game state:

```python
# Get context-aware suggestions
suggestions = generator.suggest_next_events({
    'player_hp': core.player.hp,
    'in_combat': core.in_fight,
    'player_level': core.player.level
})
```

### Validation System
Comprehensive validation ensures story sequences are feasible:

- Parameter validation (required vs optional)
- Entity/item existence checks
- Context appropriateness
- Logical flow analysis

### Error Handling
The system provides detailed feedback for debugging:

```python
validation_result = {
    'valid': False,
    'errors': ['Missing required parameter: entity'],
    'warnings': ['Entity "dragon" may not exist'],
    'suggestions': ['Consider using "snake" or "starlight_guardian"']
}
```

## Integration Examples

### Simple Story Generator
```python
def generate_simple_story(theme="adventure"):
    if theme == "exploration":
        return [
            {'function': 'display_text', 'parameters': {'text': 'You discover a hidden path...'}},
            {'function': 'explore', 'parameters': {}},
            {'function': 'investigate', 'parameters': {}},
            {'function': 'receive_item', 'parameters': {'item': 'gold'}}
        ]
```

### Adaptive Difficulty System
```python
def generate_adaptive_encounter(player_hp, player_level):
    if player_hp < 30:
        return {'function': 'rest', 'parameters': {}}
    elif player_level < 5:
        return generator.generate_balanced_encounter("easy")
    else:
        return generator.generate_balanced_encounter("normal")
```

### Context-Aware Storytelling
```python
def continue_story(current_location, player_state):
    suggestions = generator.suggest_next_events({
        'location': current_location,
        'hp': player_state.hp,
        'inventory': player_state.inventory
    })
    
    # Build sequence based on suggestions
    return build_sequence_from_suggestions(suggestions)
```

## Available Game Data

### Entities
- `snake` - Level 1 basic enemy
- `starlight_guardian` - Level 1 guardian

### Items
- `gold` - Currency
- `juice` - Restores 5 HP
- `water` - Restores 3 HP
- `heal_potion` - Restores 10 HP

### Player Attributes
- `hp` - Health points
- `strength` - Physical power
- `dexterity` - Agility
- `intelligence` - Mental acuity
- `charisma` - Social influence

## Best Practices

1. **Always validate** story sequences before execution
2. **Use function inspection** to understand available parameters
3. **Handle errors gracefully** with fallback options
4. **Maintain narrative consistency** across sequences
5. **Balance action and description** for engagement
6. **Test with different game states** to ensure robustness

## Troubleshooting

### Common Issues
- **Function not found**: Check `inspector.list_all_functions()`
- **Parameter errors**: Use `inspector.get_function_info(function_name)`
- **Validation failures**: Review error messages and fix parameters
- **Entity/item not found**: Check data files in `data/` directory

### Debug Tools
- `print_all_event_functions()` - Show all available functions
- `validator.validate_single_event()` - Test individual events
- `inspector.get_function_info()` - Get detailed function information

This system provides a robust foundation for AI-driven story generation while maintaining game balance and narrative quality.
