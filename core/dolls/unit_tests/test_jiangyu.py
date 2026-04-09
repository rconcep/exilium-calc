from core.dolls.jiangyu import *

from core.types import DamageTag, ModifierType, SpecialAttribute, FortificationLevel
from core.buffs import Buff, AttackUpII
from core.combat import DamageInstance


class TestJiangyuSkills:
    def test_form_intention_fist(self):
        result: DamageInstance = FormIntentionFist().execute()

        assert result.base_potency == 80
        assert DamageTag.ACTIVE in result.tags
        assert DamageTag.BASIC in result.tags
        assert DamageTag.MEDIUM_AMMO in result.tags
        assert DamageTag.TARGETED in result.tags
        assert DamageTag.PHYSICAL in result.tags
        assert result.buffs_before == []

    def test_thunderclap(self):
        result: DamageInstance = Thunderclap().execute()

        assert result.base_potency == 90
        assert DamageTag.ACTIVE in result.tags
        assert DamageTag.MELEE in result.tags
        assert DamageTag.AREA_OF_EFFECT in result.tags
        assert DamageTag.ELECTRIC in result.tags
        assert DamageTag.PHASE in result.tags
        assert result.buffs_before == []

    def test_lightning_smash(self):
        result: DamageInstance = LightningSmash().execute()

        assert result.base_potency == 110
        assert DamageTag.ACTIVE in result.tags
        assert DamageTag.TARGETED in result.tags
        assert DamageTag.ELECTRIC in result.tags
        assert DamageTag.PHASE in result.tags
        assert result.buffs_before == []

    def test_lightning_smash_v3_has_voltage_sag_damage_boost(self):
        result: DamageInstance = LightningSmashV3().execute()

        assert result.base_potency == 140
        assert DamageTag.ELECTRIC in result.tags
        assert DamageTag.PHASE in result.tags
        assert len(result.buffs_before) == 1
        assert result.buffs_before[0] == Buff(
            value=30,
            modifier_type=ModifierType.ADDITIVE,
            stat_type=SpecialAttribute.DAMAGE_BOOST,
            tag=DamageTag.ALL,
        )

    def test_lightning_smash_v5_has_voltage_sag_damage_boost(self):
        result: DamageInstance = LightningSmashV5().execute()

        assert result.base_potency == 140
        assert DamageTag.ELECTRIC in result.tags
        assert DamageTag.PHASE in result.tags
        assert len(result.buffs_before) == 1
        assert result.buffs_before[0] == Buff(
            value=30,
            modifier_type=ModifierType.ADDITIVE,
            stat_type=SpecialAttribute.DAMAGE_BOOST,
            tag=DamageTag.ALL,
        )

    def test_rolling_thunder(self):
        result: DamageInstance = RollingThunder().execute()

        assert result.base_potency == 130
        assert DamageTag.ACTIVE in result.tags
        assert DamageTag.ULTIMATE in result.tags
        assert DamageTag.ELECTRIC in result.tags
        assert DamageTag.PHASE in result.tags
        assert DamageTag.MEDIUM_AMMO in result.tags
        assert DamageTag.TARGETED in result.tags

    def test_interception(self):
        result: DamageInstance = Interception().execute()

        assert result.base_potency == 60
        assert DamageTag.PASSIVE in result.tags
        assert DamageTag.INTERCEPTION in result.tags
        assert DamageTag.MEDIUM_AMMO in result.tags
        assert DamageTag.TARGETED in result.tags
        assert DamageTag.ELECTRIC in result.tags
        assert DamageTag.PHASE in result.tags

    def test_support_action_not_in_stability_break(self):
        result: DamageInstance = SupportAction().execute(
            target_is_in_stability_break=False
        )

        assert result.base_potency == 45
        assert DamageTag.PASSIVE in result.tags
        assert DamageTag.SUPPORT_ACTION in result.tags
        assert DamageTag.ELECTRIC in result.tags

    def test_support_action_in_stability_break(self):
        result: DamageInstance = SupportAction().execute(
            target_is_in_stability_break=True
        )

        assert result.base_potency == 75
        assert DamageTag.PASSIVE in result.tags
        assert DamageTag.SUPPORT_ACTION in result.tags
        assert DamageTag.ELECTRIC in result.tags

    def test_urge_to_perform(self):
        result: DamageInstance = UrgeToPerform().execute()

        assert result.base_potency == 90
        assert DamageTag.PASSIVE in result.tags
        assert DamageTag.TARGETED in result.tags
        assert DamageTag.ELECTRIC in result.tags
        assert DamageTag.PHASE in result.tags


class TestJiangyu:
    def test_set_to_v0(self):
        jy: Jiangyu = Jiangyu()
        jy.set_to_v0()

        assert isinstance(jy.form_intention_fist, FormIntentionFist)
        assert isinstance(jy.thunderclap, Thunderclap)
        assert isinstance(jy.lightning_smash, LightningSmash)
        assert isinstance(jy.rolling_thunder, RollingThunder)
        assert isinstance(jy.interception, Interception)
        assert isinstance(jy.support_action, SupportAction)
        assert isinstance(jy.urge_to_perform, UrgeToPerform)

    def test_set_to_v3(self):
        jy: Jiangyu = Jiangyu()
        jy.set_to_v3()

        assert isinstance(jy.thunderclap, Thunderclap)
        assert isinstance(jy.lightning_smash, LightningSmashV3)

    def test_set_to_v4(self):
        jy: Jiangyu = Jiangyu()
        jy.set_to_v4()

        assert isinstance(jy.thunderclap, ThunderclapV4)
        assert isinstance(jy.lightning_smash, LightningSmashV3)

    def test_set_to_v5(self):
        jy: Jiangyu = Jiangyu()
        jy.set_to_v5()

        assert isinstance(jy.thunderclap, ThunderclapV4)
        assert isinstance(jy.lightning_smash, LightningSmashV5)

    def test_set_to_v6_uses_v5_abilities(self):
        jy: Jiangyu = Jiangyu()
        jy.set_to_v6()

        assert isinstance(jy.thunderclap, ThunderclapV4)
        assert isinstance(jy.lightning_smash, LightningSmashV5)

    def test_set_fortification_level_segment06(self):
        jy: Jiangyu = Jiangyu()
        jy.set_fortification_level(FortificationLevel.SEGMENT06)

        assert isinstance(jy.thunderclap, ThunderclapV4)
        assert isinstance(jy.lightning_smash, LightningSmashV5)

    def test_set_fortification_level_segment03(self):
        jy: Jiangyu = Jiangyu()
        jy.set_fortification_level(FortificationLevel.SEGMENT03)

        assert isinstance(jy.thunderclap, Thunderclap)
        assert isinstance(jy.lightning_smash, LightningSmashV3)

    def test_set_fortification_level_segment04(self):
        jy: Jiangyu = Jiangyu()
        jy.set_fortification_level(FortificationLevel.SEGMENT04)

        assert isinstance(jy.thunderclap, ThunderclapV4)
        assert isinstance(jy.lightning_smash, LightningSmashV3)
