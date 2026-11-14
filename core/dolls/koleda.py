from typing import override, ClassVar
from pydantic import Field
from enum import StrEnum

from core.types import (
    DamageTag,
    StatType,
    SpecialAttribute,
    ModifierType,
    Doll,
    FortificationLevel,
    SummonedUnit,
    PhysicalSummonedUnit,
    build_physical_summon_stat_snapshot,
)
from core.buffs import Buff
from core.combat import (
    DamageInstance,
    CombatAction,
    SinveilerDamageCalculationStrategy,
)


class SinveilerGear(StrEnum):
    """The current gear that Sinveiler is in."""

    P = "P Gear"
    N = "N Gear"
    D = "D Gear"
    S = "S Gear"
    S_PLUS = "S+ Gear"


class PredatorInstinct(CombatAction):
    """Koleda Basic Attack."""

    @override
    def execute(self) -> DamageInstance:
        label: str = "Predator Instinct"
        base_potency: int = 90

        tags: set[DamageTag] = {
            DamageTag.ACTIVE,
            DamageTag.BASIC,
            DamageTag.MEDIUM_AMMO,
            DamageTag.TARGETED,
            DamageTag.HYDRO,
            DamageTag.PHASE,
        }

        return DamageInstance(
            label=label,
            base_potency=base_potency,
            tags=tags,
            group_name="Predator Instinct",
        )


class SnowWolfsEye(CombatAction):
    """Koleda S1."""

    @override
    def execute(self, stacks_of_upshift: int) -> DamageInstance:
        label: str = "Snow Wolf's Eye"
        base_potency: int = 150

        tags: set[DamageTag] = {
            DamageTag.ACTIVE,
            DamageTag.MEDIUM_AMMO,
            DamageTag.TARGETED,
            DamageTag.HYDRO,
            DamageTag.PHASE,
        }

        potency_per_stack: int = 0
        base_potency += potency_per_stack * max(0, stacks_of_upshift)

        return DamageInstance(
            label=label,
            base_potency=base_potency,
            tags=tags,
            group_name="Snow Wolf's Eye",
        )


class SnowWolfsEyeV1(CombatAction):
    """Koleda S1 (V1)."""

    @override
    def execute(self, stacks_of_upshift: int) -> DamageInstance:
        label: str = "Snow Wolf's Eye"
        base_potency: int = 180

        tags: set[DamageTag] = {
            DamageTag.ACTIVE,
            DamageTag.MEDIUM_AMMO,
            DamageTag.TARGETED,
            DamageTag.HYDRO,
            DamageTag.PHASE,
        }

        potency_per_stack: int = 15
        base_potency += potency_per_stack * max(0, stacks_of_upshift)

        return DamageInstance(
            label=label,
            base_potency=base_potency,
            tags=tags,
            group_name="Snow Wolf's Eye",
        )


class LetsGoForADrift(CombatAction):
    """Sinveiler's S2."""

    @override
    def execute(self, gear: SinveilerGear = SinveilerGear.P) -> DamageInstance:
        label: str = "Let's Go for a Drift! (Sinveiler)"
        base_potency: int = 90

        tags: set[DamageTag] = {
            DamageTag.ACTIVE,
            DamageTag.AREA_OF_EFFECT,
            DamageTag.HYDRO,
            DamageTag.PHASE,
            DamageTag.PHYSICAL_SUMMON,
        }

        return DamageInstance(
            label=label,
            base_potency=base_potency,
            tags=tags,
            group_name="Let's Go for a Drift! (Sinveiler)",
            damage_calculation_strategy=SinveilerDamageCalculationStrategy(),
        )


class LetsGoForADriftV3(CombatAction):
    """Sinveiler's S2 (V3)."""

    @override
    def execute(self, gear: SinveilerGear = SinveilerGear.P) -> DamageInstance:
        label: str = "Let's Go for a Drift! (Sinveiler)"
        base_potency: int = 90

        match gear:
            case SinveilerGear.S_PLUS:
                base_potency += 30
            case _:
                pass

        tags: set[DamageTag] = {
            DamageTag.ACTIVE,
            DamageTag.AREA_OF_EFFECT,
            DamageTag.HYDRO,
            DamageTag.PHASE,
            DamageTag.PHYSICAL_SUMMON,
        }

        return DamageInstance(
            label=label,
            base_potency=base_potency,
            tags=tags,
            group_name="Let's Go for a Drift! (Sinveiler)",
            damage_calculation_strategy=SinveilerDamageCalculationStrategy(),
        )


class LetsGoForADriftV4(CombatAction):
    """Sinveiler's S2 (V4)."""

    @override
    def execute(self, gear: SinveilerGear = SinveilerGear.P) -> DamageInstance:
        label: str = "Let's Go for a Drift! (Sinveiler)"
        base_potency: int = 120

        match gear:
            case SinveilerGear.S_PLUS:
                base_potency += 30
            case _:
                pass

        tags: set[DamageTag] = {
            DamageTag.ACTIVE,
            DamageTag.AREA_OF_EFFECT,
            DamageTag.HYDRO,
            DamageTag.PHASE,
            DamageTag.PHYSICAL_SUMMON,
        }

        return DamageInstance(
            label=label,
            base_potency=base_potency,
            tags=tags,
            group_name="Let's Go for a Drift! (Sinveiler)",
            damage_calculation_strategy=SinveilerDamageCalculationStrategy(),
        )


class LetsGoFullSpeed(CombatAction):
    """Sinveiler's S3."""

    @override
    def execute(self, gear: SinveilerGear = SinveilerGear.P) -> DamageInstance:
        label: str = "Let's Go Full Speed! (Sinveiler)"
        base_potency: int = 90

        tags: set[DamageTag] = {
            DamageTag.ACTIVE,
            DamageTag.AREA_OF_EFFECT,
            DamageTag.HYDRO,
            DamageTag.PHASE,
            DamageTag.PHYSICAL_SUMMON,
        }

        return DamageInstance(
            label=label,
            base_potency=base_potency,
            tags=tags,
            group_name="Let's Go Full Speed! (Sinveiler)",
            damage_calculation_strategy=SinveilerDamageCalculationStrategy(),
        )


class LetsGoFullSpeedV3(CombatAction):
    """Sinveiler's S3 (V3)."""

    @override
    def execute(self, gear: SinveilerGear = SinveilerGear.P) -> DamageInstance:
        label: str = "Let's Go Full Speed! (Sinveiler)"
        base_potency: int = 90

        match gear:
            case SinveilerGear.S_PLUS:
                base_potency += 30
            case _:
                pass

        tags: set[DamageTag] = {
            DamageTag.ACTIVE,
            DamageTag.AREA_OF_EFFECT,
            DamageTag.HYDRO,
            DamageTag.PHASE,
            DamageTag.PHYSICAL_SUMMON,
        }

        return DamageInstance(
            label=label,
            base_potency=base_potency,
            tags=tags,
            group_name="Let's Go Full Speed! (Sinveiler)",
            damage_calculation_strategy=SinveilerDamageCalculationStrategy(),
        )


class LetsGoFullSpeedV5(CombatAction):
    """Sinveiler's S3 (V5)."""

    @override
    def execute(self, gear: SinveilerGear = SinveilerGear.P) -> DamageInstance:
        label: str = "Let's Go Full Speed! (Sinveiler)"
        base_potency: int = 120

        match gear:
            case SinveilerGear.S_PLUS:
                base_potency += 30
            case _:
                pass

        tags: set[DamageTag] = {
            DamageTag.ACTIVE,
            DamageTag.AREA_OF_EFFECT,
            DamageTag.HYDRO,
            DamageTag.PHASE,
            DamageTag.PHYSICAL_SUMMON,
        }

        return DamageInstance(
            label=label,
            base_potency=base_potency,
            tags=tags,
            group_name="Let's Go Full Speed! (Sinveiler)",
            damage_calculation_strategy=SinveilerDamageCalculationStrategy(),
        )


class LetsGoFullSpeedPursuit(CombatAction):
    """The pursuit/followup of Sinveiler's S3 when it's used in S or S+ Gear."""

    @override
    def execute(self, gear: SinveilerGear = SinveilerGear.P) -> DamageInstance:
        label: str = "Let's Go Full Speed! (Pursuit) (Sinveiler)"
        base_potency: int = 0

        match gear:
            case SinveilerGear.S:
                base_potency = 60
            case SinveilerGear.S_PLUS:
                base_potency = 90
            case _:
                base_potency = 0

        tags: set[DamageTag] = {
            DamageTag.AREA_OF_EFFECT,
            DamageTag.HYDRO,
            DamageTag.PHASE,
            DamageTag.PHYSICAL_SUMMON,
        }

        return DamageInstance(
            label=label,
            base_potency=base_potency,
            tags=tags,
            group_name="Let's Go Full Speed! (Sinveiler)",
            damage_calculation_strategy=SinveilerDamageCalculationStrategy(),
        )


class LetsGoFullSpeedPursuitV3(CombatAction):
    """The pursuit/followup of Sinveiler's S3 (V3) when it's used in S or S+ Gear."""

    @override
    def execute(self, gear: SinveilerGear = SinveilerGear.P) -> DamageInstance:
        label: str = "Let's Go Full Speed! (Pursuit) (Sinveiler)"
        base_potency: int = 0

        match gear:
            case SinveilerGear.S:
                base_potency = 60
            case SinveilerGear.S_PLUS:
                base_potency = 120
            case _:
                base_potency = 0

        tags: set[DamageTag] = {
            DamageTag.AREA_OF_EFFECT,
            DamageTag.HYDRO,
            DamageTag.PHASE,
            DamageTag.PHYSICAL_SUMMON,
        }

        return DamageInstance(
            label=label,
            base_potency=base_potency,
            tags=tags,
            group_name="Let's Go Full Speed! (Sinveiler)",
            damage_calculation_strategy=SinveilerDamageCalculationStrategy(),
        )


class LetsGoFullSpeedPursuitV5(CombatAction):
    """The pursuit/followup of Sinveiler's S3 (V5) when it's used in S or S+ Gear."""

    @override
    def execute(self, gear: SinveilerGear = SinveilerGear.P) -> DamageInstance:
        label: str = "Let's Go Full Speed! (Pursuit) (Sinveiler)"
        base_potency: int = 0

        match gear:
            case SinveilerGear.S:
                base_potency = 90
            case SinveilerGear.S_PLUS:
                base_potency = 150
            case _:
                base_potency = 0

        tags: set[DamageTag] = {
            DamageTag.AREA_OF_EFFECT,
            DamageTag.HYDRO,
            DamageTag.PHASE,
            DamageTag.PHYSICAL_SUMMON,
        }

        return DamageInstance(
            label=label,
            base_potency=base_potency,
            tags=tags,
            group_name="Let's Go Full Speed! (Sinveiler)",
            damage_calculation_strategy=SinveilerDamageCalculationStrategy(),
        )


class KineticRelease(CombatAction):
    """Used at the end of Sinveiler's action when it's used in S Gear."""

    @override
    def execute(self, gear: SinveilerGear = SinveilerGear.P) -> DamageInstance:
        label: str = "Kinetic Release (Sinveiler)"
        base_potency: int = 90

        tags: set[DamageTag] = {
            DamageTag.AREA_OF_EFFECT,
            DamageTag.HYDRO,
            DamageTag.PHASE,
            DamageTag.PHYSICAL_SUMMON,
        }

        return DamageInstance(
            label=label,
            base_potency=base_potency,
            tags=tags,
            group_name="Kinetic Release (Sinveiler)",
            damage_calculation_strategy=SinveilerDamageCalculationStrategy(),
        )


class KineticReleaseV2(CombatAction):
    """Used at the end of Sinveiler's action when it's used in S Gear."""

    @override
    def execute(self, gear: SinveilerGear = SinveilerGear.P) -> DamageInstance:
        label: str = "Kinetic Release (Sinveiler)"
        base_potency: int = 120

        tags: set[DamageTag] = {
            DamageTag.AREA_OF_EFFECT,
            DamageTag.HYDRO,
            DamageTag.PHASE,
            DamageTag.PHYSICAL_SUMMON,
        }

        return DamageInstance(
            label=label,
            base_potency=base_potency,
            tags=tags,
            group_name="Kinetic Release (Sinveiler)",
            damage_calculation_strategy=SinveilerDamageCalculationStrategy(),
        )


class KineticReleaseV3(CombatAction):
    """Used at the end of Sinveiler's action when it's used in S Gear."""

    @override
    def execute(self, gear: SinveilerGear = SinveilerGear.P) -> DamageInstance:
        label: str = "Kinetic Release (Sinveiler)"
        base_potency: int = 120

        match gear:
            case SinveilerGear.S_PLUS:
                base_potency += 30
            case _:
                pass

        tags: set[DamageTag] = {
            DamageTag.AREA_OF_EFFECT,
            DamageTag.HYDRO,
            DamageTag.PHASE,
            DamageTag.PHYSICAL_SUMMON,
        }

        return DamageInstance(
            label=label,
            base_potency=base_potency,
            tags=tags,
            group_name="Kinetic Release (Sinveiler)",
            damage_calculation_strategy=SinveilerDamageCalculationStrategy(),
        )


class KineticReleasePlus(CombatAction):
    """Used at the end of Sinveiler's action when it's used in S+ Gear."""

    @override
    def execute(self, gear: SinveilerGear = SinveilerGear.P) -> DamageInstance:
        label: str = "Kinetic Release+ (Sinveiler)"
        base_potency: int = 120

        tags: set[DamageTag] = {
            DamageTag.AREA_OF_EFFECT,
            DamageTag.HYDRO,
            DamageTag.PHASE,
            DamageTag.PHYSICAL_SUMMON,
        }

        return DamageInstance(
            label=label,
            base_potency=base_potency,
            tags=tags,
            group_name="Kinetic Release (Sinveiler)",
            damage_calculation_strategy=SinveilerDamageCalculationStrategy(),
        )


class KineticReleasePlusV2(CombatAction):
    """Used at the end of Sinveiler's action when it's used in S+ Gear."""

    @override
    def execute(self, gear: SinveilerGear = SinveilerGear.P) -> DamageInstance:
        label: str = "Kinetic Release+ (Sinveiler)"
        base_potency: int = 150

        tags: set[DamageTag] = {
            DamageTag.AREA_OF_EFFECT,
            DamageTag.HYDRO,
            DamageTag.PHASE,
            DamageTag.PHYSICAL_SUMMON,
        }

        return DamageInstance(
            label=label,
            base_potency=base_potency,
            tags=tags,
            group_name="Kinetic Release (Sinveiler)",
            damage_calculation_strategy=SinveilerDamageCalculationStrategy(),
        )


class KineticReleasePlusV3(CombatAction):
    """Used at the end of Sinveiler's action when it's used in S+ Gear."""

    @override
    def execute(self, gear: SinveilerGear = SinveilerGear.P) -> DamageInstance:
        label: str = "Kinetic Release+ (Sinveiler)"
        base_potency: int = 150

        match gear:
            case SinveilerGear.S_PLUS:
                base_potency += 30
            case _:
                pass

        tags: set[DamageTag] = {
            DamageTag.AREA_OF_EFFECT,
            DamageTag.HYDRO,
            DamageTag.PHASE,
            DamageTag.PHYSICAL_SUMMON,
        }

        return DamageInstance(
            label=label,
            base_potency=base_potency,
            tags=tags,
            group_name="Kinetic Release (Sinveiler)",
            damage_calculation_strategy=SinveilerDamageCalculationStrategy(),
        )


class KoledaKineticRelease(CombatAction):
    """Used at the end of Koleda's turn or after using Tactical Routebook."""

    @override
    def execute(self) -> DamageInstance:
        label: str = "Kinetic Release (Koleda)"
        base_potency: int = 90

        tags: set[DamageTag] = {
            DamageTag.AREA_OF_EFFECT,
            DamageTag.HYDRO,
            DamageTag.PHASE,
        }

        return DamageInstance(
            label=label,
            base_potency=base_potency,
            tags=tags,
            group_name="Kinetic Release (Koleda)",
        )


class KoledaKineticReleaseV2(CombatAction):
    """Used at the end of Koleda's turn or after using Tactical Routebook."""

    @override
    def execute(self) -> DamageInstance:
        label: str = "Kinetic Release (Koleda)"
        base_potency: int = 120

        tags: set[DamageTag] = {
            DamageTag.AREA_OF_EFFECT,
            DamageTag.HYDRO,
            DamageTag.PHASE,
        }

        return DamageInstance(
            label=label,
            base_potency=base_potency,
            tags=tags,
            group_name="Kinetic Release (Koleda)",
        )


class KoledaKineticReleasePlus(CombatAction):
    """Used at the end of Koleda's turn or after using Tactical Routebook."""

    @override
    def execute(self) -> DamageInstance:
        label: str = "Kinetic Release+ (Koleda)"
        base_potency: int = 120

        tags: set[DamageTag] = {
            DamageTag.AREA_OF_EFFECT,
            DamageTag.HYDRO,
            DamageTag.PHASE,
        }

        return DamageInstance(
            label=label,
            base_potency=base_potency,
            tags=tags,
            group_name="Kinetic Release (Koleda)",
        )


class KoledaKineticReleasePlusV2(CombatAction):
    """Used at the end of Koleda's turn or after using Tactical Routebook."""

    @override
    def execute(self) -> DamageInstance:
        label: str = "Kinetic Release+ (Koleda)"
        base_potency: int = 150

        tags: set[DamageTag] = {
            DamageTag.AREA_OF_EFFECT,
            DamageTag.HYDRO,
            DamageTag.PHASE,
        }

        return DamageInstance(
            label=label,
            base_potency=base_potency,
            tags=tags,
            group_name="Kinetic Release (Koleda)",
        )


# TODO: Koleda passive The Sinner - When Sinveiler uses the active skill Let's Go For a Spin!,
# Koleda gains Sinveiler's initial attack and critical damage.
# This is based on the value after any stat increase from Out for a Spin!
# Implement as a Buff?
# Does "gain" mean add to or set equal to? Adding to sounds like it would double+ the value.


class Koleda(Doll):
    """Koleda."""

    name: str = "Koleda"
    irrelevant_damage_tags: ClassVar[set[DamageTag]] = set(
        [
            DamageTag.PHYSICAL,
            DamageTag.CORROSION,
            DamageTag.BURN,
            DamageTag.FREEZE,
            DamageTag.ELECTRIC,
            DamageTag.MELEE,
            DamageTag.LIGHT_AMMO,
            DamageTag.HEAVY_AMMO,
            DamageTag.SHOTGUN_AMMO,
            DamageTag.SUPPORT_ACTION,
            DamageTag.COUNTERATTACK,
            DamageTag.INTERCEPTION,
            DamageTag.FIXED,
        ]
    )

    predator_instinct: CombatAction = Field(default_factory=PredatorInstinct)
    snow_wolfs_eye: CombatAction = Field(default_factory=SnowWolfsEye)
    lets_go_for_a_drift: CombatAction = Field(default_factory=LetsGoForADrift)
    lets_go_full_speed: CombatAction = Field(default_factory=LetsGoFullSpeed)
    lets_go_full_speed_pursuit: CombatAction = Field(
        default_factory=LetsGoFullSpeedPursuit
    )
    kinetic_release: CombatAction = Field(default_factory=KineticRelease)
    kinetic_release_plus: CombatAction = Field(default_factory=KineticReleasePlus)
    koleda_kinetic_release: CombatAction = Field(default_factory=KoledaKineticRelease)
    koleda_kinetic_release_plus: CombatAction = Field(
        default_factory=KoledaKineticReleasePlus
    )

    # Driver configuration for Sinveiler inheritance
    driver_attack: float = 0.0
    driver_defense: float = 0.0
    driver_health: float = 0.0
    driver_crit_damage: float = 0.0

    def _build_sinveiler(self) -> PhysicalSummonedUnit:
        # Sinveiler inherits all of Koleda's initial attributes.
        initial_stats, additive_modifiers, multiplicative_modifiers = (
            build_physical_summon_stat_snapshot(self)
        )

        # Apply driver stat inheritance based on fortification level
        # Different fortification levels have different inheritance percentages
        driver_inheritance_rate = self._get_driver_inheritance_rate()
        if driver_inheritance_rate > 0 and (
            self.driver_attack > 0
            or self.driver_defense > 0
            or self.driver_health > 0
            or self.driver_crit_damage > 0
        ):
            # Apply driver stats to Sinveiler's initial stats
            if self.driver_attack > 0:
                initial_stats.basic_attributes[StatType.ATTACK] += (
                    self.driver_attack * driver_inheritance_rate
                )
            if self.driver_defense > 0:
                initial_stats.basic_attributes[StatType.DEFENSE] += (
                    self.driver_defense * driver_inheritance_rate
                )
            if self.driver_health > 0:
                initial_stats.basic_attributes[StatType.HEALTH] += (
                    self.driver_health * driver_inheritance_rate
                )
            if self.driver_crit_damage > 0:
                initial_stats.basic_attributes[StatType.CRIT_DAMAGE] += (
                    self.driver_crit_damage * driver_inheritance_rate
                )

        sinveiler: PhysicalSummonedUnit = PhysicalSummonedUnit(
            name="Sinveiler",
            initial_stats=initial_stats,
            additive_modifiers=additive_modifiers,
            multiplicative_modifiers=multiplicative_modifiers,
        )

        return sinveiler

    def _get_driver_inheritance_rate(self) -> float:
        """Returns the percentage of driver stats inherited by Sinveiler based on fortification level.

        Driver inheritance rates increase with fortification level:
        - V0-V5: 50%
        - V6: 70%
        """
        match self.fortification_level:
            case FortificationLevel.SEGMENT06:
                return 0.70
            case _:
                return 0.50

    def set_driver(
        self,
        attack: float = 0.0,
        defense: float = 0.0,
        health: float = 0.0,
        crit_damage: float = 0.0,
    ) -> None:
        """Sets the driver stats for Sinveiler inheritance.

        Args:
            attack: Driver's attack stat
            defense: Driver's defense stat
            health: Driver's health stat
            crit_damage: Driver's crit damage stat
        """
        self.driver_attack = attack
        self.driver_defense = defense
        self.driver_health = health
        self.driver_crit_damage = crit_damage

    def summon_sinveiler(self) -> None:
        """Summons Sinveiler with a snapshot of Koleda's current stats."""
        if super().get_summoned_unit("Sinveiler") is None:
            self.summoned_units.append(self._build_sinveiler())

    def refresh_sinveiler(self) -> None:
        """Replaces Sinveiler with a fresh snapshot of Koleda's current stats.

        Call this whenever Koleda's stats have been mutated so that subsequent
        deepcopy-based damage calculations see up-to-date Sinveiler stats.
        """
        self.summoned_units = [u for u in self.summoned_units if u.name != "Sinveiler"]
        self.summoned_units.append(self._build_sinveiler())

    @override
    def prepare_for_calculation(self) -> None:
        self.refresh_sinveiler()

    @override
    def get_summoned_unit(self, name: str) -> SummonedUnit | None:
        self.summon_sinveiler()
        return super().get_summoned_unit(name)

    def set_to_v0(self) -> None:
        """Sets Fortification Level to Segment00."""
        self.predator_instinct = PredatorInstinct()
        self.snow_wolfs_eye = SnowWolfsEye()
        self.lets_go_for_a_drift = LetsGoForADrift()
        self.lets_go_full_speed = LetsGoFullSpeed()
        self.lets_go_full_speed_pursuit = LetsGoFullSpeedPursuit()
        self.kinetic_release = KineticRelease()
        self.kinetic_release_plus = KineticReleasePlus()
        self.koleda_kinetic_release = KoledaKineticRelease()
        self.koleda_kinetic_release_plus = KoledaKineticReleasePlus()

        self.summon_sinveiler()

    def set_to_v1(self) -> None:
        """Sets Fortification Level to Segment01."""
        self.set_to_v0()

        self.snow_wolfs_eye = SnowWolfsEyeV1()

    def set_to_v2(self) -> None:
        """Sets Fortification Level to Segment02."""
        self.set_to_v1()

        self.kinetic_release = KineticReleaseV2()
        self.kinetic_release_plus = KineticReleasePlusV2()
        self.koleda_kinetic_release = KoledaKineticReleaseV2()
        self.koleda_kinetic_release_plus = KoledaKineticReleasePlusV2()

    def set_to_v3(self) -> None:
        """Sets Fortification Level to Segment03."""
        self.set_to_v2()

        self.lets_go_for_a_drift = LetsGoForADriftV3()
        self.lets_go_full_speed = LetsGoFullSpeedV3()
        self.lets_go_full_speed_pursuit = LetsGoFullSpeedPursuitV3()
        self.kinetic_release = KineticReleaseV3()
        self.kinetic_release_plus = KineticReleasePlusV3()

    def set_to_v4(self) -> None:
        """Sets Fortification Level to Segment04."""
        self.set_to_v3()

        self.lets_go_for_a_drift = LetsGoForADriftV4()

    def set_to_v5(self) -> None:
        """Sets Fortification Level to Segment05."""
        self.set_to_v4()

        self.lets_go_full_speed = LetsGoFullSpeedV5()
        self.lets_go_full_speed_pursuit = LetsGoFullSpeedPursuitV5()

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
                self.set_to_v5()
