Name: explore
Signature: (core=None, area=None, text: str = '')
Docstring: Handles exploration logic for different areas.

========================================

Name: fight
Signature: (core: 'Core', entity: 'entity', repeat: int = 0, reward: Literal['auto', None, 'Item'] = None) -> None
Docstring: Initiates a fight sequence.

Args:
    entity: The entity to fight against.
    core: The core game object containing game state.

========================================

Name: rest
Signature: (core: 'Core', event=None, probability=0)
Docstring: None

========================================

Name: read
Signature: (core: 'Core', text_id: str = 'ancient_scroll') -> None
Docstring: None

========================================

Name: run
Signature: (core: 'Core', fail: Optional[bool] = None, decision: Optional[bool] = None) -> None
Docstring: None

========================================

Name: display_text
Signature: (core: 'Core', text='')
Docstring: None

========================================

Name: sneak
Signature: (core: 'Core' = None, place: str = None) -> None
Docstring: None

========================================

Name: apply_effect
Signature: (core: 'Core', effect=None, duration=None, str=None) -> None
Docstring: None

========================================

Name: remove_effect
Signature: (core: 'Core', effect=None, duration=None, str: str = '') -> None
Docstring: None

========================================

Name: attempt_steal
Signature: (core: 'Core', item='', stealth_check=0, on_success=None, on_fail=None)
Docstring: None

========================================

Name: interact
Signature: (core: 'Core', entity: str = '')
Docstring: None

========================================

Name: investigate
Signature: (core: 'Core', target: str = '') -> None
Docstring: None

========================================

Name: shop
Signature: (core: 'Core', level='normal', items=[], prices=[], text='')
Docstring: None

========================================

Name: skill_check
Signature: (core: 'Core', skill: str = '', limit: int = 0, on_success=None, on_sucess=None, on_fail=None) -> None
Docstring: None

========================================

Name: receive_item
Signature: (core: 'Core', item: str | list[str], text=None | str) -> None
Docstring: None

========================================

Name: attempt_escape
Signature: (core, type: str = '', difficulty=None) -> None
Docstring: None

========================================

Name: modify_player_attribute
Signature: (core: 'Core', property: str, amount: int, text: str) -> None
Docstring: None

========================================

Name: trigger_trap
Signature: (core: 'Core', type: str = 'None', lvl=1, text: str = 'You have been hit by a trap')
Docstring: None

========================================

Name: chance_event
Signature: (core: 'Core', on_success=None, on_fail=None, probability=0)
Docstring: None

========================================

Name: randomly_generate_weapons
Signature: (core: 'Core', count=1, level='low')
Docstring: Generate a list of random weapons based on the specified level.

========================================

Name: randomly_generate_items
Signature: (core: 'Core', count=1, level='low')
Docstring: Generate a list of random items based on the specified level.

========================================

Name: show_items
Signature: (core: 'Core', items=list[tuple] | tuple) -> None
Docstring: None

========================================

