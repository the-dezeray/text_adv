"""random documentation"""

from rich.live import Live
from rich.layout import Layout
from rich.console import Console
from rich.traceback import install
from readchar import readkey
import time
from util.logger import logger
from core.core import Core
from core.keyboard import KeyboardControl
from rich.progress import Progress
import sys
import select
import threading
import queue


class NonBlockingInput:
    def __init__(self):
        self.input_queue = queue.Queue()
        self.thread = threading.Thread(target=self._input_thread, daemon=True)
        self.thread.start()

    def _input_thread(self):
        while True:
            key = readkey()
            if key:
                self.input_queue.put(key)

    def get_key(self):
        try:
            return self.input_queue.get_nowait()
        except queue.Empty:
            return None


def non_blocking_readkey():
    """Check if a key is available without blocking."""
    if sys.stdin in select.select([sys.stdin], [], [], 0)[0]:
        key = sys.stdin.read(1)

        # Check if it's an escape sequence (for arrow keys)
        if key == "\x1b":  # The beginning of an escape sequence
            key += sys.stdin.read(2)  # Read the rest of the escape sequence
            if key == "\x1b[A":
                return "UP"  # Up arrow key
            elif key == "\x1b[B":
                return "DOWN"  # Down arrow key
            elif key == "\x1b[C":
                return "RIGHT"  # Right arrow key
            elif key == "\x1b[D":
                return "LEFT"  # Left arrow key
        elif key == "q":
            return "q"  # 'q' key
        elif key == "a":
            return "a"  # 'a' key

        return None  # No relevant key pressed
    return None


def main(**kwargs):
    chapter_id = kwargs.get("chapter_id", "4a")  # 4a as the default
    story = kwargs.get("story", "story.yaml")
    mute = kwargs.get("mute", False)
    tank = kwargs.get("tank", False)
    subchapter = kwargs.get("subchapter", "areas_to_explore.yaml")

    core = Core()
    core.rich_console = Console()
    install(show_locals=True, console=core.rich_console)
    core.rich_console.force_terminal = True
    core.rich_console.force_interactive = True
    core.rich_console.stderr = True
    core.rich_console.quiet = False
    core.console.layout = "INGAME"
    core.chapter_id = chapter_id
    keyboard_controller = KeyboardControl(core=core)
    job1 = core.job_progress.add_task("[green]Cooking")
    job2 = core.job_progress.add_task("[magenta]Baking", total=1200)
    job3 = core.job_progress.add_task("[cyan]Mixing", total=1400)
    input_handler = NonBlockingInput()

    with Live(
        Layout("ds"),
        screen=True,
        auto_refresh=True,
        console=core.rich_console,
    ) as core.rich_live_instance:
        core.continue_game()
        while core.running:
            key = input_handler.get_key()
            if key:
                keyboard_controller.execute_on_key(key)
            ary = core.job_progress.tasks
            for job in core.job_progress.tasks:
                if not job.finished:
                    core.job_progress.advance(job.id)
            time.sleep(0.01)


if __name__ == "__main__":
    main()
