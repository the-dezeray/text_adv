import pytest
from unittest.mock import Mock, patch
from core.core import Core
from core.story import GameEngine
from objects.player import Player
from objects.entities import Entities
from ui.console import Console
from pathlib import Path

@pytest.fixture
def core():
    return Core()

@pytest.fixture
def mock_console():
    return Mock(spec=Console)

def test_core_initialization(core):
    """Test that the core game engine initializes correctly"""
    assert core.running == True
    assert core.in_fight == False
    assert core.in_game == True
    assert core.move_on == True
    assert core._state == "INGAME"
    assert core._command_mode == False
    assert core._disable_command_mode == False
    assert isinstance(core.game_engine, GameEngine)
    assert isinstance(core.player, Player)
    assert core.next_node is None
    assert core.current_entry_text == ""
    assert core.entity is None
    assert core.others == []
    assert core.selected_option == 0
    assert core.s == "options"

def test_chapter_id_property(core):
    """Test chapter_id property getter and setter"""
    # Test setting valid chapter ID
    core.chapter_id = "1"
    assert core.chapter_id == "1"
    
    # Test setting -1
    core.chapter_id = "-1"
    assert core.chapter_id == "-1"
    
    # Test setting invalid chapter ID
    with pytest.raises(Exception):
        core.chapter_id = "invalid"

def test_command_mode_property(core):
    """Test command_mode property getter and setter"""
    # Test enabling command mode
    core.command_mode = True
    assert core._command_mode == True
    core.console.toggle_command_mode.assert_called_once()
    
    # Test disabling command mode
    core.command_mode = False
    assert core._command_mode == False
    
    # Test disabling command mode when _disable_command_mode is True
    core._disable_command_mode = True
    core.command_mode = False
    assert core._command_mode == True  # Should not change

def test_execute_yaml_function(core):
    """Test executing functions from YAML"""
    # Test valid function
    func = "core.player.hp += 10"
    core.execute_yaml_function(func)
    assert core.player.hp == 10
    
    # Test invalid function
    with pytest.raises(Exception):
        core.execute_yaml_function("invalid_function()")

def test_terminate(core):
    """Test game termination"""
    with patch('sys.exit') as mock_exit:
        core.TERMINATE()
        assert core.running == False
        if core.rich_live_instance:
            core.rich_live_instance.stop.assert_called_once()
        if core.input_block:
            core.input_block.stop.assert_called_once()
        mock_exit.assert_called_once_with(0)

def test_continue_game(core):
    """Test continuing the game"""
    # Test starting new game
    core.chapter_id = "-1"
    core.continue_game()
    assert core.chapter_id == "1a"
    
    # Test continuing existing game
    core.chapter_id = "1"
    core.continue_game()
    core.console.print.assert_called()
    core.console.refresh.assert_called_once()

def test_goto_next(core):
    """Test going to next node"""
    # Test with valid next node
    core.next_node = "2"
    core.goto_next()
    assert core.chapter_id == "2"
    
    # Test with no next node
    core.next_node = None
    core.goto_next()
    # Should not change chapter_id

def test_execute_command(core):
    """Test executing game commands"""
    # Test kill command
    with patch.object(core, 'TERMINATE') as mock_terminate:
        core.execute_command("kill")
        mock_terminate.assert_called_once()
    
    # Test unknown command
    core.execute_command("unknown")
    # Should log warning but not raise exception

def test_show_settings(core):
    """Test showing settings menu"""
    core.show_settings()
    assert core._state == "SETTINGS"
    assert core.console.layout == "SETTINGS"
    core.console.refresh.assert_called_once()

def test_show_stats(core):
    """Test showing player stats"""
    core.show_stats()
    assert core._state == "STATS"
    assert core.console.layout == "STATS"
    core.console.refresh.assert_called_once()

def test_fight_sequence(core):
    """Test fight sequence"""
    # Setup
    mock_entity = Mock(spec=Entities)
    mock_entity.hp = 100
    
    # Start fight
    core.fight(mock_entity)
    assert core.in_fight == True
    assert core.entity == mock_entity
    assert core.player.turn == True
    core.console.initialize_fight_mode.assert_called_once()
    
    # Test fight progression
    core.player.turn = False
    core.entity.turn = True
    core.continue_fight()
    assert core.player.turn == True
    assert core.entity.turn == False

def test_inventory_management(core):
    """Test inventory management"""
    # Test adding item
    item = {"name": "sword", "type": "weapon"}
    core.player.add_item(item)
    assert item in core.player.inventory
    
    # Test removing item
    core.player.remove_item(item)
    assert item not in core.player.inventory

def test_save_load_game(core):
    """Test saving and loading game state"""
    # Save game
    core.save_game("test_save")
    assert Path("saves/test_save.json").exists()
    
    # Load game
    core.load_game("test_save")
    assert core.chapter_id == "1"  # Or whatever the saved state was 