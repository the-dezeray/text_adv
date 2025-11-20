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
