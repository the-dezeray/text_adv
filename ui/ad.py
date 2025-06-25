from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ui.console import Console

def new_game_menu_items(core):
    console:"Console" = core.console
    from art import text2art
    from ui.options import MenuOption,Option,MinimalMenuOption,MinimalTextOption
    # Define menu options with ASCII text
    def transition_to_story_select(console:"Console"):
        console._transtion_layout("SELECTSTORY")
        stories = ["story 1","story 2","story 3","story 132","story 232","story 323"]
        items = []
        for story in stories:
            items.append(MinimalTextOption(
                text=story,
                func=lambda: console._transtion_layout("INGAME"),
                next_node=None,
                type="menu"
            ))
        console.clear_display()
        core.console.print(items)
    def ds():   
        console._transtion_layout("AI_STUDIO")
    
        console.refresh()
        core.ai.fake_prompt('d')
    items = [

    MinimalMenuOption(
        text="enter the library of stories",
        func=lambda: transition_to_story_select(console),
        next_node=None,
        type="menu"
    ),
    MinimalMenuOption(
        text="generate your own story with with ai",
        func=lambda: ds(),
        next_node=None,
        type="menu"
    ),
        MinimalMenuOption(
        text="load a personal story ",
        func=lambda: console.TERMINATE(),
        next_node=None,
        type="menu"
    ),
    ]
    console.clear_display()
    core.console.print(items)

def menu_items(core):
    console = core.console
    from art import text2art
    from ui.options import MenuOption,Option,MinimalMenuOption
    # Define menu options with ASCII text
    menu_items = [
    MinimalMenuOption(
        text="Continue",
        func=lambda: console._transtion_layout("INGAME"),
        next_node=None,
        type="menu",
        
    ),
    MinimalMenuOption(
        text="New game",
        func=lambda: new_game_menu_items(core),
        next_node=None,
        type="menu"
    ),
    MinimalMenuOption(
        text="Settings",
        func=lambda: console._transtion_layout("SETTINGS"),
        next_node=None,
        type="menu"
    ),
    MinimalMenuOption(
        text="About us",
        func=lambda:console._transtion_layout("ABOUTUS"),
        next_node=None,
        type="menu"
    ),
    MinimalMenuOption(
        text="Leave",
        func=lambda: console.TERMINATE(),
        next_node=None,
        type="menu"
    ),
    ]       
    return menu_items