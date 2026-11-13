from core.dolls.faelynn import *

from core.types import DamageTag, FortificationLevel


class TestFaelynnSkills:
    def test_burst_fang(self):
        result = BurstFang().execute()

        assert result.base_potency == 80
        assert result.tags == {
            DamageTag.ACTIVE,
            DamageTag.BASIC,
            DamageTag.MEDIUM_AMMO,
            DamageTag.TARGETED,
            DamageTag.PHYSICAL,
        }
        assert result.group_name == "Burst Fang"

    def test_triple_maul(self):
        result = TripleMaul().execute(stacks_of_hunt_tracking=0)

        assert result.base_potency == 60
        assert result.label == "Triple Maul (0)"
        assert result.tags == {
            DamageTag.ACTIVE,
            DamageTag.CORROSION,
            DamageTag.PHASE,
            DamageTag.MEDIUM_AMMO,
            DamageTag.AREA_OF_EFFECT,
        }
        assert result.group_name == "Triple Maul"

    def test_triple_maul_scales_with_hunt_tracking(self):
        result = TripleMaul().execute(stacks_of_hunt_tracking=3)

        assert result.base_potency == 75

    def test_triple_maul_ignores_negative_stacks(self):
        result = TripleMaul().execute(stacks_of_hunt_tracking=-2)

        assert result.base_potency == 60

    def test_triple_maul_v2_scales_with_hunt_tracking(self):
        result = TripleMaulV2().execute(stacks_of_hunt_tracking=3)

        assert result.base_potency == 90

    def test_triple_maul_v5_base(self):
        result = TripleMaulV5().execute(stacks_of_hunt_tracking=0)

        assert result.base_potency == 120

    def test_triple_maul_v5_scales_with_hunt_tracking(self):
        result = TripleMaulV5().execute(stacks_of_hunt_tracking=3)

        assert result.base_potency == 150

    def test_triple_maul_followup_base(self):
        result = TripleMaulFollowup().execute(
            number_of_targets_hit=1, boss_was_hit=False
        )

        assert result.base_potency == 0
        assert result.tags == {
            DamageTag.ACTIVE,
            DamageTag.CORROSION,
            DamageTag.PHASE,
            DamageTag.AREA_OF_EFFECT,
        }
        assert result.group_name == "Triple Maul"

    def test_triple_maul_followup_v5_no_conditions_met(self):
        result = TripleMaulFollowupV5().execute(
            number_of_targets_hit=1, boss_was_hit=False
        )

        assert result.base_potency == 0

    def test_triple_maul_followup_v5_with_many_targets(self):
        result = TripleMaulFollowupV5().execute(
            number_of_targets_hit=4, boss_was_hit=False
        )

        assert result.base_potency == 120

    def test_triple_maul_followup_v5_with_boss_hit(self):
        result = TripleMaulFollowupV5().execute(
            number_of_targets_hit=1, boss_was_hit=True
        )

        assert result.base_potency == 120

    def test_scent_trail(self):
        result = ScentTrailAction().execute()

        assert result.base_potency == 60
        assert result.tags == {
            DamageTag.PASSIVE,
            DamageTag.CORROSION,
            DamageTag.PHASE,
            DamageTag.AREA_OF_EFFECT,
        }
        assert result.group_name == "Scent Trail"

    def test_scent_trail_v2(self):
        result = ScentTrailActionV2().execute()

        assert result.base_potency == 100

    def test_loyal_dash(self):
        result = LoyalDash().execute(stacks_of_hunt_tracking=0)

        assert result.base_potency == 120
        assert result.label == "Loyal Dash (0)"
        assert result.tags == {
            DamageTag.ACTIVE,
            DamageTag.CORROSION,
            DamageTag.PHASE,
            DamageTag.AREA_OF_EFFECT,
            DamageTag.ULTIMATE,
            DamageTag.CONFECTANCE,
        }
        assert result.group_name == "Loyal Dash"

    def test_loyal_dash_scales_with_hunt_tracking(self):
        result = LoyalDash().execute(stacks_of_hunt_tracking=3)

        assert result.base_potency == 135

    def test_loyal_dash_v3_scales_with_hunt_tracking(self):
        result = LoyalDashV3().execute(stacks_of_hunt_tracking=3)

        assert result.base_potency == 150

    def test_loyal_dash_v6_base(self):
        result = LoyalDashV6().execute(stacks_of_hunt_tracking=0)

        assert result.base_potency == 150

    def test_loyal_dash_v6_scales_with_hunt_tracking(self):
        result = LoyalDashV6().execute(stacks_of_hunt_tracking=3)

        assert result.base_potency == 180

    def test_pursuit_instinct_i(self):
        result = PursuitInstinctI().execute(
            stacks_of_hunt_tracking=0, number_of_targets_hit=2
        )

        assert result.base_potency == 60
        assert result.tags == {
            DamageTag.ACTIVE,
            DamageTag.CORROSION,
            DamageTag.PHASE,
            DamageTag.AREA_OF_EFFECT,
        }
        assert result.group_name == "Pursuit Instinct I"

    def test_pursuit_instinct_i_scales_with_hunt_tracking(self):
        result = PursuitInstinctI().execute(
            stacks_of_hunt_tracking=3, number_of_targets_hit=2
        )

        assert result.base_potency == 75

    def test_pursuit_instinct_i_single_target_bonus(self):
        result = PursuitInstinctI().execute(
            stacks_of_hunt_tracking=0, number_of_targets_hit=1
        )

        assert result.base_potency == 90

    def test_pursuit_instinct_i_v3_scales_with_hunt_tracking(self):
        result = PursuitInstinctIV3().execute(
            stacks_of_hunt_tracking=3, number_of_targets_hit=2
        )

        assert result.base_potency == 90

    def test_pursuit_instinct_i_v6_base(self):
        result = PursuitInstinctIV6().execute(
            stacks_of_hunt_tracking=0, number_of_targets_hit=2
        )

        assert result.base_potency == 90

    def test_pursuit_instinct_ii(self):
        result = PursuitInstinctII().execute(
            stacks_of_hunt_tracking=0,
            number_of_targets_hit=2,
            has_collar_brand=False,
        )

        assert result.base_potency == 120
        assert result.buffs_before == []
        assert result.group_name == "Pursuit Instinct II"

    def test_pursuit_instinct_ii_with_collar_brand(self):
        result = PursuitInstinctII().execute(
            stacks_of_hunt_tracking=0, number_of_targets_hit=2, has_collar_brand=True
        )

        assert result.buffs_before == [
            Buff(
                50,
                ModifierType.ADDITIVE,
                SpecialAttribute.DAMAGE_BOOST,
                DamageTag.ALL,
            )
        ]

    def test_pursuit_instinct_ii_single_target_bonus(self):
        result = PursuitInstinctII().execute(
            stacks_of_hunt_tracking=0,
            number_of_targets_hit=1,
            has_collar_brand=False,
        )

        assert result.base_potency == 150

    def test_pursuit_instinct_ii_v3_scales_with_hunt_tracking(self):
        result = PursuitInstinctIIV3().execute(
            stacks_of_hunt_tracking=3,
            number_of_targets_hit=2,
            has_collar_brand=False,
        )

        assert result.base_potency == 150

    def test_pursuit_instinct_ii_v6_base(self):
        result = PursuitInstinctIIV6().execute(
            stacks_of_hunt_tracking=0,
            number_of_targets_hit=2,
            has_collar_brand=False,
        )

        assert result.base_potency == 170

    def test_pursuit_instinct_iii(self):
        result = PursuitInstinctIII().execute(
            stacks_of_hunt_tracking=0,
            number_of_targets_hit=2,
            has_collar_brand=False,
            target_tile_ascension_level=0,
        )

        assert result.base_potency == 240
        assert result.group_name == "Pursuit Instinct III"
        assert result.buffs_before == []
        assert result.debuffs_before == []

    def test_pursuit_instinct_iii_with_collar_brand(self):
        result = PursuitInstinctIII().execute(
            stacks_of_hunt_tracking=0,
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

    def test_pursuit_instinct_iii_with_target_tile_ascension_level(self):
        result = PursuitInstinctIII().execute(
            stacks_of_hunt_tracking=0,
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

    def test_pursuit_instinct_iii_with_collar_brand_and_target_tile_ascension_level(self):
        result = PursuitInstinctIII().execute(
            stacks_of_hunt_tracking=0,
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

    def test_pursuit_instinct_iii_target_tile_ascension_level_caps_at_three(self):
        at_cap = PursuitInstinctIII().execute(
            stacks_of_hunt_tracking=0,
            number_of_targets_hit=2,
            has_collar_brand=False,
            target_tile_ascension_level=MAX_TILE_ASCENSION_LEVEL,
        )
        over_cap = PursuitInstinctIII().execute(
            stacks_of_hunt_tracking=0,
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

    def test_pursuit_instinct_iii_ignores_non_positive_target_tile_ascension_level(self):
        result = PursuitInstinctIII().execute(
            stacks_of_hunt_tracking=0,
            number_of_targets_hit=2,
            has_collar_brand=False,
            target_tile_ascension_level=-1,
        )

        assert result.buffs_before == []
        assert result.debuffs_before == []

    def test_pursuit_instinct_iii_v3_scales_with_hunt_tracking(self):
        result = PursuitInstinctIIIV3().execute(
            stacks_of_hunt_tracking=3,
            number_of_targets_hit=2,
            has_collar_brand=False,
            target_tile_ascension_level=0,
        )

        assert result.base_potency == 270

    def test_pursuit_instinct_iii_v3_with_target_tile_ascension_level(self):
        result = PursuitInstinctIIIV3().execute(
            stacks_of_hunt_tracking=0,
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

    def test_pursuit_instinct_iii_v4_with_target_tile_ascension_level(self):
        result = PursuitInstinctIIIV4().execute(
            stacks_of_hunt_tracking=0,
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

    def test_pursuit_instinct_iii_v6_base(self):
        result = PursuitInstinctIIIV6().execute(
            stacks_of_hunt_tracking=0,
            number_of_targets_hit=2,
            has_collar_brand=False,
            target_tile_ascension_level=0,
        )

        assert result.base_potency == 480

    def test_pursuit_instinct_iii_v6_with_target_tile_ascension_level(self):
        result = PursuitInstinctIIIV6().execute(
            stacks_of_hunt_tracking=0,
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


class TestFaelynnHuntTrackingStackCap:
    """Below Fortification Level V4, stacks of Hunt Tracking are capped at 3. At V4+, the cap is 6."""

    def test_triple_maul_caps_at_three_below_v4(self):
        at_cap = TripleMaul().execute(stacks_of_hunt_tracking=HUNT_TRACKING_STACK_MAXIMUM)
        over_cap = TripleMaul().execute(stacks_of_hunt_tracking=HUNT_TRACKING_STACK_MAXIMUM + 5)

        assert at_cap.base_potency == 75
        assert over_cap.base_potency == at_cap.base_potency

    def test_triple_maul_v2_caps_at_three(self):
        at_cap = TripleMaulV2().execute(stacks_of_hunt_tracking=HUNT_TRACKING_STACK_MAXIMUM)
        over_cap = TripleMaulV2().execute(stacks_of_hunt_tracking=HUNT_TRACKING_STACK_MAXIMUM + 5)

        assert at_cap.base_potency == 90
        assert over_cap.base_potency == at_cap.base_potency

    def test_triple_maul_v4_caps_at_six(self):
        at_cap = TripleMaulV4().execute(stacks_of_hunt_tracking=HUNT_TRACKING_STACK_MAXIMUM_V4)
        over_cap = TripleMaulV4().execute(stacks_of_hunt_tracking=HUNT_TRACKING_STACK_MAXIMUM_V4 + 5)

        assert at_cap.base_potency == 120
        assert over_cap.base_potency == at_cap.base_potency

    def test_triple_maul_v5_caps_at_six(self):
        at_cap = TripleMaulV5().execute(stacks_of_hunt_tracking=HUNT_TRACKING_STACK_MAXIMUM_V4)
        over_cap = TripleMaulV5().execute(stacks_of_hunt_tracking=HUNT_TRACKING_STACK_MAXIMUM_V4 + 5)

        assert at_cap.base_potency == 180
        assert over_cap.base_potency == at_cap.base_potency

    def test_loyal_dash_caps_at_three(self):
        at_cap = LoyalDash().execute(stacks_of_hunt_tracking=HUNT_TRACKING_STACK_MAXIMUM)
        over_cap = LoyalDash().execute(stacks_of_hunt_tracking=HUNT_TRACKING_STACK_MAXIMUM + 5)

        assert at_cap.base_potency == 135
        assert over_cap.base_potency == at_cap.base_potency

    def test_loyal_dash_v3_caps_at_three(self):
        at_cap = LoyalDashV3().execute(stacks_of_hunt_tracking=HUNT_TRACKING_STACK_MAXIMUM)
        over_cap = LoyalDashV3().execute(stacks_of_hunt_tracking=HUNT_TRACKING_STACK_MAXIMUM + 5)

        assert at_cap.base_potency == 150
        assert over_cap.base_potency == at_cap.base_potency

    def test_loyal_dash_v4_caps_at_six(self):
        at_cap = LoyalDashV4().execute(stacks_of_hunt_tracking=HUNT_TRACKING_STACK_MAXIMUM_V4)
        over_cap = LoyalDashV4().execute(stacks_of_hunt_tracking=HUNT_TRACKING_STACK_MAXIMUM_V4 + 5)

        assert at_cap.base_potency == 180
        assert over_cap.base_potency == at_cap.base_potency

    def test_loyal_dash_v6_caps_at_six(self):
        at_cap = LoyalDashV6().execute(stacks_of_hunt_tracking=HUNT_TRACKING_STACK_MAXIMUM_V4)
        over_cap = LoyalDashV6().execute(stacks_of_hunt_tracking=HUNT_TRACKING_STACK_MAXIMUM_V4 + 5)

        assert at_cap.base_potency == 210
        assert over_cap.base_potency == at_cap.base_potency

    def test_pursuit_instinct_i_caps_at_three(self):
        at_cap = PursuitInstinctI().execute(
            stacks_of_hunt_tracking=HUNT_TRACKING_STACK_MAXIMUM, number_of_targets_hit=2
        )
        over_cap = PursuitInstinctI().execute(
            stacks_of_hunt_tracking=HUNT_TRACKING_STACK_MAXIMUM + 5, number_of_targets_hit=2
        )

        assert at_cap.base_potency == 75
        assert over_cap.base_potency == at_cap.base_potency

    def test_pursuit_instinct_i_v3_caps_at_three(self):
        at_cap = PursuitInstinctIV3().execute(
            stacks_of_hunt_tracking=HUNT_TRACKING_STACK_MAXIMUM, number_of_targets_hit=2
        )
        over_cap = PursuitInstinctIV3().execute(
            stacks_of_hunt_tracking=HUNT_TRACKING_STACK_MAXIMUM + 5, number_of_targets_hit=2
        )

        assert at_cap.base_potency == 90
        assert over_cap.base_potency == at_cap.base_potency

    def test_pursuit_instinct_i_v4_caps_at_six(self):
        at_cap = PursuitInstinctIV4().execute(
            stacks_of_hunt_tracking=HUNT_TRACKING_STACK_MAXIMUM_V4, number_of_targets_hit=2
        )
        over_cap = PursuitInstinctIV4().execute(
            stacks_of_hunt_tracking=HUNT_TRACKING_STACK_MAXIMUM_V4 + 5, number_of_targets_hit=2
        )

        assert at_cap.base_potency == 120
        assert over_cap.base_potency == at_cap.base_potency

    def test_pursuit_instinct_i_v6_caps_at_six(self):
        at_cap = PursuitInstinctIV6().execute(
            stacks_of_hunt_tracking=HUNT_TRACKING_STACK_MAXIMUM_V4, number_of_targets_hit=2
        )
        over_cap = PursuitInstinctIV6().execute(
            stacks_of_hunt_tracking=HUNT_TRACKING_STACK_MAXIMUM_V4 + 5, number_of_targets_hit=2
        )

        assert at_cap.base_potency == 150
        assert over_cap.base_potency == at_cap.base_potency

    def test_pursuit_instinct_ii_caps_at_three(self):
        at_cap = PursuitInstinctII().execute(
            stacks_of_hunt_tracking=HUNT_TRACKING_STACK_MAXIMUM,
            number_of_targets_hit=2,
            has_collar_brand=False,
        )
        over_cap = PursuitInstinctII().execute(
            stacks_of_hunt_tracking=HUNT_TRACKING_STACK_MAXIMUM + 5,
            number_of_targets_hit=2,
            has_collar_brand=False,
        )

        assert at_cap.base_potency == 135
        assert over_cap.base_potency == at_cap.base_potency

    def test_pursuit_instinct_ii_v3_caps_at_three(self):
        at_cap = PursuitInstinctIIV3().execute(
            stacks_of_hunt_tracking=HUNT_TRACKING_STACK_MAXIMUM,
            number_of_targets_hit=2,
            has_collar_brand=False,
        )
        over_cap = PursuitInstinctIIV3().execute(
            stacks_of_hunt_tracking=HUNT_TRACKING_STACK_MAXIMUM + 5,
            number_of_targets_hit=2,
            has_collar_brand=False,
        )

        assert at_cap.base_potency == 150
        assert over_cap.base_potency == at_cap.base_potency

    def test_pursuit_instinct_ii_v4_caps_at_six(self):
        at_cap = PursuitInstinctIIV4().execute(
            stacks_of_hunt_tracking=HUNT_TRACKING_STACK_MAXIMUM_V4,
            number_of_targets_hit=2,
            has_collar_brand=False,
        )
        over_cap = PursuitInstinctIIV4().execute(
            stacks_of_hunt_tracking=HUNT_TRACKING_STACK_MAXIMUM_V4 + 5,
            number_of_targets_hit=2,
            has_collar_brand=False,
        )

        assert at_cap.base_potency == 180
        assert over_cap.base_potency == at_cap.base_potency

    def test_pursuit_instinct_ii_v6_caps_at_six(self):
        at_cap = PursuitInstinctIIV6().execute(
            stacks_of_hunt_tracking=HUNT_TRACKING_STACK_MAXIMUM_V4,
            number_of_targets_hit=2,
            has_collar_brand=False,
        )
        over_cap = PursuitInstinctIIV6().execute(
            stacks_of_hunt_tracking=HUNT_TRACKING_STACK_MAXIMUM_V4 + 5,
            number_of_targets_hit=2,
            has_collar_brand=False,
        )

        assert at_cap.base_potency == 230
        assert over_cap.base_potency == at_cap.base_potency

    def test_pursuit_instinct_iii_caps_at_three(self):
        at_cap = PursuitInstinctIII().execute(
            stacks_of_hunt_tracking=HUNT_TRACKING_STACK_MAXIMUM,
            number_of_targets_hit=2,
            has_collar_brand=False,
            target_tile_ascension_level=0,
        )
        over_cap = PursuitInstinctIII().execute(
            stacks_of_hunt_tracking=HUNT_TRACKING_STACK_MAXIMUM + 5,
            number_of_targets_hit=2,
            has_collar_brand=False,
            target_tile_ascension_level=0,
        )

        assert at_cap.base_potency == 255
        assert over_cap.base_potency == at_cap.base_potency

    def test_pursuit_instinct_iii_v3_caps_at_three(self):
        at_cap = PursuitInstinctIIIV3().execute(
            stacks_of_hunt_tracking=HUNT_TRACKING_STACK_MAXIMUM,
            number_of_targets_hit=2,
            has_collar_brand=False,
            target_tile_ascension_level=0,
        )
        over_cap = PursuitInstinctIIIV3().execute(
            stacks_of_hunt_tracking=HUNT_TRACKING_STACK_MAXIMUM + 5,
            number_of_targets_hit=2,
            has_collar_brand=False,
            target_tile_ascension_level=0,
        )

        assert at_cap.base_potency == 270
        assert over_cap.base_potency == at_cap.base_potency

    def test_pursuit_instinct_iii_v4_caps_at_six(self):
        at_cap = PursuitInstinctIIIV4().execute(
            stacks_of_hunt_tracking=HUNT_TRACKING_STACK_MAXIMUM_V4,
            number_of_targets_hit=2,
            has_collar_brand=False,
            target_tile_ascension_level=0,
        )
        over_cap = PursuitInstinctIIIV4().execute(
            stacks_of_hunt_tracking=HUNT_TRACKING_STACK_MAXIMUM_V4 + 5,
            number_of_targets_hit=2,
            has_collar_brand=False,
            target_tile_ascension_level=0,
        )

        assert at_cap.base_potency == 300
        assert over_cap.base_potency == at_cap.base_potency

    def test_pursuit_instinct_iii_v6_caps_at_six(self):
        at_cap = PursuitInstinctIIIV6().execute(
            stacks_of_hunt_tracking=HUNT_TRACKING_STACK_MAXIMUM_V4,
            number_of_targets_hit=2,
            has_collar_brand=False,
            target_tile_ascension_level=0,
        )
        over_cap = PursuitInstinctIIIV6().execute(
            stacks_of_hunt_tracking=HUNT_TRACKING_STACK_MAXIMUM_V4 + 5,
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

        assert isinstance(doll.burst_fang, BurstFang)
        assert isinstance(doll.triple_maul, TripleMaul)
        assert isinstance(doll.triple_maul_followup, TripleMaulFollowup)
        assert isinstance(doll.scent_trail, ScentTrailAction)
        assert isinstance(doll.loyal_dash, LoyalDash)
        assert isinstance(doll.pursuit_instinct_i, PursuitInstinctI)
        assert isinstance(doll.pursuit_instinct_ii, PursuitInstinctII)
        assert isinstance(doll.pursuit_instinct_iii, PursuitInstinctIII)

    def test_set_to_v2(self):
        doll = Faelynn()
        doll.set_to_v2()

        assert isinstance(doll.triple_maul, TripleMaulV2)
        assert isinstance(doll.scent_trail, ScentTrailActionV2)

    def test_set_to_v3(self):
        doll = Faelynn()
        doll.set_to_v3()

        assert isinstance(doll.loyal_dash, LoyalDashV3)
        assert isinstance(doll.pursuit_instinct_i, PursuitInstinctIV3)
        assert isinstance(doll.pursuit_instinct_ii, PursuitInstinctIIV3)
        assert isinstance(doll.pursuit_instinct_iii, PursuitInstinctIIIV3)

    def test_set_to_v4(self):
        doll = Faelynn()
        doll.set_to_v4()

        assert isinstance(doll.triple_maul, TripleMaulV4)
        assert isinstance(doll.loyal_dash, LoyalDashV4)
        assert isinstance(doll.pursuit_instinct_i, PursuitInstinctIV4)
        assert isinstance(doll.pursuit_instinct_ii, PursuitInstinctIIV4)
        assert isinstance(doll.pursuit_instinct_iii, PursuitInstinctIIIV4)

    def test_set_to_v5(self):
        doll = Faelynn()
        doll.set_to_v5()

        assert isinstance(doll.triple_maul, TripleMaulV5)
        assert isinstance(doll.triple_maul_followup, TripleMaulFollowupV5)

    def test_set_to_v6(self):
        doll = Faelynn()
        doll.set_to_v6()

        assert isinstance(doll.loyal_dash, LoyalDashV6)
        assert isinstance(doll.pursuit_instinct_i, PursuitInstinctIV6)
        assert isinstance(doll.pursuit_instinct_ii, PursuitInstinctIIV6)
        assert isinstance(doll.pursuit_instinct_iii, PursuitInstinctIIIV6)

    def test_set_fortification_level(self):
        doll = Faelynn()

        doll.set_fortification_level(FortificationLevel.SEGMENT00)
        assert isinstance(doll.triple_maul, TripleMaul)

        doll.set_fortification_level(FortificationLevel.SEGMENT01)
        assert isinstance(doll.triple_maul, TripleMaul)

        doll.set_fortification_level(FortificationLevel.SEGMENT02)
        assert isinstance(doll.triple_maul, TripleMaulV2)
        assert isinstance(doll.scent_trail, ScentTrailActionV2)

        doll.set_fortification_level(FortificationLevel.SEGMENT03)
        assert isinstance(doll.loyal_dash, LoyalDashV3)
        assert isinstance(doll.pursuit_instinct_iii, PursuitInstinctIIIV3)

        doll.set_fortification_level(FortificationLevel.SEGMENT04)
        assert isinstance(doll.triple_maul, TripleMaulV4)
        assert isinstance(doll.loyal_dash, LoyalDashV4)
        assert isinstance(doll.pursuit_instinct_i, PursuitInstinctIV4)
        assert isinstance(doll.pursuit_instinct_ii, PursuitInstinctIIV4)
        assert isinstance(doll.pursuit_instinct_iii, PursuitInstinctIIIV4)

        doll.set_fortification_level(FortificationLevel.SEGMENT05)
        assert isinstance(doll.triple_maul, TripleMaulV5)
        assert isinstance(doll.triple_maul_followup, TripleMaulFollowupV5)

        doll.set_fortification_level(FortificationLevel.SEGMENT06)
        assert isinstance(doll.loyal_dash, LoyalDashV6)
        assert isinstance(doll.pursuit_instinct_i, PursuitInstinctIV6)
        assert isinstance(doll.pursuit_instinct_ii, PursuitInstinctIIV6)
        assert isinstance(doll.pursuit_instinct_iii, PursuitInstinctIIIV6)
