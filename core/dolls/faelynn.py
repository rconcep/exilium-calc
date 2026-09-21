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

HUNTERS_TRACKING_STACK_MAXIMUM: int = 3
HUNTERS_TRACKING_STACK_MAXIMUM_V4: int = 6


class CuspidCombo(CombatAction):
    """Faelynn Basic Attack."""

    @override
    def execute(self) -> DamageInstance:
        label: str = "Cuspid Combo"
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
            group_name="Cuspid Combo",
        )


class TripleMaule(CombatAction):
    """Faelynn S1."""

    @override
    def execute(self, stacks_of_hunters_tracking: int) -> DamageInstance:
        label: str = f"Triple Maule ({stacks_of_hunters_tracking})"
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
            0, min(HUNTERS_TRACKING_STACK_MAXIMUM, stacks_of_hunters_tracking)
        )

        return DamageInstance(
            label=label,
            base_potency=base_potency,
            tags=tags,
            group_name="Triple Maule",
        )


class TripleMauleV2(CombatAction):
    """Faelynn S1 (V2)."""

    @override
    def execute(self, stacks_of_hunters_tracking: int) -> DamageInstance:
        label: str = f"Triple Maule ({stacks_of_hunters_tracking})"
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
            0, min(HUNTERS_TRACKING_STACK_MAXIMUM, stacks_of_hunters_tracking)
        )

        return DamageInstance(
            label=label,
            base_potency=base_potency,
            tags=tags,
            group_name="Triple Maule",
        )


class TripleMauleV4(CombatAction):
    """Faelynn S1 (V4)."""

    @override
    def execute(self, stacks_of_hunters_tracking: int) -> DamageInstance:
        label: str = f"Triple Maule ({stacks_of_hunters_tracking})"
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
            0, min(HUNTERS_TRACKING_STACK_MAXIMUM_V4, stacks_of_hunters_tracking)
        )

        return DamageInstance(
            label=label,
            base_potency=base_potency,
            tags=tags,
            group_name="Triple Maule",
        )


class TripleMauleV5(CombatAction):
    """Faelynn S1 (V5)."""

    @override
    def execute(self, stacks_of_hunters_tracking: int) -> DamageInstance:
        label: str = f"Triple Maule ({stacks_of_hunters_tracking})"
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
            0, min(HUNTERS_TRACKING_STACK_MAXIMUM_V4, stacks_of_hunters_tracking)
        )

        return DamageInstance(
            label=label,
            base_potency=base_potency,
            tags=tags,
            group_name="Triple Maule",
        )


class TripleMauleFollowup(CombatAction):
    """Followup to Faelynn's S1 at V5+ if more t han 3 targets or a Boss is hit.
    The intent is to only use this if the conditions for the followup are met,
    but input args can allow the creation of placeholders that deal 0 damage.
    """

    @override
    def execute(self, number_of_targets_hit: int, boss_was_hit: bool) -> DamageInstance:
        label: str = "Triple Maule (follow-up)"
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
            group_name="Triple Maule",
        )


class TripleMauleFollowupV5(CombatAction):
    """Followup to Faelynn's S1 at V5+ if more t han 3 targets or a Boss is hit.
    The intent is to only use this if the conditions for the followup are met,
    but input args can allow the creation of placeholders that deal 0 damage.
    """

    @override
    def execute(self, number_of_targets_hit: int, boss_was_hit: bool) -> DamageInstance:
        label: str = "Triple Maule (follow-up)"
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
            group_name="Triple Maule",
        )


class ScentMarkAction(CombatAction):
    """Damage triggered whenever Scent Mark is applied to a target that already has Scent Mark."""

    @override
    def execute(self) -> DamageInstance:
        label: str = "Scent Mark"
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
            group_name="Scent Mark",
        )


class ScentMarkActionV2(CombatAction):
    """Damage triggered whenever Scent Mark is applied to a target that already has Scent Mark."""

    @override
    def execute(self) -> DamageInstance:
        label: str = "Scent Mark"
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
            group_name="Scent Mark",
        )


class LoyalHunt(CombatAction):
    """Faelynn Ultimate."""

    @override
    def execute(self, stacks_of_hunters_tracking: int) -> DamageInstance:
        label: str = f"Loyal Hunt ({stacks_of_hunters_tracking})"
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
            max(0, min(HUNTERS_TRACKING_STACK_MAXIMUM, stacks_of_hunters_tracking))
            * damage_multiplier_per_stack
        )

        return DamageInstance(
            label=label,
            base_potency=base_potency,
            tags=tags,
            group_name="Loyal Hunt",
        )


class LoyalHuntV3(CombatAction):
    """Faelynn Ultimate (V3)."""

    @override
    def execute(self, stacks_of_hunters_tracking: int) -> DamageInstance:
        label: str = f"Loyal Hunt ({stacks_of_hunters_tracking})"
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
            max(0, min(HUNTERS_TRACKING_STACK_MAXIMUM, stacks_of_hunters_tracking))
            * damage_multiplier_per_stack
        )

        return DamageInstance(
            label=label,
            base_potency=base_potency,
            tags=tags,
            group_name="Loyal Hunt",
        )


class LoyalHuntV4(CombatAction):
    """Faelynn Ultimate (V4)."""

    @override
    def execute(self, stacks_of_hunters_tracking: int) -> DamageInstance:
        label: str = f"Loyal Hunt ({stacks_of_hunters_tracking})"
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
            max(0, min(HUNTERS_TRACKING_STACK_MAXIMUM_V4, stacks_of_hunters_tracking))
            * damage_multiplier_per_stack
        )

        return DamageInstance(
            label=label,
            base_potency=base_potency,
            tags=tags,
            group_name="Loyal Hunt",
        )


class LoyalHuntV6(CombatAction):
    """Faelynn Ultimate (V6)."""

    @override
    def execute(self, stacks_of_hunters_tracking: int) -> DamageInstance:
        label: str = f"Loyal Hunt ({stacks_of_hunters_tracking})"
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
            max(0, min(HUNTERS_TRACKING_STACK_MAXIMUM_V4, stacks_of_hunters_tracking))
            * damage_multiplier_per_stack
        )

        return DamageInstance(
            label=label,
            base_potency=base_potency,
            tags=tags,
            group_name="Loyal Hunt",
        )


class HuntersInstinctI(CombatAction):
    """Faelynn's Hunter's Instinct I."""

    @override
    def execute(
        self, stacks_of_hunters_tracking: int, number_of_targets_hit: int
    ) -> DamageInstance:
        label: str = f"Hunter's Instinct I ({stacks_of_hunters_tracking})"
        base_potency: int = 60

        tags: set[DamageTag] = {
            DamageTag.ACTIVE,
            DamageTag.CORROSION,
            DamageTag.PHASE,
            DamageTag.AREA_OF_EFFECT,
        }

        damage_multiplier_per_stack: int = 5
        base_potency += (
            max(0, min(HUNTERS_TRACKING_STACK_MAXIMUM, stacks_of_hunters_tracking))
            * damage_multiplier_per_stack
        )

        if number_of_targets_hit == 1:
            base_potency += 30

        return DamageInstance(
            label=label,
            base_potency=base_potency,
            tags=tags,
            group_name="Hunter's Instinct I",
        )


class HuntersInstinctIV3(CombatAction):
    """Faelynn's Hunter's Instinct I (V3)."""

    @override
    def execute(
        self, stacks_of_hunters_tracking: int, number_of_targets_hit: int
    ) -> DamageInstance:
        label: str = f"Hunter's Instinct I ({stacks_of_hunters_tracking})"
        base_potency: int = 60

        tags: set[DamageTag] = {
            DamageTag.ACTIVE,
            DamageTag.CORROSION,
            DamageTag.PHASE,
            DamageTag.AREA_OF_EFFECT,
        }

        damage_multiplier_per_stack: int = 10
        base_potency += (
            max(0, min(HUNTERS_TRACKING_STACK_MAXIMUM, stacks_of_hunters_tracking))
            * damage_multiplier_per_stack
        )

        if number_of_targets_hit == 1:
            base_potency += 30

        return DamageInstance(
            label=label,
            base_potency=base_potency,
            tags=tags,
            group_name="Hunter's Instinct I",
        )


class HuntersInstinctIV4(CombatAction):
    """Faelynn's Hunter's Instinct I (V4)."""

    @override
    def execute(
        self, stacks_of_hunters_tracking: int, number_of_targets_hit: int
    ) -> DamageInstance:
        label: str = f"Hunter's Instinct I ({stacks_of_hunters_tracking})"
        base_potency: int = 60

        tags: set[DamageTag] = {
            DamageTag.ACTIVE,
            DamageTag.CORROSION,
            DamageTag.PHASE,
            DamageTag.AREA_OF_EFFECT,
        }

        damage_multiplier_per_stack: int = 10
        base_potency += (
            max(0, min(HUNTERS_TRACKING_STACK_MAXIMUM_V4, stacks_of_hunters_tracking))
            * damage_multiplier_per_stack
        )

        if number_of_targets_hit == 1:
            base_potency += 30

        return DamageInstance(
            label=label,
            base_potency=base_potency,
            tags=tags,
            group_name="Hunter's Instinct I",
        )


class HuntersInstinctIV6(CombatAction):
    """Faelynn's Hunter's Instinct I (V6)."""

    @override
    def execute(
        self, stacks_of_hunters_tracking: int, number_of_targets_hit: int
    ) -> DamageInstance:
        label: str = f"Hunter's Instinct I ({stacks_of_hunters_tracking})"
        base_potency: int = 90

        tags: set[DamageTag] = {
            DamageTag.ACTIVE,
            DamageTag.CORROSION,
            DamageTag.PHASE,
            DamageTag.AREA_OF_EFFECT,
        }

        damage_multiplier_per_stack: int = 10
        base_potency += (
            max(0, min(HUNTERS_TRACKING_STACK_MAXIMUM_V4, stacks_of_hunters_tracking))
            * damage_multiplier_per_stack
        )

        if number_of_targets_hit == 1:
            base_potency += 30

        return DamageInstance(
            label=label,
            base_potency=base_potency,
            tags=tags,
            group_name="Hunter's Instinct I",
        )


class HuntersInstinctII(CombatAction):
    """Faelynn's Hunter's Instinct II."""

    @override
    def execute(
        self,
        stacks_of_hunters_tracking: int,
        number_of_targets_hit: int,
        has_collar_brand: bool,
    ) -> DamageInstance:
        label: str = f"Hunter's Instinct II ({stacks_of_hunters_tracking})"
        base_potency: int = 120

        tags: set[DamageTag] = {
            DamageTag.ACTIVE,
            DamageTag.CORROSION,
            DamageTag.PHASE,
            DamageTag.AREA_OF_EFFECT,
        }

        damage_multiplier_per_stack: int = 5
        base_potency += (
            max(0, min(HUNTERS_TRACKING_STACK_MAXIMUM, stacks_of_hunters_tracking))
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
            group_name="Hunter's Instinct II",
            buffs_before=buffs_before,
        )


class HuntersInstinctIIV3(CombatAction):
    """Faelynn's Hunter's Instinct II (V3)."""

    @override
    def execute(
        self,
        stacks_of_hunters_tracking: int,
        number_of_targets_hit: int,
        has_collar_brand: bool,
    ) -> DamageInstance:
        label: str = f"Hunter's Instinct II ({stacks_of_hunters_tracking})"
        base_potency: int = 120

        tags: set[DamageTag] = {
            DamageTag.ACTIVE,
            DamageTag.CORROSION,
            DamageTag.PHASE,
            DamageTag.AREA_OF_EFFECT,
        }

        damage_multiplier_per_stack: int = 10
        base_potency += (
            max(0, min(HUNTERS_TRACKING_STACK_MAXIMUM, stacks_of_hunters_tracking))
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
            group_name="Hunter's Instinct II",
            buffs_before=buffs_before,
        )


class HuntersInstinctIIV4(CombatAction):
    """Faelynn's Hunter's Instinct II (V4)."""

    @override
    def execute(
        self,
        stacks_of_hunters_tracking: int,
        number_of_targets_hit: int,
        has_collar_brand: bool,
    ) -> DamageInstance:
        label: str = f"Hunter's Instinct II ({stacks_of_hunters_tracking})"
        base_potency: int = 120

        tags: set[DamageTag] = {
            DamageTag.ACTIVE,
            DamageTag.CORROSION,
            DamageTag.PHASE,
            DamageTag.AREA_OF_EFFECT,
        }

        damage_multiplier_per_stack: int = 10
        base_potency += (
            max(0, min(HUNTERS_TRACKING_STACK_MAXIMUM_V4, stacks_of_hunters_tracking))
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
            group_name="Hunter's Instinct II",
            buffs_before=buffs_before,
        )


class HuntersInstinctIIV6(CombatAction):
    """Faelynn's Hunter's Instinct II (V6)."""

    @override
    def execute(
        self,
        stacks_of_hunters_tracking: int,
        number_of_targets_hit: int,
        has_collar_brand: bool,
    ) -> DamageInstance:
        label: str = f"Hunter's Instinct II ({stacks_of_hunters_tracking})"
        base_potency: int = 170

        tags: set[DamageTag] = {
            DamageTag.ACTIVE,
            DamageTag.CORROSION,
            DamageTag.PHASE,
            DamageTag.AREA_OF_EFFECT,
        }

        damage_multiplier_per_stack: int = 10
        base_potency += (
            max(0, min(HUNTERS_TRACKING_STACK_MAXIMUM_V4, stacks_of_hunters_tracking))
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
            group_name="Hunter's Instinct II",
            buffs_before=buffs_before,
        )


class HuntersInstinctIII(CombatAction):
    """Faelynn's Hunter's Instinct III."""

    @override
    def execute(
        self,
        stacks_of_hunters_tracking: int,
        number_of_targets_hit: int,
        has_collar_brand: bool,
        target_tile_ascension_level: int,
    ) -> DamageInstance:
        label: str = f"Hunter's Instinct III ({stacks_of_hunters_tracking})"
        base_potency: int = 240

        tags: set[DamageTag] = {
            DamageTag.ACTIVE,
            DamageTag.CORROSION,
            DamageTag.PHASE,
            DamageTag.AREA_OF_EFFECT,
        }

        damage_multiplier_per_stack: int = 5
        base_potency += (
            max(0, min(HUNTERS_TRACKING_STACK_MAXIMUM, stacks_of_hunters_tracking))
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
            group_name="Hunter's Instinct III",
            buffs_before=buffs_before,
            debuffs_before=debuffs_before,
        )


class HuntersInstinctIIIV3(CombatAction):
    """Faelynn's Hunter's Instinct III (V3)."""

    @override
    def execute(
        self,
        stacks_of_hunters_tracking: int,
        number_of_targets_hit: int,
        has_collar_brand: bool,
        target_tile_ascension_level: int,
    ) -> DamageInstance:
        label: str = f"Hunter's Instinct III ({stacks_of_hunters_tracking})"
        base_potency: int = 240

        tags: set[DamageTag] = {
            DamageTag.ACTIVE,
            DamageTag.CORROSION,
            DamageTag.PHASE,
            DamageTag.AREA_OF_EFFECT,
        }

        damage_multiplier_per_stack: int = 10
        base_potency += (
            max(0, min(HUNTERS_TRACKING_STACK_MAXIMUM, stacks_of_hunters_tracking))
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
            group_name="Hunter's Instinct III",
            buffs_before=buffs_before,
            debuffs_before=debuffs_before,
        )


class HuntersInstinctIIIV4(CombatAction):
    """Faelynn's Hunter's Instinct III (V4)."""

    @override
    def execute(
        self,
        stacks_of_hunters_tracking: int,
        number_of_targets_hit: int,
        has_collar_brand: bool,
        target_tile_ascension_level: int,
    ) -> DamageInstance:
        label: str = f"Hunter's Instinct III ({stacks_of_hunters_tracking})"
        base_potency: int = 240

        tags: set[DamageTag] = {
            DamageTag.ACTIVE,
            DamageTag.CORROSION,
            DamageTag.PHASE,
            DamageTag.AREA_OF_EFFECT,
        }

        damage_multiplier_per_stack: int = 10
        base_potency += (
            max(0, min(HUNTERS_TRACKING_STACK_MAXIMUM_V4, stacks_of_hunters_tracking))
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
            group_name="Hunter's Instinct III",
            buffs_before=buffs_before,
            debuffs_before=debuffs_before,
        )


class HuntersInstinctIIIV6(CombatAction):
    """Faelynn's Hunter's Instinct III (V6)."""

    @override
    def execute(
        self,
        stacks_of_hunters_tracking: int,
        number_of_targets_hit: int,
        has_collar_brand: bool,
        target_tile_ascension_level: int,
    ) -> DamageInstance:
        label: str = f"Hunter's Instinct III ({stacks_of_hunters_tracking})"
        base_potency: int = 480

        tags: set[DamageTag] = {
            DamageTag.ACTIVE,
            DamageTag.CORROSION,
            DamageTag.PHASE,
            DamageTag.AREA_OF_EFFECT,
        }

        damage_multiplier_per_stack: int = 10
        base_potency += (
            max(0, min(HUNTERS_TRACKING_STACK_MAXIMUM_V4, stacks_of_hunters_tracking))
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
            group_name="Hunter's Instinct III",
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

    cuspid_combo: CombatAction = Field(default_factory=CuspidCombo)
    triple_maule: CombatAction = Field(default_factory=TripleMaule)
    triple_maule_followup: CombatAction = Field(default_factory=TripleMauleFollowup)
    scent_mark: CombatAction = Field(default_factory=ScentMarkAction)
    loyal_hunt: CombatAction = Field(default_factory=LoyalHunt)
    hunters_instinct_i: CombatAction = Field(default_factory=HuntersInstinctI)
    hunters_instinct_ii: CombatAction = Field(default_factory=HuntersInstinctII)
    hunters_instinct_iii: CombatAction = Field(default_factory=HuntersInstinctIII)

    def set_to_v0(self) -> None:
        """Sets Fortification Level to Segment00."""
        self.cuspid_combo = CuspidCombo()
        self.triple_maule = TripleMaule()
        self.triple_maule_followup = TripleMauleFollowup()
        self.scent_mark = ScentMarkAction()
        self.loyal_hunt = LoyalHunt()
        self.hunters_instinct_i = HuntersInstinctI()
        self.hunters_instinct_ii = HuntersInstinctII()
        self.hunters_instinct_iii = HuntersInstinctIII()

    def set_to_v2(self) -> None:
        """Sets Fortification Level to Segment02."""
        self.set_to_v0()

        self.triple_maule = TripleMauleV2()
        self.scent_mark = ScentMarkActionV2()

    def set_to_v3(self) -> None:
        """Sets Fortification Level to Segment03."""
        self.set_to_v2()

        self.loyal_hunt = LoyalHuntV3()
        self.hunters_instinct_i = HuntersInstinctIV3()
        self.hunters_instinct_ii = HuntersInstinctIIV3()
        self.hunters_instinct_iii = HuntersInstinctIIIV3()

    def set_to_v4(self) -> None:
        """Sets Fortification Level to Segment04."""
        self.set_to_v3()

        self.triple_maule = TripleMauleV4()
        self.loyal_hunt = LoyalHuntV4()
        self.hunters_instinct_i = HuntersInstinctIV4()
        self.hunters_instinct_ii = HuntersInstinctIIV4()
        self.hunters_instinct_iii = HuntersInstinctIIIV4()

    def set_to_v5(self) -> None:
        """Sets Fortification Level to Segment05."""
        self.set_to_v4()

        self.triple_maule = TripleMauleV5()
        self.triple_maule_followup = TripleMauleFollowupV5()

    def set_to_v6(self) -> None:
        """Sets Fortification Level to Segment06."""
        self.set_to_v5()

        self.loyal_hunt = LoyalHuntV6()
        self.hunters_instinct_i = HuntersInstinctIV6()
        self.hunters_instinct_ii = HuntersInstinctIIV6()
        self.hunters_instinct_iii = HuntersInstinctIIIV6()

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
