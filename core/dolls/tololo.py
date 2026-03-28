from typing import override, ClassVar
from pydantic import Field

from core.types import (
    DamageTag,
    ModifierType,
    SpecialAttribute,
    Doll,
    FortificationLevel,
    SummonedUnit,
)
from core.buffs import Buff
from core.combat import DamageInstance, CombatAction


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

    def set_to_v0(self) -> None:
        """Sets Fortification Level to Segment00."""
        self.meteor: CombatAction = Meteor()
        self.black_hole_inversion: CombatAction = BlackHoleInversion()
        self.supernova_impact: CombatAction = SupernovaImpact()
        self.morte_lumina: CombatAction = MorteLumina()

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

    def get_sample_data(self) -> list[DamageInstance]:
        """Returns a sample single target rotation."""
        rotation_data: list[DamageInstance] = [
            # Turn 1
            self.morte_lumina.execute(number_of_active_buffs=3),
            self.supernova_impact.execute(number_of_active_buffs=3),
            self.black_hole_inversion.execute(),
            # Turn 2
            self.morte_lumina.execute(number_of_active_buffs=3),
            self.supernova_impact.execute(number_of_active_buffs=3),
            self.black_hole_inversion.execute(),
            # Turn 3
            self.morte_lumina.execute(number_of_active_buffs=3),
            self.supernova_impact.execute(number_of_active_buffs=3),
            self.black_hole_inversion.execute(),
            # Turn 4
            self.morte_lumina.execute(number_of_active_buffs=3),
            self.supernova_impact.execute(number_of_active_buffs=3),
            self.black_hole_inversion.execute(),
            # Turn 5
            self.morte_lumina.execute(number_of_active_buffs=3),
            self.supernova_impact.execute(number_of_active_buffs=3),
            self.black_hole_inversion.execute(),
            # Turn 6
            self.morte_lumina.execute(number_of_active_buffs=3),
            self.supernova_impact.execute(number_of_active_buffs=3),
            self.black_hole_inversion.execute(),
            # Turn 7
            self.morte_lumina.execute(number_of_active_buffs=3),
            self.supernova_impact.execute(number_of_active_buffs=3),
            self.morte_lumina.execute(number_of_active_buffs=3),
        ]

        return rotation_data
