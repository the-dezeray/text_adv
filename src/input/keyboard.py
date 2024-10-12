'''Handles Keyboard key'''
from core.fight import fight
from core.game import Game
from core.entities import Entities
def execute_yaml_function(func: dict, core: Game ):

    if isinstance(func, dict):
        target = func.get("target")
        args = func.get("args", "")
      
        if target:
            # Include core in the arguments
            exec(f"{target}({args}, core=core)")

class Keyboard_control():
    def __init__(self,core):
        self.core = core
    def execute_on_key(self,key):
        core = self.core
        """handles keyboard input"""
        input_string :str= str(key)
        input_string = input_string.replace("'","")
        
        match input_string:
            case "Key.space":
                input_string = " "
            case "Key.backspace":
                input_string = ""
                self.current_entry_text =  self.current_entry_text[:-1]
            case "Key.up":
                self.scroll_options(1)         
            case "Key.down":
                self.scroll_options(-1)         
            #RUN COMMAND
            case "Key.enter":
                self.execute_selected_option() 
            #default
            case _:
                pass 
        core.console.refresh() 
    def scroll_options(self,value : int):
        core = self.core
        core.selected_option -= value
        selectable_options = len([option for option in core.options  if option.selectable == True ])
        if core.selected_option < 0 : core.selected_option = selectable_options-1
        if core.selected_option > selectable_options : core.selected_option = 0
        a= [option for option in core.options if option.selectable == True]
        for i,option in enumerate (a) :
            option.selected =False
            if i == core.selected_option :
                option.selected=True
                
    def execute_selected_option(self):
        core = self.core 
        if core.options_displayed:
            for option in core.options:
                if option.selected == True:
                    function = option
            if isinstance(function.func, str):
                core = self.core
                exec(function.func)
                  

            elif callable(function.func):
               function.func()
 
            if core.move_on == False:
                core.next_node = function.next_node

            if function.next_node != None and core.move_on != False :
                core.chapter_id = function.next_node
                for option in core.options:
                    option.selectable = False
                core.game_loop()


