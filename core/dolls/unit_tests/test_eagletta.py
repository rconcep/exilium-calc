from core.dolls.eagletta import *

from core.types import DamageTag, SpecialAttribute, StatType, FortificationLevel
from core.combat import DamageInstance


class TestEaglettaSkills:
    def test_rending_talons(self):
        rt: DamageInstance = RendingTalons().execute(2)

        assert rt.base_potency == 70
        assert DamageTag.MELEE in rt.tags
        assert DamageTag.FREEZE in rt.tags
        assert rt.buffs_before[0].value == 5
        assert rt.buffs_before[0].stat_type == SpecialAttribute.DEFENSE_IGNORE

    def test_rending_talons_v2(self):
        rt: DamageInstance = RendingTalonsV2().execute(2)

        assert rt.base_potency == 90

    def test_rending_talons_v6(self):
        rt: DamageInstance = RendingTalonsV6().execute(2)

        assert rt.base_potency == 100
        assert rt.buffs_before[0].value == 10

    def test_swift_eagle_strike(self):
        ses: DamageInstance = SwiftEagleStrike().execute()

        assert ses.base_potency == 100
        assert ses.buffs_before[0].value == 15
        assert ses.buffs_before[0].stat_type == SpecialAttribute.DAMAGE_BOOST
        assert ses.buffs_before[1].value == 5
        assert ses.buffs_before[1].stat_type == SpecialAttribute.CRITICAL_DAMAGE

    def test_swift_eagle_strike_v2(self):
        ses: DamageInstance = SwiftEagleStrikeV2().execute()

        assert ses.base_potency == 120
        assert ses.buffs_before[0].value == 25
        assert ses.buffs_before[1].value == 10

    def test_swift_eagle_strike_v6(self):
        ses: DamageInstance = SwiftEagleStrikeV6().execute()

        assert ses.base_potency == 150
        assert ses.buffs_before[0].value == 40
        assert ses.buffs_before[1].value == 15

    def test_stoop_strike(self):
        ss: DamageInstance = StoopStrike().execute()

        assert ss.base_potency == 100
        assert DamageTag.ACTIVE in ss.tags

    def test_stoop_strike_v3(self):
        ss: DamageInstance = StoopStrikeV3().execute()

        assert ss.base_potency == 120

    def test_featherstorm_feast_no_feathers(self):
        ff: DamageInstance = FeatherstormFeast().execute(
            feathers_of_war_expended=0, triggered_by_swift_eagle_strike=False
        )

        assert ff.base_potency == 120
        assert len(ff.buffs_before) == 0
        assert DamageTag.BASIC not in ff.tags

    def test_featherstorm_feast_one_feather(self):
        ff: DamageInstance = FeatherstormFeast().execute(
            feathers_of_war_expended=1, triggered_by_swift_eagle_strike=False
        )

        assert ff.base_potency == 120
        assert ff.buffs_before[0].value == 20
        assert ff.buffs_before[0].stat_type == SpecialAttribute.DAMAGE_BOOST

    def test_featherstorm_feast_three_feathers_triggered(self):
        ff: DamageInstance = FeatherstormFeast().execute(
            feathers_of_war_expended=3, triggered_by_swift_eagle_strike=True
        )

        assert ff.base_potency == 170
        assert ff.buffs_before[1].value == 35
        assert ff.buffs_before[1].stat_type == SpecialAttribute.CRITICAL_DAMAGE
        assert ff.buffs_before[2].value == 10
        assert ff.buffs_before[2].stat_type == StatType.ATTACK
        assert DamageTag.BASIC in ff.tags

    def test_featherstorm_feast_v4(self):
        ff: DamageInstance = FeatherstormFeastV4().execute(
            feathers_of_war_expended=3, triggered_by_swift_eagle_strike=False
        )

        assert ff.base_potency == 200
        assert ff.buffs_before[0].value == 30
        assert ff.buffs_before[1].value == 45
        assert ff.buffs_before[2].value == 20

    def test_featherstorm_feast_v6(self):
        ff: DamageInstance = FeatherstormFeastV6().execute(
            feathers_of_war_expended=3, triggered_by_swift_eagle_strike=False
        )

        assert ff.base_potency == 230

    def test_predation_not_in_stance(self):
        p: DamageInstance = Predation().execute(
            in_heavy_talons_stance=False, feathers_of_war_expended=3
        )

        assert p.base_potency == 60
        assert len(p.buffs_before) == 0

    def test_predation_in_stance(self):
        p: DamageInstance = Predation().execute(
            in_heavy_talons_stance=True, feathers_of_war_expended=3
        )

        assert p.base_potency == 75
        assert p.buffs_before[0].value == 5

    def test_predation_v2(self):
        p: DamageInstance = PredationV2().execute(
            in_heavy_talons_stance=True, feathers_of_war_expended=3
        )

        assert p.base_potency == 95

    def test_predation_v6(self):
        p: DamageInstance = PredationV6().execute(
            in_heavy_talons_stance=True, feathers_of_war_expended=3
        )

        assert p.base_potency == 110
        assert p.buffs_before[0].value == 10


class TestEagletta:
    def test_set_to_v0(self):
        ea: Eagletta = Eagletta()
        ea.set_to_v0()

        assert isinstance(ea.rending_talons, RendingTalons)
        assert isinstance(ea.swift_eagle_strike, SwiftEagleStrike)
        assert isinstance(ea.stoop_strike, StoopStrike)
        assert isinstance(ea.featherstorm_feast, FeatherstormFeast)
        assert isinstance(ea.predation, Predation)

    def test_set_to_v2(self):
        ea: Eagletta = Eagletta()
        ea.set_to_v2()

        assert isinstance(ea.rending_talons, RendingTalonsV2)
        assert isinstance(ea.swift_eagle_strike, SwiftEagleStrikeV2)
        assert isinstance(ea.predation, PredationV2)

    def test_set_to_v3(self):
        ea: Eagletta = Eagletta()
        ea.set_to_v3()

        assert isinstance(ea.stoop_strike, StoopStrikeV3)

    def test_set_to_v4(self):
        ea: Eagletta = Eagletta()
        ea.set_to_v4()

        assert isinstance(ea.featherstorm_feast, FeatherstormFeastV4)

    def test_set_to_v6(self):
        ea: Eagletta = Eagletta()
        ea.set_to_v6()

        assert isinstance(ea.rending_talons, RendingTalonsV6)
        assert isinstance(ea.swift_eagle_strike, SwiftEagleStrikeV6)
        assert isinstance(ea.featherstorm_feast, FeatherstormFeastV6)
        assert isinstance(ea.predation, PredationV6)

    def test_set_fortification_level(self):
        ea: Eagletta = Eagletta()
        ea.set_fortification_level(FortificationLevel.SEGMENT06)

        assert isinstance(ea.rending_talons, RendingTalonsV6)
        assert isinstance(ea.featherstorm_feast, FeatherstormFeastV6)
