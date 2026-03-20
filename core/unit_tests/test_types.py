import pytest

from core.types import (
    DamageTag,
    DamageTagMultipliers,
    IncreasedDamageMultipliers,
    StatType,
    SpecialAttribute,
    StatSheet,
    FinalStatModifiers,
    Unit,
)


class TestDamageTag:
    """ """

    def test_DamageTag(self):
        dt: DamageTag = DamageTag.COUNTERATTACK

        print(dt)
        assert str(dt) == "Counterattack"

    def test_boundary(self):
        with pytest.raises(ValueError) as _:
            DamageTag("paper")


class TestDamageTagMultipliers:
    """ """

    def test_default_constructor(self):
        dtm: DamageTagMultipliers = DamageTagMultipliers()

        assert dtm.multipliers[DamageTag.CORROSION] == 0

    def test_data_access(self):
        dtm: DamageTagMultipliers = DamageTagMultipliers()
        assert dtm.get_multiplier(DamageTag.SHOTGUN_AMMO) == 0

        dtm.set_multiplier(DamageTag.SHOTGUN_AMMO, 15)
        assert dtm.get_multiplier(DamageTag.SHOTGUN_AMMO) == 15

        dtm.add_to_multiplier(DamageTag.SHOTGUN_AMMO, 22)
        assert dtm.get_multiplier(DamageTag.SHOTGUN_AMMO) == (15 + 22)
        assert dtm.get_multiplier(DamageTag.AREA_OF_EFFECT) == 0

    def test_get_total_multiplier(self):
        tags: set[DamageTag] = [
            DamageTag.PASSIVE,
            DamageTag.SUPPORT_ACTION,
            DamageTag.TARGETED,
            DamageTag.FREEZE,
        ]

        dtm: DamageTagMultipliers = DamageTagMultipliers()
        dtm.set_multiplier(DamageTag.SUPPORT_ACTION, 25)
        dtm.set_multiplier(DamageTag.FREEZE, 20)
        dtm.set_multiplier(DamageTag.PASSIVE, 15)

        assert dtm.get_total_multiplier(tags) == (25 + 20 + 15)


class TestUnitClass:
    @staticmethod
    def construct_attacker() -> Unit:
        g: Unit = Unit()
        g.initial_stats.basic_attributes[StatType.ATTACK] = 5429
        g.initial_stats.basic_attributes[StatType.CRIT_DAMAGE] = 156.9
        g.initial_stats.basic_attributes[StatType.DEFENSE] = 1000

        g.additive_modifiers.basic_attributes[StatType.ATTACK] = 11
        g.multiplicative_modifiers.basic_attributes[StatType.ATTACK] = 15

        g.initial_stats.special_attributes[
            SpecialAttribute.DAMAGE_BOOST
        ].set_multiplier(DamageTag.BURN, 20)
        g.additive_modifiers.special_attributes[
            SpecialAttribute.DAMAGE_BOOST
        ].set_multiplier(DamageTag.BURN, 15)

        return g

    def test_get_stat_basic(self):
        g = TestUnitClass.construct_attacker()
        assert g.get_basic_attribute(StatType.ATTACK) == pytest.approx(5440 * 1.15)

    def test_get_stat_special(self):
        g = TestUnitClass.construct_attacker()
        assert g.get_special_attribute(
            SpecialAttribute.DAMAGE_BOOST, DamageTag.BURN
        ) == pytest.approx(35)

    def test_get_effective_critical_damage_multiplier(self):
        g = TestUnitClass.construct_attacker()
        g.initial_stats.special_attributes[
            SpecialAttribute.CRITICAL_DAMAGE
        ].set_multiplier(DamageTag.FREEZE, 25)
        g.initial_stats.special_attributes[
            SpecialAttribute.CRITICAL_DAMAGE
        ].set_multiplier(DamageTag.AREA_OF_EFFECT, 7)
        g.initial_stats.special_attributes[
            SpecialAttribute.CRITICAL_DAMAGE
        ].set_multiplier(DamageTag.TARGETED, 7)

        assert (
            g.get_effective_critical_damage_multiplier(
                set({DamageTag.FREEZE, DamageTag.AREA_OF_EFFECT})
            )
            == 188.9
        )
