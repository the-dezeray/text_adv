from __future__ import annotations
from enum import Enum
from rich.table import Table
from rich.padding import Padding
from rich.panel import Panel
from rich.align import Align
from rich.rule import Rule
from rich import box
from ui.components import player_tab,command_mode_layout
from ui.options import CustomRenderable
from rich.layout import Layout
from typing import TYPE_CHECKING, Tuple
from abc import ABC , abstractmethod 
if TYPE_CHECKING:
    from core.core import Core


class CustomLayout(ABC):
    def __init__(self, core: "Core")->None:
        self.core = core
        self.layout = Layout()
        self.setup()
        
    @abstractmethod
    def setup(self)->None:
        raise NotImplementedError("setup method must be implemented")
    @abstractmethod
    def update(self) -> Layout:
        raise NotImplementedError("update method must be implemented")


class LayoutCharacterSelection(CustomLayout):
    def setup(self):
        self.core.console.renderables[0].ary[0].selected = True

    def update(self) -> Layout:
        table = self.core.console.fill_ui_table()
        content = Padding(table, pad=(0, 0, 0, 0))
        layout = Layout("des")
        layout.update(content)
        return layout


class LayoutDefault(CustomLayout):
    def setup(self):
        ...
    def update(self) -> Layout:
        return Layout("des")
class LayoutAIStudio(CustomLayout):
    def setup(self)  :
        self.core.command_mode = True
        self.core.console.clear_display()
        self.core.ai.setup()
     
    def update(self) -> Layout:
        from  ui.components import input_mode_layout
        layout = Layout()
        
        layout.split_row(
            Layout(name="left", ratio=1, visible=True),
            Layout(name="middle", ratio=3),
            Layout(name="right", ratio=1, visible=True),
        )

        layout["middle"].split_column(
            Layout(name="top", ratio=4),
            Layout(name="bottom", ratio=1),
        )
        layout["left"].update("")
        layout["right"].update("")
        layout["top"].update(self.core.console.fill_ui_table())
        layout["bottom"].update(Align(input_mode_layout(self.core),align="center",vertical="middle"))
        return layout
class Lsd(CustomLayout):
    def setup(self):
        self.core.console.renderables[0].ary[0].selected = True

    def update(self) -> Layout:
        layout = Layout()
        layout.split(Layout(name="View", ratio=10), Layout(name="control"))
        layout["View"].split_row(Layout(name="Picture"), Layout(name="Stats"))

        grid = [Panel("") for _ in range(4)]
        grid[self.core.selected_option] = Panel(
            renderable="", style="bold red", height=2, width=7
        )
        from rich.columns import Columns

        layout["control"].update(Columns(renderables=grid, align="center"))
        return layout


class LayoutInGame(CustomLayout):

    def setup(self):
        from util.logger import logger
        logger.info("Setting up LayoutInGame")
        self.core.continue_game()
    def update(self):

        layout = Layout()
        layout.split_column(
            Layout(name="up", size=1),
            Layout(name="down"),

        )

        def top_bar():
            ui = "Home Inventory Settings "
            return ui

        layout["up"].update(top_bar())
        layout["down"].split_row(
            Layout(name="left", ratio=1, visible=True),
            Layout(name="middle", ratio=3),
            Layout(name="right", ratio=1, visible=True),
        )
        from typing import List
        class Enemy:
            def __init__(self, name: str, hp: int, max_hp: int, attack: int, defense: int, speed: int,
                        image_paths: List[str], description: str = "A fearsome foe.",
                        loot: List[str] = [""], abilities: List[str] =[""],
                        icon_resize: Tuple[int, int] = (16, 16),
                        xp_value: int = 0, level: int = 1):
                self.name = name
                self.hp = hp
                self.max_hp = max_hp
                self.attack = attack
                self.defense = defense
                self.speed = speed
                self.image_paths = image_paths
                self.description = description
                self.loot = loot if loot else []
                self.abilities = abilities if abilities else []
                self.icon_resize = icon_resize
                self.xp_value = xp_value
                self.level = level
                # For draw_bar, an enemy might have a 'fury' or 'stamina' bar instead of MP/EXP
                # For simplicity, we'll focus on HP for the enemy vitals bar.

        from ui.components import enemy_tab
        reaper_enemy:Enemy = Enemy(
        name="Grim Reaper",
        hp=150,
        max_hp=200,
        attack=25,
        defense=10,
        speed=15,
        image_paths="1.png", # Use the dummy paths or your actual image paths
        description="A harbinger of doom, clad in shadows.",
        abilities=["Soul Scythe", "Shadow Cloak", "Deathly Gaze"],
        loot=["Dark Soul Gem", "Scythe Fragment"],
        icon_resize=(24,24), # Slightly larger icon
        xp_value=500,
        level=10
        )
        t = command_mode_layout(self.core) if self.core.command_mode else enemy_tab(reaper_enemy)
        if self.core.in_fight:
            layout["left"].update(player_tab(core=self.core))
            layout["right"].update(t)
        else:
            layout["left"].update("")

            layout["right"].update(self.core.console.right )
        

        #layout["right"].update(self.core.console.right)
        table = None
        if self.core.console.state == "MAIN":
            table: Table = self.core.console.fill_ui_table()
            
        elif self.core.console.state == "INVENTORY":
            table = self.core.console.fill_inventory_table()
        content: Table = table
        layout["middle"].update(
            Padding(content)
        )
        """          Panel(
                content,
                padding=(0, 0),
                title="A fallen room",
                title_align="right",
                box=box.ROUNDED,
                subtitle=": [red1]5%[/red1]",
                subtitle_align="right",
                style="",
                border_style="bold light_slate_grey",
            )"""
        return layout


class LayoutInventory(CustomLayout):
    ...

class LayoutSettings(CustomLayout):
    ...

class LayoutPreGame(CustomLayout):
    ...

class LayoutStartMenu(CustomLayout):
    
    def setup(self)->None:
  
        self.layout = Layout()
        self.layout.split_row(Layout(name="left"), Layout(visible=False,name="right"))
    def update(self):
        table: Table = self.core.console.fill_ui_table()
        content = table
        


        def top_bar():
            ui = "Home Inventory Settings "
            return ui

        self.layout["left"].split_row(
            Layout(name="menus"),
        )


        ui = Panel( self.core.console.fill_ui_table(),width =50,title="terminal adventure",title_align="center",subtitle ="v3",subtitle_align="right")
        self.layout["menus"].update(Align(ui,align="center",vertical = "middle"))

        return self.layout
class LayoutAboutUs(CustomLayout):
    
    def setup(self)->None:
  
        self.layout = Layout()
        self.layout.split_row(Layout(name="left"), Layout(visible=False,name="right"))
    def update(self):
        table: Table = self.core.console.fill_ui_table()
        content = table
        


        def top_bar():
            ui = "Home Inventory Settings "
            return ui

        self.layout["left"].split_row(
            Layout(name="menus"),
        )


        ui =self.core.console.fill_ui_table()
        self.layout["menus"].update(Align(ui,align="center",vertical = "middle"))

        return self.layout

class LayoutSelectStory(CustomLayout):
    def __init__(self, core:"Core"):
        self.core = core
        self.layout = Layout()
    
    def setup(self)->None:
  
        self.layout = Layout()
        self.layout.split_row(Layout(name="left"), Layout(visible=False,name="right"))        
    def update(self):
        
        table: Table = self.core.console.fill_ui_table()
        content = table
        


        def top_bar():
            ui = "Home Inventory Settings "
            return ui

 

        ui = self.core.console.fill_ui_table(show_lines=True,show_edge = True)
        self.layout.update(Align(ui,align="center"))

        return self.layout

class LayoutLoading(CustomLayout):


    def setup(self ):

        self.core.console.renderables= ["dsiree"]
        from core.timer import Timer
        self.core.timer = Timer(time = 3,func =self.core.from_loading_to_start_menu)
    def update(self):
        from rich.align import Align
        lines = "/////////////////////////////////////////////////////////////"
     
        from rich.console import Group
        panel_group = Group(
        lines,
        f"{self.core.timer.time}",
        )
        ui = Layout(renderable=panel_group)
        return Layout(Padding(renderable=ui,pad = (10,)))
class LayoutInventory(CustomLayout):

    def update(self):
        

        layout = Layout()

        #ui = self.core.console.fill_ui_table()
        #weapons = Choices()
        renderable = self.core.console.fill_inventory_table()
        layout.update(Align(Panel(renderable=renderable,height=32,width=100),align="center"))

        return layout

