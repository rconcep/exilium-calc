from __future__ import annotations

from dataclasses import dataclass, field
from abc import ABC, abstractmethod
from typing import final

from core.types import (
    DamageTag,
    DamageTagMultipliers,
    Unit,
    StatType,
    ModifierType,
    SpecialAttribute,
    DefenseIgnoreMultipliers,
    IncreasedDamageMultipliers,
)
from core.buffs import Buff, Debuff


class DamageCalculationStrategy(ABC):
    """Strategy pattern for damage calculation. This allows for different versions of the damage formula to be used"""

    def calculate_damage(
        self,
        attacker: Unit,
        target: Unit,
        damage_instance: DamageInstance,
        is_stability_broken: bool = True,
        phase_weaknesses_exploited: int = 0,
        buffs_before: list[Buff] = [],
        debuffs_before: list[Debuff] = [],
    ) -> CombatSummary:
        """Returns a summary of the combat action.

        Arguments:
        attacker -- the attacking Unit
        target -- the target of the attack
        damage_instance -- describes the action
        is_stability_broken -- True if the target is in stability break
        phase_weaknesses_exploited -- the number of phase weaknesses exploited by the action
        buffs_before -- Buffs to apply to attacker before the action
        debuffs_before -- Debuffs to apply to target before the action
        """
        # Apply buffs and debuffs before
        self.resolve_buffs(
            attacker, target, damage_instance, buffs_before, debuffs_before
        )
        total_damage_boost_multipliers: DamageTagMultipliers = (
            attacker.get_effective_special_attribute(SpecialAttribute.DAMAGE_BOOST)
        )

        # Compute the base damage
        effective_atk, effective_def, negative_def, term1 = self.calculate_base_damage(
            attacker, target, damage_instance
        )

        if True:  # TODO: check if have reversed assault
            bonus_increased_damage = self.resolve_reversed_assault(
                damage_instance, negative_def
            )
            total_damage_boost_multipliers.add_to_multiplier(
                DamageTag.PHYSICAL, bonus_increased_damage
            )

        # TODO: check conditional modifiers before adding: exposed, in stability break,
        # close proximity, distance, has overburn, etc.
        damage_instance.tags.add(DamageTag.EXPOSED)
        damage_instance.tags.add(DamageTag.STABILITY_BROKEN)
        damage_instance.tags.add(DamageTag.BOSS)

        # Recompute adjusted potency to get the effective damage multiplier
        damage_instance.calculate_adjusted_potency(total_damage_boost_multipliers)
        effective_dmg_multiplier: float = damage_instance.adjusted_potency / 100

        # Resolve "increased damage taken" effects
        increased_damage_taken: float = self.resolve_increased_damage_taken(
            target, damage_instance
        )

        non_critical_damage: float = (
            effective_dmg_multiplier * term1 * (1 + increased_damage_taken / 100)
        )

        # Apply stability damage reduction
        if not is_stability_broken:
            non_critical_damage = non_critical_damage * (
                1
                - target.initial_stats.basic_attributes[
                    StatType.STABILITY_DAMAGE_REDUCTION
                ]
                / 100
            )

        # Apply multiplier from phase weaknesses exploited
        MORE_DAMAGE_PER_WEAKNESS_EXPLOITED: float = 0.10
        MAX_PHASE_WEAKNESSES_EXPLOITABLE: int = 2
        non_critical_damage = non_critical_damage * (
            1
            + MORE_DAMAGE_PER_WEAKNESS_EXPLOITED
            * min(phase_weaknesses_exploited, MAX_PHASE_WEAKNESSES_EXPLOITABLE)
        )

        # Account for critical hit
        crit_rate: float = attacker.get_basic_attribute(StatType.CRIT_RATE) / 100
        crit_dmg_multiplier: float = (
            attacker.get_effective_critical_damage_multiplier(damage_instance.tags)
            / 100
        )

        critical_damage: float = crit_dmg_multiplier * non_critical_damage

        effective_crit_rate: float = min(1.0, crit_rate)

        expected_damage: float = (
            effective_crit_rate * critical_damage
            + (1 - effective_crit_rate) * non_critical_damage
        )

        combat_summary: CombatSummary = CombatSummary(
            non_critical_damage=non_critical_damage,
            critical_damage=critical_damage,
            expected_damage=expected_damage,
            effective_damage_multiplier=effective_dmg_multiplier,
            effective_critical_rate=crit_rate,
            effective_critical_damage_multiplier=crit_dmg_multiplier,
            effective_attack=effective_atk,
            effective_defense=effective_def,
            negative_defense=negative_def,
        )

        return combat_summary

    @final
    def resolve_buffs(
        self,
        attacker: Unit,
        target: Unit,
        damage_instance: DamageInstance,
        buffs_before: list[Buff] = [],
        debuffs_before: list[Debuff] = [],
    ) -> None:
        """Collects all of the stat modifiers from damage_instance and the explicit buff/debuffs_before
        and applies it to the respective targets.

        Arguments:
        attacker -- the attacking Unit
        target -- the target of the attack
        damage_instance -- describes the action
        buffs_before -- Buffs to apply to attacker before the action
        debuffs_before -- Debuffs to apply to target before the action
        """
        for buff in buffs_before + damage_instance.buffs_before:
            if isinstance(buff.stat_type, StatType):
                if buff.modifier_type == ModifierType.ADDITIVE:
                    attacker.additive_modifiers.basic_attributes[
                        buff.stat_type
                    ] += buff.value
                elif buff.modifier_type == ModifierType.MULTIPLICATIVE:
                    attacker.multiplicative_modifiers.basic_attributes[
                        buff.stat_type
                    ] += buff.value
                else:
                    TypeError("Unexpected modifier type")
            elif isinstance(buff.stat_type, SpecialAttribute):
                if buff.modifier_type == ModifierType.ADDITIVE:
                    attacker.additive_modifiers.special_attributes[
                        buff.stat_type
                    ].add_to_multiplier(buff.tag, buff.value)
                elif buff.modifier_type == ModifierType.MULTIPLICATIVE:
                    attacker.multiplicative_modifiers.special_attributes[
                        buff.stat_type
                    ].add_to_multiplier(buff.tag, buff.value)
                else:
                    TypeError("Unexpected modifier type")

        for debuff in debuffs_before + damage_instance.debuffs_before:
            if isinstance(debuff.stat_type, StatType):
                if debuff.modifier_type == ModifierType.ADDITIVE:
                    target.additive_modifiers.basic_attributes[
                        debuff.stat_type
                    ] += debuff.value
                elif debuff.modifier_type == ModifierType.MULTIPLICATIVE:
                    target.multiplicative_modifiers.basic_attributes[
                        debuff.stat_type
                    ] += debuff.value
                else:
                    TypeError("Unexpected modifier type")
            elif isinstance(debuff.stat_type, SpecialAttribute):
                if debuff.modifier_type == ModifierType.ADDITIVE:
                    target.additive_modifiers.special_attributes[
                        debuff.stat_type
                    ].add_to_multiplier(debuff.tag, debuff.value)
                elif debuff.modifier_type == ModifierType.MULTIPLICATIVE:
                    target.multiplicative_modifiers.special_attributes[
                        debuff.stat_type
                    ].add_to_multiplier(debuff.tag, debuff.value)
                else:
                    TypeError("Unexpected modifier type")

    @abstractmethod
    def calculate_base_damage(
        self, attacker: Unit, target: Unit, damage_instance: DamageInstance
    ) -> tuple[float, float, float, float]:
        """Returns the term in the damage formula that is a function of attacker attack
        and target defense. In addition, returns the effective attack, effective defense,
        and any defense reduced/ignored beyond 0.

        Arguments:
        attacker -- the attacking Unit
        target -- the target of the attack
        damage_instance -- describes the action
        """
        ...

    @final
    def resolve_reversed_assault(
        self, damage_instance: DamageInstance, negative_def: float
    ) -> float:
        """Returns the increased damage bonus as a result of the Reversed Assault
        (formerly, Defense Shredding) buff.

        Arguments:
        damage_instance -- describes the action
        negative_def -- the % of defense ignored/reduced beyond 0
        """
        bonus_increased_damage: float = 0
        bonus_damage_per_negative_def: float = 0

        if DamageTag.PHYSICAL in damage_instance.tags:
            if 0 < negative_def and negative_def < 100:
                bonus_damage_per_negative_def = 0.5
            elif 100 <= negative_def and negative_def < 200:
                bonus_damage_per_negative_def = 0.75
            elif 200 <= negative_def and negative_def < 300:
                bonus_damage_per_negative_def = 1
            elif 300 <= negative_def:
                bonus_damage_per_negative_def = 1.5
            else:
                pass

            bonus_increased_damage = negative_def * bonus_damage_per_negative_def

        return bonus_increased_damage

    @final
    def resolve_increased_damage_taken(
        self, target: Unit, damage_instance: DamageInstance
    ) -> float:
        """Returns the damage multiplier based on the target's Increased Damage Taken stats and
        damage_instance.

        Arguments:
        target -- the target of the attack
        damage_instance -- describes the action
        """
        increased_damage_taken_mult: IncreasedDamageMultipliers = (
            target.initial_stats.special_attributes[
                SpecialAttribute.INCREASE_DAMAGE_TAKEN
            ]
            + target.additive_modifiers.special_attributes[
                SpecialAttribute.INCREASE_DAMAGE_TAKEN
            ]
        )

        return increased_damage_taken_mult.get_total_multiplier(damage_instance.tags)


class StandardDamageCalculationStrategy(DamageCalculationStrategy):
    """Implements the standard damage formula where base damage is solely a function of attack and defense."""

    @final
    def calculate_base_damage(
        self, attacker: Unit, target: Unit, damage_instance: DamageInstance
    ) -> tuple[float, float, float, float]:
        """Returns the term in the damage formula that is a function of attacker attack
        and target defense. In addition, returns the effective attack, effective defense,
        and any defense reduced/ignored beyond 0.

        Arguments:
        attacker -- the attacking Unit
        target -- the target of the attack
        damage_instance -- describes the action
        """
        total_defense_ignore_multipliers: DefenseIgnoreMultipliers = (
            attacker.initial_stats.special_attributes[SpecialAttribute.DEFENSE_IGNORE]
            + attacker.additive_modifiers.special_attributes[
                SpecialAttribute.DEFENSE_IGNORE
            ]
        )

        effective_atk: float = attacker.get_basic_attribute(StatType.ATTACK)
        effective_def: float = (
            target.initial_stats.basic_attributes[StatType.DEFENSE]
            + target.additive_modifiers.basic_attributes[StatType.DEFENSE]
        )

        ignore_def: float = (
            total_defense_ignore_multipliers.get_total_multiplier(damage_instance.tags)
            - target.multiplicative_modifiers.basic_attributes[StatType.DEFENSE]
        )  # defense down is additive with ignore defense
        negative_def: float = max(0, ignore_def - 100)
        effective_def: float = max(0, effective_def * (1 - ignore_def / 100))

        return (
            effective_atk,
            effective_def,
            negative_def,
            effective_atk / (1 + effective_def / effective_atk),
        )


@dataclass
class DamageInstance:
    """An instance of damage."""

    label: str
    base_potency: float
    tags: set[DamageTag] = field(default_factory=set)
    adjusted_potency: float = 0
    group_name: str = ""
    buffs_before: list[Buff] = field(default_factory=list)
    debuffs_before: list[Debuff] = field(default_factory=list)
    damage_calculation_strategy: DamageCalculationStrategy = field(
        default_factory=StandardDamageCalculationStrategy
    )

    def calculate_adjusted_potency(self, mult: DamageTagMultipliers) -> float:
        """
        Calculates the adjusted potency from the base potency, given a set of
        increased damage multipliers.

        Arguments:
        mult -- the increased damage multipliers to apply
        """
        self.adjusted_potency = (
            1 + mult.get_total_multiplier(self.tags) / 100.0
        ) * self.base_potency
        return self.adjusted_potency


@dataclass
class CombatAction(ABC):
    """Represents an action in combat (i.e., skill usage or event)."""

    @abstractmethod
    def execute(self, *args, **kwargs) -> DamageInstance:
        """Use/execute this action."""
        pass


@dataclass
class CombatSummary:
    """Summarizes the result of an a combat action."""

    non_critical_damage: float = 0
    critical_damage: float = 0
    expected_damage: float = 0
    effective_damage_multiplier: float = 0
    effective_critical_rate: float = 0
    effective_critical_damage_multiplier: float = 0
    effective_attack: float = 0
    effective_defense: float = 0
    negative_defense: float = 0


def sum_damage_instances(
    damage_instances: list[DamageInstance],
    tag: DamageTag,
    do_exclude: bool = False,
) -> DamageInstance:
    """
    Returns a DamageInstance with the combined potencies of all DamageInstances in
    damage_instances that have the DamageTag tag. If do_exclude is True, filter out
    DamageInstances by tag instead.

    Arguments:
    damage_instances -- the DamageInstance instances to be combined
    tag -- the DamageTag to filter by
    do_exclude -- True if the tag filter means 'exclude' this tag
    """
    combined_base_potency: float = 0
    combined_adjusted_potency: float = 0
    for damage_instance in damage_instances:
        do_add: bool = False

        if do_exclude and tag not in damage_instance.tags:
            do_add = True
        elif not do_exclude and tag in damage_instance.tags:
            do_add = True

        if do_add:
            combined_base_potency += damage_instance.base_potency
            combined_adjusted_potency += damage_instance.adjusted_potency

    return DamageInstance(
        "Combined",
        combined_base_potency,
        tags={tag},
        adjusted_potency=combined_adjusted_potency,
    )
