from core.dolls.sextans import *

from core.combat import DamageInstance
from core.types import DamageTag, FortificationLevel, ModifierType, SpecialAttribute


class TestSextansSkills:
    def test_dreamscape_garrote(self):
        result: DamageInstance = DreamscapeGarrote().execute()

        assert result.base_potency == 80
        assert DamageTag.ACTIVE in result.tags
        assert DamageTag.BASIC in result.tags
        assert DamageTag.MELEE in result.tags
        assert DamageTag.TARGETED in result.tags
        assert DamageTag.PHYSICAL in result.tags
        assert result.group_name == "Dreamscape Garrote"

    def test_sanctuary_lauds_scales_with_coagulation(self):
        result: DamageInstance = SanctuaryLauds().execute(stacks_of_coagulation=6)

        assert result.base_potency == 150
        assert DamageTag.ELECTRIC in result.tags
        assert DamageTag.PHASE in result.tags
        assert result.group_name == "Sanctuary Lauds"

    def test_sanctuary_lauds_caps_at_max_stacks(self):
        result: DamageInstance = SanctuaryLauds().execute(stacks_of_coagulation=5000)

        assert result.base_potency == 10080

    def test_death_knell_and_v5_base_potency(self):
        v0: DamageInstance = DeathKnell().execute(stacks_of_coagulation=2)
        v5: DamageInstance = DeathKnellV5().execute(stacks_of_coagulation=2)

        assert v0.base_potency == 110
        assert v5.base_potency == 140
        assert v0.group_name == "Death Knell"
        assert v5.group_name == "Death Knell"

    def test_blood_kiss(self):
        result: DamageInstance = BloodKiss().execute(multiplier_of_death_knell=360)

        assert result.base_potency == 360
        assert DamageTag.PASSIVE in result.tags
        assert DamageTag.MELEE in result.tags
        assert result.group_name == "Blood Kiss"

    def test_midnight_vesper(self):
        result: DamageInstance = MidnightVesper().execute(stacks_of_coagulation=3)

        assert result.base_potency == 150
        assert DamageTag.ULTIMATE in result.tags
        assert DamageTag.AREA_OF_EFFECT in result.tags
        assert result.group_name == "Midnight Vesper"

    def test_lacerating_wound(self):
        result: DamageInstance = LaceratingWound().execute(
            original_damage_instance_potency=95
        )

        assert result.base_potency == 38
        assert DamageTag.PASSIVE in result.tags
        assert result.group_name == "Lacerating Wound"

    def test_blood_insignia_applies_stack_scaling_and_trigger_falloff(self):
        result: DamageInstance = BloodInsignia().execute(
            stacks_of_coagulation=5,
            previous_triggers_this_round=2,
        )

        # 60 + (5 * 3) - (2 * 20)
        assert result.base_potency == 35

    def test_blood_insignia_has_minimum_potency(self):
        result: DamageInstance = BloodInsignia().execute(
            stacks_of_coagulation=0,
            previous_triggers_this_round=99,
        )

        assert result.base_potency == 30

    def test_blood_insignia_v3_scaling(self):
        result: DamageInstance = BloodInsigniaV3().execute(
            stacks_of_coagulation=5,
            previous_triggers_this_round=0,
        )

        assert result.base_potency == 80

    def test_blood_insignia_v6_has_defense_ignore_buff(self):
        result: DamageInstance = BloodInsigniaV6().execute(
            stacks_of_coagulation=0,
            previous_triggers_this_round=0,
        )

        assert result.base_potency == 90
        assert len(result.buffs_before) == 1
        assert result.buffs_before[0].value == 30
        assert result.buffs_before[0].modifier_type == ModifierType.ADDITIVE
        assert result.buffs_before[0].stat_type == SpecialAttribute.DEFENSE_IGNORE
        assert result.buffs_before[0].tag == DamageTag.ALL


class TestSextansFortification:
    def test_set_to_v0(self):
        doll: Sextans = Sextans()
        doll.set_to_v0()

        assert isinstance(doll.dreamscape_garrote, DreamscapeGarrote)
        assert isinstance(doll.sanctuary_lauds, SanctuaryLauds)
        assert isinstance(doll.death_knell, DeathKnell)
        assert isinstance(doll.midnight_vesper, MidnightVesper)
        assert isinstance(doll.blood_insignia, BloodInsignia)
        assert isinstance(doll.lacerating_wound, LaceratingWound)

    def test_set_to_v3(self):
        doll: Sextans = Sextans()
        doll.set_to_v3()

        assert isinstance(doll.death_knell, DeathKnell)
        assert isinstance(doll.blood_insignia, BloodInsigniaV3)

    def test_set_to_v5(self):
        doll: Sextans = Sextans()
        doll.set_to_v5()

        assert isinstance(doll.death_knell, DeathKnellV5)
        assert isinstance(doll.blood_insignia, BloodInsigniaV3)

    def test_set_to_v6(self):
        doll: Sextans = Sextans()
        doll.set_to_v6()

        assert isinstance(doll.death_knell, DeathKnellV5)
        assert isinstance(doll.blood_insignia, BloodInsigniaV6)

    def test_set_fortification_level(self):
        doll: Sextans = Sextans()

        doll.set_fortification_level(FortificationLevel.SEGMENT04)
        assert isinstance(doll.blood_insignia, BloodInsigniaV3)
        assert isinstance(doll.death_knell, DeathKnell)

        doll.set_fortification_level(FortificationLevel.SEGMENT06)
        assert doll.fortification_level == FortificationLevel.SEGMENT06
        assert isinstance(doll.death_knell, DeathKnellV5)
        assert isinstance(doll.blood_insignia, BloodInsigniaV6)
