
import inspect

from .explore import explore
from .fight import fight
from .rest import rest
from .read import read
from .run import run
from .display_text import display_text
from .sneak import sneak
from .apply_effect import apply_effect, remove_effect
from .attempt_steal import attempt_steal
from .interact import interact
from .investigate import investigate
from .shop import shop
from .skill_check import skill_check
from .receive_item import receive_item
from .escape import attempt_escape
from .modify_player_attribute import modify_player_attribute
from .trigger_trap import trigger_trap
from .chance_event import chance_event
from .generators import (randomly_generate_weapons, randomly_generate_items,show_items)

with open("data/events_description.tx.t","a")as file:
    for     event in (explore, fight, rest, read, run, display_text, sneak, apply_effect, remove_effect,
                    attempt_steal, interact, investigate, shop, skill_check, receive_item,
                    attempt_escape, modify_player_attribute, trigger_trap, chance_event,
                    randomly_generate_weapons, randomly_generate_items, show_items):
                    # Get function name
                    name = event.__name__

                    # Get docstring
                    docstring = inspect.getdoc(event)

                    # Get signature (arguments and defaults)
                    signature = str(inspect.signature(event))

                    # Write to file
                    file.write(f"Name: {name}\n")
                    file.write(f"Signature: {signature}\n")
                    file.write(f"Docstring: {docstring}\n")
                    file.write("\n" + "="*40 + "\n\n")
                    
