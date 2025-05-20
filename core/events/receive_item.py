from ui.options import ui_text_panel,Option
def receive_item(core, item:str) -> None:
    core.console.clear_display()
    text = "you have obtained"
    core.console.print(
        ui_text_panel(text=text)
    )

             
    core.console.print([Option(text="pick up", func=lambda: core.goto_next(), ),Option(text="leave", func=lambda: core.goto_next(),)])

