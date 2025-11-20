
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


class LayoutType(Enum):
    """Enum for different layout types"""
    CHARACTER_SELECTION = "character_selection"
    DEFAULT = "default"
    AI_STUDIO = "ai_studio"
    LSD = "lsd"
    IN_GAME = "in_game"
    INVENTORY = "inventory"
    SETTINGS = "settings"
    PRE_GAME = "pre_game"
    START_MENU = "start_menu"
    MENU= "menu"
    ABOUT_US = "about_us"
    SELECT_STORY = "select_story"
    LOADING = "loading"

from dataclasses import dataclass
from typing import Optional, List
@dataclass
class LayoutConfig:
    """Configuration for layout components"""
    left_ratio: int = 1
    middle_ratio: int = 3
    right_ratio: int = 1
    top_ratio: int = 4
    bottom_ratio: int = 1
    panel_width: int = 50
    panel_title: str = "terminal adventure"
    panel_subtitle: str = "v3"
    show_left: bool = True
    show_right: bool = True


class LayoutFactory:
    """Factory class for creating layout instances"""
    from ui.layouts.default import LayoutDefault
    from ui.layouts.character_selection import LayoutCharacterSelection
    from ui.layouts.ai_studio import LayoutAIStudio
    from ui.layouts.lsd import Lsd
    from ui.layouts.ingame import LayoutInGame
    from ui.layouts.inventory import LayoutInventory
    from ui.layouts.settings import LayoutSettings
    from ui.layouts.pre_game import LayoutPreGame
    from ui.layouts.start_menu import LayoutStartMenu
    from ui.layouts.about_us import LayoutAboutUs
    from ui.layouts.select_story import LayoutSelectStory
    from ui.layouts.loading import LayoutLoading

    _layout_classes = {
        LayoutType.CHARACTER_SELECTION: LayoutCharacterSelection,
        LayoutType.DEFAULT: LayoutDefault,
        LayoutType.AI_STUDIO: LayoutAIStudio,
        LayoutType.LSD: Lsd,
        LayoutType.IN_GAME: LayoutInGame,
        LayoutType.INVENTORY: LayoutInventory,
        LayoutType.SETTINGS: LayoutSettings,
        LayoutType.PRE_GAME: LayoutPreGame,
        LayoutType.START_MENU: LayoutStartMenu,
        LayoutType.ABOUT_US: LayoutAboutUs,
        LayoutType.MENU: LayoutStartMenu,
        LayoutType.SELECT_STORY: LayoutSelectStory,
        LayoutType.LOADING: LayoutLoading,
    }
    
    @classmethod
    def create_layout(
        cls,
        layout_type: LayoutType,
        core: "Core",
        config: Optional[LayoutConfig] = None
    ) -> LayoutDefault:
        """Create a layout instance of the specified type"""
        layout_class = cls._layout_classes.get(layout_type)
        if not layout_class:
            raise ValueError(f"Unknown layout type: {layout_type}")
        
        return layout_class(core)
    
    @classmethod
    def get_available_layouts(cls) -> List[LayoutType]:
        """Get list of available layout types"""
        return list(cls._layout_classes.keys())

