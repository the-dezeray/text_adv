from util.logger import logger
from ui.options import ui_text_panel,Option
def skill_check(core, skill:str = "",limit:int = 0,on_success =None,on_sucess = None,on_fail = None) -> None:
    notices = [""]
    skills = ["hp","dmg","charm","mp","cash"]
    if skill in skills:
            if limit >= core.player[skill] :
                  if on_success:
                        on_success()
    else:
        logger.info("skill not defined")
        return 
