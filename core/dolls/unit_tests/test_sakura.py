from core.buffs import Buff, Debuff
from core.combat import DamageInstance
from core.dolls.sakura import *
from core.types import (
    DamageTag,
    FortificationLevel,
    ModifierType,
    SpecialAttribute,
)


class TestSakuraSkills:
    def test_sakura_chime(self):
        sakura_chime: DamageInstance = SakuraChime().execute()

        assert sakura_chime.base_potency == 80
        assert DamageTag.ACTIVE in sakura_chime.tags
        assert DamageTag.BASIC in sakura_chime.tags
        assert DamageTag.LIGHT_AMMO in sakura_chime.tags
        assert DamageTag.TARGETED in sakura_chime.tags
        assert DamageTag.PHYSICAL in sakura_chime.tags
        assert sakura_chime.group_name == "Sakura Chime"

    def test_falling_blossom_versions(self):
        falling_blossom: DamageInstance = FallingBlossom().execute()
        falling_blossom_v2: DamageInstance = FallingBlossomV2().execute()

        assert falling_blossom.base_potency == 60
        assert falling_blossom_v2.base_potency == 75
        assert DamageTag.BURN in falling_blossom.tags
        assert DamageTag.PHASE in falling_blossom.tags
        assert DamageTag.CONFECTANCE in falling_blossom.tags

    def test_misfortune_delivery(self):
        misfortune_delivery: DamageInstance = MisfortuneDelivery().execute()

        assert misfortune_delivery.base_potency == 130
        assert DamageTag.ACTIVE in misfortune_delivery.tags
        assert DamageTag.BURN in misfortune_delivery.tags
        assert DamageTag.PHASE in misfortune_delivery.tags
        assert DamageTag.LIGHT_AMMO in misfortune_delivery.tags
        assert DamageTag.TARGETED in misfortune_delivery.tags
        assert DamageTag.CONFECTANCE in misfortune_delivery.tags
        assert misfortune_delivery.group_name == "Misfortune Delivery"

    def test_grand_isekai_adventure_versions(self):
        grand_isekai_adventure: DamageInstance = GrandIsekaiAdventure().execute()
        grand_isekai_adventure_v5: DamageInstance = GrandIsekaiAdventureV5().execute()

        assert grand_isekai_adventure.base_potency == 90
        assert grand_isekai_adventure_v5.base_potency == 120
        assert DamageTag.ULTIMATE in grand_isekai_adventure.tags
        assert DamageTag.AREA_OF_EFFECT in grand_isekai_adventure.tags

    def test_sakura_mark_base_and_v1(self):
        sakura_mark: DamageInstance = SakuraMark().execute(
            target_has_bad_luck=True,
            target_is_on_burn_tile=True,
        )
        sakura_mark_v1: DamageInstance = SakuraMarkV1().execute(
            target_has_bad_luck=True,
            target_is_on_burn_tile=True,
        )

        assert sakura_mark.base_potency == 60
        assert sakura_mark.debuffs_before == [
            Debuff(
                value=10,
                modifier_type=ModifierType.ADDITIVE,
                stat_type=SpecialAttribute.INCREASE_DAMAGE_TAKEN,
                tag=DamageTag.ALL,
            )
        ]
        assert sakura_mark.buffs_before == []

        assert sakura_mark_v1.base_potency == 90
        assert sakura_mark_v1.debuffs_before == sakura_mark.debuffs_before
        assert sakura_mark_v1.buffs_before == [
            Buff(
                value=30,
                modifier_type=ModifierType.ADDITIVE,
                stat_type=SpecialAttribute.DAMAGE_BOOST,
                tag=DamageTag.ALL,
            )
        ]

    def test_sakura_mark_v3_and_v4(self):
        sakura_mark_v3: DamageInstance = SakuraMarkV3().execute(
            target_has_bad_luck=True,
            target_is_on_burn_tile=True,
        )
        sakura_mark_v4: DamageInstance = SakuraMarkV4().execute(
            target_has_bad_luck=True,
            target_is_on_burn_tile=True,
        )

        assert sakura_mark_v3.base_potency == 90
        assert sakura_mark_v4.base_potency == 90

        assert sakura_mark_v3.buffs_before == [
            Buff(
                value=30,
                modifier_type=ModifierType.ADDITIVE,
                stat_type=SpecialAttribute.DAMAGE_BOOST,
                tag=DamageTag.ALL,
            ),
            Buff(
                value=15,
                modifier_type=ModifierType.ADDITIVE,
                stat_type=SpecialAttribute.DEFENSE_IGNORE,
                tag=DamageTag.ALL,
            ),
        ]

        assert sakura_mark_v3.debuffs_before == [
            Debuff(
                value=10,
                modifier_type=ModifierType.ADDITIVE,
                stat_type=SpecialAttribute.INCREASE_DAMAGE_TAKEN,
                tag=DamageTag.ALL,
            )
        ]
        assert sakura_mark_v4.debuffs_before == [
            Debuff(
                value=30,
                modifier_type=ModifierType.ADDITIVE,
                stat_type=SpecialAttribute.INCREASE_DAMAGE_TAKEN,
                tag=DamageTag.ALL,
            )
        ]


class TestSakura:
    def test_set_to_v0(self):
        sakura: Sakura = Sakura()
        sakura.set_to_v0()

        assert isinstance(sakura.sakura_chime, SakuraChime)
        assert isinstance(sakura.falling_blossom, FallingBlossom)
        assert isinstance(sakura.misfortune_delivery, MisfortuneDelivery)
        assert isinstance(sakura.grand_isekai_adventure, GrandIsekaiAdventure)
        assert isinstance(sakura.sakura_mark, SakuraMark)

    def test_set_to_v1(self):
        sakura: Sakura = Sakura()
        sakura.set_to_v1()

        assert isinstance(sakura.sakura_mark, SakuraMarkV1)

    def test_set_to_v5(self):
        sakura: Sakura = Sakura()
        sakura.set_to_v5()

        assert isinstance(sakura.falling_blossom, FallingBlossomV2)
        assert isinstance(sakura.grand_isekai_adventure, GrandIsekaiAdventureV5)
        assert isinstance(sakura.sakura_mark, SakuraMarkV4)

    def test_set_to_fortification_level(self):
        sakura: Sakura = Sakura()

        sakura.set_fortification_level(FortificationLevel.SEGMENT03)
        assert isinstance(sakura.falling_blossom, FallingBlossomV2)
        assert isinstance(sakura.sakura_mark, SakuraMarkV3)

        sakura.set_fortification_level(FortificationLevel.SEGMENT06)
        assert sakura.fortification_level == FortificationLevel.SEGMENT06
        assert isinstance(sakura.grand_isekai_adventure, GrandIsekaiAdventureV5)
        assert isinstance(sakura.sakura_mark, SakuraMarkV4)
