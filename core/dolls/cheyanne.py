from typing import override, ClassVar
from pydantic import Field

from core.types import (
    DamageTag,
    ModifierType,
    SpecialAttribute,
    Doll,
    FortificationLevel,
    StatType,
    SummonedUnit,
)
from core.buffs import Buff
from core.combat import DamageInstance, CombatAction


# Analytical Value
# V1: When dealing damage, for every 10% of the target's Analytical Value, critical damage is increased by 5%. (Passive)
# Innate: When Cheyanne attacks, if the target's Analytical Value is >= 50%, critical damage is increased by 30%. If < 50%, critical damage is increased by 10%
def get_analytical_value_buff(analytical_value: int) -> Buff:
    """Returns the critical damage buff corresponding to the effect of Analytical Value.

    Arguments:
        analytical_value: The target's Analytical Value as a percentage (0-100).
    """
    return Buff(
        value=30 if analytical_value >= 50 else 10,
        modifier_type=ModifierType.ADDITIVE,
        stat_type=SpecialAttribute.CRITICAL_DAMAGE,
        tag=DamageTag.ALL,
    )


def get_analytical_value_buffV1(analytical_value: int) -> Buff:
    """Returns the critical damage buff corresponding to the effect of Analytical Value
    in addition to the effect from Cheyanne's passive.

    Arguments:
        analytical_value: The target's Analytical Value as a percentage (0-100).
    """
    passive_buff_value: int = (analytical_value // 10) * 5

    return Buff(
        value=(30 if analytical_value >= 50 else 10) + passive_buff_value,
        modifier_type=ModifierType.ADDITIVE,
        stat_type=SpecialAttribute.CRITICAL_DAMAGE,
        tag=DamageTag.ALL,
    )


class PlayingToPotential(CombatAction):
    """Cheyanne basic attack."""

    @override
    def execute(self, analytical_value: int) -> DamageInstance:
        label: str = "Playing to Potential"
        base_potency: int = 80
        tags: set[DamageTag] = {
            DamageTag.ACTIVE,
            DamageTag.BASIC,
            DamageTag.HEAVY_AMMO,
            DamageTag.TARGETED,
            DamageTag.PHYSICAL,
        }

        analytical_value_buff: Buff = get_analytical_value_buff(analytical_value)

        return DamageInstance(
            label=label,
            base_potency=base_potency,
            tags=tags,
            buffs_before=[analytical_value_buff],
            group_name="Playing to Potential",
        )


class PlayingToPotentialV1(CombatAction):
    """Cheyanne basic attack (V1)."""

    @override
    def execute(self, analytical_value: int) -> DamageInstance:
        label: str = "Playing to Potential"
        base_potency: int = 80
        tags: set[DamageTag] = {
            DamageTag.ACTIVE,
            DamageTag.BASIC,
            DamageTag.HEAVY_AMMO,
            DamageTag.TARGETED,
            DamageTag.PHYSICAL,
        }

        analytical_value_buff: Buff = get_analytical_value_buffV1(analytical_value)

        return DamageInstance(
            label=label,
            base_potency=base_potency,
            tags=tags,
            buffs_before=[analytical_value_buff],
            group_name="Playing to Potential",
        )


class SteadfastPursuit(CombatAction):
    """Cheyanne S2."""

    @override
    def execute(self, analytical_value: int) -> DamageInstance:
        label: str = "Steadfast Pursuit"
        base_potency: int = 80
        tags: set[DamageTag] = {
            DamageTag.ACTIVE,
            DamageTag.HEAVY_AMMO,
            DamageTag.TARGETED,
            DamageTag.PHYSICAL,
        }

        analytical_value_buff: Buff = get_analytical_value_buff(analytical_value)

        return DamageInstance(
            label=label,
            base_potency=base_potency,
            tags=tags,
            group_name="Steadfast Pursuit",
            buffs_before=[analytical_value_buff],
        )


class SteadfastPursuitV1(CombatAction):
    """Cheyanne S2 (V1)."""

    @override
    def execute(self, analytical_value: int) -> DamageInstance:
        label: str = "Steadfast Pursuit"
        base_potency: int = 80
        tags: set[DamageTag] = {
            DamageTag.ACTIVE,
            DamageTag.HEAVY_AMMO,
            DamageTag.TARGETED,
            DamageTag.PHYSICAL,
        }

        analytical_value_buff: Buff = get_analytical_value_buffV1(analytical_value)

        return DamageInstance(
            label=label,
            base_potency=base_potency,
            tags=tags,
            group_name="Steadfast Pursuit",
            buffs_before=[analytical_value_buff],
        )


class PiercingTheHeavensIntoTheSun(CombatAction):
    """Cheyanne S3."""

    @override
    def execute(
        self,
        target_has_bullseye: bool,
        few_enemies_with_low_analytical_value: bool,
        stacks_of_prepared_stance: int,
    ) -> DamageInstance:
        label: str = "Piercing the Heavens into the Sun"
        base_potency: int = 200
        tags: set[DamageTag] = {
            DamageTag.ACTIVE,
            DamageTag.PHYSICAL,
            DamageTag.HEAVY_AMMO,
            DamageTag.TARGETED,
            DamageTag.CONFECTANCE,
        }

        buffs_before: list[Buff] = []

        # Resets the target's Analytical Value to 100%
        reset_analytical_value: int = 100
        analytical_value_buff: Buff = get_analytical_value_buff(reset_analytical_value)
        buffs_before.append(analytical_value_buff)

        # If the target has Bullseye, then the critical damage is increased by 30%.
        if target_has_bullseye:
            buffs_before.append(
                Buff(
                    value=30,
                    modifier_type=ModifierType.ADDITIVE,
                    stat_type=SpecialAttribute.CRITICAL_DAMAGE,
                    tag=DamageTag.ALL,
                )
            )

        return DamageInstance(
            label=label,
            base_potency=base_potency,
            tags=tags,
            group_name="Piercing the Heavens into the Sun",
            buffs_before=buffs_before,
        )


class PiercingTheHeavensIntoTheSunV1(CombatAction):
    """Cheyanne S3 (V1)."""

    @override
    def execute(
        self,
        target_has_bullseye: bool,
        few_enemies_with_low_analytical_value: bool,
        stacks_of_prepared_stance: int,
    ) -> DamageInstance:
        label: str = "Piercing the Heavens into the Sun"
        base_potency: int = 200
        tags: set[DamageTag] = {
            DamageTag.ACTIVE,
            DamageTag.PHYSICAL,
            DamageTag.HEAVY_AMMO,
            DamageTag.TARGETED,
            DamageTag.CONFECTANCE,
        }

        buffs_before: list[Buff] = []

        # Resets the target's Analytical Value to 100%
        reset_analytical_value: int = 100
        analytical_value_buff: Buff = get_analytical_value_buffV1(
            reset_analytical_value
        )
        buffs_before.append(analytical_value_buff)

        # If the target has Bullseye, then the critical damage is increased by 30%.
        if target_has_bullseye:
            buffs_before.append(
                Buff(
                    value=30,
                    modifier_type=ModifierType.ADDITIVE,
                    stat_type=SpecialAttribute.CRITICAL_DAMAGE,
                    tag=DamageTag.ALL,
                )
            )

        return DamageInstance(
            label=label,
            base_potency=base_potency,
            tags=tags,
            group_name="Piercing the Heavens into the Sun",
            buffs_before=buffs_before,
        )


class PiercingTheHeavensIntoTheSunV2(CombatAction):
    """Cheyanne S3 (V2)."""

    @override
    def execute(
        self,
        target_has_bullseye: bool,
        few_enemies_with_low_analytical_value: bool,
        stacks_of_prepared_stance: int,
    ) -> DamageInstance:
        label: str = "Piercing the Heavens into the Sun"
        base_potency: int = 280
        tags: set[DamageTag] = {
            DamageTag.ACTIVE,
            DamageTag.PHYSICAL,
            DamageTag.HEAVY_AMMO,
            DamageTag.TARGETED,
            DamageTag.CONFECTANCE,
        }

        buffs_before: list[Buff] = []

        # Resets the target's Analytical Value to 100%
        reset_analytical_value: int = 100
        analytical_value_buff: Buff = get_analytical_value_buffV1(
            reset_analytical_value
        )
        buffs_before.append(analytical_value_buff)

        # If the target has Bullseye, then the critical damage is increased by 30% and 50% of their defense is ignored.
        if target_has_bullseye:
            buffs_before.append(
                Buff(
                    value=30,
                    modifier_type=ModifierType.ADDITIVE,
                    stat_type=SpecialAttribute.CRITICAL_DAMAGE,
                    tag=DamageTag.ALL,
                )
            )

            buffs_before.append(
                Buff(
                    value=50,
                    modifier_type=ModifierType.ADDITIVE,
                    stat_type=SpecialAttribute.DEFENSE_IGNORE,
                    tag=DamageTag.ALL,
                )
            )

        return DamageInstance(
            label=label,
            base_potency=base_potency,
            tags=tags,
            group_name="Piercing the Heavens into the Sun",
            buffs_before=buffs_before,
        )


class PiercingTheHeavensIntoTheSunV5(CombatAction):
    """Cheyanne S3 (V5)."""

    @override
    def execute(
        self,
        target_has_bullseye: bool,
        few_enemies_with_low_analytical_value: bool,
        stacks_of_prepared_stance: int,
    ) -> DamageInstance:
        label: str = "Piercing the Heavens into the Sun"
        base_potency: int = 330
        tags: set[DamageTag] = {
            DamageTag.ACTIVE,
            DamageTag.PHYSICAL,
            DamageTag.HEAVY_AMMO,
            DamageTag.TARGETED,
            DamageTag.CONFECTANCE,
        }

        # If there are 3 or less enemies on the field with Analytical Value less than 50%, the damage multiplier is increased to 380%.
        if few_enemies_with_low_analytical_value:
            base_potency = 380

        buffs_before: list[Buff] = []

        # Resets the target's Analytical Value to 100%
        reset_analytical_value: int = 100
        analytical_value_buff: Buff = get_analytical_value_buffV1(
            reset_analytical_value
        )
        buffs_before.append(analytical_value_buff)

        # If the target has Bullseye, then the critical damage is increased by 30% and 50% of their defense is ignored.
        if target_has_bullseye:
            buffs_before.append(
                Buff(
                    value=30,
                    modifier_type=ModifierType.ADDITIVE,
                    stat_type=SpecialAttribute.CRITICAL_DAMAGE,
                    tag=DamageTag.ALL,
                )
            )

            buffs_before.append(
                Buff(
                    value=50,
                    modifier_type=ModifierType.ADDITIVE,
                    stat_type=SpecialAttribute.DEFENSE_IGNORE,
                    tag=DamageTag.ALL,
                )
            )

        return DamageInstance(
            label=label,
            base_potency=base_potency,
            tags=tags,
            group_name="Piercing the Heavens into the Sun",
            buffs_before=buffs_before,
        )


class PiercingTheHeavensIntoTheSunV6(CombatAction):
    """Cheyanne S3 (V6)."""

    @override
    def execute(
        self,
        target_has_bullseye: bool,
        few_enemies_with_low_analytical_value: bool,
        stacks_of_prepared_stance: int,
    ) -> DamageInstance:
        label: str = "Piercing the Heavens into the Sun"
        base_potency: int = 330
        tags: set[DamageTag] = {
            DamageTag.ACTIVE,
            DamageTag.PHYSICAL,
            DamageTag.HEAVY_AMMO,
            DamageTag.TARGETED,
            DamageTag.CONFECTANCE,
        }

        # If there are 3 or less enemies on the field with Analytical Value less than 50%, the damage multiplier is increased to 380%.
        if few_enemies_with_low_analytical_value:
            base_potency = 380

        # For each stack of Prepared Stance, increases damage multiplier by 80%. (Up to 3 stacks)
        max_stacks_of_prepared_stance: int = 3
        potency_per_stack_of_prepared_stance: int = 80

        if stacks_of_prepared_stance > 0:
            base_potency += potency_per_stack_of_prepared_stance * min(
                stacks_of_prepared_stance, max_stacks_of_prepared_stance
            )

        buffs_before: list[Buff] = []

        # Resets the target's Analytical Value to 100%
        reset_analytical_value: int = 100
        analytical_value_buff: Buff = get_analytical_value_buffV1(
            reset_analytical_value
        )
        buffs_before.append(analytical_value_buff)

        # If the target has Bullseye, then the critical damage is increased by 30% and 50% of their defense is ignored.
        if target_has_bullseye:
            buffs_before.append(
                Buff(
                    value=30,
                    modifier_type=ModifierType.ADDITIVE,
                    stat_type=SpecialAttribute.CRITICAL_DAMAGE,
                    tag=DamageTag.ALL,
                )
            )

            buffs_before.append(
                Buff(
                    value=50,
                    modifier_type=ModifierType.ADDITIVE,
                    stat_type=SpecialAttribute.DEFENSE_IGNORE,
                    tag=DamageTag.ALL,
                )
            )

        return DamageInstance(
            label=label,
            base_potency=base_potency,
            tags=tags,
            group_name="Piercing the Heavens into the Sun",
            buffs_before=buffs_before,
        )


class ThinkBeforeYouAct(CombatAction):
    """Passive attack from Cheyanne. Triggered when an enemy completes its turn or when an enemy with
    Bullseye ends its turn and Cheyanne has Fixed Key 6 - Full Attention equipped."""

    @override
    def execute(self, analytical_value: int) -> DamageInstance:
        label: str = "Think Before You Act"
        base_potency: int = 120
        tags: set[DamageTag] = {
            DamageTag.PASSIVE,
            DamageTag.HEAVY_AMMO,
            DamageTag.TARGETED,
            DamageTag.PHYSICAL,
        }

        buffs_before: list[Buff] = []

        # If the target has a Analytical Value of 50% or greater, then the damage multiplier is increased to 180%.
        if analytical_value >= 50:
            base_potency = 180

        analytical_value_buff: Buff = get_analytical_value_buff(analytical_value)
        buffs_before.append(analytical_value_buff)

        return DamageInstance(
            label=label,
            base_potency=base_potency,
            tags=tags,
            group_name="Think Before You Act",
            buffs_before=buffs_before,
        )


class ThinkBeforeYouActV1(CombatAction):
    """Passive attack from Cheyanne. Triggered when an enemy completes its turn or when an enemy with
    Bullseye ends its turn and Cheyanne has Fixed Key 6 - Full Attention equipped."""

    @override
    def execute(self, analytical_value: int) -> DamageInstance:
        label: str = "Think Before You Act"
        base_potency: int = 120
        tags: set[DamageTag] = {
            DamageTag.PASSIVE,
            DamageTag.HEAVY_AMMO,
            DamageTag.TARGETED,
            DamageTag.PHYSICAL,
        }

        buffs_before: list[Buff] = []

        # If the target has a Analytical Value of 50% or greater, then the damage multiplier is increased to 180%.
        if analytical_value >= 50:
            base_potency = 180

        analytical_value_buff: Buff = get_analytical_value_buffV1(analytical_value)
        buffs_before.append(analytical_value_buff)

        return DamageInstance(
            label=label,
            base_potency=base_potency,
            tags=tags,
            group_name="Think Before You Act",
            buffs_before=buffs_before,
        )


class ThinkBeforeYouActV6(CombatAction):
    """Passive attack from Cheyanne. Triggered when an enemy completes its turn or when an enemy with
    Bullseye ends its turn and Cheyanne has Fixed Key 6 - Full Attention equipped."""

    @override
    def execute(self, analytical_value: int) -> DamageInstance:
        label: str = "Think Before You Act"
        base_potency: int = 160
        tags: set[DamageTag] = {
            DamageTag.PASSIVE,
            DamageTag.HEAVY_AMMO,
            DamageTag.TARGETED,
            DamageTag.PHYSICAL,
        }

        buffs_before: list[Buff] = []

        # If the target has a Analytical Value of 50% or greater, then the damage multiplier is increased to 220%.
        if analytical_value >= 50:
            base_potency = 220

        analytical_value_buff: Buff = get_analytical_value_buffV1(analytical_value)
        buffs_before.append(analytical_value_buff)

        return DamageInstance(
            label=label,
            base_potency=base_potency,
            tags=tags,
            group_name="Think Before You Act",
            buffs_before=buffs_before,
        )


class Cheyanne(Doll):
    """Cheyanne."""

    name: str = "Cheyanne"
    irrelevant_damage_tags: ClassVar[set[DamageTag]] = set(
        [
            DamageTag.CORROSION,
            DamageTag.HYDRO,
            DamageTag.BURN,
            DamageTag.ELECTRIC,
            DamageTag.FREEZE,
            DamageTag.PHASE,
            DamageTag.MELEE,
            DamageTag.LIGHT_AMMO,
            DamageTag.MEDIUM_AMMO,
            DamageTag.SHOTGUN_AMMO,
            DamageTag.SUPPORT_ACTION,
            DamageTag.INTERCEPTION,
            DamageTag.COUNTERATTACK,
            DamageTag.AREA_OF_EFFECT,
            DamageTag.ULTIMATE,
            DamageTag.PHYSICAL_SUMMON,
            DamageTag.FIXED,
        ]
    )

    playing_to_potential: CombatAction = PlayingToPotential()
    steadfast_pursuit: CombatAction = SteadfastPursuit()
    piercing_the_heavens_into_the_sun: CombatAction = PiercingTheHeavensIntoTheSun()
    think_before_you_act: CombatAction = ThinkBeforeYouAct()

    def set_to_v0(self) -> None:
        """Sets Fortification Level to Segment00."""
        self.playing_to_potential = PlayingToPotential()
        self.steadfast_pursuit = SteadfastPursuit()
        self.piercing_the_heavens_into_the_sun = PiercingTheHeavensIntoTheSun()
        self.think_before_you_act = ThinkBeforeYouAct()

    def set_to_v1(self) -> None:
        """Sets Fortification Level to Segment01."""
        self.set_to_v0()

        self.playing_to_potential = PlayingToPotentialV1()
        self.steadfast_pursuit = SteadfastPursuitV1()
        self.piercing_the_heavens_into_the_sun = PiercingTheHeavensIntoTheSunV1()
        self.think_before_you_act = ThinkBeforeYouActV1()

    def set_to_v2(self) -> None:
        """Sets Fortification Level to Segment02."""
        self.set_to_v1()

        self.piercing_the_heavens_into_the_sun = PiercingTheHeavensIntoTheSunV2()

    def set_to_v5(self) -> None:
        """Sets Fortification Level to Segment05."""
        self.set_to_v2()

        self.piercing_the_heavens_into_the_sun = PiercingTheHeavensIntoTheSunV5()

    def set_to_v6(self) -> None:
        """Sets Fortification Level to Segment06."""
        self.set_to_v5()

        self.piercing_the_heavens_into_the_sun = PiercingTheHeavensIntoTheSunV6()
        self.think_before_you_act = ThinkBeforeYouActV6()

    @override
    def set_fortification_level(self, level: FortificationLevel):
        self.fortification_level = level
        match level:
            case FortificationLevel.SEGMENT00:
                self.set_to_v0()
            case FortificationLevel.SEGMENT01:
                self.set_to_v1()
            case FortificationLevel.SEGMENT02:
                self.set_to_v2()
            case FortificationLevel.SEGMENT03:
                self.set_to_v2()
            case FortificationLevel.SEGMENT04:
                self.set_to_v2()
            case FortificationLevel.SEGMENT05:
                self.set_to_v5()
            case FortificationLevel.SEGMENT06:
                self.set_to_v6()
