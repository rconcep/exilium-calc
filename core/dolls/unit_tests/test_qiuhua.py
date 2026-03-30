from core.buffs import Buff
from core.combat import DamageInstance, QiuhuaDamageCalculationStrategy
from core.dolls.qiuhua import *
from core.types import (
    DamageTag,
    FortificationLevel,
    ModifierType,
    SpecialAttribute,
)


class TestQiuhuaSkills:
    def test_trailblaze(self):
        trailblaze: DamageInstance = Trailblaze().execute()

        assert trailblaze.base_potency == 80
        assert DamageTag.ACTIVE in trailblaze.tags
        assert DamageTag.BASIC in trailblaze.tags
        assert DamageTag.SHOTGUN_AMMO in trailblaze.tags
        assert DamageTag.TARGETED in trailblaze.tags
        assert DamageTag.PHYSICAL in trailblaze.tags
        assert trailblaze.group_name == "Trailblaze"
        assert isinstance(
            trailblaze.damage_calculation_strategy,
            QiuhuaDamageCalculationStrategy,
        )

    def test_searing_sizzle_within_range(self):
        searing_sizzle: DamageInstance = SearingSizzle().execute(
            target_is_within_4_tiles=True,
            target_has_scorch_mark=False,
        )

        assert searing_sizzle.base_potency == 120
        assert DamageTag.BURN in searing_sizzle.tags
        assert searing_sizzle.buffs_before == [
            Buff(
                5,
                ModifierType.ADDITIVE,
                SpecialAttribute.DAMAGE_BOOST,
                DamageTag.ALL,
            )
        ]

    def test_searing_sizzle_v5_all_conditions(self):
        searing_sizzle: DamageInstance = SearingSizzleV5().execute(
            target_is_within_4_tiles=True,
            target_has_scorch_mark=True,
        )

        assert searing_sizzle.base_potency == 120
        assert searing_sizzle.buffs_before == [
            Buff(
                30,
                ModifierType.ADDITIVE,
                SpecialAttribute.DAMAGE_BOOST,
                DamageTag.ALL,
            ),
            Buff(
                15,
                ModifierType.ADDITIVE,
                SpecialAttribute.DAMAGE_BOOST,
                DamageTag.ALL,
            ),
        ]

    def test_soaring_leap_and_v4(self):
        soaring_leap: DamageInstance = SoaringLeap().execute()
        soaring_leap_v4: DamageInstance = SoaringLeapV4().execute()

        assert soaring_leap.base_potency == 30
        assert soaring_leap_v4.base_potency == 80
        assert soaring_leap.group_name == "Soaring Leap"
        assert DamageTag.BURN in soaring_leap.tags

    def test_boil_and_reduce(self):
        boil_and_reduce: DamageInstance = BoilAndReduce().execute(
            confectance_index_spent=4,
        )

        assert boil_and_reduce.base_potency == 110
        assert DamageTag.ULTIMATE in boil_and_reduce.tags
        assert DamageTag.CONFECTANCE in boil_and_reduce.tags

    def test_boil_and_reduce_v6(self):
        boil_and_reduce: DamageInstance = BoilAndReduceV6().execute(
            confectance_index_spent=4,
        )

        assert boil_and_reduce.base_potency == 110
        assert boil_and_reduce.buffs_before == [
            Buff(
                15,
                ModifierType.ADDITIVE,
                SpecialAttribute.DAMAGE_BOOST,
                DamageTag.ONLY_HIT_ONE_TARGET,
            )
        ]

    def test_scorch_mark_versions(self):
        scorch_mark: DamageInstance = ScorchMark().execute(stacks=20)
        scorch_mark_v3: DamageInstance = ScorchMarkV3().execute(stacks=20)
        scorch_mark_v6: DamageInstance = ScorchMarkV6().execute(stacks=20)

        assert scorch_mark.base_potency == 84
        assert scorch_mark_v3.base_potency == 140
        assert scorch_mark_v6.base_potency == 200
        assert DamageTag.PASSIVE in scorch_mark.tags

    def test_emergency_support(self):
        emergency_support: DamageInstance = EmergencySupport().execute()

        assert emergency_support.base_potency == 60
        assert DamageTag.SUPPORT_ACTION in emergency_support.tags
        assert DamageTag.PASSIVE in emergency_support.tags
        assert emergency_support.group_name == "Emergency Support"


class TestQiuhua:
    def test_set_to_v0(self):
        qiuhua: Qiuhua = Qiuhua()
        qiuhua.set_to_v0()

        assert isinstance(qiuhua.searing_sizzle, SearingSizzle)
        assert isinstance(qiuhua.soaring_leap, SoaringLeap)
        assert isinstance(qiuhua.boil_and_reduce, BoilAndReduce)
        assert isinstance(qiuhua.scorch_mark, ScorchMark)

    def test_set_to_v3(self):
        qiuhua: Qiuhua = Qiuhua()
        qiuhua.set_to_v3()

        assert isinstance(qiuhua.scorch_mark, ScorchMarkV3)

    def test_set_to_v6(self):
        qiuhua: Qiuhua = Qiuhua()
        qiuhua.set_to_v6()

        assert isinstance(qiuhua.searing_sizzle, SearingSizzleV5)
        assert isinstance(qiuhua.soaring_leap, SoaringLeapV4)
        assert isinstance(qiuhua.boil_and_reduce, BoilAndReduceV6)
        assert isinstance(qiuhua.scorch_mark, ScorchMarkV6)

    def test_set_to_fortification_level(self):
        qiuhua: Qiuhua = Qiuhua()
        qiuhua.set_fortification_level(FortificationLevel.SEGMENT03)
        assert isinstance(qiuhua.scorch_mark, ScorchMarkV3)

        qiuhua.set_fortification_level(FortificationLevel.SEGMENT06)
        assert qiuhua.fortification_level == FortificationLevel.SEGMENT06
        assert isinstance(qiuhua.boil_and_reduce, BoilAndReduceV6)
        assert isinstance(qiuhua.scorch_mark, ScorchMarkV6)
