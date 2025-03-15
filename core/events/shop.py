from ui.options import Option, Choices


def shop(core, level="normal"):
    core.console.load_shop()
    core.options.append(
        Option(text=string, type="header", func=lambda: None, selectable=False)
    )
    core.options.append(
        Choices(
            renderable=Option(
                text="Proceed", func=lambda: core.goto_next(), selectable=False
            )
        )
    )
