from rich.table import Table
from rich.padding import Padding
from rich.panel import Panel
class Console():

    def __init__(self,core):
        self.core = core
        self.layout = None
        self.table = None
    def refresh(self):
        table = self.build_table()
        self.core.interface[self.core.s].update(table)
        pass
    def build_table(self):
        core = self.core
        self.table = Table(expand=True,show_edge=False,show_header=False)
        self.table.add_column()
        options : list = core.options
        if len(options) > 9 :
            options = options[9:]
        for index ,option in enumerate(options):    
            style = "none"
            x = 5
            if option.selected:
                if options[index].preview:
                    options[index].preview()
                style = "bold green"
                x += 5
            #self.table.add_row(Padding(Panel(option.text,border_style=style),pad =(0,0,0,x)))
            if option.type == 'header' :
                renderable  = _dialogue_text(text = option.text,style = style)
            else: 
                renderable = _option_button(text = option.text,style = style,x=x)
            self.table.add_row(renderable)
        return self.table 
def _dialogue_text(text,style):
    instance : Padding = Padding (
            
                text,
            pad = (0,0,0,0)
    )
    return instance

def _option_button(text,style,x):
    instance : Padding = Padding (
            Panel(
                text,
                width= 20,
                border_style = style,
                ),
            pad = (0,10,0,x)
    )
    return instance

