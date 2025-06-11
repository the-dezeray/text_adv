from core.events import *
from util.logger import logger
import traceback
from rich.live import Live
from rich.console import Console
from rich.layout import Layout
from typing import Dict, List, Optional, NamedTuple

from core.core import Core

core = Core()
core.test_mode = True
d = core.run_test()
core.console.clear_display()

core.rich_live_instance.stop()
console = Console()
from rich import print
print(d["results"])