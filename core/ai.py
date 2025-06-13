from ui.options import ui_text_panel
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from core.core import Core

class AI:
    def __init__(self, core: "Core"):
        self.core = core
    def generate_note(self, id: str) -> str:
        return "note is not implemented yet"
    def prompt(self, message: str) -> None:
        responce = self._prompt_model(message)
        self.core.console.clear_display()
        self.core.console.print(ui_text_panel(text=responce))
    def _prompt_model(self, message: str) ->str:
        return "This is a test responce"