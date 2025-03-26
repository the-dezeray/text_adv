"""core of the game"""

from util.file_handler import load_yaml_file  # pylint: disable=unused-import
from ui.options import Option, Choices
from rich.layout import Layout
from objects.entities import Entities  # pylint: disable=unused-import
from objects.item import Items
from objects.player import Player
from ui.console import Console

from util.logger import logger

# Unused functions called using the exec functions
from core.events.navigate import navigate  # noqa: F401  # type: ignore
from core.events.explore import explore  # noqa: F401
from core.functions import receive  # noqa: F401  # type: ignore
from core.events.fight import fight  # noqa: F401  # type: ignorei
from core.events.rest import rest  # noqa: F401  # type: ignore
from core.events.read import read  # noqa: F401  # type: ignore
from core.events.meditate import meditate  # noqa: F401  # type: ignore
from core.events.run import run  # noqa: F401  # type: ignore
from core.events.search import search  # noqa: F401  # type: ignore
from core.events.trap import trap  # noqa: F401  # type: ignore
from core.events.sneak import sneak  # noqa: F401  # type: ignore
from core.events.encounter import encounter  # noqa: F401  # type: ignore
from core.events.goto import goto  # noqa: F401  # type: ignore
from core.events.haverst import harvest  # noqa: F401  # type: ignore
from core.events.interact import interact  # noqa: F401  # type: ignore
from core.events.investigate import investigate  # noqa: F401  # type: ignore
from core.events.place import place  # noqa: F401  # type: ignore
from core.events.shop import shop  # noqa: F401  # type: ignore
from core.events.search_in import search_in  # noqa: F401  # type: ignore

from rich.padding import Padding
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn
from typing import TYPE_CHECKING
import datetime
import sys

if TYPE_CHECKING:
    from ui.console import Console
    from rich.live import Live


class Core:
    def __init__(self) -> None:
        self.rich_console: "Live" = None
        self.running: bool = True
        self.ant = []
        self.in_fight: bool = False
        self.story: dict = load_yaml_file("data/story.yaml")
        self._chapter_id = -1  # default value
        self.progress = Progress()
        self.in_game = True
        self.rich_live_instance = None
        self.temp_story = None
        self.move_on = True
        self.entity = None
        self.key_listener = None
        self.s = "options"
        self.selected_option: int = 0
        self.others = []
        self._disable_command_mode = False
        self._layout = Layout()
        self.player = Player()
        self.player_turn: bool = False
        self.next_node: str = None
        self.options = []
        self.current_entry_text: str = ""
        self._command_mode: bool = False
        self._state = "INGAME"
        self.job_progress = Progress(
            "{task.description}",
            SpinnerColumn(),
            BarColumn(),
            TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
        )
        self.console: Console = Console(core=self)
        self._post_initialize()
        self.job_progress = Progress(
            "{task.description}",
            SpinnerColumn(),
            BarColumn(),
            TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
        )
        self.overall_progress = Progress()
        self.overall_task = self.overall_progress.add_task("All Jobs", total=int(1000))

    def _get_next_nodes():
        story = load_yaml_file("data/story.yaml")
        ary = []
        for _chapter in story.items():
            for i in _chapter[1]["choices"]:
                ary.append(i["next_node"])
        return ary

    def exit() -> None:
        sys.exit()

    def _post_initialize(self) -> None:
        current_time = datetime.datetime.now()
        logger.info(f"New game instance {current_time}")
        self.check_story()

    def layout_transtion_to(self, layout):
        match layout:
            case "INGAME":
                self.chapter_id = "1a"
                self.console.layout = "INGAME"
                self.continue_game()
            case "NEWGAME":
                self.console.layout = "NEWGAME"
                ...
            case "SETTINGS":
                ...
            case "ABOUT US":
                ...

    def show_inventory(self):
        self.state = "INVENTORY"

    def show_settings(self):
        self.state = "SETTINGS"

    def show_stats(self):
        self.state = "STATS"

    def show_menu(self):
        self.options = []
        from art import text2art

        # Define menu options with ASCII text
        menu_items = [
            {
                "text": "Continue game",
                "function": lambda: self.layout_transtion_to("INGAME"),
                "next_node": None,
            },
            {
                "text": "New game",
                "function": lambda: self.layout_transtion_to("NEWGAME"),
                "next_node": None,
            },
            {
                "text": "Settings",
                "function": lambda: self.layout_transtion_to("SETTINGS"),
                "next_node": None,
            },
            {
                "text": "About us",
                "function": lambda: self.layout_transtion_to("ABOUTUS"),
                "next_node": None,
            },
            {"text": "Leave", "function": lambda: self.TERMINATE(), "next_node": None},
        ]

        self.options.append(Choices(ary=menu_items, menu_type="menu"))
        self.console.layout = "MENU"

    def check_story(self) -> None:
        print("Checking story")

    @property
    def chapter_id(self) -> str:
        return self._chapter_id

    @chapter_id.getter
    def chapter_id(self) -> str:
        return self._chapter_id

    @chapter_id.setter
    def chapter_id(self, value) -> None:
        story = self.story if self.temp_story is None else self.temp_story
        if value == "-1" or value == -1:
            value = -1
        elif value not in story:
            logger.critical(
                f"The chapter '{value}' is not defined in the default yaml file. check if defined in yaml"
            )
            raise ValueError(
                f"The chapter '{value}' is not defined in the default yaml file. check if defined in yaml"
            )

        self._chapter_id = value

    def execute_yaml_function(self, func: str) -> any:
        core = self
        logger.info(f"Executing function: {func}")
        local_scope = {"core": core}  # Define the scope where 'core' is available
        try:
            exec(func, globals(), local_scope)
        except Exception as e:
            logger.error(f"chapter : {self.chapter_id}")
            logger.error(
                f"Error executing function: {func} - {e} : function exists in yaml file however execution failed mostly likely to the function not defined as  a local or global variable"
            )

    @property
    def command_mode(self):
        return self._command_mode

    @command_mode.getter
    def command_mode(self):
        return self._command_mode

    @command_mode.setter
    def command_mode(self, value):
        if not self._disable_command_mode:
            self._command_mode = bool(value)  # Ensure it is a boolean
            self.console.toggle_command_mode()

        self.chapter_id = "1a"
        self.console.layout = "INGAME"

    def TERMINATE(self):
        self.running = False
        self.console.options = []

        quit()
        exit()

    def continue_game(self) -> None:
        # set the selected option to 0
        self.selected_option = 0
        """if self.chapter_id == -1:
            self.console.layout = "CHARACTER_SELECTION"""
        if self.chapter_id == -1:
            self.show_menu()

        else:
            if self.temp_story is not None:
                story = self.story
            else:
                story = self.temp_story
            current_chapter = self.story[self.chapter_id]
            self.options = []
            from ui.options import ui_text_panel

            self.options.append(ui_text_panel(text=current_chapter["text"]))

            # or index,choice in enumerate(current_chapter["choices"]):
            self.options.append(Choices(current_chapter["choices"]))
        self.console.refresh()

    def goto_next(self) -> None:
        """Go to the next node in the story"""
        logger.info("Going to next node")

        self.chapter_id = self.next_node
        self.continue_game()

    def clear_logs(): ...
    def restart(): ...
    def raw_exec(): ...
