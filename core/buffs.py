from pydantic import BaseModel
from dataclasses import dataclass
from abc import ABC
from typing import Any, Dict
import inspect

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

    # Class attributes for config generation
    display_name: str = ""
    max_stack_count: int = 0  # 0 means no stacks, >0 means stacks with this max
    stack_input_type: str = "select"  # 'select' or 'number'


class Buff(BuffBase):
    """Represents a buff to a Doll."""

    ...


class Debuff(BuffBase):
    """Represents a debuff to a target."""

    ...


class RadiantRise(Buff):
    """Buff granted to Robella by her S2, Radiant Memory."""

    display_name = "Radiant Rise (Robella)"
    max_stack_count = 1
    stack_input_type = "select"

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

    display_name = "Light of Bond"
    max_stack_count = 4000
    stack_input_type = "number"

    def __init__(self, target_ally_initial_attack: float):
        """
        Arguments:
        target_ally_initial_attack -- the initial attack of the ally targeted by Light of Bond
        """
        self.value = 0.20 * target_ally_initial_attack
        self.modifier_type = ModifierType.ADDITIVE
        self.stat_type = StatType.ATTACK


class Unity(Buff):
    """Buff from Robella. Only applies when dealing Freeze damage."""

    display_name = "Unity"
    max_stack_count = 4000
    stack_input_type = "number"

    def __init__(self, robella_initial_attack: float):
        """
        Arguments:
        robella_initial_attack -- the initial attack of Robella
        """
        self.value = 0.10 * robella_initial_attack
        self.modifier_type = ModifierType.ADDITIVE
        self.stat_type = StatType.ATTACK


class UnityEnhanced(Buff):
    """Buff from Robella. Only applies when dealing Freeze damage."""

    display_name = "Unity: Enhanced"
    max_stack_count = 4000
    stack_input_type = "number"

    def __init__(self, robella_initial_attack: float):
        """
        Arguments:
        robella_initial_attack -- the initial attack of Robella
        """
        self.value = 0.15 * robella_initial_attack
        self.modifier_type = ModifierType.ADDITIVE
        self.stat_type = StatType.ATTACK


class SenseWeakness(Buff):
    """Robella self-buff."""

    display_name = "Sense Weakness (Robella)"
    max_stack_count = 10
    stack_input_type = "number"

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


class ColdConviction(Buff):
    """Makiatto buff granted by Cold Precision Shot."""

    display_name = "Cold Conviction (Makiatto)"
    max_stack_count = 3
    stack_input_type = "select"

    def __init__(self, stacks: int):
        """
        Arguments:
        stacks -- the number of stacks of this buff, up to 3
        """
        self.value = 10 * min(ColdConviction.max_stack_count, stacks)
        self.modifier_type = ModifierType.MULTIPLICATIVE
        self.stat_type = StatType.ATTACK


class Rapture(Buff):
    """Makiatto buff granted by Interception crits."""

    display_name = "Rapture (Makiatto)"
    max_stack_count = 4
    stack_input_type = "select"

    def __init__(self, stacks: int):
        """
        Arguments:
        stacks -- the number of stacks of this buff, up to 4
        """
        self.value = 7.5 * min(Rapture.max_stack_count, stacks)
        self.modifier_type = ModifierType.ADDITIVE
        self.stat_type = SpecialAttribute.DAMAGE_BOOST
        self.tag = DamageTag.ALL


class PredatorsPrinciple(Buff):
    """Buff granted to Voymastina when Confectance Index is full."""

    display_name = "Predator's Principle (Voymastina)"
    max_stack_count = 1
    stack_input_type = "select"

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

    display_name = "Venator (Voymastina)"
    max_stack_count = 1
    stack_input_type = "select"

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

    display_name = "Cooperative Hunt (Voymastina)"
    max_stack_count = 3
    stack_input_type = "select"

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


class SynchronizedPower(Buff):
    """Attack is increased by 15%."""

    display_name = "Synchronized Power (Lainie)"
    max_stack_count = 1
    stack_input_type = "select"

    def __init__(self):
        self.value = 15
        self.modifier_type = ModifierType.MULTIPLICATIVE
        self.stat_type = StatType.ATTACK


class NeverGiveUp(Buff):
    """Buff granted to Yoohee; applied to allied units when dealing Physical damage."""

    display_name = "Never Give Up (Yoohee)"
    max_stack_count = 4
    stack_input_type = "select"

    def __init__(self, stacks: int):
        """
        Arguments:
        stacks -- the number of stacks of this buff, up to 4
        """
        value: int = 15 * min(4, stacks)

        self.value = value
        self.modifier_type = ModifierType.ADDITIVE
        self.stat_type = SpecialAttribute.DEFENSE_IGNORE
        self.tag = DamageTag.PHYSICAL


class TroupesCore(Buff):
    """Buff granted to Yoohee."""

    display_name = "Troupe's Core (Yoohee)"
    max_stack_count = 1
    stack_input_type = "select"

    def __init__(self, yoohee_fortification_level: FortificationLevel):
        """
        Arguments:
        yoohee_fortification_level -- the Fortification Level of Yoohee granting this buff
        """
        if yoohee_fortification_level >= FortificationLevel.SEGMENT03:
            self.value = 50
        self.modifier_type = ModifierType.ADDITIVE
        self.stat_type = SpecialAttribute.DEFENSE_IGNORE
        self.tag = DamageTag.ALL


class GracefulSpin(Buff):
    """Buff granted by Yoohee. Mutually exclusive with Passionate Spin."""

    display_name = "Graceful Spin (Yoohee)"
    max_stack_count = 1
    stack_input_type = "select"

    def __init__(self):
        self.value = 10
        self.modifier_type = ModifierType.ADDITIVE
        self.stat_type = SpecialAttribute.CRITICAL_DAMAGE
        self.tag = DamageTag.ALL


class PassionateSpin(Buff):
    """Buff granted by Yoohee. Mutually exclusive with Graceful Spin."""

    display_name = "Passionate Spin (Yoohee)"
    max_stack_count = 1
    stack_input_type = "select"

    def __init__(self):
        self.value = 10
        self.modifier_type = ModifierType.ADDITIVE
        self.stat_type = SpecialAttribute.CRITICAL_DAMAGE
        self.tag = DamageTag.ALL


class PreshowWarmup(Buff):
    """Buff granted by Yoohee (V6)."""

    display_name = "Preshow Warmup (Yoohee)"
    max_stack_count = 1
    stack_input_type = "select"

    def __init__(self):
        self.value = 25
        self.modifier_type = ModifierType.ADDITIVE
        self.stat_type = SpecialAttribute.CRITICAL_DAMAGE
        self.tag = DamageTag.PHYSICAL


class UnshakableConfidence(Buff):
    """Buff granted to Mosin-Nagant after support actions."""

    display_name = "Unshakable Confidence (Mosin-Nagant)"
    max_stack_count = 4
    stack_input_type = "select"

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

    display_name = "Power Surge"
    max_stack_count = 3
    stack_input_type = "select"

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

    display_name = "Lightspike (Tololo)"
    max_stack_count = 8
    stack_input_type = "select"

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

    display_name = "Superconductive Code (Leva)"
    max_stack_count = 4
    stack_input_type = "select"

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

    display_name = "Superconductive Chain (Leva)"
    max_stack_count = 1
    stack_input_type = "select"

    def __init__(self):
        self.value = 10
        self.modifier_type = ModifierType.MULTIPLICATIVE
        self.stat_type = StatType.ATTACK


class PositiveCharge(Buff):
    """Electric buff."""

    display_name = "Positive Charge"
    max_stack_count = 1
    stack_input_type = "select"

    def __init__(self, target_has_negative_charge: bool):
        """
        Arguments:
        target_has_negative_charge -- True if the target of the attack has a negative charge
        """
        self.value = 35 if target_has_negative_charge else 0
        self.modifier_type = ModifierType.ADDITIVE
        self.stat_type = SpecialAttribute.DAMAGE_BOOST
        self.tag = DamageTag.ELECTRIC


class Clue(Buff):
    """Nikketa buff"""

    display_name = "Clue"
    max_stack_count = 10
    stack_input_type = "select"

    def __init__(self, stacks: int, nikketa_fortification_level: FortificationLevel):
        """
        Arguments:
        stacks -- the number of stacks
        alva_fortification_level -- the Fortification Level of the Alva applying this debuff
        """
        if nikketa_fortification_level >= FortificationLevel.SEGMENT03:
            max_stacks = 10
        else:
            max_stacks = 5

        self.value = 5 * min(max_stacks, stacks)
        self.modifier_type = ModifierType.ADDITIVE
        self.stat_type = SpecialAttribute.DAMAGE_BOOST
        self.tag = DamageTag.PASSIVE


class Justice(Buff):
    """Nikketa buff"""

    display_name = "Justice"
    max_stack_count = 5
    stack_input_type = "select"

    def __init__(self): ...

    def get_buffs(self, stacks: int):
        """
        Arguments:
        stacks -- the number of stacks
        """
        self.value = 30
        self.modifier_type = ModifierType.ADDITIVE
        self.stat_type = StatType.CRIT_RATE

        ret: list[Buff] = [
            self,
        ]

        ret.append(
            Buff(
                value=30,
                modifier_type=ModifierType.ADDITIVE,
                stat_type=SpecialAttribute.CRITICAL_DAMAGE,
                tag=DamageTag.ALL,
            ),
        )

        return ret


class AttackUpI(Buff):
    """Attack is increased by 10%. Considered a buff."""

    display_name = "Attack Up I"
    max_stack_count = 1
    stack_input_type = "select"

    def __init__(self):
        self.value = 10
        self.modifier_type = ModifierType.MULTIPLICATIVE
        self.stat_type = StatType.ATTACK


class AttackUpII(Buff):
    """Attack is increased by 15%. Considered a buff."""

    display_name = "Attack Up II"
    max_stack_count = 1
    stack_input_type = "select"

    def __init__(self):
        self.value = 15
        self.modifier_type = ModifierType.MULTIPLICATIVE
        self.stat_type = StatType.ATTACK


class CriticalRateBoostI(Buff):
    """Increases critical rate by 10%."""

    display_name = "Critical Rate Boost I"
    max_stack_count = 1
    stack_input_type = "select"

    def __init__(self):
        self.value = 10
        self.modifier_type = ModifierType.ADDITIVE
        self.stat_type = StatType.CRIT_RATE


class CriticalRateBoostII(Buff):
    """Increases critical rate by 20%."""

    display_name = "Critical Rate Boost II"
    max_stack_count = 1
    stack_input_type = "select"

    def __init__(self):
        self.value = 20
        self.modifier_type = ModifierType.ADDITIVE
        self.stat_type = StatType.CRIT_RATE


class DamageUpI(Buff):
    """Increases damage dealt by 10%."""

    display_name = "Damage Up I"
    max_stack_count = 1
    stack_input_type = "select"

    def __init__(self):
        self.value = 10
        self.modifier_type = ModifierType.ADDITIVE
        self.stat_type = SpecialAttribute.DAMAGE_BOOST
        self.tag = DamageTag.ALL


class DamageUpII(Buff):
    """Increases damage dealt by 20%."""

    display_name = "Damage Up II"
    max_stack_count = 1
    stack_input_type = "select"

    def __init__(self):
        self.value = 20
        self.modifier_type = ModifierType.ADDITIVE
        self.stat_type = SpecialAttribute.DAMAGE_BOOST
        self.tag = DamageTag.ALL


class TargetedAttackBoostI(Buff):
    """Targeted damage is increased by 10%."""

    display_name = "Targeted Attack BoostI"
    max_stack_count = 1
    stack_input_type = "select"

    def __init__(self):
        self.value = 10
        self.modifier_type = ModifierType.ADDITIVE
        self.stat_type = SpecialAttribute.DAMAGE_BOOST
        self.tag = DamageTag.TARGETED


class TargetedAttackBoostII(Buff):
    """Targeted damage is increased by 20%."""

    display_name = "Targeted Attack Boost II"
    max_stack_count = 1
    stack_input_type = "select"

    def __init__(self):
        self.value = 20
        self.modifier_type = ModifierType.ADDITIVE
        self.stat_type = SpecialAttribute.DAMAGE_BOOST
        self.tag = DamageTag.TARGETED


class PiercingI(Buff):
    """Targeted damage ignores 20% of the target's defense."""

    display_name = "Piercing I"
    max_stack_count = 1
    stack_input_type = "select"

    def __init__(self):
        self.value = 20
        self.modifier_type = ModifierType.ADDITIVE
        self.stat_type = SpecialAttribute.DEFENSE_IGNORE
        self.tag = DamageTag.TARGETED


class PiercingII(Buff):
    """Targeted damage ignores 30% of the target's defense."""

    display_name = "Piercing II"
    max_stack_count = 1
    stack_input_type = "select"

    def __init__(self):
        self.value = 30
        self.modifier_type = ModifierType.ADDITIVE
        self.stat_type = SpecialAttribute.DEFENSE_IGNORE
        self.tag = DamageTag.TARGETED


class PhaseBoostI(Buff):
    """Increased Phase damage dealt by 10%."""

    display_name = "Phase Boost I"
    max_stack_count = 1
    stack_input_type = "select"

    def __init__(self):
        self.value = 10
        self.modifier_type = ModifierType.ADDITIVE
        self.stat_type = SpecialAttribute.DAMAGE_BOOST
        self.tag = DamageTag.PHASE


class PhaseBoostII(Buff):
    """Increased Phase damage dealt by 20%."""

    display_name = "Phase Boost II"
    max_stack_count = 1
    stack_input_type = "select"

    def __init__(self):
        self.value = 20
        self.modifier_type = ModifierType.ADDITIVE
        self.stat_type = SpecialAttribute.DAMAGE_BOOST
        self.tag = DamageTag.PHASE


class Crumble(Debuff):
    """When attacked by Voymastina, this unit's defense is reduced by 40%. Considered a debuff."""

    display_name = "Crumble (Voymastina)"
    max_stack_count = 1
    stack_input_type = "select"

    def __init__(self):
        self.value = -40
        self.modifier_type = ModifierType.MULTIPLICATIVE
        self.stat_type = StatType.DEFENSE


class Rend(Debuff):
    """Physical damage taken is increased by 30%."""

    display_name = "Rend"
    max_stack_count = 1
    stack_input_type = "select"

    def __init__(self):
        self.value = 30
        self.modifier_type = ModifierType.ADDITIVE
        self.stat_type = SpecialAttribute.INCREASE_DAMAGE_TAKEN
        self.tag = DamageTag.PHYSICAL


class ParapluiesPenetration(Debuff):
    """Lainie debuff"""

    display_name = "Parapluie's Penetration (Lainie)"
    max_stack_count = 6
    stack_input_type = "select"

    def __init__(self, stacks: int, lainie_fortification_level: FortificationLevel):
        """
        Arguments:
        stacks -- the number of stacks of this buff
        lainie_fortification_level -- the Fortification Level of the Lainie applying this debuff
        """
        # Expansion Key: Superimposed Algorithm - Additional 6%
        reduction_per_stack: int = -(15 + 6)
        max_stacks: int = 3

        if lainie_fortification_level >= FortificationLevel.SEGMENT01:
            max_stacks = 6

        self.value = reduction_per_stack * min(max_stacks, stacks)

        self.modifier_type = ModifierType.MULTIPLICATIVE
        self.stat_type = StatType.DEFENSE


class PrecognitionForesight(Debuff):
    """Lainie debuff"""

    display_name = "Precognition Foresight (Lainie)"
    max_stack_count = 6
    stack_input_type = "select"

    def __init__(self, lainie_fortification_level: FortificationLevel):
        """
        Arguments:
        lainie_fortification_level -- the Fortification Level of the Lainie applying this debuff
        """
        if lainie_fortification_level >= FortificationLevel.SEGMENT03:
            self.value = -20
        else:
            self.value = -10

        self.modifier_type = ModifierType.MULTIPLICATIVE
        self.stat_type = StatType.DEFENSE
        self.tag = DamageTag.PHYSICAL


class PrecognitionAwareness(Debuff):
    """Lainie's Simulacrum debuff"""

    display_name = "Precognition Awareness (Simulacrum)"
    max_stack_count = 6
    stack_input_type = "select"

    def __init__(self, lainie_fortification_level: FortificationLevel):
        """
        Arguments:
        lainie_fortification_level -- the Fortification Level of the Lainie applying this debuff
        """
        if lainie_fortification_level >= FortificationLevel.SEGMENT03:
            self.value = -20
        else:
            self.value = -10

        self.modifier_type = ModifierType.MULTIPLICATIVE
        self.stat_type = StatType.DEFENSE
        self.tag = DamageTag.PHYSICAL


class SugarOverdose(Debuff):
    """Damage taken from Makiatto is increased by 15%."""

    display_name = "Sugar Overdose (Makiatto)"
    max_stack_count = 1
    stack_input_type = "select"

    def __init__(self):
        self.value = 15
        self.modifier_type = ModifierType.ADDITIVE
        self.stat_type = SpecialAttribute.INCREASE_DAMAGE_TAKEN
        self.tag = DamageTag.ALL


class MurderousIntent(Debuff):
    """Increase incoming Freeze damage from Makiatto."""

    display_name = "Murderous Intent (Makiatto)"
    max_stack_count = 1
    stack_input_type = "select"

    def __init__(self, phase_weakness_exploited: bool):
        if phase_weakness_exploited:
            self.value = 30
        else:
            self.value = 20
        self.modifier_type = ModifierType.ADDITIVE
        self.stat_type = SpecialAttribute.INCREASE_DAMAGE_TAKEN
        self.tag = DamageTag.FREEZE


class ElectricSparks(Debuff):
    """Electric damage taken from Mosin-Nagant is increased by 15%."""

    display_name = "Electric Sparks"
    max_stack_count = 1
    stack_input_type = "select"

    def __init__(self):
        self.value = 15
        self.modifier_type = ModifierType.ADDITIVE
        self.stat_type = SpecialAttribute.INCREASE_DAMAGE_TAKEN
        self.tag = DamageTag.ELECTRIC


class VoltageSag(Debuff):
    """Jiangyu debuff"""

    display_name = "Voltage Sag"
    max_stack_count = 6
    stack_input_type = "select"

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

    display_name = "Hypothermia"
    max_stack_count = 1
    stack_input_type = "select"

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


class Frostbite(Debuff):
    """Freeze damage taken is increased by 20%. Removed after gaining Hoarfrost."""

    display_name = "Frostbite"
    max_stack_count = 1
    stack_input_type = "select"

    def __init__(self):
        self.value = 20

        self.modifier_type = ModifierType.ADDITIVE
        self.stat_type = SpecialAttribute.INCREASE_DAMAGE_TAKEN
        self.tag = DamageTag.FREEZE


class Guilt(Debuff):
    """Nikketa debuff"""

    display_name = "Guilt"
    max_stack_count = 1
    stack_input_type = "select"

    def __init__(self, nikketa_fortification_level: FortificationLevel):
        """
        Arguments:
        nikketa_fortification_level -- the Fortification Level of the Nikketa applying this debuff
        """
        if nikketa_fortification_level >= FortificationLevel.SEGMENT04:
            self.value = 10
        else:
            self.value = 5

        self.modifier_type = ModifierType.ADDITIVE
        self.stat_type = SpecialAttribute.INCREASE_DAMAGE_TAKEN
        self.tag = DamageTag.HYDRO


class VulnerableI(Debuff):
    """Increase damage taken by 10%."""

    display_name = "Vulnerable I"
    max_stack_count = 1
    stack_input_type = "select"

    def __init__(self):
        self.value = 10
        self.modifier_type = ModifierType.ADDITIVE
        self.stat_type = SpecialAttribute.INCREASE_DAMAGE_TAKEN
        self.tag = DamageTag.ALL


class VulnerableII(Debuff):
    """Increase damage taken by 20%."""

    display_name = "Vulnerable II"
    max_stack_count = 1
    stack_input_type = "select"

    def __init__(self):
        self.value = 20
        self.modifier_type = ModifierType.ADDITIVE
        self.stat_type = SpecialAttribute.INCREASE_DAMAGE_TAKEN
        self.tag = DamageTag.ALL


class DefenseDownI(Debuff):
    """Reduce defense by 20%. Considered a defense buff."""

    display_name = "Defense Down I"
    max_stack_count = 1
    stack_input_type = "select"

    def __init__(self):
        self.value = -20
        self.modifier_type = ModifierType.MULTIPLICATIVE
        self.stat_type = StatType.DEFENSE


class DefenseDownII(Debuff):
    """Reduce defense by 30%. Considered a defense buff."""

    display_name = "Defense Down II"
    max_stack_count = 1
    stack_input_type = "select"

    def __init__(self):
        self.value = -30
        self.modifier_type = ModifierType.MULTIPLICATIVE
        self.stat_type = StatType.DEFENSE


def _generate_field(param_name, annotation, default, cls):
    label = param_name.replace("_", " ").title()
    if annotation == FortificationLevel:
        return {
            "key": param_name,
            "type": "select",
            "label": label,
            "options": [n for n in FortificationLevel],
            "default": FortificationLevel.SEGMENT06,
        }
    elif annotation == bool:
        return {
            "key": param_name,
            "type": "checkbox",
            "label": label,
            "default": True,
        }
    elif annotation in (int, float):
        if "stack" in param_name.lower():
            input_type = getattr(cls, "stack_input_type", "select")
            max_count = getattr(cls, "max_stack_count", 10)
            if input_type == "number":
                return {
                    "key": param_name,
                    "type": "number",
                    "label": label,
                    "default": max_count,
                }
            return {
                "key": param_name,
                "type": "select",
                "label": label,
                "options": [n for n in range(0, max_count + 1)],
                "default": max_count,
            }
        return {
            "key": param_name,
            "type": "number",
            "label": label,
            "default": 0,
        }
    return {
        "key": param_name,
        "type": "text",
        "label": label,
        "default": "",
    }


def _get_display_name(cls):
    if hasattr(cls, "display_name") and cls.display_name:
        return cls.display_name
    return cls.__name__


def _get_option_config(subclass_base, custom_entries):
    """Generic config builder for Buff/Debuff subclasses."""
    classes = [
        cls
        for name, cls in globals().items()
        if isinstance(cls, type)
        and issubclass(cls, subclass_base)
        and cls not in {subclass_base, BuffBase}
    ]

    config: Dict[str, Dict[str, Any]] = {}

    for cls in classes:
        display_name = _get_display_name(cls)

        if hasattr(cls, "get_buffs"):
            sig = inspect.signature(cls.get_buffs)
            params = [p for p in sig.parameters.values() if p.name != "self"]
            fields = [
                _generate_field(p.name, p.annotation, p.default, cls) for p in params
            ]
            function = cls().get_buffs
        else:
            sig = inspect.signature(cls.__init__)
            params = [p for p in sig.parameters.values() if p.name != "self"]
            fields = [
                _generate_field(p.name, p.annotation, p.default, cls) for p in params
            ]
            function = cls

        config[display_name] = {
            "fields": fields,
            "function": function,
        }

    config.update(custom_entries())
    return config


def get_buffs_option_config() -> Dict[str, Dict[str, Any]]:
    """Generate Buff options config."""

    def custom_buffs():
        return {
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
            }
        }

    return _get_option_config(Buff, custom_buffs)


def get_debuffs_option_config() -> Dict[str, Dict[str, Any]]:
    """Generate Debuff options config."""

    def custom_debuffs():
        return {
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
            }
        }

    return _get_option_config(Debuff, custom_debuffs)


# Generate the config at module level
buffs_option_config = get_buffs_option_config()
debuffs_option_config = get_debuffs_option_config()
