from rich.live import Live
from rich.console import Console
from rich.traceback import install
from readchar import readkey
import time

from core.core import Core
from core.keyboard import KeyboardControl


def main(chapter_id="4a"):
    install(show_locals=True)
    core = Core()
    core.rich_console = Console()
    core.rich_console.force_terminal = True
    core.rich_console.force_interactive = True
    core.rich_console.stderr = True
    core.rich_console.quiet = False
    core.console.layout = "INGAME"
    core.chapter_id = chapter_id
    keyboard_controller = KeyboardControl(core=core)

    try:
        with Live(
            core.interface,
            refresh_per_second=10,
            screen=True,
            console=core.rich_console,
        ) as core.love:
            core.continue_game()
            while core.running:
                ke = readkey()
                if ke != "":
                    keyboard_controller.execute_on_key(ke)
                else:
                    time.sleep(1)
    except KeyboardInterrupt:
        print("\nProgram interrupted by the user.")
        core.running = (
            False  # Optionally set `core.running` to False to cleanly exit the loop
        )
    except Exception:
        core.rich_console.print_exception(show_locals=True)
    finally:
        # Optional cleanup if needed
        print("Exiting program...")


if __name__ == "__main__":
    main()
