from ui.options import CustomRenderable
from util.logger import logger, event_logger
from util.file_handler import load_yaml_file


@event_logger
def explore(core=None, area=None):
    stories = load_yaml_file("data/areas_to_explore.yaml")

    story: dict = stories["forest_light"]

    if story != None:
        core.game_engine.set_temp_story(story)
        core.chapter_id = "1a"
        core.continue_game()
        print("exit")
    else:
        logger.error(f"story: {area} not defined ")
