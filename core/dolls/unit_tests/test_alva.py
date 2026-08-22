from core.dolls.alva import *
from core.types import DamageTag, FortificationLevel, StatType, Unit
from core.combat import AlvaHoarfrostBreakDamageCalculationStrategy, DamageInstance
import pytest


class TestAlvaSkills:
    def test_laceration(self):
        lac: DamageInstance = Laceration().execute()

        assert lac.base_potency == 80
        assert DamageTag.ACTIVE in lac.tags
        assert DamageTag.BASIC in lac.tags
        assert DamageTag.PHYSICAL in lac.tags

    def test_snow_wolfs_heart(self):
        s1: DamageInstance = SnowWolfsHeart().execute()

        assert s1.base_potency == 100
        assert DamageTag.FREEZE in s1.tags
        assert DamageTag.PHASE in s1.tags

    def test_frosted_echo(self):
        s2: DamageInstance = FrostedEcho().execute(confectance_index=6)

        assert s2.base_potency == 90
        assert DamageTag.CONFECTANCE in s2.tags

    def test_frosted_echo_v1(self):
        s2: DamageInstance = FrostedEchoV1().execute(confectance_index=6)

        assert s2.base_potency == 120
        assert DamageTag.AREA_OF_EFFECT in s2.tags

    def test_hoarfrost_break(self):
        hb: DamageInstance = HoarfrostBreak().execute(shield_value=1000)

        assert hb.base_potency == 80
        assert DamageTag.PASSIVE in hb.tags
        assert isinstance(
            hb.damage_calculation_strategy, AlvaHoarfrostBreakDamageCalculationStrategy
        )
        assert hb.damage_calculation_strategy.shield_value == 1000

    def test_hoarfrost_break_v5(self):
        hb: DamageInstance = HoarfrostBreakV5().execute(shield_value=1000)

        assert hb.base_potency == 120
        assert isinstance(
            hb.damage_calculation_strategy, AlvaHoarfrostBreakDamageCalculationStrategy
        )
        assert hb.damage_calculation_strategy.shield_value == 1000

    def test_nix_requiem(self):
        ult: DamageInstance = NixRequiem().execute(confectance_index=6)

        assert ult.base_potency == 180
        assert DamageTag.ULTIMATE in ult.tags

    def test_nix_requiem_v2(self):
        ult: DamageInstance = NixRequiemV2().execute(confectance_index=6)

        assert ult.base_potency == 240

    def test_interception(self):
        inter: DamageInstance = Interception().execute()

        assert inter.base_potency == 60
        assert DamageTag.INTERCEPTION in inter.tags


class TestAlva:
    def test_set_to_v0(self):
        al: Alva = Alva()
        al.set_to_v0()

        assert isinstance(al.laceration, Laceration)
        assert isinstance(al.snow_wolfs_heart, SnowWolfsHeart)
        assert isinstance(al.frosted_echo, FrostedEcho)
        assert isinstance(al.hoarfrost_break, HoarfrostBreak)
        assert isinstance(al.nix_requiem, NixRequiem)
        assert isinstance(al.interception, Interception)

    def test_set_to_v1(self):
        al: Alva = Alva()
        al.set_to_v1()

        assert isinstance(al.frosted_echo, FrostedEchoV1)

    def test_set_to_v2(self):
        al: Alva = Alva()
        al.set_to_v2()

        assert isinstance(al.frosted_echo, FrostedEchoV1)
        assert isinstance(al.nix_requiem, NixRequiemV2)

    def test_set_to_v5(self):
        al: Alva = Alva()
        al.set_to_v5()

        assert isinstance(al.hoarfrost_break, HoarfrostBreakV5)
        assert isinstance(al.nix_requiem, NixRequiemV2)

    def test_set_fortification_level_v4(self):
        al: Alva = Alva()
        al.set_fortification_level(FortificationLevel.SEGMENT04)

        assert isinstance(al.frosted_echo, FrostedEchoV1)
        assert isinstance(al.nix_requiem, NixRequiemV2)

    def test_set_fortification_level_v6(self):
        al: Alva = Alva()
        al.set_fortification_level(FortificationLevel.SEGMENT06)

        assert isinstance(al.hoarfrost_break, HoarfrostBreakV5)
        assert isinstance(al.nix_requiem, NixRequiemV2)


class TestAlvaHoarfrostBreakDamageCalculationStrategy:
    def test_calculate_base_damage_uses_shield_value_in_place_of_attack(self):
        strategy = AlvaHoarfrostBreakDamageCalculationStrategy(shield_value=1000)
        attacker = Alva()
        target = Unit()
        target.initial_stats.basic_attributes[StatType.DEFENSE] = 200

        di = DamageInstance(label="Hoarfrost Break", base_potency=80, tags=set())

        (
            effective_atk,
            effective_def,
            negative_def,
            term1,
        ) = strategy.calculate_base_damage(attacker, target, di)

        assert effective_atk == 1000
        assert effective_def == 200
        assert negative_def == 0
        assert term1 == pytest.approx(1000 / (1 + 200 / 1000))

    def test_defense_reduces_damage_and_base_potency_scales_it(self):
        doll = Alva()
        doll.set_to_v0()

        di: DamageInstance = HoarfrostBreak().execute(shield_value=1000)
        target = Unit()
        target.initial_stats.basic_attributes[StatType.DEFENSE] = 200

        summary = di.damage_calculation_strategy.calculate_damage(doll, target, di)

        # term1 = 1000 / (1 + 200 / 1000) = 833.33, scaled by 80% base potency = 666.67.
        assert summary.non_critical_damage == pytest.approx(666.666667)
        assert summary.effective_attack == 1000
        assert summary.effective_defense == 200

    def test_preserves_tags_unlike_fixed_damage_instance(self):
        di: DamageInstance = HoarfrostBreak().execute(shield_value=1000)

        assert DamageTag.FIXED not in di.tags
        assert DamageTag.FREEZE in di.tags
        assert DamageTag.PHASE in di.tags
