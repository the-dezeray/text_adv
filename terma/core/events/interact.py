from terma.util.file_handler import load_yaml_file
from terma.util.paths import world_asset
from terma.util.logger import logger
from terma.ui.options import Option , ui_text_panel
from typing import TYPE_CHECKING
from terma.core.function_runner import execute_string
if TYPE_CHECKING:
    from terma.core.core import Core
def interact(core:"Core",entity: str = ""):
    interactions_dict = load_yaml_file(world_asset("interactions.yaml"))
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
            
            Option(text=response["text"], func=lambda f=rfunction,core=core:execute_string(core, f)  )
            )

        

