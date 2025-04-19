from ui.options import Option, Choices,choose_me


def shop(core, level="normal"):
    core.console.load_shop()
    core.options.append(
        choose_me(text="shop", type="header", func=lambda: None, selectable=False)
    )
    core.options.append(
        choose_me(text="Proceed", func=lambda: core.goto_next(), selectable=False)
        
    )
