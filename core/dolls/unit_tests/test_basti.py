from core.dolls.basti import *

from core.buffs import Buff
from core.types import (
    DamageTag,
    FortificationLevel,
    ModifierType,
    SpecialAttribute,
)


class TestBastiSkills:
    def test_reckless_provocation(self):
        result = RecklessProvocation().execute()

        assert result.base_potency == 80
        assert result.tags == {
            DamageTag.ACTIVE,
            DamageTag.BASIC,
            DamageTag.LIGHT_AMMO,
            DamageTag.TARGETED,
            DamageTag.PHYSICAL,
        }
        assert result.group_name == "Reckless Provocation"

    def test_self_destruct(self):
        result = SelfDestruct().execute()

        assert result.base_potency == 100
        assert result.tags == {
            DamageTag.ACTIVE,
            DamageTag.CORROSION,
            DamageTag.PHASE,
            DamageTag.AREA_OF_EFFECT,
        }
        assert result.group_name == "Self-Destruct (Cutie Pie)"

    def test_self_destruct_v6(self):
        result = SelfDestructV6().execute()

        assert result.base_potency == 130

    def test_candy_coated_carnage(self):
        result = CandyCoatedCarnage().execute(number_of_targets_hit=3)

        assert result.base_potency == 150
        assert result.tags == {
            DamageTag.ACTIVE,
            DamageTag.CORROSION,
            DamageTag.PHASE,
            DamageTag.AREA_OF_EFFECT,
            DamageTag.ULTIMATE,
        }
        assert result.buffs_before == []

    def test_candy_coated_carnage_v4(self):
        result = CandyCoatedCarnageV4().execute(number_of_targets_hit=3)

        assert result.base_potency == 200
        assert result.buffs_before == []

    def test_candy_coated_carnage_v5_scales_with_targets(self):
        result = CandyCoatedCarnageV5().execute(number_of_targets_hit=3)

        assert result.base_potency == 200
        assert result.buffs_before == [
            Buff(
                60,
                ModifierType.ADDITIVE,
                SpecialAttribute.DAMAGE_BOOST,
                DamageTag.ULTIMATE,
            )
        ]

    def test_candy_coated_carnage_v5_caps_at_five_targets(self):
        result = CandyCoatedCarnageV5().execute(number_of_targets_hit=9)

        assert result.buffs_before == [
            Buff(
                100,
                ModifierType.ADDITIVE,
                SpecialAttribute.DAMAGE_BOOST,
                DamageTag.ULTIMATE,
            )
        ]

    def test_grudge(self):
        result = Grudge().execute()

        assert result.base_potency == 100
        assert result.tags == {
            DamageTag.PASSIVE,
            DamageTag.CORROSION,
            DamageTag.PHASE,
            DamageTag.AREA_OF_EFFECT,
            DamageTag.SUPPORT_ACTION,
        }
        assert result.group_name == "Grudge"

    def test_grudge_v5(self):
        result = GrudgeV5().execute()

        assert result.base_potency == 200


class TestBasti:
    def test_set_to_v0(self):
        doll = Basti()
        doll.set_to_v0()

        assert isinstance(doll.reckless_provocation, RecklessProvocation)
        assert isinstance(doll.self_destruct, SelfDestruct)
        assert isinstance(doll.candy_coated_carnage, CandyCoatedCarnage)
        assert isinstance(doll.grudge, Grudge)

    def test_set_to_v4(self):
        doll = Basti()
        doll.set_to_v4()

        assert isinstance(doll.reckless_provocation, RecklessProvocation)
        assert isinstance(doll.self_destruct, SelfDestruct)
        assert isinstance(doll.candy_coated_carnage, CandyCoatedCarnageV4)
        assert isinstance(doll.grudge, Grudge)

    def test_set_to_v5(self):
        doll = Basti()
        doll.set_to_v5()

        assert isinstance(doll.reckless_provocation, RecklessProvocation)
        assert isinstance(doll.self_destruct, SelfDestruct)
        assert isinstance(doll.candy_coated_carnage, CandyCoatedCarnageV5)
        assert isinstance(doll.grudge, GrudgeV5)

    def test_set_to_v6(self):
        doll = Basti()
        doll.set_to_v6()

        assert isinstance(doll.reckless_provocation, RecklessProvocation)
        assert isinstance(doll.self_destruct, SelfDestructV6)
        assert isinstance(doll.candy_coated_carnage, CandyCoatedCarnageV5)
        assert isinstance(doll.grudge, GrudgeV5)

    def test_set_fortification_level(self):
        doll = Basti()

        doll.set_fortification_level(FortificationLevel.SEGMENT04)
        assert isinstance(doll.candy_coated_carnage, CandyCoatedCarnageV4)
        assert isinstance(doll.grudge, Grudge)

        doll.set_fortification_level(FortificationLevel.SEGMENT05)
        assert isinstance(doll.candy_coated_carnage, CandyCoatedCarnageV5)
        assert isinstance(doll.grudge, GrudgeV5)

        doll.set_fortification_level(FortificationLevel.SEGMENT06)
        assert isinstance(doll.self_destruct, SelfDestructV6)
        assert isinstance(doll.candy_coated_carnage, CandyCoatedCarnageV5)
        assert isinstance(doll.grudge, GrudgeV5)
