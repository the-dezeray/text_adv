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

from ui.layouts.custom_layout import CustomLayout


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
        console = self.core.console
        layout["down"].split_row(
            Layout(name="left", ratio=console.left_ratio, visible=True),
            Layout(name="middle", ratio=3),
            Layout(name="right", ratio=console.right_ratio, visible=True),
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

        if self.core.in_fight:
            layout["left"].update(player_tab(core=self.core))
            layout["right"].update(enemy_tab(reaper_enemy))
        else:
            layout["left"].update("")
            renderable = ""
            if self.core.command_mode:
                layout["left"].visible = False
                layout["right"].ratio = 2
                renderable = command_mode_layout(self.core)
            layout["right"].update(renderable)

        #layout["right"].update(self.core.console.right)
        table = None
        if self.core.console.state == "MAIN":
            table: Table = self.core.console.fill_ui_table()
            

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
