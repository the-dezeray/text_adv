from util.file_handler import load_yaml_file
from util.logger import logger
from objects.item import Item
from enum import Enum
from typing import List, TypedDict, Optional,cast


class EffectType(Enum):
    BLEED = "bleed"
    STUN = "stun"
    BURN = "burn"
    SLOW = "slow"
    VAMPERISM = "vamperism"
    SHOCK = "shock"
    HOLY = "holy"





class WeaponItem(Item):
    """
    A class representing a weapon item.
    """

    def __init__(self, **kwargs) -> None:
        super().__init__(type="weapon")

        self.name: Optional[str] = kwargs.get("name")
        self.effects: List[EffectType] = self._parse_effects(kwargs.get("effects", []))
        self.defence: int = kwargs.get("defence", 0)
        self.damage: int = kwargs.get("damage", 0)
        self.condition: Optional[str] = kwargs.get("condition")
        self.crit: int = kwargs.get("crit", 0)
        self.cursed: bool = kwargs.get("cursed", False)
        self.description: Optional[str] = kwargs.get("description")
        self.rarity: Optional[int] = kwargs.get("rarity")

    def _parse_effects(self, effects: List[str]) -> List[EffectType]:
        valid_effects = []
        for effect in effects:
            if effect in EffectType._value2member_map_:
                valid_effects.append(EffectType(effect))
            else:
                logger.warning(f"Ignoring unknown effect: {effect}")
        return valid_effects

    def deal_damage(self, player=None) -> None:
        """
        Example damage dealing logic.
        """
        total_damage = self.damage
        if self.crit > 0:
            total_damage += int(self.damage * (self.crit / 100))
        logger.info(f"{self.name} deals {total_damage} damage{' with effects: ' + ', '.join(e.value for e in self.effects) if self.effects else ''}.")
        # Actual logic to affect `player` would go here

    def __repr__(self):
        return f"<WeaponItem name={self.name}, damage={self.damage}, effects={[e.value for e in self.effects]}, rarity={self.rarity}>"


class WeaponFactory:
    WEAPON_DICT = load_yaml_file("data/weapons.yaml")

    mid_level_weapons = [name for name, data in WEAPON_DICT.items() if data.get("lvl") == "mid"]
    high_level_weapons = [name for name, data in WEAPON_DICT.items() if data.get("lvl") == "high"]
    low_level_weapons = [name for name, data in WEAPON_DICT.items()  if data.get("lvl") == "low"]


    @classmethod
    def generate_randomly(cls,level:str = "low",count:int = 1) -> List[WeaponItem]:
        """
        Generate a list of random weapons based on the specified level.
        """
        if level == "mid":
            weapon_names = cls.mid_level_weapons
        elif level == "high":
            weapon_names = cls.high_level_weapons
        else:
            weapon_names = cls.low_level_weapons

        if not weapon_names:
            logger.warning(f"No weapons found for level '{level}'.")
            return []

        from random import sample
        selected_names = sample(weapon_names, min(count, len(weapon_names)))
        return [weapon for name in selected_names if (weapon := cls.generate(name)) is not None]

    def load_data(cls, path="data/weapons.yaml"):
        cls.WEAPON_DICT = load_yaml_file(path)
        logger.info(f"Loaded {len(cls.WEAPON_DICT)} weapons from {path}")

    @classmethod
    def generate(cls, name: str,amount=1) -> Optional[WeaponItem]:
        args = cls.WEAPON_DICT.get(name)
        if args:
            logger.info(f"Generating weapon '{name}'")
            return WeaponItem(**args)
        else:
            logger.warning(f"Weapon '{name}' not found in weapon data.")
            return None
