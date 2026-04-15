from typing import override, ClassVar
from pydantic import Field

from core.types import (
    DamageTag,
    FortificationLevel,
    Doll,
    SummonedUnit,
    StatType,
    ModifierType,
    SpecialAttribute,
)
from core.buffs import Buff
from core.combat import DamageInstance, CombatAction, HelenDamageCalculationStrategy


class Condensation(CombatAction):
    """Helen Basic Attack."""

    @override
    def execute(self, stacks_sharpened_edge: int) -> DamageInstance:
        label: str = f"Condensation ({stacks_sharpened_edge} Sharpened Edge)"
        base_potency: int = 80
        tags: set[DamageTag] = {
            DamageTag.ACTIVE,
            DamageTag.BASIC,
            DamageTag.SHOTGUN_AMMO,
            DamageTag.TARGETED,
            DamageTag.FREEZE,
            DamageTag.PHASE,
        }

        critical_rate_increase_per_stack_sharpened_edge: int = 10
        freeze_damage_increase_per_stack_sharpened_edge: int = 10

        buffs_before: list[Buff] = []

        if stacks_sharpened_edge > 0:
            # Passive: Fearless Valkyrie
            # While Helen has [Sharpened Edge], the damage multiplier of her basic attack is increased to 180%.
            base_potency = 180

            # For every 1 stack of [Sharpened Edge], increases own critical rate and Freeze damage dealt by basic attack by 10%.
            buffs_before.append(
                Buff(
                    value=stacks_sharpened_edge
                    * critical_rate_increase_per_stack_sharpened_edge,
                    modifier_type=ModifierType.ADDITIVE,
                    stat_type=StatType.CRIT_RATE,
                    tag=DamageTag.BASIC,
                )
            )

            buffs_before.append(
                Buff(
                    value=stacks_sharpened_edge
                    * freeze_damage_increase_per_stack_sharpened_edge,
                    modifier_type=ModifierType.ADDITIVE,
                    stat_type=SpecialAttribute.DAMAGE_BOOST,
                    tag=DamageTag.BASIC,
                )
            )

        return DamageInstance(
            label=label,
            base_potency=base_potency,
            tags=tags,
            group_name="Condensation",
            buffs_before=buffs_before,
            damage_calculation_strategy=HelenDamageCalculationStrategy(),
        )


class CondensationV6(CombatAction):
    """Helen Basic Attack (V6)."""

    @override
    def execute(self, stacks_sharpened_edge: int) -> DamageInstance:
        label: str = f"Condensation ({stacks_sharpened_edge} Sharpened Edge)"
        base_potency: int = 80
        tags: set[DamageTag] = {
            DamageTag.ACTIVE,
            DamageTag.BASIC,
            DamageTag.SHOTGUN_AMMO,
            DamageTag.TARGETED,
            DamageTag.FREEZE,
            DamageTag.PHASE,
        }

        critical_rate_increase_per_stack_sharpened_edge: int = 10
        freeze_damage_increase_per_stack_sharpened_edge: int = 10

        buffs_before: list[Buff] = []

        if stacks_sharpened_edge > 0:
            # Passive: Fearless Valkyrie
            # While Helen has [Sharpened Edge], the damage multiplier of her basic attack is increased to 300%.
            base_potency = 300

            # For every 1 stack of [Sharpened Edge], increases own critical rate and Freeze damage dealt by basic attack by 10%.
            buffs_before.append(
                Buff(
                    value=stacks_sharpened_edge
                    * critical_rate_increase_per_stack_sharpened_edge,
                    modifier_type=ModifierType.ADDITIVE,
                    stat_type=StatType.CRIT_RATE,
                    tag=DamageTag.BASIC,
                )
            )

            buffs_before.append(
                Buff(
                    value=stacks_sharpened_edge
                    * freeze_damage_increase_per_stack_sharpened_edge,
                    modifier_type=ModifierType.ADDITIVE,
                    stat_type=SpecialAttribute.DAMAGE_BOOST,
                    tag=DamageTag.BASIC,
                )
            )

        return DamageInstance(
            label=label,
            base_potency=base_potency,
            tags=tags,
            group_name="Condensation",
            buffs_before=buffs_before,
            damage_calculation_strategy=HelenDamageCalculationStrategy(),
        )


class Helen(Doll):
    """Helen."""

    name: str = "Helen"
    irrelevant_damage_tags: ClassVar[set[DamageTag]] = set(
        [
            DamageTag.PHYSICAL,
            DamageTag.CORROSION,
            DamageTag.BURN,
            DamageTag.HYDRO,
            DamageTag.ELECTRIC,
            DamageTag.MELEE,
            DamageTag.MEDIUM_AMMO,
            DamageTag.HEAVY_AMMO,
            DamageTag.LIGHT_AMMO,
            DamageTag.SUPPORT_ACTION,
            DamageTag.INTERCEPTION,
            DamageTag.COUNTERATTACK,
            DamageTag.AREA_OF_EFFECT,
            DamageTag.ULTIMATE,
            DamageTag.PHYSICAL_SUMMON,
            DamageTag.FIXED,
            DamageTag.CONFECTANCE,
        ]
    )

    condensation: CombatAction = Field(default_factory=Condensation)

    def set_to_v0(self) -> None:
        """Sets Fortification Level to Segment00."""
        self.condensation = Condensation()

    def set_to_v6(self) -> None:
        """Sets Fortification Level to Segment06."""
        self.set_to_v0()

        self.condensation = CondensationV6()

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
                self.set_to_v6()
