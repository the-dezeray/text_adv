from rich.live import Live
from rich.layout import Layout
from rich.console import Console
from rich.traceback import install
from readchar import readkey
import time

from core.core import Core
from core.keyboard import KeyboardControl


def main(**kwargs):
    chapter_id = kwargs.get("chapter_id", '4a') # 4a as the default
    story = kwargs.get("story", "story.yaml")
    mute = kwargs.get("mute", False)
    tank = kwargs.get("tank", False)
    subchapter = kwargs.get("subchapter", "areas_to_explore.yaml")
    
    core = Core()
    core.rich_console = Console()
    install(show_locals=True,console=core.rich_console)
    core.rich_console.force_terminal = True
    core.rich_console.force_interactive = True
    core.rich_console.stderr = True
    core.rich_console.quiet = False
    core.console.layout = "INGAME"
    core.chapter_id = chapter_id
    keyboard_controller = KeyboardControl(core=core)

    try:
        with Live(
            Layout("ds"),
            screen=True,
            auto_refresh=True,
            console=core.rich_console,
        ) as core.rich_live_instance:
            core.continue_game()
            while core.running:
                ke = readkey()
                if ke != "":
                    keyboard_controller.execute_on_key(ke)
                else:
                    time.sleep(1)
    except KeyboardInterrupt:
        print("keyboard interrupt  pressed")
        core.TERMINATE()
    except Exception:
        core.rich_console.print_exception(show_locals=True)
    finally:
        # Optional cleanup if needed
        print("Exiting program...")


if __name__ == "__main__":
    main()
