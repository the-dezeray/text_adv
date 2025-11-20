from pathlib import Path

ROOT_DIR  = Path(__file__).resolve().parent.parent

def asset(*parts:str)->Path:
    return ROOT_DIR / "assets" / Path(*parts)
def world_asset(*parts:str)->Path:
    return asset("world",*parts)
