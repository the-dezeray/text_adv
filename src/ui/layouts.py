from rich.layout import Layout
from rich.text import Text

def main_layout():
    layout = Layout(name="tm")
    
    layout.split_row(
    Layout(name="other",ratio = 1,visible=True,renderable=Text(" ")),
    Layout(name="main",ratio = 3),
    Layout(name="options", ratio = 1,visible=True,renderable=Text(" ")),
    )
    
    return layout
