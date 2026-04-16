from core.buffs import Buff
from core.dolls.mechty import BedtimeWarmup, Dreamquake, Mechty
from core.types import (
    DamageTag,
    FortificationLevel,
    ModifierType,
    SpecialAttribute,
)


class TestMechtySkills:
    def test_dreamquake(self):
        result = Dreamquake().execute()

        assert result.base_potency == 130
        assert result.tags == {
            DamageTag.ACTIVE,
            DamageTag.CORROSION,
            DamageTag.PHASE,
            DamageTag.MEDIUM_AMMO,
            DamageTag.AREA_OF_EFFECT,
        }
        assert result.group_name == "Dreamquake"

    def test_bedtime_warmup_default(self):
        result = BedtimeWarmup().execute(
            in_turbo_mode=False,
            enhanced_by_dreamquake=False,
            is_sleepwalking=False,
        )

        assert result.base_potency == 80
        assert result.tags == {
            DamageTag.ACTIVE,
            DamageTag.BASIC,
            DamageTag.MEDIUM_AMMO,
            DamageTag.TARGETED,
            DamageTag.PHYSICAL,
        }
        assert result.buffs_before == []
        assert result.group_name == "Bedtime Warmup"

    def test_bedtime_warmup_turbo_mode_converts_damage_type(self):
        result = BedtimeWarmup().execute(
            in_turbo_mode=True,
            enhanced_by_dreamquake=False,
            is_sleepwalking=False,
        )

        assert DamageTag.PHYSICAL not in result.tags
        assert DamageTag.CORROSION in result.tags
        assert DamageTag.PHASE in result.tags

    def test_bedtime_warmup_enhanced_by_dreamquake(self):
        result = BedtimeWarmup().execute(
            in_turbo_mode=False,
            enhanced_by_dreamquake=True,
            is_sleepwalking=False,
        )

        assert result.buffs_before == [
            Buff(
                100,
                ModifierType.ADDITIVE,
                SpecialAttribute.DAMAGE_BOOST,
                DamageTag.BASIC,
            )
        ]

    def test_bedtime_warmup_sleepwalking_raises_potency(self):
        result = BedtimeWarmup().execute(
            in_turbo_mode=False,
            enhanced_by_dreamquake=False,
            is_sleepwalking=True,
        )

        assert result.base_potency == 130


class TestMechty:
    def test_set_to_v0(self):
        mechty = Mechty()
        mechty.set_to_v0()

        assert isinstance(mechty.bedtime_warmup, BedtimeWarmup)
        assert isinstance(mechty.dreamquake, Dreamquake)

    def test_set_fortification_level(self):
        mechty = Mechty()

        for level in FortificationLevel:
            mechty.set_fortification_level(level)
            assert isinstance(mechty.bedtime_warmup, BedtimeWarmup)
            assert isinstance(mechty.dreamquake, Dreamquake)
