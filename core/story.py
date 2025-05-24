"""Story management system for the text adventure game."""

from typing import Dict, Any, Optional, List, Union
from util.logger import logger
from util.file_handler import load_yaml_file
from pathlib import Path


class StoryNode:
    """Represents a single node in the game story."""
    def __init__(self, node_id: Union[str, int], data: Dict[str, Any]):
        self.id = str(node_id)  # Convert node_id to string
        self.location = data.get("location")
        self.text = data.get("text", "")
        self.choices = data.get("choices", [])
        
    def get_next_node_id(self, choice_index: int) -> Optional[str]:
        """Get the ID of the next node based on the choice index."""
        if 0 <= choice_index < len(self.choices):
            return str(self.choices[choice_index].get("next_node"))
        return None
        
    def get_function(self, choice_index: int) -> Optional[str]:
        """Get the function string for a particular choice."""
        if 0 <= choice_index < len(self.choices):
            return self.choices[choice_index].get("function")
        return None


class StoryGraph:
    """Manages the entire story structure as a graph of nodes."""
    def __init__(self, story_data: Dict[str, Any]):
        self.nodes: Dict[str, StoryNode] = {}
        
        # Create StoryNode objects for each node in the story data
        for node_id, node_data in story_data.items():
            self.nodes[str(node_id)] = StoryNode(node_id, node_data)
            
    def get_node(self, node_id: Union[str, int]) -> Optional[StoryNode]:
        """Get a node by its ID."""
        return self.nodes.get(str(node_id))
        
    def validate(self) -> List[str]:
        """Validate the story graph, returning a list of errors."""
        errors = []
        
        # Check for broken links (next_node values that don't exist)
        for node_id, node in self.nodes.items():
            for i, choice in enumerate(node.choices):
                next_node_id = str(choice.get("next_node"))
                if next_node_id and next_node_id not in self.nodes:
                    errors.append(f"Node '{node_id}' choice {i+1} points to non-existent node '{next_node_id}'")
        
        # Check for unreachable nodes
        reachable_nodes = set()
        start_node = "0"  # Assuming 0 is always the start
        
        def mark_reachable(node_id: str) -> None:
            if node_id in reachable_nodes or node_id not in self.nodes:
                return
                
            reachable_nodes.add(node_id)
            node = self.nodes[node_id]
            
            for choice in node.choices:
                next_node = str(choice.get("next_node"))
                if next_node:
                    mark_reachable(next_node)
                    
        mark_reachable(start_node)
        
        unreachable = set(self.nodes.keys()) - reachable_nodes
        for node_id in unreachable:
            errors.append(f"Node '{node_id}' is unreachable from the start node")
            
        return errors


class GameEngine:
    """Manages the game's story and state."""
    def __init__(self, story_path: str = "data/gemini_story.yaml"):
        self.story_data = self.load_story(story_path)
        self.story = StoryGraph(self.story_data)
        self.current_node_id = "0"  # Default starting point
        self.temp_story: Optional[StoryGraph] = None
        
    def load_story(self, story_path: str) -> Dict[str, Any]:
        """Load the story from YAML file.
        
        Args:
            story_path: Path to the story YAML file
            
        Returns:
            Dict[str, Any]: The loaded story data
        """
        try:
            path = Path(story_path)
            if not path.exists():
                raise FileNotFoundError(f"Story file not found: {story_path}")
            data = load_yaml_file(str(path))
            logger.info(f"Loaded story data: {data}")
            return data
        except Exception as e:
            logger.error(f"Error loading story: {e}")
            return {}
            
    def validate_story(self) -> bool:
        """Validate the story structure.
        
        Returns:
            bool: True if the story is valid, False otherwise
        """
        errors = self.story.validate()
        if errors:
            for error in errors:
                logger.error(f"[bold red]{error}[/bold red]")
            return False
        return True
        
    def get_current_node(self) -> Optional[StoryNode]:
        """Get the current story node.
        
        Returns:
            Optional[StoryNode]: The current node or None if not found
        """
        story = self.temp_story if self.temp_story is not None else self.story
        return story.get_node(self.current_node_id)
        
    def set_current_node(self, node_id: Union[str, int]) -> None:
        """Set the current story node.
        
        Args:
            node_id: The ID of the node to set as current
        """
        story = self.temp_story if self.temp_story is not None else self.story
        node_id_str = str(node_id)
        if node_id_str not in story.nodes:
            error_msg = f"The node '{node_id_str}' is not defined in the story"
            logger.critical(error_msg)
            raise ValueError(error_msg)
        self.current_node_id = node_id_str
        logger.info(f"Changed to node: {node_id_str}")
        
    def set_temp_story(self, story_data: Dict[str, Any]) -> None:
        """Set a temporary story for the current session.
        
        Args:
            story_data: The story data to use temporarily
        """
        self.temp_story = StoryGraph(story_data)
        self.current_node_id = "0"  # Reset to start of temp story