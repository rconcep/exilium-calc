from core.combat import (
    DamageInstance,
    OTs14TotalSuppressionDamageCalculationStrategy,
    OverloadPulseDamageCalculationStrategy,
    StandardDamageCalculationStrategy,
)
from core.dolls import ots_14
from core.types import DamageTag, FortificationLevel, SpecialAttribute, StatType, Unit


class TestOTs14Skills:
    def test_combat_instinct(self):
        di: DamageInstance = ots_14.CombatInstinct().execute()

        assert di.base_potency == 90
        assert DamageTag.ACTIVE in di.tags
        assert DamageTag.BASIC in di.tags
        assert DamageTag.MEDIUM_AMMO in di.tags
        assert DamageTag.TARGETED in di.tags
        assert DamageTag.OMNI in di.tags
        assert di.label == "Shooting Instinct"
        assert di.group_name == "Shooting Instinct"

    def test_critical_splash_versions(self):
        base: DamageInstance = ots_14.CriticalSplash().execute(previous_uses=0)
        v3: DamageInstance = ots_14.CriticalSplashV3().execute(previous_uses=0)
        v4: DamageInstance = ots_14.CriticalSplashV4().execute(previous_uses=2)

        assert base.base_potency == 150
        assert v3.base_potency == 200
        assert v4.base_potency == 300

    def test_overload_pulse_versions(self):
        base: DamageInstance = ots_14.OverloadPulse().execute(
            accumulated_damage=10000,
            uses_of_critical_splash=3,
        )
        v4: DamageInstance = ots_14.OverloadPulseV4().execute(
            accumulated_damage=10000,
            uses_of_critical_splash=3,
        )

        assert base.base_potency == 1000
        assert v4.base_potency == 4000
        assert DamageTag.FIXED in base.tags
        assert DamageTag.FIXED in v4.tags
        assert isinstance(
            base.damage_calculation_strategy, OverloadPulseDamageCalculationStrategy
        )

    def test_overload_pulse_uses_flat_damage_then_applies_fixed_damage_boost(self):
        doll = ots_14.OTs14()
        doll.initial_stats.basic_attributes[StatType.ATTACK] = 4000
        doll.initial_stats.special_attributes[
            SpecialAttribute.DAMAGE_BOOST
        ].set_multiplier(DamageTag.FIXED, 50)

        di: DamageInstance = ots_14.OverloadPulse().execute(
            accumulated_damage=10000,
            uses_of_critical_splash=0,
        )
        target = Unit()
        target.initial_stats.basic_attributes[StatType.DEFENSE] = 10000

        summary = di.damage_calculation_strategy.calculate_damage(doll, target, di)

        assert summary.non_critical_damage == 1500
        assert summary.critical_damage == 1500
        assert summary.expected_damage == 1500

    def test_total_suppression_uses_default_strategy_without_demolition_mode(self):
        di: DamageInstance = ots_14.TotalSuppression().execute(
            is_in_demolition_mode=False
        )

        assert di.base_potency == 120
        assert isinstance(
            di.damage_calculation_strategy, StandardDamageCalculationStrategy
        )

    def test_total_suppression_uses_ots14_strategy_in_demolition_mode(self):
        di: DamageInstance = ots_14.TotalSuppression().execute(
            is_in_demolition_mode=True
        )

        assert di.base_potency == 120
        assert isinstance(
            di.damage_calculation_strategy,
            OTs14TotalSuppressionDamageCalculationStrategy,
        )


class TestOTs14:
    def test_set_to_v0(self):
        doll = ots_14.OTs14()
        doll.set_to_v0()

        assert isinstance(doll.combat_instinct, ots_14.CombatInstinct)
        assert isinstance(doll.critical_splash, ots_14.CriticalSplash)
        assert isinstance(doll.overload_pulse, ots_14.OverloadPulse)
        assert isinstance(doll.total_suppression, ots_14.TotalSuppression)

    def test_set_to_v4_and_v5(self):
        doll = ots_14.OTs14()

        doll.set_to_v4()
        assert isinstance(doll.critical_splash, ots_14.CriticalSplashV4)
        assert isinstance(doll.overload_pulse, ots_14.OverloadPulseV4)

        doll.set_to_v5()
        assert isinstance(doll.total_suppression, ots_14.TotalSuppressionV5)

    def test_set_fortification_level(self):
        doll = ots_14.OTs14()

        doll.set_fortification_level(FortificationLevel.SEGMENT03)
        assert isinstance(doll.critical_splash, ots_14.CriticalSplashV3)
        assert isinstance(doll.total_suppression, ots_14.TotalSuppressionV2)

        doll.set_fortification_level(FortificationLevel.SEGMENT06)
        assert doll.fortification_level == FortificationLevel.SEGMENT06
        assert isinstance(doll.total_suppression, ots_14.TotalSuppressionV5)


class TestOTs14TotalSuppressionDamageCalculationStrategy:
    @staticmethod
    def construct_defender() -> Unit:
        target = Unit()
        target.initial_stats.basic_attributes[StatType.DEFENSE] = 1000
        return target

    def test_demolition_damage_boost_scales_with_initial_critical_damage(self):
        doll = ots_14.OTs14()
        doll.set_fortification_level(FortificationLevel.SEGMENT00)
        doll.initial_stats.basic_attributes[StatType.ATTACK] = 4000
        doll.initial_stats.basic_attributes[StatType.CRIT_RATE] = 60
        doll.initial_stats.basic_attributes[StatType.CRIT_DAMAGE] = 150

        di: DamageInstance = doll.total_suppression.execute(is_in_demolition_mode=True)
        target = self.construct_defender()

        strategy = di.damage_calculation_strategy
        strategy.apply_assumed_target_state_tags(di)
        strategy.resolve_buffs(doll, target, di)
        adjusted_potency = strategy.calculate_adjusted_potency(doll, target, di)

        # Base potency in demolition mode is 240.
        # Strategy adds +150% damage boost from 150 initial critical damage.
        assert adjusted_potency == 600

    def test_v5_adds_potency_scaling_from_initial_critical_damage(self):
        doll = ots_14.OTs14()
        doll.set_fortification_level(FortificationLevel.SEGMENT05)
        doll.initial_stats.basic_attributes[StatType.ATTACK] = 4000
        doll.initial_stats.basic_attributes[StatType.CRIT_RATE] = 60
        doll.initial_stats.basic_attributes[StatType.CRIT_DAMAGE] = 150

        di: DamageInstance = doll.total_suppression.execute(is_in_demolition_mode=True)
        target = self.construct_defender()

        strategy = di.damage_calculation_strategy
        strategy.apply_assumed_target_state_tags(di)
        strategy.resolve_buffs(doll, target, di)
        adjusted_potency = strategy.calculate_adjusted_potency(doll, target, di)

        # V5 starts at 150, gains +150 potency, then demolition-mode doubles to 600,
        # then +150% damage boost yields 1500.
        assert adjusted_potency == 1500
