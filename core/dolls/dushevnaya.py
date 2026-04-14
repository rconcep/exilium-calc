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


class Daybreak(CombatAction):
    """Dushevnaya basic attack."""

    @override
    def execute(self) -> DamageInstance:
        label: str = "Daybreak"
        base_potency: int = 80
        tags: set[DamageTag] = {
            DamageTag.ACTIVE,
            DamageTag.BASIC,
            DamageTag.HEAVY_AMMO,
            DamageTag.TARGETED,
            DamageTag.FREEZE,
            DamageTag.PHASE,
        }

        # Expansion Key - Wintersong of the Hero:
        # Targeted damage dealt by Dushevnaya is converted to Freeze damage

        return DamageInstance(
            label=label,
            base_potency=base_potency,
            tags=tags,
            group_name="Daybreak",
        )


class HerosCode(CombatAction):
    """Dushevnaya S1."""

    @override
    def execute(
        self,
        stacks_of_ices_grace: int,
        target_on_freeze_tile: bool,
        has_fixed_key_1: bool,
    ) -> DamageInstance:
        label: str = "Hero's Code"
        base_potency: int = 110
        tags: set[DamageTag] = {
            DamageTag.ACTIVE,
            DamageTag.HEAVY_AMMO,
            DamageTag.TARGETED,
            DamageTag.FREEZE,
            DamageTag.PHASE,
        }

        # Expansion Key - Wintersong of the Hero:
        # Targeted damage dealt by Dushevnaya is converted to Freeze damage

        buffs_before: list[Buff] = []
        ices_grace_stack_maximum: int = 4

        # Fixed Key 1 - Lance of Longinus:
        # Each Ice's Grace stack gained above the maximum amount increases the critical rate of Hero's Code by 5%, up to a maximum increase of 30%.
        if has_fixed_key_1 and (stacks_of_ices_grace > ices_grace_stack_maximum):
            excess_stacks: int = stacks_of_ices_grace - ices_grace_stack_maximum
            critical_rate_increase_per_excess_stack: int = 5
            max_critical_rate_increase_from_excess_stacks: int = 30
            total_critical_rate_increase_from_excess_stacks: int = min(
                excess_stacks * critical_rate_increase_per_excess_stack,
                max_critical_rate_increase_from_excess_stacks,
            )
            buffs_before.append(
                Buff(
                    total_critical_rate_increase_from_excess_stacks,
                    ModifierType.ADDITIVE,
                    StatType.CRIT_RATE,
                )
            )

        if stacks_of_ices_grace >= ices_grace_stack_maximum:
            # The damage is converted into Freeze damage and if the target is on a Freeze tile, damage dealt is increased to 130%.
            if target_on_freeze_tile:
                base_potency = 130

        return DamageInstance(
            label=label,
            base_potency=base_potency,
            tags=tags,
            group_name="Hero's Code",
            buffs_before=buffs_before,
        )


class HerosCodeV4(CombatAction):
    """Dushevnaya S1 (V4)."""

    @override
    def execute(
        self,
        stacks_of_ices_grace: int,
        target_on_freeze_tile: bool,
        has_fixed_key_1: bool,
    ) -> DamageInstance:
        label: str = "Hero's Code"
        base_potency: int = 110
        tags: set[DamageTag] = {
            DamageTag.ACTIVE,
            DamageTag.HEAVY_AMMO,
            DamageTag.TARGETED,
            DamageTag.FREEZE,
            DamageTag.PHASE,
        }

        # Expansion Key - Wintersong of the Hero:
        # Targeted damage dealt by Dushevnaya is converted to Freeze damage

        buffs_before: list[Buff] = []
        ices_grace_stack_maximum: int = 4

        # Fixed Key 1 - Lance of Longinus:
        # Each Ice's Grace stack gained above the maximum amount increases the critical rate of Hero's Code by 5%, up to a maximum increase of 30%.
        if has_fixed_key_1 and (stacks_of_ices_grace > ices_grace_stack_maximum):
            excess_stacks: int = stacks_of_ices_grace - ices_grace_stack_maximum
            critical_rate_increase_per_excess_stack: int = 5
            max_critical_rate_increase_from_excess_stacks: int = 30
            total_critical_rate_increase_from_excess_stacks: int = min(
                excess_stacks * critical_rate_increase_per_excess_stack,
                max_critical_rate_increase_from_excess_stacks,
            )
            buffs_before.append(
                Buff(
                    total_critical_rate_increase_from_excess_stacks,
                    ModifierType.ADDITIVE,
                    StatType.CRIT_RATE,
                )
            )

        if stacks_of_ices_grace >= ices_grace_stack_maximum:
            # The damage is converted into Freeze damage and if the target is on a Freeze tile, damage dealt is increased to 130%.
            base_potency = 140
            if target_on_freeze_tile:
                base_potency = 160

        return DamageInstance(
            label=label,
            base_potency=base_potency,
            tags=tags,
            group_name="Hero's Code",
            buffs_before=buffs_before,
        )


class MarzannasSanction(CombatAction):
    """Dushevnaya S2."""

    @override
    def execute(self, is_enhanced: bool) -> DamageInstance:
        label: str = "Marzanna's Sanction"
        base_potency: int = 50
        tags: set[DamageTag] = {
            DamageTag.ACTIVE,
            DamageTag.FREEZE,
            DamageTag.PHASE,
            DamageTag.AREA_OF_EFFECT,
            DamageTag.CONFECTANCE,
        }

        if is_enhanced:
            base_potency = 70

        return DamageInstance(
            label=label,
            base_potency=base_potency,
            tags=tags,
            group_name="Marzanna's Sanction",
        )


class MarzannasSanctionV3(CombatAction):
    """Dushevnaya S2 (V3)."""

    @override
    def execute(self, is_enhanced: bool) -> DamageInstance:
        label: str = "Marzanna's Sanction"
        base_potency: int = 70
        tags: set[DamageTag] = {
            DamageTag.ACTIVE,
            DamageTag.FREEZE,
            DamageTag.PHASE,
            DamageTag.AREA_OF_EFFECT,
            DamageTag.CONFECTANCE,
        }

        if is_enhanced:
            base_potency = 90

        return DamageInstance(
            label=label,
            base_potency=base_potency,
            tags=tags,
            group_name="Marzanna's Sanction",
        )


class SupportAction(CombatAction):
    """Support Action from Glacial Domain status."""

    @override
    def execute(self) -> DamageInstance:
        label: str = "Support Action"
        base_potency: int = 80
        tags: set[DamageTag] = {
            DamageTag.PASSIVE,
            DamageTag.SUPPORT_ACTION,
            DamageTag.HEAVY_AMMO,
            DamageTag.TARGETED,
            DamageTag.FREEZE,
            DamageTag.PHASE,
        }

        return DamageInstance(
            label=label,
            base_potency=base_potency,
            tags=tags,
            group_name="Support Action",
        )


class Dushevnaya(Doll):
    """Dushevnaya."""

    name: str = "Dushevnaya"
    irrelevant_damage_tags: ClassVar[set[DamageTag]] = set(
        [
            DamageTag.CORROSION,
            DamageTag.HYDRO,
            DamageTag.BURN,
            DamageTag.ELECTRIC,
            DamageTag.MELEE,
            DamageTag.LIGHT_AMMO,
            DamageTag.MEDIUM_AMMO,
            DamageTag.SHOTGUN_AMMO,
            DamageTag.INTERCEPTION,
            DamageTag.COUNTERATTACK,
            DamageTag.AREA_OF_EFFECT,
            DamageTag.ULTIMATE,
            DamageTag.PHYSICAL_SUMMON,
            DamageTag.FIXED,
        ]
    )

    daybreak: CombatAction = Field(default_factory=Daybreak)
    heros_code: CombatAction = Field(default_factory=HerosCode)
    marzannas_sanction: CombatAction = Field(default_factory=MarzannasSanction)
    support_action: CombatAction = Field(default_factory=SupportAction)

    def set_to_v0(self) -> None:
        """Sets Fortification Level to Segment00."""
        self.daybreak = Daybreak()
        self.heros_code = HerosCode()
        self.marzannas_sanction = MarzannasSanction()
        self.support_action = SupportAction()

        # Passive - Blessed Artwork:
        # Increase all allied units' damage by 10%
        self.initial_stats.special_attributes[
            SpecialAttribute.DAMAGE_BOOST
        ].set_multiplier(DamageTag.ALL, 10)

        # With an additional 10% boost specifically for Freeze damage.
        self.initial_stats.special_attributes[
            SpecialAttribute.DAMAGE_BOOST
        ].set_multiplier(DamageTag.FREEZE, 10)

        # Fixed Key 2 - Adventurer's Will:
        # When an active attack only hits 1 target, increases Freeze damage dealt by 20%.
        # Since Expansion Key - Wintersong of the Hero converts all of Dushevnaya's targeted damage into Freeze damage,
        # this effectively means that when any of her active attacks only hit 1 target, the damage dealt by that attack is increased by 20%.
        self.initial_stats.special_attributes[
            SpecialAttribute.DAMAGE_BOOST
        ].set_multiplier(DamageTag.TARGETED, 20)

        # Expansion Key - Wintersong of the Hero:
        # Freeze damage dealt by allied units is increased by 5%, up to a maximum of 15%.
        self.initial_stats.special_attributes[
            SpecialAttribute.DAMAGE_BOOST
        ].set_multiplier(DamageTag.FREEZE, 10 + 5)

        # Targeted damage dealt by Dushevnaya is converted to Freeze damage and ignores 30% of the target's defense.
        self.initial_stats.special_attributes[
            SpecialAttribute.DEFENSE_IGNORE
        ].set_multiplier(DamageTag.TARGETED, 30)

    def set_to_v3(self) -> None:
        """Sets Fortification Level to Segment03."""
        self.set_to_v0()

        self.marzannas_sanction = MarzannasSanctionV3()

    def set_to_v4(self) -> None:
        """Sets Fortification Level to Segment05."""
        self.set_to_v3()

        self.heros_code = HerosCodeV4()

    def set_to_v6(self) -> None:
        """Sets Fortification Level to Segment06."""
        self.set_to_v4()

        # Passive - Blessed Artwork:
        # Instead increases all allied units' damage by 20% with an additional 40% boost specifically for Freeze damage.
        self.initial_stats.special_attributes[
            SpecialAttribute.DAMAGE_BOOST
        ].set_multiplier(DamageTag.ALL, 20)
        self.initial_stats.special_attributes[
            SpecialAttribute.DAMAGE_BOOST
        ].set_multiplier(DamageTag.FREEZE, 40 + 5)

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
                self.set_to_v3()
            case FortificationLevel.SEGMENT04:
                self.set_to_v4()
            case FortificationLevel.SEGMENT05:
                self.set_to_v4()
            case FortificationLevel.SEGMENT06:
                self.set_to_v6()
