from ui.options import Option, Choices
from util.logger import logger, event_logger
from rich.panel import Panel
from rich.table import Table

from time import sleep

from rich.live import Live
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn
from rich.table import Table

from ui.options import ui_text_panel
scrolls = {
    "ancient_scroll": "You unroll the brittle parchment, the faint scent of dust and something akin to ozone filling your nostrils \n The script, a swirling, alien calligraphy, seems to writhe before your eyes \n As you focus, the words resolve, not into legible text, but into a series of fractured images \n You see… a vast, starless sky, split by a crackling, violet fissure\n You see… a city of obsidian towers, their surfaces reflecting distorted, fleeting faces\n You see… your own hand, aged and withered, clutching a blackened, broken shard\n You see… a pair of luminous, yellow eyes, watching you from the depths of a suffocating darkness\n The images flicker and change, a chaotic slideshow of unsettling visions\n A chill creeps up your spine, and you feel a prickling sensation, as if unseen eyes are now fixed upon you, both within and beyond the scroll's strange depths\n Do you dare to continue deciphering these fractured glimpses, or do you quickly roll the scroll shut, hoping to banish the unsettling visions?"
}


@event_logger
def read(core, scroll: str = ""):
    string = scrolls.get(scroll, None)
    if string != None:
        core.options = []

        core.options.append(
            ui_text_panel(text=string)
        )
        core.options.append(Choices(renderable= Option(text="Proceed", func=lambda: core.goto_next(), selectable=True)))
        grid = Table.grid()
        grid.add_column()

        job_progress = Progress(
            "{task.description}",
            SpinnerColumn(),
            BarColumn(),
            TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
        )
        job1 = job_progress.add_task("[green]Cooking")
        job2 = job_progress.add_task("[magenta]Baking", total=200)
        job3 = job_progress.add_task("[cyan]Mixing", total=400)

        total = sum(task.total for task in job_progress.tasks)
        overall_progress = Progress()
        overall_task = overall_progress.add_task("All Jobs", total=int(total))

        progress_table = Table.grid()
        progress_table.add_row(
            Panel.fit(
                overall_progress,
                title="Overall Progress",
                border_style="green",
                padding=(2, 2),
            ),
            Panel.fit(
                job_progress, title="[b]Jobs", border_style="red", padding=(1, 2)
            ),
        )

        grid.add_row(progress_table)
        grid.add_row("[b]You have:[/b]")
        grid.add_row(
            Panel(
                "lost a lof bold",
                subtitle="curse",
                style="bold yellow",
                subtitle_align="right",
            )
        )
        grid.add_row(
            Panel(
                "received key of death",
                subtitle="gift",
                style="bold green",
                subtitle_align="right",
            )
        )
        grid.add_row(
            Panel(
                "recieved curse you will meet death soon hehehe",
                subtitle="prophecy",
                style="bold purple",
                subtitle_align="right",
            )
        )
        core.console.right = grid
