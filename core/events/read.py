from ui.options import CustomRenderable, Option
from util.logger import logger, event_logger
from rich.panel import Panel
from rich.table import Table
from rich.rule import Rule
from rich.style import Style
from time import sleep

from rich.live import Live
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn
from rich.table import Table
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from core.core import Core
from ui.options import ui_text_panel
texts: dict[str,str] = {
    "ancient_scroll": "You unroll the brittle parchment, the faint scent of dust and something akin to ozone filling your nostrils \n The script, a swirling, alien calligraphy, seems to writhe before your eyes \n As you focus, the words resolve, not into legible text, but into a series of fractured images \n You see… a vast, starless sky, split by a crackling, violet fissure\n You see… a city of obsidian towers, their surfaces reflecting distorted, fleeting faces\n You see… your own hand, aged and withered, clutching a blackened, broken shard\n You see… a pair of luminous, yellow eyes, watching you from the depths of a suffocating darkness\n The images flicker and change, a chaotic slideshow of unsettling visions\n A chill creeps up your spine, and you feel a prickling sensation, as if unseen eyes are now fixed upon you, both within and beyond the scroll's strange depths\n Do you dare to continue deciphering these fractured glimpses, or do you quickly roll the scroll shut, hoping to banish the unsettling visions?",
"well": "You look into the well and see your reflection. You are a young man with a beard and a scar on your face. You are wearing a cloak and a sword. You are standing in a forest. You are looking at the well."
}


@event_logger
def read(core:"Core", text_id: str = "ancient_scroll") -> None:
    string = texts.get(text_id, None)
    if string :
        core.console.clear_display()
        rule_style = Style(color="orange3", bold=True)
        core.console.print(Rule(title="reading the scroll", align="center", style=rule_style))

        core.console.print(
            Panel(
                renderable=string,
                title=text_id,
                title_align="left",
                border_style="dark_orange",
                style=Style(color="light_goldenrod2")
            )
        )

        
        core.console.print( Option(text="Proceed", func=lambda: core.goto_next()))
    elif string == None and core.auto_generate_text:
        node =core.game_engine.get_current_node()
        if node:
            id= node.id
            text = core.ai.generate_note(id)
            if text:
                core.console.print(
                ui_text_panel(text=text)
                    )
                core.console.print( Option(text="Proceed", func=lambda: core.goto_next()))
        else:
            logger.critical("No node found")
            core.console.print( Option(text="Proceed", func=lambda: core.goto_next()))