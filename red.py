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


def non_blocking_readkey():
    """Check if a key is available without blocking."""
    if sys.stdin in select.select([sys.stdin], [], [], 0)[0]:
        return sys.stdin.read(1)
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
    job2 = core.job_progress.add_task("[magenta]Baking", total=200)
    job3 = core.job_progress.add_task("[cyan]Mixing", total=400)

    try:
        with Live(
            Layout("ds"),
            screen=True,
            auto_refresh=True,
            console=core.rich_console,
        ) as core.rich_live_instance:
            core.continue_game()
            while core.running:
                ary = core.job_progress.tasks
                for job in core.job_progress.tasks:
                    if not job.finished:
                        core.job_progress.advance(job.id)
                ke = readkey()

                if ke != "":
                    logger.info(f"Key pressed: {ke}")
                    keyboard_controller.execute_on_key(ke)
                core.rich_console.print("d")
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
