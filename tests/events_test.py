# test if all are decorated

import pytest
from unittest.mock import Mock, patch
from core.core import Core
from core.events import (
    navigate, explore, fight, rest, read, meditate, run, search,
    trap, sneak, encounter, goto, harvest, interact, investigate,
    place, shop, search_in, skill_check, receive_item, escape
)

@pytest.fixture
def mock_core():
    core = Mock(spec=Core)
    core.console = Mock()
    core.player = Mock()
    core.entity = Mock()
    core.goto_next = Mock()
    return core

def test_navigate(mock_core):
    navigate(mock_core, location="treasure")
    mock_core.console.clear_display.assert_called_once()
    mock_core.console.print.assert_called()

def test_fight(mock_core):
    mock_entity = Mock()
    fight(mock_core, entity=mock_entity)
    assert mock_core.in_fight == True
    assert mock_core.entity == mock_entity
    mock_core.console.initialize_fight_mode.assert_called_once()

def test_rest(mock_core):
    rest(mock_core)
    mock_core.console.clear_display.assert_called_once()
    mock_core.console.print.assert_called()

def test_search(mock_core):
    search(mock_core)
    mock_core.goto_next.assert_called_once()

def test_trap(mock_core):
    trap(mock_core, type="fire")
    mock_core.console.print.assert_called()
    mock_core.player.contact_with_trap.assert_called_once()

def test_shop(mock_core):
    shop(mock_core, level="normal")
    mock_core.console.load_shop.assert_called_once()
    mock_core.console.print.assert_called()

def test_skill_check(mock_core):
    skill_check(mock_core, skill="hp", limit=10)
    mock_core.goto_next.assert_called_once()

def test_receive_item(mock_core):
    receive_item(mock_core, item="sword")
    mock_core.console.clear_display.assert_called_once()
    mock_core.console.print.assert_called()

def test_escape(mock_core):
    escape(mock_core, type="persuade", difficulty=10)
    mock_core.console.clear_display.assert_called_once()
    mock_core.console.print.assert_called()

def test_investigate(mock_core):
    investigate(mock_core, target="murals")
    mock_core.goto_next.assert_called_once()

def test_search_in(mock_core):
    search_in(mock_core, place="chest")
    mock_core.goto_next.assert_called_once()

def test_sneak(mock_core):
    sneak(mock_core, place="room")
    mock_core.goto_next.assert_called_once()

def test_meditate(mock_core):
    meditate(mock_core, value="focus")
    mock_core.goto_next.assert_called_once()

def test_run(mock_core):
    run(mock_core, fail=False, decision=True)
    mock_core.goto_next.assert_called_once()

def test_place(mock_core):
    place(mock_core)
    # Add assertions based on implementation

def test_goto(mock_core):
    goto(mock_core)
    # Add assertions based on implementation

def test_harvest(mock_core):
    harvest(mock_core)
    # Add assertions based on implementation

def test_interact(mock_core):
    interact(mock_core)
    # Add assertions based on implementation

def test_encounter(mock_core):
    encounter(mock_core)
    # Add assertions based on implementation

# Test error cases
def test_fight_no_entity(mock_core):
    fight(mock_core, entity=None)
    assert mock_core.in_fight == False

def test_search_in_no_place(mock_core):
    with pytest.raises(ValueError):
        search_in(mock_core, place=None)

def test_sneak_no_place(mock_core):
    with pytest.raises(ValueError):
        sneak(mock_core, place=None)

def test_investigate_no_target(mock_core):
    with pytest.raises(ValueError):
        investigate(mock_core, target=None)
