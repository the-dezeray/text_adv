from ui.options import CustomRenderable,Option


def shop(core, level="normal"):
    core.console.load_shop()
    core.console.print(
        Option(text="shop", func=lambda: None, selectable=False)
    )
    core.console.print(
        Option(text="Proceed", func=lambda: core.goto_next(), selectable=False)
        
    )
