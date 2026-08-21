from core.dolls.nemesis_gnosis import *

from core.buffs import Buff
from core.types import (
    DamageTag,
    FortificationLevel,
    ModifierType,
    SpecialAttribute,
)


class TestNemesisGnosisSkills:
    def test_starfall(self):
        result = Starfall().execute()

        assert result.base_potency == 80
        assert result.tags == {
            DamageTag.ACTIVE,
            DamageTag.BASIC,
            DamageTag.HEAVY_AMMO,
            DamageTag.TARGETED,
            DamageTag.PHYSICAL,
        }
        assert result.group_name == "Starfall"

    def test_calamity_resonance(self):
        result = CalamityResonance().execute()

        assert result.base_potency == 80
        assert result.tags == {
            DamageTag.ACTIVE,
            DamageTag.HEAVY_AMMO,
            DamageTag.TARGETED,
            DamageTag.CORROSION,
        }
        assert result.group_name == "Calamity Resonance"

    def test_prismatic_refraction_base(self):
        result = PrismaticRefraction().execute(
            has_first_prophecy=False,
            has_second_prophecy=False,
            has_no_allies_nearby=False,
        )

        assert result.base_potency == 120
        assert result.tags == {
            DamageTag.ACTIVE,
            DamageTag.HEAVY_AMMO,
            DamageTag.TARGETED,
            DamageTag.CORROSION,
        }
        assert result.group_name == "Prismatic Refraction"
        assert result.buffs_before == []

    def test_prismatic_refraction_with_first_prophecy(self):
        result = PrismaticRefraction().execute(
            has_first_prophecy=True,
            has_second_prophecy=False,
            has_no_allies_nearby=False,
        )

        assert result.base_potency == 140

    def test_prismatic_refraction_with_second_prophecy_and_no_allies(self):
        result = PrismaticRefraction().execute(
            has_first_prophecy=False,
            has_second_prophecy=True,
            has_no_allies_nearby=True,
        )

        assert result.buffs_before == [
            Buff(
                20,
                modifier_type=ModifierType.ADDITIVE,
                stat_type=SpecialAttribute.DAMAGE_BOOST,
                tag=DamageTag.ALL,
            )
        ]

    def test_prismatic_refraction_second_prophecy_requires_no_allies(self):
        result = PrismaticRefraction().execute(
            has_first_prophecy=False,
            has_second_prophecy=True,
            has_no_allies_nearby=False,
        )

        assert result.buffs_before == []

    def test_prismatic_refraction_v4_with_first_prophecy(self):
        result = PrismaticRefractionV4().execute(
            has_first_prophecy=True,
            has_second_prophecy=False,
            has_no_allies_nearby=False,
        )

        assert result.base_potency == 160

    def test_prismatic_refraction_v4_with_second_prophecy_and_no_allies(self):
        result = PrismaticRefractionV4().execute(
            has_first_prophecy=False,
            has_second_prophecy=True,
            has_no_allies_nearby=True,
        )

        assert result.buffs_before == [
            Buff(
                40,
                modifier_type=ModifierType.ADDITIVE,
                stat_type=SpecialAttribute.DAMAGE_BOOST,
                tag=DamageTag.ALL,
            )
        ]

    def test_fates_reprise_base(self):
        result = FatesReprise().execute(
            confectance_index_consumed=0,
            has_fifth_prophecy=False,
            has_sixth_prophecy=False,
        )

        assert result.base_potency == 140
        assert result.label == "Fate's Reprise (0)"
        assert result.tags == {
            DamageTag.ACTIVE,
            DamageTag.CORROSION,
            DamageTag.HEAVY_AMMO,
            DamageTag.AREA_OF_EFFECT,
            DamageTag.CONFECTANCE,
            DamageTag.ULTIMATE,
        }
        assert result.group_name == "Fate's Reprise"
        assert result.buffs_before == []

    def test_fates_reprise_scales_with_confectance_index(self):
        result = FatesReprise().execute(
            confectance_index_consumed=4,
            has_fifth_prophecy=False,
            has_sixth_prophecy=False,
        )

        assert result.base_potency == 180

    def test_fates_reprise_caps_confectance_index_at_six(self):
        result = FatesReprise().execute(
            confectance_index_consumed=9,
            has_fifth_prophecy=False,
            has_sixth_prophecy=False,
        )

        assert result.base_potency == 200

    def test_fates_reprise_with_sixth_prophecy(self):
        result = FatesReprise().execute(
            confectance_index_consumed=3,
            has_fifth_prophecy=False,
            has_sixth_prophecy=True,
        )

        assert result.buffs_before == [
            Buff(
                value=30,
                modifier_type=ModifierType.ADDITIVE,
                stat_type=SpecialAttribute.DAMAGE_BOOST,
                tag=DamageTag.ALL,
            )
        ]

    def test_fates_reprise_v2_with_fifth_prophecy(self):
        result = FatesRepriseV2().execute(
            confectance_index_consumed=0,
            has_fifth_prophecy=True,
            has_sixth_prophecy=False,
        )

        assert result.buffs_before == [
            Buff(
                value=50,
                modifier_type=ModifierType.ADDITIVE,
                stat_type=SpecialAttribute.DAMAGE_BOOST,
                tag=DamageTag.ALL,
            )
        ]

    def test_fates_reprise_v2_with_fifth_and_sixth_prophecy(self):
        result = FatesRepriseV2().execute(
            confectance_index_consumed=2,
            has_fifth_prophecy=True,
            has_sixth_prophecy=True,
        )

        assert result.buffs_before == [
            Buff(
                value=20,
                modifier_type=ModifierType.ADDITIVE,
                stat_type=SpecialAttribute.DAMAGE_BOOST,
                tag=DamageTag.ALL,
            ),
            Buff(
                value=50,
                modifier_type=ModifierType.ADDITIVE,
                stat_type=SpecialAttribute.DAMAGE_BOOST,
                tag=DamageTag.ALL,
            ),
        ]

    def test_support_action(self):
        result = SupportAction().execute(has_judicial_privilege=False)

        assert result.base_potency == 60
        assert result.tags == {
            DamageTag.PASSIVE,
            DamageTag.SUPPORT_ACTION,
            DamageTag.HEAVY_AMMO,
            DamageTag.TARGETED,
            DamageTag.CORROSION,
            DamageTag.PHASE,
        }
        assert result.group_name == "Support Action"

    def test_support_action_with_judicial_privilege(self):
        result = SupportAction().execute(has_judicial_privilege=True)

        assert result.base_potency == 90

    def test_support_action_v1(self):
        result = SupportActionV1().execute(has_judicial_privilege=False)

        assert result.base_potency == 110

    def test_support_action_v1_with_judicial_privilege(self):
        result = SupportActionV1().execute(has_judicial_privilege=True)

        assert result.base_potency == 140

    def test_support_action_v5(self):
        result = SupportActionV5().execute(has_judicial_privilege=False)

        assert result.base_potency == 110

    def test_support_action_v5_with_judicial_privilege(self):
        result = SupportActionV5().execute(has_judicial_privilege=True)

        assert result.base_potency == 150

    def test_third_prophecy(self):
        result = ThirdProphecy().execute(triggered_out_of_turn=False)

        assert result.base_potency == 60
        assert result.tags == {
            DamageTag.PASSIVE,
            DamageTag.AREA_OF_EFFECT,
            DamageTag.CORROSION,
            DamageTag.PHASE,
        }
        assert result.group_name == "Third Prophecy"

    def test_third_prophecy_triggered_out_of_turn(self):
        result = ThirdProphecy().execute(triggered_out_of_turn=True)

        assert DamageTag.SUPPORT_ACTION in result.tags

    def test_third_prophecy_v5(self):
        result = ThirdProphecyV5().execute(triggered_out_of_turn=False)

        assert result.base_potency == 80

    def test_third_prophecy_v5_triggered_out_of_turn(self):
        result = ThirdProphecyV5().execute(triggered_out_of_turn=True)

        assert DamageTag.SUPPORT_ACTION in result.tags


class TestNemesisGnosis:
    def test_set_to_v0(self):
        doll = NemesisGnosis()
        doll.set_to_v0()

        assert isinstance(doll.starfall, Starfall)
        assert isinstance(doll.calamity_resonance, CalamityResonance)
        assert isinstance(doll.prismatic_refraction, PrismaticRefraction)
        assert isinstance(doll.fates_reprise, FatesReprise)
        assert isinstance(doll.support_action, SupportAction)
        assert isinstance(doll.third_prophecy, ThirdProphecy)

    def test_set_to_v1(self):
        doll = NemesisGnosis()
        doll.set_to_v1()

        assert isinstance(doll.support_action, SupportActionV1)
        assert isinstance(doll.fates_reprise, FatesReprise)

    def test_set_to_v2(self):
        doll = NemesisGnosis()
        doll.set_to_v2()

        assert isinstance(doll.support_action, SupportActionV1)
        assert isinstance(doll.fates_reprise, FatesRepriseV2)
        assert isinstance(doll.prismatic_refraction, PrismaticRefraction)

    def test_set_to_v4(self):
        doll = NemesisGnosis()
        doll.set_to_v4()

        assert isinstance(doll.fates_reprise, FatesRepriseV2)
        assert isinstance(doll.prismatic_refraction, PrismaticRefractionV4)
        assert isinstance(doll.third_prophecy, ThirdProphecy)

    def test_set_to_v5(self):
        doll = NemesisGnosis()
        doll.set_to_v5()

        assert isinstance(doll.prismatic_refraction, PrismaticRefractionV4)
        assert isinstance(doll.third_prophecy, ThirdProphecyV5)
        assert isinstance(doll.support_action, SupportActionV5)

    def test_set_fortification_level(self):
        doll = NemesisGnosis()

        doll.set_fortification_level(FortificationLevel.SEGMENT01)
        assert isinstance(doll.support_action, SupportActionV1)

        doll.set_fortification_level(FortificationLevel.SEGMENT02)
        assert isinstance(doll.fates_reprise, FatesRepriseV2)

        doll.set_fortification_level(FortificationLevel.SEGMENT03)
        assert isinstance(doll.fates_reprise, FatesRepriseV2)
        assert isinstance(doll.prismatic_refraction, PrismaticRefraction)

        doll.set_fortification_level(FortificationLevel.SEGMENT04)
        assert isinstance(doll.prismatic_refraction, PrismaticRefractionV4)

        doll.set_fortification_level(FortificationLevel.SEGMENT05)
        assert isinstance(doll.third_prophecy, ThirdProphecyV5)
        assert isinstance(doll.support_action, SupportActionV5)

        doll.set_fortification_level(FortificationLevel.SEGMENT06)
        assert isinstance(doll.third_prophecy, ThirdProphecyV5)
        assert isinstance(doll.support_action, SupportActionV5)
