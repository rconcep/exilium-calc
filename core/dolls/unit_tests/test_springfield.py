from core.dolls.springfield import *

from core.combat import DamageInstance, HealthScalingDamageCalculationStrategy
from core.types import DamageTag, FortificationLevel


class TestSpringfieldSkills:
    def test_gentle_approach(self):
        da: DamageInstance = GentleApproach().execute()

        assert da.base_potency == 80
        assert DamageTag.ACTIVE in da.tags
        assert DamageTag.BASIC in da.tags
        assert DamageTag.HEAVY_AMMO in da.tags
        assert DamageTag.TARGETED in da.tags
        assert DamageTag.PHYSICAL in da.tags
        assert da.group_name == "Gentle Approach"

    def test_intel_manipulation(self):
        da: DamageInstance = IntelManipulation().execute()

        assert da.base_potency == 130
        assert DamageTag.ACTIVE in da.tags
        assert DamageTag.HEAVY_AMMO in da.tags
        assert DamageTag.TARGETED in da.tags
        assert DamageTag.HYDRO in da.tags
        assert DamageTag.PHASE in da.tags
        assert da.group_name == "Intel Manipulation"

    def test_intel_manipulation_v4(self):
        da: DamageInstance = IntelManipulationV4().execute()

        assert da.base_potency == 150
        assert da.group_name == "Intel Manipulation"

    def test_path_of_protection(self):
        da: DamageInstance = PathOfProtection().execute()

        assert da.base_potency == 80
        assert DamageTag.ACTIVE in da.tags
        assert DamageTag.HYDRO in da.tags
        assert DamageTag.PHASE in da.tags
        assert DamageTag.AREA_OF_EFFECT in da.tags
        assert DamageTag.ULTIMATE in da.tags
        assert da.group_name == "Path of Protection"

    def test_counterattack_scaling(self):
        da: DamageInstance = Counterattack().execute()

        assert da.base_potency == 100
        assert da.group_name == "Counterattack (Taryz)"
        assert isinstance(
            da.damage_calculation_strategy, HealthScalingDamageCalculationStrategy
        )
        assert da.damage_calculation_strategy.health_scalar == 0.2

    def test_counterattack_v6_scaling(self):
        da: DamageInstance = CounterattackV6().execute()

        assert da.base_potency == 100
        assert isinstance(
            da.damage_calculation_strategy, HealthScalingDamageCalculationStrategy
        )
        assert da.damage_calculation_strategy.health_scalar == 0.4

    def test_support_action_scaling(self):
        da: DamageInstance = SupportAction().execute()

        assert da.base_potency == 0
        assert DamageTag.PASSIVE in da.tags
        assert DamageTag.SUPPORT_ACTION in da.tags
        assert DamageTag.HYDRO in da.tags
        assert DamageTag.PHASE in da.tags
        assert da.group_name == "Support Action (Taryz)"
        assert isinstance(
            da.damage_calculation_strategy, HealthScalingDamageCalculationStrategy
        )
        assert da.damage_calculation_strategy.health_scalar == 0.2

    def test_support_action_v3(self):
        da: DamageInstance = SupportActionV3().execute()

        assert da.base_potency == 100
        assert isinstance(
            da.damage_calculation_strategy, HealthScalingDamageCalculationStrategy
        )
        assert da.damage_calculation_strategy.health_scalar == 0.2

    def test_support_action_v6(self):
        da: DamageInstance = SupportActionV6().execute()

        assert da.base_potency == 100
        assert isinstance(
            da.damage_calculation_strategy, HealthScalingDamageCalculationStrategy
        )
        assert da.damage_calculation_strategy.health_scalar == 0.4


class TestSpringfield:
    def test_set_to_v0(self):
        springfield: Springfield = Springfield()
        springfield.set_to_v0()

        assert isinstance(springfield.gentle_approach, GentleApproach)
        assert isinstance(springfield.intel_manipulation, IntelManipulation)
        assert isinstance(springfield.path_of_protection, PathOfProtection)
        assert isinstance(springfield.counterattack, Counterattack)
        assert isinstance(springfield.support_action, SupportAction)

    def test_set_to_v3(self):
        springfield: Springfield = Springfield()
        springfield.set_to_v3()

        assert isinstance(springfield.support_action, SupportActionV3)

    def test_set_to_v4(self):
        springfield: Springfield = Springfield()
        springfield.set_to_v4()

        assert isinstance(springfield.intel_manipulation, IntelManipulationV4)

    def test_set_to_v6(self):
        springfield: Springfield = Springfield()
        springfield.set_to_v6()

        assert isinstance(springfield.support_action, SupportActionV6)
        assert isinstance(springfield.counterattack, CounterattackV6)

    def test_set_fortification_level(self):
        springfield: Springfield = Springfield()

        springfield.set_fortification_level(FortificationLevel.SEGMENT00)
        assert isinstance(springfield.intel_manipulation, IntelManipulation)

        springfield.set_fortification_level(FortificationLevel.SEGMENT03)
        assert isinstance(springfield.support_action, SupportActionV3)

        springfield.set_fortification_level(FortificationLevel.SEGMENT04)
        assert isinstance(springfield.intel_manipulation, IntelManipulationV4)

        springfield.set_fortification_level(FortificationLevel.SEGMENT06)
        assert isinstance(springfield.counterattack, CounterattackV6)
        assert springfield.fortification_level == FortificationLevel.SEGMENT06
