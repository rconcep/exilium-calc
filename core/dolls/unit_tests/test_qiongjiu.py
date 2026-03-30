from core.dolls.qiongjiu import *

from core.types import (
    DamageTag,
    ModifierType,
    SpecialAttribute,
    StatType,
    FortificationLevel,
)
from core.buffs import Buff, DamageUpII
from core.combat import DamageInstance


class TestQiongjiu_SkillFuse:
    def test_basic_potency(self):
        result: DamageInstance = Fuse().execute()

        assert result.base_potency == 80

    def test_tags(self):
        result: DamageInstance = Fuse().execute()

        assert DamageTag.ACTIVE in result.tags
        assert DamageTag.BASIC in result.tags
        assert DamageTag.MEDIUM_AMMO in result.tags
        assert DamageTag.TARGETED in result.tags
        assert DamageTag.PHYSICAL in result.tags

    def test_no_buffs(self):
        result: DamageInstance = Fuse().execute()

        assert result.buffs_before == []


class TestQiongjiu_SkillCommonRail:
    def test_basic_potency(self):
        result: DamageInstance = CommonRail().execute()

        assert result.base_potency == 150

    def test_tags(self):
        result: DamageInstance = CommonRail().execute()

        assert DamageTag.ACTIVE in result.tags
        assert DamageTag.BURN in result.tags
        assert DamageTag.PHASE in result.tags
        assert DamageTag.MEDIUM_AMMO in result.tags
        assert DamageTag.TARGETED in result.tags


class TestQiongjiu_SkillGuideToVictory:
    def test_basic_potency(self):
        result: DamageInstance = GuideToVictory().execute(
            target_has_overburn=False,
            has_fixed_key_4=False,
            is_secondary_target=False,
        )

        assert result.base_potency == 110

    def test_tags(self):
        result: DamageInstance = GuideToVictory().execute(
            target_has_overburn=False,
            has_fixed_key_4=False,
            is_secondary_target=False,
        )

        assert DamageTag.ACTIVE in result.tags
        assert DamageTag.AREA_OF_EFFECT in result.tags
        assert DamageTag.BURN in result.tags
        assert DamageTag.PHASE in result.tags

    def test_no_buffs_without_fixed_key_4(self):
        result: DamageInstance = GuideToVictory().execute(
            target_has_overburn=False,
            has_fixed_key_4=False,
            is_secondary_target=True,
        )

        assert result.buffs_before == []

    def test_damage_penalty_on_secondary_target_with_fixed_key_4(self):
        result: DamageInstance = GuideToVictory().execute(
            target_has_overburn=False,
            has_fixed_key_4=True,
            is_secondary_target=True,
        )

        assert len(result.buffs_before) == 1
        assert result.buffs_before[0] == Buff(
            value=-30,
            modifier_type=ModifierType.ADDITIVE,
            stat_type=SpecialAttribute.DAMAGE_BOOST,
            tag=DamageTag.ALL,
        )

    def test_no_penalty_on_primary_target_with_fixed_key_4(self):
        result: DamageInstance = GuideToVictory().execute(
            target_has_overburn=False,
            has_fixed_key_4=True,
            is_secondary_target=False,
        )

        assert result.buffs_before == []


class TestQiongjiu_SkillGuideToVictoryV2:
    def test_crit_rate_buff_when_target_has_overburn(self):
        result: DamageInstance = GuideToVictoryV2().execute(
            target_has_overburn=True,
            has_fixed_key_4=False,
            is_secondary_target=False,
        )

        assert len(result.buffs_before) == 1
        assert result.buffs_before[0] == Buff(
            value=100,
            modifier_type=ModifierType.ADDITIVE,
            stat_type=StatType.CRIT_RATE,
            tag=DamageTag.ALL,
        )

    def test_no_crit_rate_buff_without_overburn(self):
        result: DamageInstance = GuideToVictoryV2().execute(
            target_has_overburn=False,
            has_fixed_key_4=False,
            is_secondary_target=False,
        )

        assert result.buffs_before == []

    def test_both_buffs_overburn_and_fixed_key_4_secondary(self):
        result: DamageInstance = GuideToVictoryV2().execute(
            target_has_overburn=True,
            has_fixed_key_4=True,
            is_secondary_target=True,
        )

        assert len(result.buffs_before) == 2
        assert result.buffs_before[0] == Buff(
            value=100,
            modifier_type=ModifierType.ADDITIVE,
            stat_type=StatType.CRIT_RATE,
            tag=DamageTag.ALL,
        )
        assert result.buffs_before[1] == Buff(
            value=-30,
            modifier_type=ModifierType.ADDITIVE,
            stat_type=SpecialAttribute.DAMAGE_BOOST,
            tag=DamageTag.ALL,
        )

    def test_damage_penalty_only_when_no_overburn(self):
        result: DamageInstance = GuideToVictoryV2().execute(
            target_has_overburn=False,
            has_fixed_key_4=True,
            is_secondary_target=True,
        )

        assert len(result.buffs_before) == 1
        assert result.buffs_before[0] == Buff(
            value=-30,
            modifier_type=ModifierType.ADDITIVE,
            stat_type=SpecialAttribute.DAMAGE_BOOST,
            tag=DamageTag.ALL,
        )


class TestQiongjiu_SkillSupportAction:
    def test_basic_potency(self):
        result: DamageInstance = SupportAction().execute(has_expansion_key=True)

        assert result.base_potency == 90

    def test_tags_with_expansion_key(self):
        result: DamageInstance = SupportAction().execute(has_expansion_key=True)

        assert DamageTag.PASSIVE in result.tags
        assert DamageTag.SUPPORT_ACTION in result.tags
        assert DamageTag.MEDIUM_AMMO in result.tags
        assert DamageTag.TARGETED in result.tags
        assert DamageTag.BURN in result.tags
        assert DamageTag.PHASE in result.tags
        assert DamageTag.PHYSICAL not in result.tags

    def test_tags_without_expansion_key(self):
        result: DamageInstance = SupportAction().execute(has_expansion_key=False)

        assert DamageTag.PHYSICAL in result.tags
        assert DamageTag.BURN not in result.tags
        assert DamageTag.PHASE not in result.tags

    def test_no_buffs(self):
        result: DamageInstance = SupportAction().execute(has_expansion_key=True)

        assert result.buffs_before == []


class TestQiongjiu_SkillSupportActionV3:
    def test_damage_boost_buff(self):
        result: DamageInstance = SupportActionV3().execute(has_expansion_key=True)

        assert len(result.buffs_before) == 1
        assert result.buffs_before[0] == Buff(
            value=10,
            modifier_type=ModifierType.ADDITIVE,
            stat_type=SpecialAttribute.DAMAGE_BOOST,
            tag=DamageTag.SUPPORT_ACTION,
        )

    def test_tags_with_expansion_key(self):
        result: DamageInstance = SupportActionV3().execute(has_expansion_key=True)

        assert DamageTag.BURN in result.tags
        assert DamageTag.PHASE in result.tags
        assert DamageTag.PHYSICAL not in result.tags

    def test_tags_without_expansion_key(self):
        result: DamageInstance = SupportActionV3().execute(has_expansion_key=False)

        assert DamageTag.PHYSICAL in result.tags
        assert DamageTag.BURN not in result.tags


class TestQiongjiu_SkillSupportActionV5:
    def test_buffs_include_damage_boost_and_damage_up_ii(self):
        result: DamageInstance = SupportActionV5().execute(has_expansion_key=True)

        assert len(result.buffs_before) == 2
        assert result.buffs_before[0] == Buff(
            value=10,
            modifier_type=ModifierType.ADDITIVE,
            stat_type=SpecialAttribute.DAMAGE_BOOST,
            tag=DamageTag.SUPPORT_ACTION,
        )
        assert result.buffs_before[1] == DamageUpII()

    def test_tags_with_expansion_key(self):
        result: DamageInstance = SupportActionV5().execute(has_expansion_key=True)

        assert DamageTag.BURN in result.tags
        assert DamageTag.PHASE in result.tags
        assert DamageTag.PHYSICAL not in result.tags

    def test_tags_without_expansion_key(self):
        result: DamageInstance = SupportActionV5().execute(has_expansion_key=False)

        assert DamageTag.PHYSICAL in result.tags
        assert DamageTag.BURN not in result.tags


class TestQiongjiu_DollFortification:
    def test_set_to_v0(self):
        qj: Qiongjiu = Qiongjiu()
        qj.set_to_v0()

        assert isinstance(qj.fuse, Fuse)
        assert isinstance(qj.common_rail, CommonRail)
        assert isinstance(qj.guide_to_victory, GuideToVictory)
        assert isinstance(qj.support_action, SupportAction)

    def test_set_to_v0_expansion_key_burn_damage_boost(self):
        qj: Qiongjiu = Qiongjiu()
        qj.set_to_v0()

        assert (
            qj.initial_stats.special_attributes[
                SpecialAttribute.DAMAGE_BOOST
            ].get_multiplier(DamageTag.ALL)
            == 15
        )

    def test_set_to_v0_exposed_damage_boost(self):
        qj: Qiongjiu = Qiongjiu()
        qj.set_to_v0()

        assert (
            qj.initial_stats.special_attributes[
                SpecialAttribute.DAMAGE_BOOST
            ].get_multiplier(DamageTag.EXPOSED)
            == 10
        )

    def test_set_to_v2(self):
        qj: Qiongjiu = Qiongjiu()
        qj.set_to_v2()

        assert isinstance(qj.guide_to_victory, GuideToVictoryV2)
        assert isinstance(qj.support_action, SupportAction)

    def test_set_to_v3(self):
        qj: Qiongjiu = Qiongjiu()
        qj.set_to_v3()

        assert isinstance(qj.guide_to_victory, GuideToVictoryV2)
        assert isinstance(qj.support_action, SupportActionV3)

    def test_set_to_v5(self):
        qj: Qiongjiu = Qiongjiu()
        qj.set_to_v5()

        assert isinstance(qj.support_action, SupportActionV5)

    def test_set_to_v6_exposed_damage_boost(self):
        qj: Qiongjiu = Qiongjiu()
        qj.set_to_v6()

        assert (
            qj.initial_stats.special_attributes[
                SpecialAttribute.DAMAGE_BOOST
            ].get_multiplier(DamageTag.EXPOSED)
            == 20
        )

    def test_set_fortification_level_v0(self):
        qj: Qiongjiu = Qiongjiu()
        qj.set_fortification_level(FortificationLevel.SEGMENT00)

        assert isinstance(qj.guide_to_victory, GuideToVictory)
        assert isinstance(qj.support_action, SupportAction)

    def test_set_fortification_level_v1_same_as_v0(self):
        qj: Qiongjiu = Qiongjiu()
        qj.set_fortification_level(FortificationLevel.SEGMENT01)

        assert isinstance(qj.guide_to_victory, GuideToVictory)
        assert isinstance(qj.support_action, SupportAction)

    def test_set_fortification_level_v2(self):
        qj: Qiongjiu = Qiongjiu()
        qj.set_fortification_level(FortificationLevel.SEGMENT02)

        assert isinstance(qj.guide_to_victory, GuideToVictoryV2)
        assert isinstance(qj.support_action, SupportAction)

    def test_set_fortification_level_v3(self):
        qj: Qiongjiu = Qiongjiu()
        qj.set_fortification_level(FortificationLevel.SEGMENT03)

        assert isinstance(qj.support_action, SupportActionV3)

    def test_set_fortification_level_v4_same_as_v3(self):
        qj: Qiongjiu = Qiongjiu()
        qj.set_fortification_level(FortificationLevel.SEGMENT04)

        assert isinstance(qj.support_action, SupportActionV3)

    def test_set_fortification_level_v5(self):
        qj: Qiongjiu = Qiongjiu()
        qj.set_fortification_level(FortificationLevel.SEGMENT05)

        assert isinstance(qj.support_action, SupportActionV5)

    def test_set_fortification_level_v6(self):
        qj: Qiongjiu = Qiongjiu()
        qj.set_fortification_level(FortificationLevel.SEGMENT06)

        assert isinstance(qj.support_action, SupportActionV5)
        assert (
            qj.initial_stats.special_attributes[
                SpecialAttribute.DAMAGE_BOOST
            ].get_multiplier(DamageTag.EXPOSED)
            == 20
        )
