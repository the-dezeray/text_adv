'''handle dispalying and printing on screen'''
from rich.table import Table
from rich.padding import Padding
from rich.panel import Panel
from rich.align import Align
from ui.options import Option
from rich import box
class Console():

    def __init__(self,core):
        self.core = core
        self.layout = None
        self.table = None
        
    def refresh(self):
        table = self.build_table()
        self.core.interface['main'].update(Padding(table,pad=(0,0,0,0)))
        self.core.love.update(self.core.interface)
        
        
    def build_table(self):
        core = self.core

        self.table = Table(expand=True,show_edge=True,show_header=False,style='bold red',box=box.ROUNDED )
        self.table.add_column(justify="center")

        options : list = core.options
        
        if len(options) > 9 :
            options = options[9:]
        v = True
        for option in options:
            if option.selected:
                v = False
                
        if v == True:
            if options:
                options[0].selected = True

        for index in range(0,len(options)):  
         
            option = options[index]
            style = "none"
            horizontal_align = "left"
            left_padding = 0
            
            if option.selected:
                if options[index].preview:
                    options[index].preview()
                style = "bold green"
                left_padding += 5
          
            
            #self.table.add_row(Padding(Panel(option.text,border_style=style),pad =(0,0,0,x)))
            if option.type == 'header' :
                renderable  = _dialogue_text(text = option.text,style = style)
            elif option.type == "enemy_health_bar":
                renderable  = _enemy_health_bar(text = option.text,style = style)
            elif option.type.endswith("profile"):
                
                if option.type == "enemy_profile": 
                    horizontal_align = "left"
                else :
                    horizontal_align = "left"
                renderable  = _dialogue_text(text = option.text,style = style)
            else: 
                renderable = _option_button(text = option.text,style = style,left_padding=left_padding)

            
            self.table.add_row(Align((renderable),align =horizontal_align))
        return self.table 
def _dialogue_text(text,style):
    instance : Padding = Padding ( text,pad =(2,0,0,0)
    )
    return instance
def _enemy_health_bar(text,style):
   
    instance :Padding  =Padding( Panel(text), pad = (0,0,0,0) )
    return instance
def _option_button(text,style,top_padding = 0,right_padding = 0,bottom_padding = 0, left_padding = 0):
    instance : Padding = Padding ( Panel(text,width= 20,border_style = style,), pad = (top_padding,right_padding,bottom_padding,left_padding) )
    return instance


def _display_player_weapons():
    pass
def _display_alernative():
    pass
def show_player_actions(player):
    _display_player_weapons(player)
    _display_alernative()
    
