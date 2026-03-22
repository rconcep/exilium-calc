from core.dolls.leva import *
from core.types import (
    DamageTag,
    SpecialAttribute,
    StatType,
    FortificationLevel,
    ModifierType,
)
from core.buffs import Buff
from core.combat import DamageInstance


class TestLevaSkills:
    def test_dangerous_smile(self):
        ds: DamageInstance = DangerousSmile().execute()

        assert ds.base_potency == 80
        assert DamageTag.ACTIVE in ds.tags
        assert DamageTag.BASIC in ds.tags
        assert DamageTag.LIGHT_AMMO in ds.tags
        assert DamageTag.TARGETED in ds.tags
        assert DamageTag.PHYSICAL in ds.tags

    def test_rational_suppression(self):
        rs: DamageInstance = RationalSuppression().execute()

        assert rs.base_potency == 120
        assert DamageTag.ACTIVE in rs.tags
        assert DamageTag.ELECTRIC in rs.tags
        assert DamageTag.PHASE in rs.tags
        assert DamageTag.AREA_OF_EFFECT in rs.tags

    def test_rational_suppression_v4(self):
        rs: DamageInstance = RationalSuppressionV4().execute()

        assert rs.base_potency == 120
        assert rs.buffs_before == [
            Buff(25, ModifierType.ADDITIVE, StatType.CRIT_DAMAGE)
        ]

    def test_ordered_disruption_false(self):
        od: DamageInstance = OrderedDisruption().execute(
            target_has_negative_charge=False
        )

        assert od.base_potency == 100
        assert DamageTag.ACTIVE in od.tags
        assert DamageTag.ELECTRIC in od.tags
        assert DamageTag.PHASE in od.tags
        assert DamageTag.LIGHT_AMMO in od.tags
        assert DamageTag.AREA_OF_EFFECT in od.tags
        assert od.buffs_before == []

    def test_ordered_disruption_true(self):
        od: DamageInstance = OrderedDisruption().execute(
            target_has_negative_charge=True
        )

        assert od.base_potency == 100
        assert od.buffs_before == [
            Buff(
                30, ModifierType.ADDITIVE, SpecialAttribute.DAMAGE_BOOST, DamageTag.ALL
            )
        ]

    def test_ordered_disruption_v2_false(self):
        od: DamageInstance = OrderedDisruptionV2().execute(
            target_has_negative_charge=False
        )

        assert od.base_potency == 130
        assert od.buffs_before == []

    def test_ordered_disruption_v2_true(self):
        od: DamageInstance = OrderedDisruptionV2().execute(
            target_has_negative_charge=True
        )

        assert od.base_potency == 130
        assert od.buffs_before == [
            Buff(
                30, ModifierType.ADDITIVE, SpecialAttribute.DAMAGE_BOOST, DamageTag.ALL
            )
        ]

    def test_quantum_calculation(self):
        qc: DamageInstance = QuantumCalculation().execute()

        assert qc.base_potency == 60
        assert DamageTag.ACTIVE in qc.tags
        assert DamageTag.ELECTRIC in qc.tags
        assert DamageTag.PHASE in qc.tags
        assert DamageTag.ULTIMATE in qc.tags
        assert DamageTag.AREA_OF_EFFECT in qc.tags
        assert DamageTag.CONFECTANCE in qc.tags

    def test_quantum_calculation_v5(self):
        qc: DamageInstance = QuantumCalculationV5().execute()

        assert qc.base_potency == 90

    def test_superconductive_strike_1(self):
        ss: DamageInstance = SuperconductiveStrike().execute(
            superconductive_code_consumed=1
        )

        assert ss.base_potency == 60
        assert DamageTag.ACTIVE in ss.tags
        assert DamageTag.ELECTRIC in ss.tags
        assert DamageTag.PHASE in ss.tags
        assert DamageTag.MELEE in ss.tags
        assert DamageTag.TARGETED in ss.tags

    def test_superconductive_strike_2(self):
        ss: DamageInstance = SuperconductiveStrike().execute(
            superconductive_code_consumed=2
        )

        assert ss.base_potency == 70

    def test_superconductive_strike_3(self):
        ss: DamageInstance = SuperconductiveStrike().execute(
            superconductive_code_consumed=3
        )

        assert ss.base_potency == 85

    def test_superconductive_strike_4(self):
        ss: DamageInstance = SuperconductiveStrike().execute(
            superconductive_code_consumed=4
        )

        assert ss.base_potency == 120

    def test_superconductive_strike_v3_1(self):
        ss: DamageInstance = SuperconductiveStrikeV3().execute(
            superconductive_code_consumed=1
        )

        assert ss.base_potency == 75
        assert ss.buffs_before == [
            Buff(
                15,
                ModifierType.ADDITIVE,
                SpecialAttribute.DEFENSE_IGNORE,
                DamageTag.ALL,
            )
        ]

    def test_superconductive_strike_v3_2(self):
        ss: DamageInstance = SuperconductiveStrikeV3().execute(
            superconductive_code_consumed=2
        )

        assert ss.base_potency == 90

    def test_superconductive_strike_v3_3(self):
        ss: DamageInstance = SuperconductiveStrikeV3().execute(
            superconductive_code_consumed=3
        )

        assert ss.base_potency == 120

    def test_superconductive_strike_v3_4(self):
        ss: DamageInstance = SuperconductiveStrikeV3().execute(
            superconductive_code_consumed=4
        )

        assert ss.base_potency == 180

    def test_emergency_support(self):
        es: DamageInstance = EmergencySupport().execute()

        assert es.base_potency == 60
        assert DamageTag.PASSIVE in es.tags
        assert DamageTag.SUPPORT_ACTION in es.tags
        assert DamageTag.PHASE in es.tags
        assert DamageTag.ELECTRIC in es.tags
        assert DamageTag.MELEE in es.tags
        assert DamageTag.TARGETED in es.tags

    def test_overclocking_strike(self):
        os: DamageInstance = OverclockingStrike().execute(excess_stability_damage=10)

        assert os.base_potency == 50  # 5 * 10
        assert DamageTag.PASSIVE in os.tags
        assert DamageTag.PHASE in os.tags
        assert DamageTag.ELECTRIC in os.tags
        assert DamageTag.TARGETED in os.tags

    def test_overclocking_strike_v5(self):
        os: DamageInstance = OverclockingStrikeV5().execute(excess_stability_damage=10)

        assert os.base_potency == 80  # 8 * 10


class TestLeva:
    def test_set_to_v0(self):
        leva: Leva = Leva()
        leva.set_to_v0()

        assert isinstance(leva.dangerous_smile, DangerousSmile)
        assert isinstance(leva.rational_suppression, RationalSuppression)
        assert isinstance(leva.ordered_disruption, OrderedDisruption)
        assert isinstance(leva.quantum_calculation, QuantumCalculation)
        assert isinstance(leva.superconductive_strike, SuperconductiveStrike)
        assert isinstance(leva.emergency_support, EmergencySupport)
        assert isinstance(leva.overclocking_strike, OverclockingStrike)

        # Check special attributes
        assert (
            leva.initial_stats.special_attributes[
                SpecialAttribute.DAMAGE_BOOST
            ].get_multiplier(DamageTag.ELECTRIC)
            == 20
        )
        assert (
            leva.initial_stats.special_attributes[
                SpecialAttribute.CRITICAL_DAMAGE
            ].get_multiplier(DamageTag.ALL)
            == 14
        )

    def test_set_to_v1(self):
        leva: Leva = Leva()
        leva.set_to_v1()

        assert (
            leva.initial_stats.special_attributes[
                SpecialAttribute.DAMAGE_BOOST
            ].get_multiplier(DamageTag.ELECTRIC)
            == 25
        )

    def test_set_to_v2(self):
        leva: Leva = Leva()
        leva.set_to_v2()

        assert isinstance(leva.ordered_disruption, OrderedDisruptionV2)

    def test_set_to_v3(self):
        leva: Leva = Leva()
        leva.set_to_v3()

        assert isinstance(leva.superconductive_strike, SuperconductiveStrikeV3)

    def test_set_to_v4(self):
        leva: Leva = Leva()
        leva.set_to_v4()

        assert isinstance(leva.rational_suppression, RationalSuppressionV4)

    def test_set_to_v5(self):
        leva: Leva = Leva()
        leva.set_to_v5()

        assert isinstance(leva.quantum_calculation, QuantumCalculationV5)
        assert isinstance(leva.overclocking_strike, OverclockingStrikeV5)

    def test_set_to_v6(self):
        leva: Leva = Leva()
        leva.set_to_v6()

        assert leva.multiplicative_modifiers.basic_attributes[StatType.ATTACK] == 15

    def test_set_fortification_level(self):
        leva: Leva = Leva()
        leva.set_fortification_level(FortificationLevel.SEGMENT00)

        assert isinstance(leva.dangerous_smile, DangerousSmile)

        leva.set_fortification_level(FortificationLevel.SEGMENT06)

        assert isinstance(leva.quantum_calculation, QuantumCalculationV5)
        assert isinstance(leva.overclocking_strike, OverclockingStrikeV5)
