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
    build_physical_summon_stat_snapshot,
)
from core.buffs import Buff
from core.combat import (
    DamageInstance,
    CombatAction,
    SelfHologramDamageCalculationStrategy,
)


class AssaultShot(CombatAction):
    """Mityl Basic Attack."""

    @override
    def execute(self) -> DamageInstance:
        label: str = "Assault Shot"
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
            group_name="Assault Shot",
        )


class AirDash(CombatAction):
    """Mityl S2."""

    @override
    def execute(self, is_skill_reuse: bool) -> DamageInstance:
        label: str = "Air Dash"
        base_potency: int = 130

        tags: set[DamageTag] = {
            DamageTag.ACTIVE,
            DamageTag.LIGHT_AMMO,
            DamageTag.TARGETED,
            DamageTag.HYDRO,
            DamageTag.PHASE,
            DamageTag.CONFECTANCE,
        }

        buffs_before: list[Buff] = []

        if is_skill_reuse:
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
            group_name="Air Dash",
            buffs_before=buffs_before,
        )


class AirDashV4(CombatAction):
    """Mityl S2 (V4)."""

    @override
    def execute(self, is_skill_reuse: bool) -> DamageInstance:
        label: str = "Air Dash"
        base_potency: int = 160

        tags: set[DamageTag] = {
            DamageTag.ACTIVE,
            DamageTag.LIGHT_AMMO,
            DamageTag.TARGETED,
            DamageTag.HYDRO,
            DamageTag.PHASE,
            DamageTag.CONFECTANCE,
        }

        buffs_before: list[Buff] = []

        if is_skill_reuse:
            buffs_before.append(
                Buff(
                    50,
                    ModifierType.ADDITIVE,
                    SpecialAttribute.DAMAGE_BOOST,
                    DamageTag.ALL,
                )
            )

        return DamageInstance(
            label=label,
            base_potency=base_potency,
            tags=tags,
            group_name="Air Dash",
            buffs_before=buffs_before,
        )


class SupportAction(CombatAction):
    """Self Hologram's Support Action after Mityl uses her S2."""

    @override
    def execute(self) -> DamageInstance:
        label: str = "Support Action (Self Hologram)"
        base_potency: int = 0  # This action is not available until V5

        tags: set[DamageTag] = {
            DamageTag.HYDRO,
            DamageTag.PHASE,
            DamageTag.PHYSICAL_SUMMON,
            DamageTag.TARGETED,
            DamageTag.PASSIVE,
            DamageTag.SUPPORT_ACTION,  # TODO: Confirm if this tag should be included for the support action
        }

        return DamageInstance(
            label=label,
            base_potency=base_potency,
            tags=tags,
            group_name="Support Action (Self Hologram)",
            damage_calculation_strategy=SelfHologramDamageCalculationStrategy(),
        )


class SupportActionV5(CombatAction):
    """Self Hologram's Support Action after Mityl uses her S2."""

    @override
    def execute(self) -> DamageInstance:
        label: str = "Support Action (Self Hologram)"
        base_potency: int = 60

        tags: set[DamageTag] = {
            DamageTag.HYDRO,
            DamageTag.PHASE,
            DamageTag.PHYSICAL_SUMMON,
            DamageTag.TARGETED,
            DamageTag.PASSIVE,
            DamageTag.SUPPORT_ACTION,  # TODO: Confirm if this tag should be included for the support action
        }

        return DamageInstance(
            label=label,
            base_potency=base_potency,
            tags=tags,
            group_name="Support Action (Self Hologram)",
            damage_calculation_strategy=SelfHologramDamageCalculationStrategy(),
        )


class AlignedResonance(CombatAction):
    """Self Hologram's action used at the end of the allied turn."""

    @override
    def execute(self) -> DamageInstance:
        label: str = "Aligned Resonance (Self Hologram)"
        base_potency: int = 40

        tags: set[DamageTag] = {
            DamageTag.HYDRO,
            DamageTag.PHASE,
            DamageTag.PHYSICAL_SUMMON,
            DamageTag.TARGETED,
            DamageTag.PASSIVE,
        }

        return DamageInstance(
            label=label,
            base_potency=base_potency,
            tags=tags,
            group_name="Aligned Resonance (Self Hologram)",
            damage_calculation_strategy=SelfHologramDamageCalculationStrategy(),
        )


class AlignedResonanceV1(CombatAction):
    """Self Hologram's action used at the end of the allied turn."""

    @override
    def execute(self) -> DamageInstance:
        label: str = "Aligned Resonance (Self Hologram)"
        base_potency: int = 60

        tags: set[DamageTag] = {
            DamageTag.HYDRO,
            DamageTag.PHASE,
            DamageTag.PHYSICAL_SUMMON,
            DamageTag.TARGETED,
            DamageTag.PASSIVE,
        }

        return DamageInstance(
            label=label,
            base_potency=base_potency,
            tags=tags,
            group_name="Aligned Resonance (Self Hologram)",
            damage_calculation_strategy=SelfHologramDamageCalculationStrategy(),
        )


class HologramAssault(CombatAction):
    """Self Hologram's basic attack."""

    @override
    def execute(self) -> DamageInstance:
        label: str = "Hologram Assault (Self Hologram)"
        base_potency: int = 100

        tags: set[DamageTag] = {
            DamageTag.HYDRO,
            DamageTag.PHASE,
            DamageTag.PHYSICAL_SUMMON,
            DamageTag.TARGETED,
            DamageTag.BASIC,
        }

        return DamageInstance(
            label=label,
            base_potency=base_potency,
            tags=tags,
            group_name="Hologram Assault (Self Hologram)",
            damage_calculation_strategy=SelfHologramDamageCalculationStrategy(),
        )


class HologramAssaultV2(CombatAction):
    """Self Hologram's basic attack."""

    @override
    def execute(self) -> DamageInstance:
        label: str = "Hologram Assault (Self Hologram)"
        base_potency: int = 120

        tags: set[DamageTag] = {
            DamageTag.HYDRO,
            DamageTag.PHASE,
            DamageTag.PHYSICAL_SUMMON,
            DamageTag.TARGETED,
            DamageTag.BASIC,
        }

        return DamageInstance(
            label=label,
            base_potency=base_potency,
            tags=tags,
            group_name="Hologram Assault (Self Hologram)",
            damage_calculation_strategy=SelfHologramDamageCalculationStrategy(),
        )


class Mityl(Doll):
    """Mityl."""

    name: str = "Mityl"
    irrelevant_damage_tags: ClassVar[set[DamageTag]] = set(
        [
            DamageTag.CORROSION,
            DamageTag.BURN,
            DamageTag.FREEZE,
            DamageTag.ELECTRIC,
            DamageTag.MELEE,
            DamageTag.HEAVY_AMMO,
            DamageTag.MEDIUM_AMMO,
            DamageTag.SHOTGUN_AMMO,
            DamageTag.COUNTERATTACK,
            DamageTag.INTERCEPTION,
            DamageTag.FIXED,
        ]
    )

    assault_shot: CombatAction = Field(default_factory=AssaultShot)
    air_dash: CombatAction = Field(default_factory=AirDash)
    support_action: CombatAction = Field(default_factory=SupportAction)
    aligned_resonance: CombatAction = Field(default_factory=AlignedResonance)
    hologram_assault: CombatAction = Field(default_factory=HologramAssault)

    def _build_self_hologram(self) -> PhysicalSummonedUnit:
        # Self Hologram inherits all of Mityl's initial attributes.
        initial_stats, additive_modifiers, multiplicative_modifiers = (
            build_physical_summon_stat_snapshot(self)
        )
        self_hologram: PhysicalSummonedUnit = PhysicalSummonedUnit(
            name="Self Hologram",
            initial_stats=initial_stats,
            additive_modifiers=additive_modifiers,
            multiplicative_modifiers=multiplicative_modifiers,
        )

        return self_hologram

    def summon_self_hologram(self) -> None:
        """Summons Self Hologram with a snapshot of Mityl's current stats."""
        if super().get_summoned_unit("Self Hologram") is None:
            self.summoned_units.append(self._build_self_hologram())

    def refresh_self_hologram(self) -> None:
        """Replaces Self Hologram with a fresh snapshot of Mityl's current stats.

        Call this whenever Mityl's stats have been mutated so that subsequent
        deepcopy-based damage calculations see up-to-date Self Hologram stats.
        """
        self.summoned_units = [
            u for u in self.summoned_units if u.name != "Self Hologram"
        ]
        self.summoned_units.append(self._build_self_hologram())

    @override
    def prepare_for_calculation(self) -> None:
        self.refresh_self_hologram()

    @override
    def get_summoned_unit(self, name: str) -> SummonedUnit | None:
        self.summon_self_hologram()
        return super().get_summoned_unit(name)

    def set_to_v0(self) -> None:
        """Sets Fortification Level to Segment00."""
        self.assault_shot = AssaultShot()
        self.air_dash = AirDash()
        self.support_action = SupportAction()
        self.aligned_resonance = AlignedResonance()
        self.hologram_assault = HologramAssault()

        self.summon_self_hologram()

    def set_to_v1(self) -> None:
        """Sets Fortification Level to Segment01."""
        self.set_to_v0()

        self.aligned_resonance = AlignedResonanceV1()

    def set_to_v2(self) -> None:
        """Sets Fortification Level to Segment02."""
        self.set_to_v1()

        self.hologram_assault = HologramAssaultV2()

    def set_to_v4(self) -> None:
        """Sets Fortification Level to Segment04."""
        self.set_to_v2()
        self.air_dash = AirDashV4()

    def set_to_v5(self) -> None:
        """Sets Fortification Level to Segment05."""
        self.set_to_v4()

        self.support_action = SupportActionV5()

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
                self.set_to_v4()
            case FortificationLevel.SEGMENT05:
                self.set_to_v5()
            case FortificationLevel.SEGMENT06:
                self.set_to_v5()
