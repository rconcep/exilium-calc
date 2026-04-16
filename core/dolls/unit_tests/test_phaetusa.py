from core.combat import DamageInstance
from core.dolls.phaetusa import (
    BLOOD_OATH_DAMAGE_MULTIPLIER_INCREASE,
    MAX_STACKS_OF_BLADE_RESONANCE,
    DoubleDescent,
    DoubleDescentV2,
    DualSlash,
    LaceratingWound,
    Phaetusa,
    SupportAction,
    SupportActionV5,
    TwinParadise,
    TwinParadiseV4,
)
from core.types import DamageTag, FortificationLevel


class TestPhaetusaSkills:
    def test_dual_slash(self):
        result: DamageInstance = DualSlash().execute(has_blood_oath=False)

        assert result.base_potency == 80
        assert result.tags == {
            DamageTag.ACTIVE,
            DamageTag.BASIC,
            DamageTag.MELEE,
            DamageTag.TARGETED,
            DamageTag.PHYSICAL,
        }

    def test_dual_slash_with_blood_oath(self):
        result: DamageInstance = DualSlash().execute(has_blood_oath=True)

        assert result.base_potency == 80 + BLOOD_OATH_DAMAGE_MULTIPLIER_INCREASE

    def test_double_descent(self):
        result: DamageInstance = DoubleDescent().execute(has_blood_oath=True)

        assert result.base_potency == 90 + BLOOD_OATH_DAMAGE_MULTIPLIER_INCREASE
        assert DamageTag.PHASE in result.tags
        assert DamageTag.CORROSION in result.tags

    def test_double_descent_v2(self):
        result: DamageInstance = DoubleDescentV2().execute(has_blood_oath=True)

        assert result.base_potency == 120 + BLOOD_OATH_DAMAGE_MULTIPLIER_INCREASE

    def test_twin_paradise(self):
        result: DamageInstance = TwinParadise().execute(
            has_blood_oath=True,
            stacks_of_blade_resonance=1,
        )

        assert result.base_potency == 600
        assert result.group_name == "Twin Paradise"
        assert DamageTag.ULTIMATE in result.tags

    def test_twin_paradise_v4_and_stack_cap(self):
        result: DamageInstance = TwinParadiseV4().execute(
            has_blood_oath=True,
            stacks_of_blade_resonance=MAX_STACKS_OF_BLADE_RESONANCE + 10,
        )

        assert result.base_potency == 1520

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

        assert isinstance(doll.dual_slash, DualSlash)
        assert isinstance(doll.double_descent, DoubleDescent)
        assert isinstance(doll.twin_paradise, TwinParadise)
        assert isinstance(doll.support_action, SupportAction)

    def test_set_to_v2(self):
        doll = Phaetusa()
        doll.set_to_v2()

        assert isinstance(doll.double_descent, DoubleDescentV2)
        assert isinstance(doll.twin_paradise, TwinParadise)

    def test_set_to_v4(self):
        doll = Phaetusa()
        doll.set_to_v4()

        assert isinstance(doll.double_descent, DoubleDescentV2)
        assert isinstance(doll.twin_paradise, TwinParadiseV4)

    def test_set_to_v5(self):
        doll = Phaetusa()
        doll.set_to_v5()

        assert isinstance(doll.double_descent, DoubleDescentV2)
        assert isinstance(doll.twin_paradise, TwinParadiseV4)
        assert isinstance(doll.support_action, SupportActionV5)

    def test_set_fortification_level(self):
        doll = Phaetusa()
        doll.set_fortification_level(FortificationLevel.SEGMENT06)

        assert doll.fortification_level == FortificationLevel.SEGMENT06
        assert isinstance(doll.double_descent, DoubleDescentV2)
        assert isinstance(doll.twin_paradise, TwinParadiseV4)
        assert isinstance(doll.support_action, SupportActionV5)
