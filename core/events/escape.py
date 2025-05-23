from ui.options import ui_text_panel,Option
def attempt_escape(core, type:str = None,difficulty =None) -> None:
    core.console.clear_display()
    text = "try to escape"
    core.console.print(
        ui_text_panel(text=text)
    )

             
    core.console.print([Option(text="run for it", func=lambda: core.goto_next(), ),Option(text="run back", func=lambda: core.goto_next(),)])

