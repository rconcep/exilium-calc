from core.combat import DamageInstance
from core.dolls.cheyanne import *
from core.types import (
    DamageTag,
    FortificationLevel,
    ModifierType,
    SpecialAttribute,
)


class TestCheyanneBuffs:
    def test_get_analysis_score_buff_below_50(self):
        buff = get_analysis_score_buff(49)

        assert buff.value == 10
        assert buff.modifier_type == ModifierType.ADDITIVE
        assert buff.stat_type == SpecialAttribute.CRITICAL_DAMAGE
        assert buff.tag == DamageTag.ALL

    def test_get_analysis_score_buff_at_50(self):
        buff = get_analysis_score_buff(50)

        assert buff.value == 30

    def test_get_analysis_score_buff_v1_scales_with_analysis_score(self):
        buff = get_analysis_score_buffV1(50)

        # 30 from passive threshold + 25 from V1 passive scaling
        assert buff.value == 55


class TestCheyanneSkills:
    def test_definitely_not_360_noscope(self):
        result: DamageInstance = DefinitelyNot360NoScope().execute(analysis_score=40)

        assert result.base_potency == 80
        assert DamageTag.BASIC in result.tags
        assert DamageTag.PHYSICAL in result.tags
        assert result.group_name == "Definitely Not 360 NoScope"
        assert len(result.buffs_before) == 1
        assert result.buffs_before[0].value == 10

    def test_definitely_not_360_noscope_v1(self):
        result: DamageInstance = DefinitelyNot360NoScopeV1().execute(analysis_score=60)

        # 30 from passive threshold + 30 from V1 passive scaling
        assert result.buffs_before[0].value == 60

    def test_focused_pursuit(self):
        result: DamageInstance = FocusedPursuit().execute(analysis_score=80)

        assert result.base_potency == 80
        assert DamageTag.ACTIVE in result.tags
        assert DamageTag.HEAVY_AMMO in result.tags
        assert result.buffs_before[0].value == 30

    def test_focused_pursuit_v1(self):
        result: DamageInstance = FocusedPursuitV1().execute(analysis_score=70)

        # 30 from passive threshold + 35 from V1 passive scaling
        assert result.buffs_before[0].value == 65

    def test_heavenpierce_without_bullseye(self):
        result: DamageInstance = Heavenpierce().execute(
            target_has_bullseye=False,
            few_enemies_with_low_analysis_score=False,
            stacks_of_prepared_stance=0,
        )

        assert result.base_potency == 200
        assert DamageTag.CONFECTANCE in result.tags
        assert len(result.buffs_before) == 1
        assert result.buffs_before[0].value == 30

    def test_heavenpierce_v2_with_bullseye(self):
        result: DamageInstance = HeavenpierceV2().execute(
            target_has_bullseye=True,
            few_enemies_with_low_analysis_score=False,
            stacks_of_prepared_stance=0,
        )

        assert result.base_potency == 280
        assert len(result.buffs_before) == 3
        assert result.buffs_before[0].value == 80
        assert result.buffs_before[1].stat_type == SpecialAttribute.CRITICAL_DAMAGE
        assert result.buffs_before[1].value == 30
        assert result.buffs_before[2].stat_type == SpecialAttribute.DEFENSE_IGNORE
        assert result.buffs_before[2].value == 50

    def test_heavenpierce_v5_few_enemies_bonus(self):
        result: DamageInstance = HeavenpierceV5().execute(
            target_has_bullseye=False,
            few_enemies_with_low_analysis_score=True,
            stacks_of_prepared_stance=0,
        )

        assert result.base_potency == 380

    def test_heavenpierce_v6_prepared_stance_caps_at_3(self):
        result: DamageInstance = HeavenpierceV6().execute(
            target_has_bullseye=False,
            few_enemies_with_low_analysis_score=True,
            stacks_of_prepared_stance=5,
        )

        # 380 with few-enemies condition + (80 * 3 max stacks)
        assert result.base_potency == 620

    def test_deliberate_action(self):
        result: DamageInstance = DeliberateAction().execute(analysis_score=49)

        assert result.base_potency == 120
        assert result.buffs_before[0].value == 10

    def test_deliberate_action_v1(self):
        result: DamageInstance = DeliberateActionV1().execute(analysis_score=50)

        assert result.base_potency == 180
        assert result.buffs_before[0].value == 55

    def test_deliberate_action_v6(self):
        result: DamageInstance = DeliberateActionV6().execute(analysis_score=50)

        assert result.base_potency == 220
        assert result.buffs_before[0].value == 55


class TestCheyanneFortification:
    def test_set_to_v0(self):
        doll = Cheyanne()
        doll.set_to_v0()

        assert isinstance(doll.definitely_not_360_noscope, DefinitelyNot360NoScope)
        assert isinstance(doll.focused_pursuit, FocusedPursuit)
        assert isinstance(doll.heavenpierce, Heavenpierce)
        assert isinstance(doll.deliberate_action, DeliberateAction)

    def test_set_to_v1(self):
        doll = Cheyanne()
        doll.set_to_v1()

        assert isinstance(doll.definitely_not_360_noscope, DefinitelyNot360NoScopeV1)
        assert isinstance(doll.focused_pursuit, FocusedPursuitV1)
        assert isinstance(doll.heavenpierce, HeavenpierceV1)
        assert isinstance(doll.deliberate_action, DeliberateActionV1)

    def test_set_to_v2(self):
        doll = Cheyanne()
        doll.set_to_v2()

        assert isinstance(doll.heavenpierce, HeavenpierceV2)

    def test_set_to_v5(self):
        doll = Cheyanne()
        doll.set_to_v5()

        assert isinstance(doll.heavenpierce, HeavenpierceV5)

    def test_set_to_v6(self):
        doll = Cheyanne()
        doll.set_to_v6()

        assert isinstance(doll.heavenpierce, HeavenpierceV6)
        assert isinstance(doll.deliberate_action, DeliberateActionV6)

    def test_set_fortification_level_segment04(self):
        doll = Cheyanne()
        doll.set_fortification_level(FortificationLevel.SEGMENT04)

        assert doll.fortification_level == FortificationLevel.SEGMENT04
        assert isinstance(doll.definitely_not_360_noscope, DefinitelyNot360NoScopeV1)
        assert isinstance(doll.focused_pursuit, FocusedPursuitV1)
        assert isinstance(doll.heavenpierce, HeavenpierceV2)
        assert isinstance(doll.deliberate_action, DeliberateActionV1)
