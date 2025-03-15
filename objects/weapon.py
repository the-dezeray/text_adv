from util.file_handler import load_yaml_file
from util.logger import logger
from objects.item import Item
from enum import Enum


class EFFECTS(Enum):
    BLEED = "bleed"
    STUN = "stun"
    BURN = "burn"
    SLOW = "slow"
    VAMPERISM = "vamperism"
    SHOCK = "shock"
    HOLY = "holy"


class WeaponItem(Item):
    """
    weapon class
    effects: ["bleed","stun","burn","slow","vamperism","shock","holy"] are the possible effects

    """

    def __init__(self, **kwargs) -> None:
        super().__init__(type="weapon")
        self.type = "weapon"  # there will be the same for all

        self.name: str = kwargs.pop("name", None)  # Extract 'name' from kwargs
        self.effects: list[str] = kwargs.pop(
            "effects", []
        )  # Extract 'effects' from kwargs
        self.defence: int = kwargs.pop("defence", 0)  # Extract 'defence' from kwargs
        self.damage: int = kwargs.pop("damage", 0)  # Extract 'damage' from kwargs
        self.condition: str = kwargs.pop(
            "condition", None
        )  # Extract 'condition' from kwargs
        self.crit: int = kwargs.pop("crit", 0)  # Extract 'crit' from kwargs
        self.cursed: bool = kwargs.pop("cursed", False)  # Extract 'cursed' from kwargs
        self.description: str = kwargs.pop(
            "description", None
        )  # Extract 'description' from kwargs
        self.rarity: int = kwargs.pop(
            "rarity", None
        )  # Extract 'rarity' from kwargs 0 to 10

    def deal_damage(self, player=None) -> None:
        pass


class Weapon:
    WEAPON_DICT = load_yaml_file("data/weapons.yaml")

    @classmethod
    def generate(cls, name) -> WeaponItem:
        logger.info(f"Generating weapon {name}")
        return WeaponItem(**cls.WEAPON_DICT[name])
