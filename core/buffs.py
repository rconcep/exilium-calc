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


class BlazingAssaultII(Buff):
    """Attack is increased by 15%. Considered a buff."""

    display_name = "Blazing Assault II"
    max_stack_count = 1
    stack_input_type = "select"

    def __init__(self):
        self.value = 15
        self.modifier_type = ModifierType.MULTIPLICATIVE
        self.stat_type = StatType.ATTACK


class GoodLuck(Buff):
    """Buff granted to Sakura."""

    display_name = "Good Luck (Sakura)"
    max_stack_count = 1
    stack_input_type = "select"

    def __init__(self): ...

    def get_buffs(self, sakura_fortification_level: FortificationLevel):
        """
        Arguments:
        sakura_fortification_level -- the Fortification Level of the Sakura granting this buff
        """
        ret: list[Buff] = []

        if sakura_fortification_level < FortificationLevel.SEGMENT03:
            # V0-V2: If Sakura has Good Luck, damage dealt is increased by 20%.
            self.value = 20
        else:
            # V3: If Sakura has Good Luck, damage dealt is increased by 50%.
            self.value = 50
            self.modifier_type = ModifierType.ADDITIVE
            self.stat_type = SpecialAttribute.DAMAGE_BOOST
            self.tag = DamageTag.ALL

        ret.append(self)

        if sakura_fortification_level >= FortificationLevel.SEGMENT03:
            # V3: If Sakura has Good Luck, critical damage is increased by 25%.
            ret.append(
                Buff(
                    value=25,
                    modifier_type=ModifierType.ADDITIVE,
                    stat_type=SpecialAttribute.CRITICAL_DAMAGE,
                    tag=DamageTag.ALL,
                )
            )

        return ret


class Accelerant(Buff):
    """Buff granted by Vector's Ultimate."""

    display_name = "Accelerant (Vector)"
    max_stack_count = 7
    stack_input_type = "number"

    def __init__(self): ...

    def get_buffs(
        self, vector_fortification_level: FortificationLevel, number_of_burn_buffs: int
    ):
        """
        Arguments:
        vector_fortification_level -- the Fortification Level of the Vector granting this buff
        """
        ret: list[Buff] = []

        # Damage dealt when dealing Burn damage
        if vector_fortification_level >= FortificationLevel.SEGMENT02:
            self.value = 30
        else:
            self.value = 10

        self.modifier_type = ModifierType.ADDITIVE
        self.stat_type = SpecialAttribute.DAMAGE_BOOST
        self.tag = DamageTag.BURN

        ret.append(self)

        # V6: Every Burn buff increases damage dealt by 5%
        if (
            vector_fortification_level >= FortificationLevel.SEGMENT06
            and number_of_burn_buffs > 0
        ):
            ret.append(
                Buff(
                    value=5 * max(0, number_of_burn_buffs),
                    modifier_type=ModifierType.ADDITIVE,
                    stat_type=SpecialAttribute.DAMAGE_BOOST,
                    tag=DamageTag.ALL,
                )
            )

            # Critical damage is increased by 15%
            ret.append(
                Buff(
                    value=15,
                    modifier_type=ModifierType.ADDITIVE,
                    stat_type=SpecialAttribute.CRITICAL_DAMAGE,
                    tag=DamageTag.ALL,
                )
            )

        return ret


class ApatheticResistance(Buff):
    """Buff granted to Vector by her Ultimate (V6)."""

    display_name = "Apathetic Resistance (Vector)"
    max_stack_count = 1
    stack_input_type = "select"

    def __init__(self, vector_fortification_level: FortificationLevel):
        if vector_fortification_level >= FortificationLevel.SEGMENT06:
            self.value = 25
        else:
            self.value = 0

        self.modifier_type = ModifierType.ADDITIVE
        self.stat_type = SpecialAttribute.CRITICAL_DAMAGE
        self.tag = DamageTag.ALL


class Embers(Buff):
    """Buff granted by fully charging Thermal Conduction."""

    display_name = "Embers"
    max_stack_count = 6  # Theoretically infinite, but no battle lasts long enough.
    stack_input_type = "select"

    def __init__(self): ...

    def get_buffs(self, stack: int):
        """
        Arguments:
        stack -- the number of stacks of this buff, up to 6
        """
        ret: list[Buff] = []

        # Burn damage dealt is increased by 30%. (For two turns while active.)
        self.value = 30
        self.modifier_type = ModifierType.ADDITIVE
        self.stat_type = SpecialAttribute.DAMAGE_BOOST
        self.tag = DamageTag.BURN

        ret.append(self)

        # Critical damage is permanently increased by 5% (per stack).
        critical_damage_increase_per_stack: int = 5
        ret.append(
            Buff(
                value=critical_damage_increase_per_stack
                * min(Embers.max_stack_count, stack),
                modifier_type=ModifierType.ADDITIVE,
                stat_type=SpecialAttribute.CRITICAL_DAMAGE,
                tag=DamageTag.ALL,
            )
        )

        return ret


class GlacialDomain(Buff):
    """Dushevnaya buff, granted by her Ultimate."""

    display_name = "Glacial Domain (Dushevnaya)"
    max_stack_count = 1
    stack_input_type = "select"

    def __init__(self, dushevnaya_fortification_level: int):
        """
        Arguments:
        dushevnaya_fortification_level -- the Fortification Level of Dushevnaya
        """
        # V5: While Glacial Domain is active, ignores 30% of the target's defense.
        if dushevnaya_fortification_level >= FortificationLevel.SEGMENT05:
            self.value = 30
        else:
            self.value = 0

        self.modifier_type = ModifierType.ADDITIVE
        self.stat_type = SpecialAttribute.DEFENSE_IGNORE
        self.tag = DamageTag.ALL


class ArcticBenediction(Buff):
    """Dushevnaya buff, granted by her Ultimate."""

    display_name = "Arctic Benediction"
    max_stack_count = 1
    stack_input_type = "select"

    def __init__(self, dushevnaya_fortification_level: int):
        """
        Arguments:
        dushevnaya_fortification_level -- the Fortification Level of Dushevnaya
        """
        if dushevnaya_fortification_level >= FortificationLevel.SEGMENT01:
            self.value = 20
        else:
            self.value = 10

        self.modifier_type = ModifierType.ADDITIVE
        self.stat_type = SpecialAttribute.DAMAGE_BOOST
        self.tag = DamageTag.ALL


class LateBloomer(Buff):
    """Alva buff granted by her Fixed Key 4 - Late Bloomer."""

    display_name = "Late Bloomer (Alva)"
    max_stack_count = 6
    stack_input_type = "select"

    def __init__(self, stacks_of_battle_prep_consumed: int):
        """
        Arguments:
        stacks_of_battle_prep_consumed -- the number of stacks of this buff, up to 6
        """
        self.value = 3 * min(
            LateBloomer.max_stack_count, stacks_of_battle_prep_consumed
        )
        self.modifier_type = ModifierType.MULTIPLICATIVE
        self.stat_type = StatType.ATTACK


class BrumalBarrier(Buff):
    """Buff granted by Alva, provided by her passive, Freezing Touch."""

    display_name = "Brumal Barrier (Alva)"
    max_stack_count = 1
    stack_input_type = "number"

    def __init__(self): ...

    def get_buffs(self, alva_fortification_level: FortificationLevel, shield_size: int):
        """
        Arguments:
        alva_fortification_level -- the Fortification Level of the Alva granting this buff
        shield_size -- the size of the shield provided by Alva
        """
        ret: list[Buff] = []

        freeze_damage_boost_per_shield: float = (
            1.5 / 1000
        )  # 2% for every 1000 points of Shield HP
        critical_damage_per_shield: float = (
            0 / 1000
        )  # 1% for every 1000 points of Shield HP

        if alva_fortification_level >= FortificationLevel.SEGMENT05:
            freeze_damage_boost_per_shield = (
                3 / 1000
            )  # 3% for every 1000 points of Shield HP
            critical_damage_per_shield = (
                2 / 1000
            )  # 2% for every 1000 points of Shield HP
        elif alva_fortification_level >= FortificationLevel.SEGMENT03:
            critical_damage_per_shield = (
                1 / 1000
            )  # 1% for every 1000 points of Shield HP

        self.value = freeze_damage_boost_per_shield * shield_size
        self.modifier_type = ModifierType.ADDITIVE
        self.stat_type = SpecialAttribute.DAMAGE_BOOST
        self.tag = DamageTag.FREEZE
        ret.append(self)

        if critical_damage_per_shield > 0:
            ret.append(
                Buff(
                    value=critical_damage_per_shield * shield_size,
                    modifier_type=ModifierType.ADDITIVE,
                    stat_type=SpecialAttribute.CRITICAL_DAMAGE,
                    tag=DamageTag.FREEZE,
                )
            )

        return ret


class CoveringMode(Buff):
    """Buff granted by Alva. This is the Freeze damage boost component."""

    display_name = "Covering Mode (Alva)"
    max_stack_count = 1
    stack_input_type = "select"

    def __init__(self):
        self.value = 20
        self.modifier_type = ModifierType.ADDITIVE
        self.stat_type = SpecialAttribute.DAMAGE_BOOST
        self.tag = DamageTag.FREEZE  # This assumes the target has a shield.


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


class DivineProtection(Buff):
    """Helen buff."""

    display_name = "Divine Protection"
    max_stack_count = 1
    stack_input_type = "select"

    def __init__(self, helen_fortification_level: int):
        """
        Arguments:
        helen_fortification_level -- the Fortification Level of Helen
        """
        if helen_fortification_level >= FortificationLevel.SEGMENT04:
            self.value = 30
        else:
            self.value = 0

        self.modifier_type = ModifierType.ADDITIVE
        self.stat_type = SpecialAttribute.DAMAGE_BOOST
        self.tag = DamageTag.FREEZE


class FrostchillDrive(Buff):
    """Helen buff."""

    display_name = "Frostchill Drive (Helen)"
    max_stack_count = 3
    stack_input_type = "number"

    def __init__(self, helen_fortification_level: int, stacks: int):
        """
        Arguments:
        helen_fortification_level -- the Fortification Level of Helen
        stacks -- the number of stacks of this buff
        """
        damage_boost_per_stack: int = 0

        if helen_fortification_level >= FortificationLevel.SEGMENT05:
            damage_boost_per_stack = 20

        self.value = damage_boost_per_stack * min(
            FrostchillDrive.max_stack_count, stacks
        )
        self.modifier_type = ModifierType.ADDITIVE
        self.stat_type = SpecialAttribute.DAMAGE_BOOST
        self.tag = DamageTag.FREEZE


class Tuning(Buff):
    """Daiyan buff. This is for the non-permanent Tuning stacks."""

    display_name = "Tuning (Daiyan)"
    max_stack_count = 10
    stack_input_type = "select"

    def __init__(self): ...

    def get_buffs(self, stacks: int):
        """
        Arguments:
        stacks -- the number of stacks of this buff, up to 10
        """
        crit_chance_per_stack: int = 3
        crit_damage_per_stack: int = 3

        ret: list[Buff] = []
        if stacks > 0:
            self.value = crit_chance_per_stack * min(Tuning.max_stack_count, stacks)
            self.modifier_type = ModifierType.ADDITIVE
            self.stat_type = StatType.CRIT_RATE
            ret.append(self)

            ret.append(
                Buff(
                    crit_damage_per_stack * min(stacks, Tuning.max_stack_count),
                    ModifierType.ADDITIVE,
                    StatType.CRIT_DAMAGE,
                    DamageTag.ALL,
                )
            )

        return ret


class PermanentTuning(Buff):
    """Daiyan buff. This is for the permanent Tuning stacks."""

    display_name = "Permanent Tuning (Daiyan)"
    max_stack_count = 6
    stack_input_type = "select"

    def __init__(self): ...

    def get_buffs(self, stacks: int):
        """
        Arguments:
        stacks -- the number of stacks of this buff, up to 6
        """
        crit_chance_per_stack: int = 3
        crit_damage_per_stack: int = 3

        # Expansion Key - Flowing Melody of the Clouds: For each stack of permanent Tuning Daiyan
        # possesses, ignores 10% of enemy target's defense when attacking.
        defense_ignore_per_stack: int = 10

        ret: list[Buff] = []
        if stacks > 0:
            self.value = crit_chance_per_stack * min(
                PermanentTuning.max_stack_count, stacks
            )
            self.modifier_type = ModifierType.ADDITIVE
            self.stat_type = StatType.CRIT_RATE
            ret.append(self)

            ret.append(
                Buff(
                    crit_damage_per_stack
                    * min(stacks, PermanentTuning.max_stack_count),
                    ModifierType.ADDITIVE,
                    StatType.CRIT_DAMAGE,
                    DamageTag.ALL,
                )
            )

            ret.append(
                Buff(
                    defense_ignore_per_stack
                    * min(stacks, PermanentTuning.max_stack_count),
                    ModifierType.ADDITIVE,
                    SpecialAttribute.DEFENSE_IGNORE,
                    DamageTag.ALL,
                )
            )

        return ret


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


class Chi(Buff):
    """Jiangyu buff."""

    display_name = "Chi (Jiangyu)"
    max_stack_count = 3
    stack_input_type = "select"

    def __init__(self, jiangyu_fortification_level: FortificationLevel):
        """
        Arguments:
        jiangyu_fortification_level -- the Fortification Level of the Jiangyu with this buff
        """
        if jiangyu_fortification_level == FortificationLevel.SEGMENT06:
            self.value = 15
            self.modifier_type = ModifierType.ADDITIVE
            self.stat_type = SpecialAttribute.DAMAGE_BOOST
            self.tag = DamageTag.ELECTRIC


class PowerSurge(Buff):
    """Jiangyu buff."""

    display_name = "Power Surge"
    max_stack_count = 6
    stack_input_type = "select"

    def __init__(self): ...

    def get_buffs(
        self,
        stacks: int,
        jiangyu_fortification_level: FortificationLevel,
        target_voltage_sag_stacks: int,
    ):
        """
        Arguments:
        stacks -- the number of stacks of this buff, up to 3
        jiangyu_fortification_level -- the Fortification Level of the Jiangyu granting this buff
        target_voltage_sag_stacks -- the number of stacks of Voltage Sag on the target, up to 6
        """
        # the class attr max_stack_count is 6 for code-gen to support Voltage Sag's maximum of 6
        max_power_surge_stacks: int = 3

        self.value = 5 * min(max_power_surge_stacks, stacks)
        self.modifier_type = ModifierType.ADDITIVE
        self.stat_type = SpecialAttribute.DEFENSE_IGNORE
        self.tag = DamageTag.ELECTRIC

        if jiangyu_fortification_level == FortificationLevel.SEGMENT06:
            self.value = 2 * self.value

        ret: list[Buff] = []
        ret.append(self)

        # Jiangyu Expansion Key - Urge to Perform:
        # When an allied unit with 3 stacks of Power Surge deals damage, for each stack of
        # Voltage Sag on the enemy unit, the allied unit's critical rate is increased by 2%
        # and its critical damage is increased by 3%.
        if stacks == 3 and target_voltage_sag_stacks > 0:
            ret.append(
                Buff(
                    value=2
                    * min(VoltageSag.max_stack_count, target_voltage_sag_stacks),
                    modifier_type=ModifierType.ADDITIVE,
                    stat_type=StatType.CRIT_RATE,
                    tag=DamageTag.ALL,
                )
            )
            ret.append(
                Buff(
                    value=3
                    * min(VoltageSag.max_stack_count, target_voltage_sag_stacks),
                    modifier_type=ModifierType.ADDITIVE,
                    stat_type=StatType.CRIT_DAMAGE,
                    tag=DamageTag.ALL,
                )
            )

        return ret


class StoredCharge(Buff):
    """Belka buff."""

    display_name = "Stored Charge (Belka)"
    max_stack_count = 10
    stack_input_type = "select"

    def __init__(self, belka_fortification_level: FortificationLevel, stacks: int):
        """
        Arguments:
        belka_fortification_level -- the Fortification Level of Belka with this buff
        """
        max_stacks: int = 6
        electric_damage_boost_per_stack: int = 5
        if belka_fortification_level >= FortificationLevel.SEGMENT04:
            max_stacks = StoredCharge.max_stack_count

        self.value = electric_damage_boost_per_stack * min(max_stacks, stacks)
        self.modifier_type = ModifierType.ADDITIVE
        self.stat_type = SpecialAttribute.DAMAGE_BOOST
        self.tag = DamageTag.ELECTRIC


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


class OverflowingCare(Buff):
    """Springfield buff"""

    display_name = "Overflowing Care"
    max_stack_count = 105
    stack_input_type = "number"

    def __init__(
        self,
        springfield_fortification_level: FortificationLevel,
        percent_excess_healing: float,
    ):
        """
        Arguments:
        springfield_fortification_level -- the Fortification Level of the Springfield applying this buff
        percent_excess_healing -- the percent of healing that exceeded the target's max health
        """
        # Increased Hydro damage dealt by 1% for every 1.5% excess healing, up to a maximum of 35% (V0) or 70% (V1)
        damage_boost_per_percent_excess_healing: float = (
            1 / 1.5
        )  # 1% damage boost for every 1.5% excess healing

        if springfield_fortification_level >= FortificationLevel.SEGMENT01:
            max_damage_boost = 70
        else:
            max_damage_boost = 35

        self.value = damage_boost_per_percent_excess_healing * max(
            0, percent_excess_healing
        )
        self.value = min(self.value, max_damage_boost)
        self.modifier_type = ModifierType.ADDITIVE
        self.stat_type = SpecialAttribute.DAMAGE_BOOST
        self.tag = DamageTag.HYDRO


class DeepRootedBonds(Buff):
    """Springfield buff"""

    display_name = "Deep-Rooted Bonds"
    max_stack_count = 1
    stack_input_type = "select"

    def __init__(self):
        # Max HP is increased by 100% of the buff holder's Max HP.
        self.value = 100
        self.modifier_type = ModifierType.MULTIPLICATIVE
        self.stat_type = StatType.HEALTH


class EaglesVigilance(Buff):
    """Buff granted to all allies when Taryz is on the field (from Springfield's passive, V3+)."""

    display_name = "Eagle's Vigilance (Taryz)"
    max_stack_count = 1
    stack_input_type = "select"

    def __init__(self, springfield_fortification_level: FortificationLevel):
        # When Taryz is on the field, Hydro damage dealt by all allied units' out-of-turn attacks
        # is increased by 40%.
        # Supposed to only apply to Hydro damage, but will assume that the user will only apply this buff
        # to Dolls that deal Hydro damage with their out-of-turn attacks.
        if springfield_fortification_level >= FortificationLevel.SEGMENT03:
            self.value = 40
        else:
            self.value = 0
        self.modifier_type = ModifierType.ADDITIVE
        self.stat_type = SpecialAttribute.DAMAGE_BOOST
        self.tag = DamageTag.PASSIVE


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


class CompetitiveSpirit(Buff):
    """Klukai buff"""

    display_name = "Competitive Spirit (Klukai)"
    max_stack_count = 12
    stack_input_type = "select"

    def __init__(self, stacks: int, klukai_fortification_level: FortificationLevel):
        value_per_stack: int = 5

        if klukai_fortification_level >= FortificationLevel.SEGMENT02:
            max_stacks: int = CompetitiveSpirit.max_stack_count
        else:
            max_stacks: int = 8

        self.value = value_per_stack * min(max_stacks, stacks)
        self.modifier_type = ModifierType.ADDITIVE
        self.stat_type = SpecialAttribute.DAMAGE_BOOST
        self.tag = DamageTag.CORROSION


class Candyglaze(Buff):
    """Lind buff"""

    display_name = "Candyglaze (Lind)"
    max_stack_count = 30
    stack_input_type = "select"

    def __init__(self, stacks: int, lind_fortification_level: FortificationLevel):
        if lind_fortification_level >= FortificationLevel.SEGMENT01:
            max_stacks: int = Candyglaze.max_stack_count
            value_per_stack: int = 2
        else:
            max_stacks: int = 10
            value_per_stack: int = 1

        self.value = value_per_stack * min(max_stacks, stacks)
        self.modifier_type = ModifierType.ADDITIVE
        self.stat_type = SpecialAttribute.DAMAGE_BOOST
        self.tag = DamageTag.CORROSION


class DreamGuardian(Buff):
    """Buff from Mechty. AoE damage dealt by Support Attacks is increased by 30%."""

    display_name = "Dream Guardian"
    max_stack_count = 1
    stack_input_type = "select"

    def __init__(self):
        self.value = 30
        self.modifier_type = ModifierType.ADDITIVE
        self.stat_type = SpecialAttribute.DAMAGE_BOOST
        self.tag = (
            DamageTag.SUPPORT_ACTION
        )  # This assumes the user will only apply this buff to Dolls that deal damage with AOE Support Actions.


class NightmareForm(Buff):
    """Buff from Mechty. AoE damage dealt is increased and AoE damage dealt by Support Attacks is also increased.  Additionally
    changes the damage type of AoE Support Attacks to Corrosion.
    """

    display_name = "Nightmare Form"
    max_stack_count = 1
    stack_input_type = "select"

    def __init__(self): ...

    def get_buffs(self, mechty_fortification_level: FortificationLevel):
        """
        Arguments:
        mechty_fortification_level -- the Fortification Level of the Mechty granting this buff
        """
        aoe_damage_boost: int = 10
        aoe_support_damage_boost: int = 50

        if mechty_fortification_level >= FortificationLevel.SEGMENT06:
            aoe_damage_boost: int = 20
            aoe_support_damage_boost: int = 80

        ret: list[Buff] = []

        self.value = aoe_damage_boost
        self.modifier_type = ModifierType.ADDITIVE
        self.stat_type = SpecialAttribute.DAMAGE_BOOST
        self.tag = DamageTag.AREA_OF_EFFECT

        ret.append(
            self,
        )

        # This assumes the user will only apply this buff to Dolls that deal damage with AoE Support Actions,
        # and that the change of damage type to Corrosion is handled elsewhere in the code.
        ret.append(
            Buff(
                value=aoe_support_damage_boost,
                modifier_type=ModifierType.ADDITIVE,
                stat_type=SpecialAttribute.DAMAGE_BOOST,
                tag=DamageTag.SUPPORT_ACTION,
            )
        )

        return ret


class ReturnForm(Buff):
    """Effect of V3+ Phaetusa after using Return Form (increase attack by 50% for 1 round)."""

    display_name = "Return Form (Phaetusa)"
    max_stack_count = 1
    stack_input_type = "select"

    def __init__(self, phaetusa_fortification_level: FortificationLevel):
        if phaetusa_fortification_level >= FortificationLevel.SEGMENT03:
            self.value = 50
        else:
            self.value = 0

        self.modifier_type = ModifierType.MULTIPLICATIVE
        self.stat_type = StatType.ATTACK
        self.tag = DamageTag.ALL


class ReplicationTrap(Buff):
    """Permanent effect of V1+ Phaetusa - gain 15% critical damage for every 2 uses of Replication Trap."""

    display_name = "Replication Trap (Phaetusa)"
    max_stack_count = 6
    stack_input_type = "input"

    def __init__(
        self,
        uses_of_replication_trap: int,
        phaetusa_fortification_level: FortificationLevel,
    ):
        critical_damage_per_two_uses: int = 0
        if phaetusa_fortification_level >= FortificationLevel.SEGMENT03:
            critical_damage_per_two_uses = 15

        self.value = critical_damage_per_two_uses * (uses_of_replication_trap // 2)
        self.modifier_type = ModifierType.ADDITIVE
        self.stat_type = SpecialAttribute.CRITICAL_DAMAGE
        self.tag = DamageTag.ALL


class SupportBoostI(Buff):
    """Increases damage dealt with Support Action by 15%. Damage against exposed units is increased by 10%."""

    display_name = "Support Boost I"
    max_stack_count = 1
    stack_input_type = "select"

    def __init__(self): ...

    def get_buffs(self):
        self.value = 15
        self.modifier_type = ModifierType.ADDITIVE
        self.stat_type = SpecialAttribute.DAMAGE_BOOST
        self.tag = DamageTag.SUPPORT_ACTION

        ret: list[Buff] = [
            self,
        ]

        ret.append(
            Buff(
                value=10,
                modifier_type=ModifierType.ADDITIVE,
                stat_type=SpecialAttribute.DAMAGE_BOOST,
                tag=DamageTag.EXPOSED,
            ),
        )

        return ret


class SupportBoostII(Buff):
    """Increases damage dealt with Support Action by 30%. Damage against exposed units is increased by 10%."""

    display_name = "Support Boost II"
    max_stack_count = 1
    stack_input_type = "select"

    def __init__(self): ...

    def get_buffs(self):
        self.value = 30
        self.modifier_type = ModifierType.ADDITIVE
        self.stat_type = SpecialAttribute.DAMAGE_BOOST
        self.tag = DamageTag.SUPPORT_ACTION

        ret: list[Buff] = [
            self,
        ]

        ret.append(
            Buff(
                value=10,
                modifier_type=ModifierType.ADDITIVE,
                stat_type=SpecialAttribute.DAMAGE_BOOST,
                tag=DamageTag.EXPOSED,
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


class AttackUpIII(Buff):
    """Attack is increased by 20%. Considered a buff."""

    display_name = "Attack Up III"
    max_stack_count = 1
    stack_input_type = "select"

    def __init__(self):
        self.value = 20
        self.modifier_type = ModifierType.MULTIPLICATIVE
        self.stat_type = StatType.ATTACK


class CriticalDamageUpII(Buff):
    """Critical damage is increased by 20%."""

    display_name = "Critical Damage Up II"
    max_stack_count = 1
    stack_input_type = "select"

    def __init__(self):
        self.value = 20
        self.modifier_type = ModifierType.ADDITIVE
        self.stat_type = StatType.CRIT_DAMAGE
        self.tag = DamageTag.ALL


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


class DefenseUpIII(Buff):
    """Defense is increased by 40%. Considered a buff."""

    display_name = "Defense Up III"
    max_stack_count = 1
    stack_input_type = "select"

    def __init__(self):
        self.value = 40
        self.modifier_type = ModifierType.MULTIPLICATIVE
        self.stat_type = StatType.DEFENSE


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
        # Expansion Key: Algorithmic Stack - Additional 6%
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


class OverheatCombustion(Debuff):
    """Vector debuff"""

    display_name = "Overheat Combustion"
    max_stack_count = 1
    stack_input_type = "select"

    def __init__(self, vector_fortification_level: FortificationLevel):
        """
        Arguments:
        vector_fortification_level -- the Fortification Level of the Vector applying this debuff
        """
        if vector_fortification_level >= FortificationLevel.SEGMENT01:
            self.value = 30
        else:
            self.value = 0

        self.modifier_type = ModifierType.ADDITIVE
        self.stat_type = SpecialAttribute.INCREASE_DAMAGE_TAKEN
        self.tag = DamageTag.BURN


class Conflagration(Debuff):
    """Debuff from Incineration tiles. Increases burn damage taken by 20%. Considered a Burn debuff."""

    display_name = "Conflagration"
    max_stack_count = 1
    stack_input_type = "select"

    def __init__(self):
        """ """
        self.value = 20

        self.modifier_type = ModifierType.ADDITIVE
        self.stat_type = SpecialAttribute.INCREASE_DAMAGE_TAKEN
        self.tag = DamageTag.BURN


class Smolder(Debuff):
    """Vector debuff"""

    display_name = "Smolder"
    max_stack_count = 3
    stack_input_type = "number"

    def __init__(
        self,
        vector_fortification_level: FortificationLevel,
        number_of_burn_debuffs: int,
    ):
        """
        Arguments:
        stacks -- the number of stacks of this buff
        vector_fortification_level -- the Fortification Level of the Vector applying this debuff
        """
        if vector_fortification_level >= FortificationLevel.SEGMENT04:
            increased_damage_taken_per_stack: int = 3
            self.value = increased_damage_taken_per_stack * max(
                0, number_of_burn_debuffs
            )
        else:
            self.value = 0

        self.modifier_type = ModifierType.ADDITIVE
        self.stat_type = SpecialAttribute.INCREASE_DAMAGE_TAKEN
        self.tag = DamageTag.ALL


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


class FalseIntelligence(Debuff):
    """Springfield debuff. Increased Hydro damage taken when in Stability Break."""

    display_name = "False Intelligence"
    max_stack_count = 1
    stack_input_type = "select"

    def __init__(self, springfield_fortification_level: FortificationLevel):
        """
        Arguments:
        springfield_fortification_level -- the Fortification Level of the Springfield applying this debuff
        """
        # Assume the user will only apply this debuff when the target is in Stability Break,
        # since that's when it's supposed to apply.
        # At V4, increases Hydro damage taken by 20% at Segment 4 and above, and 10% otherwise.
        if springfield_fortification_level >= FortificationLevel.SEGMENT04:
            self.value = 20
        else:
            self.value = 10

        self.modifier_type = ModifierType.ADDITIVE
        self.stat_type = SpecialAttribute.INCREASE_DAMAGE_TAKEN
        self.tag = DamageTag.HYDRO


class Taryz(Debuff):
    """The target that Taryz is following. At V3+, increased Hydro damage taken by 10%."""

    display_name = "Taryz"
    max_stack_count = 1
    stack_input_type = "select"

    def __init__(self, springfield_fortification_level: FortificationLevel):
        """
        Arguments:
        springfield_fortification_level -- the Fortification Level of the Springfield applying this debuff
        """
        if springfield_fortification_level >= FortificationLevel.SEGMENT03:
            self.value = 10
        else:
            self.value = 0

        self.modifier_type = ModifierType.ADDITIVE
        self.stat_type = SpecialAttribute.INCREASE_DAMAGE_TAKEN
        self.tag = DamageTag.HYDRO


class VulnerabilityAnalysis(Debuff):
    """Applied by Assault Taryz before attacking. Hydro damage taken
    is increased by 5% per stack, stacking up to 3 times."""

    display_name = "Vulnerability Analysis"
    max_stack_count = 3
    stack_input_type = "select"

    def __init__(
        self, springfield_fortification_level: FortificationLevel, stacks: int
    ):
        """
        Arguments:
        springfield_fortification_level -- the Fortification Level of the Springfield applying this debuff
        stacks -- the number of stacks of this debuff, up to 3
        """
        if springfield_fortification_level >= FortificationLevel.SEGMENT06:
            increased_damage_taken_per_stack: int = 5
        else:
            # Only available with V6 Springfield.
            increased_damage_taken_per_stack: int = 0

        self.value = increased_damage_taken_per_stack * stacks
        self.modifier_type = ModifierType.ADDITIVE
        self.stat_type = SpecialAttribute.INCREASE_DAMAGE_TAKEN
        self.tag = DamageTag.HYDRO


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


class Overzealous(Debuff):
    """Increase damage taken by 30% from Vepley."""

    display_name = "Overzealous (Vepley)"
    max_stack_count = 1
    stack_input_type = "select"

    def __init__(self):
        self.value = 30
        self.modifier_type = ModifierType.ADDITIVE
        self.stat_type = SpecialAttribute.INCREASE_DAMAGE_TAKEN
        self.tag = DamageTag.ALL


class CorrosiveInfusion(Debuff):
    """Debuff from Klukai. Triggers at the end of the holder's turn. At V2+, reduces the holder's defense."""

    display_name = "Corrosive Infusion (Klukai)"
    max_stack_count = 15
    stack_input_type = "select"

    def __init__(self, stacks: int, klukai_fortification_level: FortificationLevel):
        """
        Arguments:
        klukai_fortification_level -- the Fortification Level of the Klukai applying this debuff
        """
        if klukai_fortification_level >= FortificationLevel.SEGMENT02:
            self.value = -1 * min(15, stacks)
        else:
            self.value = 0

        self.modifier_type = ModifierType.MULTIPLICATIVE
        self.stat_type = StatType.DEFENSE
        self.tag = DamageTag.ALL


class ToxinInundation(Debuff):
    """Corrosion damage taken is increased by 25%. Considered a Corrosion defense debuff."""

    display_name = "Toxin Inundation"
    max_stack_count = 1
    stack_input_type = "select"

    def __init__(self):
        self.value = 25
        self.modifier_type = ModifierType.ADDITIVE
        self.stat_type = SpecialAttribute.INCREASE_DAMAGE_TAKEN
        self.tag = DamageTag.CORROSION


class AcidCorrosionII(Debuff):
    """Reduces defense by 30%. Considered a Corrosion defense debuff."""

    display_name = "Acid Corrosion II"
    max_stack_count = 1
    stack_input_type = "select"

    def __init__(self):
        self.value = -30
        self.modifier_type = ModifierType.MULTIPLICATIVE
        self.stat_type = StatType.DEFENSE
        self.tag = DamageTag.CORROSION


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
