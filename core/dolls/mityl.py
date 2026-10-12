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
    HologramCloneDamageCalculationStrategy,
)


class Ambush(CombatAction):
    """Mityl Basic Attack."""

    @override
    def execute(self) -> DamageInstance:
        label: str = "Ambush"
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
            group_name="Ambush",
        )


class AerialDash(CombatAction):
    """Mityl S2."""

    @override
    def execute(
        self,
        starting_tile_is_hydro_tile: bool,
        ending_tile_is_hydro_tile: bool,
    ) -> DamageInstance:
        label: str = "Aerial Dash"
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

        # TODO: Dandegate description says under this condition, "this skill can be used again and the damage dealt is increased by 30%".
        # This interpretation assumes that the increased damage dealt applies to the first instance and not the instance of the skill
        # used again. One could interpret it as the increased damage only applies to the subsequent use of the skill.
        if starting_tile_is_hydro_tile and ending_tile_is_hydro_tile:
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
            group_name="Aerial Dash",
            buffs_before=buffs_before,
        )


class AerialDashV4(CombatAction):
    """Mityl S2 (V4)."""

    @override
    def execute(
        self,
        starting_tile_is_hydro_tile: bool,
        ending_tile_is_hydro_tile: bool,
    ) -> DamageInstance:
        label: str = "Aerial Dash"
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

        # TODO: Dandegate description says under this condition, "this skill can be used again and the damage dealt is increased by 50%".
        # This interpretation assumes that the increased damage dealt applies to the first instance and not the instance of the skill
        # used again. One could interpret it as the increased damage only applies to the subsequent use of the skill.
        if starting_tile_is_hydro_tile or ending_tile_is_hydro_tile:
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
            group_name="Aerial Dash",
            buffs_before=buffs_before,
        )


class SupportAction(CombatAction):
    """Hologram - Clone's Support Action after Mityl uses her S2."""

    @override
    def execute(self) -> DamageInstance:
        label: str = "Support Action (Hologram - Clone)"
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
            group_name="Support Action (Hologram - Clone)",
            damage_calculation_strategy=HologramCloneDamageCalculationStrategy(),
        )


class SupportActionV5(CombatAction):
    """Hologram - Clone's Support Action after Mityl uses her S2."""

    @override
    def execute(self) -> DamageInstance:
        label: str = "Support Action (Hologram - Clone)"
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
            group_name="Support Action (Hologram - Clone)",
            damage_calculation_strategy=HologramCloneDamageCalculationStrategy(),
        )


class ConvergenceResonance(CombatAction):
    """Hologram - Clone's action used at the end of the allied turn."""

    @override
    def execute(self) -> DamageInstance:
        label: str = "Convergence Resonance (Hologram - Clone)"
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
            group_name="Convergence Resonance (Hologram - Clone)",
            damage_calculation_strategy=HologramCloneDamageCalculationStrategy(),
        )


class ConvergenceResonanceV1(CombatAction):
    """Hologram - Clone's action used at the end of the allied turn."""

    @override
    def execute(self) -> DamageInstance:
        label: str = "Convergence Resonance (Hologram - Clone)"
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
            group_name="Convergence Resonance (Hologram - Clone)",
            damage_calculation_strategy=HologramCloneDamageCalculationStrategy(),
        )


class HologramStrike(CombatAction):
    """Hologram - Clone's basic attack."""

    @override
    def execute(self) -> DamageInstance:
        label: str = "Hologram Strike (Hologram - Clone)"
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
            group_name="Hologram Strike (Hologram - Clone)",
            damage_calculation_strategy=HologramCloneDamageCalculationStrategy(),
        )


class HologramStrikeV2(CombatAction):
    """Hologram - Clone's basic attack."""

    @override
    def execute(self) -> DamageInstance:
        label: str = "Hologram Strike (Hologram - Clone)"
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
            group_name="Hologram Strike (Hologram - Clone)",
            damage_calculation_strategy=HologramCloneDamageCalculationStrategy(),
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

    ambush: CombatAction = Field(default_factory=Ambush)
    aerial_dash: CombatAction = Field(default_factory=AerialDash)
    support_action: CombatAction = Field(default_factory=SupportAction)
    convergence_resonance: CombatAction = Field(default_factory=ConvergenceResonance)
    hologram_strike: CombatAction = Field(default_factory=HologramStrike)

    def _build_hologram_clone(self) -> PhysicalSummonedUnit:
        # Hologram - Clone inherits all of Mityl's initial attributes.
        initial_stats, additive_modifiers, multiplicative_modifiers = (
            build_physical_summon_stat_snapshot(self)
        )
        hologram_clone: PhysicalSummonedUnit = PhysicalSummonedUnit(
            name="Hologram - Clone",
            initial_stats=initial_stats,
            additive_modifiers=additive_modifiers,
            multiplicative_modifiers=multiplicative_modifiers,
        )

        return hologram_clone

    def summon_hologram_clone(self) -> None:
        """Summons Hologram - Clone with a snapshot of Mityl's current stats."""
        if super().get_summoned_unit("Hologram - Clone") is None:
            self.summoned_units.append(self._build_hologram_clone())

    def refresh_hologram_clone(self) -> None:
        """Replaces Hologram - Clone with a fresh snapshot of Mityl's current stats.

        Call this whenever Mityl's stats have been mutated so that subsequent
        deepcopy-based damage calculations see up-to-date Hologram - Clone stats.
        """
        self.summoned_units = [
            u for u in self.summoned_units if u.name != "Hologram - Clone"
        ]
        self.summoned_units.append(self._build_hologram_clone())

    @override
    def prepare_for_calculation(self) -> None:
        self.refresh_hologram_clone()

    @override
    def get_summoned_unit(self, name: str) -> SummonedUnit | None:
        self.summon_hologram_clone()
        return super().get_summoned_unit(name)

    def set_to_v0(self) -> None:
        """Sets Fortification Level to Segment00."""
        self.ambush = Ambush()
        self.aerial_dash = AerialDash()
        self.support_action = SupportAction()
        self.convergence_resonance = ConvergenceResonance()
        self.hologram_strike = HologramStrike()

        self.summon_hologram_clone()

    def set_to_v1(self) -> None:
        """Sets Fortification Level to Segment01."""
        self.set_to_v0()

        self.convergence_resonance = ConvergenceResonanceV1()

    def set_to_v2(self) -> None:
        """Sets Fortification Level to Segment02."""
        self.set_to_v1()

        self.hologram_strike = HologramStrikeV2()

    def set_to_v4(self) -> None:
        """Sets Fortification Level to Segment04."""
        self.set_to_v2()
        self.aerial_dash = AerialDashV4()

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


# TODO: Buffs/debuffs to implement
# * Saturation Overflow
#   * Note: base version specifies attack boost for buff holder while V3 version
#     specifies attack boost for buff holder and their Hologram. Due to snapshotting
#     the base version will inadvertently apply the boost to the Hologram as implemented.
# * Screen Title / separate each rank into separate buffs since they are cumulative
# * Mimic Rookie
#   * Critical rate of user and Hologram
# * Understudy
#   * Critical damage of the user and Hologram
# * Legendary Star
#   * Damage dealt by user and Hologram is increased <per allied unit on the field>
# * Convergence Amplification (V6)
#   * Damage dealt by Hologram (buff holder) increased by 15% per stack, up to 6 times
