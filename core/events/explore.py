from ui.options import Option, Choices
from util.logger import logger
from util.file_handler import load_yaml_file
def explore(core= None,area= None):
    stories = load_yaml_file("data/areas_to_explore.yaml")

    story : dict = stories["forest_light"]
 
    if story != None:
        core.chapter_id = "1a"
        core.temp_story = story
        core.continue_game()
        print("exit")
    else:
        logger.error(f"story: {area} not defined ")