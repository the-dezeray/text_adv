from ui.options import ui_text_panel

def apply_effect( effect=None, duration=None, core=None, str=None) -> None:
    core.console.print(ui_text_panel(text=str))
    core.goto_next()

def remove_effect( effect=None, duration=None, core=None, str=None) -> None:
    core.console.print(ui_text_panel(text=str))
    core.goto_next()