from core.dolls.voymastina import *
from core.types import DamageTag, SpecialAttribute
from core.buffs import Buff, Debuff
from core.combat import DamageInstance


class TestVoymastinaSkills:
    def test_dreadful_judgment(self):
        dj: DamageInstance = DreadUltimatum().execute()

        assert dj.base_potency == 80
        assert DamageTag.PHYSICAL in dj.tags
        assert DamageTag.BASIC in dj.tags

    def test_s1_passive(self):
        su: DamageInstance = SiriusFallPassive().execute(has_fixed_key_4=True)

        assert su.base_potency == 100
        assert DamageTag.PHYSICAL in su.tags
        assert DamageTag.AREA_OF_EFFECT in su.tags
        assert DamageTag.PASSIVE in su.tags
        assert su.buffs_before[0] == Buff(
            20,
            modifier_type=ModifierType.ADDITIVE,
            stat_type=SpecialAttribute.DAMAGE_BOOST,
            tag=DamageTag.ALL,
        )

    def test_s1_active(self):
        su: DamageInstance = SiriusFallActive().execute()

        assert su.base_potency == 120
        assert DamageTag.PHYSICAL in su.tags
        assert DamageTag.AREA_OF_EFFECT in su.tags
        assert DamageTag.ACTIVE in su.tags

    def test_eye_of_the_white_mastiff_passive(self):
        eye: DamageInstance = EyeOfTheWhiteMastiffPassive().execute()

        assert eye.base_potency == 100
        assert DamageTag.PHYSICAL in eye.tags
        assert DamageTag.TARGETED in eye.tags
        assert DamageTag.PASSIVE in eye.tags

    def test_lockon_attack(self):
        la: DamageInstance = LockOnAttack().execute()

        assert la.base_potency == 80
        assert DamageTag.PHYSICAL in la.tags
        assert DamageTag.AREA_OF_EFFECT in la.tags
        assert DamageTag.PASSIVE in la.tags

    def test_ult_passive(self):
        cf: DamageInstance = PileBunkerPassive().execute()

        assert cf.base_potency == 150
        assert DamageTag.PHYSICAL in cf.tags
        assert DamageTag.MELEE in cf.tags
        assert DamageTag.PASSIVE in cf.tags

    def test_ult_active(self):
        cf: DamageInstance = PileBunkerActive().execute()

        assert cf.base_potency == 200
        assert DamageTag.PHYSICAL in cf.tags
        assert DamageTag.MELEE in cf.tags
        assert DamageTag.ULTIMATE in cf.tags

    def test_s1_passive_v1(self):
        su: DamageInstance = SiriusFallPassiveV1().execute()

        assert su.base_potency == 150
        assert DamageTag.PHYSICAL in su.tags
        assert DamageTag.AREA_OF_EFFECT in su.tags
        assert DamageTag.PASSIVE in su.tags
        assert su.buffs_before[0] == Buff(
            20,
            modifier_type=ModifierType.ADDITIVE,
            stat_type=SpecialAttribute.DAMAGE_BOOST,
            tag=DamageTag.ALL,
        )

    def test_s1_active_v1(self):
        su: DamageInstance = SiriusFallActiveV1().execute()

        assert su.base_potency == 180
        assert DamageTag.PHYSICAL in su.tags
        assert DamageTag.AREA_OF_EFFECT in su.tags
        assert DamageTag.ACTIVE in su.tags

    def test_ult_passive_v2(self):
        cf: DamageInstance = PileBunkerPassiveV2().execute()

        assert cf.base_potency == 150
        assert DamageTag.PHYSICAL in cf.tags
        assert DamageTag.MELEE in cf.tags
        assert DamageTag.PASSIVE in cf.tags
        assert cf.buffs_before[0] == Buff(
            10, modifier_type=ModifierType.MULTIPLICATIVE, stat_type=StatType.ATTACK
        )

    def test_ult_active_v2(self):
        cf: DamageInstance = PileBunkerActiveV2().execute(
            has_activated_fixed_key_6=True
        )

        assert cf.base_potency == 300
        assert DamageTag.PHYSICAL in cf.tags
        assert DamageTag.MELEE in cf.tags
        assert DamageTag.ULTIMATE in cf.tags
        assert cf.buffs_before[0] == Buff(
            15,
            modifier_type=ModifierType.ADDITIVE,
            stat_type=SpecialAttribute.DAMAGE_BOOST,
            tag=DamageTag.ULTIMATE,
        )
        assert cf.buffs_before[1] == Buff(
            10, modifier_type=ModifierType.MULTIPLICATIVE, stat_type=StatType.ATTACK
        )

    def test_eye_of_the_white_mastiff_passive_v3(self):
        eye: DamageInstance = EyeOfTheWhiteMastiffPassiveV3().execute()

        assert eye.base_potency == 300
        assert DamageTag.PHYSICAL in eye.tags
        assert DamageTag.TARGETED in eye.tags
        assert DamageTag.PASSIVE in eye.tags

    def test_lockon_attack_v3(self):
        la: DamageInstance = LockOnAttackV3().execute()

        assert la.base_potency == 130
        assert DamageTag.PHYSICAL in la.tags
        assert DamageTag.AREA_OF_EFFECT in la.tags
        assert DamageTag.PASSIVE in la.tags

    def test_ult_passive_v5(self):
        cf: DamageInstance = PileBunkerPassiveV5().execute()

        assert cf.base_potency == 150
        assert DamageTag.PHYSICAL in cf.tags
        assert DamageTag.MELEE in cf.tags
        assert DamageTag.PASSIVE in cf.tags
        assert cf.buffs_before[0] == Buff(
            10, modifier_type=ModifierType.MULTIPLICATIVE, stat_type=StatType.ATTACK
        )
        assert cf.debuffs_before[0] == DefenseDownII()

    def test_ult_active_v5(self):
        cf: DamageInstance = PileBunkerActiveV5().execute()

        assert cf.base_potency == 300
        assert DamageTag.PHYSICAL in cf.tags
        assert DamageTag.MELEE in cf.tags
        assert DamageTag.ULTIMATE in cf.tags
        assert cf.buffs_before[0] == Buff(
            10, modifier_type=ModifierType.MULTIPLICATIVE, stat_type=StatType.ATTACK
        )
        assert cf.debuffs_before[0] == DefenseDownII()


class TestVoymastina:
    def test_set_to_v0(self):
        tina: Voymastina = Voymastina()
        tina.set_to_v0()

        assert isinstance(tina.dread_ultimatum, DreadUltimatum)
        assert isinstance(tina.sirius_fall_passive, SiriusFallPassive)
        assert isinstance(tina.sirius_fall_active, SiriusFallActive)
        assert isinstance(
            tina.eye_of_the_white_mastiff_passive, EyeOfTheWhiteMastiffPassive
        )
        assert isinstance(tina.lockon_attack, LockOnAttack)
        assert isinstance(tina.pile_bunker_passive, PileBunkerPassive)
        assert isinstance(tina.pile_bunker_active, PileBunkerActive)

    def test_set_to_v1(self):
        tina: Voymastina = Voymastina()
        tina.set_to_v1()

        assert isinstance(tina.sirius_fall_passive, SiriusFallPassiveV1)
        assert isinstance(tina.sirius_fall_active, SiriusFallActiveV1)

    def test_set_to_v2(self):
        tina: Voymastina = Voymastina()
        tina.set_to_v2()

        assert isinstance(tina.pile_bunker_passive, PileBunkerPassiveV2)
        assert isinstance(tina.pile_bunker_active, PileBunkerActiveV2)

    def test_set_to_v3(self):
        tina: Voymastina = Voymastina()
        tina.set_to_v3()

        assert isinstance(
            tina.eye_of_the_white_mastiff_passive, EyeOfTheWhiteMastiffPassiveV3
        )
        assert isinstance(tina.lockon_attack, LockOnAttackV3)

    def test_set_to_v5(self):
        tina: Voymastina = Voymastina()
        tina.set_to_v5()

        assert isinstance(tina.pile_bunker_passive, PileBunkerPassiveV5)
        assert isinstance(tina.pile_bunker_active, PileBunkerActiveV5)

    def test_set_to_v6(self):
        tina: Voymastina = Voymastina()
        tina.set_to_v6()

        assert (
            tina.initial_stats.special_attributes[
                SpecialAttribute.DEFENSE_IGNORE
            ].get_multiplier(DamageTag.PHYSICAL)
            == 125
        )

    def test_set_to_fortification_level(self):
        tina: Voymastina = Voymastina()
        tina.set_fortification_level(FortificationLevel.SEGMENT06)

        assert isinstance(tina.pile_bunker_passive, PileBunkerPassiveV5)
        assert isinstance(tina.pile_bunker_active, PileBunkerActiveV5)
