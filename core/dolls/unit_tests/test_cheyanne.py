from core.combat import DamageInstance
from core.dolls.cheyanne import *
from core.types import (
    DamageTag,
    FortificationLevel,
    ModifierType,
    SpecialAttribute,
)


class TestCheyanneBuffs:
    def test_get_analytical_value_buff_below_50(self):
        buff = get_analytical_value_buff(49)

        assert buff.value == 10
        assert buff.modifier_type == ModifierType.ADDITIVE
        assert buff.stat_type == SpecialAttribute.CRITICAL_DAMAGE
        assert buff.tag == DamageTag.ALL

    def test_get_analytical_value_buff_at_50(self):
        buff = get_analytical_value_buff(50)

        assert buff.value == 30

    def test_get_analytical_value_buff_v1_scales_with_analytical_value(self):
        buff = get_analytical_value_buffV1(50)

        # 30 from passive threshold + 25 from V1 passive scaling
        assert buff.value == 55


class TestCheyanneSkills:
    def test_playing_to_potential(self):
        result: DamageInstance = PlayingToPotential().execute(analytical_value=40)

        assert result.base_potency == 80
        assert DamageTag.BASIC in result.tags
        assert DamageTag.PHYSICAL in result.tags
        assert result.group_name == "Playing to Potential"
        assert len(result.buffs_before) == 1
        assert result.buffs_before[0].value == 10

    def test_playing_to_potential_v1(self):
        result: DamageInstance = PlayingToPotentialV1().execute(analytical_value=60)

        # 30 from passive threshold + 30 from V1 passive scaling
        assert result.buffs_before[0].value == 60

    def test_steadfast_pursuit(self):
        result: DamageInstance = SteadfastPursuit().execute(analytical_value=80)

        assert result.base_potency == 80
        assert DamageTag.ACTIVE in result.tags
        assert DamageTag.HEAVY_AMMO in result.tags
        assert result.buffs_before[0].value == 30

    def test_steadfast_pursuit_v1(self):
        result: DamageInstance = SteadfastPursuitV1().execute(analytical_value=70)

        # 30 from passive threshold + 35 from V1 passive scaling
        assert result.buffs_before[0].value == 65

    def test_piercing_the_heavens_into_the_sun_without_bullseye(self):
        result: DamageInstance = PiercingTheHeavensIntoTheSun().execute(
            target_has_bullseye=False,
            few_enemies_with_low_analytical_value=False,
            stacks_of_prepared_stance=0,
        )

        assert result.base_potency == 200
        assert DamageTag.CONFECTANCE in result.tags
        assert len(result.buffs_before) == 1
        assert result.buffs_before[0].value == 30

    def test_piercing_the_heavens_into_the_sun_v2_with_bullseye(self):
        result: DamageInstance = PiercingTheHeavensIntoTheSunV2().execute(
            target_has_bullseye=True,
            few_enemies_with_low_analytical_value=False,
            stacks_of_prepared_stance=0,
        )

        assert result.base_potency == 280
        assert len(result.buffs_before) == 3
        assert result.buffs_before[0].value == 80
        assert result.buffs_before[1].stat_type == SpecialAttribute.CRITICAL_DAMAGE
        assert result.buffs_before[1].value == 30
        assert result.buffs_before[2].stat_type == SpecialAttribute.DEFENSE_IGNORE
        assert result.buffs_before[2].value == 50

    def test_piercing_the_heavens_into_the_sun_v5_few_enemies_bonus(self):
        result: DamageInstance = PiercingTheHeavensIntoTheSunV5().execute(
            target_has_bullseye=False,
            few_enemies_with_low_analytical_value=True,
            stacks_of_prepared_stance=0,
        )

        assert result.base_potency == 380

    def test_piercing_the_heavens_into_the_sun_v6_prepared_stance_caps_at_3(self):
        result: DamageInstance = PiercingTheHeavensIntoTheSunV6().execute(
            target_has_bullseye=False,
            few_enemies_with_low_analytical_value=True,
            stacks_of_prepared_stance=5,
        )

        # 380 with few-enemies condition + (80 * 3 max stacks)
        assert result.base_potency == 620

    def test_think_before_you_act(self):
        result: DamageInstance = ThinkBeforeYouAct().execute(analytical_value=49)

        assert result.base_potency == 120
        assert result.buffs_before[0].value == 10

    def test_think_before_you_act_v1(self):
        result: DamageInstance = ThinkBeforeYouActV1().execute(analytical_value=50)

        assert result.base_potency == 180
        assert result.buffs_before[0].value == 55

    def test_think_before_you_act_v6(self):
        result: DamageInstance = ThinkBeforeYouActV6().execute(analytical_value=50)

        assert result.base_potency == 220
        assert result.buffs_before[0].value == 55


class TestCheyanneFortification:
    def test_set_to_v0(self):
        doll = Cheyanne()
        doll.set_to_v0()

        assert isinstance(doll.playing_to_potential, PlayingToPotential)
        assert isinstance(doll.steadfast_pursuit, SteadfastPursuit)
        assert isinstance(
            doll.piercing_the_heavens_into_the_sun, PiercingTheHeavensIntoTheSun
        )
        assert isinstance(doll.think_before_you_act, ThinkBeforeYouAct)

    def test_set_to_v1(self):
        doll = Cheyanne()
        doll.set_to_v1()

        assert isinstance(doll.playing_to_potential, PlayingToPotentialV1)
        assert isinstance(doll.steadfast_pursuit, SteadfastPursuitV1)
        assert isinstance(
            doll.piercing_the_heavens_into_the_sun, PiercingTheHeavensIntoTheSunV1
        )
        assert isinstance(doll.think_before_you_act, ThinkBeforeYouActV1)

    def test_set_to_v2(self):
        doll = Cheyanne()
        doll.set_to_v2()

        assert isinstance(
            doll.piercing_the_heavens_into_the_sun, PiercingTheHeavensIntoTheSunV2
        )

    def test_set_to_v5(self):
        doll = Cheyanne()
        doll.set_to_v5()

        assert isinstance(
            doll.piercing_the_heavens_into_the_sun, PiercingTheHeavensIntoTheSunV5
        )

    def test_set_to_v6(self):
        doll = Cheyanne()
        doll.set_to_v6()

        assert isinstance(
            doll.piercing_the_heavens_into_the_sun, PiercingTheHeavensIntoTheSunV6
        )
        assert isinstance(doll.think_before_you_act, ThinkBeforeYouActV6)

    def test_set_fortification_level_segment04(self):
        doll = Cheyanne()
        doll.set_fortification_level(FortificationLevel.SEGMENT04)

        assert doll.fortification_level == FortificationLevel.SEGMENT04
        assert isinstance(doll.playing_to_potential, PlayingToPotentialV1)
        assert isinstance(doll.steadfast_pursuit, SteadfastPursuitV1)
        assert isinstance(
            doll.piercing_the_heavens_into_the_sun, PiercingTheHeavensIntoTheSunV2
        )
        assert isinstance(doll.think_before_you_act, ThinkBeforeYouActV1)
