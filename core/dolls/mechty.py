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


class BedtimeWarmup(CombatAction):
    """Mechty Basic Attack."""

    @override
    def execute(
        self, in_turbo_mode: bool, enhanced_by_dreamquake: bool, is_sleepwalking: bool
    ) -> DamageInstance:
        label: str = "Bedtime Warmup"
        base_potency: int = 80

        tags: set[DamageTag] = {
            DamageTag.ACTIVE,
            DamageTag.BASIC,
            DamageTag.MEDIUM_AMMO,
            DamageTag.TARGETED,
            DamageTag.PHYSICAL,
        }

        # When in Turbo Mode, damage type is changed to Corrosion damage
        if in_turbo_mode:
            tags.remove(DamageTag.PHYSICAL)
            tags.add(DamageTag.CORROSION)
            tags.add(DamageTag.PHASE)

        buffs_before: list[Buff] = []

        if enhanced_by_dreamquake:
            buffs_before.append(
                Buff(
                    100,
                    ModifierType.ADDITIVE,
                    SpecialAttribute.DAMAGE_BOOST,
                    DamageTag.BASIC,
                )
            )

        if is_sleepwalking:
            base_potency = 130

        return DamageInstance(
            label=label,
            base_potency=base_potency,
            tags=tags,
            group_name="Bedtime Warmup",
            buffs_before=buffs_before,
        )


class Dreamquake(CombatAction):
    """Mechty S1."""

    @override
    def execute(
        self,
    ) -> DamageInstance:
        label: str = "Dreamquake"
        base_potency: int = 130
        tags: set[DamageTag] = {
            DamageTag.ACTIVE,
            DamageTag.CORROSION,
            DamageTag.PHASE,
            DamageTag.MEDIUM_AMMO,
            DamageTag.AREA_OF_EFFECT,
        }

        return DamageInstance(
            label=label,
            base_potency=base_potency,
            tags=tags,
            group_name="Dreamquake",
        )


class Mechty(Doll):
    """Mechty."""

    name: str = "Mechty"
    irrelevant_damage_tags: ClassVar[set[DamageTag]] = set(
        [
            DamageTag.ELECTRIC,
            DamageTag.BURN,
            DamageTag.HYDRO,
            DamageTag.FREEZE,
            DamageTag.LIGHT_AMMO,
            DamageTag.HEAVY_AMMO,
            DamageTag.SHOTGUN_AMMO,
            DamageTag.SUPPORT_ACTION,
            DamageTag.INTERCEPTION,
            DamageTag.COUNTERATTACK,
            DamageTag.PHYSICAL_SUMMON,
            DamageTag.FIXED,
        ]
    )

    bedtime_warmup: CombatAction = Field(default_factory=BedtimeWarmup)
    dreamquake: CombatAction = Field(default_factory=Dreamquake)

    def set_to_v0(self) -> None:
        """Sets Fortification Level to Segment00."""
        self.bedtime_warmup = BedtimeWarmup()
        self.dreamquake = Dreamquake()

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
                self.set_to_v0()
            case FortificationLevel.SEGMENT05:
                self.set_to_v0()
            case FortificationLevel.SEGMENT06:
                self.set_to_v0()
