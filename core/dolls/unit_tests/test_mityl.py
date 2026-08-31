from core.dolls.mityl import *
from core.types import (
    DamageTag,
    SpecialAttribute,
    StatType,
    FortificationLevel,
    ModifierType,
)
from core.buffs import Buff
from core.combat import DamageInstance, HologramCloneDamageCalculationStrategy


class TestMitylSkills:
    def test_ambush(self):
        ambush: DamageInstance = Ambush().execute()

        assert ambush.base_potency == 80
        assert DamageTag.ACTIVE in ambush.tags
        assert DamageTag.BASIC in ambush.tags
        assert DamageTag.LIGHT_AMMO in ambush.tags
        assert DamageTag.TARGETED in ambush.tags
        assert DamageTag.PHYSICAL in ambush.tags
        assert ambush.group_name == "Ambush"

    def test_aerial_dash_no_hydro_tiles(self):
        ad: DamageInstance = AerialDash().execute(
            starting_tile_is_hydro_tile=False, ending_tile_is_hydro_tile=False
        )

        assert ad.base_potency == 130
        assert DamageTag.ACTIVE in ad.tags
        assert DamageTag.LIGHT_AMMO in ad.tags
        assert DamageTag.TARGETED in ad.tags
        assert DamageTag.HYDRO in ad.tags
        assert DamageTag.PHASE in ad.tags
        assert DamageTag.CONFECTANCE in ad.tags
        assert ad.buffs_before == []
        assert ad.group_name == "Aerial Dash"

    def test_aerial_dash_partial_hydro_tiles_no_bonus(self):
        ad: DamageInstance = AerialDash().execute(
            starting_tile_is_hydro_tile=True, ending_tile_is_hydro_tile=False
        )

        assert ad.buffs_before == []

    def test_aerial_dash_both_hydro_tiles_grants_bonus(self):
        ad: DamageInstance = AerialDash().execute(
            starting_tile_is_hydro_tile=True, ending_tile_is_hydro_tile=True
        )

        assert ad.buffs_before == [
            Buff(
                30, ModifierType.ADDITIVE, SpecialAttribute.DAMAGE_BOOST, DamageTag.ALL
            )
        ]

    def test_aerial_dash_v4_no_hydro_tiles(self):
        ad: DamageInstance = AerialDashV4().execute(
            starting_tile_is_hydro_tile=False, ending_tile_is_hydro_tile=False
        )

        assert ad.base_potency == 160
        assert ad.buffs_before == []

    def test_aerial_dash_v4_partial_hydro_tile_grants_bonus(self):
        ad: DamageInstance = AerialDashV4().execute(
            starting_tile_is_hydro_tile=True, ending_tile_is_hydro_tile=False
        )

        assert ad.buffs_before == [
            Buff(
                50, ModifierType.ADDITIVE, SpecialAttribute.DAMAGE_BOOST, DamageTag.ALL
            )
        ]

    def test_aerial_dash_v4_both_hydro_tiles_grants_bonus(self):
        ad: DamageInstance = AerialDashV4().execute(
            starting_tile_is_hydro_tile=True, ending_tile_is_hydro_tile=True
        )

        assert ad.buffs_before == [
            Buff(
                50, ModifierType.ADDITIVE, SpecialAttribute.DAMAGE_BOOST, DamageTag.ALL
            )
        ]

    def test_support_action(self):
        sa: DamageInstance = SupportAction().execute()

        assert sa.base_potency == 0
        assert DamageTag.HYDRO in sa.tags
        assert DamageTag.PHASE in sa.tags
        assert DamageTag.PHYSICAL_SUMMON in sa.tags
        assert DamageTag.TARGETED in sa.tags
        assert DamageTag.PASSIVE in sa.tags
        assert DamageTag.SUPPORT_ACTION in sa.tags
        assert sa.group_name == "Support Action (Hologram - Clone)"
        assert isinstance(
            sa.damage_calculation_strategy, HologramCloneDamageCalculationStrategy
        )

    def test_support_action_v5(self):
        sa: DamageInstance = SupportActionV5().execute()

        assert sa.base_potency == 60
        assert sa.group_name == "Support Action (Hologram - Clone)"
        assert isinstance(
            sa.damage_calculation_strategy, HologramCloneDamageCalculationStrategy
        )

    def test_convergence_resonance(self):
        cr: DamageInstance = ConvergenceResonance().execute()

        assert cr.base_potency == 40
        assert DamageTag.HYDRO in cr.tags
        assert DamageTag.PHASE in cr.tags
        assert DamageTag.PHYSICAL_SUMMON in cr.tags
        assert DamageTag.TARGETED in cr.tags
        assert DamageTag.PASSIVE in cr.tags
        assert cr.group_name == "Convergence Resonance (Hologram - Clone)"
        assert isinstance(
            cr.damage_calculation_strategy, HologramCloneDamageCalculationStrategy
        )

    def test_convergence_resonance_v1(self):
        cr: DamageInstance = ConvergenceResonanceV1().execute()

        assert cr.base_potency == 60
        assert cr.group_name == "Convergence Resonance (Hologram - Clone)"

    def test_hologram_strike(self):
        hs: DamageInstance = HologramStrike().execute()

        assert hs.base_potency == 100
        assert DamageTag.HYDRO in hs.tags
        assert DamageTag.PHASE in hs.tags
        assert DamageTag.PHYSICAL_SUMMON in hs.tags
        assert DamageTag.TARGETED in hs.tags
        assert DamageTag.BASIC in hs.tags
        assert hs.group_name == "Hologram Strike (Hologram - Clone)"
        assert isinstance(
            hs.damage_calculation_strategy, HologramCloneDamageCalculationStrategy
        )

    def test_hologram_strike_v2(self):
        hs: DamageInstance = HologramStrikeV2().execute()

        assert hs.base_potency == 120
        assert hs.group_name == "Hologram Strike (Hologram - Clone)"


class TestMitylSummon:
    def test_get_summoned_unit_auto_summons_hologram_clone(self):
        mityl: Mityl = Mityl()

        summon = mityl.get_summoned_unit("Hologram - Clone")

        assert summon is not None
        assert summon.name == "Hologram - Clone"
        assert len(mityl.summoned_units) == 1

    def test_summon_hologram_clone_is_idempotent(self):
        mityl: Mityl = Mityl()

        mityl.summon_hologram_clone()
        mityl.summon_hologram_clone()

        assert len(mityl.summoned_units) == 1

    def test_refresh_hologram_clone_syncs_stats(self):
        """refresh_hologram_clone should snapshot Mityl's current stats onto the clone."""
        mityl: Mityl = Mityl()
        mityl.set_to_v0()
        mityl.initial_stats.basic_attributes[StatType.ATTACK] = 5000
        mityl.initial_stats.basic_attributes[StatType.HEALTH] = 3000

        mityl.refresh_hologram_clone()

        clone = next(u for u in mityl.summoned_units if u.name == "Hologram - Clone")
        assert clone.initial_stats.basic_attributes[StatType.ATTACK] == 5000
        assert clone.initial_stats.basic_attributes[StatType.HEALTH] == 3000

    def test_refresh_hologram_clone_replaces_stale_summon(self):
        """Calling refresh_hologram_clone twice leaves exactly one clone."""
        mityl: Mityl = Mityl()
        mityl.set_to_v0()
        mityl.initial_stats.basic_attributes[StatType.ATTACK] = 1111

        mityl.refresh_hologram_clone()
        mityl.initial_stats.basic_attributes[StatType.ATTACK] = 2222
        mityl.refresh_hologram_clone()

        assert len(mityl.summoned_units) == 1
        clone = next(u for u in mityl.summoned_units if u.name == "Hologram - Clone")
        assert clone.initial_stats.basic_attributes[StatType.ATTACK] == 2222

    def test_prepare_for_calculation_refreshes_hologram_clone(self):
        """prepare_for_calculation should act as refresh_hologram_clone."""
        mityl: Mityl = Mityl()
        mityl.set_to_v0()
        mityl.initial_stats.basic_attributes[StatType.ATTACK] = 4000

        mityl.prepare_for_calculation()

        assert len(mityl.summoned_units) == 1
        clone = next(u for u in mityl.summoned_units if u.name == "Hologram - Clone")
        assert clone.initial_stats.basic_attributes[StatType.ATTACK] == 4000


class TestMitylFortification:
    def test_set_to_v0(self):
        mityl: Mityl = Mityl()
        mityl.set_to_v0()

        assert isinstance(mityl.ambush, Ambush)
        assert isinstance(mityl.aerial_dash, AerialDash)
        assert isinstance(mityl.support_action, SupportAction)
        assert isinstance(mityl.convergence_resonance, ConvergenceResonance)
        assert isinstance(mityl.hologram_strike, HologramStrike)
        assert mityl.get_summoned_unit("Hologram - Clone") is not None

    def test_set_to_v1(self):
        mityl: Mityl = Mityl()
        mityl.set_to_v1()

        assert isinstance(mityl.convergence_resonance, ConvergenceResonanceV1)

    def test_set_to_v2(self):
        mityl: Mityl = Mityl()
        mityl.set_to_v2()

        assert isinstance(mityl.hologram_strike, HologramStrikeV2)
        assert isinstance(mityl.convergence_resonance, ConvergenceResonanceV1)

    def test_set_to_v4(self):
        mityl: Mityl = Mityl()
        mityl.set_to_v4()

        assert isinstance(mityl.aerial_dash, AerialDashV4)
        assert isinstance(mityl.hologram_strike, HologramStrikeV2)

    def test_set_to_v5(self):
        mityl: Mityl = Mityl()
        mityl.set_to_v5()

        assert isinstance(mityl.support_action, SupportActionV5)
        assert isinstance(mityl.aerial_dash, AerialDashV4)

    def test_set_fortification_level_segment03_matches_v2(self):
        mityl: Mityl = Mityl()
        mityl.set_fortification_level(FortificationLevel.SEGMENT03)

        assert isinstance(mityl.hologram_strike, HologramStrikeV2)
        assert isinstance(mityl.aerial_dash, AerialDash)

    def test_set_fortification_level_segment06_matches_v5(self):
        mityl: Mityl = Mityl()
        mityl.set_fortification_level(FortificationLevel.SEGMENT06)

        assert isinstance(mityl.support_action, SupportActionV5)
        assert isinstance(mityl.aerial_dash, AerialDashV4)

    def test_set_to_v0_after_v5_resets_upgraded_skills(self):
        mityl: Mityl = Mityl()
        mityl.set_to_v5()

        assert isinstance(mityl.support_action, SupportActionV5)

        mityl.set_to_v0()

        assert isinstance(mityl.support_action, SupportAction)
        assert isinstance(mityl.aerial_dash, AerialDash)
