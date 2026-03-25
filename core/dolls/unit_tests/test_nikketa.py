from core.dolls.nikketa import *
from core.types import (
    DamageTag,
    SpecialAttribute,
    StatType,
    FortificationLevel,
    ModifierType,
)
from core.buffs import Buff
from core.combat import DamageInstance


class TestNikketaSkills:
    def test_active_deterrence(self):
        ad: DamageInstance = ActiveDeterrence().execute()

        assert ad.base_potency == 80
        assert DamageTag.ACTIVE in ad.tags
        assert DamageTag.BASIC in ad.tags
        assert DamageTag.HEAVY_AMMO in ad.tags
        assert DamageTag.TARGETED in ad.tags
        assert DamageTag.PHYSICAL in ad.tags
        assert ad.group_name == "Active Deterrence"

    def test_k9_deployment(self):
        k9: DamageInstance = K9Deployment().execute()

        assert k9.base_potency == 80
        assert DamageTag.ACTIVE in k9.tags
        assert DamageTag.HEAVY_AMMO in k9.tags
        assert DamageTag.AREA_OF_EFFECT in k9.tags
        assert DamageTag.PHYSICAL in k9.tags
        assert k9.group_name == "K9 Deployment"

    def test_judgment_strike_targeted(self):
        js: DamageInstance = JudgmentStrike().execute(has_fixed_key_3=False)

        assert js.base_potency == 80
        assert DamageTag.ACTIVE in js.tags
        assert DamageTag.PHASE in js.tags
        assert DamageTag.HYDRO in js.tags
        assert DamageTag.TARGETED in js.tags
        assert js.group_name == "Judgment Strike"

    def test_judgment_strike_aoe(self):
        js: DamageInstance = JudgmentStrike().execute(has_fixed_key_3=True)

        assert js.base_potency == 80
        assert DamageTag.ACTIVE in js.tags
        assert DamageTag.PHASE in js.tags
        assert DamageTag.HYDRO in js.tags
        assert DamageTag.AREA_OF_EFFECT in js.tags
        assert js.group_name == "Judgment Strike"

    def test_judgment_strike_v1_targeted(self):
        js: DamageInstance = JudgmentStrikeV1().execute(has_fixed_key_3=False)

        assert js.base_potency == 100
        assert DamageTag.ACTIVE in js.tags
        assert DamageTag.PHASE in js.tags
        assert DamageTag.HYDRO in js.tags
        assert DamageTag.TARGETED in js.tags
        assert js.group_name == "Judgment Strike"

    def test_judgment_strike_v1_aoe(self):
        js: DamageInstance = JudgmentStrikeV1().execute(has_fixed_key_3=True)

        assert js.base_potency == 100
        assert DamageTag.ACTIVE in js.tags
        assert DamageTag.PHASE in js.tags
        assert DamageTag.HYDRO in js.tags
        assert DamageTag.AREA_OF_EFFECT in js.tags
        assert js.group_name == "Judgment Strike"

    def test_righteous_verdict_no_guilt(self):
        rv: DamageInstance = RighteousVerdict().execute(
            target_has_guilt=False, confectance_index_spent=3, is_out_of_turn=False
        )

        assert rv.base_potency == 130
        assert DamageTag.ULTIMATE in rv.tags
        assert DamageTag.PHASE in rv.tags
        assert DamageTag.HYDRO in rv.tags
        assert DamageTag.HEAVY_AMMO in rv.tags
        assert DamageTag.TARGETED in rv.tags
        assert DamageTag.CONFECTANCE in rv.tags
        assert rv.buffs_before == [
            Buff(0, ModifierType.ADDITIVE, SpecialAttribute.DAMAGE_BOOST, DamageTag.ALL)
        ]
        assert rv.group_name == "Righteous Verdict"

    def test_righteous_verdict_with_guilt(self):
        rv: DamageInstance = RighteousVerdict().execute(
            target_has_guilt=True, confectance_index_spent=3, is_out_of_turn=False
        )

        assert rv.base_potency == 260  # 130 * 2
        assert DamageTag.ULTIMATE in rv.tags
        assert DamageTag.PHASE in rv.tags
        assert DamageTag.HYDRO in rv.tags
        assert DamageTag.HEAVY_AMMO in rv.tags
        assert DamageTag.TARGETED in rv.tags
        assert DamageTag.CONFECTANCE in rv.tags
        assert rv.buffs_before == [
            Buff(0, ModifierType.ADDITIVE, SpecialAttribute.DAMAGE_BOOST, DamageTag.ALL)
        ]
        assert rv.group_name == "Righteous Verdict"

    def test_righteous_verdict_out_of_turn(self):
        rv: DamageInstance = RighteousVerdict().execute(
            target_has_guilt=False, confectance_index_spent=3, is_out_of_turn=True
        )

        assert rv.base_potency == 130
        assert DamageTag.PASSIVE in rv.tags
        assert rv.group_name == "Righteous Verdict"

    def test_righteous_verdict_extra_confectance(self):
        rv: DamageInstance = RighteousVerdict().execute(
            target_has_guilt=False, confectance_index_spent=5, is_out_of_turn=False
        )

        assert rv.base_potency == 130
        assert rv.buffs_before == [
            Buff(
                10, ModifierType.ADDITIVE, SpecialAttribute.DAMAGE_BOOST, DamageTag.ALL
            )  # 5 * (5-3)
        ]
        assert rv.group_name == "Righteous Verdict"

    def test_righteous_verdict_v2_no_guilt(self):
        rv: DamageInstance = RighteousVerdictV2().execute(
            target_has_guilt=False, confectance_index_spent=2, is_out_of_turn=False
        )

        assert rv.base_potency == 150
        assert rv.buffs_before == [
            Buff(0, ModifierType.ADDITIVE, SpecialAttribute.DAMAGE_BOOST, DamageTag.ALL)
        ]

    def test_righteous_verdict_v2_with_guilt(self):
        rv: DamageInstance = RighteousVerdictV2().execute(
            target_has_guilt=True, confectance_index_spent=2, is_out_of_turn=False
        )

        assert rv.base_potency == 300  # 150 * 2

    def test_righteous_verdict_v2_extra_confectance(self):
        rv: DamageInstance = RighteousVerdictV2().execute(
            target_has_guilt=False, confectance_index_spent=4, is_out_of_turn=False
        )

        assert rv.base_potency == 150
        assert rv.buffs_before == [
            Buff(
                10, ModifierType.ADDITIVE, SpecialAttribute.DAMAGE_BOOST, DamageTag.ALL
            )  # 5 * (4-2)
        ]

    def test_righteous_verdict_v6_no_guilt(self):
        rv: DamageInstance = RighteousVerdictV6().execute(
            target_has_guilt=False, confectance_index_spent=2, is_out_of_turn=False
        )

        assert rv.base_potency == 150
        assert rv.buffs_before == [
            Buff(0, ModifierType.ADDITIVE, SpecialAttribute.DAMAGE_BOOST, DamageTag.ALL)
        ]

    def test_righteous_verdict_v6_extra_confectance(self):
        rv: DamageInstance = RighteousVerdictV6().execute(
            target_has_guilt=False, confectance_index_spent=4, is_out_of_turn=False
        )

        assert rv.base_potency == 150
        assert rv.buffs_before == [
            Buff(
                20, ModifierType.ADDITIVE, SpecialAttribute.DAMAGE_BOOST, DamageTag.ALL
            )  # 10 * (4-2)
        ]

    def test_kulich_counterattack(self):
        kc: DamageInstance = KulichCounterattack().execute()

        assert kc.base_potency == 80
        assert DamageTag.PASSIVE in kc.tags
        assert DamageTag.COUNTERATTACK in kc.tags
        assert DamageTag.HYDRO in kc.tags
        assert DamageTag.PHASE in kc.tags
        assert DamageTag.PHYSICAL_SUMMON in kc.tags
        assert kc.group_name == "Kulich's Counterattack"
        assert isinstance(
            kc.damage_calculation_strategy, KulichDamageCalculationStrategy
        )
