from typing import override, ClassVar
from pydantic import Field

from core.types import (
    DamageTag,
    StatType,
    SpecialAttribute,
    ModifierType,
    FortificationLevel,
    Doll,
    SummonedUnit,
)
from core.buffs import Buff
from core.combat import DamageInstance, CombatAction


class DangerousSmile(CombatAction):
    """Leva Basic Attack."""

    @override
    def execute(self) -> DamageInstance:
        label: str = "Dangerous Smile"
        base_potency: int = 80

        tags: set[DamageTag] = {
            DamageTag.ACTIVE,
            DamageTag.BASIC,
            DamageTag.LIGHT_AMMO,
            DamageTag.TARGETED,
            DamageTag.PHYSICAL,
        }

        return DamageInstance(
            label=label,
            base_potency=base_potency,
            tags=tags,
            group_name="Dangerous Smile",
        )


class RationalSuppression(CombatAction):
    """Leva S1."""

    @override
    def execute(self) -> DamageInstance:
        label: str = "Rational Suppression"
        base_potency: int = 120
        tags: set[DamageTag] = {
            DamageTag.ACTIVE,
            DamageTag.ELECTRIC,
            DamageTag.PHASE,
            DamageTag.AREA_OF_EFFECT,
        }

        return DamageInstance(
            label=label,
            base_potency=base_potency,
            tags=tags,
            group_name="Rational Suppression",
        )


class RationalSuppressionV4(CombatAction):
    """Leva S1 (V4)."""

    @override
    def execute(self) -> DamageInstance:
        label: str = "Rational Suppression"
        base_potency: int = 120
        tags: set[DamageTag] = {
            DamageTag.ACTIVE,
            DamageTag.ELECTRIC,
            DamageTag.PHASE,
            DamageTag.AREA_OF_EFFECT,
        }

        return DamageInstance(
            label=label,
            base_potency=base_potency,
            tags=tags,
            group_name="Rational Suppression",
            buffs_before=[
                Buff(25, ModifierType.ADDITIVE, StatType.CRIT_DAMAGE),
            ],
        )


class OrderedDisruption(CombatAction):
    """Leva S2."""

    @override
    def execute(self, target_has_negative_charge: bool) -> DamageInstance:
        label: str = "Ordered Disruption"
        base_potency: int = 100
        tags: set[DamageTag] = {
            DamageTag.ACTIVE,
            DamageTag.ELECTRIC,
            DamageTag.PHASE,
            DamageTag.LIGHT_AMMO,
            DamageTag.AREA_OF_EFFECT,
        }

        buffs_before: list[Buff] = []

        if target_has_negative_charge:
            buffs_before.append(
                Buff(
                    30,
                    ModifierType.ADDITIVE,
                    SpecialAttribute.DAMAGE_BOOST,
                    DamageTag.ALL,
                )
            )

        return DamageInstance(
            label=label,
            base_potency=base_potency,
            tags=tags,
            group_name="Ordered Disruption",
            buffs_before=buffs_before,
        )


class OrderedDisruptionV2(CombatAction):
    """Leva S2 (V2)."""

    @override
    def execute(self, target_has_negative_charge: bool) -> DamageInstance:
        label: str = "Ordered Disruption"
        base_potency: int = 130
        tags: set[DamageTag] = {
            DamageTag.ACTIVE,
            DamageTag.ELECTRIC,
            DamageTag.PHASE,
            DamageTag.LIGHT_AMMO,
            DamageTag.AREA_OF_EFFECT,
        }

        buffs_before: list[Buff] = []

        if target_has_negative_charge:
            buffs_before.append(
                Buff(
                    30,
                    ModifierType.ADDITIVE,
                    SpecialAttribute.DAMAGE_BOOST,
                    DamageTag.ALL,
                )
            )

        return DamageInstance(
            label=label,
            base_potency=base_potency,
            tags=tags,
            group_name="Ordered Disruption",
            buffs_before=buffs_before,
        )


class QuantumCalculation(CombatAction):
    """Leva Ultimate."""

    @override
    def execute(self) -> DamageInstance:
        label: str = "Quantum Calculation"
        base_potency: int = 60
        tags: set[DamageTag] = {
            DamageTag.ACTIVE,
            DamageTag.ELECTRIC,
            DamageTag.PHASE,
            DamageTag.ULTIMATE,
            DamageTag.AREA_OF_EFFECT,
            DamageTag.CONFECTANCE,
        }

        return DamageInstance(
            label=label,
            base_potency=base_potency,
            tags=tags,
            group_name="Quantum Calculation",
        )


class QuantumCalculationV5(CombatAction):
    """Leva Ultimate (V5)."""

    @override
    def execute(self) -> DamageInstance:
        label: str = "Quantum Calculation"
        base_potency: int = 90
        tags: set[DamageTag] = {
            DamageTag.ACTIVE,
            DamageTag.ELECTRIC,
            DamageTag.PHASE,
            DamageTag.ULTIMATE,
            DamageTag.AREA_OF_EFFECT,
            DamageTag.CONFECTANCE,
        }

        return DamageInstance(
            label=label,
            base_potency=base_potency,
            tags=tags,
            group_name="Quantum Calculation",
        )


class SuperconductiveStrike(CombatAction):
    """Leva extra action after Ultimate."""

    @override
    def execute(self, superconductive_code_consumed: int) -> DamageInstance:
        label: str = f"Superconductive Strike ({superconductive_code_consumed})"
        base_potency: int = 75

        match superconductive_code_consumed:
            case 1:
                base_potency = 60
            case 2:
                base_potency = 70
            case 3:
                base_potency = 85
            case 4:
                base_potency = 120
            case _:
                ValueError("Only 1~4 is acceptable!")

        tags: set[DamageTag] = {
            DamageTag.ACTIVE,
            DamageTag.ELECTRIC,
            DamageTag.PHASE,
            DamageTag.MELEE,
            DamageTag.TARGETED,
        }

        return DamageInstance(
            label=label,
            base_potency=base_potency,
            tags=tags,
            group_name="Superconductive Strike",
        )


class SuperconductiveStrikeV3(CombatAction):
    """Leva extra action after Ultimate (V3)."""

    @override
    def execute(self, superconductive_code_consumed: int) -> DamageInstance:
        label: str = f"Superconductive Strike ({superconductive_code_consumed})"
        base_potency: int = 75

        match superconductive_code_consumed:
            case 1:
                base_potency = 75
            case 2:
                base_potency = 90
            case 3:
                base_potency = 120
            case 4:
                base_potency = 180
            case _:
                ValueError("Only 1~4 is acceptable!")

        tags: set[DamageTag] = {
            DamageTag.ACTIVE,
            DamageTag.ELECTRIC,
            DamageTag.PHASE,
            DamageTag.MELEE,
            DamageTag.TARGETED,
        }

        return DamageInstance(
            label=label,
            base_potency=base_potency,
            tags=tags,
            group_name="Superconductive Strike",
            buffs_before=[
                Buff(
                    15,
                    ModifierType.ADDITIVE,
                    SpecialAttribute.DEFENSE_IGNORE,
                    DamageTag.ALL,
                ),
            ],
        )


class EmergencySupport(CombatAction):
    """Support action when Negative Charge is applied to an enemy."""

    @override
    def execute(self) -> DamageInstance:
        label: str = "Emergency Support"
        base_potency: int = 60

        tags: set[DamageTag] = {
            DamageTag.PASSIVE,
            DamageTag.SUPPORT_ACTION,
            DamageTag.PHASE,
            DamageTag.ELECTRIC,
            DamageTag.MELEE,
            DamageTag.TARGETED,
        }

        return DamageInstance(
            label=label,
            base_potency=base_potency,
            tags=tags,
            group_name="Emergency Support",
        )


class OverclockingStrike(CombatAction):
    """Additional effect when inflicting excess stability damage from
    the Overclocking Strike buff.
    """

    @override
    def execute(self, excess_stability_damage: int) -> DamageInstance:
        label: str = f"Overclocking Strike ({excess_stability_damage})"
        base_potency: int = 5 * excess_stability_damage

        tags: set[DamageTag] = {
            DamageTag.PASSIVE,
            DamageTag.PHASE,
            DamageTag.ELECTRIC,
            DamageTag.TARGETED,
        }

        return DamageInstance(
            label=label,
            base_potency=base_potency,
            tags=tags,
            group_name="Overclocking Strike",
        )


class OverclockingStrikeV5(CombatAction):
    """Additional effect when inflicting excess stability damage from
    the Overclocking Strike buff (V5).
    """

    @override
    def execute(self, excess_stability_damage: int) -> DamageInstance:
        label: str = f"Overclocking Strike ({excess_stability_damage})"
        base_potency: int = 8 * excess_stability_damage

        tags: set[DamageTag] = {
            DamageTag.PASSIVE,
            DamageTag.PHASE,
            DamageTag.ELECTRIC,
            DamageTag.TARGETED,
        }

        return DamageInstance(
            label=label,
            base_potency=base_potency,
            tags=tags,
            group_name="Overclocking Strike",
        )


class Leva(Doll):
    """Leva."""

    name: str = "Leva"
    irrelevant_damage_tags: ClassVar[set[DamageTag]] = set(
        [
            DamageTag.CORROSION,
            DamageTag.BURN,
            DamageTag.HYDRO,
            DamageTag.FREEZE,
            DamageTag.MEDIUM_AMMO,
            DamageTag.HEAVY_AMMO,
            DamageTag.SHOTGUN_AMMO,
            DamageTag.INTERCEPTION,
            DamageTag.COUNTERATTACK,
            DamageTag.AREA_OF_EFFECT,
        ]
    )

    dangerous_smile: CombatAction = Field(default_factory=DangerousSmile)
    rational_suppression: CombatAction = Field(
        default_factory=RationalSuppression,
    )
    ordered_disruption: CombatAction = Field(
        default_factory=OrderedDisruption,
    )
    quantum_calculation: CombatAction = Field(
        default_factory=QuantumCalculation,
    )
    superconductive_strike: CombatAction = Field(
        default_factory=SuperconductiveStrike,
    )
    emergency_support: CombatAction = Field(
        default_factory=EmergencySupport,
    )
    overclocking_strike: CombatAction = Field(
        default_factory=OverclockingStrike,
    )

    def set_to_v0(self) -> None:
        """Sets Fortification Level to Segment00."""
        self.dangerous_smile: CombatAction = DangerousSmile()
        self.rational_suppression: CombatAction = RationalSuppression()
        self.ordered_disruption: CombatAction = OrderedDisruption()
        self.quantum_calculation: CombatAction = QuantumCalculation()
        self.superconductive_strike: CombatAction = SuperconductiveStrike()
        self.emergency_support: CombatAction = EmergencySupport()
        self.overclocking_strike: CombatAction = OverclockingStrike()

        # If Leva has positive charge, Electric damage dealt is increased by 10%.
        self.initial_stats.special_attributes[
            SpecialAttribute.DAMAGE_BOOST
        ].set_multiplier(
            DamageTag.ELECTRIC,
            10,
        )

        # Expansion Key
        # At the start of battle, Electric damage dealt by Leva is
        # increased by 2% ... for each Electric attributed Doll
        self.initial_stats.special_attributes[
            SpecialAttribute.DAMAGE_BOOST
        ].set_multiplier(
            DamageTag.ELECTRIC,
            20,
        )

        # When attacking targets with Negative Charge, critical
        # damage is increased by 7%. If the target is in Stability
        # Break, it is increased by an additional 7%.
        self.initial_stats.special_attributes[
            SpecialAttribute.CRITICAL_DAMAGE
        ].set_multiplier(DamageTag.ALL, 14)

    def set_to_v1(self) -> None:
        """Sets Fortification Level to Segment01."""
        self.set_to_v0()

        # When she has positive charge, Electric damage dealt is increased to 25% instead
        self.initial_stats.special_attributes[
            SpecialAttribute.DAMAGE_BOOST
        ].set_multiplier(
            DamageTag.ELECTRIC,
            25,
        )

    def set_to_v2(self) -> None:
        """Sets Fortification Level to Segment02."""
        self.set_to_v1()

        self.ordered_disruption: CombatAction = OrderedDisruptionV2()

    def set_to_v3(self) -> None:
        """Sets Fortification Level to Segment03."""
        self.set_to_v2()

        self.superconductive_strike: CombatAction = SuperconductiveStrikeV3()

    def set_to_v4(self) -> None:
        """Sets Fortification Level to Segment04."""
        self.set_to_v3()

        self.rational_suppression: CombatAction = RationalSuppressionV4()

    def set_to_v5(self) -> None:
        """Sets Fortification Level to Segment05."""
        self.set_to_v4()

        self.quantum_calculation: CombatAction = QuantumCalculationV5()
        self.overclocking_strike: CombatAction = OverclockingStrikeV5()

    def set_to_v6(self) -> None:
        """Sets Fortification Level to Segment06."""
        self.set_to_v5()

        # Leva's attack is increased by 15% the first time she reaches 4 stacks
        # of Superconductive Code in a battle.
        self.multiplicative_modifiers.basic_attributes[StatType.ATTACK] = 15

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
                self.set_to_v3()
            case FortificationLevel.SEGMENT04:
                self.set_to_v4()
            case FortificationLevel.SEGMENT05:
                self.set_to_v5()
            case FortificationLevel.SEGMENT06:
                self.set_to_v6()

    def get_sample_data(self) -> list[DamageInstance]:
        """Returns a sample single target rotation."""
        rotation_data: list[DamageInstance] = [
            # Turn 1
            self.emergency_support.execute(),
            self.overclocking_strike.execute(excess_stability_damage=1 + 2 + 5),
            self.emergency_support.execute(),
            self.overclocking_strike.execute(excess_stability_damage=1 + 2 + 5),
            self.emergency_support.execute(),
            self.overclocking_strike.execute(excess_stability_damage=1 + 2 + 5),
            self.emergency_support.execute(),
            self.overclocking_strike.execute(excess_stability_damage=1 + 2 + 5),
            self.quantum_calculation.execute(),
            self.overclocking_strike.execute(excess_stability_damage=1 + 2 + 5),
            self.superconductive_strike.execute(superconductive_code_consumed=4),
            self.overclocking_strike.execute(excess_stability_damage=8 + 2 + 5),
            # Turn 2
            self.emergency_support.execute(),
            self.overclocking_strike.execute(excess_stability_damage=1 + 2 + 5),
            self.emergency_support.execute(),
            self.overclocking_strike.execute(excess_stability_damage=1 + 2 + 5),
            self.emergency_support.execute(),
            self.overclocking_strike.execute(excess_stability_damage=1 + 2 + 5),
            self.emergency_support.execute(),
            self.overclocking_strike.execute(excess_stability_damage=1 + 2 + 5),
            self.ordered_disruption.execute(target_has_negative_charge=True),
            self.overclocking_strike.execute(excess_stability_damage=2 + 2 + 5),
            self.superconductive_strike.execute(superconductive_code_consumed=4),
            self.overclocking_strike.execute(excess_stability_damage=8 + 2 + 5),
            # Turn 3
            self.emergency_support.execute(),
            self.overclocking_strike.execute(excess_stability_damage=1 + 2 + 5),
            self.emergency_support.execute(),
            self.overclocking_strike.execute(excess_stability_damage=1 + 2 + 5),
            self.emergency_support.execute(),
            self.overclocking_strike.execute(excess_stability_damage=1 + 2 + 5),
            self.emergency_support.execute(),
            self.overclocking_strike.execute(excess_stability_damage=1 + 2 + 5),
            self.quantum_calculation.execute(),
            self.overclocking_strike.execute(excess_stability_damage=1 + 2 + 5),
            self.superconductive_strike.execute(superconductive_code_consumed=4),
            self.overclocking_strike.execute(excess_stability_damage=8 + 2 + 5),
            # Turn 4
            self.emergency_support.execute(),
            self.overclocking_strike.execute(excess_stability_damage=1 + 2 + 5),
            self.emergency_support.execute(),
            self.overclocking_strike.execute(excess_stability_damage=1 + 2 + 5),
            self.emergency_support.execute(),
            self.overclocking_strike.execute(excess_stability_damage=1 + 2 + 5),
            self.emergency_support.execute(),
            self.overclocking_strike.execute(excess_stability_damage=1 + 2 + 5),
            self.ordered_disruption.execute(target_has_negative_charge=True),
            self.overclocking_strike.execute(excess_stability_damage=2 + 2 + 5),
            self.superconductive_strike.execute(superconductive_code_consumed=4),
            self.overclocking_strike.execute(excess_stability_damage=8 + 2 + 5),
            # Turn 5
            self.emergency_support.execute(),
            self.overclocking_strike.execute(excess_stability_damage=1 + 2 + 5),
            self.emergency_support.execute(),
            self.overclocking_strike.execute(excess_stability_damage=1 + 2 + 5),
            self.emergency_support.execute(),
            self.overclocking_strike.execute(excess_stability_damage=1 + 2 + 5),
            self.emergency_support.execute(),
            self.overclocking_strike.execute(excess_stability_damage=1 + 2 + 5),
            self.quantum_calculation.execute(),
            self.overclocking_strike.execute(excess_stability_damage=1 + 2 + 5),
            self.superconductive_strike.execute(superconductive_code_consumed=4),
            self.overclocking_strike.execute(excess_stability_damage=8 + 2 + 5),
            # Turn 6
            self.emergency_support.execute(),
            self.overclocking_strike.execute(excess_stability_damage=1 + 2 + 5),
            self.emergency_support.execute(),
            self.overclocking_strike.execute(excess_stability_damage=1 + 2 + 5),
            self.emergency_support.execute(),
            self.overclocking_strike.execute(excess_stability_damage=1 + 2 + 5),
            self.emergency_support.execute(),
            self.overclocking_strike.execute(excess_stability_damage=1 + 2 + 5),
            self.ordered_disruption.execute(target_has_negative_charge=True),
            self.overclocking_strike.execute(excess_stability_damage=2 + 2 + 5),
            self.superconductive_strike.execute(superconductive_code_consumed=4),
            self.overclocking_strike.execute(excess_stability_damage=8 + 2 + 5),
            # Turn 7
            self.emergency_support.execute(),
            self.overclocking_strike.execute(excess_stability_damage=1 + 2 + 5),
            self.emergency_support.execute(),
            self.overclocking_strike.execute(excess_stability_damage=1 + 2 + 5),
            self.emergency_support.execute(),
            self.overclocking_strike.execute(excess_stability_damage=1 + 2 + 5),
            self.emergency_support.execute(),
            self.overclocking_strike.execute(excess_stability_damage=1 + 2 + 5),
            self.quantum_calculation.execute(),
            self.overclocking_strike.execute(excess_stability_damage=1 + 2 + 5),
            self.superconductive_strike.execute(superconductive_code_consumed=4),
            self.overclocking_strike.execute(excess_stability_damage=8 + 2 + 5),
        ]

        return rotation_data
