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

if TYPE_CHECKING:
    from core.core import Core


class CustomLayout:
    def __init__(self, core):
        self.core = core
        self.__post_init__()
    def __post_init__(self):
        ...
    def update(self) -> Layout: ...


class LayoutCharacterSelection(CustomLayout):
    def __post_init__(self):
        self.core.console.renderables[0].ary[0].selected = True

    def update(self) -> Layout:
        table = self.core.console.fill_ui_table()
        content = Padding(table, pad=(0, 0, 0, 0))
        layout = Layout("des")
        layout.update(content)
        return layout


class LayoutDefault(CustomLayout):

    def update(self) -> Layout:
        return Layout("des")


class Lsd(CustomLayout):
    def __post_init__(self):
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

    def __post_init__(self):
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

            layout["right"].update(t if self.core.command_mode else "")
        

        #layout["right"].update(self.core.console.right)
        table = None
        if self.core.console.state == "MAIN":
            table: Table = self.core.console.fill_ui_table()
            
        elif self.core.console.state == "INVENTORY":
            table = self.core.console.fill_inventory_table()
        content: Table = table
        layout["middle"].update(
            Panel(
                content,
                padding=(0, 0),
                title="A fallen room",
                title_align="right",
                box=box.ROUNDED,
                subtitle=": [red1]5%[/red1]",
                subtitle_align="right",
                style="",
                border_style="bold light_slate_grey",
            )
        )

        return layout


class LayoutInventory(CustomLayout):
    ...

class LayoutSettings(CustomLayout):
    ...

class LayoutPreGame(CustomLayout):
    ...

class LayoutStartMenu(CustomLayout):

    def update(self):
        table: Table = self.core.console.fill_ui_table()
        content = table
        layout = Layout()
        layout.split_column(Layout(name="up", size=1), Layout(name="down"))

        def top_bar():
            ui = "Home Inventory Settings "
            return ui

        layout["up"].update(top_bar())
        layout["down"].split_row(
            Layout(name="menus", ratio=3),
        )


        ui = self.core.console.fill_ui_table()
        layout["menus"].update(Panel(ui))

        return layout


class LayoutLoading(CustomLayout):


    def __post_init__(self ):

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

