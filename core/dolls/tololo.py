from typing import override, ClassVar
from pydantic import Field

from core.types import (
    DamageTag,
    ModifierType,
    StatType,
    SpecialAttribute,
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
    GeostationarySatelliteDamageCalculationStrategy,
)


class Meteor(CombatAction):
    """Tololo Basic Attack."""

    @override
    def execute(self) -> DamageInstance:
        label: str = "Meteor"
        base_potency: int = 80
        tags: set[DamageTag] = {
            DamageTag.ACTIVE,
            DamageTag.BASIC,
            DamageTag.PHYSICAL,
            DamageTag.MEDIUM_AMMO,
            DamageTag.TARGETED,
        }

        return DamageInstance(
            label=label, base_potency=base_potency, tags=tags, group_name="Meteor"
        )


class BlackHoleInversion(CombatAction):
    """Tololo S1."""

    @override
    def execute(self) -> DamageInstance:
        label: str = "Black Hole Inversion"
        base_potency: int = 130
        tags: set[DamageTag] = {
            DamageTag.ACTIVE,
            DamageTag.PHASE,
            DamageTag.HYDRO,
            DamageTag.MEDIUM_AMMO,
            DamageTag.TARGETED,
        }

        return DamageInstance(
            label=label,
            base_potency=base_potency,
            tags=tags,
            group_name="Black Hole Inversion",
        )


class SupernovaImpact(CombatAction):
    """Tololo S2."""

    @override
    def execute(self, number_of_active_buffs: int = 0) -> DamageInstance:
        label: str = "Supernova Impact"
        base_potency: int = 130

        buffs_before: list[Buff] = []

        if number_of_active_buffs >= 2:
            buffs_before.append(
                Buff(
                    20,
                    ModifierType.ADDITIVE,
                    SpecialAttribute.DAMAGE_BOOST,
                    DamageTag.ALL,
                )
            )

        tags: set[DamageTag] = {
            DamageTag.ACTIVE,
            DamageTag.PHYSICAL,
            DamageTag.MEDIUM_AMMO,
            DamageTag.TARGETED,
        }

        return DamageInstance(
            label=label,
            base_potency=base_potency,
            tags=tags,
            group_name="Supernova Impact",
            buffs_before=buffs_before,
        )


class SupernovaImpactV2(CombatAction):
    """Tololo S2 (V2)."""

    @override
    def execute(self, number_of_active_buffs: int = 0) -> DamageInstance:
        label: str = "Supernova Impact"
        base_potency: int = 130

        tags: set[DamageTag] = {
            DamageTag.ACTIVE,
            DamageTag.MEDIUM_AMMO,
            DamageTag.TARGETED,
        }

        buffs_before: list[Buff] = []

        if number_of_active_buffs >= 2:
            buffs_before.append(
                Buff(
                    20,
                    ModifierType.ADDITIVE,
                    SpecialAttribute.DAMAGE_BOOST,
                    DamageTag.ALL,
                )
            )

        if number_of_active_buffs >= 3:
            tags.add(DamageTag.HYDRO)
            tags.add(DamageTag.PHASE)

        return DamageInstance(
            label=label,
            base_potency=base_potency,
            tags=tags,
            group_name="Supernova Impact",
            buffs_before=buffs_before,
        )


class MorteLumina(CombatAction):
    """Tololo Ultimate."""

    @override
    def execute(self, number_of_active_buffs: int = 0) -> DamageInstance:
        label: str = "Morte Lumina"
        base_potency: int = 180
        tags: set[DamageTag] = {
            DamageTag.ACTIVE,
            DamageTag.ULTIMATE,
            DamageTag.TARGETED,
            DamageTag.HYDRO,
            DamageTag.PHASE,
        }

        buffs_before: list[Buff] = []

        if number_of_active_buffs >= 3:
            buffs_before.append(
                Buff(
                    15,
                    ModifierType.ADDITIVE,
                    SpecialAttribute.DAMAGE_BOOST,
                    DamageTag.ALL,
                )
            )

        return DamageInstance(
            label=label,
            base_potency=base_potency,
            tags=tags,
            group_name="Morte Lumina",
            buffs_before=buffs_before,
        )


class MorteLuminaV3(CombatAction):
    """Tololo Ultimate (V3)."""

    @override
    def execute(self, number_of_active_buffs: int = 0) -> DamageInstance:
        label: str = "Morte Lumina"
        base_potency: int = 180
        tags: set[DamageTag] = {
            DamageTag.ACTIVE,
            DamageTag.ULTIMATE,
            DamageTag.TARGETED,
            DamageTag.HYDRO,
            DamageTag.PHASE,
        }

        buffs_before: list[Buff] = []

        if number_of_active_buffs >= 3:
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
            group_name="Morte Lumina",
            buffs_before=buffs_before,
        )


class CallOfTheStars(CombatAction):
    """Passive skill of Geostationary Satellite.

    Note: The buffs from Observation Advantage are encapsulated here as they only apply
    to the Geostationary Satellite.
    """

    @override
    def execute(self, stacks_of_observation_advantage: int = 0) -> DamageInstance:
        label: str = "Call of the Stars (Geostationary Satellite)"
        base_potency: int = 130
        tags: set[DamageTag] = {
            DamageTag.TARGETED,
            DamageTag.MEDIUM_AMMO,
            DamageTag.HYDRO,
            DamageTag.PHASE,
            DamageTag.PHYSICAL_SUMMON,
        }

        buffs_before: list[Buff] = []

        attack_boost: int = 0
        damage_boost: int = 0
        critical_damage: int = 0

        if stacks_of_observation_advantage >= 3:
            attack_boost = 10
            damage_boost = 40
            critical_damage = 10

            base_potency += 60
        elif stacks_of_observation_advantage >= 1:
            attack_boost = 5
            damage_boost = 20
            critical_damage = 5

        if stacks_of_observation_advantage > 0:
            buffs_before.append(
                Buff(
                    attack_boost,
                    ModifierType.MULTIPLICATIVE,
                    StatType.ATTACK,
                    DamageTag.PHYSICAL_SUMMON,
                )
            )
            buffs_before.append(
                Buff(
                    damage_boost,
                    ModifierType.ADDITIVE,
                    SpecialAttribute.DAMAGE_BOOST,
                    DamageTag.PHYSICAL_SUMMON,
                )
            )
            buffs_before.append(
                Buff(
                    critical_damage,
                    ModifierType.ADDITIVE,
                    SpecialAttribute.CRITICAL_DAMAGE,
                    DamageTag.PHYSICAL_SUMMON,
                )
            )

        return DamageInstance(
            label=label,
            base_potency=base_potency,
            tags=tags,
            group_name="Call of the Stars (Geostationary Satellite)",
            buffs_before=buffs_before,
            damage_calculation_strategy=GeostationarySatelliteDamageCalculationStrategy(),
        )


class Tololo(Doll):
    """Tololo."""

    name: str = "Tololo"
    irrelevant_damage_tags: ClassVar[set[DamageTag]] = set(
        [
            DamageTag.CORROSION,
            DamageTag.BURN,
            DamageTag.FREEZE,
            DamageTag.ELECTRIC,
            DamageTag.MELEE,
            DamageTag.LIGHT_AMMO,
            DamageTag.HEAVY_AMMO,
            DamageTag.SHOTGUN_AMMO,
            DamageTag.SUPPORT_ACTION,
            DamageTag.INTERCEPTION,
            DamageTag.COUNTERATTACK,
            DamageTag.AREA_OF_EFFECT,
            DamageTag.PASSIVE,
            DamageTag.CONFECTANCE,
        ]
    )

    meteor: CombatAction = Field(default_factory=Meteor)
    black_hole_inversion: CombatAction = Field(default_factory=BlackHoleInversion)
    supernova_impact: CombatAction = Field(default_factory=SupernovaImpact)
    morte_lumina: CombatAction = Field(default_factory=MorteLumina)
    call_of_the_stars: CombatAction = Field(default_factory=CallOfTheStars)

    def _build_geostationary_satellite(self) -> PhysicalSummonedUnit:
        # Geostationary Satellite inherits all of Tololo's initial attributes at 100%.
        initial_stats, additive_modifiers, multiplicative_modifiers = (
            build_physical_summon_stat_snapshot(self)
        )

        geostationary_satellite: PhysicalSummonedUnit = PhysicalSummonedUnit(
            name="Geostationary Satellite",
            initial_stats=initial_stats,
            additive_modifiers=additive_modifiers,
            multiplicative_modifiers=multiplicative_modifiers,
        )

        return geostationary_satellite

    def summon_geostationary_satellite(self) -> None:
        """Summons Geostationary Satellite with a snapshot of Tololo's current stats."""
        if super().get_summoned_unit("Geostationary Satellite") is None:
            self.summoned_units.append(self._build_geostationary_satellite())

    def refresh_geostationary_satellite(self) -> None:
        """Replaces Geostationary Satellite with a fresh snapshot of Tololo's current stats.

        Call this whenever Tololo's stats have been mutated so that subsequent
        deepcopy-based damage calculations see up-to-date Geostationary Satellite stats.
        """
        self.summoned_units = [
            u for u in self.summoned_units if u.name != "Geostationary Satellite"
        ]
        self.summoned_units.append(self._build_geostationary_satellite())

    @override
    def prepare_for_calculation(self) -> None:
        self.refresh_geostationary_satellite()

    @override
    def get_summoned_unit(self, name: str) -> SummonedUnit | None:
        self.summon_geostationary_satellite()
        return super().get_summoned_unit(name)

    def set_to_v0(self) -> None:
        """Sets Fortification Level to Segment00."""
        self.meteor: CombatAction = Meteor()
        self.black_hole_inversion: CombatAction = BlackHoleInversion()
        self.supernova_impact: CombatAction = SupernovaImpact()
        self.morte_lumina: CombatAction = MorteLumina()
        self.call_of_the_stars: CombatAction = CallOfTheStars()

        self.summon_geostationary_satellite()

    def set_to_v2(self) -> None:
        """Sets Fortification Level to Segment02."""
        self.set_to_v0()

        self.supernova_impact: CombatAction = SupernovaImpactV2()

    def set_to_v3(self) -> None:
        """Sets Fortification Level to Segment03."""
        self.set_to_v2()

        self.morte_lumina: CombatAction = MorteLuminaV3()

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
                self.set_to_v3()
            case FortificationLevel.SEGMENT05:
                self.set_to_v3()
            case FortificationLevel.SEGMENT06:
                self.set_to_v3()
