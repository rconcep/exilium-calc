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


class RecklessProvocation(CombatAction):
    """Basti Basic Attack."""

    @override
    def execute(self) -> DamageInstance:
        label: str = "Reckless Provocation"
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
            group_name="Reckless Provocation",
        )


class SelfDestruct(CombatAction):
    """Cutie Pie summon's Self-Destruct."""

    @override
    def execute(
        self,
    ) -> DamageInstance:
        label: str = "Self-Destruct (Cutie Pie)"
        base_potency: int = 100
        tags: set[DamageTag] = {
            DamageTag.ACTIVE,
            DamageTag.CORROSION,
            DamageTag.PHASE,
            DamageTag.AREA_OF_EFFECT,
        }

        return DamageInstance(
            label=label,
            base_potency=base_potency,
            tags=tags,
            group_name="Self-Destruct (Cutie Pie)",
        )


class SelfDestructV6(CombatAction):
    """Cutie Pie summon's Self-Destruct (V6)."""

    @override
    def execute(
        self,
    ) -> DamageInstance:
        label: str = "Self-Destruct (Cutie Pie)"
        base_potency: int = 130
        tags: set[DamageTag] = {
            DamageTag.ACTIVE,
            DamageTag.CORROSION,
            DamageTag.PHASE,
            DamageTag.AREA_OF_EFFECT,
        }

        return DamageInstance(
            label=label,
            base_potency=base_potency,
            tags=tags,
            group_name="Self-Destruct (Cutie Pie)",
        )


class CandyCoatedCarnage(CombatAction):
    """Basti's ultimate."""

    @override
    def execute(
        self,
        number_of_targets_hit: int,
    ) -> DamageInstance:
        label: str = "Candy-Coated Carnage"
        base_potency: int = 150
        tags: set[DamageTag] = {
            DamageTag.ACTIVE,
            DamageTag.CORROSION,
            DamageTag.PHASE,
            DamageTag.AREA_OF_EFFECT,
            DamageTag.ULTIMATE,
        }

        return DamageInstance(
            label=label,
            base_potency=base_potency,
            tags=tags,
            group_name="Candy-Coated Carnage",
        )


class CandyCoatedCarnageV4(CombatAction):
    """Basti's ultimate (V4)."""

    @override
    def execute(
        self,
        number_of_targets_hit: int,
    ) -> DamageInstance:
        label: str = "Candy-Coated Carnage"
        base_potency: int = 200
        tags: set[DamageTag] = {
            DamageTag.ACTIVE,
            DamageTag.CORROSION,
            DamageTag.PHASE,
            DamageTag.AREA_OF_EFFECT,
            DamageTag.ULTIMATE,
        }

        return DamageInstance(
            label=label,
            base_potency=base_potency,
            tags=tags,
            group_name="Candy-Coated Carnage",
        )


class CandyCoatedCarnageV5(CombatAction):
    """Basti's ultimate."""

    @override
    def execute(
        self,
        number_of_targets_hit: int,
    ) -> DamageInstance:
        label: str = "Candy-Coated Carnage"
        base_potency: int = 200
        tags: set[DamageTag] = {
            DamageTag.ACTIVE,
            DamageTag.CORROSION,
            DamageTag.PHASE,
            DamageTag.AREA_OF_EFFECT,
            DamageTag.ULTIMATE,
        }

        # For each target hit, the damage dealt is increased by 20%, up to a maximum of 100% increased damage at 5 targets hit.
        damage_increase_per_target = 20
        max_damage_increase = 100
        damage_increase_from_targets_hit = min(
            number_of_targets_hit * damage_increase_per_target, max_damage_increase
        )

        buffs_before: list[Buff] = [
            Buff(
                damage_increase_from_targets_hit,
                ModifierType.ADDITIVE,
                SpecialAttribute.DAMAGE_BOOST,
                DamageTag.ULTIMATE,
            )
        ]

        return DamageInstance(
            label=label,
            base_potency=base_potency,
            tags=tags,
            group_name="Candy-Coated Carnage",
            buffs_before=buffs_before,
        )


class Grudge(CombatAction):
    """Special support attack triggered before a holder of the Grudge debuff within range of Basti attacks."""

    @override
    def execute(
        self,
    ) -> DamageInstance:
        label: str = "Grudge"
        base_potency: int = 100
        tags: set[DamageTag] = {
            DamageTag.PASSIVE,
            DamageTag.CORROSION,
            DamageTag.PHASE,
            DamageTag.AREA_OF_EFFECT,
            DamageTag.SUPPORT_ACTION,
        }

        return DamageInstance(
            label=label,
            base_potency=base_potency,
            tags=tags,
            group_name="Grudge",
        )


class GrudgeV5(CombatAction):
    """Special support attack triggered before a holder of the Grudge debuff within range of Basti attacks."""

    @override
    def execute(
        self,
    ) -> DamageInstance:
        label: str = "Grudge"
        base_potency: int = 200
        tags: set[DamageTag] = {
            DamageTag.PASSIVE,
            DamageTag.CORROSION,
            DamageTag.PHASE,
            DamageTag.AREA_OF_EFFECT,
            DamageTag.SUPPORT_ACTION,
        }

        return DamageInstance(
            label=label,
            base_potency=base_potency,
            tags=tags,
            group_name="Grudge",
        )


class Basti(Doll):
    """Basti."""

    name: str = "Basti"
    irrelevant_damage_tags: ClassVar[set[DamageTag]] = set(
        [
            DamageTag.ELECTRIC,
            DamageTag.BURN,
            DamageTag.HYDRO,
            DamageTag.FREEZE,
            DamageTag.MEDIUM_AMMO,
            DamageTag.HEAVY_AMMO,
            DamageTag.SHOTGUN_AMMO,
            DamageTag.INTERCEPTION,
            DamageTag.COUNTERATTACK,
            DamageTag.FIXED,
        ]
    )

    reckless_provocation: CombatAction = Field(default_factory=RecklessProvocation)
    self_destruct: CombatAction = Field(default_factory=SelfDestruct)
    candy_coated_carnage: CombatAction = Field(default_factory=CandyCoatedCarnage)
    grudge: CombatAction = Field(default_factory=Grudge)

    def set_to_v0(self) -> None:
        """Sets Fortification Level to Segment00."""
        self.reckless_provocation = RecklessProvocation()
        self.self_destruct = SelfDestruct()
        self.candy_coated_carnage = CandyCoatedCarnage()
        self.grudge = Grudge()

    def set_to_v4(self) -> None:
        """Sets Fortification Level to Segment04."""
        self.set_to_v0()
        self.candy_coated_carnage = CandyCoatedCarnageV4()

    def set_to_v5(self) -> None:
        """Sets Fortification Level to Segment05."""
        self.set_to_v4()
        self.candy_coated_carnage = CandyCoatedCarnageV5()
        self.grudge = GrudgeV5()

    def set_to_v6(self) -> None:
        """Sets Fortification Level to Segment06."""
        self.set_to_v5()
        self.self_destruct = SelfDestructV6()

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
                self.set_to_v0()
            case FortificationLevel.SEGMENT04:
                self.set_to_v4()
            case FortificationLevel.SEGMENT05:
                self.set_to_v5()
            case FortificationLevel.SEGMENT06:
                self.set_to_v6()
