from core.combat import DamageInstance, HelenDamageCalculationStrategy
from core.dolls.helen import *
from core.types import (
    DamageTag,
    FortificationLevel,
    ModifierType,
    SpecialAttribute,
    StatType,
)
from core.buffs import Buff


class TestHelenSkills:
    def test_condensation_no_sharpened_edge_base_potency(self):
        result: DamageInstance = Condensation().execute(stacks_sharpened_edge=0)

        assert result.base_potency == 80

    def test_condensation_no_sharpened_edge_tags(self):
        result: DamageInstance = Condensation().execute(stacks_sharpened_edge=0)

        assert DamageTag.ACTIVE in result.tags
        assert DamageTag.BASIC in result.tags
        assert DamageTag.SHOTGUN_AMMO in result.tags
        assert DamageTag.TARGETED in result.tags
        assert DamageTag.FREEZE in result.tags
        assert DamageTag.PHASE in result.tags

    def test_condensation_no_sharpened_edge_no_buffs(self):
        result: DamageInstance = Condensation().execute(stacks_sharpened_edge=0)

        assert result.buffs_before == []

    def test_condensation_no_sharpened_edge_group_name(self):
        result: DamageInstance = Condensation().execute(stacks_sharpened_edge=0)

        assert result.group_name == "Condensation"

    def test_condensation_no_sharpened_edge_uses_helen_strategy(self):
        result: DamageInstance = Condensation().execute(stacks_sharpened_edge=0)

        assert isinstance(
            result.damage_calculation_strategy, HelenDamageCalculationStrategy
        )

    def test_condensation_with_sharpened_edge_increases_potency_to_180(self):
        result: DamageInstance = Condensation().execute(stacks_sharpened_edge=1)

        assert result.base_potency == 180

    def test_condensation_with_sharpened_edge_adds_crit_rate_buff(self):
        stacks: int = 5
        result: DamageInstance = Condensation().execute(stacks_sharpened_edge=stacks)

        expected_crit_rate_buff = Buff(
            value=50,
            modifier_type=ModifierType.ADDITIVE,
            stat_type=StatType.CRIT_RATE,
            tag=DamageTag.BASIC,
        )
        assert expected_crit_rate_buff in result.buffs_before

    def test_condensation_with_sharpened_edge_adds_freeze_damage_boost_buff(self):
        stacks: int = 5
        result: DamageInstance = Condensation().execute(stacks_sharpened_edge=stacks)

        expected_freeze_damage_buff = Buff(
            value=50,
            modifier_type=ModifierType.ADDITIVE,
            stat_type=SpecialAttribute.DAMAGE_BOOST,
            tag=DamageTag.BASIC,
        )
        assert expected_freeze_damage_buff in result.buffs_before

    def test_condensation_buffs_scale_linearly_with_stacks(self):
        stacks: int = 20
        result: DamageInstance = Condensation().execute(stacks_sharpened_edge=stacks)

        expected_crit_rate_buff = Buff(
            value=200,
            modifier_type=ModifierType.ADDITIVE,
            stat_type=StatType.CRIT_RATE,
            tag=DamageTag.BASIC,
        )
        expected_freeze_damage_buff = Buff(
            value=200,
            modifier_type=ModifierType.ADDITIVE,
            stat_type=SpecialAttribute.DAMAGE_BOOST,
            tag=DamageTag.BASIC,
        )
        assert expected_crit_rate_buff in result.buffs_before
        assert expected_freeze_damage_buff in result.buffs_before

    def test_condensation_v6_no_sharpened_edge_base_potency(self):
        result: DamageInstance = CondensationV6().execute(stacks_sharpened_edge=0)

        assert result.base_potency == 80

    def test_condensation_v6_with_sharpened_edge_increases_potency_to_300(self):
        result: DamageInstance = CondensationV6().execute(stacks_sharpened_edge=1)

        assert result.base_potency == 300

    def test_condensation_v6_with_sharpened_edge_adds_crit_rate_buff(self):
        stacks: int = 10
        result: DamageInstance = CondensationV6().execute(stacks_sharpened_edge=stacks)

        expected_crit_rate_buff = Buff(
            value=100,
            modifier_type=ModifierType.ADDITIVE,
            stat_type=StatType.CRIT_RATE,
            tag=DamageTag.BASIC,
        )
        assert expected_crit_rate_buff in result.buffs_before

    def test_condensation_v6_with_sharpened_edge_adds_freeze_damage_boost_buff(self):
        stacks: int = 10
        result: DamageInstance = CondensationV6().execute(stacks_sharpened_edge=stacks)

        expected_freeze_damage_buff = Buff(
            value=100,
            modifier_type=ModifierType.ADDITIVE,
            stat_type=SpecialAttribute.DAMAGE_BOOST,
            tag=DamageTag.BASIC,
        )
        assert expected_freeze_damage_buff in result.buffs_before

    def test_condensation_v6_uses_helen_strategy(self):
        result: DamageInstance = CondensationV6().execute(stacks_sharpened_edge=0)

        assert isinstance(
            result.damage_calculation_strategy, HelenDamageCalculationStrategy
        )


class TestHelenFortification:
    def test_set_to_v0_uses_condensation(self):
        helen: Helen = Helen()
        helen.set_to_v0()

        assert isinstance(helen.condensation, Condensation)

    def test_set_to_v6_uses_condensation_v6(self):
        helen: Helen = Helen()
        helen.set_to_v6()

        assert isinstance(helen.condensation, CondensationV6)

    def test_set_fortification_level_segment00_uses_condensation(self):
        helen: Helen = Helen()
        helen.set_fortification_level(FortificationLevel.SEGMENT00)

        assert isinstance(helen.condensation, Condensation)

    def test_set_fortification_level_segment01_uses_condensation(self):
        helen: Helen = Helen()
        helen.set_fortification_level(FortificationLevel.SEGMENT01)

        assert isinstance(helen.condensation, Condensation)

    def test_set_fortification_level_segment02_uses_condensation(self):
        helen: Helen = Helen()
        helen.set_fortification_level(FortificationLevel.SEGMENT02)

        assert isinstance(helen.condensation, Condensation)

    def test_set_fortification_level_segment03_uses_condensation(self):
        helen: Helen = Helen()
        helen.set_fortification_level(FortificationLevel.SEGMENT03)

        assert isinstance(helen.condensation, Condensation)

    def test_set_fortification_level_segment04_uses_condensation(self):
        helen: Helen = Helen()
        helen.set_fortification_level(FortificationLevel.SEGMENT04)

        assert isinstance(helen.condensation, Condensation)

    def test_set_fortification_level_segment05_uses_condensation(self):
        helen: Helen = Helen()
        helen.set_fortification_level(FortificationLevel.SEGMENT05)

        assert isinstance(helen.condensation, Condensation)

    def test_set_fortification_level_segment06_uses_condensation_v6(self):
        helen: Helen = Helen()
        helen.set_fortification_level(FortificationLevel.SEGMENT06)

        assert isinstance(helen.condensation, CondensationV6)
