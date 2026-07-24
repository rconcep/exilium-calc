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
    build_physical_summon_stat_snapshot,
)
from core.buffs import Buff
from core.combat import (
    DamageInstance,
    CombatAction,
    KulichDamageCalculationStrategy,
)


class ActiveDeterrence(CombatAction):
    """Nikketa Basic Attack."""

    @override
    def execute(self) -> DamageInstance:
        label: str = "Active Deterrence"
        base_potency: int = 80

        tags: set[DamageTag] = {
            DamageTag.ACTIVE,
            DamageTag.BASIC,
            DamageTag.HEAVY_AMMO,
            DamageTag.TARGETED,
            DamageTag.PHYSICAL,
        }

        return DamageInstance(
            label=label,
            base_potency=base_potency,
            tags=tags,
            group_name="Active Deterrence",
        )


class K9Deployment(CombatAction):
    """Nikketa S1."""

    @override
    def execute(self) -> DamageInstance:
        label: str = "K9 Deployment"
        base_potency: int = 80

        tags: set[DamageTag] = {
            DamageTag.ACTIVE,
            DamageTag.HEAVY_AMMO,
            DamageTag.AREA_OF_EFFECT,
            DamageTag.PHYSICAL,
        }

        return DamageInstance(
            label=label,
            base_potency=base_potency,
            tags=tags,
            group_name="K9 Deployment",
        )


class JudgmentStrike(CombatAction):
    """Nikketa S2."""

    @override
    def execute(self, has_fixed_key_3: bool) -> DamageInstance:
        label: str = "Judgment Strike"
        base_potency: int = 80

        tags: set[DamageTag] = {
            DamageTag.ACTIVE,
            DamageTag.PHASE,
            DamageTag.HYDRO,
        }

        if has_fixed_key_3:
            tags.add(DamageTag.AREA_OF_EFFECT)
        else:
            tags.add(DamageTag.TARGETED)

        return DamageInstance(
            label=label,
            base_potency=base_potency,
            tags=tags,
            group_name="Judgment Strike",
        )


class JudgmentStrikeV1(CombatAction):
    """Nikketa S2 (V1)."""

    @override
    def execute(self, has_fixed_key_3: bool) -> DamageInstance:
        label: str = "Judgment Strike"
        base_potency: int = 100

        tags: set[DamageTag] = {
            DamageTag.ACTIVE,
            DamageTag.PHASE,
            DamageTag.HYDRO,
        }

        if has_fixed_key_3:
            tags.add(DamageTag.AREA_OF_EFFECT)
        else:
            tags.add(DamageTag.TARGETED)

        return DamageInstance(
            label=label,
            base_potency=base_potency,
            tags=tags,
            group_name="Judgment Strike",
        )


class RighteousVerdict(CombatAction):
    """Nikketa Ultimate."""

    @override
    def execute(
        self,
        target_has_guilt: bool,
        confectance_index_spent: int,
        is_out_of_turn: bool,
    ) -> DamageInstance:
        label: str = "Righteous Verdict"
        base_potency: int = 130
        confectance_index_cost: int = 3

        tags: set[DamageTag] = {
            DamageTag.ULTIMATE,
            DamageTag.PHASE,
            DamageTag.HYDRO,
            DamageTag.HEAVY_AMMO,
            DamageTag.TARGETED,
            DamageTag.CONFECTANCE,
        }

        # If the target has Guilt, performs an additional attack
        if target_has_guilt:
            base_potency *= 2

        # Triggered by Kulich's counterattack
        if is_out_of_turn:
            tags.add(DamageTag.PASSIVE)

        damage_boost_per_confectance_index: int = 5
        damage_boost: float = damage_boost_per_confectance_index * (
            confectance_index_spent - confectance_index_cost
        )

        return DamageInstance(
            label=label,
            base_potency=base_potency,
            tags=tags,
            group_name="Righteous Verdict",
            buffs_before=[
                Buff(
                    value=damage_boost,
                    modifier_type=ModifierType.ADDITIVE,
                    stat_type=SpecialAttribute.DAMAGE_BOOST,
                    tag=DamageTag.ALL,
                )
            ],
        )


class RighteousVerdictV2(CombatAction):
    """Nikketa Ultimate (V2)."""

    @override
    def execute(
        self,
        target_has_guilt: bool,
        confectance_index_spent: int,
        is_out_of_turn: bool,
    ) -> DamageInstance:
        label: str = "Righteous Verdict"
        base_potency: int = 150
        confectance_index_cost: int = 2

        tags: set[DamageTag] = {
            DamageTag.ULTIMATE,
            DamageTag.PHASE,
            DamageTag.HYDRO,
            DamageTag.HEAVY_AMMO,
            DamageTag.TARGETED,
            DamageTag.CONFECTANCE,
        }

        # If the target has Guilt, performs an additional attack
        if target_has_guilt:
            base_potency *= 2

        # Triggered by Kulich's counterattack
        if is_out_of_turn:
            tags.add(DamageTag.PASSIVE)

        damage_boost_per_confectance_index: int = 5
        damage_boost: float = damage_boost_per_confectance_index * (
            confectance_index_spent - confectance_index_cost
        )

        return DamageInstance(
            label=label,
            base_potency=base_potency,
            tags=tags,
            group_name="Righteous Verdict",
            buffs_before=[
                Buff(
                    value=damage_boost,
                    modifier_type=ModifierType.ADDITIVE,
                    stat_type=SpecialAttribute.DAMAGE_BOOST,
                    tag=DamageTag.ALL,
                )
            ],
        )


class RighteousVerdictV6(CombatAction):
    """Nikketa Ultimate (V6)."""

    @override
    def execute(
        self,
        target_has_guilt: bool,
        confectance_index_spent: int,
        is_out_of_turn: bool,
    ) -> DamageInstance:
        label: str = "Righteous Verdict"
        base_potency: int = 150
        confectance_index_cost: int = 2

        tags: set[DamageTag] = {
            DamageTag.ULTIMATE,
            DamageTag.PHASE,
            DamageTag.HYDRO,
            DamageTag.HEAVY_AMMO,
            DamageTag.TARGETED,
            DamageTag.CONFECTANCE,
        }

        # If the target has Guilt, performs an additional attack
        if target_has_guilt:
            base_potency *= 2

        # Triggered by Kulich's counterattack
        if is_out_of_turn:
            tags.add(DamageTag.PASSIVE)

        damage_boost_per_confectance_index: int = 10
        damage_boost: float = damage_boost_per_confectance_index * (
            confectance_index_spent - confectance_index_cost
        )

        return DamageInstance(
            label=label,
            base_potency=base_potency,
            tags=tags,
            group_name="Righteous Verdict",
            buffs_before=[
                Buff(
                    value=damage_boost,
                    modifier_type=ModifierType.ADDITIVE,
                    stat_type=SpecialAttribute.DAMAGE_BOOST,
                    tag=DamageTag.ALL,
                )
            ],
        )


class KulichCounterattack(CombatAction):
    """Kulich's counterattack."""

    @override
    def execute(self) -> DamageInstance:
        label: str = "Counterattack (Kulich)"
        base_potency: int = 80

        tags: set[DamageTag] = {
            DamageTag.PASSIVE,
            DamageTag.COUNTERATTACK,
            DamageTag.HYDRO,
            DamageTag.PHASE,
            DamageTag.PHYSICAL_SUMMON,
            DamageTag.TARGETED,
        }

        return DamageInstance(
            label=label,
            base_potency=base_potency,
            tags=tags,
            group_name="Counterattack (Kulich)",
            damage_calculation_strategy=KulichDamageCalculationStrategy(),
        )


class Nikketa(Doll):
    """Nikketa."""

    name: str = "Nikketa"
    irrelevant_damage_tags: ClassVar[set[DamageTag]] = set(
        [
            DamageTag.CORROSION,
            DamageTag.BURN,
            DamageTag.FREEZE,
            DamageTag.ELECTRIC,
            DamageTag.MELEE,
            DamageTag.LIGHT_AMMO,
            DamageTag.MEDIUM_AMMO,
            DamageTag.SHOTGUN_AMMO,
            DamageTag.SUPPORT_ACTION,
            DamageTag.INTERCEPTION,
        ]
    )

    active_deterrence: CombatAction = Field(default_factory=ActiveDeterrence)
    k9_deployment: CombatAction = Field(default_factory=K9Deployment)
    judgment_strike: CombatAction = Field(default_factory=JudgmentStrike)
    righteous_verdict: CombatAction = Field(default_factory=RighteousVerdict)
    kulich_counterattack: CombatAction = Field(default_factory=KulichCounterattack)

    def _build_kulich(self) -> PhysicalSummonedUnit:
        initial_stats, additive_modifiers, multiplicative_modifiers = (
            build_physical_summon_stat_snapshot(self)
        )
        kulich: PhysicalSummonedUnit = PhysicalSummonedUnit(
            name="Kulich",
            initial_stats=initial_stats,
            additive_modifiers=additive_modifiers,
            multiplicative_modifiers=multiplicative_modifiers,
        )

        # TODO: health ratio upgrades to 1.0 at V5
        health_ratio: float = 0.8
        attack_ratio: float = 0.8
        defense_ratio: float = 1.0

        kulich.initial_stats.basic_attributes[StatType.HEALTH] *= health_ratio
        kulich.initial_stats.basic_attributes[StatType.ATTACK] *= attack_ratio
        kulich.initial_stats.basic_attributes[StatType.DEFENSE] *= defense_ratio

        return kulich

    def summon_kulich(self) -> None:
        """Summons Kulich with a snapshot of Nikketa's current stats."""
        if super().get_summoned_unit("Kulich") is None:
            self.summoned_units.append(self._build_kulich())

    def refresh_kulich(self) -> None:
        """Replaces Kulich with a fresh snapshot of Nikketa's current stats.

        Call this whenever Nikketa's stats have been mutated so that subsequent
        deepcopy-based damage calculations see up-to-date Kulich stats.
        """
        self.summoned_units = [u for u in self.summoned_units if u.name != "Kulich"]
        self.summoned_units.append(self._build_kulich())

    @override
    def prepare_for_calculation(self) -> None:
        self.refresh_kulich()

    @override
    def get_summoned_unit(self, name: str) -> SummonedUnit | None:
        self.summon_kulich()
        return super().get_summoned_unit(name)

    def set_to_v0(self) -> None:
        """Sets Fortification Level to Segment00."""
        self.active_deterrence = ActiveDeterrence()
        self.k9_deployment = K9Deployment()
        self.judgment_strike = JudgmentStrike()
        self.righteous_verdict = RighteousVerdict()
        self.kulich_counterattack = KulichCounterattack()

        self.summon_kulich()

    def set_to_v1(self) -> None:
        """Sets Fortification Level to Segment01."""
        self.set_to_v0()
        self.judgment_strike = JudgmentStrikeV1()

    def set_to_v2(self) -> None:
        """Sets Fortification Level to Segment02."""
        self.set_to_v1()
        self.righteous_verdict = RighteousVerdictV2()

    def set_to_v5(self) -> None:
        """Sets Fortification Level to Segment05."""
        self.set_to_v2()
        self.righteous_verdict = RighteousVerdictV6()

    def set_to_v6(self) -> None:
        """Sets Fortification Level to Segment06."""
        self.set_to_v5()

        self.righteous_verdict = RighteousVerdictV6()

    @override
    def set_fortification_level(self, level: FortificationLevel):
        self.fortification_level = level
        match level:
            case FortificationLevel.SEGMENT00:
                self.set_to_v0()
            case FortificationLevel.SEGMENT01:
                self.set_to_v1()
            case FortificationLevel.SEGMENT02:
                self.set_to_v2()
            case FortificationLevel.SEGMENT03:
                self.set_to_v2()
            case FortificationLevel.SEGMENT04:
                self.set_to_v2()
            case FortificationLevel.SEGMENT05:
                self.set_to_v5()
            case FortificationLevel.SEGMENT06:
                self.set_to_v6()

    def get_sample_rotation(self) -> list[DamageInstance]:
        """Returns a sample single target rotation."""
        rotation_data: list[DamageInstance] = [
            # Turn 1
            self.judgment_strike.execute(has_fixed_key_3=False),
            self.k9_deployment.execute(),
            self.kulich_counterattack.execute(),
            self.righteous_verdict.execute(
                target_has_guilt=True, confectance_index_spent=0, is_out_of_turn=True
            ),
            self.kulich_counterattack.execute(),
            self.righteous_verdict.execute(
                target_has_guilt=True, confectance_index_spent=0, is_out_of_turn=True
            ),
            # Turn 2
            self.judgment_strike.execute(has_fixed_key_3=False),
            self.righteous_verdict.execute(
                target_has_guilt=True, confectance_index_spent=3, is_out_of_turn=False
            ),
            self.kulich_counterattack.execute(),
            self.righteous_verdict.execute(
                target_has_guilt=True, confectance_index_spent=0, is_out_of_turn=True
            ),
            self.kulich_counterattack.execute(),
            self.righteous_verdict.execute(
                target_has_guilt=True, confectance_index_spent=0, is_out_of_turn=True
            ),
            # Turn 3
            self.judgment_strike.execute(has_fixed_key_3=False),  # Justice = 5
            self.righteous_verdict.execute(
                target_has_guilt=True, confectance_index_spent=4, is_out_of_turn=False
            ),
            self.righteous_verdict.execute(
                target_has_guilt=True, confectance_index_spent=0, is_out_of_turn=False
            ),
            self.kulich_counterattack.execute(),
            self.righteous_verdict.execute(
                target_has_guilt=True, confectance_index_spent=0, is_out_of_turn=True
            ),
            self.kulich_counterattack.execute(),
            self.righteous_verdict.execute(
                target_has_guilt=True, confectance_index_spent=0, is_out_of_turn=True
            ),
            # Turn 4
            self.judgment_strike.execute(has_fixed_key_3=False),
            self.righteous_verdict.execute(
                target_has_guilt=True, confectance_index_spent=3, is_out_of_turn=False
            ),
            self.kulich_counterattack.execute(),
            self.righteous_verdict.execute(
                target_has_guilt=True, confectance_index_spent=0, is_out_of_turn=True
            ),
            self.kulich_counterattack.execute(),
            self.righteous_verdict.execute(
                target_has_guilt=True, confectance_index_spent=0, is_out_of_turn=True
            ),
            # Turn 5
            self.judgment_strike.execute(has_fixed_key_3=False),
            self.righteous_verdict.execute(
                target_has_guilt=True, confectance_index_spent=3, is_out_of_turn=False
            ),
            # Justice = 5
            self.kulich_counterattack.execute(),
            self.righteous_verdict.execute(
                target_has_guilt=True, confectance_index_spent=0, is_out_of_turn=True
            ),
            self.kulich_counterattack.execute(),
            self.righteous_verdict.execute(
                target_has_guilt=True, confectance_index_spent=0, is_out_of_turn=True
            ),
            # Turn 6
            self.judgment_strike.execute(has_fixed_key_3=False),
            self.righteous_verdict.execute(
                target_has_guilt=True, confectance_index_spent=4, is_out_of_turn=False
            ),
            self.righteous_verdict.execute(
                target_has_guilt=True, confectance_index_spent=0, is_out_of_turn=False
            ),
            self.kulich_counterattack.execute(),
            self.righteous_verdict.execute(
                target_has_guilt=True, confectance_index_spent=0, is_out_of_turn=True
            ),
            self.kulich_counterattack.execute(),
            self.righteous_verdict.execute(
                target_has_guilt=True, confectance_index_spent=0, is_out_of_turn=True
            ),
            # Turn 7
            self.judgment_strike.execute(has_fixed_key_3=False),
            self.righteous_verdict.execute(
                target_has_guilt=True, confectance_index_spent=4, is_out_of_turn=False
            ),
            self.righteous_verdict.execute(
                target_has_guilt=True, confectance_index_spent=0, is_out_of_turn=False
            ),
            self.kulich_counterattack.execute(),
            self.righteous_verdict.execute(
                target_has_guilt=True, confectance_index_spent=0, is_out_of_turn=True
            ),
            self.kulich_counterattack.execute(),
            self.righteous_verdict.execute(
                target_has_guilt=True, confectance_index_spent=0, is_out_of_turn=True
            ),
        ]

        return rotation_data
