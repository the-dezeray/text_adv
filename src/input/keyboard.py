'''Handles Keyboard key'''
from core.fight import fight
from core.entities import Entities
def get_selectable_options(options : list):
    return [option for option in options  if option.selectable == True ]

def execute_yaml_function(func: dict, core ):

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
                core.selected_option = 1    
                self.execute_selected_option() 
            #default
            case _:
                pass 
        core.console.refresh() 
        
    def scroll_options(self,value : int):
        core = self.core
        core.selected_option -= value
        selectable_options = get_selectable_options(core.options)
        options_len= len(selectable_options)
        if core.selected_option < 0 :
             core.selected_option = options_len-1
        elif core.selected_option >= options_len :
             core.selected_option = 0
        
        
        for i,option in enumerate (selectable_options) :
            option.selected = False
            if i == core.selected_option :
                option.selected=True
                
    def execute_selected_option(self):
        from core.core import Core
        core :  Core = self.core 

        for option in core.options:
            if option.selected == True:

                if isinstance(option.func, str):
                    core = self.core
                    exec(option.func)
                    
                elif callable(option.func):
                    option.func()
    
                    core.next_node = option.next_node
                else:
                    core.chapter_id = option.next_node
                    core.continue_game()



