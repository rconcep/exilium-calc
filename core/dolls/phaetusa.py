from typing import Any, override, ClassVar
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


BLOOD_OATH_DAMAGE_MULTIPLIER_INCREASE: int = 200
MAX_STACKS_OF_BLADE_RESONANCE: int = 3


class DualSlash(CombatAction):
    """Phaetusa Basic Attack."""

    @override
    def execute(self, has_blood_oath: bool) -> DamageInstance:
        label: str = "Dual Slash"
        base_potency: int = 80

        tags: set[DamageTag] = {
            DamageTag.ACTIVE,
            DamageTag.BASIC,
            DamageTag.MELEE,
            DamageTag.TARGETED,
            DamageTag.PHYSICAL,
        }

        if has_blood_oath:
            base_potency += BLOOD_OATH_DAMAGE_MULTIPLIER_INCREASE

        return DamageInstance(
            label=label,
            base_potency=base_potency,
            tags=tags,
            group_name="Dual Slash",
        )


class DoubleDescent(CombatAction):
    """Phaetusa S1."""

    @override
    def execute(self, has_blood_oath: bool) -> DamageInstance:
        label: str = "Double Descent"
        base_potency: int = 90

        tags: set[DamageTag] = {
            DamageTag.ACTIVE,
            DamageTag.CORROSION,
            DamageTag.PHASE,
            DamageTag.MELEE,
            DamageTag.AREA_OF_EFFECT,
        }

        if has_blood_oath:
            base_potency += BLOOD_OATH_DAMAGE_MULTIPLIER_INCREASE

        return DamageInstance(
            label=label,
            base_potency=base_potency,
            tags=tags,
            group_name="Double Descent",
        )


class DoubleDescentV2(CombatAction):
    """Phaetusa S1 (V2)."""

    @override
    def execute(self, has_blood_oath: bool) -> DamageInstance:
        label: str = "Double Descent"
        base_potency: int = 120

        tags: set[DamageTag] = {
            DamageTag.ACTIVE,
            DamageTag.CORROSION,
            DamageTag.PHASE,
            DamageTag.MELEE,
            DamageTag.AREA_OF_EFFECT,
        }

        if has_blood_oath:
            base_potency += BLOOD_OATH_DAMAGE_MULTIPLIER_INCREASE

        return DamageInstance(
            label=label,
            base_potency=base_potency,
            tags=tags,
            group_name="Double Descent",
        )


class TwinParadise(CombatAction):
    """Phaetusa Ultimate."""

    @override
    def execute(
        self, has_blood_oath: bool, stacks_of_blade_resonance: int
    ) -> DamageInstance:
        label: str = f"Twin Paradise ({stacks_of_blade_resonance})"
        base_potency: int = 90

        tags: set[DamageTag] = {
            DamageTag.ACTIVE,
            DamageTag.CORROSION,
            DamageTag.PHASE,
            DamageTag.MELEE,
            DamageTag.AREA_OF_EFFECT,
            DamageTag.ULTIMATE,
        }

        buffs_before: list[Buff] = []

        if has_blood_oath:
            base_potency += BLOOD_OATH_DAMAGE_MULTIPLIER_INCREASE

        if stacks_of_blade_resonance > 0:
            # Consumes all stacks of Blade Resonance: for each stack consumed,
            # increase the damage multiplier of this skill by 10% and the total damage dealt by 1x.
            # => Add 10 to base potency per stack then multiply the base potency by (1 + number of stacks)
            # to get the final potency.
            potency_per_stack: int = 10
            base_potency += (
                min(stacks_of_blade_resonance, MAX_STACKS_OF_BLADE_RESONANCE)
                * potency_per_stack
            )
            base_potency *= 1 + min(
                stacks_of_blade_resonance, MAX_STACKS_OF_BLADE_RESONANCE
            )

        return DamageInstance(
            label=label,
            base_potency=base_potency,
            tags=tags,
            group_name="Twin Paradise",
            buffs_before=buffs_before,
        )


class TwinParadiseV4(CombatAction):
    """Phaetusa Ultimate (V4)."""

    @override
    def execute(
        self, has_blood_oath: bool, stacks_of_blade_resonance: int
    ) -> DamageInstance:
        label: str = f"Twin Paradise ({stacks_of_blade_resonance})"
        base_potency: int = 120

        tags: set[DamageTag] = {
            DamageTag.ACTIVE,
            DamageTag.CORROSION,
            DamageTag.PHASE,
            DamageTag.MELEE,
            DamageTag.AREA_OF_EFFECT,
            DamageTag.ULTIMATE,
        }

        buffs_before: list[Buff] = []

        if has_blood_oath:
            base_potency += BLOOD_OATH_DAMAGE_MULTIPLIER_INCREASE

        if stacks_of_blade_resonance > 0:
            # Consumes all stacks of Blade Resonance: for each stack consumed,
            # increase the damage multiplier of this skill by 10% and the total damage dealt by 1x.
            # => Add 10 to base potency per stack then multiply the base potency by (1 + number of stacks)
            # to get the final potency.
            potency_per_stack: int = 20
            base_potency += (
                min(stacks_of_blade_resonance, MAX_STACKS_OF_BLADE_RESONANCE)
                * potency_per_stack
            )
            base_potency *= 1 + min(
                stacks_of_blade_resonance, MAX_STACKS_OF_BLADE_RESONANCE
            )

        return DamageInstance(
            label=label,
            base_potency=base_potency,
            tags=tags,
            group_name="Twin Paradise",
            buffs_before=buffs_before,
        )


class LaceratingWound(CombatAction):
    """Effect from Lacerating Wound debuff applied from Replication Trap.
    When taking damage, if the attacker used a blade, take an additional instance of damage equal to 40% of the original damage.
    Modeled as a separate instance taking in the original damage instance potency and using 40% of it.
    """

    @override
    def execute(self, original_damage_instance_potency: int) -> DamageInstance:
        label: str = f"Lacerating Wound ({original_damage_instance_potency})"
        base_potency: int = int(original_damage_instance_potency * 0.4)

        tags: set[DamageTag] = {
            DamageTag.PASSIVE,
            DamageTag.CORROSION,
            DamageTag.PHASE,
            DamageTag.AREA_OF_EFFECT,
        }

        return DamageInstance(
            label=label,
            base_potency=base_potency,
            tags=tags,
            group_name="Lacerating Wound",
        )


class SupportAction(CombatAction):
    """Phaetusa Support Action."""

    @override
    def execute(self) -> DamageInstance:
        label: str = "Support Action"
        base_potency: int = 90

        tags: set[DamageTag] = {
            DamageTag.PASSIVE,
            DamageTag.SUPPORT_ACTION,
            DamageTag.MELEE,
            DamageTag.CORROSION,
            DamageTag.PHASE,
            DamageTag.AREA_OF_EFFECT,
        }

        return DamageInstance(
            label=label,
            base_potency=base_potency,
            tags=tags,
            group_name="Support Action",
        )


class SupportActionV5(CombatAction):
    """Phaetusa Support Action (V5)."""

    @override
    def execute(self) -> DamageInstance:
        label: str = "Support Action"
        base_potency: int = 120

        tags: set[DamageTag] = {
            DamageTag.PASSIVE,
            DamageTag.SUPPORT_ACTION,
            DamageTag.MELEE,
            DamageTag.CORROSION,
            DamageTag.PHASE,
            DamageTag.AREA_OF_EFFECT,
        }

        return DamageInstance(
            label=label,
            base_potency=base_potency,
            tags=tags,
            group_name="Support Action",
        )


class Phaetusa(Doll):
    """Phaetusa."""

    name: str = "Phaetusa"
    irrelevant_damage_tags: ClassVar[set[DamageTag]] = set(
        [
            DamageTag.BURN,
            DamageTag.FREEZE,
            DamageTag.HYDRO,
            DamageTag.ELECTRIC,
            DamageTag.LIGHT_AMMO,
            DamageTag.MEDIUM_AMMO,
            DamageTag.HEAVY_AMMO,
            DamageTag.SHOTGUN_AMMO,
            DamageTag.COUNTERATTACK,
            DamageTag.INTERCEPTION,
            DamageTag.FIXED,
            DamageTag.PHYSICAL_SUMMON,
        ]
    )

    dual_slash: CombatAction = Field(default_factory=DualSlash)
    double_descent: CombatAction = Field(default_factory=DoubleDescent)
    twin_paradise: CombatAction = Field(default_factory=TwinParadise)
    support_action: CombatAction = Field(default_factory=SupportAction)
    lacerating_wound: CombatAction = Field(default_factory=LaceratingWound)

    def set_to_v0(self) -> None:
        """Sets Fortification Level to Segment00."""
        self.dual_slash = DualSlash()
        self.double_descent = DoubleDescent()
        self.twin_paradise = TwinParadise()
        self.support_action = SupportAction()
        self.lacerating_wound = LaceratingWound()

    def set_to_v2(self) -> None:
        """Sets Fortification Level to Segment02."""
        self.set_to_v0()

        self.double_descent = DoubleDescentV2()

    def set_to_v4(self) -> None:
        """Sets Fortification Level to Segment04."""
        self.set_to_v2()

        self.twin_paradise = TwinParadiseV4()

    def set_to_v5(self) -> None:
        """Sets Fortification Level to Segment05."""
        self.set_to_v4()

        self.support_action = SupportActionV5()

    @override
    def set_fortification_level(self, level: FortificationLevel) -> None:
        self.fortification_level = level
        match level:
            case FortificationLevel.SEGMENT00:
                self.set_to_v0()
            case FortificationLevel.SEGMENT01:
                self.set_to_v0()
            case FortificationLevel.SEGMENT02:
                self.set_to_v2()
            case FortificationLevel.SEGMENT03:
                self.set_to_v2()
            case FortificationLevel.SEGMENT04:
                self.set_to_v4()
            case FortificationLevel.SEGMENT05:
                self.set_to_v5()
            case FortificationLevel.SEGMENT06:
                self.set_to_v5()
