from core.buffs import Buff
from core.combat import DamageInstance
from core.dolls.lenna import *
from core.types import (
    DamageTag,
    FortificationLevel,
    ModifierType,
    SpecialAttribute,
    StatType,
)


class TestLennaSkills:
    def test_territory_awareness_base(self):
        territory_awareness: DamageInstance = TerritoryAwareness().execute(
            follows_leaping_pursuit=False
        )

        assert territory_awareness.base_potency == 80
        assert DamageTag.BASIC in territory_awareness.tags
        assert DamageTag.PHYSICAL in territory_awareness.tags
        assert territory_awareness.buffs_before == []

    def test_territory_awareness_follows_leaping_pursuit(self):
        territory_awareness: DamageInstance = TerritoryAwareness().execute(
            follows_leaping_pursuit=True
        )

        assert territory_awareness.base_potency == 180
        assert territory_awareness.buffs_before == [
            Buff(
                value=15,
                modifier_type=ModifierType.MULTIPLICATIVE,
                stat_type=StatType.ATTACK,
                tag=DamageTag.ALL,
            )
        ]

    def test_wild_extinction_base_without_confectance(self):
        wild_extinction: DamageInstance = WildExtinction().execute(
            confectance_index=2,
            follows_leaping_pursuit=False,
        )

        assert wild_extinction.base_potency == 120
        assert DamageTag.ELECTRIC in wild_extinction.tags
        assert wild_extinction.buffs_before == []

    def test_wild_extinction_with_max_confectance_and_leaping(self):
        wild_extinction: DamageInstance = WildExtinction().execute(
            confectance_index=6,
            follows_leaping_pursuit=True,
        )

        assert wild_extinction.base_potency == 220
        assert wild_extinction.buffs_before[0] == Buff(
            value=30,
            modifier_type=ModifierType.ADDITIVE,
            stat_type=SpecialAttribute.DAMAGE_BOOST,
            tag=DamageTag.ALL,
        )
        assert wild_extinction.buffs_before[1] == Buff(
            value=30,
            modifier_type=ModifierType.MULTIPLICATIVE,
            stat_type=StatType.ATTACK,
            tag=DamageTag.ALL,
        )

    def test_wild_extinction_v2_with_max_confectance_and_leaping(self):
        wild_extinction: DamageInstance = WildExtinctionV2().execute(
            confectance_index=6,
            follows_leaping_pursuit=True,
        )

        assert wild_extinction.base_potency == 220
        assert wild_extinction.buffs_before[0] == Buff(
            value=50,
            modifier_type=ModifierType.ADDITIVE,
            stat_type=SpecialAttribute.DAMAGE_BOOST,
            tag=DamageTag.ALL,
        )
        assert wild_extinction.buffs_before[1].value == 30

    def test_wild_extinction_v6_with_max_confectance_and_leaping(self):
        wild_extinction: DamageInstance = WildExtinctionV6().execute(
            confectance_index=6,
            follows_leaping_pursuit=True,
        )

        assert wild_extinction.base_potency == 220
        assert wild_extinction.buffs_before[0] == Buff(
            value=70,
            modifier_type=ModifierType.ADDITIVE,
            stat_type=SpecialAttribute.DAMAGE_BOOST,
            tag=DamageTag.ALL,
        )
        assert wild_extinction.buffs_before[1].value == 30

    def test_leaping_pursuit_base(self):
        leaping_pursuit: DamageInstance = LeapingPursuit().execute(confectance_index=2)

        assert leaping_pursuit.base_potency == 30
        assert leaping_pursuit.buffs_before == []

    def test_leaping_pursuit_with_max_confectance(self):
        leaping_pursuit: DamageInstance = LeapingPursuit().execute(confectance_index=6)

        assert leaping_pursuit.base_potency == 30
        assert leaping_pursuit.buffs_before == [
            Buff(
                value=15,
                modifier_type=ModifierType.MULTIPLICATIVE,
                stat_type=StatType.ATTACK,
                tag=DamageTag.ALL,
            )
        ]

    def test_leaping_pursuit_v6_with_max_confectance(self):
        leaping_pursuit: DamageInstance = LeapingPursuitV6().execute(
            confectance_index=6
        )

        assert leaping_pursuit.base_potency == 30
        assert leaping_pursuit.buffs_before[0] == Buff(
            value=20,
            modifier_type=ModifierType.ADDITIVE,
            stat_type=SpecialAttribute.DAMAGE_BOOST,
            tag=DamageTag.ALL,
        )
        assert leaping_pursuit.buffs_before[1] == Buff(
            value=15,
            modifier_type=ModifierType.MULTIPLICATIVE,
            stat_type=StatType.ATTACK,
            tag=DamageTag.ALL,
        )

    def test_hunting_strategy_follows_leaping_pursuit(self):
        hunting_strategy: DamageInstance = HuntingStrategy().execute(
            confectance_index=6,
            follows_leaping_pursuit=True,
        )

        assert hunting_strategy.base_potency == 180
        assert hunting_strategy.buffs_before == [
            Buff(
                value=30,
                modifier_type=ModifierType.MULTIPLICATIVE,
                stat_type=StatType.ATTACK,
                tag=DamageTag.ALL,
            )
        ]

    def test_hunting_strategy_v6_follows_leaping_pursuit(self):
        hunting_strategy: DamageInstance = HuntingStrategyV6().execute(
            confectance_index=6,
            follows_leaping_pursuit=True,
        )

        assert hunting_strategy.base_potency == 180
        assert hunting_strategy.buffs_before[0] == Buff(
            value=20,
            modifier_type=ModifierType.ADDITIVE,
            stat_type=SpecialAttribute.DAMAGE_BOOST,
            tag=DamageTag.ALL,
        )
        assert hunting_strategy.buffs_before[1] == Buff(
            value=30,
            modifier_type=ModifierType.MULTIPLICATIVE,
            stat_type=StatType.ATTACK,
            tag=DamageTag.ALL,
        )


class TestLenna:
    def test_set_to_v0(self):
        lenna = Lenna()
        lenna.set_to_v0()

        assert isinstance(lenna.territory_awareness, TerritoryAwareness)
        assert isinstance(lenna.wild_extinction, WildExtinction)
        assert isinstance(lenna.leaping_pursuit, LeapingPursuit)
        assert isinstance(lenna.hunting_strategy, HuntingStrategy)

    def test_set_to_v2(self):
        lenna = Lenna()
        lenna.set_to_v2()

        assert isinstance(lenna.territory_awareness, TerritoryAwareness)
        assert isinstance(lenna.wild_extinction, WildExtinctionV2)
        assert isinstance(lenna.leaping_pursuit, LeapingPursuit)
        assert isinstance(lenna.hunting_strategy, HuntingStrategy)

    def test_set_to_v6(self):
        lenna = Lenna()
        lenna.set_to_v6()

        assert isinstance(lenna.territory_awareness, TerritoryAwareness)
        assert isinstance(lenna.wild_extinction, WildExtinctionV6)
        assert isinstance(lenna.leaping_pursuit, LeapingPursuitV6)
        assert isinstance(lenna.hunting_strategy, HuntingStrategyV6)

    def test_set_fortification_level(self):
        lenna = Lenna()
        lenna.set_fortification_level(FortificationLevel.SEGMENT06)

        assert isinstance(lenna.wild_extinction, WildExtinctionV6)
        assert isinstance(lenna.leaping_pursuit, LeapingPursuitV6)
        assert isinstance(lenna.hunting_strategy, HuntingStrategyV6)
