from core.dolls.welrod import *

from core.combat import (
    DamageInstance,
    WelrodStandardDamageCalculationStrategy,
    WelrodConvictionAndPunishmentDamageCalculationStrategy,
    WelrodCrimeBacklashDamageCalculationStrategy,
)
from core.types import DamageTag, FortificationLevel


class TestWelrodSkills:
    def test_silent_takedown(self):
        da: DamageInstance = SilentTakedown().execute()

        assert da.base_potency == 80
        assert DamageTag.ACTIVE in da.tags
        assert DamageTag.BASIC in da.tags
        assert DamageTag.LIGHT_AMMO in da.tags
        assert DamageTag.TARGETED in da.tags
        assert DamageTag.PHYSICAL in da.tags
        assert da.group_name == "Silent Takedown"
        assert isinstance(
            da.damage_calculation_strategy, WelrodStandardDamageCalculationStrategy
        )

    def test_joint_investigation(self):
        da: DamageInstance = JointInvestigation().execute()

        assert da.base_potency == 100
        assert DamageTag.ACTIVE in da.tags
        assert DamageTag.CORROSION in da.tags
        assert DamageTag.PHASE in da.tags
        assert DamageTag.AREA_OF_EFFECT in da.tags
        assert da.group_name == "Joint Investigation"

    def test_conviction_and_punishment(self):
        da: DamageInstance = ConvictionAndPunishment().execute()

        assert da.base_potency == 100
        assert da.group_name == "Conviction and Punishment"
        assert isinstance(
            da.damage_calculation_strategy,
            WelrodConvictionAndPunishmentDamageCalculationStrategy,
        )
        assert da.damage_calculation_strategy.potency_to_max_health_increase == 1
        assert da.damage_calculation_strategy.maximum_potency_increase == 60

    def test_conviction_and_punishment_v4(self):
        da: DamageInstance = ConvictionAndPunishmentV4().execute()

        assert da.base_potency == 120
        assert DamageTag.TARGETED in da.tags
        assert DamageTag.CONFECTANCE in da.tags
        assert da.group_name == "Conviction and Punishment"
        assert isinstance(
            da.damage_calculation_strategy,
            WelrodConvictionAndPunishmentDamageCalculationStrategy,
        )
        assert da.damage_calculation_strategy.potency_to_max_health_increase == 1.5
        assert da.damage_calculation_strategy.maximum_potency_increase == 150

    def test_hour_of_reckoning(self):
        da: DamageInstance = HourOfReckoning().execute(
            instances_of_damage_taken=0, number_of_targets_hit=0
        )

        assert da.base_potency == 100
        assert DamageTag.ULTIMATE in da.tags
        assert da.group_name == "Hour of Reckoning"

    def test_hour_of_reckoning_v3(self):
        da: DamageInstance = HourOfReckoningV3().execute(
            instances_of_damage_taken=0, number_of_targets_hit=0
        )

        assert da.base_potency == 120
        assert da.group_name == "Hour of Reckoning"

    def test_hour_of_reckoning_v5_scaling(self):
        da: DamageInstance = HourOfReckoningV5().execute(
            instances_of_damage_taken=1, number_of_targets_hit=2
        )

        assert da.base_potency == 120
        assert len(da.buffs_before) == 2
        # 1 instance of damage taken -> 40 damage boost (capped at 80)
        assert da.buffs_before[0].value == 40
        # 2 targets hit -> 40 damage boost (capped at 100)
        assert da.buffs_before[1].value == 40

    def test_hour_of_reckoning_v5_caps(self):
        da: DamageInstance = HourOfReckoningV5().execute(
            instances_of_damage_taken=10, number_of_targets_hit=10
        )

        assert da.buffs_before[0].value == 80
        assert da.buffs_before[1].value == 100

    def test_crime_backlash(self):
        da: DamageInstance = CrimeBacklashAction().execute(
            detectives_immunity_accumulated_damage=1000
        )

        assert da.base_potency == 100
        assert DamageTag.PASSIVE in da.tags
        assert da.group_name == "Crime Backlash"
        assert isinstance(
            da.damage_calculation_strategy,
            WelrodCrimeBacklashDamageCalculationStrategy,
        )
        assert da.damage_calculation_strategy.accumulated_damage == 1000
        assert da.damage_calculation_strategy.fraction_of_accumulated_damage == 0.25
        assert da.damage_calculation_strategy.fraction_of_maximum_health == 0.15

    def test_crime_backlash_v3(self):
        da: DamageInstance = CrimeBacklashActionV3().execute(
            detectives_immunity_accumulated_damage=1000
        )

        assert isinstance(
            da.damage_calculation_strategy,
            WelrodCrimeBacklashDamageCalculationStrategy,
        )
        assert da.damage_calculation_strategy.fraction_of_accumulated_damage == 0.50
        assert da.damage_calculation_strategy.fraction_of_maximum_health == 0.30

    def test_suspect(self):
        da: DamageInstance = SuspectAction().execute()

        assert da.base_potency == 180
        assert da.group_name == "Suspect"
        assert DamageTag.FIXED in da.tags

    def test_suspect_v5(self):
        da: DamageInstance = SuspectActionV5().execute()

        assert da.base_potency == 360
        assert da.group_name == "Suspect"

    def test_case_detective(self):
        da: DamageInstance = CaseDetectiveEndOfAction().execute(
            detectives_immunity_accumulated_damage=500
        )

        assert da.base_potency == 100
        assert da.group_name == "Case Detective"
        assert isinstance(
            da.damage_calculation_strategy,
            WelrodCrimeBacklashDamageCalculationStrategy,
        )
        assert da.damage_calculation_strategy.fraction_of_accumulated_damage == 0.30
        assert da.damage_calculation_strategy.fraction_of_maximum_health == 0


class TestWelrod:
    def test_set_to_v0(self):
        welrod: Welrod = Welrod()
        welrod.set_to_v0()

        assert isinstance(welrod.silent_takedown, SilentTakedown)
        assert isinstance(welrod.joint_investigation, JointInvestigation)
        assert isinstance(welrod.conviction_and_punishment, ConvictionAndPunishment)
        assert isinstance(welrod.crime_backlash, CrimeBacklashAction)
        assert isinstance(welrod.suspect, SuspectAction)
        assert isinstance(welrod.hour_of_reckoning, HourOfReckoning)
        assert isinstance(welrod.case_detective, CaseDetectiveEndOfAction)

    def test_set_to_v3(self):
        welrod: Welrod = Welrod()
        welrod.set_to_v3()

        assert isinstance(welrod.hour_of_reckoning, HourOfReckoningV3)
        assert isinstance(welrod.crime_backlash, CrimeBacklashActionV3)
        # V0 actions should still be intact (cumulative setup)
        assert isinstance(welrod.silent_takedown, SilentTakedown)

    def test_set_to_v4(self):
        welrod: Welrod = Welrod()
        welrod.set_to_v4()

        assert isinstance(welrod.conviction_and_punishment, ConvictionAndPunishmentV4)
        # V3 actions should still be intact (cumulative setup)
        assert isinstance(welrod.hour_of_reckoning, HourOfReckoningV3)

    def test_set_to_v5(self):
        welrod: Welrod = Welrod()
        welrod.set_to_v5()

        assert isinstance(welrod.hour_of_reckoning, HourOfReckoningV5)
        assert isinstance(welrod.suspect, SuspectActionV5)
        # V4 actions should still be intact (cumulative setup)
        assert isinstance(welrod.conviction_and_punishment, ConvictionAndPunishmentV4)

    def test_set_fortification_level(self):
        welrod: Welrod = Welrod()

        welrod.set_fortification_level(FortificationLevel.SEGMENT00)
        assert isinstance(welrod.hour_of_reckoning, HourOfReckoning)

        welrod.set_fortification_level(FortificationLevel.SEGMENT03)
        assert isinstance(welrod.hour_of_reckoning, HourOfReckoningV3)

        welrod.set_fortification_level(FortificationLevel.SEGMENT04)
        assert isinstance(welrod.conviction_and_punishment, ConvictionAndPunishmentV4)

        welrod.set_fortification_level(FortificationLevel.SEGMENT05)
        assert isinstance(welrod.hour_of_reckoning, HourOfReckoningV5)
        assert isinstance(welrod.suspect, SuspectActionV5)

        welrod.set_fortification_level(FortificationLevel.SEGMENT06)
        assert welrod.fortification_level == FortificationLevel.SEGMENT06
        assert isinstance(welrod.hour_of_reckoning, HourOfReckoningV5)
