from __future__ import annotations

from pydantic import BaseModel, Field
from abc import ABC, abstractmethod
from typing import final, override, TypeGuard

from core.types import (
    DamageTag,
    DamageTagMultipliers,
    Unit,
    Doll,
    FortificationLevel,
    SummonOwningAttacker,
    StatType,
    ModifierType,
    SpecialAttribute,
    DefenseIgnoreMultipliers,
    IncreasedDamageMultipliers,
    SummonedUnit,
    PhysicalSummonedUnit,
)
from core.buffs import Buff, Debuff


def _is_doll_attacker(attacker: Unit) -> TypeGuard[Doll]:
    """Returns True when attacker is a Doll."""
    return isinstance(attacker, Doll)


def _require_summon_owning_attacker(attacker: Unit) -> SummonOwningAttacker:
    """Returns attacker narrowed to a summon-owning, fortification-aware type."""
    if not isinstance(attacker, Doll):
        raise TypeError("This strategy requires a Doll attacker")

    return attacker


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

        # Compute the base damage
        effective_atk, effective_def, negative_def, term1 = self.calculate_base_damage(
            attacker, target, damage_instance
        )

        # Resolve the unit whose stats should receive/be read for combat modifiers.
        # For summon-based strategies this is the summon, not the Doll owner.
        effective_unit: Unit = self.get_effective_attacker(attacker)

        if True:  # TODO: check if have reversed assault
            bonus_increased_damage = self.resolve_reversed_assault(
                damage_instance, negative_def
            )
            effective_unit.additive_modifiers.special_attributes[
                SpecialAttribute.DAMAGE_BOOST
            ].add_to_multiplier(DamageTag.PHYSICAL, bonus_increased_damage)

        # TODO: check conditional modifiers before adding: exposed, in stability break,
        # close proximity, distance, has overburn, etc.
        damage_instance.tags.add(DamageTag.EXPOSED)
        damage_instance.tags.add(DamageTag.STABILITY_BROKEN)
        damage_instance.tags.add(DamageTag.BOSS)

        # Get the effective damage multiplier
        effective_dmg_multiplier: float = self.get_effective_multiplier(
            attacker=attacker,
            target=target,
            damage_instance=damage_instance,
            buffs_before=buffs_before,
            debuffs_before=debuffs_before,
        )

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
        crit_rate: float = effective_unit.get_basic_attribute(StatType.CRIT_RATE) / 100
        crit_dmg_multiplier: float = (
            effective_unit.get_effective_critical_damage_multiplier(
                damage_instance.tags
            )
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

    def get_effective_attacker(self, attacker: Unit) -> Unit:
        """Returns the Unit whose combat stats should be read/written in the damage template.

        For most strategies this is the attacker itself. Override in summon-based
        strategies to redirect crit stats and damage-boost writes to the summon.
        """
        return attacker

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
    def do_adjust_potency(
        self,
        attacker: Unit,
        target: Unit,
        damage_instance: DamageInstance,
        buffs_before: list[Buff] = [],
        debuffs_before: list[Debuff] = [],
    ) -> None:
        """
        Modifies damage_instance to set adjusted potencies. Not
        intended to be used in the calculate_damage template
        because it would resolve buffs twice.

        Arguments:
        attacker -- the attacking Unit
        target -- the target of the attack
        damage_instance -- describes the action
        buffs_before -- Buffs to apply to attacker before the action
        debuffs_before -- Debuffs to apply to target before the action
        """
        self.resolve_buffs(
            attacker=attacker,
            target=target,
            damage_instance=damage_instance,
            buffs_before=buffs_before,
            debuffs_before=debuffs_before,
        )

        self.calculate_adjusted_potency(
            attacker=attacker,
            target=target,
            damage_instance=damage_instance,
        )

    def calculate_adjusted_potency(
        self,
        attacker: Unit,
        target: Unit,
        damage_instance: DamageInstance,
    ) -> float:
        """
        Returns the adjusted potency for damage_instance, accounting for attacker and target.

        Arguments:
        attacker -- the attacking Unit
        target -- the target of the attack
        damage_instance -- describes the action
        buffs_before -- Buffs to apply to attacker before the action
        debuffs_before -- Debuffs to apply to target before the action
        """
        adjusted_potency: float = damage_instance.base_potency * (
            1
            + attacker.get_effective_special_attribute(
                SpecialAttribute.DAMAGE_BOOST
            ).get_total_multiplier(damage_instance.tags)
            / 100
        )

        damage_instance.adjusted_potency = adjusted_potency

        return adjusted_potency

    @final
    def get_effective_multiplier(
        self,
        attacker: Unit,
        target: Unit,
        damage_instance: DamageInstance,
        buffs_before: list[Buff] = [],
        debuffs_before: list[Debuff] = [],
    ) -> float:
        """Returns the effective multiplier of damage_instance.

        Arguments:
        attacker -- the attacking Unit
        target -- the target of the attack
        damage_instance -- describes the action
        buffs_before -- Buffs to apply to attacker before the action
        debuffs_before -- Debuffs to apply to target before the action
        """
        adjusted_potency: float = self.calculate_adjusted_potency(
            attacker=attacker,
            target=target,
            damage_instance=damage_instance,
        )

        return adjusted_potency / 100

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
    @override
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


class KulichDamageCalculationStrategy(DamageCalculationStrategy):
    """Implements the base damage for Nikketa's Kulich."""

    @final
    def _require_kulich_summon(self, attacker: Unit) -> SummonedUnit:
        owner: SummonOwningAttacker = _require_summon_owning_attacker(attacker)
        summon: SummonedUnit | None = owner.get_summoned_unit("Kulich")
        if summon is None:
            raise ValueError("Kulich summon is required for this strategy")

        return summon

    @final
    @override
    def get_effective_attacker(self, attacker: Unit) -> Unit:
        return self._require_kulich_summon(attacker)

    @final
    @override
    def resolve_buffs(
        self,
        attacker: Unit,
        target: Unit,
        damage_instance: DamageInstance,
        buffs_before: list[Buff] = [],
        debuffs_before: list[Debuff] = [],
    ) -> None:
        summon: SummonedUnit = self._require_kulich_summon(attacker)
        return super().resolve_buffs(
            summon, target, damage_instance, buffs_before, debuffs_before
        )

    @final
    @override
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

        summon: SummonedUnit = self._require_kulich_summon(attacker)

        effective_atk: float = summon.get_basic_attribute(StatType.ATTACK)
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


class LainieDamageCalculationStrategy(DamageCalculationStrategy):
    """Damage calculation strategy for Lainie, implementing her passive."""

    @final
    @override
    def calculate_base_damage(
        self, attacker: Unit, target: Unit, damage_instance: DamageInstance
    ) -> tuple[float, float, float, float]:
        return StandardDamageCalculationStrategy().calculate_base_damage(
            attacker=attacker,
            target=target,
            damage_instance=damage_instance,
        )

    @override
    def resolve_buffs(
        self,
        attacker: Unit,
        target: Unit,
        damage_instance: DamageInstance,
        buffs_before: list[Buff] = [],
        debuffs_before: list[Debuff] = [],
    ) -> None:
        """Implement Lainie's passive: Precognition Foresight. Grants critical strike chance based on initial max health."""
        super().resolve_buffs(
            attacker, target, damage_instance, buffs_before, debuffs_before
        )

        # Only expecting to run this for Lainie
        if _is_doll_attacker(attacker):
            initial_max_health: float = attacker.initial_stats.basic_attributes[
                StatType.HEALTH
            ]

            health_per_crit_chance: float = 12
            crit_chance_from_passive: float = 0

            if attacker.fortification_level >= FortificationLevel.SEGMENT03:
                health_per_crit_chance = 6
                crit_chance_from_passive = min(
                    60, initial_max_health / health_per_crit_chance * 0.1
                )
            else:
                crit_chance_from_passive = min(
                    30, initial_max_health / health_per_crit_chance * 0.1
                )

            attacker.additive_modifiers.basic_attributes[
                StatType.CRIT_RATE
            ] += crit_chance_from_passive

            # Lainie's Fixed Key 6 - OGAS's Might
            _, effective_def, _, _ = self.calculate_base_damage(
                attacker, target, damage_instance
            )

            if effective_def <= 0:
                attacker.additive_modifiers.special_attributes[
                    SpecialAttribute.CRITICAL_DAMAGE
                ].add_to_multiplier(DamageTag.ALL, 5)

    @override
    def calculate_adjusted_potency(
        self,
        attacker: Unit,
        target: Unit,
        damage_instance: DamageInstance,
    ) -> float:
        """
        Implements Lainie's passive.

        Arguments:
        attacker -- the attacking Unit
        target -- the target of the attack
        damage_instance -- describes the action
        buffs_before -- Buffs to apply to attacker before the action
        debuffs_before -- Debuffs to apply to target before the action
        """
        bonus_potency_from_passive: float = 0

        _, effective_def, _, _ = self.calculate_base_damage(
            attacker, target, damage_instance
        )

        if _is_doll_attacker(attacker) and effective_def <= 0:
            health_to_potency_conversion_rate: float = 0.1

            if attacker.fortification_level >= FortificationLevel.SEGMENT05:
                health_to_potency_conversion_rate = 0.3
            elif attacker.fortification_level >= FortificationLevel.SEGMENT03:
                health_to_potency_conversion_rate = 0.2

            bonus_potency_from_passive: float = (
                attacker.initial_stats.basic_attributes[StatType.HEALTH]
                * health_to_potency_conversion_rate
            )

        adjusted_potency: float = (
            damage_instance.base_potency + bonus_potency_from_passive
        ) * (
            1
            + attacker.get_effective_special_attribute(
                SpecialAttribute.DAMAGE_BOOST
            ).get_total_multiplier(damage_instance.tags)
            / 100
        )

        damage_instance.adjusted_potency = adjusted_potency

        return adjusted_potency


class SimulacrumDamageCalculationStrategy(DamageCalculationStrategy):
    """Damage calculation strategy for Lainie's Simulacrum, implementing her passive."""

    @final
    @override
    def get_effective_attacker(self, attacker: Unit) -> Unit:
        owner: SummonOwningAttacker = _require_summon_owning_attacker(attacker)
        summon: SummonedUnit | None = owner.get_summoned_unit("Simulacrum")
        if summon is None:
            raise ValueError("Simulacrum summon is required for this strategy")
        return summon

    @final
    @override
    def calculate_base_damage(
        self, attacker: Unit, target: Unit, damage_instance: DamageInstance
    ) -> tuple[float, float, float, float]:
        owner: SummonOwningAttacker = _require_summon_owning_attacker(attacker)
        summon: SummonedUnit | None = owner.get_summoned_unit("Simulacrum")
        if summon is None:
            raise ValueError("Simulacrum summon is required for this strategy")

        return StandardDamageCalculationStrategy().calculate_base_damage(
            attacker=summon,
            target=target,
            damage_instance=damage_instance,
        )

    @override
    def resolve_buffs(
        self,
        attacker: Unit,
        target: Unit,
        damage_instance: DamageInstance,
        buffs_before: list[Buff] = [],
        debuffs_before: list[Debuff] = [],
    ) -> None:
        """Implement Lainie's Simulacrum's passive: Precognition Perception. Grants critical strike chance based on initial max health."""
        owner: SummonOwningAttacker = _require_summon_owning_attacker(attacker)
        summon: SummonedUnit | None = owner.get_summoned_unit("Simulacrum")
        if summon is None:
            raise ValueError("Simulacrum summon is required for this strategy")

        super().resolve_buffs(
            summon, target, damage_instance, buffs_before, debuffs_before
        )

        # Only expecting to run this for Lainie's Simulacrum
        if isinstance(summon, PhysicalSummonedUnit):
            initial_max_health: float = summon.initial_stats.basic_attributes[
                StatType.HEALTH
            ]

            health_per_crit_chance: float = 12
            crit_chance_from_passive: float = 0

            if owner.fortification_level >= FortificationLevel.SEGMENT03:
                health_per_crit_chance = 6
                crit_chance_from_passive = min(
                    60, initial_max_health / health_per_crit_chance * 0.1
                )
            else:
                crit_chance_from_passive = min(
                    30, initial_max_health / health_per_crit_chance * 0.1
                )

            summon.additive_modifiers.basic_attributes[
                StatType.CRIT_RATE
            ] += crit_chance_from_passive

            # Lainie's Fixed Key 6 - OGAS's Might
            _, effective_def, _, _ = self.calculate_base_damage(
                attacker, target, damage_instance
            )

            if effective_def <= 0:
                summon.additive_modifiers.special_attributes[
                    SpecialAttribute.CRITICAL_DAMAGE
                ].add_to_multiplier(DamageTag.ALL, 5)

    @override
    def calculate_adjusted_potency(
        self,
        attacker: Unit,
        target: Unit,
        damage_instance: DamageInstance,
    ) -> float:
        """
        Implements Lainie's Simulacrum's passive.

        Arguments:
        attacker -- the attacking Unit
        target -- the target of the attack
        damage_instance -- describes the action
        buffs_before -- Buffs to apply to attacker before the action
        debuffs_before -- Debuffs to apply to target before the action
        """
        bonus_potency_from_passive: float = 0
        owner: SummonOwningAttacker = _require_summon_owning_attacker(attacker)
        summon: SummonedUnit | None = owner.get_summoned_unit("Simulacrum")
        if summon is None:
            raise ValueError("Simulacrum summon is required for this strategy")

        _, effective_def, _, _ = self.calculate_base_damage(
            attacker, target, damage_instance
        )

        if isinstance(summon, PhysicalSummonedUnit) and effective_def <= 0:
            health_to_potency_conversion_rate: float = 0.1

            if owner.fortification_level >= FortificationLevel.SEGMENT05:
                health_to_potency_conversion_rate = 0.3
            elif owner.fortification_level >= FortificationLevel.SEGMENT03:
                health_to_potency_conversion_rate = 0.2

            bonus_potency_from_passive: float = (
                summon.initial_stats.basic_attributes[StatType.HEALTH]
                * health_to_potency_conversion_rate
            )

        adjusted_potency: float = (
            damage_instance.base_potency + bonus_potency_from_passive
        ) * (
            1
            + summon.get_effective_special_attribute(
                SpecialAttribute.DAMAGE_BOOST
            ).get_total_multiplier(damage_instance.tags)
            / 100
        )

        damage_instance.adjusted_potency = adjusted_potency

        return adjusted_potency


class DamageInstance(BaseModel):
    """An instance of damage."""

    model_config = {"arbitrary_types_allowed": True}

    label: str
    base_potency: float
    tags: set[DamageTag] = Field(default_factory=set)
    adjusted_potency: float = 0
    group_name: str = ""
    buffs_before: list[Buff] = Field(default_factory=list)
    debuffs_before: list[Debuff] = Field(default_factory=list)
    damage_calculation_strategy: DamageCalculationStrategy = Field(
        default_factory=StandardDamageCalculationStrategy
    )


class CombatAction(ABC, BaseModel):
    """Represents an action in combat (i.e., skill usage or event)."""

    @abstractmethod
    def execute(self, *args, **kwargs) -> DamageInstance:
        """Use/execute this action."""
        pass


class CombatSummary(BaseModel):
    """Summarizes the result of a combat action."""

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
        label="Combined",
        base_potency=combined_base_potency,
        tags={tag},
        adjusted_potency=combined_adjusted_potency,
    )
