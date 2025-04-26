
def menu_items(core):
    console = core.console
    from art import text2art
    from ui.options import menu__ui,choose_me
    # Define menu options with ASCII text
    menu_items = [
    menu__ui(
        text="Continue",
        func=lambda: console._transtion_layout("INGAME"),
        next_node=None,
        type="menu",
        
    ),
    menu__ui(
        text="New game",
        func=lambda: console._transtion_layout("NEWGAME"),
        next_node=None,
        type="menu"
    ),
    menu__ui(
        text="Settings",
        func=lambda: console._transtion_layout("SETTINGS"),
        next_node=None,
        type="menu"
    ),
    menu__ui(
        text="About us",
        func=lambda:console._transtion_layout("ABOUTUS"),
        next_node=None,
        type="menu"
    ),
    menu__ui(
        text="Leave",
        func=lambda: console.TERMINATE(),
        next_node=None,
        type="menu"
    ),
    ]       
    return menu_items