import pytest
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


class TestCallOfTheStars:
    """Tests for Call of the Stars (Geostationary Satellite passive)."""

    def test_base_potency(self):
        """Base potency should be 130."""
        skill = CallOfTheStars()
        di = skill.execute(stacks_of_observation_advantage=0)

        assert di.base_potency == 130
        assert di.label == "Call of the Stars (Geostationary Satellite)"

    def test_has_physical_summon_tag(self):
        """Should be tagged as PHYSICAL_SUMMON."""
        skill = CallOfTheStars()
        di = skill.execute(stacks_of_observation_advantage=0)

        assert DamageTag.PHYSICAL_SUMMON in di.tags
        assert DamageTag.HYDRO in di.tags
        assert DamageTag.PHASE in di.tags

    def test_no_buffs_at_zero_stacks(self):
        """No stacks should produce no buffs."""
        skill = CallOfTheStars()
        di = skill.execute(stacks_of_observation_advantage=0)

        assert len(di.buffs_before) == 0
        assert di.base_potency == 130

    def test_buffs_at_one_stack(self):
        """1 stack should add small buffs."""
        skill = CallOfTheStars()
        di = skill.execute(stacks_of_observation_advantage=1)

        assert len(di.buffs_before) == 3
        # Check for attack, damage boost, and critical damage buffs
        buff_types = {buff.stat_type for buff in di.buffs_before}
        assert StatType.ATTACK in buff_types
        assert SpecialAttribute.DAMAGE_BOOST in buff_types
        assert SpecialAttribute.CRITICAL_DAMAGE in buff_types

    def test_buff_values_at_one_stack(self):
        """1 stack should give: attack +5%, damage +20%, crit damage +5%."""
        skill = CallOfTheStars()
        di = skill.execute(stacks_of_observation_advantage=1)

        # Base potency unchanged at 1 stack
        assert di.base_potency == 130

        attack_buff = next(
            (b for b in di.buffs_before if b.stat_type == StatType.ATTACK),
            None,
        )
        damage_buff = next(
            (
                b
                for b in di.buffs_before
                if b.stat_type == SpecialAttribute.DAMAGE_BOOST
            ),
            None,
        )
        crit_buff = next(
            (
                b
                for b in di.buffs_before
                if b.stat_type == SpecialAttribute.CRITICAL_DAMAGE
            ),
            None,
        )

        assert attack_buff is not None and attack_buff.value == 5
        assert damage_buff is not None and damage_buff.value == 20
        assert crit_buff is not None and crit_buff.value == 5

    def test_buff_values_at_three_stacks(self):
        """3 stacks should give: attack +10%, damage +40%, crit damage +10%, potency +60."""
        skill = CallOfTheStars()
        di = skill.execute(stacks_of_observation_advantage=3)

        # Base potency increases by 60 at 3 stacks
        assert di.base_potency == 190

        attack_buff = next(
            (b for b in di.buffs_before if b.stat_type == StatType.ATTACK),
            None,
        )
        damage_buff = next(
            (
                b
                for b in di.buffs_before
                if b.stat_type == SpecialAttribute.DAMAGE_BOOST
            ),
            None,
        )
        crit_buff = next(
            (
                b
                for b in di.buffs_before
                if b.stat_type == SpecialAttribute.CRITICAL_DAMAGE
            ),
            None,
        )

        assert attack_buff is not None and attack_buff.value == 10
        assert damage_buff is not None and damage_buff.value == 40
        assert crit_buff is not None and crit_buff.value == 10

    def test_uses_damage_calculation_strategy(self):
        """Should use GeostationarySatelliteDamageCalculationStrategy."""
        skill = CallOfTheStars()
        di = skill.execute()

        assert isinstance(
            di.damage_calculation_strategy,
            GeostationarySatelliteDamageCalculationStrategy,
        )

    def test_correct_group_name(self):
        """Group name should match skill label."""
        skill = CallOfTheStars()
        di = skill.execute()

        assert di.group_name == "Call of the Stars (Geostationary Satellite)"


class TestGeostationarySatelliteSummon:
    """Tests for Geostationary Satellite summon functionality."""

    def test_summon_created_on_initialization(self):
        """Geostationary Satellite should be created when get_summoned_unit is called."""
        tololo = Tololo()
        summon = tololo.get_summoned_unit("Geostationary Satellite")

        assert summon is not None
        assert summon.name == "Geostationary Satellite"

    def test_summon_inherits_stats(self):
        """Geostationary Satellite should inherit all of Tololo's initial stats."""
        tololo = Tololo()
        tololo.initial_stats.basic_attributes[StatType.ATTACK] = 5000
        tololo.initial_stats.basic_attributes[StatType.CRIT_RATE] = 75
        tololo.initial_stats.basic_attributes[StatType.CRIT_DAMAGE] = 150

        summon = tololo.get_summoned_unit("Geostationary Satellite")
        assert summon is not None

        # Stats should be inherited at 100%
        assert summon.initial_stats.basic_attributes[StatType.ATTACK] == 5000
        assert summon.initial_stats.basic_attributes[StatType.CRIT_RATE] == 75
        assert summon.initial_stats.basic_attributes[StatType.CRIT_DAMAGE] == 150

    def test_summon_refresh_on_stat_change(self):
        """Refreshing summon should update its stats from Tololo."""
        tololo = Tololo()
        tololo.initial_stats.basic_attributes[StatType.ATTACK] = 1000
        tololo.summon_geostationary_satellite()

        summon1 = tololo.get_summoned_unit("Geostationary Satellite")
        assert summon1 is not None
        assert summon1.initial_stats.basic_attributes[StatType.ATTACK] == 1000

        # Change Tololo's stats and refresh
        tololo.initial_stats.basic_attributes[StatType.ATTACK] = 2000
        tololo.refresh_geostationary_satellite()

        summon2 = tololo.get_summoned_unit("Geostationary Satellite")
        assert summon2 is not None
        assert summon2.initial_stats.basic_attributes[StatType.ATTACK] == 2000

    def test_multiple_summon_calls_idempotent(self):
        """Multiple calls to get_summoned_unit should be idempotent."""
        tololo = Tololo()
        tololo.get_summoned_unit("Geostationary Satellite")
        tololo.get_summoned_unit("Geostationary Satellite")
        tololo.get_summoned_unit("Geostationary Satellite")

        satellites = [
            u for u in tololo.summoned_units if u.name == "Geostationary Satellite"
        ]
        assert len(satellites) == 1

    def test_prepare_for_calculation_refreshes_summon(self):
        """prepare_for_calculation should refresh the summon."""
        tololo = Tololo()
        tololo.initial_stats.basic_attributes[StatType.ATTACK] = 1000
        tololo.summon_geostationary_satellite()

        summon1 = tololo.get_summoned_unit("Geostationary Satellite")
        assert summon1.initial_stats.basic_attributes[StatType.ATTACK] == 1000

        tololo.initial_stats.basic_attributes[StatType.ATTACK] = 3000
        tololo.prepare_for_calculation()

        summon2 = tololo.get_summoned_unit("Geostationary Satellite")
        assert summon2.initial_stats.basic_attributes[StatType.ATTACK] == 3000

    def test_summon_exists_in_summoned_units_list(self):
        """Geostationary Satellite should be in the summoned_units list."""
        tololo = Tololo()
        tololo.get_summoned_unit("Geostationary Satellite")

        assert any(u.name == "Geostationary Satellite" for u in tololo.summoned_units)

    def test_summon_inherits_additive_modifiers(self):
        """Geostationary Satellite should inherit Tololo's additive modifiers."""
        tololo = Tololo()
        tololo.additive_modifiers.special_attributes[
            SpecialAttribute.DAMAGE_BOOST
        ].set_multiplier(DamageTag.PHYSICAL_SUMMON, 50)
        tololo.additive_modifiers.special_attributes[
            SpecialAttribute.DAMAGE_BOOST
        ].set_multiplier(DamageTag.ALL, 42)
        tololo.additive_modifiers.special_attributes[
            SpecialAttribute.DAMAGE_BOOST
        ].set_multiplier(DamageTag.HYDRO, 22)

        tololo.prepare_for_calculation()
        summon = tololo.get_summoned_unit("Geostationary Satellite")

        assert summon is not None
        # Check that the summon has the same modifier setup
        assert summon.additive_modifiers.special_attributes[
            SpecialAttribute.DAMAGE_BOOST
        ].get_multiplier(DamageTag.PHYSICAL_SUMMON) == pytest.approx(50, rel=1e-5)

        # Check that the summon did not inherit non-PHYSICAL_SUMMON modifiers
        assert summon.additive_modifiers.special_attributes[
            SpecialAttribute.DAMAGE_BOOST
        ].get_multiplier(DamageTag.ALL) == pytest.approx(0, rel=1e-5)


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

    def test_summon_available_at_all_fortification_levels(self):
        """Geostationary Satellite should be available at all fortification levels."""
        for level in FortificationLevel:
            tololo = Tololo()
            tololo.set_fortification_level(level)
            summon = tololo.get_summoned_unit("Geostationary Satellite")
            assert summon is not None, f"Summon missing at {level}"
