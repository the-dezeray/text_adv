from typing import TypedDict
class Story(TypedDict):
    id: str
    last_accessed: int
    file_path: str
    current_node: str
