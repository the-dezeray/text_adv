from rich.live import Live
from pynput.keyboard import Listener
from rich.console import Console
from core.core import Core
from input.keyboard import KeyboardControl
from rich.traceback import install
import time


def main(chapter_id = "5b"):

    install(show_locals=True)
    core = Core()
    core.rich_console = Console()
    core.chapter_id = chapter_id
    keyboard_controller = KeyboardControl(core=core)

    try:
        # Start the keyboard listener
        with Listener(on_press=keyboard_controller.execute_on_key) as core.key_listener:
            with Live(core.interface, refresh_per_second=10,screen=False) as core.love:
                core.continue_game()
                # Main game loop
                while core.running:
                    time.sleep(1)
            core.key_listener.join()

    except KeyboardInterrupt:
        print("\nProgram interrupted by the user.")
        core.running = False  # Optionally set `core.running` to False to cleanly exit the loop
    except Exception:
        core.rich_console.print_exception(show_locals=True)
    finally:
        # Optional cleanup if needed
        print("Exiting program...")
        core.key_listener.stop()  # Ensure the listener is stopped


if __name__ == "__main__":
    main()
