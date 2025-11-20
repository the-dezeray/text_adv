import yaml
import pytest
from pathlib import Path
from core.story import GameEngine


def _load_yaml_file(file_path):
    with open(file_path, "r") as f:
        data = yaml.safe_load(f)
        return data


def _get_next_nodes(story):
    story = _load_yaml_file("data/story.yaml")
    ary = []
    for _chapter in story.items():
        for i in _chapter[1]["choices"]:
            print(i["next_node"])
            ary.append(i["next_node"])
    return ary


def _get_from_all_choices(key: str = ""):
    story = _load_yaml_file("data/story.yaml")
    ary: list[str] = []
    for _chapter in story.items():
        for i in _chapter[1]["choices"]:
            _dict: dict = i
            value = _dict.get(key, None)
            if value:
                ary.append(value)
    return ary


"""@pytest.mark.parametrize("func_call", _get_from_all_choices("function"))
def test_function_execution(func_call):
    try:
        eval(func_call)  # Execute function call
    except Exception as e:
        pytest.fail(f"Function execution failed: {func_call} - Error: {e}")"""


def test_all_next_node_exist():
    story = _load_yaml_file("data/story.yaml")

    nodes = _get_next_nodes(story)
    for node in nodes:
        assert node in story


def test_node_function_():
    story = _load_yaml_file("data/story.yaml")
    nodes = _get_next_nodes(story)
    for node in nodes:
        assert node in story


@pytest.fixture
def story_data():
    return _load_yaml_file("data/story.yaml")


@pytest.fixture
def game_engine():
    return GameEngine()


def test_story_yaml_structure(story_data):
    """Test that the story YAML has the correct structure"""
    assert isinstance(story_data, dict), "Story data should be a dictionary"
    
    for node_id, node_data in story_data.items():
        assert isinstance(node_id, str), f"Node ID {node_id} should be a string"
        assert isinstance(node_data, dict), f"Node data for {node_id} should be a dictionary"
        assert "location" in node_data, f"Node {node_id} missing 'location' field"
        assert "text" in node_data, f"Node {node_id} missing 'text' field"
        assert "choices" in node_data, f"Node {node_id} missing 'choices' field"
        
        choices = node_data["choices"]
        assert isinstance(choices, list), f"Choices for node {node_id} should be a list"
        
        for choice in choices:
            assert isinstance(choice, dict), f"Choice in node {node_id} should be a dictionary"
            assert "text" in choice, f"Choice in node {node_id} missing 'text' field"
            assert "next_node" in choice, f"Choice in node {node_id} missing 'next_node' field"


def test_all_next_nodes_exist(story_data):
    """Test that all next_node references point to existing nodes"""
    nodes = set(story_data.keys())
    next_nodes = set()
    
    for node_data in story_data.values():
        for choice in node_data["choices"]:
            next_nodes.add(choice["next_node"])
    
    # Check that all next_nodes exist in the story
    for next_node in next_nodes:
        assert next_node in nodes, f"Next node {next_node} does not exist in story"


def test_function_execution(game_engine):
    """Test that all function calls in the story are valid"""
    story_data = _load_yaml_file("data/story.yaml")
    
    for node_data in story_data.values():
        for choice in node_data["choices"]:
            if "function" in choice and choice["function"]:
                try:
                    # Create a mock core for testing
                    mock_core = type('MockCore', (), {})()
                    # Execute the function
                    exec(choice["function"], {"core": mock_core})
                except Exception as e:
                    pytest.fail(f"Function execution failed: {choice['function']} - Error: {e}")


def test_node_validation(game_engine):
    """Test that the game engine can validate nodes"""
    story_data = _load_yaml_file("data/story.yaml")
    
    # Test valid node
    valid_node = list(story_data.keys())[0]
    assert game_engine.validate_node(valid_node), f"Valid node {valid_node} failed validation"
    
    # Test invalid node
    invalid_node = "nonexistent_node"
    assert not game_engine.validate_node(invalid_node), f"Invalid node {invalid_node} passed validation"


def test_choice_validation(game_engine):
    """Test that choices are properly validated"""
    story_data = _load_yaml_file("data/story.yaml")
    
    for node_id, node_data in story_data.items():
        for choice in node_data["choices"]:
            assert "text" in choice, f"Choice in node {node_id} missing text"
            assert "next_node" in choice, f"Choice in node {node_id} missing next_node"
            assert choice["next_node"] in story_data, f"Choice in node {node_id} points to invalid next_node"


def test_story_progression(game_engine):
    """Test that story progression works correctly"""
    story_data = _load_yaml_file("data/story.yaml")
    start_node = "1a"  # Assuming this is the start node
    
    # Test initial state
    game_engine.set_current_node(start_node)
    assert game_engine.current_node_id == start_node
    
    # Test progression through a few nodes
    current_node = start_node
    for _ in range(3):  # Test 3 steps of progression
        node_data = story_data[current_node]
        next_node = node_data["choices"][0]["next_node"]  # Take first choice
        game_engine.set_current_node(next_node)
        assert game_engine.current_node_id == next_node
        current_node = next_node


def test_story_loops(game_engine):
    """Test that the story doesn't have any infinite loops"""
    story_data = _load_yaml_file("data/story.yaml")
    visited = set()
    
    def check_for_loops(node_id, path=None):
        if path is None:
            path = []
        
        if node_id in path:
            pytest.fail(f"Loop detected: {' -> '.join(path + [node_id])}")
        
        if node_id in visited:
            return
        
        visited.add(node_id)
        path.append(node_id)
        
        node_data = story_data[node_id]
        for choice in node_data["choices"]:
            next_node = choice["next_node"]
            check_for_loops(next_node, path.copy())
    
    # Start from the first node
    start_node = list(story_data.keys())[0]
    check_for_loops(start_node)
