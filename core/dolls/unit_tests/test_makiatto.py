from core.dolls.makiatto import *
from core.types import (
    DamageTag,
    SpecialAttribute,
    StatType,
    FortificationLevel,
    ModifierType,
)
from core.buffs import Buff
from core.combat import DamageInstance


class TestMakiattoSkills:
    def test_lone_wolf_territory(self):
        da: DamageInstance = LoneWolfTerritory().execute()

        assert da.base_potency == 80
        assert DamageTag.ACTIVE in da.tags
        assert DamageTag.BASIC in da.tags
        assert DamageTag.HEAVY_AMMO in da.tags
        assert DamageTag.TARGETED in da.tags
        assert DamageTag.PHYSICAL in da.tags

    def test_cold_precision_shot(self):
        da: DamageInstance = ColdPrecisionShot().execute()

        assert da.base_potency == 160
        assert DamageTag.FREEZE in da.tags
        assert da.buffs_before == [
            Buff(
                30,
                ModifierType.ADDITIVE,
                SpecialAttribute.CRITICAL_DAMAGE,
                DamageTag.ALL,
            )
        ]

    def test_cold_precision_shot_v1(self):
        da: DamageInstance = ColdPrecisionShotV1().execute()

        assert da.base_potency == 100

    def test_cold_precision_shot_second(self):
        da: DamageInstance = ColdPrecisionShotSecond().execute(
            first_hit_was_critical=False
        )

        assert da.base_potency == 0
        assert da.tags == set()

    def test_cold_precision_shot_second_v1_non_crit(self):
        da: DamageInstance = ColdPrecisionShotSecondV1().execute(
            first_hit_was_critical=False
        )

        assert da.base_potency == 100
        assert da.buffs_before == []

    def test_cold_precision_shot_second_v1_crit(self):
        da: DamageInstance = ColdPrecisionShotSecondV1().execute(
            first_hit_was_critical=True
        )

        assert da.base_potency == 100
        assert da.buffs_before[0] == Buff(
            80, ModifierType.ADDITIVE, SpecialAttribute.CRITICAL_DAMAGE, DamageTag.ALL
        )
        assert da.buffs_before[1] == Buff(
            100, ModifierType.ADDITIVE, StatType.CRIT_RATE
        )

    def test_professional_tactics(self):
        da: DamageInstance = ProfessionalTactics().execute()

        assert da.base_potency == 130
        assert DamageTag.ACTIVE in da.tags
        assert DamageTag.PHYSICAL in da.tags

    def test_interception(self):
        da: DamageInstance = Interception().execute()

        assert da.base_potency == 90
        assert DamageTag.PASSIVE in da.tags
        assert DamageTag.INTERCEPTION in da.tags


class TestMakiatto:
    def test_set_to_v0(self):
        makiatto: Makiatto = Makiatto()
        makiatto.set_to_v0()

        assert isinstance(makiatto.lone_wolf_territory, LoneWolfTerritory)
        assert isinstance(makiatto.professional_tactics, ProfessionalTactics)
        assert isinstance(makiatto.cold_precision_shot_first, ColdPrecisionShot)
        assert isinstance(makiatto.cold_precision_shot_second, ColdPrecisionShotSecond)
        assert isinstance(makiatto.interception, Interception)

        assert makiatto.initial_stats.basic_attributes[StatType.CRIT_RATE] == 40
        assert (
            makiatto.initial_stats.special_attributes[
                SpecialAttribute.CRITICAL_DAMAGE
            ].get_multiplier(DamageTag.ALL)
            == -10
        )
        assert (
            makiatto.initial_stats.special_attributes[
                SpecialAttribute.DAMAGE_BOOST
            ].get_multiplier(DamageTag.ALL)
            == 30
        )
        assert (
            makiatto.initial_stats.special_attributes[
                SpecialAttribute.CRITICAL_DAMAGE
            ].get_multiplier(DamageTag.INTERCEPTION)
            == 30
        )

    def test_set_to_v1(self):
        makiatto: Makiatto = Makiatto()
        makiatto.set_to_v1()

        assert isinstance(makiatto.cold_precision_shot_first, ColdPrecisionShotV1)
        assert isinstance(
            makiatto.cold_precision_shot_second, ColdPrecisionShotSecondV1
        )

    def test_set_to_v5(self):
        makiatto: Makiatto = Makiatto()
        makiatto.set_to_v5()

        assert (
            makiatto.initial_stats.special_attributes[
                SpecialAttribute.DAMAGE_BOOST
            ].get_multiplier(DamageTag.ALL)
            == 0
        )
        assert (
            makiatto.initial_stats.special_attributes[
                SpecialAttribute.DAMAGE_BOOST
            ].get_multiplier(DamageTag.FREEZE)
            == 30
        )

    def test_set_fortification_level(self):
        makiatto: Makiatto = Makiatto()
        makiatto.set_fortification_level(FortificationLevel.SEGMENT00)

        assert isinstance(makiatto.cold_precision_shot_first, ColdPrecisionShot)

        makiatto.set_fortification_level(FortificationLevel.SEGMENT06)

        assert isinstance(makiatto.cold_precision_shot_first, ColdPrecisionShotV1)
