from core.combat import DamageInstance
from core.dolls.phaetusa import (
    BLOODQUENCHED_DAMAGE_MULTIPLIER_INCREASE,
    MAX_STACKS_OF_BLADE_RESONANCE,
    DualWingedDescent,
    DualWingedDescentV6,
    DualWingedDescentV2,
    OneStrikeTwoCuts,
    OneStrikeTwoCutsV6,
    LaceratingWound,
    Phaetusa,
    SupportAction,
    SupportActionV5,
    TwofoldRapture,
    TwofoldRaptureV6,
    TwofoldRaptureV4,
)
from core.types import DamageTag, FortificationLevel


class TestPhaetusaSkills:
    def test_one_strike_two_cuts(self):
        result: DamageInstance = OneStrikeTwoCuts().execute(has_bloodquenched=False)

        assert result.base_potency == 80
        assert result.tags == {
            DamageTag.ACTIVE,
            DamageTag.BASIC,
            DamageTag.MELEE,
            DamageTag.TARGETED,
            DamageTag.PHYSICAL,
        }

    def test_one_strike_two_cuts_with_bloodquenched(self):
        result: DamageInstance = OneStrikeTwoCuts().execute(has_bloodquenched=True)

        assert result.base_potency == 80

    def test_dual_winged_descent(self):
        result: DamageInstance = DualWingedDescent().execute(has_bloodquenched=True)

        assert result.base_potency == 90
        assert DamageTag.PHASE in result.tags
        assert DamageTag.CORROSION in result.tags

    def test_dual_winged_descent_v2(self):
        result: DamageInstance = DualWingedDescentV2().execute(has_bloodquenched=True)

        assert result.base_potency == 120

    def test_twofold_rapture(self):
        result: DamageInstance = TwofoldRapture().execute(
            has_bloodquenched=True,
            stacks_of_blade_resonance=1,
        )

        assert result.base_potency == 200
        assert result.group_name == "Twofold Rapture"
        assert DamageTag.ULTIMATE in result.tags

    def test_twofold_rapture_v4_and_stack_cap(self):
        result: DamageInstance = TwofoldRaptureV4().execute(
            has_bloodquenched=True,
            stacks_of_blade_resonance=MAX_STACKS_OF_BLADE_RESONANCE + 10,
        )

        assert result.base_potency == 720

    def test_one_strike_two_cuts_v6_with_bloodquenched(self):
        result: DamageInstance = OneStrikeTwoCutsV6().execute(has_bloodquenched=True)

        assert result.base_potency == 80 + BLOODQUENCHED_DAMAGE_MULTIPLIER_INCREASE

    def test_dual_winged_descent_v6_with_bloodquenched(self):
        result: DamageInstance = DualWingedDescentV6().execute(has_bloodquenched=True)

        assert result.base_potency == 120 + BLOODQUENCHED_DAMAGE_MULTIPLIER_INCREASE

    def test_twofold_rapture_v6_and_stack_cap(self):
        result: DamageInstance = TwofoldRaptureV6().execute(
            has_bloodquenched=True,
            stacks_of_blade_resonance=MAX_STACKS_OF_BLADE_RESONANCE + 10,
        )

        assert result.base_potency == 920

    def test_lacerating_wound(self):
        result: DamageInstance = LaceratingWound().execute(
            original_damage_instance_potency=680
        )

        assert result.base_potency == 272
        assert result.group_name == "Lacerating Wound"
        assert DamageTag.PASSIVE in result.tags

    def test_support_action(self):
        result: DamageInstance = SupportAction().execute()

        assert result.base_potency == 90
        assert DamageTag.SUPPORT_ACTION in result.tags

    def test_support_action_v5(self):
        result: DamageInstance = SupportActionV5().execute()

        assert result.base_potency == 120
        assert DamageTag.SUPPORT_ACTION in result.tags


class TestPhaetusa:
    def test_set_to_v0(self):
        doll = Phaetusa()
        doll.set_to_v0()

        assert isinstance(doll.one_strike_two_cuts, OneStrikeTwoCuts)
        assert isinstance(doll.dual_winged_descent, DualWingedDescent)
        assert isinstance(doll.twofold_rapture, TwofoldRapture)
        assert isinstance(doll.support_action, SupportAction)

    def test_set_to_v2(self):
        doll = Phaetusa()
        doll.set_to_v2()

        assert isinstance(doll.dual_winged_descent, DualWingedDescentV2)
        assert isinstance(doll.twofold_rapture, TwofoldRapture)

    def test_set_to_v4(self):
        doll = Phaetusa()
        doll.set_to_v4()

        assert isinstance(doll.dual_winged_descent, DualWingedDescentV2)
        assert isinstance(doll.twofold_rapture, TwofoldRaptureV4)

    def test_set_to_v5(self):
        doll = Phaetusa()
        doll.set_to_v5()

        assert isinstance(doll.dual_winged_descent, DualWingedDescentV2)
        assert isinstance(doll.twofold_rapture, TwofoldRaptureV4)
        assert isinstance(doll.support_action, SupportActionV5)

    def test_set_to_v6(self):
        doll = Phaetusa()
        doll.set_to_v6()

        assert isinstance(doll.one_strike_two_cuts, OneStrikeTwoCutsV6)
        assert isinstance(doll.dual_winged_descent, DualWingedDescentV6)
        assert isinstance(doll.twofold_rapture, TwofoldRaptureV6)
        assert isinstance(doll.support_action, SupportActionV5)

    def test_set_fortification_level(self):
        doll = Phaetusa()
        doll.set_fortification_level(FortificationLevel.SEGMENT06)

        assert doll.fortification_level == FortificationLevel.SEGMENT06
        assert isinstance(doll.one_strike_two_cuts, OneStrikeTwoCutsV6)
        assert isinstance(doll.dual_winged_descent, DualWingedDescentV6)
        assert isinstance(doll.twofold_rapture, TwofoldRaptureV6)
        assert isinstance(doll.support_action, SupportActionV5)
