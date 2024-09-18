from rich.layout import Layout
def make_layout() -> Layout:
    """return a structured Layout object

    Returns:
        Layout: Layout object
    """
    layout = Layout(name="root") 
    layout.split(
    
        Layout(name="options", ratio = 3),
        

    )
    return layout

def character_selection_layout()->Layout:
    layout = Layout("root")
    layout.split_row(
        Layout(name ="options",ratio = 1),
        Layout(name ="preview",ratio = 2) 
    )

    return layout
 
def preview_layout():
    layout = Layout("char_preview")

def character_preview_layout():
    layout = Layout(name="char_preview")
    from rich.table import Table
    from rich.panel import Panel
    table = Table(expand= True,show_header=False,)
    table.add_column()
    table.add_row(Panel("",height=15,width=30,border_style= "bold red"),"Name:  Desire the great \n Class : SSdsafdsfdfs \n Health : [green]##########[/green]")
    layout["char_preview"].update(table)
    return layout

def gameplay_layout():
    layout = Layout(name="repo")
    layout.split(Layout(name = "preview"))

    return layout
from rich.padding import Padding
from rich.panel import Panel
def  option_template(text :str = None)->Padding:
    return Padding(Panel("de"))

