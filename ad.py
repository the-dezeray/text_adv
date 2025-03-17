from rich_pixels import Pixels
from rich.console import Console

from rich_pixels import Pixels
from rich.console import Console
from PIL import Image

console = Console()

with Image.open("./sdf.png") as image:
    pixels = Pixels.from_image(image,resize= (80,50))

console.print(pixels)