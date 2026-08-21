from typing import ClassVar, override

from pydantic import Field

from core.combat import (
    CombatAction,
    DamageInstance,
    FixedDamageInstance,
    OTs14TotalSuppressionDamageCalculationStrategy,
    OverloadPulseDamageCalculationStrategy,
)
from core.types import DamageTag, Doll, FortificationLevel, SummonedUnit


class ShootingInstinct(CombatAction):
    """OTs-14 basic attack."""

    @override
    def execute(self) -> DamageInstance:
        label: str = "Shooting Instinct"
        base_potency: int = 90
        tags: set[DamageTag] = {
            DamageTag.ACTIVE,
            DamageTag.BASIC,
            DamageTag.MEDIUM_AMMO,
            DamageTag.TARGETED,
            DamageTag.OMNI,
        }

        return DamageInstance(
            label=label,
            base_potency=base_potency,
            tags=tags,
            group_name="Shooting Instinct",
        )


class CriticalBlast(CombatAction):
    """OTs-14 basic attack available only when OTs-14 is in Reverse Assimilation."""

    @override
    def execute(self, previous_uses: int) -> DamageInstance:
        label: str = "Critical Blast"
        base_potency: int = 150
        tags: set[DamageTag] = {
            DamageTag.ACTIVE,
            DamageTag.BASIC,
            DamageTag.AREA_OF_EFFECT,
            DamageTag.OMNI,
        }

        return DamageInstance(
            label=label,
            base_potency=base_potency,
            tags=tags,
            group_name="Critical Blast",
        )


class CriticalBlastV3(CombatAction):
    """OTs-14 basic attack available only when OTs-14 is in Reverse Assimilation (V3)."""

    @override
    def execute(self, previous_uses: int) -> DamageInstance:
        label: str = "Critical Blast"
        base_potency: int = 200
        tags: set[DamageTag] = {
            DamageTag.ACTIVE,
            DamageTag.BASIC,
            DamageTag.AREA_OF_EFFECT,
            DamageTag.OMNI,
        }

        return DamageInstance(
            label=label,
            base_potency=base_potency,
            tags=tags,
            group_name="Critical Blast",
        )


class CriticalBlastV4(CombatAction):
    """OTs-14 basic attack available only when OTs-14 is in Reverse Assimilation (V4)."""

    @override
    def execute(self, previous_uses: int) -> DamageInstance:
        label: str = f"Critical Blast ({previous_uses})"
        base_potency: int = 200
        tags: set[DamageTag] = {
            DamageTag.ACTIVE,
            DamageTag.BASIC,
            DamageTag.AREA_OF_EFFECT,
            DamageTag.OMNI,
        }

        potency_per_previous_use: int = 50
        base_potency += potency_per_previous_use * max(0, previous_uses)

        return DamageInstance(
            label=label,
            base_potency=base_potency,
            tags=tags,
            group_name="Critical Blast",
        )


class OverloadPulse(CombatAction):
    """Fixed damage from consuming Overload Pulse via Critical Blast."""

    @override
    def execute(
        self, accumulated_damage: int, uses_of_critical_splash: int
    ) -> DamageInstance:
        label: str = "Overload Pulse"

        fixed_damage_ratio: float = 0.1
        base_potency: int = int(accumulated_damage * fixed_damage_ratio)

        return FixedDamageInstance(
            label=label,
            base_potency=base_potency,
            group_name="Overload Pulse",
            damage_calculation_strategy=OverloadPulseDamageCalculationStrategy(),
        )


class OverloadPulseV4(CombatAction):
    """Fixed damage from consuming Overload Pulse via Critical Blast (V4)."""

    @override
    def execute(
        self, accumulated_damage: int, uses_of_critical_splash: int
    ) -> DamageInstance:
        label: str = "Overload Pulse"

        fixed_damage_ratio: float = 0.1
        fixed_damage_ratio_per_use: float = 0.1
        total_fixed_damage_ratio: float = (
            fixed_damage_ratio
            + fixed_damage_ratio_per_use * max(0, uses_of_critical_splash)
        )

        base_potency: int = int(accumulated_damage * total_fixed_damage_ratio)

        return FixedDamageInstance(
            label=label,
            base_potency=base_potency,
            group_name="Overload Pulse",
            damage_calculation_strategy=OverloadPulseDamageCalculationStrategy(),
        )


class TotalSuppression(CombatAction):
    """OTs-14 S1."""

    @override
    def execute(self, is_in_demolition_mode: bool) -> DamageInstance:
        label: str = "Total Suppression"
        base_potency: int = 120
        tags: set[DamageTag] = {
            DamageTag.ACTIVE,
            DamageTag.AREA_OF_EFFECT,
            DamageTag.OMNI,
        }

        ret_di: DamageInstance = DamageInstance(
            label=label,
            base_potency=base_potency,
            tags=tags,
            group_name="Total Suppression",
        )

        if is_in_demolition_mode:
            ret_di.damage_calculation_strategy = (
                OTs14TotalSuppressionDamageCalculationStrategy()
            )

        return ret_di


class TotalSuppressionV2(CombatAction):
    """OTs-14 S1 (V2)."""

    @override
    def execute(self, is_in_demolition_mode: bool) -> DamageInstance:
        label: str = "Total Suppression"
        base_potency: int = 150
        tags: set[DamageTag] = {
            DamageTag.ACTIVE,
            DamageTag.AREA_OF_EFFECT,
            DamageTag.OMNI,
        }

        ret_di: DamageInstance = DamageInstance(
            label=label,
            base_potency=base_potency,
            tags=tags,
            group_name="Total Suppression",
        )

        if is_in_demolition_mode:
            ret_di.damage_calculation_strategy = (
                OTs14TotalSuppressionDamageCalculationStrategy()
            )

        return ret_di


class TotalSuppressionV5(CombatAction):
    """OTs-14 S1 (V5)."""

    @override
    def execute(self, is_in_demolition_mode: bool) -> DamageInstance:
        label: str = "Total Suppression"
        base_potency: int = 150
        tags: set[DamageTag] = {
            DamageTag.ACTIVE,
            DamageTag.AREA_OF_EFFECT,
            DamageTag.OMNI,
        }

        ret_di: DamageInstance = DamageInstance(
            label=label,
            base_potency=base_potency,
            tags=tags,
            group_name="Total Suppression",
        )

        if is_in_demolition_mode:
            ret_di.damage_calculation_strategy = (
                OTs14TotalSuppressionDamageCalculationStrategy()
            )

        return ret_di


CombatInstinct = ShootingInstinct
CriticalSplash = CriticalBlast
CriticalSplashV3 = CriticalBlastV3
CriticalSplashV4 = CriticalBlastV4


class OTs14(Doll):
    """OTs-14."""

    name: str = "OTs-14"
    irrelevant_damage_tags: ClassVar[set[DamageTag]] = {
        DamageTag.PHYSICAL,
        DamageTag.MELEE,
        DamageTag.LIGHT_AMMO,
        DamageTag.SHOTGUN_AMMO,
        DamageTag.HEAVY_AMMO,
        DamageTag.SUPPORT_ACTION,
        DamageTag.INTERCEPTION,
        DamageTag.COUNTERATTACK,
        DamageTag.ULTIMATE,
        DamageTag.PHYSICAL_SUMMON,
    }

    combat_instinct: CombatAction = Field(default_factory=ShootingInstinct)
    critical_splash: CombatAction = Field(default_factory=CriticalBlast)
    overload_pulse: CombatAction = Field(default_factory=OverloadPulse)
    total_suppression: CombatAction = Field(default_factory=TotalSuppression)

    def set_to_v0(self) -> None:
        """Sets Fortification Level to Segment00."""
        self.combat_instinct = ShootingInstinct()
        self.critical_splash = CriticalBlast()
        self.overload_pulse = OverloadPulse()
        self.total_suppression = TotalSuppression()

    def set_to_v2(self) -> None:
        """Sets Fortification Level to Segment02."""
        self.set_to_v0()
        self.total_suppression = TotalSuppressionV2()

    def set_to_v3(self) -> None:
        """Sets Fortification Level to Segment03."""
        self.set_to_v2()
        self.critical_splash = CriticalBlastV3()

    def set_to_v4(self) -> None:
        """Sets Fortification Level to Segment04."""
        self.set_to_v3()
        self.critical_splash = CriticalBlastV4()
        self.overload_pulse = OverloadPulseV4()

    def set_to_v5(self) -> None:
        """Sets Fortification Level to Segment05."""
        self.set_to_v4()
        self.total_suppression = TotalSuppressionV5()

    @override
    def set_fortification_level(self, level: FortificationLevel):
        self.fortification_level = level
        match level:
            case FortificationLevel.SEGMENT00:
                self.set_to_v0()
            case FortificationLevel.SEGMENT01:
                self.set_to_v0()
            case FortificationLevel.SEGMENT02:
                self.set_to_v2()
            case FortificationLevel.SEGMENT03:
                self.set_to_v3()
            case FortificationLevel.SEGMENT04:
                self.set_to_v4()
            case FortificationLevel.SEGMENT05:
                self.set_to_v5()
            case FortificationLevel.SEGMENT06:
                self.set_to_v5()


__all__ = [
    "ShootingInstinct",
    "CriticalBlast",
    "CriticalBlastV3",
    "CriticalBlastV4",
    "CombatInstinct",
    "CriticalSplash",
    "CriticalSplashV3",
    "CriticalSplashV4",
    "OverloadPulse",
    "OverloadPulseV4",
    "TotalSuppression",
    "TotalSuppressionV2",
    "TotalSuppressionV5",
    "OTs14",
]
