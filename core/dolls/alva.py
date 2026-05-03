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
)
from core.buffs import Buff
from core.combat import DamageInstance, CombatAction


class Laceration(CombatAction):
    """Alva basic attack."""

    @override
    def execute(self) -> DamageInstance:
        label: str = "Laceration"
        base_potency: int = 80
        tags: set[DamageTag] = {
            DamageTag.ACTIVE,
            DamageTag.BASIC,
            DamageTag.MEDIUM_AMMO,
            DamageTag.TARGETED,
            DamageTag.PHYSICAL,
        }

        return DamageInstance(
            label=label,
            base_potency=base_potency,
            tags=tags,
            group_name="Laceration",
        )


class SnowWolfsHeart(CombatAction):
    """Alva S1."""

    @override
    def execute(self) -> DamageInstance:
        label: str = "Snow Wolf's Heart"
        base_potency: int = 100
        tags: set[DamageTag] = {
            DamageTag.ACTIVE,
            DamageTag.MEDIUM_AMMO,
            DamageTag.TARGETED,
            DamageTag.FREEZE,
            DamageTag.PHASE,
        }

        return DamageInstance(
            label=label,
            base_potency=base_potency,
            tags=tags,
            group_name="Snow Wolf's Heart",
        )


class FrostedEcho(CombatAction):
    """Alva S2."""

    @override
    def execute(self, confectance_index: int = 0) -> DamageInstance:
        label: str = "Frosted Echo"
        tags: set[DamageTag] = {
            DamageTag.ACTIVE,
            DamageTag.CONFECTANCE,
            DamageTag.AREA_OF_EFFECT,
            DamageTag.FREEZE,
            DamageTag.PHASE,
        }

        potency_per_confectance_index: int = 15
        base_potency: int = potency_per_confectance_index * confectance_index

        return DamageInstance(
            label=label,
            base_potency=base_potency,
            tags=tags,
            group_name="Frosted Echo",
        )


class FrostedEchoV1(CombatAction):
    """Alva S2 (V1)."""

    @override
    def execute(self, confectance_index: int = 0) -> DamageInstance:
        label: str = "Frosted Echo"
        tags: set[DamageTag] = {
            DamageTag.ACTIVE,
            DamageTag.CONFECTANCE,
            DamageTag.AREA_OF_EFFECT,
            DamageTag.FREEZE,
            DamageTag.PHASE,
        }

        potency_per_confectance_index: int = 20
        base_potency: int = potency_per_confectance_index * confectance_index

        return DamageInstance(
            label=label,
            base_potency=base_potency,
            tags=tags,
            group_name="Frosted Echo",
        )


class HoarfrostBreak(CombatAction):
    """Alva's attack when an enemy's Hoarfrost shield is broken."""

    @override
    def execute(self) -> DamageInstance:
        label: str = "Hoarfrost Break"
        tags: set[DamageTag] = {
            DamageTag.PASSIVE,
            DamageTag.TARGETED,
            DamageTag.FREEZE,
            DamageTag.PHASE,
        }

        # Shield size is up to 500% of Alva's Attack, so this is essentially a 200 potency attack at max shield size.
        base_potency: int = 200

        return DamageInstance(
            label=label,
            base_potency=base_potency,
            tags=tags,
            group_name="Hoarfrost Break",
        )


class HoarfrostBreakV5(CombatAction):
    """Alva's attack when an enemy's Hoarfrost shield is broken (V5)."""

    @override
    def execute(self) -> DamageInstance:
        label: str = "Hoarfrost Break"
        tags: set[DamageTag] = {
            DamageTag.PASSIVE,
            DamageTag.TARGETED,
            DamageTag.FREEZE,
            DamageTag.PHASE,
        }

        # Shield size is up to 500% of Alva's Attack, so this is essentially a 300 potency attack at max shield size.
        base_potency: int = 300

        return DamageInstance(
            label=label,
            base_potency=base_potency,
            tags=tags,
            group_name="Hoarfrost Break",
        )


class NixRequiem(CombatAction):
    """Alva Ultimate."""

    @override
    def execute(self, confectance_index: int = 0) -> DamageInstance:
        label: str = "Nix Requiem"
        tags: set[DamageTag] = {
            DamageTag.ACTIVE,
            DamageTag.FREEZE,
            DamageTag.CONFECTANCE,
            DamageTag.PHASE,
            DamageTag.MEDIUM_AMMO,
            DamageTag.TARGETED,
            DamageTag.ULTIMATE,
        }

        potency_per_confectance_index: int = 30
        base_potency: int = potency_per_confectance_index * confectance_index

        return DamageInstance(
            label=label,
            base_potency=base_potency,
            tags=tags,
            group_name="Nix Requiem",
        )


class NixRequiemV2(CombatAction):
    """Alva Ultimate (V2)."""

    @override
    def execute(self, confectance_index: int = 0) -> DamageInstance:
        label: str = "Nix Requiem"
        tags: set[DamageTag] = {
            DamageTag.ACTIVE,
            DamageTag.FREEZE,
            DamageTag.CONFECTANCE,
            DamageTag.PHASE,
            DamageTag.MEDIUM_AMMO,
            DamageTag.TARGETED,
            DamageTag.ULTIMATE,
        }

        potency_per_confectance_index: int = 40
        base_potency: int = potency_per_confectance_index * confectance_index

        return DamageInstance(
            label=label,
            base_potency=base_potency,
            tags=tags,
            group_name="Nix Requiem",
        )


class Interception(CombatAction):
    """Interception from Covering Mode."""

    @override
    def execute(self) -> DamageInstance:
        label: str = "Interception"
        base_potency: int = 60
        tags: set[DamageTag] = {
            DamageTag.PASSIVE,
            DamageTag.INTERCEPTION,
            DamageTag.MEDIUM_AMMO,
            DamageTag.TARGETED,
            DamageTag.FREEZE,
            DamageTag.PHASE,
        }

        return DamageInstance(
            label=label,
            base_potency=base_potency,
            tags=tags,
            group_name="Interception",
        )


class Alva(Doll):
    """Alva."""

    name: str = "Alva"
    irrelevant_damage_tags: ClassVar[set[DamageTag]] = set(
        [
            DamageTag.CORROSION,
            DamageTag.HYDRO,
            DamageTag.BURN,
            DamageTag.ELECTRIC,
            DamageTag.MELEE,
            DamageTag.LIGHT_AMMO,
            DamageTag.HEAVY_AMMO,
            DamageTag.SHOTGUN_AMMO,
            DamageTag.SUPPORT_ACTION,
            DamageTag.COUNTERATTACK,
            DamageTag.FIXED,
        ]
    )

    laceration: CombatAction = Field(default_factory=Laceration)
    snow_wolfs_heart: CombatAction = Field(default_factory=SnowWolfsHeart)
    frosted_echo: CombatAction = Field(default_factory=FrostedEcho)
    hoarfrost_break: CombatAction = Field(default_factory=HoarfrostBreak)
    nix_requiem: CombatAction = Field(default_factory=NixRequiem)
    interception: CombatAction = Field(default_factory=Interception)

    def set_to_v0(self) -> None:
        """Sets Fortification Level to Segment00."""
        self.laceration: CombatAction = Laceration()
        self.snow_wolfs_heart: CombatAction = SnowWolfsHeart()
        self.frosted_echo: CombatAction = FrostedEcho()
        self.hoarfrost_break: CombatAction = HoarfrostBreak()
        self.nix_requiem: CombatAction = NixRequiem()
        self.interception: CombatAction = Interception()

        # Covering Mode: grants 20% critical hit rate - assumed to be active at all times.
        self.initial_stats.conditional_basic_attributes[
            StatType.CRIT_RATE
        ].set_multiplier(DamageTag.ALL, 20)

    def set_to_v1(self) -> None:
        """Sets Fortification Level to Segment01."""
        self.set_to_v0()

        self.frosted_echo: CombatAction = FrostedEchoV1()

    def set_to_v2(self) -> None:
        """Sets Fortification Level to Segment02."""
        self.set_to_v1()

        self.nix_requiem: CombatAction = NixRequiemV2()

    def set_to_v5(self) -> None:
        """Sets Fortification Level to Segment05."""
        self.set_to_v2()

        self.hoarfrost_break: CombatAction = HoarfrostBreakV5()

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
                self.set_to_v2()
            case FortificationLevel.SEGMENT05:
                self.set_to_v5()
            case FortificationLevel.SEGMENT06:
                self.set_to_v5()
