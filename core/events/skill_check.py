from util.logger import logger
from ui.options import ui_text_panel,Option
from typing import TYPE_CHECKING

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
            core.goto_next()
    else:
        if on_fail:
            on_fail()
            core.goto_next()
    return
