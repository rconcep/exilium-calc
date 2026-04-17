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


class Guardian(CombatAction):
    """Helen Basic Attack."""

    @override
    def execute(self, stacks_icy_edge: int) -> DamageInstance:
        label: str = f"Guardian ({stacks_icy_edge} Icy Edge)"
        base_potency: int = 80
        tags: set[DamageTag] = {
            DamageTag.ACTIVE,
            DamageTag.BASIC,
            DamageTag.SHOTGUN_AMMO,
            DamageTag.TARGETED,
            DamageTag.FREEZE,
            DamageTag.PHASE,
        }

        critical_rate_increase_per_stack_icy_edge: int = 10
        freeze_damage_increase_per_stack_icy_edge: int = 10

        buffs_before: list[Buff] = []

        if stacks_icy_edge > 0:
            # Passive: Fearless Valkyrie
            # While Helen has [Icy Edge], the damage multiplier of her basic attack is increased to 180%.
            base_potency = 180

            # For every 1 stack of [Icy Edge], increases own critical rate and Freeze damage dealt by basic attack by 10%.
            buffs_before.append(
                Buff(
                    value=stacks_icy_edge * critical_rate_increase_per_stack_icy_edge,
                    modifier_type=ModifierType.ADDITIVE,
                    stat_type=StatType.CRIT_RATE,
                    tag=DamageTag.BASIC,
                )
            )

            buffs_before.append(
                Buff(
                    value=stacks_icy_edge * freeze_damage_increase_per_stack_icy_edge,
                    modifier_type=ModifierType.ADDITIVE,
                    stat_type=SpecialAttribute.DAMAGE_BOOST,
                    tag=DamageTag.BASIC,
                )
            )

        return DamageInstance(
            label=label,
            base_potency=base_potency,
            tags=tags,
            group_name="Guardian",
            buffs_before=buffs_before,
            damage_calculation_strategy=HelenDamageCalculationStrategy(),
        )


class GuardianV6(CombatAction):
    """Helen Basic Attack (V6)."""

    @override
    def execute(self, stacks_icy_edge: int) -> DamageInstance:
        label: str = f"Guardian ({stacks_icy_edge} Icy Edge)"
        base_potency: int = 80
        tags: set[DamageTag] = {
            DamageTag.ACTIVE,
            DamageTag.BASIC,
            DamageTag.SHOTGUN_AMMO,
            DamageTag.TARGETED,
            DamageTag.FREEZE,
            DamageTag.PHASE,
        }

        critical_rate_increase_per_stack_icy_edge: int = 10
        freeze_damage_increase_per_stack_icy_edge: int = 10

        buffs_before: list[Buff] = []

        if stacks_icy_edge > 0:
            # Passive: Fearless Valkyrie
            # While Helen has [Icy Edge], the damage multiplier of her basic attack is increased to 300%.
            base_potency = 300

            # For every 1 stack of [Icy Edge], increases own critical rate and Freeze damage dealt by basic attack by 10%.
            buffs_before.append(
                Buff(
                    value=stacks_icy_edge * critical_rate_increase_per_stack_icy_edge,
                    modifier_type=ModifierType.ADDITIVE,
                    stat_type=StatType.CRIT_RATE,
                    tag=DamageTag.BASIC,
                )
            )

            buffs_before.append(
                Buff(
                    value=stacks_icy_edge * freeze_damage_increase_per_stack_icy_edge,
                    modifier_type=ModifierType.ADDITIVE,
                    stat_type=SpecialAttribute.DAMAGE_BOOST,
                    tag=DamageTag.BASIC,
                )
            )

        return DamageInstance(
            label=label,
            base_potency=base_potency,
            tags=tags,
            group_name="Guardian",
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

    guardian: CombatAction = Field(default_factory=Guardian)

    def set_to_v0(self) -> None:
        """Sets Fortification Level to Segment00."""
        self.guardian = Guardian()

    def set_to_v6(self) -> None:
        """Sets Fortification Level to Segment06."""
        self.set_to_v0()

        self.guardian = GuardianV6()

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
