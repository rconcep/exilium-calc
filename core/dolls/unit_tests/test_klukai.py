from core.dolls.klukai import *

from core.types import (
    DamageTag,
    ModifierType,
    SpecialAttribute,
    StatType,
    FortificationLevel,
)
from core.buffs import Buff, Debuff, DefenseDownII
from core.combat import DamageInstance


class TestKlukaiSkills:
    def test_swift_strike(self):
        result: DamageInstance = SwiftStrike().execute()

        assert result.base_potency == 80
        assert DamageTag.ACTIVE in result.tags
        assert DamageTag.BASIC in result.tags
        assert DamageTag.MEDIUM_AMMO in result.tags
        assert DamageTag.TARGETED in result.tags
        assert DamageTag.PHYSICAL in result.tags

    def test_pinpoint_detonation_second_v4_scales_with_stacks(self):
        result: DamageInstance = PinpointDetonationSecondV4().execute(
            stacks_corrosion_infusion=7
        )

        assert result.base_potency == 95

    def test_overpowering_corrosion_with_toxic_infiltration(self):
        result: DamageInstance = OverpoweringCorrosion().execute(
            target_has_toxic_infiltration=True
        )

        assert result.base_potency == 90
        assert result.buffs_before == [
            Buff(
                value=15,
                modifier_type=ModifierType.ADDITIVE,
                stat_type=SpecialAttribute.DAMAGE_BOOST,
                tag=DamageTag.ALL,
            )
        ]

    def test_devastating_drift_v3_boss_with_fixed_key_2(self):
        result: DamageInstance = DevastatingDriftV3().execute(
            number_targets_hit=1,
            target_is_boss=True,
            has_fixed_key_2=True,
            has_fixed_key_5=False,
        )

        assert result.base_potency == 100
        assert result.buffs_before == [
            Buff(
                value=30,
                modifier_type=ModifierType.ADDITIVE,
                stat_type=SpecialAttribute.DAMAGE_BOOST,
                tag=DamageTag.ONLY_HIT_ONE_TARGET,
            ),
            Buff(
                value=50,
                modifier_type=ModifierType.ADDITIVE,
                stat_type=SpecialAttribute.DAMAGE_BOOST,
                tag=DamageTag.ALL,
            ),
        ]
        assert DefenseDownII() in result.debuffs_before

    def test_devastating_drift_v6_fixed_key_5_buff(self):
        result: DamageInstance = DevastatingDriftV6().execute(
            number_targets_hit=1,
            target_is_boss=False,
            has_fixed_key_2=False,
            has_fixed_key_5=True,
        )

        assert result.buffs_before[0] == Buff(
            value=40,
            modifier_type=ModifierType.ADDITIVE,
            stat_type=SpecialAttribute.DAMAGE_BOOST,
            tag=DamageTag.ALL,
        )

    def test_corrosive_infusion_v2_caps_stacks_and_applies_defense_debuff(self):
        result: DamageInstance = CorrosiveInfusionV2().execute(stacks=20)

        assert result.base_potency == 180
        assert result.debuffs_before == [
            Debuff(
                value=-15,
                modifier_type=ModifierType.MULTIPLICATIVE,
                stat_type=StatType.DEFENSE,
                tag=DamageTag.ALL,
            )
        ]

    def test_toxic_infiltration_v5(self):
        result: DamageInstance = ToxicInfiltrationV5().execute()

        assert result.base_potency == 80
        assert DamageTag.PASSIVE in result.tags
        assert DamageTag.CORROSION in result.tags


class TestKlukaiFortification:
    def test_set_to_v0(self):
        klukai: Klukai = Klukai()
        klukai.set_to_v0()

        assert isinstance(klukai.pinpoint_detonation_first, PinpointDetonationFirst)
        assert isinstance(klukai.pinpoint_detonation_second, PinpointDetonationSecond)
        assert isinstance(klukai.overpowering_corrosion, OverpoweringCorrosion)
        assert isinstance(klukai.devastating_drift, DevastatingDrift)
        assert isinstance(klukai.corrosive_infusion, CorrosiveInfusion)
        assert isinstance(klukai.toxic_infiltration, ToxicInfiltration)

    def test_set_to_v6(self):
        klukai: Klukai = Klukai()
        klukai.set_to_v6()

        assert isinstance(klukai.pinpoint_detonation_first, PinpointDetonationFirstV4)
        assert isinstance(klukai.pinpoint_detonation_second, PinpointDetonationSecondV4)
        assert isinstance(klukai.overpowering_corrosion, OverpoweringCorrosionV5)
        assert isinstance(klukai.devastating_drift, DevastatingDriftV6)
        assert isinstance(klukai.corrosive_infusion, CorrosiveInfusionV2)
        assert isinstance(klukai.toxic_infiltration, ToxicInfiltrationV5)

    def test_set_fortification_level_v3(self):
        klukai: Klukai = Klukai()
        klukai.set_fortification_level(FortificationLevel.SEGMENT03)

        assert isinstance(klukai.overpowering_corrosion, OverpoweringCorrosionV1)
        assert isinstance(klukai.devastating_drift, DevastatingDriftV3)
        assert isinstance(klukai.corrosive_infusion, CorrosiveInfusionV2)
