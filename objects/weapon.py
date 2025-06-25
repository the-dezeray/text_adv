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

    @classmethod
    def load_data(cls, path="data/weapons.yaml"):
        cls.WEAPON_DICT = load_yaml_file(path)
        logger.info(f"Loaded {len(cls.WEAPON_DICT)} weapons from {path}")

    @classmethod
    def generate(cls, name: str) -> Optional[WeaponItem]:
        args = cls.WEAPON_DICT.get(name)
        if args:
            logger.info(f"Generating weapon '{name}'")
            return WeaponItem(**args)
        else:
            logger.warning(f"Weapon '{name}' not found in weapon data.")
            return None
