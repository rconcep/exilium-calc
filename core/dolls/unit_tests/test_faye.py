from core.buffs import Buff
from core.combat import (
    DamageInstance,
    FayeDamageCalculationStrategy,
    FixedDamageInstance,
)
from core.dolls.faye import *
from core.types import (
    DamageTag,
    FortificationLevel,
    ModifierType,
    SpecialAttribute,
    StatType,
)


class TestFayeSkills:
    def test_practice_shot(self):
        practice_shot: DamageInstance = PracticeShot().execute()

        assert practice_shot.base_potency == 80
        assert DamageTag.BASIC in practice_shot.tags
        assert practice_shot.group_name == "Practice Shot"

    def test_ruinous_whirl_without_fixed_key_2(self):
        ruinous_whirl: DamageInstance = RuinousWhirl().execute(has_fixed_key_2=False)

        assert ruinous_whirl.base_potency == 80
        assert DamageTag.CONFECTANCE in ruinous_whirl.tags
        assert ruinous_whirl.buffs_before == []
        assert isinstance(
            ruinous_whirl.damage_calculation_strategy,
            FayeDamageCalculationStrategy,
        )

    def test_ruinous_whirl_with_fixed_key_2(self):
        ruinous_whirl: DamageInstance = RuinousWhirl().execute(has_fixed_key_2=True)

        assert ruinous_whirl.buffs_before == [
            Buff(
                value=20,
                modifier_type=ModifierType.ADDITIVE,
                stat_type=SpecialAttribute.DAMAGE_BOOST,
                tag=DamageTag.ONLY_HIT_ONE_TARGET,
            )
        ]

    def test_fissioned_firelight(self):
        fissioned_firelight: DamageInstance = FissionedFirelight().execute()

        assert fissioned_firelight.base_potency == 120
        assert DamageTag.TARGETED in fissioned_firelight.tags
        assert isinstance(
            fissioned_firelight.damage_calculation_strategy,
            FayeDamageCalculationStrategy,
        )

    def test_fissioned_firelight_v2(self):
        fissioned_firelight: DamageInstance = FissionedFirelightV2().execute()

        assert fissioned_firelight.base_potency == 140

    def test_no_survivors_below_rend_threshold(self):
        no_survivors: DamageInstance = NoSurvivors().execute(stacks_of_rend=5)

        assert no_survivors.base_potency == 160
        assert no_survivors.buffs_before == []

    def test_no_survivors_at_rend_threshold(self):
        no_survivors: DamageInstance = NoSurvivors().execute(stacks_of_rend=6)

        assert no_survivors.buffs_before == [
            Buff(
                value=120,
                modifier_type=ModifierType.ADDITIVE,
                stat_type=SpecialAttribute.DAMAGE_BOOST,
                tag=DamageTag.ALL,
            )
        ]

    def test_no_survivors_v6_at_rend_threshold(self):
        no_survivors: DamageInstance = NoSurvivorsV6().execute(stacks_of_rend=6)

        assert no_survivors.buffs_before == [
            Buff(
                value=120,
                modifier_type=ModifierType.ADDITIVE,
                stat_type=SpecialAttribute.DAMAGE_BOOST,
                tag=DamageTag.ALL,
            ),
            Buff(
                value=30,
                modifier_type=ModifierType.ADDITIVE,
                stat_type=StatType.CRIT_RATE,
                tag=DamageTag.ALL,
            ),
            Buff(
                value=12,
                modifier_type=ModifierType.ADDITIVE,
                stat_type=StatType.CRIT_DAMAGE,
                tag=DamageTag.ALL,
            ),
        ]

    def test_tomahawk_throw(self):
        tomahawk_throw: DamageInstance = TomahawkThrow().execute()

        assert tomahawk_throw.base_potency == 80
        assert tomahawk_throw.group_name == "Tomahawk Combo"
        assert DamageTag.PASSIVE in tomahawk_throw.tags

    def test_axe_whirl_v3(self):
        axe_whirl: DamageInstance = AxeWhirlV3().execute()

        assert axe_whirl.base_potency == 60
        assert axe_whirl.buffs_before == [
            Buff(
                value=30,
                modifier_type=ModifierType.ADDITIVE,
                stat_type=SpecialAttribute.DAMAGE_BOOST,
                tag=DamageTag.ALL,
            )
        ]

    def test_gash(self):
        gash: FixedDamageInstance = Gash().execute(stacks_of_gash=7)

        assert gash.base_potency == 56


class TestFaye:
    def test_set_to_v0(self):
        faye: Faye = Faye()
        faye.set_to_v0()

        assert isinstance(faye.practice_shot, PracticeShot)
        assert isinstance(faye.ruinous_whirl, RuinousWhirl)
        assert isinstance(faye.fissioned_firelight, FissionedFirelight)
        assert isinstance(faye.no_survivors, NoSurvivors)
        assert isinstance(faye.gash, Gash)
        assert isinstance(faye.tomahawk_throw, TomahawkThrow)
        assert isinstance(faye.axe_whirl, AxeWhirl)

    def test_set_to_v2(self):
        faye: Faye = Faye()
        faye.set_to_v2()

        assert isinstance(faye.fissioned_firelight, FissionedFirelightV2)

    def test_set_to_v3(self):
        faye: Faye = Faye()
        faye.set_to_v3()

        assert isinstance(faye.fissioned_firelight, FissionedFirelightV2)
        assert isinstance(faye.axe_whirl, AxeWhirlV3)

    def test_set_to_v5(self):
        faye: Faye = Faye()
        faye.set_to_v5()

        assert isinstance(faye.fissioned_firelight, FissionedFirelightV2)
        assert isinstance(faye.axe_whirl, AxeWhirlV3)
        assert isinstance(faye.ruinous_whirl, RuinousWhirlV5)

    def test_set_to_v6(self):
        faye: Faye = Faye()
        faye.set_to_v6()

        assert isinstance(faye.ruinous_whirl, RuinousWhirlV5)
        assert isinstance(faye.fissioned_firelight, FissionedFirelightV2)
        assert isinstance(faye.axe_whirl, AxeWhirlV3)
        assert isinstance(faye.no_survivors, NoSurvivorsV6)

    def test_set_to_fortification_level(self):
        faye: Faye = Faye()
        faye.set_fortification_level(FortificationLevel.SEGMENT04)

        assert faye.fortification_level == FortificationLevel.SEGMENT04
        assert isinstance(faye.ruinous_whirl, RuinousWhirl)
        assert isinstance(faye.fissioned_firelight, FissionedFirelightV2)
        assert isinstance(faye.axe_whirl, AxeWhirlV3)
        assert isinstance(faye.no_survivors, NoSurvivors)
