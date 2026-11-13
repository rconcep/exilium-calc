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
)
from core.buffs import Buff, Debuff, MAX_TILE_ASCENSION_LEVEL
from core.combat import (
    DamageInstance,
    CombatAction,
)

HUNT_TRACKING_STACK_MAXIMUM: int = 3
HUNT_TRACKING_STACK_MAXIMUM_V4: int = 6


class BurstFang(CombatAction):
    """Faelynn Basic Attack."""

    @override
    def execute(self) -> DamageInstance:
        label: str = "Burst Fang"
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
            group_name="Burst Fang",
        )


class TripleMaul(CombatAction):
    """Faelynn S1."""

    @override
    def execute(self, stacks_of_hunt_tracking: int) -> DamageInstance:
        label: str = f"Triple Maul ({stacks_of_hunt_tracking})"
        base_potency: int = 60

        tags: set[DamageTag] = {
            DamageTag.ACTIVE,
            DamageTag.CORROSION,
            DamageTag.PHASE,
            DamageTag.MEDIUM_AMMO,
            DamageTag.AREA_OF_EFFECT,
        }

        damage_multiplier_per_stack: int = 5
        base_potency += damage_multiplier_per_stack * max(
            0, min(HUNT_TRACKING_STACK_MAXIMUM, stacks_of_hunt_tracking)
        )

        return DamageInstance(
            label=label,
            base_potency=base_potency,
            tags=tags,
            group_name="Triple Maul",
        )


class TripleMaulV2(CombatAction):
    """Faelynn S1 (V2)."""

    @override
    def execute(self, stacks_of_hunt_tracking: int) -> DamageInstance:
        label: str = f"Triple Maul ({stacks_of_hunt_tracking})"
        base_potency: int = 60

        tags: set[DamageTag] = {
            DamageTag.ACTIVE,
            DamageTag.CORROSION,
            DamageTag.PHASE,
            DamageTag.MEDIUM_AMMO,
            DamageTag.AREA_OF_EFFECT,
        }

        damage_multiplier_per_stack: int = 10
        base_potency += damage_multiplier_per_stack * max(
            0, min(HUNT_TRACKING_STACK_MAXIMUM, stacks_of_hunt_tracking)
        )

        return DamageInstance(
            label=label,
            base_potency=base_potency,
            tags=tags,
            group_name="Triple Maul",
        )


class TripleMaulV4(CombatAction):
    """Faelynn S1 (V4)."""

    @override
    def execute(self, stacks_of_hunt_tracking: int) -> DamageInstance:
        label: str = f"Triple Maul ({stacks_of_hunt_tracking})"
        base_potency: int = 60

        tags: set[DamageTag] = {
            DamageTag.ACTIVE,
            DamageTag.CORROSION,
            DamageTag.PHASE,
            DamageTag.MEDIUM_AMMO,
            DamageTag.AREA_OF_EFFECT,
        }

        damage_multiplier_per_stack: int = 10
        base_potency += damage_multiplier_per_stack * max(
            0, min(HUNT_TRACKING_STACK_MAXIMUM_V4, stacks_of_hunt_tracking)
        )

        return DamageInstance(
            label=label,
            base_potency=base_potency,
            tags=tags,
            group_name="Triple Maul",
        )


class TripleMaulV5(CombatAction):
    """Faelynn S1 (V5)."""

    @override
    def execute(self, stacks_of_hunt_tracking: int) -> DamageInstance:
        label: str = f"Triple Maul ({stacks_of_hunt_tracking})"
        base_potency: int = 120

        tags: set[DamageTag] = {
            DamageTag.ACTIVE,
            DamageTag.CORROSION,
            DamageTag.PHASE,
            DamageTag.MEDIUM_AMMO,
            DamageTag.AREA_OF_EFFECT,
        }

        damage_multiplier_per_stack: int = 10
        base_potency += damage_multiplier_per_stack * max(
            0, min(HUNT_TRACKING_STACK_MAXIMUM_V4, stacks_of_hunt_tracking)
        )

        return DamageInstance(
            label=label,
            base_potency=base_potency,
            tags=tags,
            group_name="Triple Maul",
        )


class TripleMaulFollowup(CombatAction):
    """Followup to Faelynn's S1 at V5+ if more than 3 targets or a Boss is hit.
    The intent is to only use this if the conditions for the followup are met,
    but input args can allow the creation of placeholders that deal 0 damage.
    """

    @override
    def execute(self, number_of_targets_hit: int, boss_was_hit: bool) -> DamageInstance:
        label: str = "Triple Maul (follow-up)"
        base_potency: int = 0

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
            group_name="Triple Maul",
        )


class TripleMaulFollowupV5(CombatAction):
    """Followup to Faelynn's S1 at V5+ if more than 3 targets or a Boss is hit.
    The intent is to only use this if the conditions for the followup are met,
    but input args can allow the creation of placeholders that deal 0 damage.
    """

    @override
    def execute(self, number_of_targets_hit: int, boss_was_hit: bool) -> DamageInstance:
        label: str = "Triple Maul (follow-up)"
        base_potency: int = 0

        tags: set[DamageTag] = {
            DamageTag.ACTIVE,
            DamageTag.CORROSION,
            DamageTag.PHASE,
            DamageTag.AREA_OF_EFFECT,
        }

        if number_of_targets_hit > 3 or boss_was_hit:
            base_potency = 120

        return DamageInstance(
            label=label,
            base_potency=base_potency,
            tags=tags,
            group_name="Triple Maul",
        )


class ScentTrailAction(CombatAction):
    """Damage triggered whenever Scent Trail is applied to a target that already has Scent Trail."""

    @override
    def execute(self) -> DamageInstance:
        label: str = "Scent Trail"
        base_potency: int = 60

        tags: set[DamageTag] = {
            DamageTag.PASSIVE,
            DamageTag.CORROSION,
            DamageTag.PHASE,
            DamageTag.AREA_OF_EFFECT,
        }

        return DamageInstance(
            label=label,
            base_potency=base_potency,
            tags=tags,
            group_name="Scent Trail",
        )


class ScentTrailActionV2(CombatAction):
    """Damage triggered whenever Scent Trail is applied to a target that already has Scent Trail."""

    @override
    def execute(self) -> DamageInstance:
        label: str = "Scent Trail"
        base_potency: int = 100

        tags: set[DamageTag] = {
            DamageTag.PASSIVE,
            DamageTag.CORROSION,
            DamageTag.PHASE,
            DamageTag.AREA_OF_EFFECT,
        }

        return DamageInstance(
            label=label,
            base_potency=base_potency,
            tags=tags,
            group_name="Scent Trail",
        )


class LoyalDash(CombatAction):
    """Faelynn Ultimate."""

    @override
    def execute(self, stacks_of_hunt_tracking: int) -> DamageInstance:
        label: str = f"Loyal Dash ({stacks_of_hunt_tracking})"
        base_potency: int = 120

        tags: set[DamageTag] = {
            DamageTag.ACTIVE,
            DamageTag.CORROSION,
            DamageTag.PHASE,
            DamageTag.AREA_OF_EFFECT,
            DamageTag.ULTIMATE,
            DamageTag.CONFECTANCE,
        }

        damage_multiplier_per_stack: int = 5
        base_potency += (
            max(0, min(HUNT_TRACKING_STACK_MAXIMUM, stacks_of_hunt_tracking))
            * damage_multiplier_per_stack
        )

        return DamageInstance(
            label=label,
            base_potency=base_potency,
            tags=tags,
            group_name="Loyal Dash",
        )


class LoyalDashV3(CombatAction):
    """Faelynn Ultimate (V3)."""

    @override
    def execute(self, stacks_of_hunt_tracking: int) -> DamageInstance:
        label: str = f"Loyal Dash ({stacks_of_hunt_tracking})"
        base_potency: int = 120

        tags: set[DamageTag] = {
            DamageTag.ACTIVE,
            DamageTag.CORROSION,
            DamageTag.PHASE,
            DamageTag.AREA_OF_EFFECT,
            DamageTag.ULTIMATE,
            DamageTag.CONFECTANCE,
        }

        damage_multiplier_per_stack: int = 10
        base_potency += (
            max(0, min(HUNT_TRACKING_STACK_MAXIMUM, stacks_of_hunt_tracking))
            * damage_multiplier_per_stack
        )

        return DamageInstance(
            label=label,
            base_potency=base_potency,
            tags=tags,
            group_name="Loyal Dash",
        )


class LoyalDashV4(CombatAction):
    """Faelynn Ultimate (V4)."""

    @override
    def execute(self, stacks_of_hunt_tracking: int) -> DamageInstance:
        label: str = f"Loyal Dash ({stacks_of_hunt_tracking})"
        base_potency: int = 120

        tags: set[DamageTag] = {
            DamageTag.ACTIVE,
            DamageTag.CORROSION,
            DamageTag.PHASE,
            DamageTag.AREA_OF_EFFECT,
            DamageTag.ULTIMATE,
            DamageTag.CONFECTANCE,
        }

        damage_multiplier_per_stack: int = 10
        base_potency += (
            max(0, min(HUNT_TRACKING_STACK_MAXIMUM_V4, stacks_of_hunt_tracking))
            * damage_multiplier_per_stack
        )

        return DamageInstance(
            label=label,
            base_potency=base_potency,
            tags=tags,
            group_name="Loyal Dash",
        )


class LoyalDashV6(CombatAction):
    """Faelynn Ultimate (V6)."""

    @override
    def execute(self, stacks_of_hunt_tracking: int) -> DamageInstance:
        label: str = f"Loyal Dash ({stacks_of_hunt_tracking})"
        base_potency: int = 150

        tags: set[DamageTag] = {
            DamageTag.ACTIVE,
            DamageTag.CORROSION,
            DamageTag.PHASE,
            DamageTag.AREA_OF_EFFECT,
            DamageTag.ULTIMATE,
            DamageTag.CONFECTANCE,
        }

        damage_multiplier_per_stack: int = 10
        base_potency += (
            max(0, min(HUNT_TRACKING_STACK_MAXIMUM_V4, stacks_of_hunt_tracking))
            * damage_multiplier_per_stack
        )

        return DamageInstance(
            label=label,
            base_potency=base_potency,
            tags=tags,
            group_name="Loyal Dash",
        )


class PursuitInstinctI(CombatAction):
    """Faelynn's Pursuit Instinct I."""

    @override
    def execute(
        self, stacks_of_hunt_tracking: int, number_of_targets_hit: int
    ) -> DamageInstance:
        label: str = f"Pursuit Instinct I ({stacks_of_hunt_tracking})"
        base_potency: int = 60

        tags: set[DamageTag] = {
            DamageTag.ACTIVE,
            DamageTag.CORROSION,
            DamageTag.PHASE,
            DamageTag.AREA_OF_EFFECT,
        }

        damage_multiplier_per_stack: int = 5
        base_potency += (
            max(0, min(HUNT_TRACKING_STACK_MAXIMUM, stacks_of_hunt_tracking))
            * damage_multiplier_per_stack
        )

        if number_of_targets_hit == 1:
            base_potency += 30

        return DamageInstance(
            label=label,
            base_potency=base_potency,
            tags=tags,
            group_name="Pursuit Instinct I",
        )


class PursuitInstinctIV3(CombatAction):
    """Faelynn's Pursuit Instinct I (V3)."""

    @override
    def execute(
        self, stacks_of_hunt_tracking: int, number_of_targets_hit: int
    ) -> DamageInstance:
        label: str = f"Pursuit Instinct I ({stacks_of_hunt_tracking})"
        base_potency: int = 60

        tags: set[DamageTag] = {
            DamageTag.ACTIVE,
            DamageTag.CORROSION,
            DamageTag.PHASE,
            DamageTag.AREA_OF_EFFECT,
        }

        damage_multiplier_per_stack: int = 10
        base_potency += (
            max(0, min(HUNT_TRACKING_STACK_MAXIMUM, stacks_of_hunt_tracking))
            * damage_multiplier_per_stack
        )

        if number_of_targets_hit == 1:
            base_potency += 30

        return DamageInstance(
            label=label,
            base_potency=base_potency,
            tags=tags,
            group_name="Pursuit Instinct I",
        )


class PursuitInstinctIV4(CombatAction):
    """Faelynn's Pursuit Instinct I (V4)."""

    @override
    def execute(
        self, stacks_of_hunt_tracking: int, number_of_targets_hit: int
    ) -> DamageInstance:
        label: str = f"Pursuit Instinct I ({stacks_of_hunt_tracking})"
        base_potency: int = 60

        tags: set[DamageTag] = {
            DamageTag.ACTIVE,
            DamageTag.CORROSION,
            DamageTag.PHASE,
            DamageTag.AREA_OF_EFFECT,
        }

        damage_multiplier_per_stack: int = 10
        base_potency += (
            max(0, min(HUNT_TRACKING_STACK_MAXIMUM_V4, stacks_of_hunt_tracking))
            * damage_multiplier_per_stack
        )

        if number_of_targets_hit == 1:
            base_potency += 30

        return DamageInstance(
            label=label,
            base_potency=base_potency,
            tags=tags,
            group_name="Pursuit Instinct I",
        )


class PursuitInstinctIV6(CombatAction):
    """Faelynn's Pursuit Instinct I (V6)."""

    @override
    def execute(
        self, stacks_of_hunt_tracking: int, number_of_targets_hit: int
    ) -> DamageInstance:
        label: str = f"Pursuit Instinct I ({stacks_of_hunt_tracking})"
        base_potency: int = 90

        tags: set[DamageTag] = {
            DamageTag.ACTIVE,
            DamageTag.CORROSION,
            DamageTag.PHASE,
            DamageTag.AREA_OF_EFFECT,
        }

        damage_multiplier_per_stack: int = 10
        base_potency += (
            max(0, min(HUNT_TRACKING_STACK_MAXIMUM_V4, stacks_of_hunt_tracking))
            * damage_multiplier_per_stack
        )

        if number_of_targets_hit == 1:
            base_potency += 30

        return DamageInstance(
            label=label,
            base_potency=base_potency,
            tags=tags,
            group_name="Pursuit Instinct I",
        )


class PursuitInstinctII(CombatAction):
    """Faelynn's Pursuit Instinct II."""

    @override
    def execute(
        self,
        stacks_of_hunt_tracking: int,
        number_of_targets_hit: int,
        has_collar_brand: bool,
    ) -> DamageInstance:
        label: str = f"Pursuit Instinct II ({stacks_of_hunt_tracking})"
        base_potency: int = 120

        tags: set[DamageTag] = {
            DamageTag.ACTIVE,
            DamageTag.CORROSION,
            DamageTag.PHASE,
            DamageTag.AREA_OF_EFFECT,
        }

        damage_multiplier_per_stack: int = 5
        base_potency += (
            max(0, min(HUNT_TRACKING_STACK_MAXIMUM, stacks_of_hunt_tracking))
            * damage_multiplier_per_stack
        )

        if number_of_targets_hit == 1:
            base_potency += 30

        buffs_before: list[Buff] = []
        if has_collar_brand:
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
            group_name="Pursuit Instinct II",
            buffs_before=buffs_before,
        )


class PursuitInstinctIIV3(CombatAction):
    """Faelynn's Pursuit Instinct II (V3)."""

    @override
    def execute(
        self,
        stacks_of_hunt_tracking: int,
        number_of_targets_hit: int,
        has_collar_brand: bool,
    ) -> DamageInstance:
        label: str = f"Pursuit Instinct II ({stacks_of_hunt_tracking})"
        base_potency: int = 120

        tags: set[DamageTag] = {
            DamageTag.ACTIVE,
            DamageTag.CORROSION,
            DamageTag.PHASE,
            DamageTag.AREA_OF_EFFECT,
        }

        damage_multiplier_per_stack: int = 10
        base_potency += (
            max(0, min(HUNT_TRACKING_STACK_MAXIMUM, stacks_of_hunt_tracking))
            * damage_multiplier_per_stack
        )

        if number_of_targets_hit == 1:
            base_potency += 30

        buffs_before: list[Buff] = []
        if has_collar_brand:
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
            group_name="Pursuit Instinct II",
            buffs_before=buffs_before,
        )


class PursuitInstinctIIV4(CombatAction):
    """Faelynn's Pursuit Instinct II (V4)."""

    @override
    def execute(
        self,
        stacks_of_hunt_tracking: int,
        number_of_targets_hit: int,
        has_collar_brand: bool,
    ) -> DamageInstance:
        label: str = f"Pursuit Instinct II ({stacks_of_hunt_tracking})"
        base_potency: int = 120

        tags: set[DamageTag] = {
            DamageTag.ACTIVE,
            DamageTag.CORROSION,
            DamageTag.PHASE,
            DamageTag.AREA_OF_EFFECT,
        }

        damage_multiplier_per_stack: int = 10
        base_potency += (
            max(0, min(HUNT_TRACKING_STACK_MAXIMUM_V4, stacks_of_hunt_tracking))
            * damage_multiplier_per_stack
        )

        if number_of_targets_hit == 1:
            base_potency += 30

        buffs_before: list[Buff] = []
        if has_collar_brand:
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
            group_name="Pursuit Instinct II",
            buffs_before=buffs_before,
        )


class PursuitInstinctIIV6(CombatAction):
    """Faelynn's Pursuit Instinct II (V6)."""

    @override
    def execute(
        self,
        stacks_of_hunt_tracking: int,
        number_of_targets_hit: int,
        has_collar_brand: bool,
    ) -> DamageInstance:
        label: str = f"Pursuit Instinct II ({stacks_of_hunt_tracking})"
        base_potency: int = 170

        tags: set[DamageTag] = {
            DamageTag.ACTIVE,
            DamageTag.CORROSION,
            DamageTag.PHASE,
            DamageTag.AREA_OF_EFFECT,
        }

        damage_multiplier_per_stack: int = 10
        base_potency += (
            max(0, min(HUNT_TRACKING_STACK_MAXIMUM_V4, stacks_of_hunt_tracking))
            * damage_multiplier_per_stack
        )

        if number_of_targets_hit == 1:
            base_potency += 30

        buffs_before: list[Buff] = []
        if has_collar_brand:
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
            group_name="Pursuit Instinct II",
            buffs_before=buffs_before,
        )


class PursuitInstinctIII(CombatAction):
    """Faelynn's Pursuit Instinct III."""

    @override
    def execute(
        self,
        stacks_of_hunt_tracking: int,
        number_of_targets_hit: int,
        has_collar_brand: bool,
        target_tile_ascension_level: int,
    ) -> DamageInstance:
        label: str = f"Pursuit Instinct III ({stacks_of_hunt_tracking})"
        base_potency: int = 240

        tags: set[DamageTag] = {
            DamageTag.ACTIVE,
            DamageTag.CORROSION,
            DamageTag.PHASE,
            DamageTag.AREA_OF_EFFECT,
        }

        damage_multiplier_per_stack: int = 5
        base_potency += (
            max(0, min(HUNT_TRACKING_STACK_MAXIMUM, stacks_of_hunt_tracking))
            * damage_multiplier_per_stack
        )

        if number_of_targets_hit == 1:
            base_potency += 30

        buffs_before: list[Buff] = []
        debuffs_before: list[Debuff] = []
        if has_collar_brand:
            buffs_before.append(
                Buff(
                    100,
                    ModifierType.ADDITIVE,
                    SpecialAttribute.DAMAGE_BOOST,
                    DamageTag.ALL,
                )
            )

        if target_tile_ascension_level > 0:
            critical_damage_per_tile_ascension_level: int = 5
            defense_reduction_per_tile_ascension_level: int = -14

            buffs_before.append(
                Buff(
                    min(MAX_TILE_ASCENSION_LEVEL, max(0, target_tile_ascension_level))
                    * critical_damage_per_tile_ascension_level,
                    ModifierType.ADDITIVE,
                    SpecialAttribute.CRITICAL_DAMAGE,
                    DamageTag.ALL,
                )
            )
            debuffs_before.append(
                Debuff(
                    min(MAX_TILE_ASCENSION_LEVEL, max(0, target_tile_ascension_level))
                    * defense_reduction_per_tile_ascension_level,
                    ModifierType.MULTIPLICATIVE,
                    StatType.DEFENSE,
                    DamageTag.ALL,
                )
            )

        return DamageInstance(
            label=label,
            base_potency=base_potency,
            tags=tags,
            group_name="Pursuit Instinct III",
            buffs_before=buffs_before,
            debuffs_before=debuffs_before,
        )


class PursuitInstinctIIIV3(CombatAction):
    """Faelynn's Pursuit Instinct III (V3)."""

    @override
    def execute(
        self,
        stacks_of_hunt_tracking: int,
        number_of_targets_hit: int,
        has_collar_brand: bool,
        target_tile_ascension_level: int,
    ) -> DamageInstance:
        label: str = f"Pursuit Instinct III ({stacks_of_hunt_tracking})"
        base_potency: int = 240

        tags: set[DamageTag] = {
            DamageTag.ACTIVE,
            DamageTag.CORROSION,
            DamageTag.PHASE,
            DamageTag.AREA_OF_EFFECT,
        }

        damage_multiplier_per_stack: int = 10
        base_potency += (
            max(0, min(HUNT_TRACKING_STACK_MAXIMUM, stacks_of_hunt_tracking))
            * damage_multiplier_per_stack
        )

        if number_of_targets_hit == 1:
            base_potency += 30

        buffs_before: list[Buff] = []
        debuffs_before: list[Debuff] = []
        if has_collar_brand:
            buffs_before.append(
                Buff(
                    100,
                    ModifierType.ADDITIVE,
                    SpecialAttribute.DAMAGE_BOOST,
                    DamageTag.ALL,
                )
            )

        if target_tile_ascension_level > 0:
            critical_damage_per_tile_ascension_level: int = 5
            defense_reduction_per_tile_ascension_level: int = -14

            buffs_before.append(
                Buff(
                    min(MAX_TILE_ASCENSION_LEVEL, max(0, target_tile_ascension_level))
                    * critical_damage_per_tile_ascension_level,
                    ModifierType.ADDITIVE,
                    SpecialAttribute.CRITICAL_DAMAGE,
                    DamageTag.ALL,
                )
            )
            debuffs_before.append(
                Debuff(
                    min(MAX_TILE_ASCENSION_LEVEL, max(0, target_tile_ascension_level))
                    * defense_reduction_per_tile_ascension_level,
                    ModifierType.MULTIPLICATIVE,
                    StatType.DEFENSE,
                    DamageTag.ALL,
                )
            )

        return DamageInstance(
            label=label,
            base_potency=base_potency,
            tags=tags,
            group_name="Pursuit Instinct III",
            buffs_before=buffs_before,
            debuffs_before=debuffs_before,
        )


class PursuitInstinctIIIV4(CombatAction):
    """Faelynn's Pursuit Instinct III (V4)."""

    @override
    def execute(
        self,
        stacks_of_hunt_tracking: int,
        number_of_targets_hit: int,
        has_collar_brand: bool,
        target_tile_ascension_level: int,
    ) -> DamageInstance:
        label: str = f"Pursuit Instinct III ({stacks_of_hunt_tracking})"
        base_potency: int = 240

        tags: set[DamageTag] = {
            DamageTag.ACTIVE,
            DamageTag.CORROSION,
            DamageTag.PHASE,
            DamageTag.AREA_OF_EFFECT,
        }

        damage_multiplier_per_stack: int = 10
        base_potency += (
            max(0, min(HUNT_TRACKING_STACK_MAXIMUM_V4, stacks_of_hunt_tracking))
            * damage_multiplier_per_stack
        )

        if number_of_targets_hit == 1:
            base_potency += 30

        buffs_before: list[Buff] = []
        debuffs_before: list[Debuff] = []
        if has_collar_brand:
            buffs_before.append(
                Buff(
                    100,
                    ModifierType.ADDITIVE,
                    SpecialAttribute.DAMAGE_BOOST,
                    DamageTag.ALL,
                )
            )

        if target_tile_ascension_level > 0:
            critical_damage_per_tile_ascension_level: int = 5
            defense_reduction_per_tile_ascension_level: int = -14

            buffs_before.append(
                Buff(
                    min(MAX_TILE_ASCENSION_LEVEL, max(0, target_tile_ascension_level))
                    * critical_damage_per_tile_ascension_level,
                    ModifierType.ADDITIVE,
                    SpecialAttribute.CRITICAL_DAMAGE,
                    DamageTag.ALL,
                )
            )
            debuffs_before.append(
                Debuff(
                    min(MAX_TILE_ASCENSION_LEVEL, max(0, target_tile_ascension_level))
                    * defense_reduction_per_tile_ascension_level,
                    ModifierType.MULTIPLICATIVE,
                    StatType.DEFENSE,
                    DamageTag.ALL,
                )
            )

        return DamageInstance(
            label=label,
            base_potency=base_potency,
            tags=tags,
            group_name="Pursuit Instinct III",
            buffs_before=buffs_before,
            debuffs_before=debuffs_before,
        )


class PursuitInstinctIIIV6(CombatAction):
    """Faelynn's Pursuit Instinct III (V6)."""

    @override
    def execute(
        self,
        stacks_of_hunt_tracking: int,
        number_of_targets_hit: int,
        has_collar_brand: bool,
        target_tile_ascension_level: int,
    ) -> DamageInstance:
        label: str = f"Pursuit Instinct III ({stacks_of_hunt_tracking})"
        base_potency: int = 480

        tags: set[DamageTag] = {
            DamageTag.ACTIVE,
            DamageTag.CORROSION,
            DamageTag.PHASE,
            DamageTag.AREA_OF_EFFECT,
        }

        damage_multiplier_per_stack: int = 10
        base_potency += (
            max(0, min(HUNT_TRACKING_STACK_MAXIMUM_V4, stacks_of_hunt_tracking))
            * damage_multiplier_per_stack
        )

        if number_of_targets_hit == 1:
            base_potency += 30

        buffs_before: list[Buff] = []
        debuffs_before: list[Debuff] = []
        if has_collar_brand:
            buffs_before.append(
                Buff(
                    100,
                    ModifierType.ADDITIVE,
                    SpecialAttribute.DAMAGE_BOOST,
                    DamageTag.ALL,
                )
            )

        if target_tile_ascension_level > 0:
            critical_damage_per_tile_ascension_level: int = 5
            defense_reduction_per_tile_ascension_level: int = -14

            buffs_before.append(
                Buff(
                    min(MAX_TILE_ASCENSION_LEVEL, max(0, target_tile_ascension_level))
                    * critical_damage_per_tile_ascension_level,
                    ModifierType.ADDITIVE,
                    SpecialAttribute.CRITICAL_DAMAGE,
                    DamageTag.ALL,
                )
            )
            debuffs_before.append(
                Debuff(
                    min(MAX_TILE_ASCENSION_LEVEL, max(0, target_tile_ascension_level))
                    * defense_reduction_per_tile_ascension_level,
                    ModifierType.MULTIPLICATIVE,
                    StatType.DEFENSE,
                    DamageTag.ALL,
                )
            )

        return DamageInstance(
            label=label,
            base_potency=base_potency,
            tags=tags,
            group_name="Pursuit Instinct III",
            buffs_before=buffs_before,
            debuffs_before=debuffs_before,
        )


class Faelynn(Doll):
    """Faelynn."""

    name: str = "Faelynn"
    irrelevant_damage_tags: ClassVar[set[DamageTag]] = set(
        [
            DamageTag.BURN,
            DamageTag.FREEZE,
            DamageTag.HYDRO,
            DamageTag.ELECTRIC,
            DamageTag.LIGHT_AMMO,
            DamageTag.MELEE,
            DamageTag.HEAVY_AMMO,
            DamageTag.SHOTGUN_AMMO,
            DamageTag.SUPPORT_ACTION,
            DamageTag.COUNTERATTACK,
            DamageTag.INTERCEPTION,
            DamageTag.FIXED,
            DamageTag.PHYSICAL_SUMMON,
        ]
    )

    burst_fang: CombatAction = Field(default_factory=BurstFang)
    triple_maul: CombatAction = Field(default_factory=TripleMaul)
    triple_maul_followup: CombatAction = Field(default_factory=TripleMaulFollowup)
    scent_trail: CombatAction = Field(default_factory=ScentTrailAction)
    loyal_dash: CombatAction = Field(default_factory=LoyalDash)
    pursuit_instinct_i: CombatAction = Field(default_factory=PursuitInstinctI)
    pursuit_instinct_ii: CombatAction = Field(default_factory=PursuitInstinctII)
    pursuit_instinct_iii: CombatAction = Field(default_factory=PursuitInstinctIII)

    def set_to_v0(self) -> None:
        """Sets Fortification Level to Segment00."""
        self.burst_fang = BurstFang()
        self.triple_maul = TripleMaul()
        self.triple_maul_followup = TripleMaulFollowup()
        self.scent_trail = ScentTrailAction()
        self.loyal_dash = LoyalDash()
        self.pursuit_instinct_i = PursuitInstinctI()
        self.pursuit_instinct_ii = PursuitInstinctII()
        self.pursuit_instinct_iii = PursuitInstinctIII()

    def set_to_v2(self) -> None:
        """Sets Fortification Level to Segment02."""
        self.set_to_v0()

        self.triple_maul = TripleMaulV2()
        self.scent_trail = ScentTrailActionV2()

    def set_to_v3(self) -> None:
        """Sets Fortification Level to Segment03."""
        self.set_to_v2()

        self.loyal_dash = LoyalDashV3()
        self.pursuit_instinct_i = PursuitInstinctIV3()
        self.pursuit_instinct_ii = PursuitInstinctIIV3()
        self.pursuit_instinct_iii = PursuitInstinctIIIV3()

    def set_to_v4(self) -> None:
        """Sets Fortification Level to Segment04."""
        self.set_to_v3()

        self.triple_maul = TripleMaulV4()
        self.loyal_dash = LoyalDashV4()
        self.pursuit_instinct_i = PursuitInstinctIV4()
        self.pursuit_instinct_ii = PursuitInstinctIIV4()
        self.pursuit_instinct_iii = PursuitInstinctIIIV4()

    def set_to_v5(self) -> None:
        """Sets Fortification Level to Segment05."""
        self.set_to_v4()

        self.triple_maul = TripleMaulV5()
        self.triple_maul_followup = TripleMaulFollowupV5()

    def set_to_v6(self) -> None:
        """Sets Fortification Level to Segment06."""
        self.set_to_v5()

        self.loyal_dash = LoyalDashV6()
        self.pursuit_instinct_i = PursuitInstinctIV6()
        self.pursuit_instinct_ii = PursuitInstinctIIV6()
        self.pursuit_instinct_iii = PursuitInstinctIIIV6()

    @override
    def set_fortification_level(self, level: FortificationLevel) -> None:
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
                self.set_to_v4()
            case FortificationLevel.SEGMENT05:
                self.set_to_v5()
            case FortificationLevel.SEGMENT06:
                self.set_to_v6()
