from ui.options import Option, Choices
def get_random():
    return 1
def trap(core= None,type :str= None):
    trap = {"name":"fire trap","damage" :1}
    core.options.append(Choices(renderable=Option(text="You have been hit by a trap",func=lambda:core.goto_next())))
    core.player.contact_with_trap(trap = trap)