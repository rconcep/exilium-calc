from typing import override, ClassVar
from pydantic import Field

from core.types import (
    DamageTag,
    StatType,
    SpecialAttribute,
    ModifierType,
    Doll,
    FortificationLevel,
    SummonedUnit,
)
from core.buffs import Buff, DamageUpII
from core.combat import DamageInstance, CombatAction


class Fuse(CombatAction):
    """Qiongjiu basic attack."""

    @override
    def execute(self) -> DamageInstance:
        label: str = "Fuse"
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
            group_name="Fuse",
        )


class CommonRail(CombatAction):
    """Qiongjiu S1."""

    @override
    def execute(self, has_active_engagement: bool = False) -> DamageInstance:
        label: str = "Common Rail"
        base_potency: int = 150
        tags: set[DamageTag] = {
            DamageTag.ACTIVE,
            DamageTag.BURN,
            DamageTag.PHASE,
            DamageTag.MEDIUM_AMMO,
            DamageTag.TARGETED,
        }

        return DamageInstance(
            label=label,
            base_potency=base_potency,
            tags=tags,
            group_name="Common Rail",
        )


class GuideToVictory(CombatAction):
    """Qiongjiu S2."""

    @override
    def execute(
        self,
        target_has_overburn: bool,
        has_fixed_key_4: bool,
        is_secondary_target: bool,
    ) -> DamageInstance:
        label: str = "Guide to Victory"
        base_potency: int = 110
        tags: set[DamageTag] = {
            DamageTag.ACTIVE,
            DamageTag.AREA_OF_EFFECT,
            DamageTag.BURN,
            DamageTag.PHASE,
        }

        buffs_before: list[Buff] = []

        if has_fixed_key_4 and is_secondary_target:
            buffs_before.append(
                Buff(
                    value=-30,
                    modifier_type=ModifierType.ADDITIVE,
                    stat_type=SpecialAttribute.DAMAGE_BOOST,
                    tag=DamageTag.ALL,
                )
            )

        return DamageInstance(
            label=label,
            base_potency=base_potency,
            tags=tags,
            group_name="Guide to Victory",
            buffs_before=buffs_before,
        )


class GuideToVictoryV2(CombatAction):
    """Qiongjiu S2 (V2)."""

    @override
    def execute(
        self,
        target_has_overburn: bool,
        has_fixed_key_4: bool,
        is_secondary_target: bool,
    ) -> DamageInstance:
        label: str = "Guide to Victory"
        base_potency: int = 110
        tags: set[DamageTag] = {
            DamageTag.ACTIVE,
            DamageTag.AREA_OF_EFFECT,
            DamageTag.BURN,
            DamageTag.PHASE,
        }

        buffs_before: list[Buff] = []

        if target_has_overburn:
            buffs_before.append(
                Buff(
                    value=100,
                    modifier_type=ModifierType.ADDITIVE,
                    stat_type=StatType.CRIT_RATE,
                    tag=DamageTag.ALL,
                )
            )

        if has_fixed_key_4 and is_secondary_target:
            buffs_before.append(
                Buff(
                    value=-30,
                    modifier_type=ModifierType.ADDITIVE,
                    stat_type=SpecialAttribute.DAMAGE_BOOST,
                    tag=DamageTag.ALL,
                )
            )

        return DamageInstance(
            label=label,
            base_potency=base_potency,
            tags=tags,
            group_name="Guide to Victory",
            buffs_before=buffs_before,
        )


class SupportAction(CombatAction):
    """Support action."""

    @override
    def execute(self, has_expansion_key: bool = True) -> DamageInstance:
        label: str = "Support Action"
        base_potency: int = 90
        tags: set[DamageTag] = {
            DamageTag.PASSIVE,
            DamageTag.SUPPORT_ACTION,
            DamageTag.MEDIUM_AMMO,
            DamageTag.TARGETED,
        }

        buffs_before: list[Buff] = []

        if has_expansion_key:
            tags.add(DamageTag.BURN)
            tags.add(DamageTag.PHASE)
        else:
            tags.add(DamageTag.PHYSICAL)

        return DamageInstance(
            label=label,
            base_potency=base_potency,
            tags=tags,
            group_name="Support Action",
            buffs_before=buffs_before,
        )


class SupportActionV3(CombatAction):
    """Support action (V3)."""

    @override
    def execute(self, has_expansion_key: bool = True) -> DamageInstance:
        label: str = "Support Action"
        base_potency: int = 90
        tags: set[DamageTag] = {
            DamageTag.PASSIVE,
            DamageTag.SUPPORT_ACTION,
            DamageTag.MEDIUM_AMMO,
            DamageTag.TARGETED,
        }

        buffs_before: list[Buff] = []

        buffs_before.append(
            Buff(
                value=10,
                modifier_type=ModifierType.ADDITIVE,
                stat_type=SpecialAttribute.DAMAGE_BOOST,
                tag=DamageTag.SUPPORT_ACTION,
            )
        )

        if has_expansion_key:
            tags.add(DamageTag.BURN)
            tags.add(DamageTag.PHASE)
        else:
            tags.add(DamageTag.PHYSICAL)

        return DamageInstance(
            label=label,
            base_potency=base_potency,
            tags=tags,
            group_name="Support Action",
            buffs_before=buffs_before,
        )


class SupportActionV5(CombatAction):
    """Support action (V5)."""

    @override
    def execute(self, has_expansion_key: bool = True) -> DamageInstance:
        label: str = "Support Action"
        base_potency: int = 90
        tags: set[DamageTag] = {
            DamageTag.PASSIVE,
            DamageTag.SUPPORT_ACTION,
            DamageTag.MEDIUM_AMMO,
            DamageTag.TARGETED,
        }

        buffs_before: list[Buff] = []

        buffs_before.append(
            Buff(
                value=10,
                modifier_type=ModifierType.ADDITIVE,
                stat_type=SpecialAttribute.DAMAGE_BOOST,
                tag=DamageTag.SUPPORT_ACTION,
            )
        )

        buffs_before.append(DamageUpII())

        if has_expansion_key:
            tags.add(DamageTag.BURN)
            tags.add(DamageTag.PHASE)
        else:
            tags.add(DamageTag.PHYSICAL)

        return DamageInstance(
            label=label,
            base_potency=base_potency,
            tags=tags,
            group_name="Support Action",
            buffs_before=buffs_before,
        )


class Qiongjiu(Doll):
    """Qiongjiu."""

    name: str = "Qiongjiu"
    irrelevant_damage_tags: ClassVar[set[DamageTag]] = set(
        [
            DamageTag.CORROSION,
            DamageTag.FREEZE,
            DamageTag.HYDRO,
            DamageTag.ELECTRIC,
            DamageTag.MELEE,
            DamageTag.LIGHT_AMMO,
            DamageTag.HEAVY_AMMO,
            DamageTag.SHOTGUN_AMMO,
            DamageTag.INTERCEPTION,
            DamageTag.COUNTERATTACK,
            DamageTag.PHYSICAL_SUMMON,
        ]
    )

    fuse: CombatAction = Field(default_factory=Fuse)
    common_rail: CombatAction = Field(default_factory=CommonRail)
    guide_to_victory: CombatAction = Field(default_factory=GuideToVictory)
    support_action: CombatAction = Field(default_factory=SupportAction)

    def set_to_v0(self) -> None:
        """Sets Fortification Level to Segment00."""
        self.fuse: CombatAction = Fuse()
        self.common_rail: CombatAction = CommonRail()
        self.guide_to_victory: CombatAction = GuideToVictory()
        self.support_action: CombatAction = SupportAction()

        # Expansion Key - Ruined Gem
        # Damage dealt to targets with Burn debuffs is increased by 15%.
        # TODO: Need tag for "targets with Burn debuffs"
        self.initial_stats.special_attributes[
            SpecialAttribute.DAMAGE_BOOST
        ].set_multiplier(DamageTag.ALL, 15)

        # Passive
        # Increases damage dealt to targets not under the protection of cover by 10%
        self.initial_stats.special_attributes[
            SpecialAttribute.DAMAGE_BOOST
        ].set_multiplier(DamageTag.EXPOSED, 10)

    def set_to_v2(self) -> None:
        """Sets Fortification Level to Segment02."""
        self.set_to_v0()

        self.guide_to_victory: CombatAction = GuideToVictoryV2()

    def set_to_v3(self) -> None:
        """Sets Fortification Level to Segment03."""
        self.set_to_v2()

        self.support_action: CombatAction = SupportActionV3()

    def set_to_v5(self) -> None:
        """Sets Fortification Level to Segment05."""
        self.set_to_v3()

        self.support_action: CombatAction = SupportActionV5()

    def set_to_v6(self) -> None:
        """Sets Fortification Level to Segment06."""
        self.set_to_v5()

        self.initial_stats.special_attributes[
            SpecialAttribute.DAMAGE_BOOST
        ].set_multiplier(DamageTag.EXPOSED, 20)

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
                self.set_to_v5()
            case FortificationLevel.SEGMENT06:
                self.set_to_v6()
