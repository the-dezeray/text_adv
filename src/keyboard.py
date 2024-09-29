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

                core.selected_option -=1
                selectable_options = len([option for option in core.options  if option.selectable == True ])
             
                if core.selected_option < 0 : core.selected_option = selectable_options-1
                if core.selected_option > selectable_options : core.selected_option = 0
                a= [option for option in core.options if option.selectable == True]
                for i,option in enumerate (a) :
                    option.selected =False
                    if i == core.selected_option :
                        option.selected=True
                        
                        
                    
            case "Key.down":
                core.selected_option += 1
        
            #RUN COMMAND
            case "Key.enter":
            
                if core.options_displayed:
                    for option in core.options:
                        if option.selected == True:
                            function = option
                    if isinstance(function.func, str):
                        if len(function.func) > 1 and function.func != None:
                            exec(function.func)

                    elif callable(function.func):
                        function.func()
        
                    if function.next_node != None:
                        self.chapter_id = function.next_node
                        for option in self.options:
                            option.selectable = False
                        core.game_loop()
            #default
            case _:
                pass 
        core.console.refresh() 

