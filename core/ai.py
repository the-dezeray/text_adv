
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from core.core import Core

class AI:
    def __init__(self, core: "Core"):
        self.core = core
    def generate_note(self, id: str) -> str:
        return "note is not implemented yet"
