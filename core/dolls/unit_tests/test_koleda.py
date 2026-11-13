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
