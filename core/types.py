from enum import Enum, StrEnum, IntEnum, STRICT
from typing import Dict, ClassVar
from dataclasses import dataclass, field
from collections import defaultdict
from abc import ABC, abstractmethod


class DamageTag(StrEnum, boundary=STRICT):
    """Tags applied to damage instances - multiple can apply simultaneously."""

    ALL = "All"

    PHYSICAL = "Physical"
    PHASE = "Phase"
    CORROSION = "Corrosion"
    BURN = "Burn"
    FREEZE = "Freeze"
    HYDRO = "Hydro"
    ELECTRIC = "Electric"

    MELEE = "Melee"
    LIGHT_AMMO = "Light Ammo"
    MEDIUM_AMMO = "Medium Ammo"
    HEAVY_AMMO = "Heavy Ammo"
    SHOTGUN_AMMO = "Shotgun Ammo"

    SUPPORT_ACTION = "Support Action"
    INTERCEPTION = "Interception"
    COUNTERATTACK = "Counterattack"
    # OUT_OF_TURN = 'Out-of-Turn'
    PASSIVE = "Passive"
    ACTIVE = "Active"

    TARGETED = "Targeted"
    AREA_OF_EFFECT = "AoE"

    CONFECTANCE = "Confectance"
    ULTIMATE = "Ultimate"
    BASIC = "Basic"

    EXPOSED = "Exposed"
    STABILITY_BROKEN = "Stability Broken"
    BOSS = "Boss"


@dataclass
class DamageTagMultipliers:
    """Contains multipliers for each DamageTag expressed
    in parts per 100 (aka, percent)."""

    multipliers: dict[DamageTag, float] = field(
        default_factory=lambda: defaultdict(float)
    )

    def get_multiplier(self, tag: DamageTag) -> float:
        """Returns the multiplier for tag."""
        return self.multipliers[tag]

    def set_multiplier(self, tag: DamageTag, val: float) -> None:
        """Sets the multiplier for tag to val."""
        self.multipliers[tag] = val

    def add_to_multiplier(self, tag: DamageTag, val: float) -> None:
        """Adds val to the multiplier for tag."""
        self.multipliers[tag] += val

    def get_total_multiplier(self, tags: list[DamageTag] | set[DamageTag]) -> float:
        """Returns the combined multiplier of tags."""
        return sum(
            [self.multipliers[tag] for tag in tags] + [self.multipliers[DamageTag.ALL]]
        )

    def __add__(self, other):
        if not isinstance(other, DamageTagMultipliers):
            return NotImplemented

        ret: DamageTagMultipliers = DamageTagMultipliers()
        ret.multipliers = {
            tag: self.multipliers[tag] + other.multipliers[tag] for tag in DamageTag
        }

        return ret


@dataclass
class IncreasedDamageMultipliers(DamageTagMultipliers):
    """Contains multipliers for 'increased damage'."""

    ...


@dataclass
class IncreasedCriticalDamageMultipliers(DamageTagMultipliers):
    """Contains multipliers for 'increased critical damage'."""

    ...


@dataclass
class DefenseIgnoreMultipliers(DamageTagMultipliers):
    """Contains percentages for ignoring defense."""

    ...


class ModifierType(StrEnum):
    """Describes whether a modifier is additive (with the 'initial' stat)
    or multiplicative (with the initial stat plus additive modifiers)."""

    ADDITIVE = "Additive"
    MULTIPLICATIVE = "Multiplicative"


class StatType(StrEnum, boundary=STRICT):
    """Basic attributes."""

    ATTACK = "Attack"
    DEFENSE = "Defense"
    HEALTH = "Health"
    CRIT_RATE = "Critical Rate"
    CRIT_DAMAGE = "Critical Damage"
    STABILITY_DAMAGE_REDUCTION = "Stability Damage Reduction"


class SpecialAttribute(Enum):
    """Conditional attributes indexed by DamageTag."""

    DAMAGE_BOOST = "Increased Damage"
    CRITICAL_DAMAGE = "Critical Damage (Conditional)"
    DEFENSE_IGNORE = "Ignore Defense"
    INCREASE_DAMAGE_TAKEN = "Increased Damage Taken"


@dataclass
class StatSheet:
    """Contains all attributes."""

    basic_attributes: Dict[StatType, float] = field(default_factory=dict)
    special_attributes: Dict[SpecialAttribute, DamageTagMultipliers] = field(
        default_factory=dict
    )

    def __post_init__(self):
        self.basic_attributes = {stat: 0 for stat in StatType}
        for sp in SpecialAttribute:
            self.special_attributes[sp] = DamageTagMultipliers()
            self.special_attributes[sp].multipliers = {tag: 0 for tag in DamageTag}


@dataclass
class FinalStatModifiers(StatSheet):
    """Contains multiplicative modifiers to final stats (e.g., increase Attack by x%).
    A value of 0: no modifier. A value of x > 0: Increase by x%. A value of x < 0:
    Decrease by x%.
    """

    def __post_init__(self):
        self.basic_attributes = {stat: 0 for stat in StatType}
        for sp in SpecialAttribute:
            self.special_attributes[sp] = DamageTagMultipliers()
            self.special_attributes[sp].multipliers = {tag: 0 for tag in DamageTag}


@dataclass
class Unit:
    """A unit in combat, like a Doll or a target."""

    # 'Initial stats' shown in the refitting room / formation screen. Composed of basic doll stats,
    # weapon+attachments, remolding pattern (excluding imagoform and growth data, just innate stats
    # from the remolding pattern), affinity, common key, affinity key, fixed key, expansion key, ...
    initial_stats: StatSheet = field(default_factory=StatSheet)

    # Additive modifiers to initial stats. From in-combat buffs, remolding pattern imagoform and
    # growth data, food buff, ...
    additive_modifiers: StatSheet = field(default_factory=StatSheet)

    # Multiplicative modifiers. Total stat is (initial + additive modifiers)*multiplicative modifiers.
    multiplicative_modifiers: FinalStatModifiers = field(
        default_factory=FinalStatModifiers
    )

    def get_basic_attribute(self, stat: StatType) -> float:
        """Returns the final value of stat."""
        initial_value: float = self.initial_stats.basic_attributes[stat]
        additive_modifier: float = self.additive_modifiers.basic_attributes[stat]
        multiplicative_modifier: float = self.multiplicative_modifiers.basic_attributes[
            stat
        ]

        return (initial_value + additive_modifier) * (1 + multiplicative_modifier / 100)

    def get_special_attribute(
        self, special_attribute: SpecialAttribute, tag: DamageTag
    ) -> float:
        """Returns the final value of special_attribute[tag]."""
        initial_value: float = self.initial_stats.special_attributes[
            special_attribute
        ].get_multiplier(tag)
        additive_modifier: float = self.additive_modifiers.special_attributes[
            special_attribute
        ].get_multiplier(tag)
        multiplicative_modifier: float = (
            self.multiplicative_modifiers.special_attributes[
                special_attribute
            ].get_multiplier(tag)
        )

        return (initial_value + additive_modifier) * (1 + multiplicative_modifier / 100)

    def get_effective_special_attribute(
        self, special_attribute: SpecialAttribute
    ) -> DamageTagMultipliers:
        """Returns the combined value of special_attribute across all tags."""
        effective_multipliers: DamageTagMultipliers = DamageTagMultipliers()
        for tag in DamageTag:
            effective_multipliers.set_multiplier(
                tag, self.get_special_attribute(special_attribute, tag)
            )

        return effective_multipliers

    def get_effective_critical_damage_multiplier(self, tags: set[DamageTag]) -> float:
        """Returns the final critical damage multiplier for a damage instance with tags."""
        return self.get_basic_attribute(StatType.CRIT_DAMAGE) + (
            self.initial_stats.special_attributes[SpecialAttribute.CRITICAL_DAMAGE]
            + self.additive_modifiers.special_attributes[
                SpecialAttribute.CRITICAL_DAMAGE
            ]
        ).get_total_multiplier(tags)


class FortificationLevel(IntEnum, boundary=STRICT):
    """The Fortification Level (a.k.a., 'V') of a Doll."""

    SEGMENT00 = 0
    SEGMENT01 = 1
    SEGMENT02 = 2
    SEGMENT03 = 3
    SEGMENT04 = 4
    SEGMENT05 = 5
    SEGMENT06 = 6


@dataclass
class Doll(ABC, Unit):
    """A Doll."""

    name: ClassVar[str] = ""

    # The set of all DamageTag that are not applicable to Doll's abilities.
    irrelevant_damage_tags: ClassVar[set[DamageTag]] = set()

    @abstractmethod
    def set_fortification_level(self, level: FortificationLevel) -> None:
        """Update Doll to the input Fortification Level."""
        pass
