from core.buffs import Buff
from core.combat import DamageInstance, LindDamageCalculationStrategy
from core.dolls.lind import *
from core.types import (
    DamageTag,
    FortificationLevel,
    ModifierType,
    SpecialAttribute,
    StatType,
)


class TestLindSkills:
    def test_repulsive_shot_without_glucose_overload(self):
        repulsive_shot: DamageInstance = RepulsiveShot().execute()

        assert repulsive_shot.base_potency == 80
        assert DamageTag.BASIC in repulsive_shot.tags
        assert DamageTag.ACTIVE in repulsive_shot.tags
        assert repulsive_shot.group_name == "Repulsive Shot"
        assert isinstance(
            repulsive_shot.damage_calculation_strategy,
            LindDamageCalculationStrategy,
        )

    def test_repulsive_shot_v2_without_glucose_overload(self):
        repulsive_shot: DamageInstance = RepulsiveShotV2().execute(
            is_glucose_overload_followup=False
        )

        assert repulsive_shot.base_potency == 80
        assert DamageTag.BASIC in repulsive_shot.tags
        assert repulsive_shot.buffs_before == []

    def test_repulsive_shot_v2_with_glucose_overload(self):
        repulsive_shot: DamageInstance = RepulsiveShotV2().execute(
            is_glucose_overload_followup=True
        )

        assert repulsive_shot.base_potency == 80
        assert len(repulsive_shot.buffs_before) == 1
        assert repulsive_shot.buffs_before[0].value == 15
        assert repulsive_shot.buffs_before[0].tag == DamageTag.ACTIVE
        assert repulsive_shot.buffs_before[0].stat_type == SpecialAttribute.DAMAGE_BOOST

    def test_assault_spray_base_without_glucose_overload(self):
        assault_spray: DamageInstance = AssaultSpray().execute(
            number_of_debuffs_on_target=6
        )

        assert assault_spray.base_potency == 100
        assert DamageTag.ACTIVE in assault_spray.tags
        assert DamageTag.CORROSION in assault_spray.tags
        assert len(assault_spray.buffs_before) == 1
        # 5 damage boost per debuff * 6 debuffs = 30
        assert assault_spray.buffs_before[0].value == 30

    def test_assault_spray_v2_with_glucose_overload(self):
        assault_spray: DamageInstance = AssaultSprayV2().execute(
            number_of_debuffs_on_target=6, is_glucose_overload_followup=True
        )

        assert assault_spray.base_potency == 100
        assert len(assault_spray.buffs_before) == 2
        # First buff is debuff damage boost
        assert assault_spray.buffs_before[0].value == 30
        assert assault_spray.buffs_before[0].tag == DamageTag.ALL
        # Second buff is glucose overload damage boost
        assert assault_spray.buffs_before[1].value == 15
        assert assault_spray.buffs_before[1].tag == DamageTag.ACTIVE

    def test_assault_spray_v4_damage_boost(self):
        assault_spray: DamageInstance = AssaultSprayV4().execute(
            number_of_debuffs_on_target=6, is_glucose_overload_followup=False
        )

        assert assault_spray.base_potency == 100
        # 10 damage boost per debuff (V4 improvement) * 6 debuffs = 60
        assert assault_spray.buffs_before[0].value == 60

    def test_assault_spray_v4_with_glucose_overload(self):
        assault_spray: DamageInstance = AssaultSprayV4().execute(
            number_of_debuffs_on_target=6, is_glucose_overload_followup=True
        )

        assert len(assault_spray.buffs_before) == 2
        assert assault_spray.buffs_before[0].value == 60
        assert assault_spray.buffs_before[1].value == 15
        assert assault_spray.buffs_before[1].tag == DamageTag.ACTIVE

    def test_overwhelming_burst_base_with_max_conditions(self):
        overwhelming_burst: DamageInstance = OverwhelmingBurst().execute(
            has_fixed_key_4=True,
            is_confectance_index_at_maximum=True,
            stacks_of_candyglaze=30,
        )

        # 100 base + (5 per stack * 30 stacks) = 250
        assert overwhelming_burst.base_potency == 250
        assert DamageTag.ACTIVE in overwhelming_burst.tags
        assert DamageTag.CONFECTANCE in overwhelming_burst.tags
        # Should have fixed key 4 buff
        assert len(overwhelming_burst.buffs_before) == 1
        assert overwhelming_burst.buffs_before[0].value == 30
        assert overwhelming_burst.buffs_before[0].tag == DamageTag.ONLY_HIT_ONE_TARGET

    def test_overwhelming_burst_v2_with_glucose_overload(self):
        overwhelming_burst: DamageInstance = OverwhelmingBurstV2().execute(
            has_fixed_key_4=True,
            is_confectance_index_at_maximum=True,
            stacks_of_candyglaze=30,
            is_glucose_overload_followup=True,
        )

        assert overwhelming_burst.base_potency == 250
        # Should have fixed key 4 buff + glucose overload buff
        assert len(overwhelming_burst.buffs_before) == 2
        assert overwhelming_burst.buffs_before[0].value == 30
        assert overwhelming_burst.buffs_before[1].value == 15
        assert overwhelming_burst.buffs_before[1].tag == DamageTag.ACTIVE

    def test_overwhelming_burst_v5_with_glucose_overload(self):
        overwhelming_burst: DamageInstance = OverwhelmingBurstV5().execute(
            has_fixed_key_4=True,
            is_confectance_index_at_maximum=True,
            stacks_of_candyglaze=30,
            is_glucose_overload_followup=True,
        )

        # 120 base (V5) + (10 per stack (V5) * 30 stacks) = 420
        assert overwhelming_burst.base_potency == 420
        # Should have crit damage buff + fixed key 4 buff + glucose overload buff
        assert len(overwhelming_burst.buffs_before) == 3
        # Crit damage buff
        assert overwhelming_burst.buffs_before[0].value == 20
        assert overwhelming_burst.buffs_before[0].stat_type == StatType.CRIT_DAMAGE
        # Fixed key 4 buff
        assert overwhelming_burst.buffs_before[1].value == 30
        assert overwhelming_burst.buffs_before[1].tag == DamageTag.ONLY_HIT_ONE_TARGET
        # Glucose overload buff
        assert overwhelming_burst.buffs_before[2].value == 15
        assert overwhelming_burst.buffs_before[2].tag == DamageTag.ACTIVE

    def test_honeytrap_base(self):
        honeytrap: DamageInstance = Honeytrap().execute()

        assert honeytrap.base_potency == 80
        assert DamageTag.PASSIVE in honeytrap.tags
        assert DamageTag.CORROSION in honeytrap.tags
        assert honeytrap.buffs_before == []

    def test_honeytrap_v3(self):
        honeytrap: DamageInstance = HoneytrapV3().execute()

        assert honeytrap.base_potency == 120
        assert len(honeytrap.buffs_before) == 1
        assert honeytrap.buffs_before[0].value == 15
        assert honeytrap.buffs_before[0].stat_type == StatType.CRIT_DAMAGE

    def test_lind_fortification_levels(self):
        lind = Lind()

        # Test V0
        lind.set_to_v0()
        assert isinstance(lind.repulsive_shot, RepulsiveShot)
        assert isinstance(lind.assault_spray, AssaultSpray)
        assert isinstance(lind.overwhelming_burst, OverwhelmingBurst)
        assert isinstance(lind.honeytrap, Honeytrap)

        # Test V2
        lind.set_to_v2()
        assert isinstance(lind.repulsive_shot, RepulsiveShotV2)
        assert isinstance(lind.assault_spray, AssaultSprayV2)
        assert isinstance(lind.overwhelming_burst, OverwhelmingBurstV2)

        # Test V4
        lind.set_to_v4()
        assert isinstance(lind.assault_spray, AssaultSprayV4)

        # Test V5
        lind.set_to_v5()
        assert isinstance(lind.overwhelming_burst, OverwhelmingBurstV5)

        # Test V3 (Honeytrap upgrade)
        lind.set_to_v3()
        assert isinstance(lind.honeytrap, HoneytrapV3)

    def test_lind_fortification_level_setter(self):
        lind = Lind()

        lind.set_fortification_level(FortificationLevel.SEGMENT05)
        assert isinstance(lind.repulsive_shot, RepulsiveShotV2)
        assert isinstance(lind.assault_spray, AssaultSprayV4)
        assert isinstance(lind.overwhelming_burst, OverwhelmingBurstV5)
        assert isinstance(lind.honeytrap, HoneytrapV3)
