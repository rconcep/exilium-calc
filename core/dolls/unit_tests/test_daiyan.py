from core.dolls.daiyan import *

from core.types import (
    DamageTag,
    SpecialAttribute,
    StatType,
    FortificationLevel,
    ModifierType,
)
from core.combat import DamageInstance


class TestDaiyanSkills:
    def test_plucking_strings(self):
        ps: DamageInstance = PluckingStrings().execute(
            did_not_intercept_last_round=False
        )

        assert ps.base_potency == 80
        assert DamageTag.BASIC in ps.tags
        assert DamageTag.MEDIUM_AMMO in ps.tags
        assert DamageTag.PHYSICAL in ps.tags
        assert DamageTag.TARGETED in ps.tags
        assert DamageTag.ACTIVE in ps.tags

    def test_plucking_strings_intercept_bonus(self):
        ps: DamageInstance = PluckingStrings().execute(
            did_not_intercept_last_round=True
        )

        assert ps.base_potency == 230  # 80 + 150

    def test_absolute_tuning(self):
        at: DamageInstance = AbsoluteTuning().execute(
            did_not_intercept_last_round=False
        )

        assert at.base_potency == 150
        assert DamageTag.CONFECTANCE in at.tags
        assert DamageTag.LIGHT_AMMO in at.tags
        assert DamageTag.PHYSICAL in at.tags
        assert DamageTag.TARGETED in at.tags

    def test_absolute_tuning_intercept_bonus(self):
        at: DamageInstance = AbsoluteTuning().execute(did_not_intercept_last_round=True)

        assert at.base_potency == 300  # 150 + 150

    def test_ethereal_resonance(self):
        er: DamageInstance = EtherealResonance().execute(
            did_not_intercept_last_round=False
        )

        assert er.base_potency == 190
        assert DamageTag.ULTIMATE in er.tags
        assert DamageTag.MEDIUM_AMMO in er.tags
        assert DamageTag.PHYSICAL in er.tags

    def test_ethereal_resonance_intercept_bonus(self):
        er: DamageInstance = EtherealResonance().execute(
            did_not_intercept_last_round=True
        )

        assert er.base_potency == 340  # 190 + 150

    def test_interception_below_threshold(self):
        i: DamageInstance = Interception().execute(stacks_of_tuning=2)

        assert i.base_potency == 150
        assert DamageTag.INTERCEPTION in i.tags
        assert DamageTag.PASSIVE in i.tags
        assert DamageTag.LIGHT_AMMO in i.tags
        assert len(i.buffs_before) == 0

    def test_interception_at_threshold(self):
        i: DamageInstance = Interception().execute(stacks_of_tuning=3)

        assert i.base_potency == 150
        assert len(i.buffs_before) == 1
        assert i.buffs_before[0].value == 20
        assert i.buffs_before[0].modifier_type == ModifierType.ADDITIVE
        assert i.buffs_before[0].tag == DamageTag.INTERCEPTION

    def test_interception_above_threshold(self):
        i: DamageInstance = Interception().execute(stacks_of_tuning=6)

        assert i.base_potency == 150
        assert len(i.buffs_before) == 1
        assert i.buffs_before[0].value == 20

    def test_interception_v4_below_threshold(self):
        i: DamageInstance = InterceptionV4().execute(stacks_of_tuning=2)

        assert i.base_potency == 180
        assert len(i.buffs_before) == 1
        assert i.buffs_before[0].value == 0

    def test_interception_v4_middle_threshold(self):
        i: DamageInstance = InterceptionV4().execute(stacks_of_tuning=3)

        assert i.base_potency == 180
        assert i.buffs_before[0].value == 20

    def test_interception_v4_middle_threshold_boundary(self):
        i: DamageInstance = InterceptionV4().execute(stacks_of_tuning=4)

        assert i.base_potency == 180
        assert i.buffs_before[0].value == 20

    def test_interception_v4_high_threshold(self):
        i: DamageInstance = InterceptionV4().execute(stacks_of_tuning=5)

        assert i.base_potency == 180
        assert i.buffs_before[0].value == 40

    def test_interception_v4_high_threshold_above(self):
        i: DamageInstance = InterceptionV4().execute(stacks_of_tuning=8)

        assert i.base_potency == 180
        assert i.buffs_before[0].value == 40

    def test_flowing_melody_no_stacks(self):
        fm: DamageInstance = FlowingMelodyOfTheClouds().execute(
            stacks_of_permanent_tuning=0
        )

        assert fm.base_potency == 0
        assert DamageTag.PHYSICAL in fm.tags
        assert DamageTag.TARGETED in fm.tags

    def test_flowing_melody_six_stacks(self):
        fm: DamageInstance = FlowingMelodyOfTheClouds().execute(
            stacks_of_permanent_tuning=6
        )

        assert fm.base_potency == 600  # 6 * 100

    def test_flowing_melody_max_stacks(self):
        fm: DamageInstance = FlowingMelodyOfTheClouds().execute(
            stacks_of_permanent_tuning=10
        )

        assert fm.base_potency == 1000  # 10 * 100

    def test_flowing_melody_exceeds_max(self):
        fm: DamageInstance = FlowingMelodyOfTheClouds().execute(
            stacks_of_permanent_tuning=15
        )

        assert fm.base_potency == 1000  # capped at 10 stacks


class TestDaiyan:
    def test_set_to_v0(self):
        d: Daiyan = Daiyan()
        d.set_to_v0()

        assert isinstance(d.plucking_strings, PluckingStrings)
        assert isinstance(d.absolute_tuning, AbsoluteTuning)
        assert isinstance(d.ethereal_resonance, EtherealResonance)
        assert isinstance(d.interception, Interception)
        assert isinstance(d.flowing_melody_of_the_clouds, FlowingMelodyOfTheClouds)

    def test_set_to_v4(self):
        d: Daiyan = Daiyan()
        d.set_to_v4()

        assert isinstance(d.interception, InterceptionV4)
        assert isinstance(d.plucking_strings, PluckingStrings)
        assert isinstance(d.ethereal_resonance, EtherealResonance)

    def test_set_fortification_level_segment00(self):
        d: Daiyan = Daiyan()
        d.set_fortification_level(FortificationLevel.SEGMENT00)

        assert isinstance(d.interception, Interception)

    def test_set_fortification_level_segment03(self):
        d: Daiyan = Daiyan()
        d.set_fortification_level(FortificationLevel.SEGMENT03)

        assert isinstance(d.interception, Interception)

    def test_set_fortification_level_segment04(self):
        d: Daiyan = Daiyan()
        d.set_fortification_level(FortificationLevel.SEGMENT04)

        assert isinstance(d.interception, InterceptionV4)

    def test_set_fortification_level_segment06(self):
        d: Daiyan = Daiyan()
        d.set_fortification_level(FortificationLevel.SEGMENT06)

        assert isinstance(d.interception, InterceptionV4)
