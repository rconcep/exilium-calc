from core.dolls.vepley import *
from core.types import DamageTag, ModifierType, SpecialAttribute, StatType
from core.buffs import Buff, Debuff, VulnerableII
from core.combat import DamageInstance


class TestVepleySkills:
    def test_live_interaction(self):
        li: DamageInstance = LiveInteraction().execute()

        assert li.base_potency == 80
        assert DamageTag.PHYSICAL in li.tags
        assert DamageTag.BASIC in li.tags
        assert DamageTag.SHOTGUN_AMMO in li.tags
        assert DamageTag.TARGETED in li.tags
        assert DamageTag.ACTIVE in li.tags
        assert li.buffs_before == []

    def test_all_out_performance(self):
        aop: DamageInstance = AllOutPerformance().execute()

        assert aop.base_potency == 75
        assert DamageTag.PHYSICAL in aop.tags
        assert DamageTag.SHOTGUN_AMMO in aop.tags
        assert DamageTag.AREA_OF_EFFECT in aop.tags
        assert DamageTag.ACTIVE in aop.tags
        assert aop.buffs_before == []
        assert len(aop.debuffs_before) == 1
        assert aop.debuffs_before[0] == VulnerableII()

    def test_exclusive_stage(self):
        es: DamageInstance = ExclusiveStage().execute()

        assert es.base_potency == 150
        assert DamageTag.PHYSICAL in es.tags
        assert DamageTag.TARGETED in es.tags
        assert DamageTag.ACTIVE in es.tags
        assert es.buffs_before == []

    def test_exclusive_stage_v2(self):
        es: DamageInstance = ExclusiveStageV2().execute()

        assert es.base_potency == 150
        assert len(es.buffs_before) == 1
        assert es.buffs_before[0] == Buff(
            value=100,
            modifier_type=ModifierType.ADDITIVE,
            stat_type=StatType.CRIT_RATE,
        )

    def test_infectious_enthusiasm(self):
        ie: DamageInstance = InfectiousEnthusiasm().execute()

        assert ie.base_potency == 100
        assert DamageTag.PHYSICAL in ie.tags
        assert DamageTag.AREA_OF_EFFECT in ie.tags
        assert DamageTag.ULTIMATE in ie.tags
        assert DamageTag.ACTIVE in ie.tags
        assert ie.buffs_before == []


class TestVepley:
    def test_set_to_v0(self):
        vp: Vepley = Vepley()
        vp.set_to_v0()

        assert isinstance(vp.live_interaction, LiveInteraction)
        assert isinstance(vp.all_out_performance, AllOutPerformance)
        assert isinstance(vp.exclusive_stage, ExclusiveStage)
        assert isinstance(vp.infectious_enthusiasm, InfectiousEnthusiasm)
        # Expansion Key base: 15% defense ignore for all attacks
        assert (
            vp.initial_stats.special_attributes[
                SpecialAttribute.DEFENSE_IGNORE
            ].get_multiplier(DamageTag.ALL)
            == 15
        )
        # Expansion Key conditional: additional 15% defense ignore vs movement-debuffed targets
        assert (
            vp.initial_stats.special_attributes[
                SpecialAttribute.DEFENSE_IGNORE
            ].get_multiplier(DamageTag.HAS_MOVEMENT_DEBUFF)
            == 15
        )
        # Idol Talent passive: 20% damage boost vs movement-debuffed targets
        assert (
            vp.initial_stats.special_attributes[
                SpecialAttribute.DAMAGE_BOOST
            ].get_multiplier(DamageTag.HAS_MOVEMENT_DEBUFF)
            == 20
        )

    def test_set_to_v2(self):
        vp: Vepley = Vepley()
        vp.set_to_v2()

        assert isinstance(vp.exclusive_stage, ExclusiveStageV2)
        assert isinstance(vp.infectious_enthusiasm, InfectiousEnthusiasm)

    def test_set_to_v3(self):
        vp: Vepley = Vepley()
        vp.set_to_v3()

        assert isinstance(vp.exclusive_stage, ExclusiveStageV2)
        assert isinstance(vp.infectious_enthusiasm, InfectiousEnthusiasm)

    def test_set_fortification_level_v1_unchanged(self):
        vp: Vepley = Vepley()
        vp.set_fortification_level(FortificationLevel.SEGMENT01)

        assert isinstance(vp.exclusive_stage, ExclusiveStage)
        assert isinstance(vp.infectious_enthusiasm, InfectiousEnthusiasm)

    def test_set_fortification_level_v2(self):
        vp: Vepley = Vepley()
        vp.set_fortification_level(FortificationLevel.SEGMENT02)

        assert isinstance(vp.exclusive_stage, ExclusiveStageV2)
        assert isinstance(vp.infectious_enthusiasm, InfectiousEnthusiasm)

    def test_set_fortification_level_v3(self):
        vp: Vepley = Vepley()
        vp.set_fortification_level(FortificationLevel.SEGMENT03)

        assert isinstance(vp.exclusive_stage, ExclusiveStageV2)
        assert isinstance(vp.infectious_enthusiasm, InfectiousEnthusiasm)

    def test_set_fortification_level_v6(self):
        vp: Vepley = Vepley()
        vp.set_fortification_level(FortificationLevel.SEGMENT06)

        assert isinstance(vp.exclusive_stage, ExclusiveStageV2)
        assert isinstance(vp.infectious_enthusiasm, InfectiousEnthusiasm)
