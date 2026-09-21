from core.dolls.faelynn import *

from core.types import DamageTag, FortificationLevel


class TestFaelynnSkills:
    def test_cuspid_combo(self):
        result = CuspidCombo().execute()

        assert result.base_potency == 80
        assert result.tags == {
            DamageTag.ACTIVE,
            DamageTag.BASIC,
            DamageTag.MEDIUM_AMMO,
            DamageTag.TARGETED,
            DamageTag.PHYSICAL,
        }
        assert result.group_name == "Cuspid Combo"

    def test_triple_maule(self):
        result = TripleMaule().execute(stacks_of_hunters_tracking=0)

        assert result.base_potency == 60
        assert result.label == "Triple Maule (0)"
        assert result.tags == {
            DamageTag.ACTIVE,
            DamageTag.CORROSION,
            DamageTag.PHASE,
            DamageTag.MEDIUM_AMMO,
            DamageTag.AREA_OF_EFFECT,
        }
        assert result.group_name == "Triple Maule"

    def test_triple_maule_scales_with_hunters_tracking(self):
        result = TripleMaule().execute(stacks_of_hunters_tracking=3)

        assert result.base_potency == 75

    def test_triple_maule_ignores_negative_stacks(self):
        result = TripleMaule().execute(stacks_of_hunters_tracking=-2)

        assert result.base_potency == 60

    def test_triple_maule_v2_scales_with_hunters_tracking(self):
        result = TripleMauleV2().execute(stacks_of_hunters_tracking=3)

        assert result.base_potency == 90

    def test_triple_maule_v5_base(self):
        result = TripleMauleV5().execute(stacks_of_hunters_tracking=0)

        assert result.base_potency == 120

    def test_triple_maule_v5_scales_with_hunters_tracking(self):
        result = TripleMauleV5().execute(stacks_of_hunters_tracking=3)

        assert result.base_potency == 150

    def test_triple_maule_followup_base(self):
        result = TripleMauleFollowup().execute(
            number_of_targets_hit=1, boss_was_hit=False
        )

        assert result.base_potency == 0
        assert result.tags == {
            DamageTag.ACTIVE,
            DamageTag.CORROSION,
            DamageTag.PHASE,
            DamageTag.AREA_OF_EFFECT,
        }
        assert result.group_name == "Triple Maule"

    def test_triple_maule_followup_v5_no_conditions_met(self):
        result = TripleMauleFollowupV5().execute(
            number_of_targets_hit=1, boss_was_hit=False
        )

        assert result.base_potency == 0

    def test_triple_maule_followup_v5_with_many_targets(self):
        result = TripleMauleFollowupV5().execute(
            number_of_targets_hit=4, boss_was_hit=False
        )

        assert result.base_potency == 120

    def test_triple_maule_followup_v5_with_boss_hit(self):
        result = TripleMauleFollowupV5().execute(
            number_of_targets_hit=1, boss_was_hit=True
        )

        assert result.base_potency == 120

    def test_scent_mark(self):
        result = ScentMarkAction().execute()

        assert result.base_potency == 60
        assert result.tags == {
            DamageTag.PASSIVE,
            DamageTag.CORROSION,
            DamageTag.PHASE,
            DamageTag.AREA_OF_EFFECT,
        }
        assert result.group_name == "Scent Mark"

    def test_scent_mark_v2(self):
        result = ScentMarkActionV2().execute()

        assert result.base_potency == 100

    def test_loyal_hunt(self):
        result = LoyalHunt().execute(stacks_of_hunters_tracking=0)

        assert result.base_potency == 120
        assert result.label == "Loyal Hunt (0)"
        assert result.tags == {
            DamageTag.ACTIVE,
            DamageTag.CORROSION,
            DamageTag.PHASE,
            DamageTag.AREA_OF_EFFECT,
            DamageTag.ULTIMATE,
            DamageTag.CONFECTANCE,
        }
        assert result.group_name == "Loyal Hunt"

    def test_loyal_hunt_scales_with_hunters_tracking(self):
        result = LoyalHunt().execute(stacks_of_hunters_tracking=3)

        assert result.base_potency == 135

    def test_loyal_hunt_v3_scales_with_hunters_tracking(self):
        result = LoyalHuntV3().execute(stacks_of_hunters_tracking=3)

        assert result.base_potency == 150

    def test_loyal_hunt_v6_base(self):
        result = LoyalHuntV6().execute(stacks_of_hunters_tracking=0)

        assert result.base_potency == 150

    def test_loyal_hunt_v6_scales_with_hunters_tracking(self):
        result = LoyalHuntV6().execute(stacks_of_hunters_tracking=3)

        assert result.base_potency == 180

    def test_hunters_instinct_i(self):
        result = HuntersInstinctI().execute(
            stacks_of_hunters_tracking=0, number_of_targets_hit=2
        )

        assert result.base_potency == 60
        assert result.tags == {
            DamageTag.ACTIVE,
            DamageTag.CORROSION,
            DamageTag.PHASE,
            DamageTag.AREA_OF_EFFECT,
        }
        assert result.group_name == "Hunter's Instinct I"

    def test_hunters_instinct_i_scales_with_hunters_tracking(self):
        result = HuntersInstinctI().execute(
            stacks_of_hunters_tracking=3, number_of_targets_hit=2
        )

        assert result.base_potency == 75

    def test_hunters_instinct_i_single_target_bonus(self):
        result = HuntersInstinctI().execute(
            stacks_of_hunters_tracking=0, number_of_targets_hit=1
        )

        assert result.base_potency == 90

    def test_hunters_instinct_i_v3_scales_with_hunters_tracking(self):
        result = HuntersInstinctIV3().execute(
            stacks_of_hunters_tracking=3, number_of_targets_hit=2
        )

        assert result.base_potency == 90

    def test_hunters_instinct_i_v6_base(self):
        result = HuntersInstinctIV6().execute(
            stacks_of_hunters_tracking=0, number_of_targets_hit=2
        )

        assert result.base_potency == 90

    def test_hunters_instinct_ii(self):
        result = HuntersInstinctII().execute(
            stacks_of_hunters_tracking=0,
            number_of_targets_hit=2,
            has_collar_brand=False,
        )

        assert result.base_potency == 120
        assert result.buffs_before == []
        assert result.group_name == "Hunter's Instinct II"

    def test_hunters_instinct_ii_with_collar_brand(self):
        result = HuntersInstinctII().execute(
            stacks_of_hunters_tracking=0, number_of_targets_hit=2, has_collar_brand=True
        )

        assert result.buffs_before == [
            Buff(
                50,
                ModifierType.ADDITIVE,
                SpecialAttribute.DAMAGE_BOOST,
                DamageTag.ALL,
            )
        ]

    def test_hunters_instinct_ii_single_target_bonus(self):
        result = HuntersInstinctII().execute(
            stacks_of_hunters_tracking=0,
            number_of_targets_hit=1,
            has_collar_brand=False,
        )

        assert result.base_potency == 150

    def test_hunters_instinct_ii_v3_scales_with_hunters_tracking(self):
        result = HuntersInstinctIIV3().execute(
            stacks_of_hunters_tracking=3,
            number_of_targets_hit=2,
            has_collar_brand=False,
        )

        assert result.base_potency == 150

    def test_hunters_instinct_ii_v6_base(self):
        result = HuntersInstinctIIV6().execute(
            stacks_of_hunters_tracking=0,
            number_of_targets_hit=2,
            has_collar_brand=False,
        )

        assert result.base_potency == 170

    def test_hunters_instinct_iii(self):
        result = HuntersInstinctIII().execute(
            stacks_of_hunters_tracking=0,
            number_of_targets_hit=2,
            has_collar_brand=False,
            target_tile_ascension_level=0,
        )

        assert result.base_potency == 240
        assert result.group_name == "Hunter's Instinct III"
        assert result.buffs_before == []
        assert result.debuffs_before == []

    def test_hunters_instinct_iii_with_collar_brand(self):
        result = HuntersInstinctIII().execute(
            stacks_of_hunters_tracking=0,
            number_of_targets_hit=2,
            has_collar_brand=True,
            target_tile_ascension_level=0,
        )

        assert result.buffs_before == [
            Buff(
                100,
                ModifierType.ADDITIVE,
                SpecialAttribute.DAMAGE_BOOST,
                DamageTag.ALL,
            )
        ]

    def test_hunters_instinct_iii_with_target_tile_ascension_level(self):
        result = HuntersInstinctIII().execute(
            stacks_of_hunters_tracking=0,
            number_of_targets_hit=2,
            has_collar_brand=False,
            target_tile_ascension_level=2,
        )

        assert result.buffs_before == [
            Buff(
                10,
                ModifierType.ADDITIVE,
                SpecialAttribute.CRITICAL_DAMAGE,
                DamageTag.ALL,
            )
        ]
        assert result.debuffs_before == [
            Debuff(
                -28,
                ModifierType.MULTIPLICATIVE,
                StatType.DEFENSE,
                DamageTag.ALL,
            )
        ]

    def test_hunters_instinct_iii_with_collar_brand_and_target_tile_ascension_level(self):
        result = HuntersInstinctIII().execute(
            stacks_of_hunters_tracking=0,
            number_of_targets_hit=2,
            has_collar_brand=True,
            target_tile_ascension_level=2,
        )

        assert result.buffs_before == [
            Buff(
                100,
                ModifierType.ADDITIVE,
                SpecialAttribute.DAMAGE_BOOST,
                DamageTag.ALL,
            ),
            Buff(
                10,
                ModifierType.ADDITIVE,
                SpecialAttribute.CRITICAL_DAMAGE,
                DamageTag.ALL,
            ),
        ]

    def test_hunters_instinct_iii_target_tile_ascension_level_caps_at_three(self):
        at_cap = HuntersInstinctIII().execute(
            stacks_of_hunters_tracking=0,
            number_of_targets_hit=2,
            has_collar_brand=False,
            target_tile_ascension_level=MAX_TILE_ASCENSION_LEVEL,
        )
        over_cap = HuntersInstinctIII().execute(
            stacks_of_hunters_tracking=0,
            number_of_targets_hit=2,
            has_collar_brand=False,
            target_tile_ascension_level=MAX_TILE_ASCENSION_LEVEL + 5,
        )

        assert at_cap.buffs_before == [
            Buff(
                15,
                ModifierType.ADDITIVE,
                SpecialAttribute.CRITICAL_DAMAGE,
                DamageTag.ALL,
            )
        ]
        assert at_cap.debuffs_before == [
            Debuff(
                -42,
                ModifierType.MULTIPLICATIVE,
                StatType.DEFENSE,
                DamageTag.ALL,
            )
        ]
        assert over_cap.buffs_before == at_cap.buffs_before
        assert over_cap.debuffs_before == at_cap.debuffs_before

    def test_hunters_instinct_iii_ignores_non_positive_target_tile_ascension_level(self):
        result = HuntersInstinctIII().execute(
            stacks_of_hunters_tracking=0,
            number_of_targets_hit=2,
            has_collar_brand=False,
            target_tile_ascension_level=-1,
        )

        assert result.buffs_before == []
        assert result.debuffs_before == []

    def test_hunters_instinct_iii_v3_scales_with_hunters_tracking(self):
        result = HuntersInstinctIIIV3().execute(
            stacks_of_hunters_tracking=3,
            number_of_targets_hit=2,
            has_collar_brand=False,
            target_tile_ascension_level=0,
        )

        assert result.base_potency == 270

    def test_hunters_instinct_iii_v3_with_target_tile_ascension_level(self):
        result = HuntersInstinctIIIV3().execute(
            stacks_of_hunters_tracking=0,
            number_of_targets_hit=2,
            has_collar_brand=False,
            target_tile_ascension_level=MAX_TILE_ASCENSION_LEVEL,
        )

        assert result.buffs_before == [
            Buff(
                15,
                ModifierType.ADDITIVE,
                SpecialAttribute.CRITICAL_DAMAGE,
                DamageTag.ALL,
            )
        ]
        assert result.debuffs_before == [
            Debuff(
                -42,
                ModifierType.MULTIPLICATIVE,
                StatType.DEFENSE,
                DamageTag.ALL,
            )
        ]

    def test_hunters_instinct_iii_v4_with_target_tile_ascension_level(self):
        result = HuntersInstinctIIIV4().execute(
            stacks_of_hunters_tracking=0,
            number_of_targets_hit=2,
            has_collar_brand=False,
            target_tile_ascension_level=MAX_TILE_ASCENSION_LEVEL,
        )

        assert result.buffs_before == [
            Buff(
                15,
                ModifierType.ADDITIVE,
                SpecialAttribute.CRITICAL_DAMAGE,
                DamageTag.ALL,
            )
        ]
        assert result.debuffs_before == [
            Debuff(
                -42,
                ModifierType.MULTIPLICATIVE,
                StatType.DEFENSE,
                DamageTag.ALL,
            )
        ]

    def test_hunters_instinct_iii_v6_base(self):
        result = HuntersInstinctIIIV6().execute(
            stacks_of_hunters_tracking=0,
            number_of_targets_hit=2,
            has_collar_brand=False,
            target_tile_ascension_level=0,
        )

        assert result.base_potency == 480

    def test_hunters_instinct_iii_v6_with_target_tile_ascension_level(self):
        result = HuntersInstinctIIIV6().execute(
            stacks_of_hunters_tracking=0,
            number_of_targets_hit=2,
            has_collar_brand=False,
            target_tile_ascension_level=MAX_TILE_ASCENSION_LEVEL,
        )

        assert result.buffs_before == [
            Buff(
                15,
                ModifierType.ADDITIVE,
                SpecialAttribute.CRITICAL_DAMAGE,
                DamageTag.ALL,
            )
        ]
        assert result.debuffs_before == [
            Debuff(
                -42,
                ModifierType.MULTIPLICATIVE,
                StatType.DEFENSE,
                DamageTag.ALL,
            )
        ]


class TestFaelynnHuntersTrackingStackCap:
    """Below Fortification Level V4, stacks of Hunter's Tracking are capped at 3. At V4+, the cap is 6."""

    def test_triple_maule_caps_at_three_below_v4(self):
        at_cap = TripleMaule().execute(stacks_of_hunters_tracking=HUNTERS_TRACKING_STACK_MAXIMUM)
        over_cap = TripleMaule().execute(stacks_of_hunters_tracking=HUNTERS_TRACKING_STACK_MAXIMUM + 5)

        assert at_cap.base_potency == 75
        assert over_cap.base_potency == at_cap.base_potency

    def test_triple_maule_v2_caps_at_three(self):
        at_cap = TripleMauleV2().execute(stacks_of_hunters_tracking=HUNTERS_TRACKING_STACK_MAXIMUM)
        over_cap = TripleMauleV2().execute(stacks_of_hunters_tracking=HUNTERS_TRACKING_STACK_MAXIMUM + 5)

        assert at_cap.base_potency == 90
        assert over_cap.base_potency == at_cap.base_potency

    def test_triple_maule_v4_caps_at_six(self):
        at_cap = TripleMauleV4().execute(stacks_of_hunters_tracking=HUNTERS_TRACKING_STACK_MAXIMUM_V4)
        over_cap = TripleMauleV4().execute(stacks_of_hunters_tracking=HUNTERS_TRACKING_STACK_MAXIMUM_V4 + 5)

        assert at_cap.base_potency == 120
        assert over_cap.base_potency == at_cap.base_potency

    def test_triple_maule_v5_caps_at_six(self):
        at_cap = TripleMauleV5().execute(stacks_of_hunters_tracking=HUNTERS_TRACKING_STACK_MAXIMUM_V4)
        over_cap = TripleMauleV5().execute(stacks_of_hunters_tracking=HUNTERS_TRACKING_STACK_MAXIMUM_V4 + 5)

        assert at_cap.base_potency == 180
        assert over_cap.base_potency == at_cap.base_potency

    def test_loyal_hunt_caps_at_three(self):
        at_cap = LoyalHunt().execute(stacks_of_hunters_tracking=HUNTERS_TRACKING_STACK_MAXIMUM)
        over_cap = LoyalHunt().execute(stacks_of_hunters_tracking=HUNTERS_TRACKING_STACK_MAXIMUM + 5)

        assert at_cap.base_potency == 135
        assert over_cap.base_potency == at_cap.base_potency

    def test_loyal_hunt_v3_caps_at_three(self):
        at_cap = LoyalHuntV3().execute(stacks_of_hunters_tracking=HUNTERS_TRACKING_STACK_MAXIMUM)
        over_cap = LoyalHuntV3().execute(stacks_of_hunters_tracking=HUNTERS_TRACKING_STACK_MAXIMUM + 5)

        assert at_cap.base_potency == 150
        assert over_cap.base_potency == at_cap.base_potency

    def test_loyal_hunt_v4_caps_at_six(self):
        at_cap = LoyalHuntV4().execute(stacks_of_hunters_tracking=HUNTERS_TRACKING_STACK_MAXIMUM_V4)
        over_cap = LoyalHuntV4().execute(stacks_of_hunters_tracking=HUNTERS_TRACKING_STACK_MAXIMUM_V4 + 5)

        assert at_cap.base_potency == 180
        assert over_cap.base_potency == at_cap.base_potency

    def test_loyal_hunt_v6_caps_at_six(self):
        at_cap = LoyalHuntV6().execute(stacks_of_hunters_tracking=HUNTERS_TRACKING_STACK_MAXIMUM_V4)
        over_cap = LoyalHuntV6().execute(stacks_of_hunters_tracking=HUNTERS_TRACKING_STACK_MAXIMUM_V4 + 5)

        assert at_cap.base_potency == 210
        assert over_cap.base_potency == at_cap.base_potency

    def test_hunters_instinct_i_caps_at_three(self):
        at_cap = HuntersInstinctI().execute(
            stacks_of_hunters_tracking=HUNTERS_TRACKING_STACK_MAXIMUM, number_of_targets_hit=2
        )
        over_cap = HuntersInstinctI().execute(
            stacks_of_hunters_tracking=HUNTERS_TRACKING_STACK_MAXIMUM + 5, number_of_targets_hit=2
        )

        assert at_cap.base_potency == 75
        assert over_cap.base_potency == at_cap.base_potency

    def test_hunters_instinct_i_v3_caps_at_three(self):
        at_cap = HuntersInstinctIV3().execute(
            stacks_of_hunters_tracking=HUNTERS_TRACKING_STACK_MAXIMUM, number_of_targets_hit=2
        )
        over_cap = HuntersInstinctIV3().execute(
            stacks_of_hunters_tracking=HUNTERS_TRACKING_STACK_MAXIMUM + 5, number_of_targets_hit=2
        )

        assert at_cap.base_potency == 90
        assert over_cap.base_potency == at_cap.base_potency

    def test_hunters_instinct_i_v4_caps_at_six(self):
        at_cap = HuntersInstinctIV4().execute(
            stacks_of_hunters_tracking=HUNTERS_TRACKING_STACK_MAXIMUM_V4, number_of_targets_hit=2
        )
        over_cap = HuntersInstinctIV4().execute(
            stacks_of_hunters_tracking=HUNTERS_TRACKING_STACK_MAXIMUM_V4 + 5, number_of_targets_hit=2
        )

        assert at_cap.base_potency == 120
        assert over_cap.base_potency == at_cap.base_potency

    def test_hunters_instinct_i_v6_caps_at_six(self):
        at_cap = HuntersInstinctIV6().execute(
            stacks_of_hunters_tracking=HUNTERS_TRACKING_STACK_MAXIMUM_V4, number_of_targets_hit=2
        )
        over_cap = HuntersInstinctIV6().execute(
            stacks_of_hunters_tracking=HUNTERS_TRACKING_STACK_MAXIMUM_V4 + 5, number_of_targets_hit=2
        )

        assert at_cap.base_potency == 150
        assert over_cap.base_potency == at_cap.base_potency

    def test_hunters_instinct_ii_caps_at_three(self):
        at_cap = HuntersInstinctII().execute(
            stacks_of_hunters_tracking=HUNTERS_TRACKING_STACK_MAXIMUM,
            number_of_targets_hit=2,
            has_collar_brand=False,
        )
        over_cap = HuntersInstinctII().execute(
            stacks_of_hunters_tracking=HUNTERS_TRACKING_STACK_MAXIMUM + 5,
            number_of_targets_hit=2,
            has_collar_brand=False,
        )

        assert at_cap.base_potency == 135
        assert over_cap.base_potency == at_cap.base_potency

    def test_hunters_instinct_ii_v3_caps_at_three(self):
        at_cap = HuntersInstinctIIV3().execute(
            stacks_of_hunters_tracking=HUNTERS_TRACKING_STACK_MAXIMUM,
            number_of_targets_hit=2,
            has_collar_brand=False,
        )
        over_cap = HuntersInstinctIIV3().execute(
            stacks_of_hunters_tracking=HUNTERS_TRACKING_STACK_MAXIMUM + 5,
            number_of_targets_hit=2,
            has_collar_brand=False,
        )

        assert at_cap.base_potency == 150
        assert over_cap.base_potency == at_cap.base_potency

    def test_hunters_instinct_ii_v4_caps_at_six(self):
        at_cap = HuntersInstinctIIV4().execute(
            stacks_of_hunters_tracking=HUNTERS_TRACKING_STACK_MAXIMUM_V4,
            number_of_targets_hit=2,
            has_collar_brand=False,
        )
        over_cap = HuntersInstinctIIV4().execute(
            stacks_of_hunters_tracking=HUNTERS_TRACKING_STACK_MAXIMUM_V4 + 5,
            number_of_targets_hit=2,
            has_collar_brand=False,
        )

        assert at_cap.base_potency == 180
        assert over_cap.base_potency == at_cap.base_potency

    def test_hunters_instinct_ii_v6_caps_at_six(self):
        at_cap = HuntersInstinctIIV6().execute(
            stacks_of_hunters_tracking=HUNTERS_TRACKING_STACK_MAXIMUM_V4,
            number_of_targets_hit=2,
            has_collar_brand=False,
        )
        over_cap = HuntersInstinctIIV6().execute(
            stacks_of_hunters_tracking=HUNTERS_TRACKING_STACK_MAXIMUM_V4 + 5,
            number_of_targets_hit=2,
            has_collar_brand=False,
        )

        assert at_cap.base_potency == 230
        assert over_cap.base_potency == at_cap.base_potency

    def test_hunters_instinct_iii_caps_at_three(self):
        at_cap = HuntersInstinctIII().execute(
            stacks_of_hunters_tracking=HUNTERS_TRACKING_STACK_MAXIMUM,
            number_of_targets_hit=2,
            has_collar_brand=False,
            target_tile_ascension_level=0,
        )
        over_cap = HuntersInstinctIII().execute(
            stacks_of_hunters_tracking=HUNTERS_TRACKING_STACK_MAXIMUM + 5,
            number_of_targets_hit=2,
            has_collar_brand=False,
            target_tile_ascension_level=0,
        )

        assert at_cap.base_potency == 255
        assert over_cap.base_potency == at_cap.base_potency

    def test_hunters_instinct_iii_v3_caps_at_three(self):
        at_cap = HuntersInstinctIIIV3().execute(
            stacks_of_hunters_tracking=HUNTERS_TRACKING_STACK_MAXIMUM,
            number_of_targets_hit=2,
            has_collar_brand=False,
            target_tile_ascension_level=0,
        )
        over_cap = HuntersInstinctIIIV3().execute(
            stacks_of_hunters_tracking=HUNTERS_TRACKING_STACK_MAXIMUM + 5,
            number_of_targets_hit=2,
            has_collar_brand=False,
            target_tile_ascension_level=0,
        )

        assert at_cap.base_potency == 270
        assert over_cap.base_potency == at_cap.base_potency

    def test_hunters_instinct_iii_v4_caps_at_six(self):
        at_cap = HuntersInstinctIIIV4().execute(
            stacks_of_hunters_tracking=HUNTERS_TRACKING_STACK_MAXIMUM_V4,
            number_of_targets_hit=2,
            has_collar_brand=False,
            target_tile_ascension_level=0,
        )
        over_cap = HuntersInstinctIIIV4().execute(
            stacks_of_hunters_tracking=HUNTERS_TRACKING_STACK_MAXIMUM_V4 + 5,
            number_of_targets_hit=2,
            has_collar_brand=False,
            target_tile_ascension_level=0,
        )

        assert at_cap.base_potency == 300
        assert over_cap.base_potency == at_cap.base_potency

    def test_hunters_instinct_iii_v6_caps_at_six(self):
        at_cap = HuntersInstinctIIIV6().execute(
            stacks_of_hunters_tracking=HUNTERS_TRACKING_STACK_MAXIMUM_V4,
            number_of_targets_hit=2,
            has_collar_brand=False,
            target_tile_ascension_level=0,
        )
        over_cap = HuntersInstinctIIIV6().execute(
            stacks_of_hunters_tracking=HUNTERS_TRACKING_STACK_MAXIMUM_V4 + 5,
            number_of_targets_hit=2,
            has_collar_brand=False,
            target_tile_ascension_level=0,
        )

        assert at_cap.base_potency == 540
        assert over_cap.base_potency == at_cap.base_potency


class TestFaelynn:
    def test_set_to_v0(self):
        doll = Faelynn()
        doll.set_to_v0()

        assert isinstance(doll.cuspid_combo, CuspidCombo)
        assert isinstance(doll.triple_maule, TripleMaule)
        assert isinstance(doll.triple_maule_followup, TripleMauleFollowup)
        assert isinstance(doll.scent_mark, ScentMarkAction)
        assert isinstance(doll.loyal_hunt, LoyalHunt)
        assert isinstance(doll.hunters_instinct_i, HuntersInstinctI)
        assert isinstance(doll.hunters_instinct_ii, HuntersInstinctII)
        assert isinstance(doll.hunters_instinct_iii, HuntersInstinctIII)

    def test_set_to_v2(self):
        doll = Faelynn()
        doll.set_to_v2()

        assert isinstance(doll.triple_maule, TripleMauleV2)
        assert isinstance(doll.scent_mark, ScentMarkActionV2)

    def test_set_to_v3(self):
        doll = Faelynn()
        doll.set_to_v3()

        assert isinstance(doll.loyal_hunt, LoyalHuntV3)
        assert isinstance(doll.hunters_instinct_i, HuntersInstinctIV3)
        assert isinstance(doll.hunters_instinct_ii, HuntersInstinctIIV3)
        assert isinstance(doll.hunters_instinct_iii, HuntersInstinctIIIV3)

    def test_set_to_v4(self):
        doll = Faelynn()
        doll.set_to_v4()

        assert isinstance(doll.triple_maule, TripleMauleV4)
        assert isinstance(doll.loyal_hunt, LoyalHuntV4)
        assert isinstance(doll.hunters_instinct_i, HuntersInstinctIV4)
        assert isinstance(doll.hunters_instinct_ii, HuntersInstinctIIV4)
        assert isinstance(doll.hunters_instinct_iii, HuntersInstinctIIIV4)

    def test_set_to_v5(self):
        doll = Faelynn()
        doll.set_to_v5()

        assert isinstance(doll.triple_maule, TripleMauleV5)
        assert isinstance(doll.triple_maule_followup, TripleMauleFollowupV5)

    def test_set_to_v6(self):
        doll = Faelynn()
        doll.set_to_v6()

        assert isinstance(doll.loyal_hunt, LoyalHuntV6)
        assert isinstance(doll.hunters_instinct_i, HuntersInstinctIV6)
        assert isinstance(doll.hunters_instinct_ii, HuntersInstinctIIV6)
        assert isinstance(doll.hunters_instinct_iii, HuntersInstinctIIIV6)

    def test_set_fortification_level(self):
        doll = Faelynn()

        doll.set_fortification_level(FortificationLevel.SEGMENT00)
        assert isinstance(doll.triple_maule, TripleMaule)

        doll.set_fortification_level(FortificationLevel.SEGMENT01)
        assert isinstance(doll.triple_maule, TripleMaule)

        doll.set_fortification_level(FortificationLevel.SEGMENT02)
        assert isinstance(doll.triple_maule, TripleMauleV2)
        assert isinstance(doll.scent_mark, ScentMarkActionV2)

        doll.set_fortification_level(FortificationLevel.SEGMENT03)
        assert isinstance(doll.loyal_hunt, LoyalHuntV3)
        assert isinstance(doll.hunters_instinct_iii, HuntersInstinctIIIV3)

        doll.set_fortification_level(FortificationLevel.SEGMENT04)
        assert isinstance(doll.triple_maule, TripleMauleV4)
        assert isinstance(doll.loyal_hunt, LoyalHuntV4)
        assert isinstance(doll.hunters_instinct_i, HuntersInstinctIV4)
        assert isinstance(doll.hunters_instinct_ii, HuntersInstinctIIV4)
        assert isinstance(doll.hunters_instinct_iii, HuntersInstinctIIIV4)

        doll.set_fortification_level(FortificationLevel.SEGMENT05)
        assert isinstance(doll.triple_maule, TripleMauleV5)
        assert isinstance(doll.triple_maule_followup, TripleMauleFollowupV5)

        doll.set_fortification_level(FortificationLevel.SEGMENT06)
        assert isinstance(doll.loyal_hunt, LoyalHuntV6)
        assert isinstance(doll.hunters_instinct_i, HuntersInstinctIV6)
        assert isinstance(doll.hunters_instinct_ii, HuntersInstinctIIV6)
        assert isinstance(doll.hunters_instinct_iii, HuntersInstinctIIIV6)
