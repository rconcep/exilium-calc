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
    LiushihDamageCalculationStrategy,
    PegasusDamageCalculationStrategy,
)


class LineBreaker(CombatAction):
    """Liushih Basic Attack."""

    @override
    def execute(self, stacks_of_precision: int) -> DamageInstance:
        label: str = "Line Breaker"
        base_potency: int = 90

        tags: set[DamageTag] = {
            DamageTag.ACTIVE,
            DamageTag.BASIC,
            DamageTag.HEAVY_AMMO,
            DamageTag.TARGETED,
            DamageTag.HYDRO,
            DamageTag.PHASE,
        }

        # Precision: Damage multiplier of basic attack is increased by 10%.
        potency_per_stack: int = 10
        base_potency += potency_per_stack * stacks_of_precision

        return DamageInstance(
            label=label,
            base_potency=base_potency,
            tags=tags,
            group_name="Line Breaker",
            damage_calculation_strategy=LiushihDamageCalculationStrategy(),
        )


class LineBreakerV3(CombatAction):
    """Liushih Basic Attack (V3)."""

    @override
    def execute(self, stacks_of_precision: int) -> DamageInstance:
        label: str = "Line Breaker"
        base_potency: int = 90

        tags: set[DamageTag] = {
            DamageTag.ACTIVE,
            DamageTag.BASIC,
            DamageTag.HEAVY_AMMO,
            DamageTag.TARGETED,
            DamageTag.HYDRO,
            DamageTag.PHASE,
        }

        # Precision: Damage multiplier of basic attack is increased by 20%.
        potency_per_stack: int = 20
        base_potency += potency_per_stack * stacks_of_precision

        return DamageInstance(
            label=label,
            base_potency=base_potency,
            tags=tags,
            group_name="Line Breaker",
            damage_calculation_strategy=LiushihDamageCalculationStrategy(),
        )


class AllOrNothing(CombatAction):
    """Liushih S1."""

    @override
    def execute(self) -> DamageInstance:
        label: str = "All or Nothing"
        base_potency: int = 90

        tags: set[DamageTag] = {
            DamageTag.ACTIVE,
            DamageTag.HEAVY_AMMO,
            DamageTag.TARGETED,
            DamageTag.HYDRO,
            DamageTag.PHASE,
        }

        return DamageInstance(
            label=label,
            base_potency=base_potency,
            tags=tags,
            group_name="All or Nothing",
            damage_calculation_strategy=LiushihDamageCalculationStrategy(),
        )


class AllOrNothingV3(CombatAction):
    """Liushih S1 (V3)."""

    @override
    def execute(self) -> DamageInstance:
        label: str = "All or Nothing"
        base_potency: int = 120

        tags: set[DamageTag] = {
            DamageTag.ACTIVE,
            DamageTag.HEAVY_AMMO,
            DamageTag.TARGETED,
            DamageTag.HYDRO,
            DamageTag.PHASE,
        }

        return DamageInstance(
            label=label,
            base_potency=base_potency,
            tags=tags,
            group_name="All or Nothing",
            damage_calculation_strategy=LiushihDamageCalculationStrategy(),
        )


class LeadingTheCharge(CombatAction):
    """Liushih Ultimate."""

    @override
    def execute(self) -> DamageInstance:
        label: str = "Leading the Charge"
        base_potency: int = 90

        tags: set[DamageTag] = {
            DamageTag.ULTIMATE,
            DamageTag.PHASE,
            DamageTag.HYDRO,
            DamageTag.TARGETED,
        }

        return DamageInstance(
            label=label,
            base_potency=base_potency,
            tags=tags,
            group_name="Leading the Charge",
            damage_calculation_strategy=LiushihDamageCalculationStrategy(),
        )


class LeadingTheChargeV4(CombatAction):
    """Liushih Ultimate (V4)."""

    @override
    def execute(self) -> DamageInstance:
        label: str = "Leading the Charge"
        base_potency: int = 120

        tags: set[DamageTag] = {
            DamageTag.ULTIMATE,
            DamageTag.PHASE,
            DamageTag.HYDRO,
            DamageTag.TARGETED,
        }

        return DamageInstance(
            label=label,
            base_potency=base_potency,
            tags=tags,
            group_name="Leading the Charge",
            damage_calculation_strategy=LiushihDamageCalculationStrategy(),
        )


class CloseInDefenseAutocannon(CombatAction):
    """Pegasus's follow-up attack."""

    @override
    def execute(self, stacks_of_precision: int) -> DamageInstance:
        label: str = "Close-In Defense Autocannon (Pegasus)"
        base_potency: int = 110

        tags: set[DamageTag] = {
            DamageTag.HYDRO,
            DamageTag.PHASE,
            DamageTag.PHYSICAL_SUMMON,
            DamageTag.TARGETED,
            DamageTag.BASIC,
            DamageTag.PASSIVE,
            DamageTag.HEAVY_AMMO,
        }

        # Precision: Damage multiplier of basic attack is increased by 10%.
        potency_per_stack: int = 10
        base_potency += potency_per_stack * stacks_of_precision

        return DamageInstance(
            label=label,
            base_potency=base_potency,
            tags=tags,
            group_name="Close-In Defense Autocannon (Pegasus)",
            damage_calculation_strategy=PegasusDamageCalculationStrategy(),
        )


class CloseInDefenseAutocannonV3(CombatAction):
    """Pegasus's follow-up attack (V3)."""

    @override
    def execute(self, stacks_of_precision: int) -> DamageInstance:
        label: str = "Close-In Defense Autocannon (Pegasus)"
        base_potency: int = 110

        tags: set[DamageTag] = {
            DamageTag.HYDRO,
            DamageTag.PHASE,
            DamageTag.PHYSICAL_SUMMON,
            DamageTag.TARGETED,
            DamageTag.BASIC,
            DamageTag.PASSIVE,
            DamageTag.HEAVY_AMMO,
        }

        # Precision: Damage multiplier of basic attack is increased by 20%.
        potency_per_stack: int = 20
        base_potency += potency_per_stack * stacks_of_precision

        return DamageInstance(
            label=label,
            base_potency=base_potency,
            tags=tags,
            group_name="Close-In Defense Autocannon (Pegasus)",
            damage_calculation_strategy=PegasusDamageCalculationStrategy(),
        )


class Liushih(Doll):
    """Liushih."""

    name: str = "Liushih"
    irrelevant_damage_tags: ClassVar[set[DamageTag]] = set(
        [
            DamageTag.CORROSION,
            DamageTag.BURN,
            DamageTag.FREEZE,
            DamageTag.ELECTRIC,
            DamageTag.MELEE,
            DamageTag.LIGHT_AMMO,
            DamageTag.MEDIUM_AMMO,
            DamageTag.SHOTGUN_AMMO,
            DamageTag.SUPPORT_ACTION,
            DamageTag.COUNTERATTACK,
            DamageTag.INTERCEPTION,
            DamageTag.FIXED,
        ]
    )

    line_breaker: CombatAction = Field(default_factory=LineBreaker)
    all_or_nothing: CombatAction = Field(default_factory=AllOrNothing)
    leading_the_charge: CombatAction = Field(default_factory=LeadingTheCharge)
    close_in_defense_autocannon: CombatAction = Field(
        default_factory=CloseInDefenseAutocannon
    )

    def _build_pegasus(self) -> PhysicalSummonedUnit:
        # Pegasus inherits all of Liushih's initial attributes.
        pegasus: PhysicalSummonedUnit = PhysicalSummonedUnit(
            name="Pegasus",
            initial_stats=self.initial_stats.model_copy(deep=True),
            additive_modifiers=self.additive_modifiers.model_copy(deep=True),
            multiplicative_modifiers=self.multiplicative_modifiers.model_copy(
                deep=True
            ),
        )

        return pegasus

    def summon_pegasus(self) -> None:
        """Summons Pegasus with a snapshot of Liushih's current stats."""
        if super().get_summoned_unit("Pegasus") is None:
            self.summoned_units.append(self._build_pegasus())

    def refresh_pegasus(self) -> None:
        """Replaces Pegasus with a fresh snapshot of Liushih's current stats.

        Call this whenever Liushih's stats have been mutated so that subsequent
        deepcopy-based damage calculations see up-to-date Pegasus stats.
        """
        self.summoned_units = [u for u in self.summoned_units if u.name != "Pegasus"]
        self.summoned_units.append(self._build_pegasus())

    @override
    def prepare_for_calculation(self) -> None:
        self.refresh_pegasus()

    @override
    def get_summoned_unit(self, name: str) -> SummonedUnit | None:
        self.summon_pegasus()
        return super().get_summoned_unit(name)

    def set_to_v0(self) -> None:
        """Sets Fortification Level to Segment00."""
        self.line_breaker = LineBreaker()
        self.all_or_nothing = AllOrNothing()
        self.leading_the_charge = LeadingTheCharge()
        self.close_in_defense_autocannon = CloseInDefenseAutocannon()

        self.summon_pegasus()

    def set_to_v3(self) -> None:
        """Sets Fortification Level to Segment03."""
        self.set_to_v0()
        self.line_breaker = LineBreakerV3()
        self.all_or_nothing = AllOrNothingV3()
        self.close_in_defense_autocannon = CloseInDefenseAutocannonV3()

    def set_to_v4(self) -> None:
        """Sets Fortification Level to Segment04."""
        self.set_to_v3()
        self.leading_the_charge = LeadingTheChargeV4()

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
                self.set_to_v3()
            case FortificationLevel.SEGMENT04:
                self.set_to_v4()
            case FortificationLevel.SEGMENT05:
                self.set_to_v4()
            case FortificationLevel.SEGMENT06:
                self.set_to_v4()
