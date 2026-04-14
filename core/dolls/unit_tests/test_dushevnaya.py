from core.buffs import Buff
from core.dolls.dushevnaya import (
    Daybreak,
    Dushevnaya,
    HerosCode,
    HerosCodeV4,
    MarzannasSanction,
    MarzannasSanctionV3,
    SupportAction,
)
from core.types import (
    DamageTag,
    FortificationLevel,
    ModifierType,
    SpecialAttribute,
    StatType,
)


class TestDushevnayaSkills:
    def test_daybreak(self):
        result = Daybreak().execute()

        assert result.base_potency == 80
        assert result.tags == {
            DamageTag.ACTIVE,
            DamageTag.BASIC,
            DamageTag.HEAVY_AMMO,
            DamageTag.TARGETED,
            DamageTag.FREEZE,
            DamageTag.PHASE,
        }

    def test_heros_code_without_enhancement(self):
        result = HerosCode().execute(
            stacks_of_ices_grace=3,
            target_on_freeze_tile=False,
            has_fixed_key_1=False,
        )

        assert result.base_potency == 110
        assert result.buffs_before == []
        assert DamageTag.FREEZE in result.tags
        assert DamageTag.PHASE in result.tags

    def test_heros_code_on_freeze_tile_at_max_stacks(self):
        result = HerosCode().execute(
            stacks_of_ices_grace=4,
            target_on_freeze_tile=True,
            has_fixed_key_1=False,
        )

        assert result.base_potency == 130
        assert result.buffs_before == []
        assert DamageTag.FREEZE in result.tags
        assert DamageTag.PHASE in result.tags

    def test_heros_code_applies_fixed_key_crit_rate_buff(self):
        result = HerosCode().execute(
            stacks_of_ices_grace=6,
            target_on_freeze_tile=False,
            has_fixed_key_1=True,
        )

        assert result.base_potency == 110
        assert result.buffs_before == [
            Buff(10, ModifierType.ADDITIVE, StatType.CRIT_RATE)
        ]

    def test_heros_code_caps_fixed_key_crit_rate_buff(self):
        result = HerosCode().execute(
            stacks_of_ices_grace=12,
            target_on_freeze_tile=False,
            has_fixed_key_1=True,
        )

        assert result.buffs_before == [
            Buff(30, ModifierType.ADDITIVE, StatType.CRIT_RATE)
        ]

    def test_heros_code_v4_enhancement(self):
        result = HerosCodeV4().execute(
            stacks_of_ices_grace=4,
            target_on_freeze_tile=False,
            has_fixed_key_1=False,
        )
        assert result.base_potency == 140

        result = HerosCodeV4().execute(
            stacks_of_ices_grace=4,
            target_on_freeze_tile=True,
            has_fixed_key_1=False,
        )
        assert result.base_potency == 160

    def test_marzannas_sanction(self):
        result = MarzannasSanction().execute(is_enhanced=False)
        assert result.base_potency == 50
        assert DamageTag.AREA_OF_EFFECT in result.tags
        assert DamageTag.CONFECTANCE in result.tags

        result = MarzannasSanction().execute(is_enhanced=True)
        assert result.base_potency == 70

    def test_marzannas_sanction_v3(self):
        result = MarzannasSanctionV3().execute(is_enhanced=False)
        assert result.base_potency == 70

        result = MarzannasSanctionV3().execute(is_enhanced=True)
        assert result.base_potency == 90

    def test_support_action(self):
        result = SupportAction().execute()

        assert result.base_potency == 80
        assert result.tags == {
            DamageTag.PASSIVE,
            DamageTag.SUPPORT_ACTION,
            DamageTag.HEAVY_AMMO,
            DamageTag.TARGETED,
            DamageTag.FREEZE,
            DamageTag.PHASE,
        }


class TestDushevnaya:
    def test_set_to_v0(self):
        doll = Dushevnaya()
        doll.set_to_v0()

        assert isinstance(doll.daybreak, Daybreak)
        assert isinstance(doll.heros_code, HerosCode)
        assert isinstance(doll.marzannas_sanction, MarzannasSanction)
        assert isinstance(doll.support_action, SupportAction)
        assert (
            doll.initial_stats.special_attributes[
                SpecialAttribute.DAMAGE_BOOST
            ].get_multiplier(DamageTag.ALL)
            == 10
        )
        assert (
            doll.initial_stats.special_attributes[
                SpecialAttribute.DAMAGE_BOOST
            ].get_multiplier(DamageTag.FREEZE)
            == 15
        )
        assert (
            doll.initial_stats.special_attributes[
                SpecialAttribute.DAMAGE_BOOST
            ].get_multiplier(DamageTag.TARGETED)
            == 20
        )
        assert (
            doll.initial_stats.special_attributes[
                SpecialAttribute.DEFENSE_IGNORE
            ].get_multiplier(DamageTag.TARGETED)
            == 30
        )

    def test_set_to_v3(self):
        doll = Dushevnaya()
        doll.set_to_v3()

        assert isinstance(doll.heros_code, HerosCode)
        assert isinstance(doll.marzannas_sanction, MarzannasSanctionV3)

    def test_set_to_v4(self):
        doll = Dushevnaya()
        doll.set_to_v4()

        assert isinstance(doll.heros_code, HerosCodeV4)
        assert isinstance(doll.marzannas_sanction, MarzannasSanctionV3)

    def test_set_to_v6(self):
        doll = Dushevnaya()
        doll.set_to_v6()

        assert isinstance(doll.heros_code, HerosCodeV4)
        assert (
            doll.initial_stats.special_attributes[
                SpecialAttribute.DAMAGE_BOOST
            ].get_multiplier(DamageTag.ALL)
            == 20
        )
        assert (
            doll.initial_stats.special_attributes[
                SpecialAttribute.DAMAGE_BOOST
            ].get_multiplier(DamageTag.FREEZE)
            == 45
        )

    def test_set_fortification_level(self):
        doll = Dushevnaya()
        doll.set_fortification_level(FortificationLevel.SEGMENT05)

        assert isinstance(doll.heros_code, HerosCodeV4)
        assert isinstance(doll.marzannas_sanction, MarzannasSanctionV3)
