from rich_pixels import Pixels
from rich.console import Console

console = Console()
pixels = Pixels.from_image_path("sword10.png",)
console.print(pixels)