
def menu_items(core):
    console = core.console
    from art import text2art
    from ui.options import MenuOption,Option
    # Define menu options with ASCII text
    menu_items = [
    MenuOption(
        text="Continue",
        func=lambda: console._transtion_layout("INGAME"),
        next_node=None,
        type="menu",
        
    ),
    MenuOption(
        text="New game",
        func=lambda: console._transtion_layout("NEWGAME"),
        next_node=None,
        type="menu"
    ),
    MenuOption(
        text="Settings",
        func=lambda: console._transtion_layout("SETTINGS"),
        next_node=None,
        type="menu"
    ),
    MenuOption(
        text="About us",
        func=lambda:console._transtion_layout("ABOUTUS"),
        next_node=None,
        type="menu"
    ),
    MenuOption(
        text="Leave",
        func=lambda: console.TERMINATE(),
        next_node=None,
        type="menu"
    ),
    ]       
    return menu_items