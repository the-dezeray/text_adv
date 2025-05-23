from ui.options import CustomRenderable
from util.logger import logger, event_logger
from util.file_handler import load_yaml_file


@event_logger
def explore(core=None, area=None):
    areas = ["creak","swamp","webs","bolders"]

    if area in areas:
        match area:
    else:
        logger.error(f"story: {area} not defined ")
