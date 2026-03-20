from core.dolls.tololo import *

from core.types import DamageTag, SpecialAttribute, StatType, FortificationLevel
from core.combat import DamageInstance


class TestTololoSkills:
    def test_meteor(self):
        di: DamageInstance = Meteor().execute()

        assert di.base_potency == 80
        assert DamageTag.PHYSICAL in di.tags

    def test_black_hole_inversion(self):
        di: DamageInstance = BlackHoleInversion().execute()

        assert di.base_potency == 130
        assert DamageTag.HYDRO in di.tags

    def test_supernova_impact(self):
        di: DamageInstance = SupernovaImpact().execute(number_of_active_buffs=0)

        assert di.base_potency == 130
        assert DamageTag.PHYSICAL in di.tags

        di: DamageInstance = SupernovaImpact().execute(number_of_active_buffs=2)

        assert len(di.buffs_before) > 0

    def test_supernova_impact_v2(self):
        di: DamageInstance = SupernovaImpactV2().execute(number_of_active_buffs=3)

        assert di.base_potency == 130
        assert DamageTag.HYDRO in di.tags

    def test_morte_lumina(self):
        di: DamageInstance = MorteLumina().execute(number_of_active_buffs=0)

        assert di.base_potency == 180
        assert DamageTag.ULTIMATE in di.tags

        di: DamageInstance = MorteLumina().execute(number_of_active_buffs=3)
        assert di.buffs_before[0].value == 15

    def test_morte_lumina_v3(self):
        di: DamageInstance = MorteLuminaV3().execute(number_of_active_buffs=3)
        assert di.buffs_before[0].value == 30


class TestTololo:
    def test_set_to_v0(self):
        tololo: Tololo = Tololo()
        tololo.set_to_v0()

        assert isinstance(tololo.meteor, Meteor)
        assert isinstance(tololo.black_hole_inversion, BlackHoleInversion)
        assert isinstance(tololo.supernova_impact, SupernovaImpact)
        assert isinstance(tololo.morte_lumina, MorteLumina)

    def test_set_to_v2(self):
        tololo: Tololo = Tololo()
        tololo.set_to_v2()

        assert isinstance(tololo.supernova_impact, SupernovaImpactV2)

    def test_set_to_v3(self):
        tololo: Tololo = Tololo()
        tololo.set_to_v3()

        assert isinstance(tololo.morte_lumina, MorteLuminaV3)

    def test_set_to_fortification_level(self):
        tololo: Tololo = Tololo()
        tololo.set_fortification_level(FortificationLevel.SEGMENT06)

        assert isinstance(tololo.supernova_impact, SupernovaImpactV2)
        assert isinstance(tololo.morte_lumina, MorteLuminaV3)
