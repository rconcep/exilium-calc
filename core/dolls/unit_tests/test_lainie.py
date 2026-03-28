from core.dolls.lainie import *
from core.types import DamageTag, SpecialAttribute, FortificationLevel, ModifierType
from core.buffs import Buff
from core.combat import (
    DamageInstance,
    LainieDamageCalculationStrategy,
    SimulacrumDamageCalculationStrategy,
)


class TestLainieSkills:
    def test_victory_protocol(self):
        vp: DamageInstance = VictoryProtocol().execute()

        assert vp.base_potency == 80
        assert DamageTag.BASIC in vp.tags
        assert DamageTag.PHYSICAL in vp.tags
        assert isinstance(
            vp.damage_calculation_strategy, LainieDamageCalculationStrategy
        )

    def test_combat_algorithm(self):
        ca: DamageInstance = CombatAlgorithm().execute(
            target_has_nonpositive_defense=False
        )

        assert ca.base_potency == 140
        assert ca.buffs_before == [
            Buff(
                value=15,
                modifier_type=ModifierType.ADDITIVE,
                stat_type=SpecialAttribute.CRITICAL_DAMAGE,
                tag=DamageTag.ALL,
            )
        ]

    def test_combat_algorithm_with_nonpositive_defense(self):
        ca: DamageInstance = CombatAlgorithm().execute(
            target_has_nonpositive_defense=True
        )

        assert ca.base_potency == 140
        assert ca.buffs_before[0] == Buff(
            value=15,
            modifier_type=ModifierType.ADDITIVE,
            stat_type=SpecialAttribute.CRITICAL_DAMAGE,
            tag=DamageTag.ALL,
        )
        assert ca.buffs_before[1] == Buff(
            value=30,
            modifier_type=ModifierType.ADDITIVE,
            stat_type=SpecialAttribute.DEFENSE_IGNORE,
            tag=DamageTag.ALL,
        )

    def test_combat_algorithm_v2_with_nonpositive_defense(self):
        ca: DamageInstance = CombatAlgorithmV2().execute(
            target_has_nonpositive_defense=True
        )

        assert ca.base_potency == 140
        assert ca.buffs_before[1] == Buff(
            value=50,
            modifier_type=ModifierType.ADDITIVE,
            stat_type=SpecialAttribute.DEFENSE_IGNORE,
            tag=DamageTag.ALL,
        )
        assert ca.buffs_before[2] == Buff(
            value=10,
            modifier_type=ModifierType.ADDITIVE,
            stat_type=SpecialAttribute.CRITICAL_DAMAGE,
            tag=DamageTag.ALL,
        )

    def test_combat_algorithm_v6(self):
        ca: DamageInstance = CombatAlgorithmV6().execute(
            target_has_nonpositive_defense=False
        )

        assert ca.base_potency == 160

    def test_computational_crush(self):
        cc: DamageInstance = ComputationalCrush().execute()

        assert cc.base_potency == 200
        assert DamageTag.AREA_OF_EFFECT in cc.tags
        assert cc.buffs_before == [
            Buff(
                value=15,
                modifier_type=ModifierType.ADDITIVE,
                stat_type=SpecialAttribute.CRITICAL_DAMAGE,
                tag=DamageTag.ALL,
            )
        ]

    def test_phantom_barrage(self):
        pb: DamageInstance = PerplexedReflex().execute()

        assert pb.base_potency == 80
        assert DamageTag.PHYSICAL_SUMMON in pb.tags
        assert isinstance(
            pb.damage_calculation_strategy, SimulacrumDamageCalculationStrategy
        )

    def test_offense_simulation_floor_and_no_bonus(self):
        os: DamageInstance = OffenseSimulation().execute(
            number_of_targets=6,
            hit_same_target_as_combat_algorithm=True,
        )

        assert os.base_potency == 80
        assert len(os.buffs_before) == 1
        assert os.buffs_before[0] == Buff(
            value=15,
            modifier_type=ModifierType.ADDITIVE,
            stat_type=SpecialAttribute.CRITICAL_DAMAGE,
            tag=DamageTag.ALL,
        )

    def test_offense_simulation_defense_ignore_bonus(self):
        os: DamageInstance = OffenseSimulation().execute(
            number_of_targets=2,
            hit_same_target_as_combat_algorithm=False,
        )

        assert os.base_potency == 100
        assert os.buffs_before[1] == Buff(
            value=30,
            modifier_type=ModifierType.ADDITIVE,
            stat_type=SpecialAttribute.DEFENSE_IGNORE,
            tag=DamageTag.ALL,
        )

    def test_offense_simulation_v2_bonus(self):
        os: DamageInstance = OffenseSimulationV2().execute(
            number_of_targets=2,
            hit_same_target_as_combat_algorithm=False,
        )

        assert os.base_potency == 100
        assert os.buffs_before[1] == Buff(
            value=50,
            modifier_type=ModifierType.ADDITIVE,
            stat_type=SpecialAttribute.DEFENSE_IGNORE,
            tag=DamageTag.ALL,
        )

    def test_offense_simulation_v6_floor(self):
        os: DamageInstance = OffenseSimulationV6().execute(
            number_of_targets=8,
            hit_same_target_as_combat_algorithm=True,
        )

        assert os.base_potency == 100

    def test_cognition_overclock(self):
        co: DamageInstance = HashrateOverclock().execute()

        assert co.base_potency == 120
        assert DamageTag.PHYSICAL_SUMMON in co.tags
        assert co.buffs_before[0] == Buff(
            value=15,
            modifier_type=ModifierType.ADDITIVE,
            stat_type=SpecialAttribute.CRITICAL_DAMAGE,
            tag=DamageTag.ALL,
        )


class TestLainie:
    def test_get_summoned_unit_auto_summons_simulacrum(self):
        lainie: Lainie = Lainie()

        summon = lainie.get_summoned_unit("Simulacrum")

        assert summon is not None
        assert summon.name == "Simulacrum"
        assert len(lainie.summoned_units) == 1

    def test_summon_simulacrum_is_idempotent(self):
        lainie: Lainie = Lainie()

        lainie.summon_simulacrum()
        lainie.summon_simulacrum()

        assert len(lainie.summoned_units) == 1

    def test_set_to_v0(self):
        lainie: Lainie = Lainie()
        lainie.set_to_v0()

        assert isinstance(lainie.victory_protocol, VictoryProtocol)
        assert isinstance(lainie.combat_algorithm, CombatAlgorithm)
        assert isinstance(lainie.computational_crush, ComputationalCrush)
        assert isinstance(lainie.perplexed_reflex, PerplexedReflex)
        assert isinstance(lainie.offense_simulation, OffenseSimulation)
        assert isinstance(lainie.hashrate_overclock, HashrateOverclock)
        assert lainie.get_summoned_unit("Simulacrum") is not None

    def test_set_to_v2(self):
        lainie: Lainie = Lainie()
        lainie.set_to_v2()

        assert isinstance(lainie.combat_algorithm, CombatAlgorithmV2)
        assert isinstance(lainie.offense_simulation, OffenseSimulationV2)

    def test_set_to_v6(self):
        lainie: Lainie = Lainie()
        lainie.set_to_v6()

        assert isinstance(lainie.combat_algorithm, CombatAlgorithmV6)
        assert isinstance(lainie.offense_simulation, OffenseSimulationV6)

    def test_set_to_fortification_level(self):
        lainie: Lainie = Lainie()
        lainie.set_fortification_level(FortificationLevel.SEGMENT06)

        assert isinstance(lainie.combat_algorithm, CombatAlgorithmV6)
        assert isinstance(lainie.offense_simulation, OffenseSimulationV6)

    def test_set_to_v0_after_v6_resets_upgraded_skills(self):
        lainie: Lainie = Lainie()
        lainie.set_to_v6()

        assert isinstance(lainie.combat_algorithm, CombatAlgorithmV6)
        assert isinstance(lainie.offense_simulation, OffenseSimulationV6)

        lainie.set_to_v0()

        assert isinstance(lainie.combat_algorithm, CombatAlgorithm)
        assert isinstance(lainie.offense_simulation, OffenseSimulation)

    def test_refresh_simulacrum_syncs_stats(self):
        """refresh_simulacrum should create the Simulacrum with Lainie's current stats."""
        lainie: Lainie = Lainie()
        # summon_simulacrum is called during set_to_v0 with zero stats
        lainie.set_to_v0()
        lainie.initial_stats.basic_attributes[StatType.ATTACK] = 5000
        lainie.initial_stats.basic_attributes[StatType.HEALTH] = 3000

        lainie.refresh_simulacrum()

        summon = next(u for u in lainie.summoned_units if u.name == "Simulacrum")
        assert summon.initial_stats.basic_attributes[StatType.ATTACK] == 5000
        assert summon.initial_stats.basic_attributes[StatType.HEALTH] == 3000

    def test_refresh_simulacrum_replaces_stale_summon(self):
        """Calling refresh_simulacrum twice leaves exactly one Simulacrum."""
        lainie: Lainie = Lainie()
        lainie.set_to_v0()
        lainie.initial_stats.basic_attributes[StatType.ATTACK] = 1111

        lainie.refresh_simulacrum()
        lainie.initial_stats.basic_attributes[StatType.ATTACK] = 2222
        lainie.refresh_simulacrum()

        assert len(lainie.summoned_units) == 1
        summon = next(u for u in lainie.summoned_units if u.name == "Simulacrum")
        assert summon.initial_stats.basic_attributes[StatType.ATTACK] == 2222
