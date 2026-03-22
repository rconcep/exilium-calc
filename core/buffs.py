from dataclasses import dataclass
from abc import ABC
from typing import Any, Dict

from core.types import (
    StatType,
    SpecialAttribute,
    DamageTag,
    ModifierType,
    FortificationLevel,
)


@dataclass
class BuffBase(ABC):
    """Base class for Buffs/Debuffs."""

    # Value of the buff or debuff. Note that debuffs are likely to have negative values to represent
    # reductions of an attribute.
    value: float

    # Whether the buff/debuff is additive or multiplicative.
    modifier_type: ModifierType

    # Select exactly one of the following stat categories to have a value. The rest should be None.
    # e.g., If specifying "Attack (% increase)", set statType to StatType.ATTACK_BOOST and
    # the others to None. If specifying increased damage for freeze type damage, set statType
    # to SpecialAttribute.DAMAGE_BOOST and tag to DamageTag.FREEZE.
    stat_type: StatType | SpecialAttribute
    tag: DamageTag = DamageTag.ALL


@dataclass
class Buff(BuffBase):
    """Represents a buff to a Doll."""

    ...


@dataclass
class Debuff(BuffBase):
    """Represents a debuff to a target."""

    ...


class RadiantRise(Buff):
    """Buff granted to Robella by her S2, Radiant Memory."""

    def __init__(self, fortification_level: FortificationLevel):
        """
        Arguments:
        fortification_level -- the Fortification Level of Robella
        """
        self.value = 50 if fortification_level >= FortificationLevel.SEGMENT02 else 30
        self.modifier_type = ModifierType.ADDITIVE
        self.stat_type = SpecialAttribute.DAMAGE_BOOST
        self.tag = DamageTag.ALL


class LightOfBond(Buff):
    """V1 effect of Light of Bond (Unity) (Robella)."""

    def __init__(self, target_ally_initial_attack: float):
        """
        Arguments:
        target_ally_initial_attack -- the initial attack of the ally targeted by Light of Bond
        """
        self.value = 0.20 * target_ally_initial_attack
        self.modifier_type = ModifierType.ADDITIVE
        self.stat_type = StatType.ATTACK


class SenseWeakness(Buff):
    """Robella self-buff."""

    def __init__(self): ...

    def get_buffs(self, stacks: int):
        """
        Arguments:
        stacks -- the number of stacks of this effect
        """
        ret: list[Buff] = []

        if stacks > 2:
            ret.append(Buff(20, ModifierType.ADDITIVE, StatType.CRIT_RATE))

        if stacks > 5:
            ret.append(Buff(30, ModifierType.ADDITIVE, StatType.CRIT_DAMAGE))

        return ret


class PredatorsPrinciple(Buff):
    """Buff granted to Voymastina when Confectance Index is full."""

    def __init__(self): ...

    def get_buffs(self):
        self.value = 50
        self.modifier_type = ModifierType.ADDITIVE
        self.stat_type = SpecialAttribute.DEFENSE_IGNORE
        self.tag = DamageTag.ACTIVE

        ret: list[Buff] = []
        ret.append(self)
        ret.append(Buff(30, ModifierType.ADDITIVE, StatType.CRIT_RATE))
        ret.append(Buff(25, ModifierType.ADDITIVE, StatType.CRIT_DAMAGE))

        return ret


class Venator(Buff):
    """Buff granted to Voymastina (V6) at the start of battle."""

    def __init__(self): ...

    def get_buffs(self):
        self.value = 45
        self.modifier_type = ModifierType.ADDITIVE
        self.stat_type = SpecialAttribute.DAMAGE_BOOST
        self.tag = DamageTag.ALL

        ret: list[Buff] = []
        ret.append(self)
        ret.append(Buff(30, ModifierType.ADDITIVE, StatType.CRIT_DAMAGE))

        return ret


class CooperativeHunt(Buff):
    """Buff granted to Voymastina (V4) when performing a support action."""

    def __init__(self): ...

    def get_buffs(self, stacks: int):
        """
        Arguments:
        stacks -- the number of stacks of this buff, up to 3
        """
        value: int = 10 * min(3, stacks)

        self.value = value
        self.modifier_type = ModifierType.ADDITIVE
        self.stat_type = SpecialAttribute.DAMAGE_BOOST
        self.tag = DamageTag.ALL

        ret: list[Buff] = [
            self,
        ]
        ret.append(Buff(value, ModifierType.ADDITIVE, StatType.CRIT_RATE))

        return ret


class UnshakableConfidence(Buff):
    """Buff granted to Mosin-Nagant after support actions."""

    def __init__(self): ...

    def get_buffs(self, stacks: int):
        """
        Arguments:
        stacks -- the number of stacks of this buff, up to 4
        """
        self.value = 5 * min(4, stacks)
        self.modifier_type = ModifierType.ADDITIVE
        self.stat_type = SpecialAttribute.CRITICAL_DAMAGE
        self.tag = DamageTag.ULTIMATE

        ret: list[Buff] = []
        ret.append(self)
        ret.append(Buff(5 * min(4, stacks), ModifierType.ADDITIVE, StatType.CRIT_RATE))

        return ret


class PowerSurge(Buff):
    """Jiangyu buff."""

    def __init__(self, stacks: int, jiangyu_fortification_level: FortificationLevel):
        """
        Arguments:
        stacks -- the number of stacks of this buff, up to 3
        jiangyu_fortification_level -- the Fortification Level of the Jiangyu granting this buff
        """
        self.value = 5 * min(3, stacks)
        self.modifier_type = ModifierType.ADDITIVE
        self.stat_type = SpecialAttribute.DEFENSE_IGNORE
        self.tag = DamageTag.ELECTRIC

        if jiangyu_fortification_level == FortificationLevel.SEGMENT06:
            self.value = 2 * self.value


class Lightspike(Buff):
    """Tololo buff."""

    def __init__(self): ...

    def get_buffs(
        self, stacks: int, tololo_fortification_level: FortificationLevel
    ) -> list[Buff]:
        """
        Arguments:
        stacks -- the number of stacks of this buff, up to 8
        tololo_fortification_level -- the Fortification Level of Tololo
        """
        if tololo_fortification_level >= FortificationLevel.SEGMENT05:
            value_per_stack: int = 5
        else:
            value_per_stack: int = 3

        self.value = value_per_stack * min(8, stacks)
        self.modifier_type = ModifierType.ADDITIVE
        self.stat_type = StatType.CRIT_RATE

        ret: list[Buff] = [
            self,
        ]

        ret.append(
            Buff(
                self.value,
                modifier_type=ModifierType.ADDITIVE,
                stat_type=StatType.CRIT_DAMAGE,
            )
        )

        return ret


class SuperconductiveCode(Buff):
    """Leva buff."""

    def __init__(self): ...

    def get_buffs(self, stacks: int) -> list[Buff]:
        """
        Arguments:
        stacks -- the number of stacks of this buff, up to 4
        """

        self.value = 5 * min(4, stacks)
        self.modifier_type = ModifierType.ADDITIVE
        self.stat_type = StatType.CRIT_RATE

        ret: list[Buff] = [
            self,
        ]

        ret.append(
            Buff(
                7.5 * min(4, stacks),
                modifier_type=ModifierType.ADDITIVE,
                stat_type=StatType.CRIT_DAMAGE,
            )
        )

        return ret


class SuperconductiveChain(Buff):
    """Buff granted to Leva at 4 stacks of Superconductive Code."""

    def __init__(self):
        self.value = 10
        self.modifier_type = ModifierType.MULTIPLICATIVE
        self.stat_type = StatType.ATTACK


class PositiveCharge(Buff):
    """Electric buff."""

    def __init__(self, target_has_negative_charge: bool):
        """
        Arguments:
        target_has_negative_charge -- True if the target of the attack has a negative charge
        """
        self.value = 35 if target_has_negative_charge else 0
        self.modifier_type = ModifierType.ADDITIVE
        self.stat_type = SpecialAttribute.DAMAGE_BOOST
        self.tag = DamageTag.ELECTRIC


class AttackUpI(Buff):
    """Attack is increased by 10%. Considered a buff."""

    def __init__(self):
        self.value = 10
        self.modifier_type = ModifierType.MULTIPLICATIVE
        self.stat_type = StatType.ATTACK


class AttackUpII(Buff):
    """Attack is increased by 15%. Considered a buff."""

    def __init__(self):
        self.value = 15
        self.modifier_type = ModifierType.MULTIPLICATIVE
        self.stat_type = StatType.ATTACK


class CriticalRateBoostI(Buff):
    """Increases critical rate by 10%."""

    def __init__(self):
        self.value = 10
        self.modifier_type = ModifierType.ADDITIVE
        self.stat_type = StatType.CRIT_RATE


class CriticalRateBoostII(Buff):
    """Increases critical rate by 20%."""

    def __init__(self):
        self.value = 20
        self.modifier_type = ModifierType.ADDITIVE
        self.stat_type = StatType.CRIT_RATE


class DamageUpI(Buff):
    """Increases damage dealt by 10%."""

    def __init__(self):
        self.value = 10
        self.modifier_type = ModifierType.ADDITIVE
        self.stat_type = SpecialAttribute.DAMAGE_BOOST
        self.tag = DamageTag.ALL


class DamageUpII(Buff):
    """Increases damage dealt by 20%."""

    def __init__(self):
        self.value = 20
        self.modifier_type = ModifierType.ADDITIVE
        self.stat_type = SpecialAttribute.DAMAGE_BOOST
        self.tag = DamageTag.ALL


class TargetedAttackBoostI(Buff):
    """Targeted damage is increased by 10%."""

    def __init__(self):
        self.value = 10
        self.modifier_type = ModifierType.ADDITIVE
        self.stat_type = SpecialAttribute.DAMAGE_BOOST
        self.tag = DamageTag.TARGETED


class TargetedAttackBoostII(Buff):
    """Targeted damage is increased by 20%."""

    def __init__(self):
        self.value = 20
        self.modifier_type = ModifierType.ADDITIVE
        self.stat_type = SpecialAttribute.DAMAGE_BOOST
        self.tag = DamageTag.TARGETED


class PiercingI(Buff):
    """Targeted damage ignores 20% of the target's defense."""

    def __init__(self):
        self.value = 20
        self.modifier_type = ModifierType.ADDITIVE
        self.stat_type = SpecialAttribute.DEFENSE_IGNORE
        self.tag = DamageTag.TARGETED


class PiercingII(Buff):
    """Targeted damage ignores 30% of the target's defense."""

    def __init__(self):
        self.value = 30
        self.modifier_type = ModifierType.ADDITIVE
        self.stat_type = SpecialAttribute.DEFENSE_IGNORE
        self.tag = DamageTag.TARGETED


class PhaseBoostI(Buff):
    """Increased Phase damage dealt by 10%."""

    def __init__(self):
        self.value = 10
        self.modifier_type = ModifierType.ADDITIVE
        self.stat_type = SpecialAttribute.DAMAGE_BOOST
        self.tag = DamageTag.PHASE


class PhaseBoostII(Buff):
    """Increased Phase damage dealt by 20%."""

    def __init__(self):
        self.value = 20
        self.modifier_type = ModifierType.ADDITIVE
        self.stat_type = SpecialAttribute.DAMAGE_BOOST
        self.tag = DamageTag.PHASE


class Crumble(Debuff):
    """When attacked by Voymastina, this unit's defense is reduced by 40%. Considered a debuff."""

    def __init__(self):
        self.value = -40
        self.modifier_type = ModifierType.MULTIPLICATIVE
        self.stat_type = StatType.DEFENSE


class Rend(Debuff):
    """Physical damage taken is increased by 30%."""

    def __init__(self):
        self.value = 30
        self.modifier_type = ModifierType.ADDITIVE
        self.stat_type = SpecialAttribute.INCREASE_DAMAGE_TAKEN
        self.tag = DamageTag.PHYSICAL


class ElectricSparks(Debuff):
    """Electric damage taken from Mosin-Nagant is increased by 15%."""

    def __init__(self):
        self.value = 15
        self.modifier_type = ModifierType.ADDITIVE
        self.stat_type = SpecialAttribute.INCREASE_DAMAGE_TAKEN
        self.tag = DamageTag.ELECTRIC


class VoltageSag(Debuff):
    """Jiangyu debuff"""

    def __init__(self, stacks: int, jiangyu_fortification_level: FortificationLevel):
        """
        Arguments:
        stacks -- the number of stacks of this buff
        jiangyu_fortification_level -- the Fortification Level of the Jiangyu applying this debuff
        """
        if jiangyu_fortification_level == FortificationLevel.SEGMENT06:
            self.value = 6 * min(6, stacks)
        else:
            self.value = 6 * min(3, stacks)

        self.modifier_type = ModifierType.ADDITIVE
        self.stat_type = SpecialAttribute.INCREASE_DAMAGE_TAKEN
        self.tag = DamageTag.ELECTRIC


class Hypothermia(Debuff):
    """Alva debuff"""

    def __init__(self, alva_fortification_level: FortificationLevel):
        """
        Arguments:
        alva_fortification_level -- the Fortification Level of the Alva applying this debuff
        """
        if alva_fortification_level >= FortificationLevel.SEGMENT05:
            self.value = 40
        else:
            self.value = 20

        self.modifier_type = ModifierType.ADDITIVE
        self.stat_type = SpecialAttribute.INCREASE_DAMAGE_TAKEN
        self.tag = DamageTag.FREEZE


class VulnerableI(Debuff):
    """Increase damage taken by 10%."""

    def __init__(self):
        self.value = 10
        self.modifier_type = ModifierType.ADDITIVE
        self.stat_type = SpecialAttribute.INCREASE_DAMAGE_TAKEN
        self.tag = DamageTag.ALL


class VulnerableII(Debuff):
    """Increase damage taken by 20%."""

    def __init__(self):
        self.value = 20
        self.modifier_type = ModifierType.ADDITIVE
        self.stat_type = SpecialAttribute.INCREASE_DAMAGE_TAKEN
        self.tag = DamageTag.ALL


class DefenseDownI(Debuff):
    """Reduce defense by 20%. Considered a defense buff."""

    def __init__(self):
        self.value = -20
        self.modifier_type = ModifierType.MULTIPLICATIVE
        self.stat_type = StatType.DEFENSE


class DefenseDownII(Debuff):
    """Reduce defense by 30%. Considered a defense buff."""

    def __init__(self):
        self.value = -30
        self.modifier_type = ModifierType.MULTIPLICATIVE
        self.stat_type = StatType.DEFENSE


buffs_option_config: Dict[str, Dict[str, Any]] = {
    "Radiant Rise (Robella)": {
        "fields": [
            {
                "key": "fortification_level",
                "type": "select",
                "label": "Robella Fortification Level",
                "options": [n for n in FortificationLevel],
                "default": FortificationLevel.SEGMENT06,
            },
        ],
        "function": RadiantRise,
    },
    "Light of Bond": {
        "fields": [
            {
                "key": "target_ally_initial_attack",
                "type": "number",
                "label": "Target Ally's Initial Attack",
                "default": 3800,
            },
        ],
        "function": LightOfBond,
    },
    "Sense Weakness (Robella)": {
        "fields": [
            {"key": "stacks", "type": "number", "label": "Stacks", "default": 10},
        ],
        "function": SenseWeakness().get_buffs,
    },
    "Predator's Principle (Voymastina)": {
        "fields": [],
        "function": PredatorsPrinciple().get_buffs,
    },
    "Venator (Voymastina)": {"fields": [], "function": Venator().get_buffs},
    "Cooperative Hunt (Voymastina)": {
        "fields": [
            {
                "key": "stacks",
                "type": "select",
                "label": "Stacks",
                "options": [n for n in range(0, 4)],
                "default": 3,
            },
        ],
        "function": CooperativeHunt().get_buffs,
    },
    "Unshakable Confidence (Mosin-Nagant)": {
        "fields": [
            {
                "key": "stacks",
                "type": "select",
                "label": "Stacks",
                "options": [n for n in range(0, 5)],
                "default": 4,
            },
        ],
        "function": UnshakableConfidence().get_buffs,
    },
    "Power Surge": {
        "fields": [
            {
                "key": "stacks",
                "type": "select",
                "label": "Stacks",
                "options": [n for n in range(0, 4)],
                "default": 3,
            },
            {
                "key": "jiangyu_fortification_level",
                "type": "select",
                "label": "Jiangyu Fortification Level",
                "options": [n for n in FortificationLevel],
                "default": FortificationLevel.SEGMENT06,
            },
        ],
        "function": PowerSurge,
    },
    "Lightspike (Tololo)": {
        "fields": [
            {
                "key": "stacks",
                "type": "select",
                "label": "Stacks",
                "options": [n for n in range(0, 9)],
                "default": 8,
            },
            {
                "key": "tololo_fortification_level",
                "type": "select",
                "label": "Tololo Fortification Level",
                "options": [n for n in FortificationLevel],
                "default": FortificationLevel.SEGMENT06,
            },
        ],
        "function": Lightspike().get_buffs,
    },
    "Superconductive Code (Leva)": {
        "fields": [
            {
                "key": "stacks",
                "type": "select",
                "label": "Stacks",
                "options": [n for n in range(0, 5)],
                "default": 4,
            },
        ],
        "function": SuperconductiveCode().get_buffs,
    },
    "Superconductive Chain (Leva)": {"fields": [], "function": SuperconductiveChain},
    "Positive Charge": {
        "fields": [
            {
                "key": "target_has_negative_charge",
                "type": "checkbox",
                "label": "Target Has Negative Charge",
                "default": True,
            },
        ],
        "function": PositiveCharge,
    },
    "Attack Up I": {"fields": [], "function": AttackUpI},
    "Attack Up II": {"fields": [], "function": AttackUpII},
    "Critical Rate Boost I": {"fields": [], "function": CriticalRateBoostI},
    "Critical Rate Boost II": {"fields": [], "function": CriticalRateBoostII},
    "Damage Up I": {"fields": [], "function": DamageUpI},
    "Damage Up II": {"fields": [], "function": DamageUpII},
    "Targeted Attack Boost I": {"fields": [], "function": TargetedAttackBoostI},
    "Targeted Attack Boost II": {"fields": [], "function": TargetedAttackBoostII},
    "Piercing I": {"fields": [], "function": PiercingI},
    "Piercing II": {"fields": [], "function": PiercingII},
    "Phase Boost I": {"fields": [], "function": PhaseBoostI},
    "Phase Boost II": {"fields": [], "function": PhaseBoostII},
    # Custom buff
    "Custom Buff": {
        "fields": [
            {"key": "value", "type": "number", "label": "Value", "default": 0},
            {
                "key": "modifier_type",
                "type": "select",
                "label": "Modifier Type",
                "options": [ModifierType.ADDITIVE, ModifierType.MULTIPLICATIVE],
                "default": ModifierType.MULTIPLICATIVE,
            },
            {
                "key": "stat_type",
                "type": "select",
                "label": "Stat",
                "options": [stat for stat in StatType]
                + [stat for stat in SpecialAttribute],
                "default": StatType.ATTACK,
            },
            {
                "key": "tag",
                "type": "select",
                "label": "Damage Tag",
                "options": [tag for tag in DamageTag],
                "default": DamageTag.ALL,
            },
        ],
        "function": Buff,
    },
}

debuffs_option_config: Dict[str, Dict[str, Any]] = {
    "Crumble": {"fields": [], "function": Crumble},
    "Rend": {"fields": [], "function": Rend},
    "Electric Sparks": {"fields": [], "function": ElectricSparks},
    "Voltage Sag": {
        "fields": [
            {
                "key": "stacks",
                "type": "select",
                "label": "Stacks",
                "options": [n for n in range(0, 7)],
                "default": 6,
            },
            {
                "key": "jiangyu_fortification_level",
                "type": "select",
                "label": "Jiangyu Fortification Level",
                "options": [n for n in FortificationLevel],
                "default": FortificationLevel.SEGMENT06,
            },
        ],
        "function": VoltageSag,
    },
    "Hypothermia": {
        "fields": [
            {
                "key": "alva_fortification_level",
                "type": "select",
                "label": "Alva Fortification Level",
                "options": [n for n in FortificationLevel],
                "default": FortificationLevel.SEGMENT05,
            },
        ],
        "function": Hypothermia,
    },
    "Defense Down I": {"fields": [], "function": DefenseDownI},
    "Defense Down II": {"fields": [], "function": DefenseDownII},
    "Vulnerable I": {"fields": [], "function": VulnerableI},
    "Vulnerable II": {"fields": [], "function": VulnerableII},
    "Custom Debuff": {
        "fields": [
            {"key": "value", "type": "number", "label": "Value", "default": 0},
            {
                "key": "modifier_type",
                "type": "select",
                "label": "Modifier Type",
                "options": [ModifierType.ADDITIVE, ModifierType.MULTIPLICATIVE],
                "default": ModifierType.MULTIPLICATIVE,
            },
            {
                "key": "stat_type",
                "type": "select",
                "label": "Stat",
                "options": [stat for stat in StatType]
                + [stat for stat in SpecialAttribute],
                "default": StatType.ATTACK,
            },
            {
                "key": "tag",
                "type": "select",
                "label": "Damage Tag",
                "options": [tag for tag in DamageTag],
                "default": DamageTag.ALL,
            },
        ],
        "function": Debuff,
    },
}
