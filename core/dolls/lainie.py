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
    LainieDamageCalculationStrategy,
    SimulacrumDamageCalculationStrategy,
)


def _get_algorithmic_stack_buff(confectance_index: int) -> Buff:
    if confectance_index < 0 or confectance_index > 6:
        raise ValueError("confectance_index must be between 0 and 6, inclusive.")

    return Buff(
        value=confectance_index * 15,
        modifier_type=ModifierType.ADDITIVE,
        stat_type=SpecialAttribute.CRITICAL_DAMAGE,
        tag=DamageTag.ALL,
    )


class VictoryProtocol(CombatAction):
    """Lainie Basic Attack."""

    @override
    def execute(self, confectance_index: int) -> DamageInstance:
        label: str = "Victory Protocol"
        base_potency: int = 80

        tags: set[DamageTag] = {
            DamageTag.ACTIVE,
            DamageTag.BASIC,
            DamageTag.LIGHT_AMMO,
            DamageTag.TARGETED,
            DamageTag.PHYSICAL,
        }

        buffs_before: list[Buff] = []

        # Expansion Key - Algorithmic Stack
        buffs_before.append(_get_algorithmic_stack_buff(confectance_index))

        return DamageInstance(
            label=label,
            base_potency=base_potency,
            tags=tags,
            group_name="Victory Protocol",
            buffs_before=buffs_before,
            damage_calculation_strategy=LainieDamageCalculationStrategy(),
        )


class CombatAlgorithm(CombatAction):
    """Lainie S1."""

    @override
    def execute(
        self, target_has_nonpositive_defense: bool, confectance_index: int
    ) -> DamageInstance:
        label: str = "Combat Algorithm"
        base_potency: int = 140

        tags: set[DamageTag] = {
            DamageTag.ACTIVE,
            DamageTag.PHYSICAL,
            DamageTag.LIGHT_AMMO,
            DamageTag.TARGETED,
        }

        buffs_before: list[Buff] = []

        # Expansion Key - Algorithmic Stack
        buffs_before.append(_get_algorithmic_stack_buff(confectance_index))

        # If triggered by Simulacrum's Offense Simulation, if the selected target has 0 or less defense,
        # Combat Algorithm will ignore an additional 30% of the target's defense for this attack.
        if target_has_nonpositive_defense:
            buffs_before.append(
                Buff(
                    value=30,
                    modifier_type=ModifierType.ADDITIVE,
                    stat_type=SpecialAttribute.DEFENSE_IGNORE,
                    tag=DamageTag.ALL,
                )
            )

        return DamageInstance(
            label=label,
            base_potency=base_potency,
            tags=tags,
            group_name="Combat Algorithm",
            damage_calculation_strategy=LainieDamageCalculationStrategy(),
            buffs_before=buffs_before,
        )


class CombatAlgorithmV2(CombatAction):
    """Lainie S1 (V2)."""

    @override
    def execute(
        self, target_has_nonpositive_defense: bool, confectance_index: int
    ) -> DamageInstance:
        label: str = "Combat Algorithm"
        base_potency: int = 140

        tags: set[DamageTag] = {
            DamageTag.ACTIVE,
            DamageTag.PHYSICAL,
            DamageTag.LIGHT_AMMO,
            DamageTag.TARGETED,
        }

        buffs_before: list[Buff] = []

        # Expansion Key - Algorithmic Stack
        buffs_before.append(_get_algorithmic_stack_buff(confectance_index))

        # If triggered by Simulacrum's Offense Simulation, if the selected target has 0 or less defense,
        # Combat Algorithm will ignore an additional 50% of the target's defense for this attack.
        # Additionally, increases Critical damage by 10%
        if target_has_nonpositive_defense:
            buffs_before.append(
                Buff(
                    value=50,
                    modifier_type=ModifierType.ADDITIVE,
                    stat_type=SpecialAttribute.DEFENSE_IGNORE,
                    tag=DamageTag.ALL,
                )
            )
            buffs_before.append(
                Buff(
                    value=10,
                    modifier_type=ModifierType.ADDITIVE,
                    stat_type=SpecialAttribute.CRITICAL_DAMAGE,
                    tag=DamageTag.ALL,
                )
            )

        return DamageInstance(
            label=label,
            base_potency=base_potency,
            tags=tags,
            group_name="Combat Algorithm",
            damage_calculation_strategy=LainieDamageCalculationStrategy(),
            buffs_before=buffs_before,
        )


class CombatAlgorithmV6(CombatAction):
    """Lainie S1 (V6)."""

    @override
    def execute(
        self, target_has_nonpositive_defense: bool, confectance_index: int
    ) -> DamageInstance:
        label: str = "Combat Algorithm"
        base_potency: int = 160

        tags: set[DamageTag] = {
            DamageTag.ACTIVE,
            DamageTag.PHYSICAL,
            DamageTag.LIGHT_AMMO,
            DamageTag.TARGETED,
        }

        buffs_before: list[Buff] = []

        # Expansion Key - Algorithmic Stack
        buffs_before.append(_get_algorithmic_stack_buff(confectance_index))

        # If triggered by Simulacrum's Offense Simulation, if the selected target has 0 or less defense,
        # Combat Algorithm will ignore an additional 50% of the target's defense for this attack.
        # Additionally, increases Critical damage by 10%
        if target_has_nonpositive_defense:
            buffs_before.append(
                Buff(
                    value=50,
                    modifier_type=ModifierType.ADDITIVE,
                    stat_type=SpecialAttribute.DEFENSE_IGNORE,
                    tag=DamageTag.ALL,
                )
            )
            buffs_before.append(
                Buff(
                    value=10,
                    modifier_type=ModifierType.ADDITIVE,
                    stat_type=SpecialAttribute.CRITICAL_DAMAGE,
                    tag=DamageTag.ALL,
                )
            )

        return DamageInstance(
            label=label,
            base_potency=base_potency,
            tags=tags,
            group_name="Combat Algorithm",
            damage_calculation_strategy=LainieDamageCalculationStrategy(),
            buffs_before=buffs_before,
        )


class ComputationalCrush(CombatAction):
    """Lainie S2."""

    @override
    def execute(self, confectance_index: int) -> DamageInstance:
        label: str = "Computational Crush"
        base_potency: int = 120

        tags: set[DamageTag] = {
            DamageTag.ACTIVE,
            DamageTag.PHYSICAL,
            DamageTag.AREA_OF_EFFECT,
        }

        buffs_before: list[Buff] = []

        # Expansion Key - Algorithmic Stack
        buffs_before.append(_get_algorithmic_stack_buff(confectance_index))

        return DamageInstance(
            label=label,
            base_potency=base_potency,
            tags=tags,
            group_name="Computational Crush",
            damage_calculation_strategy=LainieDamageCalculationStrategy(),
            buffs_before=buffs_before,
        )


class PerplexedReflex(CombatAction):
    """Simulacrum Basic Attack."""

    @override
    def execute(self, confectance_index: int) -> DamageInstance:
        label: str = "Perplexed Reflex"
        base_potency: int = 80

        tags: set[DamageTag] = {
            DamageTag.ACTIVE,
            DamageTag.BASIC,
            DamageTag.LIGHT_AMMO,
            DamageTag.TARGETED,
            DamageTag.PHYSICAL,
            DamageTag.PHYSICAL_SUMMON,
        }

        buffs_before: list[Buff] = []

        # Expansion Key - Algorithmic Stack
        buffs_before.append(_get_algorithmic_stack_buff(confectance_index))

        return DamageInstance(
            label=label,
            base_potency=base_potency,
            tags=tags,
            group_name="Perplexed Reflex",
            buffs_before=buffs_before,
            damage_calculation_strategy=SimulacrumDamageCalculationStrategy(),
        )


class OffenseSimulation(CombatAction):
    """Simulacrum S1."""

    @override
    def execute(
        self,
        number_of_additional_targets: int,
        hit_same_target_as_combat_algorithm: bool,
        confectance_index: int,
    ) -> DamageInstance:
        label: str = "Offense Simulation"
        base_potency: int = max(140 - 20 * number_of_additional_targets, 80)

        tags: set[DamageTag] = {
            DamageTag.ACTIVE,
            DamageTag.LIGHT_AMMO,
            DamageTag.AREA_OF_EFFECT,
            DamageTag.PHYSICAL,
            DamageTag.PHYSICAL_SUMMON,
        }

        buffs_before: list[Buff] = []

        # Expansion Key - Algorithmic Stack
        buffs_before.append(_get_algorithmic_stack_buff(confectance_index))

        # If triggered by Lainie's Combat Algorithm, if it does not hit the same target as Combat Algorithm,
        # Offense Simulation will ignore 30% of the target's defense for this attack.
        if not hit_same_target_as_combat_algorithm:
            buffs_before.append(
                Buff(
                    value=30,
                    modifier_type=ModifierType.ADDITIVE,
                    stat_type=SpecialAttribute.DEFENSE_IGNORE,
                    tag=DamageTag.ALL,
                )
            )

        return DamageInstance(
            label=label,
            base_potency=base_potency,
            tags=tags,
            group_name="Offense Simulation",
            damage_calculation_strategy=SimulacrumDamageCalculationStrategy(),
            buffs_before=buffs_before,
        )


class OffenseSimulationV2(CombatAction):
    """Simulacrum S1 (V2)."""

    @override
    def execute(
        self,
        number_of_additional_targets: int,
        hit_same_target_as_combat_algorithm: bool,
        confectance_index: int,
    ) -> DamageInstance:
        label: str = "Offense Simulation"
        base_potency: int = max(140 - 20 * number_of_additional_targets, 80)

        tags: set[DamageTag] = {
            DamageTag.ACTIVE,
            DamageTag.LIGHT_AMMO,
            DamageTag.AREA_OF_EFFECT,
            DamageTag.PHYSICAL,
            DamageTag.PHYSICAL_SUMMON,
        }

        buffs_before: list[Buff] = []

        # Expansion Key - Algorithmic Stack
        buffs_before.append(_get_algorithmic_stack_buff(confectance_index))

        # If triggered by Lainie's Combat Algorithm, if it does not hit the same target as Combat Algorithm,
        # Offense Simulation will ignore 50% of the target's defense for this attack.
        if not hit_same_target_as_combat_algorithm:
            buffs_before.append(
                Buff(
                    value=50,
                    modifier_type=ModifierType.ADDITIVE,
                    stat_type=SpecialAttribute.DEFENSE_IGNORE,
                    tag=DamageTag.ALL,
                )
            )

        return DamageInstance(
            label=label,
            base_potency=base_potency,
            tags=tags,
            group_name="Offense Simulation",
            damage_calculation_strategy=SimulacrumDamageCalculationStrategy(),
            buffs_before=buffs_before,
        )


class OffenseSimulationV6(CombatAction):
    """Simulacrum S1 (V6)."""

    @override
    def execute(
        self,
        number_of_additional_targets: int,
        hit_same_target_as_combat_algorithm: bool,
        confectance_index: int,
    ) -> DamageInstance:
        label: str = "Offense Simulation"
        base_potency: int = max(160 - 20 * number_of_additional_targets, 100)

        tags: set[DamageTag] = {
            DamageTag.ACTIVE,
            DamageTag.LIGHT_AMMO,
            DamageTag.AREA_OF_EFFECT,
            DamageTag.PHYSICAL,
            DamageTag.PHYSICAL_SUMMON,
        }

        buffs_before: list[Buff] = []

        # Expansion Key - Algorithmic Stack
        buffs_before.append(_get_algorithmic_stack_buff(confectance_index))

        # If triggered by Lainie's Combat Algorithm, if it does not hit the same target as Combat Algorithm,
        # Offense Simulation will ignore 50% of the target's defense for this attack.
        if not hit_same_target_as_combat_algorithm:
            buffs_before.append(
                Buff(
                    value=50,
                    modifier_type=ModifierType.ADDITIVE,
                    stat_type=SpecialAttribute.DEFENSE_IGNORE,
                    tag=DamageTag.ALL,
                )
            )

        return DamageInstance(
            label=label,
            base_potency=base_potency,
            tags=tags,
            group_name="Offense Simulation",
            damage_calculation_strategy=SimulacrumDamageCalculationStrategy(),
            buffs_before=buffs_before,
        )


class HashrateOverclock(CombatAction):
    """Simulacrum S2."""

    @override
    def execute(self, confectance_index: int) -> DamageInstance:
        label: str = "Hashrate Overclock"
        base_potency: int = 120

        tags: set[DamageTag] = {
            DamageTag.ACTIVE,
            DamageTag.PHYSICAL,
            DamageTag.AREA_OF_EFFECT,
            DamageTag.PHYSICAL_SUMMON,
        }

        buffs_before: list[Buff] = []

        # Expansion Key - Algorithmic Stack
        buffs_before.append(_get_algorithmic_stack_buff(confectance_index))

        return DamageInstance(
            label=label,
            base_potency=base_potency,
            tags=tags,
            group_name="Hashrate Overclock",
            damage_calculation_strategy=SimulacrumDamageCalculationStrategy(),
            buffs_before=buffs_before,
        )


class Lainie(Doll):
    """Lainie."""

    name: str = "Lainie"
    irrelevant_damage_tags: ClassVar[set[DamageTag]] = set(
        [
            DamageTag.CORROSION,
            DamageTag.BURN,
            DamageTag.FREEZE,
            DamageTag.HYDRO,
            DamageTag.PHASE,
            DamageTag.ELECTRIC,
            DamageTag.MELEE,
            DamageTag.MEDIUM_AMMO,
            DamageTag.HEAVY_AMMO,
            DamageTag.SHOTGUN_AMMO,
            DamageTag.SUPPORT_ACTION,
            DamageTag.INTERCEPTION,
            DamageTag.COUNTERATTACK,
            DamageTag.PASSIVE,
            DamageTag.ULTIMATE,
        ]
    )

    victory_protocol: CombatAction = Field(default_factory=VictoryProtocol)
    combat_algorithm: CombatAction = Field(default_factory=CombatAlgorithm)
    computational_crush: CombatAction = Field(default_factory=ComputationalCrush)
    perplexed_reflex: CombatAction = Field(default_factory=PerplexedReflex)
    offense_simulation: CombatAction = Field(default_factory=OffenseSimulation)
    hashrate_overclock: CombatAction = Field(default_factory=HashrateOverclock)

    def _build_simulacrum(self) -> PhysicalSummonedUnit:
        return PhysicalSummonedUnit(
            name="Simulacrum",
            initial_stats=self.initial_stats.model_copy(deep=True),
            additive_modifiers=self.additive_modifiers.model_copy(deep=True),
            multiplicative_modifiers=self.multiplicative_modifiers.model_copy(
                deep=True
            ),
        )

    def summon_simulacrum(self) -> None:
        """Summons the Simulacrum with a snapshot of Lainie's current stats."""
        if super().get_summoned_unit("Simulacrum") is None:
            self.summoned_units.append(self._build_simulacrum())

    def refresh_simulacrum(self) -> None:
        """Replaces the Simulacrum with a fresh snapshot of Lainie's current stats.

        Call this whenever Lainie's stats have been mutated so that subsequent
        deepcopy-based damage calculations see up-to-date Simulacrum stats.
        """
        self.summoned_units = [u for u in self.summoned_units if u.name != "Simulacrum"]
        self.summoned_units.append(self._build_simulacrum())

    @override
    def prepare_for_calculation(self) -> None:
        self.refresh_simulacrum()

    @override
    def get_summoned_unit(self, name: str) -> SummonedUnit | None:
        self.summon_simulacrum()
        return super().get_summoned_unit(name)

    def set_to_v0(self) -> None:
        """Sets Fortification Level to Segment00."""
        self.victory_protocol = VictoryProtocol()
        self.combat_algorithm = CombatAlgorithm()
        self.computational_crush = ComputationalCrush()
        self.perplexed_reflex = PerplexedReflex()
        self.offense_simulation = OffenseSimulation()
        self.hashrate_overclock = HashrateOverclock()

        self.summon_simulacrum()

    def set_to_v2(self) -> None:
        """Sets Fortification Level to Segment02."""
        self.set_to_v0()

        self.combat_algorithm = CombatAlgorithmV2()
        self.offense_simulation = OffenseSimulationV2()

    def set_to_v6(self) -> None:
        """Sets Fortification Level to Segment06."""
        self.set_to_v2()

        self.combat_algorithm = CombatAlgorithmV6()
        self.offense_simulation = OffenseSimulationV6()

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
                self.set_to_v2()
            case FortificationLevel.SEGMENT04:
                self.set_to_v2()
            case FortificationLevel.SEGMENT05:
                self.set_to_v2()
            case FortificationLevel.SEGMENT06:
                self.set_to_v6()
