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

MAX_TILE_ASCENSION_LEVEL: int = 3


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


class WokHei(Buff):
    """Stacking buff from Qiuhua's Expansion Key - Sizzling Stir-Fry. Stacks up to 4 times."""

    display_name = "Wok Hei (Qiuhua)"
    max_stack_count = 4
    stack_input_type = "select"

    def __init__(self, stacks: int):
        burn_damage_boost_per_stack: int = 7
        self.value = burn_damage_boost_per_stack * min(WokHei.max_stack_count, stacks)
        self.modifier_type = ModifierType.ADDITIVE
        self.stat_type = SpecialAttribute.DAMAGE_BOOST
        self.tag = DamageTag.BURN


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


class Rank(Buff):
    """Buff granted to Lewis by her Tin Soldier based on its rank (this is per Soldier; use two Buff instances for two Soldiers)."""

    display_name = "Rank (Lewis)"
    max_stack_count = 4
    stack_input_type = "input"

    def __init__(self): ...

    def get_buffs(self, lewis_fortification_level: FortificationLevel, rank: int):
        """
        Arguments:
        lewis_fortification_level -- the Fortification Level of Lewis receiving this buff
        rank -- the rank of the Tin Soldier granting this buff (1, 2, or 3)
        """
        ret: list[Buff] = []

        # Higher ranks include the effects of lower ranks, so we can use a simple if/elif structure.
        # Rank I: Burn damage dealt is increased by 10%.
        # Rank II: Burn damage dealt is increased by 15% and critical rate is increased by 10%.
        # Rank II (V6): Additionally, critical damage is increased by 15%.
        # Rank III: Volley Fire triggered by Toy Carnival - implemented through rotation.

        # Burn damage dealt
        self.value = 0
        self.modifier_type = ModifierType.ADDITIVE
        self.stat_type = SpecialAttribute.DAMAGE_BOOST
        self.tag = DamageTag.BURN

        if rank >= 1:
            self.value += 10

        if rank >= 2:
            self.value += 15

        ret.append(self)

        # Critical rate
        if rank >= 2:
            ret.append(
                Buff(
                    value=10,
                    modifier_type=ModifierType.ADDITIVE,
                    stat_type=StatType.CRIT_RATE,
                    tag=DamageTag.ALL,
                )
            )

        # Critical damage (V6)
        if rank >= 2 and lewis_fortification_level >= FortificationLevel.SEGMENT06:
            ret.append(
                Buff(
                    value=15,
                    modifier_type=ModifierType.ADDITIVE,
                    stat_type=SpecialAttribute.CRITICAL_DAMAGE,
                    tag=DamageTag.ALL,
                )
            )

        return ret


class GlowingEmbers(Buff):
    """Enhanced version of Embers, granted by fully charging Thermal Conduction with Loreley on the field."""

    display_name = "Glowing Embers"
    max_stack_count = 6  # Theoretically infinite, but no battle lasts long enough.
    stack_input_type = "select"

    def __init__(self): ...

    def get_buffs(self, loreley_fortification_level: FortificationLevel, stack: int):
        """
        Arguments:
        loreley_fortification_level -- the Fortification Level of the Loreley granting this buff
        stack -- the number of stacks of this buff, up to 6
        """
        ret: list[Buff] = []

        if loreley_fortification_level >= FortificationLevel.SEGMENT02:
            # Increases damage dealt by 45%.
            self.value = 45
            self.modifier_type = ModifierType.ADDITIVE
            self.stat_type = SpecialAttribute.DAMAGE_BOOST
            self.tag = DamageTag.ALL

            ret.append(self)
        else:
            # Burn damage dealt is increased by 30%. (Baseline effect of Embers.)
            self.value = 30
            self.modifier_type = ModifierType.ADDITIVE
            self.stat_type = SpecialAttribute.DAMAGE_BOOST
            self.tag = DamageTag.BURN

            ret.append(self)

            # Increase damage dealt by 15%. (Additional effect from Glowing Embers)
            ret.append(
                Buff(
                    value=15,
                    modifier_type=ModifierType.ADDITIVE,
                    stat_type=SpecialAttribute.DAMAGE_BOOST,
                    tag=DamageTag.ALL,
                )
            )

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


class BurningTide(Buff):
    """Buff from Loreley's Ranger Mk.II."""

    display_name = "Burning Tide (Loreley)"
    max_stack_count = 1
    stack_input_type = "select"

    def __init__(self, loreley_fortification_level: FortificationLevel):
        """
        Arguments:
        loreley_fortification_level -- the Fortification Level of the Loreley granting this buff
        """
        if loreley_fortification_level >= FortificationLevel.SEGMENT06:
            self.value = 12
        else:
            self.value = 6

        self.modifier_type = ModifierType.MULTIPLICATIVE
        self.stat_type = StatType.ATTACK
        self.tag = DamageTag.ALL


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
        self.tag = DamageTag.FREEZE


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
        self.tag = DamageTag.FREEZE


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


class Succor(Buff):
    """Helen buff."""

    display_name = "Succor"
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


class FeralFactor(Buff):
    """Soppo buff"""

    display_name = "Feral Factor (Soppo)"
    max_stack_count = 20
    stack_input_type = "select"

    def __init__(self, stacks: int):
        critical_damage_per_stack: int = 5

        self.value = critical_damage_per_stack * min(
            FeralFactor.max_stack_count, stacks
        )
        self.modifier_type = ModifierType.ADDITIVE
        self.stat_type = StatType.CRIT_DAMAGE
        self.tag = DamageTag.ALL


class FeralFactorI(Buff):
    """Soppo buff"""

    display_name = "Feral Factor I (Soppo)"
    max_stack_count = 20
    stack_input_type = "select"

    def __init__(
        self,
        soppo_fortification_level: FortificationLevel,
        tile_level: int,
        stacks_of_feral_factor: int,
    ):
        """
        Arguments:
        soppo_fortification_level -- the Fortification Level of Soppo
        tile_level -- the level of the phase tile the target is on (0 if not on a phase tile)
        stacks_of_feral_factor -- the number of stacks of Feral Factor (Soppo) the target has, up to 20
        """
        self.value = 10
        if (
            soppo_fortification_level >= FortificationLevel.SEGMENT06
            and stacks_of_feral_factor >= 20
        ):
            self.value += 10

        self.modifier_type = ModifierType.ADDITIVE
        self.stat_type = SpecialAttribute.DEFENSE_IGNORE
        self.tag = DamageTag.ON_PHASE_TILE

        defense_ignore_increase_per_tile_level: int = 10

        if tile_level > 0:
            self.value += defense_ignore_increase_per_tile_level * min(
                MAX_TILE_ASCENSION_LEVEL, tile_level
            )


class FeralFactorII(Buff):
    """Soppo buff"""

    display_name = "Feral Factor II (Soppo)"
    max_stack_count = 20
    stack_input_type = "select"

    def __init__(self): ...

    def get_buffs(
        self,
        soppo_fortification_level: FortificationLevel,
        number_of_freeze_and_burn_buffs: int,
        stacks_of_feral_factor: int,
    ):
        """
        Arguments:
        soppo_fortification_level -- the Fortification Level of Soppo
        number_of_freeze_and_burn_buffs -- the number of Freeze and Burn buffs Soppo has
        stacks_of_feral_factor -- the number of stacks of Feral Factor (Soppo) the target has, up to 20
        """
        ret: list[Buff] = []

        damage_boost_per_freeze_and_burn_buff: int = 5

        # V6: If the target has 20 stacks of Feral Factor, increase damage dealt by 5%.
        if (
            soppo_fortification_level >= FortificationLevel.SEGMENT06
            and stacks_of_feral_factor >= 20
        ):
            damage_boost_per_freeze_and_burn_buff = 10

        self.value = (
            number_of_freeze_and_burn_buffs * damage_boost_per_freeze_and_burn_buff
        )
        self.modifier_type = ModifierType.ADDITIVE
        self.stat_type = SpecialAttribute.DAMAGE_BOOST
        self.tag = DamageTag.FREEZE

        ret.append(self)

        ret.append(
            Buff(
                value=self.value,
                modifier_type=ModifierType.ADDITIVE,
                stat_type=SpecialAttribute.DAMAGE_BOOST,
                tag=DamageTag.BURN,
            )
        )

        return ret


class FeralFactorIII(Buff):
    """Soppo buff"""

    display_name = "Feral Factor III (Soppo)"
    max_stack_count = 20
    stack_input_type = "select"

    def __init__(
        self,
        soppo_fortification_level: FortificationLevel,
        tile_level: int,
        stacks_of_feral_factor: int,
    ):
        """
        Arguments:
        soppo_fortification_level -- the Fortification Level of Soppo
        tile_level -- the level of the phase tile the target is on (0 if not on a phase tile)
        stacks_of_feral_factor -- the number of stacks of Feral Factor (Soppo) the target has, up to 20
        """
        self.value = 15
        self.modifier_type = ModifierType.ADDITIVE
        self.stat_type = SpecialAttribute.DAMAGE_BOOST
        self.tag = DamageTag.ON_PHASE_TILE

        if (
            soppo_fortification_level >= FortificationLevel.SEGMENT06
            and stacks_of_feral_factor >= 20
        ):
            self.value += 15

        damage_boost_per_tile_level: int = 10

        if tile_level > 0:
            self.value += damage_boost_per_tile_level * min(
                MAX_TILE_ASCENSION_LEVEL, tile_level
            )


class SlaughterTrail(Buff):
    """Buff granted from Soppo"""

    display_name = "Slaughter Trail (Soppo)"
    max_stack_count = 1
    stack_input_type = "select"

    def __init__(self):
        self.value = 20
        self.modifier_type = ModifierType.ADDITIVE
        self.stat_type = SpecialAttribute.DAMAGE_BOOST
        self.tag = DamageTag.ON_PHASE_TILE


class FrostStrike(Buff):
    """Increases attack by 10%."""

    display_name = "Frost Strike"
    max_stack_count = 1
    stack_input_type = "select"

    def __init__(self):
        self.value = 10
        self.modifier_type = ModifierType.MULTIPLICATIVE
        self.stat_type = StatType.ATTACK


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


class MimosasCalyx(Buff):
    """Cheyanne buff."""

    display_name = "Mimosa's Calyx (Cheyanne)"
    max_stack_count = 1
    stack_input_type = "select"

    def __init__(self): ...

    def get_buffs(self):
        # Increase attack by 50% and critical rate by 20%.
        self.value = 50
        self.modifier_type = ModifierType.MULTIPLICATIVE
        self.stat_type = StatType.ATTACK
        self.tag = DamageTag.ALL

        ret: list[Buff] = []
        ret.append(self)

        ret.append(Buff(20, ModifierType.ADDITIVE, StatType.CRIT_RATE, DamageTag.ALL))

        return ret


class SenseOfSecurity(Buff):
    """Buff granted to Cheyanne (V4+) for each turn Mimosa's Calyx is active, stacking up to 3 times."""

    display_name = "Sense of Security (Cheyanne)"
    max_stack_count = 3
    stack_input_type = "select"

    def __init__(self, stacks: int, cheyanne_fortification_level: FortificationLevel):
        """
        Arguments:
        stacks -- the number of stacks of this buff, up to 3
        cheyanne_fortification_level -- the Fortification Level of Cheyanne granting this buff
        """
        attack_boost_per_stack: int = 0
        if cheyanne_fortification_level >= FortificationLevel.SEGMENT05:
            attack_boost_per_stack = 20

        self.value = attack_boost_per_stack * min(
            SenseOfSecurity.max_stack_count, stacks
        )
        self.modifier_type = ModifierType.MULTIPLICATIVE
        self.stat_type = StatType.ATTACK
        self.tag = DamageTag.ALL


class Bond(Buff):
    """Buff from Asteria."""

    display_name = "Bond (Asteria)"
    max_stack_count = 4000
    stack_input_type = "number"

    def __init__(self, asteria_initial_attack: int):
        """
        Arguments:
        asteria_initial_attack -- the initial attack of Asteria
        """
        maximum_attack_gain: int = 300

        self.value = min(0.10 * asteria_initial_attack, maximum_attack_gain)
        self.modifier_type = ModifierType.ADDITIVE
        self.stat_type = StatType.ATTACK


class Sync(Buff):
    """Buff from Asteria."""

    display_name = "Sync (Asteria)"
    max_stack_count = 4000
    stack_input_type = "number"

    def __init__(self): ...

    def get_buffs(
        self,
        asteria_initial_attack: int,
        asteria_initial_critical_damage: int,
        asteria_fortification_level: FortificationLevel,
    ):
        """
        Arguments:
        asteria_initial_attack -- the initial attack of Asteria
        asteria_initial_critical_damage -- the initial critical damage of Asteria
        asteria_fortification_level -- the Fortification Level of Asteria granting this buff
        """
        maximum_attack_gain: int = 600

        self.value = min(0.10 * asteria_initial_attack, maximum_attack_gain)
        self.modifier_type = ModifierType.ADDITIVE
        self.stat_type = StatType.ATTACK

        ret: list[Buff] = []
        ret.append(self)

        if asteria_fortification_level >= FortificationLevel.SEGMENT02:
            self.value = 0.30 * asteria_initial_critical_damage
            self.modifier_type = ModifierType.ADDITIVE
            self.stat_type = StatType.CRIT_DAMAGE

            ret.append(
                Buff(
                    0.30 * asteria_initial_critical_damage,
                    ModifierType.ADDITIVE,
                    StatType.CRIT_DAMAGE,
                    DamageTag.ALL,
                )
            )

        return ret


class CrimeAndPunishment(Buff):
    """Buff from Asteria. This covers the stat increases."""

    display_name = "Crime and Punishment (Asteria)"
    max_stack_count = 0
    stack_input_type = "number"

    def __init__(self): ...

    def get_buffs(
        self,
    ):
        """
        Arguments:
        """
        self.value = 50
        self.modifier_type = ModifierType.MULTIPLICATIVE
        self.stat_type = StatType.ATTACK

        ret: list[Buff] = []
        ret.append(self)

        ret.append(Buff(30, ModifierType.ADDITIVE, StatType.CRIT_RATE, DamageTag.ALL))
        ret.append(Buff(30, ModifierType.ADDITIVE, StatType.CRIT_DAMAGE, DamageTag.ALL))

        return ret


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


class RigorSanguis(Buff):
    """Sextans buff. This is the stacking critical rate buff; the critical rate overflow
    effects are handled in the damage calculation strategy for Sextans.
    """

    display_name = "Rigor Sanguis (Sextans)"
    max_stack_count = 15
    stack_input_type = "select"

    def __init__(self, sextans_fortification_level: FortificationLevel, stacks: int):
        """
        Arguments:
        sextans_fortification_level -- the Fortification Level of Sextans with this buff
        stacks -- the number of stacks of this buff
        """
        maximum_critical_rate_bonus: int = 50
        critical_rate_per_stack: int = 5
        if sextans_fortification_level >= FortificationLevel.SEGMENT06:
            maximum_critical_rate_bonus = 75

        self.value = min(maximum_critical_rate_bonus, critical_rate_per_stack * stacks)
        self.modifier_type = ModifierType.ADDITIVE
        self.stat_type = StatType.CRIT_RATE
        self.tag = DamageTag.ALL


class AmaranthBrandElectric(Buff):
    """Sextans buff. This is the version that increases Electric damage dealt.
    In reality, it is the same buff as the Melee damage version, but implementing
    them in the same Buff would cause double-dipping for Electric+Melee damage.
    """

    display_name = "Amaranth Brand (Electric) (Sextans)"
    max_stack_count = 15
    stack_input_type = "input"

    def __init__(
        self,
        sextans_fortification_level: FortificationLevel,
        stacks_of_rigor_sanguis: int,
    ):
        """
        Arguments:
        sextans_fortification_level -- the Fortification Level of Sextans with this buff
        stacks_of_rigor_sanguis -- the number of stacks of the Rigor Sanguis buff held by Sextans
        """
        damage_boost_per_rigor_sanguis_stack: int = 3

        if sextans_fortification_level >= FortificationLevel.SEGMENT02:
            damage_boost_per_rigor_sanguis_stack = 5

        self.value = damage_boost_per_rigor_sanguis_stack * stacks_of_rigor_sanguis
        self.modifier_type = ModifierType.ADDITIVE
        self.stat_type = SpecialAttribute.DAMAGE_BOOST
        self.tag = DamageTag.ELECTRIC


class AmaranthBrandMelee(Buff):
    """Sextans buff. This is the version that increases Melee damage dealt.
    In reality, it is the same buff as the Electric damage version, but implementing
    them in the same Buff would cause double-dipping for Electric+Melee damage.
    """

    display_name = "Amaranth Brand (Melee) (Sextans)"
    max_stack_count = 15
    stack_input_type = "number"

    def __init__(
        self,
        sextans_fortification_level: FortificationLevel,
        stacks_of_rigor_sanguis: int,
    ):
        """
        Arguments:
        sextans_fortification_level -- the Fortification Level of Sextans with this buff
        stacks_of_rigor_sanguis -- the number of stacks of the Rigor Sanguis buff held by Sextans
        """
        damage_boost_per_rigor_sanguis_stack: int = 3

        if sextans_fortification_level >= FortificationLevel.SEGMENT02:
            damage_boost_per_rigor_sanguis_stack = 5

        self.value = damage_boost_per_rigor_sanguis_stack * stacks_of_rigor_sanguis
        self.modifier_type = ModifierType.ADDITIVE
        self.stat_type = SpecialAttribute.DAMAGE_BOOST
        self.tag = DamageTag.MELEE


class ElectricBoostII(Buff):
    """Increase Electric damage dealt by 20%."""

    display_name = "Electric Boost II"
    max_stack_count = 1
    stack_input_type = "number"

    def __init__(self):
        self.value = 20
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


class Elsin(Buff):
    """Effect granted when Elsin is present from Springfield's Expansion Key - Watching Each Other."""

    display_name = "Elsin"
    max_stack_count = 1
    stack_input_type = "select"

    def __init__(self):
        # If Elsin exists, damage dealt by allied physical summons is increased by 50%.
        self.value = 50
        self.modifier_type = ModifierType.ADDITIVE
        self.stat_type = SpecialAttribute.DAMAGE_BOOST
        self.tag = DamageTag.PHYSICAL_SUMMON


class Clue(Buff):
    """Nikketa buff"""

    display_name = "Clue"
    max_stack_count = 10
    stack_input_type = "select"

    def __init__(self, stacks: int, nikketa_fortification_level: FortificationLevel):
        """
        Arguments:
        stacks -- the number of stacks
        nikketa_fortification_level -- the Fortification Level of the Nikketa applying this debuff
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


class JointOps(Buff):
    """Pegasus buff. At V4+, increases critical damage of both Liushih and Pegasus."""

    display_name = "Joint Ops (Liushih)"
    max_stack_count = 1
    stack_input_type = "select"

    def __init__(self, liushih_fortification_level: FortificationLevel):
        """
        Arguments:
        liushih_fortification_level -- the Fortification Level of the Liushih granting this buff
        """
        if liushih_fortification_level >= FortificationLevel.SEGMENT04:
            self.value = 30
        else:
            self.value = 0

        self.modifier_type = ModifierType.ADDITIVE
        self.stat_type = SpecialAttribute.CRITICAL_DAMAGE
        self.tag = DamageTag.ALL


class Boldness(Buff):
    """Buff from Liushih (V5+). Damage dealt is increased by 5%."""

    display_name = "Boldness"
    max_stack_count = 10
    stack_input_type = "select"

    def __init__(self, stacks: int, liushih_fortification_level: FortificationLevel):
        """
        Arguments:
        stacks -- the number of stacks
        liushih_fortification_level -- the Fortification Level of the Liushih applying this debuff
        """
        damage_boost_per_stack: int = 0
        if liushih_fortification_level >= FortificationLevel.SEGMENT05:
            damage_boost_per_stack = 5

        self.value = damage_boost_per_stack * stacks
        self.modifier_type = ModifierType.ADDITIVE
        self.stat_type = SpecialAttribute.DAMAGE_BOOST
        self.tag = DamageTag.ALL


class Wellflow(Buff):
    """Hydro buff. Max HP increased by 10%."""

    display_name = "Wellflow"
    max_stack_count = 1
    stack_input_type = "select"

    def __init__(self):
        """
        Arguments:
        """
        self.value = 10
        self.modifier_type = ModifierType.MULTIPLICATIVE
        self.stat_type = StatType.HEALTH
        self.tag = DamageTag.ALL


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


class PatchMode(Buff):
    """Mechty buff"""

    display_name = "Patch Mode (Mechty)"
    max_stack_count = 1
    stack_input_type = "select"

    def __init__(self): ...

    def get_buffs(self, mechty_fortification_level: FortificationLevel):
        """
        Arguments:
        mechty_fortification_level -- the Fortification Level of the Mechty granting this buff
        """
        ret: list[Buff] = []

        if mechty_fortification_level >= FortificationLevel.SEGMENT06:
            # Corrosion damage dealt by all allied units is increased by 25%
            ret.append(
                Buff(
                    value=25,
                    modifier_type=ModifierType.ADDITIVE,
                    stat_type=SpecialAttribute.DAMAGE_BOOST,
                    tag=DamageTag.CORROSION,
                )
            )

            # Basic attacks deal 50% more damage
            ret.append(
                Buff(
                    value=50,
                    modifier_type=ModifierType.ADDITIVE,
                    stat_type=SpecialAttribute.DAMAGE_BOOST,
                    tag=DamageTag.BASIC,
                )
            )

            # Basic attack critical damage is increased by 80%
            ret.append(
                Buff(
                    value=80,
                    modifier_type=ModifierType.ADDITIVE,
                    stat_type=SpecialAttribute.CRITICAL_DAMAGE,
                    tag=DamageTag.BASIC,
                )
            )
        elif mechty_fortification_level >= FortificationLevel.SEGMENT02:
            # Basic attacks deal 50% more damage
            ret.append(
                Buff(
                    value=50,
                    modifier_type=ModifierType.ADDITIVE,
                    stat_type=SpecialAttribute.DAMAGE_BOOST,
                    tag=DamageTag.BASIC,
                )
            )

        return ret


class TurboMode(Buff):
    """Mechty buff"""

    display_name = "Turbo Mode (Mechty)"
    max_stack_count = 1
    stack_input_type = "select"

    def __init__(self): ...

    def get_buffs(self, mechty_fortification_level: FortificationLevel):
        """
        Arguments:
        mechty_fortification_level -- the Fortification Level of the Mechty granting this buff
        """
        ret: list[Buff] = []

        # Attack and Defense are increased by 30%
        ret.append(
            Buff(
                value=30,
                modifier_type=ModifierType.MULTIPLICATIVE,
                stat_type=StatType.ATTACK,
                tag=DamageTag.ALL,
            )
        )

        ret.append(
            Buff(
                value=30,
                modifier_type=ModifierType.MULTIPLICATIVE,
                stat_type=StatType.DEFENSE,
                tag=DamageTag.ALL,
            )
        )

        if mechty_fortification_level >= FortificationLevel.SEGMENT05:
            # Critical rate is increased by 30%
            ret.append(
                Buff(
                    value=30,
                    modifier_type=ModifierType.ADDITIVE,
                    stat_type=StatType.CRIT_RATE,
                    tag=DamageTag.ALL,
                )
            )
        elif mechty_fortification_level >= FortificationLevel.SEGMENT01:
            # Critical rate of basic attacks is increased by 30%
            ret.append(
                Buff(
                    value=30,
                    modifier_type=ModifierType.ADDITIVE,
                    stat_type=StatType.CRIT_RATE,
                    tag=DamageTag.BASIC,
                )
            )

        return ret


class SleepAidKit(Buff):
    """Mechty buff."""

    display_name = "Sleep Aid Kit (Mechty)"
    max_stack_count = 3
    stack_input_type = "select"

    def __init__(self, mechty_fortification_level: FortificationLevel, stacks: int):
        if mechty_fortification_level >= FortificationLevel.SEGMENT02:
            max_stacks: int = 3
        else:
            max_stacks: int = 2

        damage_boost_per_stack: int = 10
        self.value = damage_boost_per_stack * min(stacks, max_stacks)
        self.modifier_type = ModifierType.ADDITIVE
        self.stat_type = SpecialAttribute.DAMAGE_BOOST
        self.tag = DamageTag.ALL


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


class DreamscapeExhilaration(Buff):
    """Buff from Mechty in Sleepwalking state."""

    display_name = "Dreamscape Exhilaration (Mechty)"
    max_stack_count = 6
    stack_input_type = "select"

    def __init__(self, stacks: int):
        damage_boost_per_stack: int = 5

        self.value = damage_boost_per_stack * min(stacks, self.max_stack_count)
        self.modifier_type = ModifierType.ADDITIVE
        self.stat_type = SpecialAttribute.DAMAGE_BOOST
        self.tag = DamageTag.CORROSION


class Reversion(Buff):
    """Effect of V3+ Phaetusa after using Synchrony (increase attack by 50% for 1 round)."""

    display_name = "Reversion (Phaetusa)"
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


class OverwriteTrap(Buff):
    """Permanent effect of V1+ Phaetusa - gain 15% critical damage for every 2 uses of Overwrite Trap."""

    display_name = "Overwrite Trap (Phaetusa)"
    max_stack_count = 4
    stack_input_type = "input"

    def __init__(
        self,
        uses_of_overwrite_trap: int,
        phaetusa_fortification_level: FortificationLevel,
    ):
        critical_damage_per_two_uses: int = 0
        if phaetusa_fortification_level >= FortificationLevel.SEGMENT03:
            critical_damage_per_two_uses = 15

        self.value = critical_damage_per_two_uses * (uses_of_overwrite_trap // 2)
        self.modifier_type = ModifierType.ADDITIVE
        self.stat_type = SpecialAttribute.CRITICAL_DAMAGE
        self.tag = DamageTag.ALL


class EnergyDrink(Buff):
    """Basti buff"""

    display_name = "Energy Drink (Basti)"
    max_stack_count = 5
    stack_input_type = "select"

    def __init__(self, stacks: int, basti_fortification_level: FortificationLevel):
        if basti_fortification_level >= FortificationLevel.SEGMENT03:
            damage_boost_per_stack: int = 24
        elif basti_fortification_level >= FortificationLevel.SEGMENT02:
            damage_boost_per_stack: int = 12
        else:
            damage_boost_per_stack: int = 0

        self.value = damage_boost_per_stack * min(stacks, self.max_stack_count)
        self.modifier_type = ModifierType.ADDITIVE
        self.stat_type = SpecialAttribute.DAMAGE_BOOST
        self.tag = DamageTag.ALL


class InsigniaOfCamaraderie(Buff):
    """Basti buff"""

    display_name = "Insignia of Camaraderie (Basti)"
    max_stack_count = 1
    stack_input_type = "select"

    def __init__(self, basti_fortification_level: FortificationLevel):
        if basti_fortification_level >= FortificationLevel.SEGMENT03:
            self.value = 30
        else:
            self.value = 15

        self.modifier_type = ModifierType.ADDITIVE
        self.stat_type = SpecialAttribute.DAMAGE_BOOST
        self.tag = DamageTag.ALL


class CutieDetonation(Buff):
    """Attack buff granted to Basti and Cuties after each Cutie self-detonates."""

    display_name = "Cutie Detonation (Basti)"
    max_stack_count = 3
    stack_input_type = "input"

    def __init__(
        self, cuties_detonated: int, basti_fortification_level: FortificationLevel
    ):
        attack_boost_per_prior_detonation: int = 0

        if basti_fortification_level >= FortificationLevel.SEGMENT06:
            attack_boost_per_prior_detonation = 3

        self.value = attack_boost_per_prior_detonation * max(cuties_detonated, 0)

        self.modifier_type = ModifierType.MULTIPLICATIVE
        self.stat_type = StatType.ATTACK
        self.tag = DamageTag.ALL


class CoverMode(Buff):
    """Buff granted to allies when OTs-14 is in Cover Mode."""

    display_name = "Cover Mode (OTs-14)"
    max_stack_count = 175
    stack_input_type = "input"

    def __init__(
        self,
        ots14_initial_critical_damage: float,
        ots14_fortification_level: FortificationLevel,
    ):
        ots14_initial_critical_damage_to_buff_ratio: float = 0.10

        if ots14_fortification_level >= FortificationLevel.SEGMENT01:
            ots14_initial_critical_damage_to_buff_ratio = 0.15

        # Increase critical damage of all friendly units by x% of OTs-14's initial critical damage.
        self.value = int(
            ots14_initial_critical_damage * ots14_initial_critical_damage_to_buff_ratio
        )

        self.modifier_type = ModifierType.ADDITIVE
        self.stat_type = StatType.CRIT_DAMAGE
        self.tag = DamageTag.ALL


class DemolitionMode(Buff):
    """Buff granted to self when OTs-14 is in Demolition Mode."""

    display_name = "Demolition Mode (OTs-14)"
    max_stack_count = 17000
    stack_input_type = "input"

    def __init__(
        self,
        allies_combined_initial_attack: int,
        ots14_fortification_level: FortificationLevel,
    ):
        allies_combined_attack_to_buff_ratio: float = 0.10

        if ots14_fortification_level >= FortificationLevel.SEGMENT01:
            allies_combined_attack_to_buff_ratio = 0.15

        # Increase OTs-14's attack by x% of friendly Dolls' combined initial attack.
        self.value = int(
            allies_combined_initial_attack * allies_combined_attack_to_buff_ratio
        )

        self.modifier_type = ModifierType.ADDITIVE
        self.stat_type = StatType.ATTACK
        self.tag = DamageTag.ALL


class ReconstructionElectric(Buff):
    """Buff granted to friendly units when OTs-14 has Reconstruction: Electric."""

    display_name = "Reconstruction: Electric (OTs-14)"
    max_stack_count = 1
    stack_input_type = "input"

    def __init__(
        self,
        ots14_fortification_level: FortificationLevel,
    ):
        if ots14_fortification_level >= FortificationLevel.SEGMENT06:
            ...  # Currently no implementable difference at V6

        # Damage dealt by friendly units to targets under stability break is increased by 15%
        self.value = 15
        self.modifier_type = ModifierType.ADDITIVE
        self.stat_type = SpecialAttribute.DAMAGE_BOOST
        self.tag = DamageTag.STABILITY_BROKEN


class ReconstructionFreeze(Buff):
    """Buff granted to friendly units when OTs-14 has Reconstruction: Freeze."""

    display_name = "Reconstruction: Freeze (OTs-14)"
    max_stack_count = 1
    stack_input_type = "select"

    def __init__(self): ...

    def get_buffs(
        self,
        has_shield: bool,
        shield_value: int,
        ots14_fortification_level: FortificationLevel,
    ):
        ret: list[Buff] = []

        if has_shield:
            self.value = 15
            self.modifier_type = ModifierType.ADDITIVE
            self.stat_type = SpecialAttribute.DAMAGE_BOOST
            self.tag = DamageTag.ALL

            ret.append(self)

            if ots14_fortification_level >= FortificationLevel.SEGMENT06:
                # When friendly units deal damage, their attack is increased by 10% of their
                # Shield value.
                shield_value_to_attack_ratio: float = 0.10

                ret.append(
                    Buff(
                        value=int(shield_value * shield_value_to_attack_ratio),
                        modifier_type=ModifierType.ADDITIVE,
                        stat_type=StatType.ATTACK,
                        tag=DamageTag.ALL,
                    )
                )

        return ret


class ReconstructionHydro(Buff):
    """Buff granted to friendly units when OTs-14 has Reconstruction: Hydro."""

    display_name = "Reconstruction: Hydro (OTs-14)"
    max_stack_count = 4
    stack_input_type = "input"

    def __init__(self): ...

    def get_buffs(
        self,
        number_of_friendly_units: int,
        ots14_fortification_level: FortificationLevel,
    ):
        ret: list[Buff] = []

        if number_of_friendly_units > 0:
            damage_boost_per_friendly_unit: int = 2
            self.value = damage_boost_per_friendly_unit * max(
                0, number_of_friendly_units
            )
            self.modifier_type = ModifierType.ADDITIVE
            self.stat_type = SpecialAttribute.DAMAGE_BOOST
            self.tag = DamageTag.ALL

            ret.append(self)

            if ots14_fortification_level >= FortificationLevel.SEGMENT06:
                # Attack and Max HP of all friendly Physical Summon are increased by 1%
                # TODO: Implement Physical Summon check in the future.
                # For now, this will be enforced through the PHYSICAL_SUMMON tag on the buffs.

                ret.append(
                    Buff(
                        value=1,
                        modifier_type=ModifierType.MULTIPLICATIVE,
                        stat_type=StatType.ATTACK,
                        tag=DamageTag.PHYSICAL_SUMMON,
                    )
                )

                ret.append(
                    Buff(
                        value=1,
                        modifier_type=ModifierType.MULTIPLICATIVE,
                        stat_type=StatType.HEALTH,
                        tag=DamageTag.PHYSICAL_SUMMON,
                    )
                )

        return ret


class ReconstructionZero(Buff):
    """Buff granted to OTs-14 when she has Reconstruction: Zero."""

    display_name = "Reconstruction: Zero (OTs-14)"
    max_stack_count = 6
    stack_input_type = "select"

    def __init__(self): ...

    def get_buffs(
        self,
        is_in_demolition_mode: bool,
        initial_critical_damage: int,
        ots14_fortification_level: FortificationLevel,
    ):
        ret: list[Buff] = []
        attack_boost_magnitude: int = 30

        if ots14_fortification_level >= FortificationLevel.SEGMENT06:
            attack_boost_magnitude = 50

        # While under Demolition Mode, attack is increased by 30%
        if is_in_demolition_mode:
            self.value = attack_boost_magnitude
            self.modifier_type = ModifierType.MULTIPLICATIVE
            self.stat_type = StatType.ATTACK
            self.tag = DamageTag.ALL

        if ots14_fortification_level >= FortificationLevel.SEGMENT06:
            # For every 15% of initial critical damage, attacks ignore 5% of the target's defense.
            defense_ignore_per_interval: int = 5
            initial_critical_damage_interval: int = 15

            ret.append(
                Buff(
                    value=int(
                        defense_ignore_per_interval
                        * (initial_critical_damage // initial_critical_damage_interval)
                    ),
                    modifier_type=ModifierType.ADDITIVE,
                    stat_type=SpecialAttribute.DEFENSE_IGNORE,
                    tag=DamageTag.ALL,
                )
            )

        return ret


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


class ToxicQuagmire(Buff):
    """The effect when friendly units are on a Toxic Quagmire tile.
    TODO: Dandegate guide says "Corrosion Amplification" and "Hydro Amplification";
    I am taking this to be damage boost.
    """

    display_name = "Toxic Quagmire"
    max_stack_count = 1
    stack_input_type = "select"

    def __init__(self): ...

    def get_buffs(self, tile_ascension_level: int):
        self.value = 0
        self.modifier_type = ModifierType.ADDITIVE
        self.stat_type = SpecialAttribute.DAMAGE_BOOST
        self.tag = DamageTag.CORROSION

        ret: list[Buff] = [
            self,
        ]

        if tile_ascension_level >= 3:
            self.value = 10

            ret.append(
                Buff(
                    value=10,
                    modifier_type=ModifierType.ADDITIVE,
                    stat_type=SpecialAttribute.DAMAGE_BOOST,
                    tag=DamageTag.HYDRO,
                ),
            )

        return ret


class Thunderpool(Buff):
    """The effect when friendly units are on a Thunderpool tile."""

    display_name = "Thunderpool"
    max_stack_count = 1
    stack_input_type = "select"

    def __init__(self, tile_ascension_level: int):
        self.value = 0

        if tile_ascension_level >= 3:
            self.value = 10

        self.modifier_type = ModifierType.ADDITIVE
        self.stat_type = SpecialAttribute.DAMAGE_BOOST
        self.tag = DamageTag.PHYSICAL_SUMMON


class Crystalveil(Buff):
    """The effect when friendly units are on a Crystalveil tile."""

    display_name = "Crystalveil"
    max_stack_count = 1
    stack_input_type = "select"

    def __init__(self, tile_ascension_level: int):
        self.value = 0

        # TODO: This is supposed to be only for units with shields.
        # Applying this buff implies that the unit has a shield.
        if tile_ascension_level >= 3:
            self.value = 20

        self.modifier_type = ModifierType.ADDITIVE
        self.stat_type = SpecialAttribute.DAMAGE_BOOST
        self.tag = DamageTag.ALL


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


class Bullseye(Debuff):
    """Debuff applied by Cheyanne's S2. When attacked by Cheyanne, defense is decreased."""

    display_name = "Bullseye (Cheyanne)"
    max_stack_count = 1
    stack_input_type = "select"

    def __init__(self, cheyanne_fortification_level: FortificationLevel):
        """
        Arguments:
        cheyanne_fortification_level -- the Fortification Level of the Cheyanne applying this debuff
        """
        if cheyanne_fortification_level >= FortificationLevel.SEGMENT03:
            self.value = -100
        else:
            self.value = -50

        self.modifier_type = ModifierType.MULTIPLICATIVE
        self.stat_type = StatType.DEFENSE
        self.tag = DamageTag.PHYSICAL


class VindicatorsMark(Debuff):
    """Debuff applied by Asteria.
    The effect of adding all weapon weaknesses is not modeled here - it should
    manifest as adding a phase weakness exploited count to the target.
    The additional fixed damage dealt at V1 is not modeled here either."""

    display_name = "Vindicator's Mark (Asteria)"
    max_stack_count = 1
    stack_input_type = "select"

    def __init__(self): ...

    def get_buffs(self):
        """
        Arguments:
        """
        # When taking Physical damage, defense is reduced by 50%.
        self.value = -50
        self.modifier_type = ModifierType.MULTIPLICATIVE
        self.stat_type = StatType.DEFENSE
        self.tag = DamageTag.PHYSICAL

        ret: list[Debuff] = []
        ret.append(self)

        # Physical damage taken is increased by 20%.
        ret.append(
            Debuff(
                value=20,
                modifier_type=ModifierType.ADDITIVE,
                stat_type=SpecialAttribute.INCREASE_DAMAGE_TAKEN,
                tag=DamageTag.PHYSICAL,
            )
        )

        return ret


class Absolution(Debuff):
    """Debuff applied by Asteria.
    The stacking critical damage taken is modeled as a general increased damage taken - no critical damage taken check is performed.
    This will artificially inflate expected damage dealt for critical rates less than 100%.
    The parameter for Asteria being the attacker is so that this debuff can be applied even when Asteria is not the attacker.
    In those scenarios, the non-stacking Physical damage taken effect is still applied but the stacking effects are not.
    """

    display_name = "Absolution (Asteria)"
    max_stack_count = 6
    stack_input_type = "select"

    def __init__(self): ...

    def get_buffs(
        self,
        stacks: int,
        asteria_fortification_level: FortificationLevel,
        is_asteria_attacker: bool,
    ):
        """
        Arguments:
        stacks -- the number of stacks of this debuff, up to a maximum of 6
        asteria_fortification_level -- the Fortification Level of the Asteria applying this debuff
        is_asteria_attacker -- whether Asteria is the attacker in this scenario
        """
        ret: list[Debuff] = []

        # This debuff only exists at V5+
        if asteria_fortification_level >= FortificationLevel.SEGMENT05:
            # Physical damage taken increased by 30%.
            self.value = 30
            self.modifier_type = ModifierType.ADDITIVE
            self.stat_type = SpecialAttribute.INCREASE_DAMAGE_TAKEN
            self.tag = DamageTag.PHYSICAL

            ret: list[Debuff] = []
            ret.append(self)

            if is_asteria_attacker:
                critical_damage_taken_per_stack: int = 10

                critical_damage_taken_effect: Debuff = Debuff(
                    critical_damage_taken_per_stack
                    * min(max(0, stacks), Absolution.max_stack_count),
                    ModifierType.ADDITIVE,
                    SpecialAttribute.INCREASE_DAMAGE_TAKEN,
                    DamageTag.ALL,
                )

                ret.append(critical_damage_taken_effect)

                defense_reduction_per_stack: int = -10

                defense_reduction_effect: Debuff = Debuff(
                    defense_reduction_per_stack
                    * min(max(0, stacks), Absolution.max_stack_count),
                    ModifierType.MULTIPLICATIVE,
                    StatType.DEFENSE,
                    DamageTag.ALL,
                )

                ret.append(defense_reduction_effect)

        return ret


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


class CarmineEmblem(Debuff):
    """Sextans debuff"""

    display_name = "Carmine Emblem (Sextans)"
    max_stack_count = 3
    stack_input_type = "select"

    def __init__(self, stacks: int, sextans_fortification_level: FortificationLevel):
        """
        Arguments:
        stacks -- the number of stacks of this buff
        sextans_fortification_level -- the Fortification Level of the Sextans applying this debuff
        """
        melee_damage_taken_per_stack: int = 7
        maximum_debuff_value: int = 21

        if sextans_fortification_level == FortificationLevel.SEGMENT03:
            melee_damage_taken_per_stack = 10
            maximum_debuff_value = 30

        self.value = min(melee_damage_taken_per_stack * stacks, maximum_debuff_value)
        self.modifier_type = ModifierType.ADDITIVE
        self.stat_type = SpecialAttribute.INCREASE_DAMAGE_TAKEN
        self.tag = DamageTag.MELEE


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


class RangerMkII(Debuff):
    """All enemy units within a 5-tile radius of Ranger Mk.II take 15% increased Burn damage."""

    display_name = "Ranger Mk.II"
    max_stack_count = 1
    stack_input_type = "select"

    def __init__(self):
        """ """
        self.value = 15

        self.modifier_type = ModifierType.ADDITIVE
        self.stat_type = SpecialAttribute.INCREASE_DAMAGE_TAKEN
        self.tag = DamageTag.BURN


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


class Debility(Debuff):
    """Freeze debuff. Damage taken increased by 20%."""

    display_name = "Debility"
    max_stack_count = 1
    stack_input_type = "input"

    def __init__(self):
        self.value = 20
        self.modifier_type = ModifierType.ADDITIVE
        self.stat_type = SpecialAttribute.INCREASE_DAMAGE_TAKEN
        self.tag = DamageTag.ALL


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


class LockOn(Debuff):
    """Liushih debuff. When damaged by Liushih or enemy Physical Summon, defense is reduced by 30%."""

    display_name = "Lock On (Liushih)"
    max_stack_count = 1
    stack_input_type = "select"

    def __init__(self):
        self.value = -30
        self.modifier_type = ModifierType.MULTIPLICATIVE
        self.stat_type = StatType.DEFENSE


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


class DefenseDownIII(Debuff):
    """Reduce defense by 40%. Considered a defense buff."""

    display_name = "Defense Down III"
    max_stack_count = 1
    stack_input_type = "select"

    def __init__(self):
        self.value = -40
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


class RadioInvitationDefenseDown(Debuff):
    """From Lind's Fixed Key 3 - Radio Invitation. Reduce defense by 15%. Considered a defense buff."""

    display_name = "Radio Invitation: Defense Down"
    max_stack_count = 1
    stack_input_type = "select"

    def __init__(self):
        self.value = -15
        self.modifier_type = ModifierType.MULTIPLICATIVE
        self.stat_type = StatType.DEFENSE


class ScribbledFunnyFace(Debuff):
    """Increases Corrosion damage taken. Considered a Corrosion debuff."""

    display_name = "Scribbled Funny Face (Basti)"
    max_stack_count = 1
    stack_input_type = "select"

    def __init__(self, basti_fortification_level: FortificationLevel):
        if basti_fortification_level >= FortificationLevel.SEGMENT03:
            self.value = 30
        else:
            self.value = 15

        self.modifier_type = ModifierType.ADDITIVE
        self.stat_type = SpecialAttribute.INCREASE_DAMAGE_TAKEN
        self.tag = DamageTag.CORROSION


class ReconstructionCorrosion(Debuff):
    """Effect when OTs-14 has Reconstruction: Corrosion."""

    display_name = "Reconstruction: Corrosion (OTs-14)"
    max_stack_count = 1
    stack_input_type = "input"

    def __init__(
        self,
        number_of_debuffs: int,
        ots14_fortification_level: FortificationLevel,
    ):
        if ots14_fortification_level >= FortificationLevel.SEGMENT06:
            ...  # Currently no implementable difference at V6

        # When an enemy unit takes damage, damage taken is increased by 2% for each debuff held
        # by the enemy unit.
        increased_damage_taken_per_debuff: int = 2
        self.value = increased_damage_taken_per_debuff * max(0, number_of_debuffs)
        self.modifier_type = ModifierType.ADDITIVE
        self.stat_type = SpecialAttribute.INCREASE_DAMAGE_TAKEN
        self.tag = DamageTag.ALL


class Meltdown(Debuff):
    """After reaching 2 stacks, increases damage taken from basic attacks or active skills."""

    display_name = "Meltdown"
    max_stack_count = 1
    stack_input_type = "input"

    def __init__(self): ...

    def get_buffs(
        self,
    ):
        ret: list[Debuff] = []

        self.value = 45
        self.modifier_type = ModifierType.ADDITIVE
        self.stat_type = SpecialAttribute.INCREASE_DAMAGE_TAKEN
        self.tag = DamageTag.BASIC
        ret.append(self)

        ret.append(
            Debuff(self.value, self.modifier_type, self.stat_type, DamageTag.ACTIVE)
        )

        return ret


class ScaldingVapors(Debuff):
    """The increased damage taken effect when units are on a Scalding Vapors tile."""

    display_name = "Scalding Vapors"
    max_stack_count = 1
    stack_input_type = "input"

    def __init__(self, tile_ascension_level: int):
        self.value = 0

        # Only active at tile ascension level III
        if tile_ascension_level >= 3:
            self.value = 15

        self.modifier_type = ModifierType.ADDITIVE
        self.stat_type = SpecialAttribute.INCREASE_DAMAGE_TAKEN
        self.tag = DamageTag.ALL


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
