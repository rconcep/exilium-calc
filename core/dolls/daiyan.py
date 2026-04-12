from typing import override, ClassVar
from pydantic import Field

from core.types import (
    DamageTag,
    StatType,
    SpecialAttribute,
    ModifierType,
    Doll,
    FortificationLevel,
    SummonedUnit,
    PhysicalSummonedUnit,
)
from core.buffs import Buff
from core.combat import (
    DamageInstance,
    CombatAction,
)


class PluckingStrings(CombatAction):
    """Daiyan Basic Attack."""

    @override
    def execute(self, did_not_intercept_last_round: bool) -> DamageInstance:
        label: str = "Plucking Strings"
        base_potency: int = 80

        tags: set[DamageTag] = {
            DamageTag.ACTIVE,
            DamageTag.BASIC,
            DamageTag.MEDIUM_AMMO,
            DamageTag.TARGETED,
            DamageTag.PHYSICAL,
        }

        if did_not_intercept_last_round:
            base_potency += 150

        return DamageInstance(
            label=label,
            base_potency=base_potency,
            tags=tags,
            group_name="Plucking Strings",
        )


class AbsoluteTuning(CombatAction):
    """Daiyan S1."""

    @override
    def execute(self, did_not_intercept_last_round: bool) -> DamageInstance:
        label: str = "Absolute Tuning"
        base_potency: int = 150

        tags: set[DamageTag] = {
            DamageTag.ACTIVE,
            DamageTag.PHYSICAL,
            DamageTag.LIGHT_AMMO,
            DamageTag.TARGETED,
            DamageTag.CONFECTANCE,
        }

        if did_not_intercept_last_round:
            base_potency += 150

        return DamageInstance(
            label=label,
            base_potency=base_potency,
            tags=tags,
            group_name="Absolute Tuning",
        )


class EtherealResonance(CombatAction):
    """Daiyan Ultimate."""

    @override
    def execute(self, did_not_intercept_last_round: bool) -> DamageInstance:
        label: str = "Ethereal Resonance"
        base_potency: int = 190

        tags: set[DamageTag] = {
            DamageTag.ACTIVE,
            DamageTag.PHYSICAL,
            DamageTag.MEDIUM_AMMO,
            DamageTag.TARGETED,
            DamageTag.ULTIMATE,
        }

        if did_not_intercept_last_round:
            base_potency += 150

        return DamageInstance(
            label=label,
            base_potency=base_potency,
            tags=tags,
            group_name="Ethereal Resonance",
        )


class Interception(CombatAction):
    """Interception triggered before Daiyan takes targeted damage."""

    @override
    def execute(self, stacks_of_tuning: int) -> DamageInstance:
        label: str = "Interception"
        base_potency: int = 150

        tags: set[DamageTag] = {
            DamageTag.PASSIVE,
            DamageTag.INTERCEPTION,
            DamageTag.LIGHT_AMMO,
            DamageTag.TARGETED,
            DamageTag.PHYSICAL,
        }

        buffs_before: list[Buff] = []

        increased_damage_stacks_threshold: int = 3
        # If Daiyan has 3 or more stacks of Tuning when Interception triggers, increases damage dealt by 20%.
        if stacks_of_tuning >= increased_damage_stacks_threshold:
            buffs_before.append(
                Buff(
                    value=20,
                    modifier_type=ModifierType.ADDITIVE,
                    stat_type=SpecialAttribute.DAMAGE_BOOST,
                    tag=DamageTag.INTERCEPTION,
                )
            )

        return DamageInstance(
            label=label,
            base_potency=base_potency,
            tags=tags,
            group_name="Interception",
            buffs_before=buffs_before,
        )


class InterceptionV4(CombatAction):
    """Interception triggered before Daiyan takes targeted damage (V4)."""

    @override
    def execute(self, stacks_of_tuning: int) -> DamageInstance:
        label: str = "Interception"
        base_potency: int = 180

        tags: set[DamageTag] = {
            DamageTag.PASSIVE,
            DamageTag.INTERCEPTION,
            DamageTag.LIGHT_AMMO,
            DamageTag.TARGETED,
            DamageTag.PHYSICAL,
        }

        buffs_before: list[Buff] = []

        increased_damage_stacks_threshold_v4: int = 5
        increased_damage_stacks_threshold: int = 3

        # If Daiyan has 5 or more stacks of Tuning when Interception triggers, increases damage dealt by 40% instead.
        if stacks_of_tuning >= increased_damage_stacks_threshold_v4:
            buff_value: int = 40
        elif stacks_of_tuning >= increased_damage_stacks_threshold:
            buff_value: int = 20
        else:
            buff_value: int = 0

        buffs_before.append(
            Buff(
                value=buff_value,
                modifier_type=ModifierType.ADDITIVE,
                stat_type=SpecialAttribute.DAMAGE_BOOST,
                tag=DamageTag.INTERCEPTION,
            )
        )

        return DamageInstance(
            label=label,
            base_potency=base_potency,
            tags=tags,
            group_name="Interception",
            buffs_before=buffs_before,
        )


class FlowingMelodyOfTheClouds(CombatAction):
    """Additional attack granted by Daiyan's Expansion Key - Flowing Melody of the Clouds (Tier 2).
    Triggered by using the Ultimate skill Ethereal Resonance."""

    @override
    def execute(self, stacks_of_permanent_tuning: int) -> DamageInstance:
        label: str = f"Flowing Melody of the Clouds ({stacks_of_permanent_tuning})"
        base_potency: int = 0

        tags: set[DamageTag] = {
            DamageTag.TARGETED,
            DamageTag.PHYSICAL,
            DamageTag.ACTIVE,
        }
        if stacks_of_permanent_tuning > 0:
            potency_per_stack: int = 100
            max_tuning_stacks: int = 10
            base_potency += potency_per_stack * min(
                stacks_of_permanent_tuning, max_tuning_stacks
            )

        return DamageInstance(
            label=label,
            base_potency=base_potency,
            tags=tags,
            group_name="Flowing Melody of the Clouds",
        )


class Daiyan(Doll):
    """Daiyan."""

    name: str = "Daiyan"
    irrelevant_damage_tags: ClassVar[set[DamageTag]] = set(
        [
            DamageTag.CORROSION,
            DamageTag.BURN,
            DamageTag.FREEZE,
            DamageTag.HYDRO,
            DamageTag.PHASE,
            DamageTag.ELECTRIC,
            DamageTag.MELEE,
            DamageTag.HEAVY_AMMO,
            DamageTag.SHOTGUN_AMMO,
            DamageTag.SUPPORT_ACTION,
            DamageTag.COUNTERATTACK,
            DamageTag.FIXED,
            DamageTag.PHYSICAL_SUMMON,
        ]
    )

    plucking_strings: CombatAction = Field(default_factory=PluckingStrings)
    absolute_tuning: CombatAction = Field(default_factory=AbsoluteTuning)
    ethereal_resonance: CombatAction = Field(default_factory=EtherealResonance)
    interception: CombatAction = Field(default_factory=Interception)
    flowing_melody_of_the_clouds: CombatAction = Field(
        default_factory=FlowingMelodyOfTheClouds
    )

    def set_to_v0(self) -> None:
        """Sets Fortification Level to Segment00."""
        self.plucking_strings: CombatAction = PluckingStrings()
        self.absolute_tuning: CombatAction = AbsoluteTuning()
        self.ethereal_resonance: CombatAction = EtherealResonance()
        self.interception: CombatAction = Interception()
        self.flowing_melody_of_the_clouds: CombatAction = FlowingMelodyOfTheClouds()

    def set_to_v4(self) -> None:
        """Sets Fortification Level to Segment02."""
        self.set_to_v0()

        self.interception: CombatAction = InterceptionV4()

    @override
    def set_fortification_level(self, level: FortificationLevel):
        self.fortification_level = level
        match level:
            case FortificationLevel.SEGMENT00:
                self.set_to_v0()
            case FortificationLevel.SEGMENT01:
                self.set_to_v0()
            case FortificationLevel.SEGMENT02:
                self.set_to_v0()
            case FortificationLevel.SEGMENT03:
                self.set_to_v0()
            case FortificationLevel.SEGMENT04:
                self.set_to_v4()
            case FortificationLevel.SEGMENT05:
                self.set_to_v4()
            case FortificationLevel.SEGMENT06:
                self.set_to_v4()
