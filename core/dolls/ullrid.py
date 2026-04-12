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
    PhysicalSummonedUnit,
)
from core.buffs import Buff
from core.combat import (
    DamageInstance,
    CombatAction,
    UllridDamageCalculationStrategy,
)


class WarningShot(CombatAction):
    """Ullrid Basic Attack."""

    @override
    def execute(self) -> DamageInstance:
        label: str = "Warning Shot"
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
            group_name="Warning Shot",
            damage_calculation_strategy=UllridDamageCalculationStrategy(),
        )


class HuntersSight(CombatAction):
    """Ullrid S1."""

    @override
    def execute(self) -> DamageInstance:
        label: str = "Hunter's Sight"
        base_potency: int = 150

        tags: set[DamageTag] = {
            DamageTag.ACTIVE,
            DamageTag.PHYSICAL,
            DamageTag.LIGHT_AMMO,
            DamageTag.TARGETED,
        }

        return DamageInstance(
            label=label,
            base_potency=base_potency,
            tags=tags,
            group_name="Hunter's Sight",
            damage_calculation_strategy=UllridDamageCalculationStrategy(),
        )


class MarkOfPrey(CombatAction):
    """Action triggered when debuff holder ends their turn within a 5-tile radius of Ullrid."""

    @override
    def execute(self) -> DamageInstance:
        label: str = "Mark of Prey"
        base_potency: int = 100

        tags: set[DamageTag] = {
            DamageTag.PASSIVE,
            DamageTag.PHYSICAL,
            DamageTag.LIGHT_AMMO,
            DamageTag.AREA_OF_EFFECT,
        }

        return DamageInstance(
            label=label,
            base_potency=base_potency,
            tags=tags,
            group_name="Mark of Prey",
            damage_calculation_strategy=UllridDamageCalculationStrategy(),
        )


class BladeWhirlwind(CombatAction):
    """Ullrid S2."""

    @override
    def execute(self, attacking_same_target_within_one_action: bool) -> DamageInstance:
        label: str = "Blade Whirlwind"
        base_potency: int = 90

        tags: set[DamageTag] = {
            DamageTag.ACTIVE,
            DamageTag.PHYSICAL,
            DamageTag.MELEE,
            DamageTag.TARGETED,
            DamageTag.CONFECTANCE,
        }

        return DamageInstance(
            label=label,
            base_potency=base_potency,
            tags=tags,
            group_name="Blade Whirlwind",
            damage_calculation_strategy=UllridDamageCalculationStrategy(),
        )


class BladeWhirlwindV1(CombatAction):
    """Ullrid S2 (V1)."""

    @override
    def execute(self, attacking_same_target_within_one_action: bool) -> DamageInstance:
        label: str = "Blade Whirlwind"
        base_potency: int = 90

        tags: set[DamageTag] = {
            DamageTag.ACTIVE,
            DamageTag.PHYSICAL,
            DamageTag.MELEE,
            DamageTag.TARGETED,
            DamageTag.CONFECTANCE,
        }

        buffs_before: list[Buff] = []

        if attacking_same_target_within_one_action:
            # If attacking the same target within one action, increases damage dealt by 30%.
            buffs_before.append(
                Buff(
                    value=30,
                    modifier_type=ModifierType.ADDITIVE,
                    stat_type=SpecialAttribute.DAMAGE_BOOST,
                    tag=DamageTag.CONFECTANCE,
                )
            )

        return DamageInstance(
            label=label,
            base_potency=base_potency,
            tags=tags,
            buffs_before=buffs_before,
            group_name="Blade Whirlwind",
            damage_calculation_strategy=UllridDamageCalculationStrategy(),
        )


class DeterminedPursuit(CombatAction):
    """Followup to Blade Whirlwind when target is still alive. Granted by Expansion Key - Determined Pursuit (Tier 1)."""

    @override
    def execute(self) -> DamageInstance:
        label: str = "Determined Pursuit"
        base_potency: int = 90

        tags: set[DamageTag] = {
            DamageTag.PASSIVE,
            DamageTag.PHYSICAL,
            DamageTag.TARGETED,
        }

        # Expansion Key - Determined Pursuit (Tier 1):
        # The damage of this attack is increased by 30%.

        return DamageInstance(
            label=label,
            base_potency=base_potency,
            tags=tags,
            group_name="Determined Pursuit",
            buffs_before=[
                Buff(
                    value=30,
                    modifier_type=ModifierType.ADDITIVE,
                    stat_type=SpecialAttribute.DAMAGE_BOOST,
                    tag=DamageTag.ALL,
                )
            ],
            damage_calculation_strategy=UllridDamageCalculationStrategy(),
        )


class HiddenPursuit(CombatAction):
    """Ullrid Ultimate."""

    @override
    def execute(
        self, stacks_of_hunters_talent: int, percent_target_missing_health: float
    ) -> DamageInstance:
        label: str = f"Hidden Pursuit ({stacks_of_hunters_talent})"
        base_potency: int = 180

        tags: set[DamageTag] = {
            DamageTag.ACTIVE,
            DamageTag.PHYSICAL,
            DamageTag.MELEE,
            DamageTag.TARGETED,
            DamageTag.ULTIMATE,
        }

        buffs_before: list[Buff] = []

        increased_damage_per_stack: int = 10
        maximum_increased_damage: int = 30

        if stacks_of_hunters_talent > 0:
            buffs_before.append(
                Buff(
                    value=min(
                        stacks_of_hunters_talent * increased_damage_per_stack,
                        maximum_increased_damage,
                    ),
                    modifier_type=ModifierType.ADDITIVE,
                    stat_type=SpecialAttribute.DAMAGE_BOOST,
                    tag=DamageTag.ULTIMATE,
                )
            )

        return DamageInstance(
            label=label,
            base_potency=base_potency,
            tags=tags,
            group_name="Hidden Pursuit",
            buffs_before=buffs_before,
            damage_calculation_strategy=UllridDamageCalculationStrategy(),
        )


class HiddenPursuitV4(CombatAction):
    """Ullrid Ultimate (V4)."""

    @override
    def execute(
        self, stacks_of_hunters_talent: int, percent_target_missing_health: float
    ) -> DamageInstance:
        label: str = f"Hidden Pursuit ({stacks_of_hunters_talent})"
        base_potency: int = 180

        tags: set[DamageTag] = {
            DamageTag.ACTIVE,
            DamageTag.PHYSICAL,
            DamageTag.MELEE,
            DamageTag.TARGETED,
            DamageTag.ULTIMATE,
        }

        buffs_before: list[Buff] = []

        increased_damage_per_stack: int = 10
        maximum_increased_damage: int = 60

        if stacks_of_hunters_talent > 0:
            buffs_before.append(
                Buff(
                    value=min(
                        stacks_of_hunters_talent * increased_damage_per_stack,
                        maximum_increased_damage,
                    ),
                    modifier_type=ModifierType.ADDITIVE,
                    stat_type=SpecialAttribute.DAMAGE_BOOST,
                    tag=DamageTag.ULTIMATE,
                )
            )

        return DamageInstance(
            label=label,
            base_potency=base_potency,
            tags=tags,
            group_name="Hidden Pursuit",
            buffs_before=buffs_before,
            damage_calculation_strategy=UllridDamageCalculationStrategy(),
        )


class HiddenPursuitV6(CombatAction):
    """Ullrid Ultimate (V6)."""

    @override
    def execute(
        self, stacks_of_hunters_talent: int, percent_target_missing_health: float
    ) -> DamageInstance:
        label: str = f"Hidden Pursuit ({stacks_of_hunters_talent})"
        base_potency: int = 180

        tags: set[DamageTag] = {
            DamageTag.ACTIVE,
            DamageTag.PHYSICAL,
            DamageTag.MELEE,
            DamageTag.TARGETED,
            DamageTag.ULTIMATE,
        }

        buffs_before: list[Buff] = []

        increased_damage_per_stack: int = 10
        maximum_increased_damage: int = 60

        if stacks_of_hunters_talent > 0:
            buffs_before.append(
                Buff(
                    value=min(
                        stacks_of_hunters_talent * increased_damage_per_stack,
                        maximum_increased_damage,
                    ),
                    modifier_type=ModifierType.ADDITIVE,
                    stat_type=SpecialAttribute.DAMAGE_BOOST,
                    tag=DamageTag.ULTIMATE,
                )
            )

        # For every 2% of the enemy target's missing health, increase self attack by 1% for this skill.
        attack_increase_from_missing_health: int = int(
            percent_target_missing_health // 2
        )

        buffs_before.append(
            Buff(
                value=attack_increase_from_missing_health,
                modifier_type=ModifierType.MULTIPLICATIVE,
                stat_type=StatType.ATTACK,
            )
        )

        return DamageInstance(
            label=label,
            base_potency=base_potency,
            tags=tags,
            group_name="Hidden Pursuit",
            buffs_before=buffs_before,
            damage_calculation_strategy=UllridDamageCalculationStrategy(),
        )


class LaceratingWound(CombatAction):
    """Effect from Lacerating Wound debuff applied from Mark of Prey and Expansion Key - Determined Pursuit (Tier 2).
    When taking damage, if the attacker used a blade, take an additional instance of damage equal to 40% of the original damage.
    Modeled as a separate instance taking in the original damage instance potency and using 40% of it.

    TODO: This will break when other blade-wielding Dolls take advantage of this debuff. It should be factored out to Common
    like Overburn and implemented for each blade-wielding Doll.
    """

    @override
    def execute(self, original_damage_instance_potency: int) -> DamageInstance:
        label: str = f"Lacerating Wound ({original_damage_instance_potency})"
        base_potency: int = int(original_damage_instance_potency * 0.4)

        tags: set[DamageTag] = {
            DamageTag.PASSIVE,
            DamageTag.PHYSICAL,
            DamageTag.TARGETED,
        }

        return DamageInstance(
            label=label,
            base_potency=base_potency,
            tags=tags,
            group_name="Lacerating Wound",
            damage_calculation_strategy=UllridDamageCalculationStrategy(),
        )


class Ullrid(Doll):
    """Ullrid."""

    name: str = "Ullrid"
    irrelevant_damage_tags: ClassVar[set[DamageTag]] = set(
        [
            DamageTag.CORROSION,
            DamageTag.BURN,
            DamageTag.FREEZE,
            DamageTag.HYDRO,
            DamageTag.PHASE,
            DamageTag.ELECTRIC,
            DamageTag.MEDIUM_AMMO,
            DamageTag.HEAVY_AMMO,
            DamageTag.SHOTGUN_AMMO,
            DamageTag.SUPPORT_ACTION,
            DamageTag.COUNTERATTACK,
            DamageTag.INTERCEPTION,
            DamageTag.FIXED,
            DamageTag.PHYSICAL_SUMMON,
        ]
    )

    warning_shot: CombatAction = Field(default_factory=WarningShot)
    hunters_sight: CombatAction = Field(default_factory=HuntersSight)
    blade_whirlwind: CombatAction = Field(default_factory=BladeWhirlwind)
    determined_pursuit: CombatAction = Field(default_factory=DeterminedPursuit)
    mark_of_prey: CombatAction = Field(default_factory=MarkOfPrey)
    hidden_pursuit: CombatAction = Field(default_factory=HiddenPursuit)
    lacerating_wound: CombatAction = Field(default_factory=LaceratingWound)

    def set_to_v0(self) -> None:
        """Sets Fortification Level to Segment00."""
        self.warning_shot = WarningShot()
        self.hunters_sight = HuntersSight()
        self.blade_whirlwind = BladeWhirlwind()
        self.determined_pursuit = DeterminedPursuit()
        self.mark_of_prey = MarkOfPrey()
        self.hidden_pursuit = HiddenPursuit()
        self.lacerating_wound = LaceratingWound()

    def set_to_v1(self) -> None:
        """Sets Fortification Level to Segment01."""
        self.set_to_v0()

        self.blade_whirlwind = BladeWhirlwindV1()

    def set_to_v4(self) -> None:
        """Sets Fortification Level to Segment04."""
        self.set_to_v1()

        self.hidden_pursuit = HiddenPursuitV4()

    def set_to_v6(self) -> None:
        """Sets Fortification Level to Segment06."""
        self.set_to_v4()

        self.hidden_pursuit = HiddenPursuitV6()

    @override
    def set_fortification_level(self, level: FortificationLevel):
        self.fortification_level = level
        match level:
            case FortificationLevel.SEGMENT00:
                self.set_to_v0()
            case FortificationLevel.SEGMENT01:
                self.set_to_v1()
            case FortificationLevel.SEGMENT02:
                self.set_to_v1()
            case FortificationLevel.SEGMENT03:
                self.set_to_v1()
            case FortificationLevel.SEGMENT04:
                self.set_to_v4()
            case FortificationLevel.SEGMENT05:
                self.set_to_v4()
            case FortificationLevel.SEGMENT06:
                self.set_to_v6()
