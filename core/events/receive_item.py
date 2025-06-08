from ui.options import ui_text_panel, Option
import random

def receive_item( core ,item: str | list[str],text = None | str) -> None:

    one_item_texts = [
        "you have obtained",
        "you have found",
        "you have received",
        "an item has been added to your inventory",
        "you stumbled upon",
        "you picked up",
        "you acquired",
        "it's yours now",
        "you now possess",
    ]
    multiple_items_texts = [
        "you discover items in your hands",
        "you collected several items",
        "a group of items lies before you",
        "you've acquired a handful of things",
        "you gathered the following",
        "these items now belong to you",
        "you scoop up a few things",
        "your hands are full with",
    ]

    if isinstance(item, list):
        text = random.choice(multiple_items_texts) + " : " + ", ".join(item)
    else:
        text = random.choice(one_item_texts) + " : " + item
    core.console.print(ui_text_panel(text=text))
    core.console.print(
    #  Option( text="Proceed", func=lambda: core.goto_next() )
    core.goto_next()
    )

