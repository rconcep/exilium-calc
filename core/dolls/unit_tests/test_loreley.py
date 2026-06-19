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

    def test_searing_brand_without_blazing_embers(self):
        result: DamageInstance = SearingBrand().execute(
            has_blazing_embers=False,
            target_on_burn_tile=False,
        )

        assert result.base_potency == 130
        assert DamageTag.BURN in result.tags
        assert DamageTag.PHASE in result.tags
        assert result.group_name == "Searing Brand"

    def test_searing_brand_with_blazing_embers(self):
        result: DamageInstance = SearingBrand().execute(
            has_blazing_embers=True,
            target_on_burn_tile=False,
        )

        assert result.base_potency == 260

    def test_searing_brand_v5_applies_defense_ignore(self):
        result: DamageInstance = SearingBrandV5().execute(
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

    def test_searing_brand_v5_on_burn_tile_adds_damage_buff(self):
        result: DamageInstance = SearingBrandV5().execute(
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

    def test_red_bound_declaration_splits_without_blazing_embers(self):
        result: DamageInstance = RedBoundDeclaration().execute(
            has_blazing_embers=False,
            number_of_targets=3,
            number_of_burn_buffs=0,
        )

        assert result.base_potency == 40

    def test_red_bound_declaration_no_split_with_blazing_embers(self):
        result: DamageInstance = RedBoundDeclaration().execute(
            has_blazing_embers=True,
            number_of_targets=3,
            number_of_burn_buffs=0,
        )

        assert result.base_potency == 120

    def test_red_bound_declaration_v4_burn_buff_cap(self):
        result: DamageInstance = RedBoundDeclarationV4().execute(
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

    def test_dolorous_grace(self):
        result: DamageInstance = DolorousGrace().execute()

        assert result.base_potency == 60
        assert DamageTag.ULTIMATE in result.tags
        assert DamageTag.AREA_OF_EFFECT in result.tags
        assert result.group_name == "Dolorous Grace"

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

        assert isinstance(doll.searing_brand, SearingBrand)
        assert isinstance(doll.red_bound_declaration, RedBoundDeclaration)
        assert isinstance(doll.phosphor_pulse, PhosphorPulse)

    def test_set_to_v3(self):
        doll: Loreley = Loreley()
        doll.set_to_v3()

        assert isinstance(doll.phosphor_pulse, PhosphorPulseV3)

    def test_set_to_v4(self):
        doll: Loreley = Loreley()
        doll.set_to_v4()

        assert isinstance(doll.red_bound_declaration, RedBoundDeclarationV4)

    def test_set_to_v5(self):
        doll: Loreley = Loreley()
        doll.set_to_v5()

        assert isinstance(doll.searing_brand, SearingBrandV5)

    def test_set_fortification_level(self):
        doll: Loreley = Loreley()

        doll.set_fortification_level(FortificationLevel.SEGMENT00)
        assert isinstance(doll.searing_brand, SearingBrand)

        doll.set_fortification_level(FortificationLevel.SEGMENT03)
        assert isinstance(doll.phosphor_pulse, PhosphorPulseV3)

        doll.set_fortification_level(FortificationLevel.SEGMENT04)
        assert isinstance(doll.red_bound_declaration, RedBoundDeclarationV4)

        doll.set_fortification_level(FortificationLevel.SEGMENT05)
        assert isinstance(doll.searing_brand, SearingBrandV5)

        doll.set_fortification_level(FortificationLevel.SEGMENT06)
        assert doll.fortification_level == FortificationLevel.SEGMENT06
