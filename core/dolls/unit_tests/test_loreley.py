from core.dolls.loreley import *

from core.buffs import Buff
from core.combat import DamageInstance
from core.types import (
    DamageTag,
    FortificationLevel,
    ModifierType,
    SpecialAttribute,
)


class TestLoreleySkills:
    def test_punishment_prelude(self):
        result: DamageInstance = PunishmentPrelude().execute()

        assert result.base_potency == 80
        assert DamageTag.ACTIVE in result.tags
        assert DamageTag.BASIC in result.tags
        assert DamageTag.HEAVY_AMMO in result.tags
        assert DamageTag.TARGETED in result.tags
        assert DamageTag.PHYSICAL in result.tags
        assert result.group_name == "Punishment Prelude"

    def test_scorching_brand_without_blazing_embers(self):
        result: DamageInstance = ScorchingBrand().execute(
            has_blazing_embers=False,
            target_on_burn_tile=False,
        )

        assert result.base_potency == 130
        assert DamageTag.BURN in result.tags
        assert DamageTag.PHASE in result.tags
        assert result.group_name == "Scorching Brand"

    def test_scorching_brand_with_blazing_embers(self):
        result: DamageInstance = ScorchingBrand().execute(
            has_blazing_embers=True,
            target_on_burn_tile=False,
        )

        assert result.base_potency == 260

    def test_scorching_brand_v5_applies_defense_ignore(self):
        result: DamageInstance = ScorchingBrandV5().execute(
            has_blazing_embers=False,
            target_on_burn_tile=False,
        )

        assert result.base_potency == 130
        assert result.buffs_before == [
            Buff(
                value=30,
                modifier_type=ModifierType.ADDITIVE,
                stat_type=SpecialAttribute.DEFENSE_IGNORE,
                tag=DamageTag.ALL,
            )
        ]

    def test_scorching_brand_v5_on_burn_tile_adds_damage_buff(self):
        result: DamageInstance = ScorchingBrandV5().execute(
            has_blazing_embers=True,
            target_on_burn_tile=True,
        )

        assert result.base_potency == 260
        assert len(result.buffs_before) == 2
        assert result.buffs_before[1] == Buff(
            value=60,
            modifier_type=ModifierType.ADDITIVE,
            stat_type=SpecialAttribute.DAMAGE_BOOST,
            tag=DamageTag.ALL,
        )

    def test_crimson_binding_decree_splits_without_blazing_embers(self):
        result: DamageInstance = CrimsonBindingDecree().execute(
            has_blazing_embers=False,
            number_of_targets=3,
            number_of_burn_buffs=0,
        )

        assert result.base_potency == 40

    def test_crimson_binding_decree_no_split_with_blazing_embers(self):
        result: DamageInstance = CrimsonBindingDecree().execute(
            has_blazing_embers=True,
            number_of_targets=3,
            number_of_burn_buffs=0,
        )

        assert result.base_potency == 120

    def test_crimson_binding_decree_v4_burn_buff_cap(self):
        result: DamageInstance = CrimsonBindingDecreeV4().execute(
            has_blazing_embers=True,
            number_of_targets=1,
            number_of_burn_buffs=8,
        )

        assert result.base_potency == 150
        assert result.buffs_before == [
            Buff(
                value=40,
                modifier_type=ModifierType.ADDITIVE,
                stat_type=SpecialAttribute.DAMAGE_BOOST,
                tag=DamageTag.ALL,
            )
        ]

    def test_agonys_grace(self):
        result: DamageInstance = AgonysGrace().execute()

        assert result.base_potency == 60
        assert DamageTag.ULTIMATE in result.tags
        assert DamageTag.AREA_OF_EFFECT in result.tags
        assert result.group_name == "Agony's Grace"

    def test_phosphor_pulse_versions(self):
        v0: DamageInstance = PhosphorPulse().execute()
        v3: DamageInstance = PhosphorPulseV3().execute()

        assert v0.base_potency == 40
        assert v3.base_potency == 80
        assert DamageTag.PASSIVE in v3.tags


class TestLoreleyFortification:
    def test_set_to_v0(self):
        doll: Loreley = Loreley()
        doll.set_to_v0()

        assert isinstance(doll.scorching_brand, ScorchingBrand)
        assert isinstance(doll.crimson_binding_decree, CrimsonBindingDecree)
        assert isinstance(doll.phosphor_pulse, PhosphorPulse)

    def test_set_to_v3(self):
        doll: Loreley = Loreley()
        doll.set_to_v3()

        assert isinstance(doll.phosphor_pulse, PhosphorPulseV3)

    def test_set_to_v4(self):
        doll: Loreley = Loreley()
        doll.set_to_v4()

        assert isinstance(doll.crimson_binding_decree, CrimsonBindingDecreeV4)

    def test_set_to_v5(self):
        doll: Loreley = Loreley()
        doll.set_to_v5()

        assert isinstance(doll.scorching_brand, ScorchingBrandV5)

    def test_set_fortification_level(self):
        doll: Loreley = Loreley()

        doll.set_fortification_level(FortificationLevel.SEGMENT00)
        assert isinstance(doll.scorching_brand, ScorchingBrand)

        doll.set_fortification_level(FortificationLevel.SEGMENT03)
        assert isinstance(doll.phosphor_pulse, PhosphorPulseV3)

        doll.set_fortification_level(FortificationLevel.SEGMENT04)
        assert isinstance(doll.crimson_binding_decree, CrimsonBindingDecreeV4)

        doll.set_fortification_level(FortificationLevel.SEGMENT05)
        assert isinstance(doll.scorching_brand, ScorchingBrandV5)

        doll.set_fortification_level(FortificationLevel.SEGMENT06)
        assert doll.fortification_level == FortificationLevel.SEGMENT06
