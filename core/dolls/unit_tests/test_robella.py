from core.dolls.robella import *

from core.types import DamageTag, SpecialAttribute, StatType, FortificationLevel
from core.combat import DamageInstance


class TestRobellaSkills:
    def test_ultra_shot(self):
        """ """
        ultra_shot_0: DamageInstance = UltraShot().execute(0)

        assert ultra_shot_0.base_potency == 80
        assert DamageTag.PHYSICAL in ultra_shot_0.tags
        assert DamageTag.FREEZE not in ultra_shot_0.tags

    def test_ultra_shot_v6(self):
        ultra_shot_8: DamageInstance = UltraShotV6().execute(8)

        assert ultra_shot_8.base_potency == 152
        assert DamageTag.PHYSICAL not in ultra_shot_8.tags
        assert DamageTag.FREEZE in ultra_shot_8.tags

    def test_unity(self):
        unity: DamageInstance = Unity().execute()

        assert unity.base_potency == 20
        assert DamageTag.PASSIVE in unity.tags

    def test_unity_enhanced(self):
        """ """
        unity: DamageInstance = UnityEnhanced().execute()

        assert unity.base_potency == 30
        assert DamageTag.PASSIVE in unity.tags

    def test_frigid_infiltration(self):
        """ """
        fi: DamageInstance = FrigidInfiltration().execute(2, 0)

        assert fi.base_potency == 156
        assert DamageTag.PASSIVE in fi.tags

    def test_frigid_infiltration_v3(self):
        """ """
        fi: DamageInstance = FrigidInfiltrationV3().execute(2, 0)

        assert fi.base_potency == 156

        fi: DamageInstance = FrigidInfiltrationV3().execute(2, 6)

        assert fi.base_potency == 186

    def test_frigid_infiltration_enhanced(self):
        """ """
        fi: DamageInstance = FrigidInfiltrationEnhanced().execute(2, 0)

        assert fi.base_potency == 168
        assert DamageTag.PASSIVE in fi.tags

    def test_frigid_infiltration_enhanced_v3(self):
        """ """
        fi: DamageInstance = FrigidInfiltrationEnhancedV3().execute(2, 0)

        assert fi.base_potency == 168

        fi: DamageInstance = FrigidInfiltrationEnhancedV3().execute(2, 6)

        assert fi.base_potency == 198

    def test_howling_cyclone(self):
        """ """
        hc: DamageInstance = HowlingCyclone().execute(5)

        assert hc.base_potency == 120
        assert DamageTag.ULTIMATE in hc.tags

    def test_howling_cyclone_v4(self):
        """ """
        hc: DamageInstance = HowlingCycloneV4().execute(5)

        assert hc.base_potency == 195

    def test_howling_cyclone_v6(self):
        """ """
        hc: DamageInstance = HowlingCycloneV6().execute(11)

        assert hc.base_potency == 249


class TestRobella:
    def test_set_to_v0(self):
        ro: Robella = Robella()
        ro.set_to_v0()

        assert isinstance(ro.ultra_shot, UltraShot)
        assert isinstance(ro.unity, Unity)
        assert isinstance(ro.unity_enhanced, UnityEnhanced)
        assert isinstance(ro.frigid_infiltration, FrigidInfiltration)
        assert isinstance(ro.frigid_infiltration_enhanced, FrigidInfiltrationEnhanced)
        assert isinstance(ro.howling_cyclone, HowlingCyclone)

    def test_set_to_v3(self):
        ro: Robella = Robella()
        ro.set_to_v3()

        assert isinstance(ro.frigid_infiltration, FrigidInfiltrationV3)
        assert isinstance(ro.frigid_infiltration_enhanced, FrigidInfiltrationEnhancedV3)

    def test_set_to_v4(self):
        ro: Robella = Robella()
        ro.set_to_v4()

        assert isinstance(ro.howling_cyclone, HowlingCycloneV4)

    def test_set_to_v6(self):
        ro: Robella = Robella()
        ro.set_to_v6()

        assert isinstance(ro.ultra_shot, UltraShotV6)
        assert isinstance(ro.howling_cyclone, HowlingCycloneV6)

    def test_set_to_fortification_level(self):
        ro: Robella = Robella()
        ro.set_fortification_level(FortificationLevel.SEGMENT06)

        assert isinstance(ro.ultra_shot, UltraShotV6)
        assert isinstance(ro.howling_cyclone, HowlingCycloneV6)
