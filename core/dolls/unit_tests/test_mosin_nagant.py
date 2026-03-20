from core.dolls.mosin_nagant import *

from core.types import DamageTag, SpecialAttribute, StatType, FortificationLevel
from core.combat import DamageInstance


class TestMosinNagantSkills:
    def test_patrol_time(self):
        di: DamageInstance = PatrolTime().execute(has_active_engagement=False)

        assert di.base_potency == 80
        assert DamageTag.PHYSICAL in di.tags
        assert DamageTag.HEAVY_AMMO in di.tags

        di: DamageInstance = PatrolTime().execute(has_active_engagement=True)

        assert DamageTag.ELECTRIC in di.tags
        assert DamageTag.PHASE in di.tags
        assert di.buffs_before[0] == Buff(
            ACTIVE_ENGAGEMENT_BUFF, ModifierType.ADDITIVE, SpecialAttribute.DAMAGE_BOOST, DamageTag.ELECTRIC
        )

    def test_target_victory(self):
        di: DamageInstance = TargetVictory().execute(has_active_engagement=True)

        assert di.base_potency == 130
        assert DamageTag.PHYSICAL not in di.tags
        assert DamageTag.CONFECTANCE in di.tags

    def test_declaration_of_victory(self):
        di: DamageInstance = DeclarationOfVictory().execute(has_active_engagement=True)

        assert di.base_potency == 180
        assert DamageTag.ULTIMATE in di.tags

    def test_support_action(self):
        di: DamageInstance = SupportAction().execute(has_active_engagement=True)

        assert di.base_potency == 80
        assert DamageTag.PASSIVE in di.tags
        assert DamageTag.SUPPORT_ACTION in di.tags

    def test_patrol_time_v5(self):
        di: DamageInstance = PatrolTimeV5().execute(has_active_engagement=False)

        assert di.base_potency == 80
        assert DamageTag.PHYSICAL in di.tags
        assert DamageTag.HEAVY_AMMO in di.tags

        di: DamageInstance = PatrolTimeV5().execute(has_active_engagement=True)

        assert DamageTag.ELECTRIC in di.tags
        assert DamageTag.PHASE in di.tags
        assert di.buffs_before[0] == Buff(
            ACTIVE_ENGAGEMENT_BUFF_V5, ModifierType.ADDITIVE, SpecialAttribute.DAMAGE_BOOST, DamageTag.ELECTRIC
        )

    def test_target_victory_v5(self):
        di: DamageInstance = TargetVictoryV5().execute(has_active_engagement=True)

        assert di.base_potency == 130
        assert DamageTag.PHYSICAL not in di.tags
        assert DamageTag.CONFECTANCE in di.tags

    def test_declaration_of_victory_v5(self):
        di: DamageInstance = DeclarationOfVictoryV5().execute(
            has_active_engagement=True
        )

        assert di.base_potency == 180
        assert DamageTag.ULTIMATE in di.tags

    def test_support_action_v5(self):
        di: DamageInstance = SupportActionV5().execute(has_active_engagement=True)

        assert di.base_potency == 80
        assert DamageTag.PASSIVE in di.tags
        assert DamageTag.SUPPORT_ACTION in di.tags


class TestMosinNagant:
    def test_set_to_v0(self):
        d: MosinNagant = MosinNagant()
        d.set_to_v0()

        assert isinstance(d.patrol_time, PatrolTime)
        assert isinstance(d.target_victory, TargetVictory)
        assert isinstance(d.declaration_of_victory, DeclarationOfVictory)
        assert isinstance(d.support_action, SupportAction)

    def test_set_to_v5(self):
        d: MosinNagant = MosinNagant()
        d.set_to_v5()

        assert isinstance(d.patrol_time, PatrolTimeV5)
        assert isinstance(d.target_victory, TargetVictoryV5)
        assert isinstance(d.declaration_of_victory, DeclarationOfVictoryV5)
        assert isinstance(d.support_action, SupportActionV5)

    def test_set_to_fortification_level(self):
        d: MosinNagant = MosinNagant()
        d.set_fortification_level(FortificationLevel.SEGMENT06)

        assert isinstance(d.declaration_of_victory, DeclarationOfVictoryV5)
        assert isinstance(d.support_action, SupportActionV5)
