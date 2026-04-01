from core.dolls.lewis import *
from core.types import DamageTag, SpecialAttribute
from core.buffs import Buff
from core.combat import DamageInstance


class TestLewisSkills:
    def test_playtime(self):
        basic: DamageInstance = Playtime().execute()

        assert basic.base_potency == 80
        assert DamageTag.PHYSICAL in basic.tags
        assert DamageTag.BASIC in basic.tags

    def test_bad_guy_cleanup(self):
        da: DamageInstance = BadGuyCleanup().execute()

        assert da.base_potency == 80
        assert DamageTag.BURN in da.tags
        assert DamageTag.AREA_OF_EFFECT in da.tags

    def test_surprising_funball(self):
        da: DamageInstance = SurprisingFunball().execute()

        assert da.base_potency == 140
        assert DamageTag.BURN in da.tags
        assert DamageTag.HEAVY_AMMO in da.tags

    def test_toy_carnival(self):
        da: DamageInstance = ToyCarnival().execute(
            cumulative_tin_soldier_ranks=5, highest_rank_tin_soldier=3
        )

        assert da.base_potency == 255
        assert DamageTag.BURN in da.tags
        assert DamageTag.ULTIMATE in da.tags
        assert da.buffs_before[0] == Buff(25, ModifierType.ADDITIVE, StatType.CRIT_RATE)

    def test_volley_fire(self):
        da: DamageInstance = VolleyFire().execute(
            tin_soldier_rank=2, has_tin_soldiers_order=False
        )

        assert da.base_potency == 120
        assert DamageTag.BURN in da.tags
        assert DamageTag.PASSIVE in da.tags

    def test_volley_fire_v1(self):
        da: DamageInstance = VolleyFireV1().execute(
            tin_soldier_rank=2, has_tin_soldiers_order=True
        )

        assert da.base_potency == 170

    def test_toy_carnival_v2(self):
        da: DamageInstance = ToyCarnivalV2().execute(
            cumulative_tin_soldier_ranks=5, highest_rank_tin_soldier=3
        )

        assert da.base_potency == 275
        assert da.buffs_before[0] == Buff(25, ModifierType.ADDITIVE, StatType.CRIT_RATE)
        assert da.buffs_before[1] == DamageUpII()

    def test_surprising_funball_v3(self):
        da: DamageInstance = SurprisingFunballV3().execute()

        assert da.base_potency == 160
        assert DamageTag.BURN in da.tags
        assert DamageTag.HEAVY_AMMO in da.tags

    def test_volley_fire_v3(self):
        da: DamageInstance = VolleyFireV3().execute(
            tin_soldier_rank=2, has_tin_soldiers_order=True
        )

        assert da.base_potency == 190

    def test_bad_guy_cleanup_v4(self):
        da: DamageInstance = BadGuyCleanupV4().execute()

        assert da.base_potency == 120

    def test_toy_carnival_v5(self):
        da: DamageInstance = ToyCarnivalV5().execute(
            cumulative_tin_soldier_ranks=5, highest_rank_tin_soldier=3
        )

        assert da.base_potency == 250
        assert da.buffs_before[0] == Buff(25, ModifierType.ADDITIVE, StatType.CRIT_RATE)
        assert da.buffs_before[1] == Buff(
            25, ModifierType.ADDITIVE, StatType.CRIT_DAMAGE
        )
        assert da.buffs_before[2] == Buff(
            20, ModifierType.ADDITIVE, SpecialAttribute.DAMAGE_BOOST, DamageTag.ALL
        )


class TestLewis:
    def test_set_to_v0(self):
        lewis: Lewis = Lewis()
        lewis.set_to_v0()

        assert isinstance(lewis.playtime, Playtime)
        assert isinstance(lewis.bad_guy_cleanup, BadGuyCleanup)
        assert isinstance(lewis.surprising_funball, SurprisingFunball)
        assert isinstance(lewis.toy_carnival, ToyCarnival)
        assert isinstance(lewis.volley_fire, VolleyFire)

    def test_set_to_v1(self):
        lewis: Lewis = Lewis()
        lewis.set_to_v1()

        assert isinstance(lewis.volley_fire, VolleyFireV1)

    def test_set_to_v2(self):
        lewis: Lewis = Lewis()
        lewis.set_to_v2()

        assert isinstance(lewis.toy_carnival, ToyCarnivalV2)

    def test_set_to_v3(self):
        lewis: Lewis = Lewis()
        lewis.set_to_v3()

        assert isinstance(lewis.surprising_funball, SurprisingFunballV3)
        assert isinstance(lewis.volley_fire, VolleyFireV3)

    def test_set_to_v4(self):
        lewis: Lewis = Lewis()
        lewis.set_to_v4()

        assert isinstance(lewis.bad_guy_cleanup, BadGuyCleanupV4)

    def test_set_to_v5(self):
        lewis: Lewis = Lewis()
        lewis.set_to_v5()

        assert isinstance(lewis.toy_carnival, ToyCarnivalV5)

    def test_set_to_fortification_level(self):
        lewis: Lewis = Lewis()
        lewis.set_fortification_level(FortificationLevel.SEGMENT06)

        assert isinstance(lewis.toy_carnival, ToyCarnivalV5)
