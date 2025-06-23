from util.file_handler import load_yaml_file
from util.logger import logger
from ui.options import Option , ui_text_panel
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from core.core import Core
def interact(core:"Core",entity: str = ""):
    interactions_dict = load_yaml_file("data/interactions.yaml")
    interaction = interactions_dict[entity]

    if not interaction:
        logger.error(f"interaction for {entity} entity not found in interactions.yaml")

    current_node = "greeting"
    current_interaction = interaction["greeting"]

    if current_interaction:

        core.console.print(ui_text_panel(text=current_interaction["text"]))
        for response in current_interaction["responses"]:
            
            rfunction = response["function"]
            if not rfunction: 
                rfunction = "core.goto_next()"
            
            core.console.print(
            
            Option(text=response["text"], func=lambda f=rfunction:core.execute_yaml_function(f)  )
            )

        

