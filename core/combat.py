from __future__ import annotations

from pydantic import BaseModel, Field
from abc import ABC, abstractmethod
from typing import final, override, TypeGuard

from core.types import (
    DamageTag,
    DamageTagMultipliers,
    Unit,
    UnitLevel,
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


def _calculate_effective_and_negative_defense(
    attacker: Unit,
    target: Unit,
    damage_instance: DamageInstance,
    include_conditional_defense_modifiers: bool = True,
) -> tuple[float, float]:
    """Returns effective defense after ignore/defense-down and any overflow past zero defense."""
    total_defense_ignore_multipliers: DefenseIgnoreMultipliers = (
        attacker.initial_stats.special_attributes[SpecialAttribute.DEFENSE_IGNORE]
        + attacker.additive_modifiers.special_attributes[
            SpecialAttribute.DEFENSE_IGNORE
        ]
    )

    effective_def: float = (
        target.initial_stats.basic_attributes[StatType.DEFENSE]
        + target.additive_modifiers.basic_attributes[StatType.DEFENSE]
    )

    ignore_def: float = (
        total_defense_ignore_multipliers.get_total_multiplier(damage_instance.tags)
        - target.multiplicative_modifiers.basic_attributes[StatType.DEFENSE]
    )

    if include_conditional_defense_modifiers:
        ignore_def -= target.multiplicative_modifiers.conditional_basic_attributes[
            StatType.DEFENSE
        ].get_total_multiplier(damage_instance.tags)

    negative_def: float = max(0, ignore_def - 100)
    effective_def = max(0, effective_def * (1 - ignore_def / 100))

    return effective_def, negative_def


def resolve_reversed_assault(
    damage_instance: DamageInstance, negative_def: float
) -> float:
    """Returns the increased damage bonus as a result of the Reversed Assault buff."""
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

        bonus_increased_damage = negative_def * bonus_damage_per_negative_def

    return bonus_increased_damage


class DamageCalculationStrategy(ABC):
    """Strategy pattern for damage calculation. This allows for different versions of the damage formula to be used"""

    def calculate_damage(
        self,
        attacker: Unit,
        target: Unit,
        damage_instance: DamageInstance,
        target_combat_state: TargetCombatState | None = None,
        buffs_before: list[Buff] = [],
        debuffs_before: list[Debuff] = [],
    ) -> CombatSummary:
        """Returns a summary of the combat action.

        Arguments:
        attacker -- the attacking Unit
        target -- the target of the attack
        damage_instance -- describes the action
        target_combat_state -- encapsulated target combat state used for damage calculations
        buffs_before -- Buffs to apply to attacker before the action
        debuffs_before -- Debuffs to apply to target before the action
        """
        state: TargetCombatState = target_combat_state or TargetCombatState()

        # Ensure assumed target-state tags are available to all downstream math,
        # including attack/crit-rate and defense-ignore calculations.
        self.apply_assumed_target_state_tags(damage_instance, state)

        is_fixed_damage: bool = DamageTag.FIXED in damage_instance.tags

        # Apply buffs and debuffs before
        self.resolve_buffs(
            attacker, target, damage_instance, buffs_before, debuffs_before
        )

        # Compute the base damage
        effective_atk, effective_def, negative_def, term1 = self.calculate_base_damage(
            attacker, target, damage_instance
        )

        if is_fixed_damage:
            # For fixed damage, defense is treated as zero.
            effective_def = 0
            negative_def = 0
            term1 = effective_atk

        # Resolve the unit whose stats should receive/be read for combat modifiers.
        # For summon-based strategies this is the summon, not the Doll owner.
        effective_unit: Unit = self.get_effective_attacker(attacker)

        if True:  # TODO: check if have reversed assault
            bonus_increased_damage = resolve_reversed_assault(
                damage_instance, negative_def
            )
            effective_unit.additive_modifiers.special_attributes[
                SpecialAttribute.DAMAGE_BOOST
            ].add_to_multiplier(DamageTag.PHYSICAL, bonus_increased_damage)

        # Get the effective damage multiplier
        effective_dmg_multiplier: float = self.get_effective_multiplier(
            attacker=attacker,
            target=target,
            damage_instance=damage_instance,
            buffs_before=buffs_before,
            debuffs_before=debuffs_before,
        )

        # Resolve "increased damage taken" effects (disregard for fixed damage)
        increased_damage_taken: float = (
            0
            if is_fixed_damage
            else self.resolve_increased_damage_taken(target, damage_instance)
        )

        bonus_damage: float = self.get_bonus_damage(attacker, target, damage_instance)

        non_critical_damage: float = (
            effective_dmg_multiplier * term1 + bonus_damage
        ) * (1 + increased_damage_taken / 100)

        # Apply stability damage reduction (disregard for fixed damage)
        if not state.is_stability_broken and not is_fixed_damage:
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

        if not is_fixed_damage:
            non_critical_damage = non_critical_damage * (
                1
                + MORE_DAMAGE_PER_WEAKNESS_EXPLOITED
                * min(
                    state.phase_weaknesses_exploited,
                    MAX_PHASE_WEAKNESSES_EXPLOITABLE,
                )
            )

        # Account for critical hit
        (
            crit_rate,
            crit_dmg_multiplier,
            critical_damage,
            expected_damage,
        ) = self.calculate_crit_and_expected_damage(
            effective_unit, damage_instance, non_critical_damage
        )

        combat_summary: CombatSummary = CombatSummary(
            non_critical_damage=non_critical_damage,
            critical_damage=critical_damage,
            expected_damage=expected_damage,
            effective_damage_multiplier=effective_dmg_multiplier,
            critical_rate=crit_rate,
            effective_critical_damage_multiplier=crit_dmg_multiplier,
            effective_attack=effective_atk,
            effective_defense=effective_def,
            negative_defense=negative_def,
        )

        return combat_summary

    @final
    def apply_assumed_target_state_tags(
        self,
        damage_instance: DamageInstance,
        target_combat_state: TargetCombatState | None = None,
    ) -> None:
        """Adds target-state tags for conditional calculations using combat state and defaults."""
        state: TargetCombatState = target_combat_state or TargetCombatState()

        if DamageTag.FIXED in damage_instance.tags:
            # Fixed damage should not be affected by any conditional modifiers,
            # so we add a tag to short-circuit all conditional calculations downstream.
            damage_instance.tags = set([DamageTag.FIXED])
        else:
            damage_instance.tags.add(DamageTag.ALL)

            # Preserve current baseline assumptions for legacy behavior.
            damage_instance.tags.add(DamageTag.EXPOSED)
            damage_instance.tags.add(DamageTag.HAS_MOVEMENT_DEBUFF)
            damage_instance.tags.add(DamageTag.ONLY_HIT_ONE_TARGET)
            damage_instance.tags.add(DamageTag.NEAR)
            damage_instance.tags.add(DamageTag.FAR)

            if state.is_stability_broken:
                damage_instance.tags.add(DamageTag.STABILITY_BROKEN)

            if state.unit_level == UnitLevel.BOSS:
                damage_instance.tags.add(DamageTag.BOSS)

            if state.is_on_phase_tile or state.phase_tile_ascension_level > 0:
                damage_instance.tags.add(DamageTag.ON_PHASE_TILE)

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
                    if buff.tag == DamageTag.ALL:
                        attacker.additive_modifiers.basic_attributes[
                            buff.stat_type
                        ] += buff.value
                    else:
                        attacker.additive_modifiers.conditional_basic_attributes[
                            buff.stat_type
                        ].add_to_multiplier(buff.tag, buff.value)
                elif buff.modifier_type == ModifierType.MULTIPLICATIVE:
                    if buff.tag == DamageTag.ALL:
                        attacker.multiplicative_modifiers.basic_attributes[
                            buff.stat_type
                        ] += buff.value
                    else:
                        attacker.multiplicative_modifiers.conditional_basic_attributes[
                            buff.stat_type
                        ].add_to_multiplier(buff.tag, buff.value)
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
                    if debuff.tag == DamageTag.ALL:
                        target.additive_modifiers.basic_attributes[
                            debuff.stat_type
                        ] += debuff.value
                    else:
                        target.additive_modifiers.conditional_basic_attributes[
                            debuff.stat_type
                        ].add_to_multiplier(debuff.tag, debuff.value)
                elif debuff.modifier_type == ModifierType.MULTIPLICATIVE:
                    if debuff.tag == DamageTag.ALL:
                        target.multiplicative_modifiers.basic_attributes[
                            debuff.stat_type
                        ] += debuff.value
                    else:
                        target.multiplicative_modifiers.conditional_basic_attributes[
                            debuff.stat_type
                        ].add_to_multiplier(debuff.tag, debuff.value)
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

    def get_bonus_damage(
        self, attacker: Unit, target: Unit, damage_instance: DamageInstance
    ) -> float:
        """Returns the bonus damage that isn't multiplicative with Attack (i.e., doesn't fit in the "potency" framework).
        This will still be multiplied alongside the effective damage multiplier and increased damage taken, but is added
        after the base damage calculation rather than being a part of the base potency.
        """
        return 0

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
        # Ensure assumed target-state tags are accounted for.
        self.apply_assumed_target_state_tags(damage_instance)

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
        For fixed damage, returns base potency without damage boost modifiers.

        Arguments:
        attacker -- the attacking Unit
        target -- the target of the attack
        damage_instance -- describes the action
        buffs_before -- Buffs to apply to attacker before the action
        debuffs_before -- Debuffs to apply to target before the action
        """
        is_fixed_damage: bool = DamageTag.FIXED in damage_instance.tags

        if is_fixed_damage:
            # Fixed damage does not benefit from damage boost modifiers
            adjusted_potency: float = damage_instance.base_potency
        else:
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
    def calculate_crit_and_expected_damage(
        self,
        effective_unit: Unit,
        damage_instance: DamageInstance,
        non_critical_damage: float,
    ) -> tuple[
        float,
        float,
        float,
        float,
    ]:
        """Returns crit_rate, crit_dmg_multiplier, critical_damage, and expected_damage.

        Arguments:
        effective_unit -- the Unit whose stats should be read for crit calculations (attacker for most strategies,
        but may be the summon for summon-based strategies)
        damage_instance -- describes the action
        non_critical_damage -- the damage dealt if the attack does not crit
        """
        crit_rate: float = (
            effective_unit.get_basic_attribute(StatType.CRIT_RATE, damage_instance.tags)
            / 100
        )

        crit_dmg_multiplier: float = (
            effective_unit.get_effective_critical_damage_multiplier(
                damage_instance.tags
            )
            / 100
        )

        if DamageTag.FIXED in damage_instance.tags:
            # Fixed damage should not be affected by critical hits, so we set the crit multiplier to 1 to neutralize crits.
            crit_rate: float = 0
            crit_dmg_multiplier = 1
            critical_damage: float = non_critical_damage
            effective_crit_rate: float = 0
            expected_damage: float = non_critical_damage
        else:
            critical_damage: float = crit_dmg_multiplier * non_critical_damage

            effective_crit_rate: float = min(1.0, crit_rate)

            expected_damage: float = (
                effective_crit_rate * critical_damage
                + (1 - effective_crit_rate) * non_critical_damage
            )

        return (
            crit_rate,
            crit_dmg_multiplier,
            critical_damage,
            expected_damage,
        )

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
        effective_atk: float = attacker.get_basic_attribute(
            StatType.ATTACK, damage_instance.tags
        )
        effective_def, negative_def = _calculate_effective_and_negative_defense(
            attacker=attacker,
            target=target,
            damage_instance=damage_instance,
        )

        return (
            effective_atk,
            effective_def,
            negative_def,
            effective_atk / (1 + effective_def / effective_atk),
        )


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
    critical_rate: float = 0
    effective_critical_damage_multiplier: float = 0
    effective_attack: float = 0
    effective_defense: float = 0
    negative_defense: float = 0


class TargetCombatState(BaseModel):
    """Represents target-side combat state used during damage calculation."""

    is_stability_broken: bool = True
    phase_weaknesses_exploited: int = 0
    unit_level: UnitLevel = UnitLevel.BOSS
    is_on_phase_tile: bool = False
    phase_tile_ascension_level: int = Field(default=0, ge=0, le=3)


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


class FixedDamageInstance(DamageInstance):
    """A DamageInstance that represents fixed damage, which only scales with the source's Attack and does not critically hit."""

    label: str = "Fixed Damage"
    tags: set[DamageTag] = Field(default_factory=lambda: {DamageTag.FIXED})
    group_name: str = "Fixed Damage"
    damage_calculation_strategy: DamageCalculationStrategy = Field(
        default_factory=StandardDamageCalculationStrategy
    )


class Overburn(CombatAction):
    """Represents the fixed damage from Overburn (10% of applier's Attack)."""

    def execute(self) -> DamageInstance:
        base_potency: float = 10
        return FixedDamageInstance(
            label="Overburn",
            base_potency=base_potency,
            adjusted_potency=base_potency,
            group_name="Overburn",
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
        summon: SummonedUnit = self._require_kulich_summon(attacker)

        effective_atk: float = summon.get_basic_attribute(
            StatType.ATTACK, damage_instance.tags
        )
        effective_def, negative_def = _calculate_effective_and_negative_defense(
            attacker=attacker,
            target=target,
            damage_instance=damage_instance,
            include_conditional_defense_modifiers=False,
        )

        return (
            effective_atk,
            effective_def,
            negative_def,
            effective_atk / (1 + effective_def / effective_atk),
        )


class LainieBonusDamageCalculations:
    """Contains bonus damage calculations for Lainie that don't fit in the base damage calculation strategy framework,
    particularly her % of Initial Health added as "damage multiplier."
    """

    @staticmethod
    def get_health_conversion_rate(fortification_level: FortificationLevel) -> float:
        """Returns the health-to-damage conversion rate based on Lainie's fortification level."""
        if fortification_level >= FortificationLevel.SEGMENT05:
            return 0.3
        elif fortification_level >= FortificationLevel.SEGMENT03:
            return 0.2
        return 0.1

    @staticmethod
    def get_bonus_damage_from_unit(
        unit: Unit,
        fortification_level: FortificationLevel,
        target: Unit,
        damage_instance: DamageInstance,
    ) -> float:
        """Returns Lainie-style health-conversion bonus damage for the provided unit."""
        initial_max_health: float = unit.initial_stats.basic_attributes[StatType.HEALTH]
        health_conversion_rate: float = (
            LainieBonusDamageCalculations.get_health_conversion_rate(
                fortification_level
            )
        )

        bias: float = 0

        if True:  # TODO: check if have reversed assault
            _, negative_def = _calculate_effective_and_negative_defense(
                attacker=unit,
                target=target,
                damage_instance=damage_instance,
            )

            reversed_assault_bonus: float = (
                resolve_reversed_assault(damage_instance, negative_def) / 100
            )

            # Reversed Assault bonus should've been added already, no need to apply it again here. Just need to check if it was applied and if so, apply the same bonus to the health conversion.
            if reversed_assault_bonus >= 0.9:  # Empirically derived from test data
                bias = 350

        health_contribution_base: float = (
            initial_max_health * health_conversion_rate + bias
        )

        health_contribution: float = health_contribution_base * (
            1
            + unit.get_effective_special_attribute(
                SpecialAttribute.DAMAGE_BOOST
            ).get_total_multiplier(damage_instance.tags)
            / 100
        )

        return health_contribution


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
    def get_bonus_damage(
        self, attacker: Unit, target: Unit, damage_instance: DamageInstance
    ) -> float:
        """Implement Lainie's % of Initial Health added as "damage multiplier" bonus damage."""
        if not _is_doll_attacker(attacker):
            raise TypeError(
                "Attacker must be a Doll for Lainie bonus damage calculations"
            )

        return LainieBonusDamageCalculations.get_bonus_damage_from_unit(
            unit=attacker,
            fortification_level=attacker.fortification_level,
            target=target,
            damage_instance=damage_instance,
        )


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
    def get_bonus_damage(
        self, attacker: Unit, target: Unit, damage_instance: DamageInstance
    ) -> float:
        """Implement Lainie's Simulacrum's % of Initial Health added as "damage multiplier" bonus damage."""
        owner: SummonOwningAttacker = _require_summon_owning_attacker(attacker)
        summon: SummonedUnit | None = owner.get_summoned_unit("Simulacrum")
        if summon is None:
            raise ValueError("Simulacrum summon is required for this strategy")

        return LainieBonusDamageCalculations.get_bonus_damage_from_unit(
            unit=summon,
            fortification_level=owner.fortification_level,
            target=target,
            damage_instance=damage_instance,
        )


class YooheeDamageCalculationStrategy(StandardDamageCalculationStrategy):
    """Damage calculation strategy for Yoohee, implementing her V6 passive."""

    @override
    def resolve_buffs(
        self,
        attacker: Unit,
        target: Unit,
        damage_instance: DamageInstance,
        buffs_before: list[Buff] = [],
        debuffs_before: list[Debuff] = [],
    ) -> None:
        """Implement Yoohee's V6 passive: Main Dancer's Aura."""

        # Only expecting to run this for Yoohee (V6)
        if _is_doll_attacker(attacker) and (
            attacker.fortification_level >= FortificationLevel.SEGMENT06
        ):
            # Effect of Dance Steps on Yoohee doubled (Crit Damage +10%, get the other 10% from applying the buff)
            attacker.initial_stats.special_attributes[
                SpecialAttribute.CRITICAL_DAMAGE
            ].add_to_multiplier(DamageTag.ALL, 10)

            # Each buff applied to other allied units increases Yoohee's attack by 1.5%, to a maximum increase of 45%
            # Assume 30 buffs for max bonus, and that all buffs on allies are applied to Yoohee for simplicity
            attacker.multiplicative_modifiers.basic_attributes[StatType.ATTACK] += 45

        super().resolve_buffs(
            attacker, target, damage_instance, buffs_before, debuffs_before
        )


class QiuhuaDamageCalculationStrategy(StandardDamageCalculationStrategy):
    """Damage calculation strategy for Qiuhua, implementing her V2 passive."""

    @override
    def resolve_buffs(
        self,
        attacker: Unit,
        target: Unit,
        damage_instance: DamageInstance,
        buffs_before: list[Buff] = [],
        debuffs_before: list[Debuff] = [],
    ) -> None:
        """Implement Qiuhua's V2 and V3 passive: Zao Jun's Rule"""
        super().resolve_buffs(
            attacker, target, damage_instance, buffs_before, debuffs_before
        )

        # Only expecting to run this for Qiuhua (V2)
        if _is_doll_attacker(attacker) and (
            attacker.fortification_level >= FortificationLevel.SEGMENT02
        ):
            # When dealing damage, if critical rate of this attack exceeds 100%, every 1% of overflow
            # critical rate is converted to 1% critical damage.
            overflow_crit_rate: float = (
                attacker.get_basic_attribute(StatType.CRIT_RATE, damage_instance.tags)
                - 100
            )

            if overflow_crit_rate > 0:
                bonus_crit_dmg_multiplier: float = overflow_crit_rate
                attacker.additive_modifiers.special_attributes[
                    SpecialAttribute.CRITICAL_DAMAGE
                ].add_to_multiplier(DamageTag.ALL, bonus_crit_dmg_multiplier)

        # Only expecting to run this for Qiuhua (V3)
        if _is_doll_attacker(attacker) and (
            attacker.fortification_level >= FortificationLevel.SEGMENT03
        ):
            # A new effect is added when dealing Burn damage to enemy targets with Scorch Mark:
            # if the target holds more than 10 stacks of Scorch Mark, for each excess stack
            # Qiuhua's attack is increased by 1%.
            # TODO: Would inspect target's debuffs to see if this applies, but for now just assume 30 excess stacks
            excess_scorch_stacks: int = 30
            attack_boost_per_excess_stack: float = 1
            attacker.multiplicative_modifiers.conditional_basic_attributes[
                StatType.ATTACK
            ].add_to_multiplier(
                DamageTag.BURN, excess_scorch_stacks * attack_boost_per_excess_stack
            )


class FayeDamageCalculationStrategy(StandardDamageCalculationStrategy):
    """Damage calculation strategy for Faye, implementing her passive and Expansion Key."""

    @override
    def resolve_buffs(
        self,
        attacker: Unit,
        target: Unit,
        damage_instance: DamageInstance,
        buffs_before: list[Buff] = [],
        debuffs_before: list[Debuff] = [],
    ) -> None:
        """Apply Faye's passive defense-ignore effects and Expansion Key assumptions."""
        super().resolve_buffs(
            attacker, target, damage_instance, buffs_before, debuffs_before
        )

        # Only expecting to run this for Faye
        if _is_doll_attacker(attacker):
            # Expansion Key - Unstoppable Fighting Spirit: When dealing damage to an enemy with Gash,
            # ignore 50% of the target's defense and increase attack by 15%.
            # TODO: Would inspect target's debuffs to see if this applies, but for now just assume target has Gash
            target_has_gash: bool = True

            if target_has_gash:
                attacker.multiplicative_modifiers.basic_attributes[
                    StatType.ATTACK
                ] += 15
                attacker.additive_modifiers.special_attributes[
                    SpecialAttribute.DEFENSE_IGNORE
                ].add_to_multiplier(DamageTag.ALL, 50)

            # When attacking, Faye ignores an amount of the target's defense equal to (2%x number of Rend stacks)
            # TODO: Would inspect target's debuffs to see how many Rend stacks they have, but for now just assume 8 stacks for 16% defense ignore
            rend_stacks: int = 8

            if attacker.fortification_level >= FortificationLevel.SEGMENT01:
                defense_ignore_per_rend_stack: float = 4
            else:
                defense_ignore_per_rend_stack: float = 2

            attacker.additive_modifiers.special_attributes[
                SpecialAttribute.DEFENSE_IGNORE
            ].add_to_multiplier(
                DamageTag.ALL, rend_stacks * defense_ignore_per_rend_stack
            )


class KlukaiDamageCalculationStrategy(StandardDamageCalculationStrategy):
    """Damage calculation strategy for Klukai, implementing her Toxic Infiltration effect."""

    @override
    def resolve_buffs(
        self,
        attacker: Unit,
        target: Unit,
        damage_instance: DamageInstance,
        buffs_before: list[Buff] = [],
        debuffs_before: list[Debuff] = [],
    ) -> None:
        """Apply effect of Toxic Infiltration."""
        super().resolve_buffs(
            attacker, target, damage_instance, buffs_before, debuffs_before
        )

        # Only expecting to run this for Klukai
        if _is_doll_attacker(attacker):
            # TODO: Would inspect target's debuffs to see if this applies, but for now just assume target has Toxic Infiltration
            target_has_toxic_infiltration: bool = True

            if attacker.fortification_level >= FortificationLevel.SEGMENT05:
                # When receiving an active attack from Klukai, damage taken is increased by 30%.
                attacker.additive_modifiers.special_attributes[
                    SpecialAttribute.DAMAGE_BOOST
                ].add_to_multiplier(DamageTag.ACTIVE, 30)


class LindDamageCalculationStrategy(StandardDamageCalculationStrategy):
    """Damage calculation strategy for Lind, implementing her effects such as Ketoacidemia."""

    @override
    def resolve_buffs(
        self,
        attacker: Unit,
        target: Unit,
        damage_instance: DamageInstance,
        buffs_before: list[Buff] = [],
        debuffs_before: list[Debuff] = [],
    ) -> None:
        """Apply effect of Lind's abilities."""
        super().resolve_buffs(
            attacker, target, damage_instance, buffs_before, debuffs_before
        )

        # Only expecting to run this for Lind
        if _is_doll_attacker(attacker):
            # TODO: Would inspect target's debuffs to see if this applies, but for now just assume target has Ketoacidemia
            target_has_ketoacidemia: bool = True
            number_of_debuffs_on_target: int = (
                6  # Assume max number of debuffs for maximum bonus
            )
            max_debuffs_for_bonus: int = 6

            if attacker.fortification_level >= FortificationLevel.SEGMENT02:
                damage_boost_per_debuff: float = 12
            else:
                damage_boost_per_debuff: float = 5

            attacker.additive_modifiers.special_attributes[
                SpecialAttribute.DAMAGE_BOOST
            ].add_to_multiplier(
                DamageTag.CORROSION,
                min(number_of_debuffs_on_target, max_debuffs_for_bonus)
                * damage_boost_per_debuff,
            )


class HealthScalingDamageCalculationStrategy(DamageCalculationStrategy):
    """Implements the damage formula where base damage is a function of health, attack, and defense."""

    health_scalar: float = Field(default=0.2)  # 20%

    def __init__(self, health_scalar: float = 0.2):
        """
        Arguments:
        health_scalar -- the fraction of current Health to use as the surrogate Attack stat in the damage formula
        """
        self.health_scalar = health_scalar

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
        effective_atk: float = attacker.get_basic_attribute(
            StatType.ATTACK, damage_instance.tags
        )

        effective_health: float = (
            attacker.get_basic_attribute(StatType.HEALTH, damage_instance.tags)
            * self.health_scalar
        )

        effective_def, negative_def = _calculate_effective_and_negative_defense(
            attacker=attacker,
            target=target,
            damage_instance=damage_instance,
        )

        # For "Term 1" (base damage), use \frac{Health}{1 + \frac{Defense}{Attack}} instead of
        # \frac{Attack}{1 + \frac{Defense}{Attack}}
        # Note the Attack/Defense term in the denominator is unchanged from the standard formula.

        return (
            effective_health,
            effective_def,
            negative_def,
            effective_health / (1 + effective_def / effective_atk),
        )


class UllridDamageCalculationStrategy(StandardDamageCalculationStrategy):
    """Damage calculation strategy for Ullrid, implementing her passive effects, in particular Hunter's Talent upgraded
    with Expansion Key - Determined Pursuit Tier 2."""

    @override
    def resolve_buffs(
        self,
        attacker: Unit,
        target: Unit,
        damage_instance: DamageInstance,
        buffs_before: list[Buff] = [],
        debuffs_before: list[Debuff] = [],
    ) -> None:
        """Apply effect of Ullrid's abilities."""
        super().resolve_buffs(
            attacker, target, damage_instance, buffs_before, debuffs_before
        )

        # Only expecting to run this for Ullrid
        if _is_doll_attacker(attacker):
            # TODO: This effect is tied to having Hunter's Talent, which is effectively all the time because
            # it's gained after every active attack, even when being consumed for Hidden Pursuit. For simplicity, just assume this is always active.
            has_hunters_talent: bool = True

            if has_hunters_talent:
                # If Ullrid's critical rate is greater than 100%, for every 1% of critical rate overflow, her critical damage is increased
                # by 0.3%.
                critical_damage_per_overflow_crit_rate: float = 0.3
                overflow_crit_rate: float = (
                    attacker.get_basic_attribute(
                        StatType.CRIT_RATE, damage_instance.tags
                    )
                    - 100
                )

                attacker.additive_modifiers.special_attributes[
                    SpecialAttribute.CRITICAL_DAMAGE
                ].add_to_multiplier(
                    DamageTag.ALL,
                    max(0, overflow_crit_rate * critical_damage_per_overflow_crit_rate),
                )

                # All allied units' melee damage is increased by 10%.
                attacker.additive_modifiers.special_attributes[
                    SpecialAttribute.DAMAGE_BOOST
                ].add_to_multiplier(
                    DamageTag.MELEE,
                    10,
                )

            # Optical Camouflage passive V5+: Before attacking, if this unit has moved 2 tiles or more, increase
            # attack by 20%. This is an easy condition to satisfy at V5+ because of the additional opportunities
            # to move during Ullrid's combos, so let's just assume this is always active for simplicity.
            if attacker.fortification_level >= FortificationLevel.SEGMENT05:
                attacker.multiplicative_modifiers.basic_attributes[
                    StatType.ATTACK
                ] += 20


class BelkaDamageCalculationStrategy(StandardDamageCalculationStrategy):
    """Damage calculation strategy for Belka, implementing her passive effects, in particular the effects related to Negative Charge application."""

    @override
    def resolve_buffs(
        self,
        attacker: Unit,
        target: Unit,
        damage_instance: DamageInstance,
        buffs_before: list[Buff] = [],
        debuffs_before: list[Debuff] = [],
    ) -> None:
        """Apply effect of Belka's abilities."""
        super().resolve_buffs(
            attacker, target, damage_instance, buffs_before, debuffs_before
        )

        # Only expecting to run this for Belka
        if _is_doll_attacker(attacker):
            # TODO: Need to keep track of Negative Charge application and if the target has Negative Charge.
            # For now, assume the maximum bonus for having applied 6 stacks of Negative Charge and the target having Negative Charge is always active.
            negative_charge_stacks_applied: int = 6
            critical_rate_per_negative_charge_stack: float = 5
            max_crit_rate_from_negative_charge: float = 30
            target_has_negative_charge: bool = True

            if negative_charge_stacks_applied > 0:
                attacker.additive_modifiers.basic_attributes[StatType.CRIT_RATE] += min(
                    negative_charge_stacks_applied
                    * critical_rate_per_negative_charge_stack,
                    max_crit_rate_from_negative_charge,
                )

            # V3: If the target has Negative Charge, ignores 10% of its defense.
            if (
                attacker.fortification_level >= FortificationLevel.SEGMENT03
                and target_has_negative_charge
            ):
                attacker.additive_modifiers.special_attributes[
                    SpecialAttribute.DEFENSE_IGNORE
                ].add_to_multiplier(DamageTag.ALL, 10)


class HelenDamageCalculationStrategy(StandardDamageCalculationStrategy):
    """Damage calculation strategy for Helen, implementing her passive effects, in particular the effects related to Defense conversion to Attack."""

    @override
    def resolve_buffs(
        self,
        attacker: Unit,
        target: Unit,
        damage_instance: DamageInstance,
        buffs_before: list[Buff] = [],
        debuffs_before: list[Debuff] = [],
    ) -> None:
        """Apply effect of Helen's abilities."""
        super().resolve_buffs(
            attacker, target, damage_instance, buffs_before, debuffs_before
        )

        # Only expecting to run this for Helen
        if _is_doll_attacker(attacker):
            # At the start of battle, increase defense and maximum HP by 30%.
            attacker.multiplicative_modifiers.basic_attributes[StatType.DEFENSE] += 30
            attacker.multiplicative_modifiers.basic_attributes[StatType.HEALTH] += 30

            # Before performing a basic attack, Helen gains attack equal to x% of her defense. Helena only performs basic attacks.
            defense_to_attack_conversion_rate: float = 0.15

            if attacker.fortification_level >= FortificationLevel.SEGMENT06:
                defense_to_attack_conversion_rate = 0.70
            elif attacker.fortification_level >= FortificationLevel.SEGMENT02:
                defense_to_attack_conversion_rate = 0.30

            # Conditional Defense modifiers should not be included in this calculation since the conversion is based on Helen's defense
            # outside the context of receiving damage.
            attack_from_defense_conversion: float = (
                attacker.get_basic_attribute(StatType.DEFENSE, set([DamageTag.ALL]))
                * defense_to_attack_conversion_rate
            )

            attacker.additive_modifiers.basic_attributes[
                StatType.ATTACK
            ] += attack_from_defense_conversion


class LiushihDamageCalculationStrategy(DamageCalculationStrategy):
    """Damage calculation strategy for Lainie, implementing her passive."""

    @final
    @override
    def calculate_base_damage(
        self, attacker: Unit, target: Unit, damage_instance: DamageInstance
    ) -> tuple[float, float, float, float]:
        loaded_attack_health_ratio: float = 0.20
        return HealthScalingDamageCalculationStrategy(
            loaded_attack_health_ratio
        ).calculate_base_damage(
            attacker=attacker,
            target=target,
            damage_instance=damage_instance,
        )

    @override
    def calculate_adjusted_potency(
        self,
        attacker: Unit,
        target: Unit,
        damage_instance: DamageInstance,
    ) -> float:
        """
        Returns the adjusted potency for damage_instance, accounting for attacker and target.
        For fixed damage, returns base potency without damage boost modifiers.

        Arguments:
        attacker -- the attacking Unit
        target -- the target of the attack
        damage_instance -- describes the action
        buffs_before -- Buffs to apply to attacker before the action
        debuffs_before -- Debuffs to apply to target before the action
        """
        is_fixed_damage: bool = DamageTag.FIXED in damage_instance.tags

        if is_fixed_damage:
            # Fixed damage does not benefit from damage boost modifiers
            adjusted_potency: float = damage_instance.base_potency
        elif DamageTag.BASIC in damage_instance.tags:
            # Liushih Passive - We Fight As One:
            # For every 60 points of Liushih's initial attack, increase the basic attack damage multiplier of both herself
            # and Pegasus by 5%, up to a maximum of 50%.

            # Modify the base potency directly
            maximum_bonus_from_passive: float = 50
            attack_per_5_percent_bonus: float = 60
            bonus_potency_from_passive: float = min(
                (
                    attacker.initial_stats.basic_attributes[StatType.ATTACK]
                    // attack_per_5_percent_bonus
                )
                * 5,
                maximum_bonus_from_passive,
            )

            damage_instance.base_potency += bonus_potency_from_passive

        adjusted_potency: float = damage_instance.base_potency * (
            1
            + attacker.get_effective_special_attribute(
                SpecialAttribute.DAMAGE_BOOST
            ).get_total_multiplier(damage_instance.tags)
            / 100
        )

        damage_instance.adjusted_potency = adjusted_potency

        return adjusted_potency


class PegasusDamageCalculationStrategy(DamageCalculationStrategy):
    """Implements the base damage for Liushih's Pegasus."""

    @final
    def _require_pegasus_summon(self, attacker: Unit) -> SummonedUnit:
        owner: SummonOwningAttacker = _require_summon_owning_attacker(attacker)
        summon: SummonedUnit | None = owner.get_summoned_unit("Pegasus")
        if summon is None:
            raise ValueError("Pegasus summon is required for this strategy")

        return summon

    @final
    @override
    def get_effective_attacker(self, attacker: Unit) -> Unit:
        return self._require_pegasus_summon(attacker)

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
        summon: SummonedUnit = self._require_pegasus_summon(attacker)
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
        summon: SummonedUnit = self._require_pegasus_summon(attacker)

        loaded_attack_health_ratio: float = 0.20
        return HealthScalingDamageCalculationStrategy(
            loaded_attack_health_ratio
        ).calculate_base_damage(
            attacker=summon,
            target=target,
            damage_instance=damage_instance,
        )

    @override
    def calculate_adjusted_potency(
        self,
        attacker: Unit,
        target: Unit,
        damage_instance: DamageInstance,
    ) -> float:
        """
        Returns the adjusted potency for damage_instance, accounting for attacker and target.
        For fixed damage, returns base potency without damage boost modifiers.

        Arguments:
        attacker -- the attacking Unit
        target -- the target of the attack
        damage_instance -- describes the action
        buffs_before -- Buffs to apply to attacker before the action
        debuffs_before -- Debuffs to apply to target before the action
        """
        summon: SummonedUnit = self._require_pegasus_summon(attacker)

        is_fixed_damage: bool = DamageTag.FIXED in damage_instance.tags

        if is_fixed_damage:
            # Fixed damage does not benefit from damage boost modifiers
            adjusted_potency: float = damage_instance.base_potency
        elif DamageTag.BASIC in damage_instance.tags:
            # Liushih Passive - We Fight As One:
            # For every 60 points of Liushih's initial attack, increase the basic attack damage multiplier of both herself
            # and Pegasus by 5%, up to a maximum of 50%.

            # Modify the base potency directly
            maximum_bonus_from_passive: float = 50
            attack_per_5_percent_bonus: float = 60
            bonus_potency_from_passive: float = min(
                (
                    summon.initial_stats.basic_attributes[StatType.ATTACK]
                    // attack_per_5_percent_bonus
                )
                * 5,
                maximum_bonus_from_passive,
            )

            damage_instance.base_potency += bonus_potency_from_passive

        adjusted_potency: float = damage_instance.base_potency * (
            1
            + summon.get_effective_special_attribute(
                SpecialAttribute.DAMAGE_BOOST
            ).get_total_multiplier(damage_instance.tags)
            / 100
        )

        damage_instance.adjusted_potency = adjusted_potency

        return adjusted_potency


class LoreleyDamageCalculationStrategy(StandardDamageCalculationStrategy):
    """Damage calculation strategy for Loreley, implementing her passive effects."""

    @override
    def resolve_buffs(
        self,
        attacker: Unit,
        target: Unit,
        damage_instance: DamageInstance,
        buffs_before: list[Buff] = [],
        debuffs_before: list[Debuff] = [],
    ) -> None:
        """Apply effect of Loreley's abilities."""
        super().resolve_buffs(
            attacker, target, damage_instance, buffs_before, debuffs_before
        )

        # Only expecting to run this for Loreley
        if _is_doll_attacker(attacker):
            # Passive - Queen's Gift
            # All allied dolls wielding a rifle deals 10% increased damage
            attacker.additive_modifiers.special_attributes[
                SpecialAttribute.DAMAGE_BOOST
            ].add_to_multiplier(DamageTag.ALL, 10)

            # V3: Phosphor Pulse: for each Phosphor Pulse triggered, Loreley's damage is increased by 10%,
            # up to a maximum of 60% and critical damage is increased by 2%, up to a maximum of 12%. Assume max 6 Phosphor Pulse triggers for max bonus.
            if attacker.fortification_level >= FortificationLevel.SEGMENT03:
                phosphor_pulse_triggers: int = 6
                damage_boost_per_trigger: int = 10
                crit_dmg_boost_per_trigger: int = 2
                maximum_damage_boost_from_passive: int = 60
                maximum_crit_dmg_boost_from_passive: int = 12

                attacker.additive_modifiers.special_attributes[
                    SpecialAttribute.DAMAGE_BOOST
                ].add_to_multiplier(
                    DamageTag.ALL,
                    min(
                        phosphor_pulse_triggers * damage_boost_per_trigger,
                        maximum_damage_boost_from_passive,
                    ),
                )

                attacker.additive_modifiers.special_attributes[
                    SpecialAttribute.CRITICAL_DAMAGE
                ].add_to_multiplier(
                    DamageTag.ALL,
                    min(
                        phosphor_pulse_triggers * crit_dmg_boost_per_trigger,
                        maximum_crit_dmg_boost_from_passive,
                    ),
                )

            # V6: For each Burn type doll present, increase attack of self by 6%, up to a maximum of 30%. Assume max 5 Burn type dolls for max bonus.
            if attacker.fortification_level >= FortificationLevel.SEGMENT06:
                burn_type_dolls_present: int = 5
                attack_boost_per_burn_type_doll: float = 6
                maximum_attack_boost_from_passive: float = 30
                attacker.multiplicative_modifiers.basic_attributes[
                    StatType.ATTACK
                ] += min(
                    burn_type_dolls_present * attack_boost_per_burn_type_doll,
                    maximum_attack_boost_from_passive,
                )


class SextansDamageCalculationStrategy(StandardDamageCalculationStrategy):
    """Damage calculation strategy for Sextans, implementing her passive effects."""

    @override
    def resolve_buffs(
        self,
        attacker: Unit,
        target: Unit,
        damage_instance: DamageInstance,
        buffs_before: list[Buff] = [],
        debuffs_before: list[Debuff] = [],
    ) -> None:
        """Apply effect of Sextans's abilities."""
        super().resolve_buffs(
            attacker, target, damage_instance, buffs_before, debuffs_before
        )

        # Only expecting to run this for Sextans
        if _is_doll_attacker(attacker):
            # TODO: This effect is tied to having Coagulation, which is effectively all the time.
            # For simplicity, just assume this is always active.
            has_coagulation: bool = True

            if has_coagulation:
                # Model the critical rate overflow effects here;
                # critical rate increase per stack should be applied via Buffs

                # If Sextans's critical rate is greater than 100%, for every 1% of critical rate overflow,
                # her attack, healing, and critical damage is increased.
                bonus_per_overflow_crit_rate: float = 1
                maximum_bonus_from_overflow_crit_rate: float = 30

                overflow_crit_rate: float = (
                    attacker.get_basic_attribute(
                        StatType.CRIT_RATE, damage_instance.tags
                    )
                    - 100
                )

                if attacker.fortification_level >= FortificationLevel.SEGMENT03:
                    maximum_bonus_from_overflow_crit_rate = 45

                if overflow_crit_rate > 0:
                    attacker.multiplicative_modifiers.basic_attributes[
                        StatType.ATTACK
                    ] += min(
                        overflow_crit_rate * bonus_per_overflow_crit_rate,
                        maximum_bonus_from_overflow_crit_rate,
                    )

                    attacker.additive_modifiers.special_attributes[
                        SpecialAttribute.CRITICAL_DAMAGE
                    ].add_to_multiplier(
                        DamageTag.ALL,
                        min(
                            overflow_crit_rate * bonus_per_overflow_crit_rate,
                            maximum_bonus_from_overflow_crit_rate,
                        ),
                    )

            # Passive - Requiem: Damage dealt by all Dolls wielding blades is increased by 10%.
            # Assume Sextans is always benefiting from this passive for simplicity.
            attacker.additive_modifiers.special_attributes[
                SpecialAttribute.DAMAGE_BOOST
            ].add_to_multiplier(
                DamageTag.MELEE,
                10,
            )


class SoppoDamageCalculationStrategy(StandardDamageCalculationStrategy):
    """Damage calculation strategy for Soppo, implementing her passive effects.
    Used to implement the damage boost from her passive for all non-ultimate skills.
    """

    @override
    def resolve_buffs(
        self,
        attacker: Unit,
        target: Unit,
        damage_instance: DamageInstance,
        buffs_before: list[Buff] = [],
        debuffs_before: list[Debuff] = [],
    ) -> None:
        """Apply effect of Soppo's abilities."""
        super().resolve_buffs(
            attacker, target, damage_instance, buffs_before, debuffs_before
        )

        # Only expecting to run this for Soppo
        if _is_doll_attacker(attacker):
            # Passive - Mad Dog Syndrome
            # V0: If there are 3 or more Burn-attribute ally Dolls, damage dealt using certain skills
            # is increased against enemy units with Burn debuffs is increased by 100%.
            # If there are 3 or more Freeze-attribute ally dolls, same but with Freeze debuffs.
            # TODO: For simplicity, just assume this is always active and applies to all damage instances.

            # V4: Damage boost increased to 150% and no longer requires the target to have specific debuffs.
            damage_boost_from_passive: int = 100

            if attacker.fortification_level >= FortificationLevel.SEGMENT04:
                damage_boost_from_passive = 150

            attacker.additive_modifiers.special_attributes[
                SpecialAttribute.DAMAGE_BOOST
            ].add_to_multiplier(
                DamageTag.ALL,
                damage_boost_from_passive,
            )
