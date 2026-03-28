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
        assert kc.group_name == "Counterattack (Kulich)"
        assert isinstance(
            kc.damage_calculation_strategy, KulichDamageCalculationStrategy
        )


class TestNikketaSummon:
    def test_refresh_kulich_syncs_stats(self):
        """refresh_kulich should snapshot Nikketa's current stats onto Kulich."""
        nikketa: Nikketa = Nikketa()
        nikketa.set_to_v0()
        nikketa.initial_stats.basic_attributes[StatType.ATTACK] = 5000
        nikketa.initial_stats.basic_attributes[StatType.HEALTH] = 3000

        nikketa.refresh_kulich()

        kulich = next(u for u in nikketa.summoned_units if u.name == "Kulich")
        assert kulich.initial_stats.basic_attributes[StatType.ATTACK] == 5000 * 0.8
        assert kulich.initial_stats.basic_attributes[StatType.HEALTH] == 3000 * 0.8

    def test_refresh_kulich_replaces_stale_summon(self):
        """Calling refresh_kulich twice leaves exactly one Kulich."""
        nikketa: Nikketa = Nikketa()
        nikketa.set_to_v0()
        nikketa.initial_stats.basic_attributes[StatType.ATTACK] = 1111

        nikketa.refresh_kulich()
        nikketa.initial_stats.basic_attributes[StatType.ATTACK] = 2222
        nikketa.refresh_kulich()

        assert len(nikketa.summoned_units) == 1
        kulich = next(u for u in nikketa.summoned_units if u.name == "Kulich")
        assert kulich.initial_stats.basic_attributes[StatType.ATTACK] == 2222 * 0.8

    def test_prepare_for_calculation_refreshes_kulich(self):
        """prepare_for_calculation should act as refresh_kulich."""
        nikketa: Nikketa = Nikketa()
        nikketa.set_to_v0()
        nikketa.initial_stats.basic_attributes[StatType.ATTACK] = 4000

        nikketa.prepare_for_calculation()

        assert len(nikketa.summoned_units) == 1
        kulich = next(u for u in nikketa.summoned_units if u.name == "Kulich")
        assert kulich.initial_stats.basic_attributes[StatType.ATTACK] == 4000 * 0.8
