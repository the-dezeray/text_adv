from util.logger import logger
from ui.options import ui_text_panel,Option
from typing import TYPE_CHECKING

if TYPE_CHECKING:
      from core.core import Core
def skill_check(core:"Core", skill:str = "",limit:int = 0,on_success =None,on_sucess = None,on_fail = None) -> None:
    notices = [""]
    skills = {"hp":core.player.hp,"dmg":core.player.dmg,"charm":core.player.charm,"mp":core.player.mp,"cash":core.player.cash}
    if skill in skills:
            #if limit >= skills[skill] :
                if on_success:
                    on_success()
                core.goto_next()
    else:
        logger.info("skill not defined")
        return 
