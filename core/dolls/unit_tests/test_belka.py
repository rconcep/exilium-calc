from core.dolls.belka import *

from core.types import (
    DamageTag,
    ModifierType,
    SpecialAttribute,
    StatType,
    FortificationLevel,
)
from core.buffs import Buff
from core.combat import DamageInstance


class TestBelkaSkills:
    def test_nutcracker_shell_no_active_engagement(self):
        result: DamageInstance = NutcrackerShell().execute(has_active_engagement=False)

        assert result.base_potency == 80
        assert DamageTag.ACTIVE in result.tags
        assert DamageTag.BASIC in result.tags
        assert DamageTag.MEDIUM_AMMO in result.tags
        assert DamageTag.TARGETED in result.tags
        assert DamageTag.PHYSICAL in result.tags
        assert DamageTag.ELECTRIC not in result.tags
        assert DamageTag.PHASE not in result.tags
        assert result.buffs_before == []

    def test_nutcracker_shell_with_active_engagement(self):
        result: DamageInstance = NutcrackerShell().execute(has_active_engagement=True)

        assert result.base_potency == 80
        assert DamageTag.ELECTRIC in result.tags
        assert DamageTag.PHASE in result.tags
        assert DamageTag.PHYSICAL not in result.tags
        assert result.buffs_before == [
            Buff(
                value=ACTIVE_ENGAGEMENT_BUFF,
                modifier_type=ModifierType.ADDITIVE,
                stat_type=SpecialAttribute.DAMAGE_BOOST,
                tag=DamageTag.ELECTRIC,
            )
        ]

    def test_sylvan_vault_base(self):
        result: DamageInstance = SylvanVault().execute(
            has_active_engagement=False,
            number_positive_charge_on_field=0,
            number_negative_charge_on_field=0,
            target_is_boss_with_negative_charge=False,
        )

        assert result.base_potency == 130
        assert DamageTag.ACTIVE in result.tags
        assert DamageTag.CONFECTANCE in result.tags
        assert DamageTag.ELECTRIC in result.tags
        assert DamageTag.PHASE in result.tags
        assert result.buffs_before == []

    def test_sylvan_vault_with_active_engagement(self):
        result: DamageInstance = SylvanVault().execute(
            has_active_engagement=True,
            number_positive_charge_on_field=0,
            number_negative_charge_on_field=0,
            target_is_boss_with_negative_charge=False,
        )

        assert (
            Buff(
                value=ACTIVE_ENGAGEMENT_BUFF,
                modifier_type=ModifierType.ADDITIVE,
                stat_type=SpecialAttribute.DAMAGE_BOOST,
                tag=DamageTag.ALL,
            )
            in result.buffs_before
        )

    def test_sylvan_vault_boss_with_negative_charge(self):
        result: DamageInstance = SylvanVault().execute(
            has_active_engagement=False,
            number_positive_charge_on_field=0,
            number_negative_charge_on_field=0,
            target_is_boss_with_negative_charge=True,
        )

        assert (
            Buff(
                value=15,
                modifier_type=ModifierType.ADDITIVE,
                stat_type=SpecialAttribute.DAMAGE_BOOST,
                tag=DamageTag.ALL,
            )
            in result.buffs_before
        )

    def test_sylvan_vault_negative_charge_partial(self):
        result: DamageInstance = SylvanVault().execute(
            has_active_engagement=False,
            number_positive_charge_on_field=0,
            number_negative_charge_on_field=3,
            target_is_boss_with_negative_charge=False,
        )

        assert (
            Buff(
                value=9,
                modifier_type=ModifierType.ADDITIVE,
                stat_type=SpecialAttribute.DAMAGE_BOOST,
                tag=DamageTag.ALL,
            )
            in result.buffs_before
        )

    def test_sylvan_vault_negative_charge_capped(self):
        result: DamageInstance = SylvanVault().execute(
            has_active_engagement=False,
            number_positive_charge_on_field=0,
            number_negative_charge_on_field=6,
            target_is_boss_with_negative_charge=False,
        )

        assert (
            Buff(
                value=15,
                modifier_type=ModifierType.ADDITIVE,
                stat_type=SpecialAttribute.DAMAGE_BOOST,
                tag=DamageTag.ALL,
            )
            in result.buffs_before
        )

    def test_sylvan_vault_positive_charge_crit_damage(self):
        result: DamageInstance = SylvanVault().execute(
            has_active_engagement=False,
            number_positive_charge_on_field=5,
            number_negative_charge_on_field=0,
            target_is_boss_with_negative_charge=False,
        )

        assert (
            Buff(
                value=25,
                modifier_type=ModifierType.ADDITIVE,
                stat_type=SpecialAttribute.CRITICAL_DAMAGE,
                tag=DamageTag.ALL,
            )
            in result.buffs_before
        )

    def test_sylvan_vault_positive_charge_crit_damage_capped(self):
        result: DamageInstance = SylvanVault().execute(
            has_active_engagement=False,
            number_positive_charge_on_field=10,
            number_negative_charge_on_field=0,
            target_is_boss_with_negative_charge=False,
        )

        assert (
            Buff(
                value=25,
                modifier_type=ModifierType.ADDITIVE,
                stat_type=SpecialAttribute.CRITICAL_DAMAGE,
                tag=DamageTag.ALL,
            )
            in result.buffs_before
        )

    def test_sylvan_vault_v5_negative_charge_doubled(self):
        result: DamageInstance = SylvanVaultV5().execute(
            has_active_engagement=False,
            number_positive_charge_on_field=0,
            number_negative_charge_on_field=3,
            target_is_boss_with_negative_charge=False,
        )

        assert (
            Buff(
                value=18,
                modifier_type=ModifierType.ADDITIVE,
                stat_type=SpecialAttribute.DAMAGE_BOOST,
                tag=DamageTag.ALL,
            )
            in result.buffs_before
        )

    def test_sylvan_vault_v5_boss_negative_charge_cap(self):
        result: DamageInstance = SylvanVaultV5().execute(
            has_active_engagement=False,
            number_positive_charge_on_field=0,
            number_negative_charge_on_field=0,
            target_is_boss_with_negative_charge=True,
        )

        assert (
            Buff(
                value=30,
                modifier_type=ModifierType.ADDITIVE,
                stat_type=SpecialAttribute.DAMAGE_BOOST,
                tag=DamageTag.ALL,
            )
            in result.buffs_before
        )

    def test_sylvan_vault_v5_extra_crit_damage_buff(self):
        result: DamageInstance = SylvanVaultV5().execute(
            has_active_engagement=False,
            number_positive_charge_on_field=0,
            number_negative_charge_on_field=0,
            target_is_boss_with_negative_charge=False,
        )

        assert (
            Buff(
                value=30,
                modifier_type=ModifierType.ADDITIVE,
                stat_type=SpecialAttribute.CRITICAL_DAMAGE,
                tag=DamageTag.ALL,
            )
            in result.buffs_before
        )

    def test_crackling_core_base_potency_minimum_mobility(self):
        result: DamageInstance = CracklingCore().execute(
            has_active_engagement=False,
            mobility_expended=5,
            has_fixed_key_4=False,
            target_has_negative_charge=False,
        )

        # mobility min 10: 130 + 10*5 = 180
        assert result.base_potency == 180

    def test_crackling_core_base_potency_full_mobility(self):
        result: DamageInstance = CracklingCore().execute(
            has_active_engagement=False,
            mobility_expended=15,
            has_fixed_key_4=False,
            target_has_negative_charge=False,
        )

        # 130 + 15*5 = 205
        assert result.base_potency == 205

    def test_crackling_core_with_active_engagement(self):
        result: DamageInstance = CracklingCore().execute(
            has_active_engagement=True,
            mobility_expended=10,
            has_fixed_key_4=False,
            target_has_negative_charge=False,
        )

        assert (
            Buff(
                value=ACTIVE_ENGAGEMENT_BUFF,
                modifier_type=ModifierType.ADDITIVE,
                stat_type=SpecialAttribute.DAMAGE_BOOST,
                tag=DamageTag.ALL,
            )
            in result.buffs_before
        )

    def test_crackling_core_fixed_key_4_with_negative_charge(self):
        result: DamageInstance = CracklingCore().execute(
            has_active_engagement=False,
            mobility_expended=10,
            has_fixed_key_4=True,
            target_has_negative_charge=True,
        )

        assert (
            Buff(
                value=10,
                modifier_type=ModifierType.MULTIPLICATIVE,
                stat_type=StatType.ATTACK,
                tag=DamageTag.ALL,
            )
            in result.buffs_before
        )

    def test_crackling_core_fixed_key_4_without_negative_charge(self):
        result: DamageInstance = CracklingCore().execute(
            has_active_engagement=False,
            mobility_expended=10,
            has_fixed_key_4=True,
            target_has_negative_charge=False,
        )

        assert result.buffs_before == []

    def test_crackling_core_v1_potency_minimum_mobility(self):
        result: DamageInstance = CracklingCoreV1().execute(
            has_active_engagement=False,
            mobility_expended=5,
            has_fixed_key_4=False,
            target_has_negative_charge=False,
        )

        # mobility min 10: 130 + 10*8 = 210
        assert result.base_potency == 210

    def test_crackling_core_v1_potency_full_mobility(self):
        result: DamageInstance = CracklingCoreV1().execute(
            has_active_engagement=False,
            mobility_expended=15,
            has_fixed_key_4=False,
            target_has_negative_charge=False,
        )

        # 130 + 15*8 = 250
        assert result.base_potency == 250

    def test_crackling_core_v1_negative_charge_damage_boost(self):
        result: DamageInstance = CracklingCoreV1().execute(
            has_active_engagement=False,
            mobility_expended=10,
            has_fixed_key_4=False,
            target_has_negative_charge=True,
        )

        assert (
            Buff(
                value=15,
                modifier_type=ModifierType.ADDITIVE,
                stat_type=SpecialAttribute.DAMAGE_BOOST,
                tag=DamageTag.ALL,
            )
            in result.buffs_before
        )

    def test_leaping_arc_potency_minimum_mobility(self):
        result: DamageInstance = LeapingArc().execute(
            mobility_expended=5,
            number_of_electric_debuffs_on_target=0,
        )

        # mobility min 10: 160 + 10*5 = 210
        assert result.base_potency == 210

    def test_leaping_arc_potency_full_mobility(self):
        result: DamageInstance = LeapingArc().execute(
            mobility_expended=10,
            number_of_electric_debuffs_on_target=0,
        )

        assert result.base_potency == 210
        assert DamageTag.ACTIVE in result.tags
        assert DamageTag.ELECTRIC in result.tags
        assert DamageTag.PHASE in result.tags

    def test_leaping_arc_v6_potency_minimum_mobility(self):
        result: DamageInstance = LeapingArcV6().execute(
            mobility_expended=5,
            number_of_electric_debuffs_on_target=0,
        )

        # mobility min 10: 160 + 10*10 = 260
        assert result.base_potency == 260

    def test_leaping_arc_v6_crit_damage_with_two_electric_debuffs(self):
        result: DamageInstance = LeapingArcV6().execute(
            mobility_expended=10,
            number_of_electric_debuffs_on_target=2,
        )

        assert (
            Buff(
                value=30,
                modifier_type=ModifierType.ADDITIVE,
                stat_type=SpecialAttribute.CRITICAL_DAMAGE,
                tag=DamageTag.ALL,
            )
            in result.buffs_before
        )

    def test_leaping_arc_v6_no_crit_damage_with_one_electric_debuff(self):
        result: DamageInstance = LeapingArcV6().execute(
            mobility_expended=10,
            number_of_electric_debuffs_on_target=1,
        )

        assert result.buffs_before == []

    def test_continual_release_tags_and_potency(self):
        result: DamageInstance = ContinualRelease().execute()

        assert result.base_potency == 80
        assert DamageTag.PASSIVE in result.tags
        assert DamageTag.TARGETED in result.tags
        assert DamageTag.ELECTRIC in result.tags
        assert DamageTag.PHASE in result.tags

    def test_continual_release_v6_potency(self):
        result: DamageInstance = ContinualReleaseV6().execute()

        assert result.base_potency == 110

    def test_overflowing_electrons_base_potency_zero(self):
        result: DamageInstance = OverflowingElectrons().execute()

        assert result.base_potency == 0

    def test_overflowing_electrons_v2_potency(self):
        result: DamageInstance = OverflowingElectronsV2().execute()

        assert result.base_potency == 100


class TestBelkaFortification:
    def test_set_to_v0(self):
        belka: Belka = Belka()
        belka.set_to_v0()

        assert isinstance(belka.nutcracker_shell, NutcrackerShell)
        assert isinstance(belka.sylvan_vault, SylvanVault)
        assert isinstance(belka.crackling_core, CracklingCore)
        assert isinstance(belka.leaping_arc, LeapingArc)
        assert isinstance(belka.continual_release, ContinualRelease)
        assert isinstance(belka.overflowing_electrons, OverflowingElectrons)

    def test_set_to_v1(self):
        belka: Belka = Belka()
        belka.set_to_v1()

        assert isinstance(belka.crackling_core, CracklingCoreV1)
        assert isinstance(belka.leaping_arc, LeapingArc)
        assert isinstance(belka.continual_release, ContinualRelease)
        assert isinstance(belka.overflowing_electrons, OverflowingElectrons)

    def test_set_to_v2(self):
        belka: Belka = Belka()
        belka.set_to_v2()

        assert isinstance(belka.crackling_core, CracklingCoreV1)
        assert isinstance(belka.overflowing_electrons, OverflowingElectronsV2)

    def test_set_to_v5(self):
        belka: Belka = Belka()
        belka.set_to_v5()

        assert isinstance(belka.sylvan_vault, SylvanVaultV5)
        assert isinstance(belka.crackling_core, CracklingCoreV1)
        assert isinstance(belka.overflowing_electrons, OverflowingElectronsV2)
        assert isinstance(belka.leaping_arc, LeapingArc)
        assert isinstance(belka.continual_release, ContinualRelease)

    def test_set_to_v6(self):
        belka: Belka = Belka()
        belka.set_to_v6()

        assert isinstance(belka.sylvan_vault, SylvanVaultV5)
        assert isinstance(belka.crackling_core, CracklingCoreV1)
        assert isinstance(belka.overflowing_electrons, OverflowingElectronsV2)
        assert isinstance(belka.leaping_arc, LeapingArcV6)
        assert isinstance(belka.continual_release, ContinualReleaseV6)

    def test_set_fortification_level_segment00(self):
        belka: Belka = Belka()
        belka.set_fortification_level(FortificationLevel.SEGMENT00)

        assert isinstance(belka.crackling_core, CracklingCore)
        assert isinstance(belka.sylvan_vault, SylvanVault)

    def test_set_fortification_level_segment01(self):
        belka: Belka = Belka()
        belka.set_fortification_level(FortificationLevel.SEGMENT01)

        assert isinstance(belka.crackling_core, CracklingCoreV1)
        assert isinstance(belka.overflowing_electrons, OverflowingElectrons)

    def test_set_fortification_level_segment02(self):
        belka: Belka = Belka()
        belka.set_fortification_level(FortificationLevel.SEGMENT02)

        assert isinstance(belka.overflowing_electrons, OverflowingElectronsV2)

    def test_set_fortification_level_segment03_same_as_v2(self):
        belka: Belka = Belka()
        belka.set_fortification_level(FortificationLevel.SEGMENT03)

        assert isinstance(belka.crackling_core, CracklingCoreV1)
        assert isinstance(belka.overflowing_electrons, OverflowingElectronsV2)
        assert isinstance(belka.leaping_arc, LeapingArc)

    def test_set_fortification_level_segment05(self):
        belka: Belka = Belka()
        belka.set_fortification_level(FortificationLevel.SEGMENT05)

        assert isinstance(belka.sylvan_vault, SylvanVaultV5)
        assert isinstance(belka.leaping_arc, LeapingArc)
        assert isinstance(belka.continual_release, ContinualRelease)

    def test_set_fortification_level_segment06(self):
        belka: Belka = Belka()
        belka.set_fortification_level(FortificationLevel.SEGMENT06)

        assert isinstance(belka.sylvan_vault, SylvanVaultV5)
        assert isinstance(belka.crackling_core, CracklingCoreV1)
        assert isinstance(belka.overflowing_electrons, OverflowingElectronsV2)
        assert isinstance(belka.leaping_arc, LeapingArcV6)
        assert isinstance(belka.continual_release, ContinualReleaseV6)
