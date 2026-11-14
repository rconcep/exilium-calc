"""Unit tests for Koleda doll and Sinveiler summon."""

import pytest
from core.dolls.koleda import (
    Koleda,
    SinveilerGear,
    PredatorInstinct,
    SnowWolfsEye,
    SnowWolfsEyeV1,
    LetsGoForADrift,
    LetsGoForADriftV3,
    LetsGoForADriftV4,
    LetsGoFullSpeed,
    LetsGoFullSpeedV3,
    LetsGoFullSpeedV5,
    LetsGoFullSpeedPursuit,
    LetsGoFullSpeedPursuitV3,
    LetsGoFullSpeedPursuitV5,
    KineticRelease,
    KineticReleaseV2,
    KineticReleaseV3,
    KineticReleasePlus,
    KineticReleasePlusV2,
    KineticReleasePlusV3,
    KoledaKineticRelease,
    KoledaKineticReleaseV2,
    KoledaKineticReleasePlus,
    KoledaKineticReleasePlusV2,
)
from core.types import (
    DamageTag,
    FortificationLevel,
    StatType,
)


class TestPredatorInstinct:
    """Tests for PredatorInstinct (basic attack)."""

    def test_predator_instinct_no_args(self) -> None:
        """Basic attack should execute without arguments."""
        skill = PredatorInstinct()
        result = skill.execute()
        assert result.label == "Predator Instinct"
        assert result.base_potency == 90
        assert DamageTag.ACTIVE in result.tags
        assert DamageTag.BASIC in result.tags
        assert DamageTag.MEDIUM_AMMO in result.tags
        assert DamageTag.HYDRO in result.tags

    def test_predator_instinct_group_name(self) -> None:
        """Basic attack should have correct group name."""
        skill = PredatorInstinct()
        result = skill.execute()
        assert result.group_name == "Predator Instinct"


class TestSnowWolfsEye:
    """Tests for Snow Wolf's Eye (S1)."""

    def test_snow_wolfs_eye_no_stacks(self) -> None:
        """S1 base version with no stacks."""
        skill = SnowWolfsEye()
        result = skill.execute(stacks_of_upshift=0)
        assert result.label == "Snow Wolf's Eye"
        assert result.base_potency == 150

    def test_snow_wolfs_eye_with_stacks(self) -> None:
        """S1 base version has no scaling with stacks."""
        skill = SnowWolfsEye()
        result = skill.execute(stacks_of_upshift=5)
        assert result.base_potency == 150  # No stack scaling

    def test_snow_wolfs_eye_v1_no_stacks(self) -> None:
        """S1 V1 version with no stacks."""
        skill = SnowWolfsEyeV1()
        result = skill.execute(stacks_of_upshift=0)
        assert result.base_potency == 180

    def test_snow_wolfs_eye_v1_with_stacks(self) -> None:
        """S1 V1 scales with stacks (+15 per stack)."""
        skill = SnowWolfsEyeV1()
        result = skill.execute(stacks_of_upshift=5)
        assert result.base_potency == 180 + (15 * 5)  # 255


class TestLetsGoForADrift:
    """Tests for Let's Go for a Drift! (S2 - Sinveiler)."""

    def test_base_version(self) -> None:
        """Base version without S+ bonus."""
        skill = LetsGoForADrift()
        result = skill.execute(gear=SinveilerGear.P)
        assert result.base_potency == 90
        assert result.label == "Let's Go for a Drift! (Sinveiler)"
        assert DamageTag.AREA_OF_EFFECT in result.tags

    def test_v3_version_no_bonus(self) -> None:
        """V3 with non-S+ gear."""
        skill = LetsGoForADriftV3()
        result = skill.execute(gear=SinveilerGear.D)
        assert result.base_potency == 90

    def test_v3_version_s_plus_bonus(self) -> None:
        """V3 with S+ gear applies +30 bonus."""
        skill = LetsGoForADriftV3()
        result = skill.execute(gear=SinveilerGear.S_PLUS)
        assert result.base_potency == 120  # 90 + 30

    def test_v4_version_no_bonus(self) -> None:
        """V4 with non-S+ gear."""
        skill = LetsGoForADriftV4()
        result = skill.execute(gear=SinveilerGear.S)
        assert result.base_potency == 120

    def test_v4_version_s_plus_bonus(self) -> None:
        """V4 with S+ gear applies +30 bonus."""
        skill = LetsGoForADriftV4()
        result = skill.execute(gear=SinveilerGear.S_PLUS)
        assert result.base_potency == 150  # 120 + 30


class TestLetsGoFullSpeed:
    """Tests for Let's Go Full Speed! (S3 - Sinveiler)."""

    def test_base_version(self) -> None:
        """Base version without S+ bonus."""
        skill = LetsGoFullSpeed()
        result = skill.execute(gear=SinveilerGear.P)
        assert result.base_potency == 90

    def test_v3_version_s_plus_bonus(self) -> None:
        """V3 with S+ gear applies +30 bonus."""
        skill = LetsGoFullSpeedV3()
        result = skill.execute(gear=SinveilerGear.S_PLUS)
        assert result.base_potency == 120  # 90 + 30

    def test_v5_version_no_bonus(self) -> None:
        """V5 with non-S+ gear."""
        skill = LetsGoFullSpeedV5()
        result = skill.execute(gear=SinveilerGear.D)
        assert result.base_potency == 120

    def test_v5_version_s_plus_bonus(self) -> None:
        """V5 with S+ gear applies +30 bonus."""
        skill = LetsGoFullSpeedV5()
        result = skill.execute(gear=SinveilerGear.S_PLUS)
        assert result.base_potency == 150  # 120 + 30


class TestLetsGoFullSpeedPursuit:
    """Tests for Let's Go Full Speed! Pursuit (S3 followup)."""

    def test_base_version_p_gear(self) -> None:
        """Base version with P gear (no pursuit)."""
        skill = LetsGoFullSpeedPursuit()
        result = skill.execute(gear=SinveilerGear.P)
        assert result.base_potency == 0

    def test_base_version_s_gear(self) -> None:
        """Base version with S gear triggers pursuit."""
        skill = LetsGoFullSpeedPursuit()
        result = skill.execute(gear=SinveilerGear.S)
        assert result.base_potency == 60

    def test_base_version_s_plus_gear(self) -> None:
        """Base version with S+ gear triggers pursuit."""
        skill = LetsGoFullSpeedPursuit()
        result = skill.execute(gear=SinveilerGear.S_PLUS)
        assert result.base_potency == 90

    def test_v3_s_gear(self) -> None:
        """V3 with S gear."""
        skill = LetsGoFullSpeedPursuitV3()
        result = skill.execute(gear=SinveilerGear.S)
        assert result.base_potency == 60

    def test_v3_s_plus_gear(self) -> None:
        """V3 with S+ gear applies bonus."""
        skill = LetsGoFullSpeedPursuitV3()
        result = skill.execute(gear=SinveilerGear.S_PLUS)
        assert result.base_potency == 120  # 60 + 30 (V3 S+ bonus)

    def test_v5_s_gear(self) -> None:
        """V5 with S gear."""
        skill = LetsGoFullSpeedPursuitV5()
        result = skill.execute(gear=SinveilerGear.S)
        assert result.base_potency == 90

    def test_v5_s_plus_gear(self) -> None:
        """V5 with S+ gear applies bonus."""
        skill = LetsGoFullSpeedPursuitV5()
        result = skill.execute(gear=SinveilerGear.S_PLUS)
        assert result.base_potency == 150  # 90 + 30 (V5 S+ bonus)


class TestKineticRelease:
    """Tests for Kinetic Release (S3 followup from S Gear)."""

    def test_base_version(self) -> None:
        """Base version."""
        skill = KineticRelease()
        result = skill.execute(gear=SinveilerGear.P)
        assert result.base_potency == 90

    def test_v2_version(self) -> None:
        """V2 version with higher potency."""
        skill = KineticReleaseV2()
        result = skill.execute(gear=SinveilerGear.P)
        assert result.base_potency == 120

    def test_v3_no_bonus(self) -> None:
        """V3 with non-S+ gear."""
        skill = KineticReleaseV3()
        result = skill.execute(gear=SinveilerGear.S)
        assert result.base_potency == 120

    def test_v3_s_plus_bonus(self) -> None:
        """V3 with S+ gear applies +30 bonus."""
        skill = KineticReleaseV3()
        result = skill.execute(gear=SinveilerGear.S_PLUS)
        assert result.base_potency == 150  # 120 + 30


class TestKineticReleasePlus:
    """Tests for Kinetic Release+ (S3+ followup from S+ Gear)."""

    def test_base_version(self) -> None:
        """Base version."""
        skill = KineticReleasePlus()
        result = skill.execute(gear=SinveilerGear.P)
        assert result.base_potency == 120

    def test_v2_version(self) -> None:
        """V2 version with higher potency."""
        skill = KineticReleasePlusV2()
        result = skill.execute(gear=SinveilerGear.P)
        assert result.base_potency == 150

    def test_v3_no_bonus(self) -> None:
        """V3 with non-S+ gear."""
        skill = KineticReleasePlusV3()
        result = skill.execute(gear=SinveilerGear.S)
        assert result.base_potency == 150

    def test_v3_s_plus_bonus(self) -> None:
        """V3 with S+ gear applies +30 bonus."""
        skill = KineticReleasePlusV3()
        result = skill.execute(gear=SinveilerGear.S_PLUS)
        assert result.base_potency == 180  # 150 + 30


class TestKoledaKineticRelease:
    """Tests for Kinetic Release performed by Koleda."""

    def test_base_version(self) -> None:
        """Base version."""
        skill = KoledaKineticRelease()
        result = skill.execute()
        assert result.label == "Kinetic Release (Koleda)"
        assert result.base_potency == 90
        assert DamageTag.AREA_OF_EFFECT in result.tags
        assert DamageTag.PHYSICAL_SUMMON not in result.tags  # Koleda action, not Sinveiler

    def test_base_version_has_no_physical_summon_tag(self) -> None:
        """Base version should NOT have PHYSICAL_SUMMON tag."""
        skill = KoledaKineticRelease()
        result = skill.execute()
        assert DamageTag.PHYSICAL_SUMMON not in result.tags

    def test_v2_version(self) -> None:
        """V2 version with higher potency."""
        skill = KoledaKineticReleaseV2()
        result = skill.execute()
        assert result.base_potency == 120
        assert DamageTag.AREA_OF_EFFECT in result.tags
        assert DamageTag.PHYSICAL_SUMMON not in result.tags

    def test_all_versions_have_hydro_phase_tags(self) -> None:
        """All Koleda Kinetic Release versions should have HYDRO and PHASE tags."""
        for skill_class in [KoledaKineticRelease, KoledaKineticReleaseV2]:
            skill = skill_class()
            result = skill.execute()
            assert DamageTag.HYDRO in result.tags
            assert DamageTag.PHASE in result.tags


class TestKoledaKineticReleasePlus:
    """Tests for Kinetic Release+ performed by Koleda."""

    def test_base_version(self) -> None:
        """Base version."""
        skill = KoledaKineticReleasePlus()
        result = skill.execute()
        assert result.label == "Kinetic Release+ (Koleda)"
        assert result.base_potency == 120
        assert DamageTag.AREA_OF_EFFECT in result.tags
        assert DamageTag.PHYSICAL_SUMMON not in result.tags

    def test_v2_version(self) -> None:
        """V2 version with higher potency."""
        skill = KoledaKineticReleasePlusV2()
        result = skill.execute()
        assert result.base_potency == 150
        assert DamageTag.PHYSICAL_SUMMON not in result.tags

    def test_all_versions_have_hydro_phase_tags(self) -> None:
        """All Koleda Kinetic Release+ versions should have HYDRO and PHASE tags."""
        for skill_class in [KoledaKineticReleasePlus, KoledaKineticReleasePlusV2]:
            skill = skill_class()
            result = skill.execute()
            assert DamageTag.HYDRO in result.tags
            assert DamageTag.PHASE in result.tags


class TestKoledaFortification:
    """Tests for Koleda's fortification level system."""

    def test_koleda_v0_initialization(self) -> None:
        """Koleda at V0 has base versions of skills."""
        koleda = Koleda()
        koleda.set_fortification_level(FortificationLevel.SEGMENT00)

        assert isinstance(koleda.snow_wolfs_eye, SnowWolfsEye)
        assert isinstance(koleda.lets_go_for_a_drift, LetsGoForADrift)
        assert isinstance(koleda.lets_go_full_speed, LetsGoFullSpeed)

    def test_koleda_v1_snow_wolfs_eye_upgrade(self) -> None:
        """Koleda at V1 upgrades Snow Wolf's Eye to V1."""
        koleda = Koleda()
        koleda.set_fortification_level(FortificationLevel.SEGMENT01)

        assert isinstance(koleda.snow_wolfs_eye, SnowWolfsEyeV1)
        # V1 result with 5 stacks should be 180 + 75 = 255
        result = koleda.snow_wolfs_eye.execute(stacks_of_upshift=5)
        assert result.base_potency == 255

    def test_koleda_v3_skill_upgrades(self) -> None:
        """Koleda at V3 upgrades applicable Sinveiler skills."""
        koleda = Koleda()
        koleda.set_fortification_level(FortificationLevel.SEGMENT03)

        assert isinstance(koleda.lets_go_for_a_drift, LetsGoForADriftV3)
        assert isinstance(koleda.lets_go_full_speed, LetsGoFullSpeedV3)
        assert isinstance(koleda.lets_go_full_speed_pursuit, LetsGoFullSpeedPursuitV3)
        assert isinstance(koleda.kinetic_release, KineticReleaseV3)
        assert isinstance(koleda.kinetic_release_plus, KineticReleasePlusV3)
        # Koleda's kinetic release actions stay at V2 (not affected by S+ Gear bonuses)
        assert isinstance(koleda.koleda_kinetic_release, KoledaKineticReleaseV2)
        assert isinstance(koleda.koleda_kinetic_release_plus, KoledaKineticReleasePlusV2)

    def test_koleda_v4_additional_upgrades(self) -> None:
        """Koleda at V4 upgrades Let's Go for a Drift to V4."""
        koleda = Koleda()
        koleda.set_fortification_level(FortificationLevel.SEGMENT04)

        assert isinstance(koleda.lets_go_for_a_drift, LetsGoForADriftV4)
        # V4 has 120 base
        result = koleda.lets_go_for_a_drift.execute(gear=SinveilerGear.P)
        assert result.base_potency == 120

    def test_koleda_v5_lets_go_full_speed_upgrade(self) -> None:
        """Koleda at V5 upgrades Let's Go Full Speed to V5."""
        koleda = Koleda()
        koleda.set_fortification_level(FortificationLevel.SEGMENT05)

        assert isinstance(koleda.lets_go_full_speed, LetsGoFullSpeedV5)
        assert isinstance(koleda.lets_go_full_speed_pursuit, LetsGoFullSpeedPursuitV5)

    def test_koleda_v6_same_as_v5(self) -> None:
        """Koleda at V6 has same skills as V5."""
        koleda_v5 = Koleda()
        koleda_v5.set_fortification_level(FortificationLevel.SEGMENT05)

        koleda_v6 = Koleda()
        koleda_v6.set_fortification_level(FortificationLevel.SEGMENT06)

        assert type(koleda_v5.lets_go_full_speed) == type(koleda_v6.lets_go_full_speed)
        assert type(koleda_v5.lets_go_full_speed_pursuit) == type(
            koleda_v6.lets_go_full_speed_pursuit
        )


class TestKoledaSinveiler:
    """Tests for Sinveiler summon."""

    def test_sinveiler_created_on_initialization(self) -> None:
        """Sinveiler should be created when Koleda is initialized."""
        koleda = Koleda()
        koleda.prepare_for_calculation()

        sinveiler = koleda.get_summoned_unit("Sinveiler")
        assert sinveiler is not None
        assert sinveiler.name == "Sinveiler"

    def test_sinveiler_inherits_stats(self) -> None:
        """Sinveiler should inherit Koleda's stats."""
        koleda = Koleda()
        koleda.initial_stats.basic_attributes[StatType.ATTACK] = 1000
        koleda.initial_stats.basic_attributes[StatType.CRIT_RATE] = 50

        koleda.prepare_for_calculation()
        sinveiler = koleda.get_summoned_unit("Sinveiler")

        assert sinveiler is not None
        assert sinveiler.initial_stats.basic_attributes[StatType.ATTACK] == 1000
        assert sinveiler.initial_stats.basic_attributes[StatType.CRIT_RATE] == 50

    def test_sinveiler_refresh_on_stat_change(self) -> None:
        """Sinveiler should be refreshed when Koleda's stats change."""
        koleda = Koleda()
        koleda.initial_stats.basic_attributes[StatType.ATTACK] = 1000
        koleda.prepare_for_calculation()

        sinveiler1 = koleda.get_summoned_unit("Sinveiler")
        assert sinveiler1.initial_stats.basic_attributes[StatType.ATTACK] == 1000

        # Change Koleda's stats
        koleda.initial_stats.basic_attributes[StatType.ATTACK] = 2000
        koleda.refresh_sinveiler()

        sinveiler2 = koleda.get_summoned_unit("Sinveiler")
        assert sinveiler2.initial_stats.basic_attributes[StatType.ATTACK] == 2000

    def test_multiple_sinveiler_calls_idempotent(self) -> None:
        """Multiple calls to summon_sinveiler should be idempotent."""
        koleda = Koleda()
        koleda.summon_sinveiler()
        koleda.summon_sinveiler()
        koleda.summon_sinveiler()

        # Should only have one Sinveiler
        sinveilers = [u for u in koleda.summoned_units if u.name == "Sinveiler"]
        assert len(sinveilers) == 1


class TestSinveilerGearEnum:
    """Tests for SinveilerGear enum."""

    def test_all_gear_values(self) -> None:
        """All gear types should be defined."""
        assert SinveilerGear.P == "P Gear"
        assert SinveilerGear.N == "N Gear"
        assert SinveilerGear.D == "D Gear"
        assert SinveilerGear.S == "S Gear"
        assert SinveilerGear.S_PLUS == "S+ Gear"

    def test_gear_is_string_enum(self) -> None:
        """SinveilerGear values should be strings."""
        assert isinstance(SinveilerGear.P.value, str)
        assert isinstance(SinveilerGear.S_PLUS.value, str)


class TestKoledaDriverInheritance:
    """Tests for Koleda's driver stat inheritance system."""

    def test_set_driver_default_values(self) -> None:
        """Driver stats should default to 0."""
        koleda = Koleda()
        assert koleda.driver_attack == 0.0
        assert koleda.driver_defense == 0.0
        assert koleda.driver_health == 0.0
        assert koleda.driver_crit_damage == 0.0

    def test_set_driver_stats(self) -> None:
        """set_driver() should store driver stats."""
        koleda = Koleda()
        koleda.set_driver(attack=1000, defense=500, health=2000, crit_damage=50)
        assert koleda.driver_attack == 1000
        assert koleda.driver_defense == 500
        assert koleda.driver_health == 2000
        assert koleda.driver_crit_damage == 50

    def test_driver_inheritance_rate_v0_to_v5(self) -> None:
        """V0-V5 should have 50% driver inheritance rate."""
        koleda = Koleda()
        for level in [
            FortificationLevel.SEGMENT00,
            FortificationLevel.SEGMENT01,
            FortificationLevel.SEGMENT02,
            FortificationLevel.SEGMENT03,
            FortificationLevel.SEGMENT04,
            FortificationLevel.SEGMENT05,
        ]:
            koleda.set_fortification_level(level)
            assert koleda._get_driver_inheritance_rate() == 0.50

    def test_driver_inheritance_rate_v3(self) -> None:
        """V3 should have 50% driver inheritance rate."""
        koleda = Koleda()
        koleda.set_fortification_level(FortificationLevel.SEGMENT03)
        assert koleda._get_driver_inheritance_rate() == 0.50

    def test_driver_inheritance_rate_v4(self) -> None:
        """V4 should have 50% driver inheritance rate."""
        koleda = Koleda()
        koleda.set_fortification_level(FortificationLevel.SEGMENT04)
        assert koleda._get_driver_inheritance_rate() == 0.50

    def test_driver_inheritance_rate_v5_v6(self) -> None:
        """V5 should have 50%, V6 should have 70% driver inheritance rate."""
        koleda = Koleda()
        koleda.set_fortification_level(FortificationLevel.SEGMENT05)
        assert koleda._get_driver_inheritance_rate() == 0.50
        
        koleda.set_fortification_level(FortificationLevel.SEGMENT06)
        assert koleda._get_driver_inheritance_rate() == 0.70

    def test_driver_inheritance_applied_v3(self) -> None:
        """Driver stats should be applied to Sinveiler at V3 (50%)."""
        koleda = Koleda()
        koleda.set_fortification_level(FortificationLevel.SEGMENT03)

        # Set initial Koleda stats
        koleda.initial_stats.basic_attributes[StatType.ATTACK] = 1000

        # Set driver stats
        koleda.set_driver(attack=2000, defense=500, health=3000, crit_damage=50)

        # Refresh Sinveiler
        koleda.prepare_for_calculation()

        # Get Sinveiler
        sinveiler = koleda.get_summoned_unit("Sinveiler")
        assert sinveiler is not None

        # Sinveiler should have Koleda's attack + 50% of driver's attack
        expected_attack = 1000 + (2000 * 0.50)  # 2000
        assert sinveiler.initial_stats.basic_attributes[StatType.ATTACK] == expected_attack

    def test_driver_inheritance_applied_v6(self) -> None:
        """Driver stats should be applied to Sinveiler at V6 (70%)."""
        koleda = Koleda()
        koleda.set_fortification_level(FortificationLevel.SEGMENT06)

        # Set initial Koleda stats
        koleda.initial_stats.basic_attributes[StatType.DEFENSE] = 500

        # Set driver stats
        koleda.set_driver(attack=1000, defense=1000, health=2000, crit_damage=100)

        # Refresh Sinveiler
        koleda.prepare_for_calculation()

        # Get Sinveiler
        sinveiler = koleda.get_summoned_unit("Sinveiler")
        assert sinveiler is not None

        # Sinveiler should have Koleda's defense + 70% of driver's defense
        expected_defense = 500 + (1000 * 0.70)  # 1200
        assert sinveiler.initial_stats.basic_attributes[StatType.DEFENSE] == expected_defense

    def test_no_driver_inheritance_without_driver_stats(self) -> None:
        """Sinveiler should not be affected if driver stats are all 0."""
        koleda = Koleda()
        koleda.set_fortification_level(FortificationLevel.SEGMENT06)

        # Set Koleda's initial stats
        initial_attack = 1000
        koleda.initial_stats.basic_attributes[StatType.ATTACK] = initial_attack

        # No driver stats set (all default to 0)
        koleda.prepare_for_calculation()

        sinveiler = koleda.get_summoned_unit("Sinveiler")
        assert sinveiler is not None

        # Sinveiler should only have Koleda's stats
        assert sinveiler.initial_stats.basic_attributes[StatType.ATTACK] == initial_attack

    def test_driver_inheritance_multiple_stats(self) -> None:
        """All driver stats should be inherited proportionally."""
        koleda = Koleda()
        koleda.set_fortification_level(FortificationLevel.SEGMENT04)

        koleda.initial_stats.basic_attributes[StatType.ATTACK] = 1000
        koleda.initial_stats.basic_attributes[StatType.DEFENSE] = 500
        koleda.initial_stats.basic_attributes[StatType.HEALTH] = 2000
        koleda.initial_stats.basic_attributes[StatType.CRIT_DAMAGE] = 100

        koleda.set_driver(attack=2000, defense=1000, health=4000, crit_damage=200)

        koleda.prepare_for_calculation()
        sinveiler = koleda.get_summoned_unit("Sinveiler")
        assert sinveiler is not None

        # V4 = 50% inheritance rate
        assert sinveiler.initial_stats.basic_attributes[StatType.ATTACK] == 1000 + (2000 * 0.50)  # 2000
        assert sinveiler.initial_stats.basic_attributes[StatType.DEFENSE] == 500 + (1000 * 0.50)  # 1000
        assert sinveiler.initial_stats.basic_attributes[StatType.HEALTH] == 2000 + (4000 * 0.50)  # 4000
        assert sinveiler.initial_stats.basic_attributes[StatType.CRIT_DAMAGE] == 100 + (200 * 0.50)  # 200
