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
    PhysicalSummonedUnit,
    build_physical_summon_stat_snapshot,
)
from core.buffs import Buff
from core.combat import (
    DamageInstance,
    CombatAction,
    HealthScalingDamageCalculationStrategy,
    ElsinDamageCalculationStrategy,
)


class GentleApproach(CombatAction):
    """Springfield basic attack."""

    @override
    def execute(self) -> DamageInstance:
        label: str = "Gentle Approach"
        base_potency: int = 80
        tags: set[DamageTag] = {
            DamageTag.ACTIVE,
            DamageTag.BASIC,
            DamageTag.HEAVY_AMMO,
            DamageTag.TARGETED,
            DamageTag.PHYSICAL,
        }

        return DamageInstance(
            label=label,
            base_potency=base_potency,
            tags=tags,
            group_name="Gentle Approach",
        )


class IntelManipulation(CombatAction):
    """Springfield S1."""

    @override
    def execute(self) -> DamageInstance:
        label: str = "Intel Manipulation"
        base_potency: int = 130
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
            group_name="Intel Manipulation",
        )


class IntelManipulationV4(CombatAction):
    """Springfield S1 (V4)."""

    @override
    def execute(self) -> DamageInstance:
        label: str = "Intel Manipulation"
        base_potency: int = 150
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
            group_name="Intel Manipulation",
        )


class PathOfProtection(CombatAction):
    """Springfield Ultimate."""

    @override
    def execute(self) -> DamageInstance:
        base_potency: int = 80
        label: str = "Path of Protection"
        tags: set[DamageTag] = {
            DamageTag.ACTIVE,
            DamageTag.HYDRO,
            DamageTag.PHASE,
            DamageTag.AREA_OF_EFFECT,
            DamageTag.ULTIMATE,
        }

        return DamageInstance(
            label=label,
            base_potency=base_potency,
            tags=tags,
            group_name="Path of Protection",
        )


class Counterattack(CombatAction):
    """Counterattack from Taryz."""

    @override
    def execute(self) -> DamageInstance:
        label: str = "Counterattack (Taryz)"
        base_potency: int = 100
        tags: set[DamageTag] = {
            DamageTag.PASSIVE,
            DamageTag.COUNTERATTACK,
            DamageTag.TARGETED,
            DamageTag.HYDRO,
            DamageTag.PHASE,
        }

        return DamageInstance(
            label=label,
            base_potency=base_potency,
            tags=tags,
            group_name="Counterattack (Taryz)",
            damage_calculation_strategy=HealthScalingDamageCalculationStrategy(0.20),
        )


class CounterattackV6(CombatAction):
    """Counterattack from Taryz (V6)."""

    @override
    def execute(self) -> DamageInstance:
        label: str = "Counterattack (Taryz)"
        base_potency: int = 100
        tags: set[DamageTag] = {
            DamageTag.PASSIVE,
            DamageTag.COUNTERATTACK,
            DamageTag.TARGETED,
            DamageTag.HYDRO,
            DamageTag.PHASE,
        }

        return DamageInstance(
            label=label,
            base_potency=base_potency,
            tags=tags,
            group_name="Counterattack (Taryz)",
            damage_calculation_strategy=HealthScalingDamageCalculationStrategy(0.40),
        )


class SupportAction(CombatAction):
    """Support Action from Taryz. Only available at V3+."""

    @override
    def execute(self) -> DamageInstance:
        label: str = "Support Action (Taryz)"
        base_potency: int = 0
        tags: set[DamageTag] = {
            DamageTag.PASSIVE,
            DamageTag.SUPPORT_ACTION,
            DamageTag.TARGETED,
            DamageTag.HYDRO,
            DamageTag.PHASE,
        }

        return DamageInstance(
            label=label,
            base_potency=base_potency,
            tags=tags,
            group_name="Support Action (Taryz)",
            damage_calculation_strategy=HealthScalingDamageCalculationStrategy(0.20),
        )


class SupportActionV3(CombatAction):
    """Support Action from Taryz (V3)."""

    @override
    def execute(self) -> DamageInstance:
        label: str = "Support Action (Taryz)"
        base_potency: int = 100
        tags: set[DamageTag] = {
            DamageTag.PASSIVE,
            DamageTag.SUPPORT_ACTION,
            DamageTag.TARGETED,
            DamageTag.HYDRO,
            DamageTag.PHASE,
        }

        return DamageInstance(
            label=label,
            base_potency=base_potency,
            tags=tags,
            group_name="Support Action",
            damage_calculation_strategy=HealthScalingDamageCalculationStrategy(0.20),
        )


class SupportActionV6(CombatAction):
    """Support Action from Taryz (V6)."""

    @override
    def execute(self) -> DamageInstance:
        label: str = "Support Action (Taryz)"
        base_potency: int = 100
        tags: set[DamageTag] = {
            DamageTag.PASSIVE,
            DamageTag.SUPPORT_ACTION,
            DamageTag.TARGETED,
            DamageTag.HYDRO,
            DamageTag.PHASE,
        }

        return DamageInstance(
            label=label,
            base_potency=base_potency,
            tags=tags,
            group_name="Support Action (Taryz)",
            damage_calculation_strategy=HealthScalingDamageCalculationStrategy(0.40),
        )


class Peck(CombatAction):
    """Peck from Elsin."""

    @override
    def execute(
        self, stacks_of_inundance: int, target_has_taryz: bool
    ) -> DamageInstance:
        label: str = "Peck (Elsin)"
        base_potency: int = (
            50  # 50% of Health; strategy uses 100% of Health as the base damage
        )
        tags: set[DamageTag] = {
            # DamageTag.PASSIVE,
            DamageTag.TARGETED,
            DamageTag.HYDRO,
            DamageTag.PHASE,
            DamageTag.PHYSICAL_SUMMON,
            DamageTag.BASIC,
        }

        # Mechanics refer to increasing the damage multiplier by x% which is equivalent
        # to x% of Elsin's Health. So we can use base_potency 1:1 with % of Health
        # and the DamageCalculationStrategy uses 100% of Health as the effective base
        # damage.

        # If the target is inflicted with Taryz, the damage multiplier is increased by 30%.
        if target_has_taryz:
            base_potency += 30

        # When Elsin's passive skill Peck is triggered, consumes all Inundance stacks and for each
        # stack consumed, the damage multiplier of Peck is increased by 5%
        potency_per_stack: int = 5
        base_potency += max(0, stacks_of_inundance) * potency_per_stack

        return DamageInstance(
            label=label,
            base_potency=base_potency,
            tags=tags,
            group_name="Peck (Elsin)",
            damage_calculation_strategy=ElsinDamageCalculationStrategy(),
        )


class Springfield(Doll):
    """Springfield."""

    name: str = "Springfield"
    irrelevant_damage_tags: ClassVar[set[DamageTag]] = set(
        [
            DamageTag.CORROSION,
            DamageTag.ELECTRIC,
            DamageTag.BURN,
            DamageTag.FREEZE,
            DamageTag.MELEE,
            DamageTag.LIGHT_AMMO,
            DamageTag.MEDIUM_AMMO,
            DamageTag.SHOTGUN_AMMO,
            DamageTag.INTERCEPTION,
            DamageTag.CONFECTANCE,
            DamageTag.FIXED,
        ]
    )

    gentle_approach: CombatAction = Field(default_factory=GentleApproach)
    intel_manipulation: CombatAction = Field(default_factory=IntelManipulation)
    path_of_protection: CombatAction = Field(default_factory=PathOfProtection)
    counterattack: CombatAction = Field(default_factory=Counterattack)
    support_action: CombatAction = Field(default_factory=SupportAction)
    peck: CombatAction = Field(default_factory=Peck)

    def _build_elsin(self) -> PhysicalSummonedUnit:
        # Elsin inherits all of Springfield's initial stats.
        # Upon Summon, its own HP is doubled.
        initial_stats, additive_modifiers, multiplicative_modifiers = (
            build_physical_summon_stat_snapshot(self)
        )
        elsin: PhysicalSummonedUnit = PhysicalSummonedUnit(
            name="Elsin",
            initial_stats=initial_stats,
            additive_modifiers=additive_modifiers,
            multiplicative_modifiers=multiplicative_modifiers,
        )

        elsin.initial_stats.basic_attributes[StatType.HEALTH] *= 2

        return elsin

    def summon_elsin(self) -> None:
        """Summons Elsin with a snapshot of Springfield's current stats."""
        if super().get_summoned_unit("Elsin") is None:
            self.summoned_units.append(self._build_elsin())

    def refresh_elsin(self) -> None:
        """Replaces Elsin with a fresh snapshot of Springfield's current stats.

        Call this whenever Springfield's stats have been mutated so that subsequent
        deepcopy-based damage calculations see up-to-date Elsin stats.
        """
        self.summoned_units = [u for u in self.summoned_units if u.name != "Elsin"]
        self.summoned_units.append(self._build_elsin())

    @override
    def prepare_for_calculation(self) -> None:
        self.refresh_elsin()

    @override
    def get_summoned_unit(self, name: str) -> SummonedUnit | None:
        self.summon_elsin()
        return super().get_summoned_unit(name)

    def set_to_v0(self) -> None:
        """Sets Fortification Level to Segment00."""
        self.gentle_approach: CombatAction = GentleApproach()
        self.intel_manipulation: CombatAction = IntelManipulation()
        self.path_of_protection: CombatAction = PathOfProtection()
        self.counterattack: CombatAction = Counterattack()
        self.support_action: CombatAction = SupportAction()
        self.peck: CombatAction = Peck()

        self.summon_elsin()

    def set_to_v3(self) -> None:
        """Sets Fortification Level to Segment03."""
        self.set_to_v0()

        self.support_action: CombatAction = SupportActionV3()

    def set_to_v4(self) -> None:
        """Sets Fortification Level to Segment04."""
        self.set_to_v3()

        self.intel_manipulation: CombatAction = IntelManipulationV4()

    def set_to_v6(self) -> None:
        """Sets Fortification Level to Segment06."""
        self.set_to_v4()

        self.support_action: CombatAction = SupportActionV6()
        self.counterattack: CombatAction = CounterattackV6()

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
                self.set_to_v6()
