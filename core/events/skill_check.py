from util.logger import logger
from ui.options import ui_text_panel,Option
from typing import TYPE_CHECKING
from rich.rule import Rule
from rich.panel import Panel
if TYPE_CHECKING:
      from core.core import Core
def skill_check(core:"Core", skill:str = "",limit:int = 0,on_success =None,on_sucess = None,on_fail = None) -> None:
    notices = [""]

    skill_value = core.player.get_attribute(key=skill)
    if  not skill_value :
        logger.info(skill+"not definded ")
        core.console.print(f"[red]Skill {skill} not defined[/red]")
        return

    if skill_value >= limit:
        if on_success:
            on_success()
        core.console.print(Rule("[blink]You were tessted", align="center", style="bold red1"))
        core.goto_next()
    else:
        if on_fail:
            on_fail()
            core.console.print(Rule(title="You were tessted ", align="center", style="green"))
        core.goto_next()
    return
