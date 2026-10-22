from core.dolls.mityl import *
from core.types import (
    DamageTag,
    SpecialAttribute,
    StatType,
    FortificationLevel,
    ModifierType,
)
from core.buffs import Buff
from core.combat import DamageInstance, SelfHologramDamageCalculationStrategy


class TestMitylSkills:
    def test_assault_shot(self):
        assault_shot: DamageInstance = AssaultShot().execute()

        assert assault_shot.base_potency == 80
        assert DamageTag.ACTIVE in assault_shot.tags
        assert DamageTag.BASIC in assault_shot.tags
        assert DamageTag.LIGHT_AMMO in assault_shot.tags
        assert DamageTag.TARGETED in assault_shot.tags
        assert DamageTag.PHYSICAL in assault_shot.tags
        assert assault_shot.group_name == "Assault Shot"

    def test_air_dash_without_skill_reuse(self):
        ad: DamageInstance = AirDash().execute(is_skill_reuse=False)

        assert ad.base_potency == 130
        assert DamageTag.ACTIVE in ad.tags
        assert DamageTag.LIGHT_AMMO in ad.tags
        assert DamageTag.TARGETED in ad.tags
        assert DamageTag.HYDRO in ad.tags
        assert DamageTag.PHASE in ad.tags
        assert DamageTag.CONFECTANCE in ad.tags
        assert ad.buffs_before == []
        assert ad.group_name == "Air Dash"

    def test_air_dash_skill_reuse_grants_bonus(self):
        ad: DamageInstance = AirDash().execute(is_skill_reuse=True)

        assert ad.buffs_before == [
            Buff(
                30, ModifierType.ADDITIVE, SpecialAttribute.DAMAGE_BOOST, DamageTag.ALL
            )
        ]

    def test_air_dash_v4_without_skill_reuse(self):
        ad: DamageInstance = AirDashV4().execute(is_skill_reuse=False)

        assert ad.base_potency == 160
        assert ad.buffs_before == []

    def test_air_dash_v4_skill_reuse_grants_bonus(self):
        ad: DamageInstance = AirDashV4().execute(is_skill_reuse=True)

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
        assert sa.group_name == "Support Action (Self Hologram)"
        assert isinstance(
            sa.damage_calculation_strategy, SelfHologramDamageCalculationStrategy
        )

    def test_support_action_v5(self):
        sa: DamageInstance = SupportActionV5().execute()

        assert sa.base_potency == 60
        assert sa.group_name == "Support Action (Self Hologram)"
        assert isinstance(
            sa.damage_calculation_strategy, SelfHologramDamageCalculationStrategy
        )

    def test_aligned_resonance(self):
        cr: DamageInstance = AlignedResonance().execute()

        assert cr.base_potency == 40
        assert DamageTag.HYDRO in cr.tags
        assert DamageTag.PHASE in cr.tags
        assert DamageTag.PHYSICAL_SUMMON in cr.tags
        assert DamageTag.TARGETED in cr.tags
        assert DamageTag.PASSIVE in cr.tags
        assert cr.group_name == "Aligned Resonance (Self Hologram)"
        assert isinstance(
            cr.damage_calculation_strategy, SelfHologramDamageCalculationStrategy
        )

    def test_aligned_resonance_v1(self):
        cr: DamageInstance = AlignedResonanceV1().execute()

        assert cr.base_potency == 60
        assert cr.group_name == "Aligned Resonance (Self Hologram)"

    def test_hologram_assault(self):
        hs: DamageInstance = HologramAssault().execute()

        assert hs.base_potency == 100
        assert DamageTag.HYDRO in hs.tags
        assert DamageTag.PHASE in hs.tags
        assert DamageTag.PHYSICAL_SUMMON in hs.tags
        assert DamageTag.TARGETED in hs.tags
        assert DamageTag.BASIC in hs.tags
        assert hs.group_name == "Hologram Assault (Self Hologram)"
        assert isinstance(
            hs.damage_calculation_strategy, SelfHologramDamageCalculationStrategy
        )

    def test_hologram_assault_v2(self):
        hs: DamageInstance = HologramAssaultV2().execute()

        assert hs.base_potency == 120
        assert hs.group_name == "Hologram Assault (Self Hologram)"


class TestMitylSummon:
    def test_get_summoned_unit_auto_summons_self_hologram(self):
        mityl: Mityl = Mityl()

        summon = mityl.get_summoned_unit("Self Hologram")

        assert summon is not None
        assert summon.name == "Self Hologram"
        assert len(mityl.summoned_units) == 1

    def test_summon_self_hologram_is_idempotent(self):
        mityl: Mityl = Mityl()

        mityl.summon_self_hologram()
        mityl.summon_self_hologram()

        assert len(mityl.summoned_units) == 1

    def test_refresh_self_hologram_syncs_stats(self):
        """refresh_self_hologram should snapshot Mityl's current stats."""
        mityl: Mityl = Mityl()
        mityl.set_to_v0()
        mityl.initial_stats.basic_attributes[StatType.ATTACK] = 5000
        mityl.initial_stats.basic_attributes[StatType.HEALTH] = 3000

        mityl.refresh_self_hologram()

        self_hologram = next(u for u in mityl.summoned_units if u.name == "Self Hologram")
        assert self_hologram.initial_stats.basic_attributes[StatType.ATTACK] == 5000
        assert self_hologram.initial_stats.basic_attributes[StatType.HEALTH] == 3000

    def test_refresh_self_hologram_replaces_stale_summon(self):
        """Calling refresh_self_hologram twice leaves exactly one summon."""
        mityl: Mityl = Mityl()
        mityl.set_to_v0()
        mityl.initial_stats.basic_attributes[StatType.ATTACK] = 1111

        mityl.refresh_self_hologram()
        mityl.initial_stats.basic_attributes[StatType.ATTACK] = 2222
        mityl.refresh_self_hologram()

        assert len(mityl.summoned_units) == 1
        self_hologram = next(u for u in mityl.summoned_units if u.name == "Self Hologram")
        assert self_hologram.initial_stats.basic_attributes[StatType.ATTACK] == 2222

    def test_prepare_for_calculation_refreshes_self_hologram(self):
        """prepare_for_calculation should act as refresh_self_hologram."""
        mityl: Mityl = Mityl()
        mityl.set_to_v0()
        mityl.initial_stats.basic_attributes[StatType.ATTACK] = 4000

        mityl.prepare_for_calculation()

        assert len(mityl.summoned_units) == 1
        self_hologram = next(u for u in mityl.summoned_units if u.name == "Self Hologram")
        assert self_hologram.initial_stats.basic_attributes[StatType.ATTACK] == 4000


class TestMitylFortification:
    def test_set_to_v0(self):
        mityl: Mityl = Mityl()
        mityl.set_to_v0()

        assert isinstance(mityl.assault_shot, AssaultShot)
        assert isinstance(mityl.air_dash, AirDash)
        assert isinstance(mityl.support_action, SupportAction)
        assert isinstance(mityl.aligned_resonance, AlignedResonance)
        assert isinstance(mityl.hologram_assault, HologramAssault)
        assert mityl.get_summoned_unit("Self Hologram") is not None

    def test_set_to_v1(self):
        mityl: Mityl = Mityl()
        mityl.set_to_v1()

        assert isinstance(mityl.aligned_resonance, AlignedResonanceV1)

    def test_set_to_v2(self):
        mityl: Mityl = Mityl()
        mityl.set_to_v2()

        assert isinstance(mityl.hologram_assault, HologramAssaultV2)
        assert isinstance(mityl.aligned_resonance, AlignedResonanceV1)

    def test_set_to_v4(self):
        mityl: Mityl = Mityl()
        mityl.set_to_v4()

        assert isinstance(mityl.air_dash, AirDashV4)
        assert isinstance(mityl.hologram_assault, HologramAssaultV2)

    def test_set_to_v5(self):
        mityl: Mityl = Mityl()
        mityl.set_to_v5()

        assert isinstance(mityl.support_action, SupportActionV5)
        assert isinstance(mityl.air_dash, AirDashV4)

    def test_set_fortification_level_segment03_matches_v2(self):
        mityl: Mityl = Mityl()
        mityl.set_fortification_level(FortificationLevel.SEGMENT03)

        assert isinstance(mityl.hologram_assault, HologramAssaultV2)
        assert isinstance(mityl.air_dash, AirDash)

    def test_set_fortification_level_segment06_matches_v5(self):
        mityl: Mityl = Mityl()
        mityl.set_fortification_level(FortificationLevel.SEGMENT06)

        assert isinstance(mityl.support_action, SupportActionV5)
        assert isinstance(mityl.air_dash, AirDashV4)

    def test_set_to_v0_after_v5_resets_upgraded_skills(self):
        mityl: Mityl = Mityl()
        mityl.set_to_v5()

        assert isinstance(mityl.support_action, SupportActionV5)

        mityl.set_to_v0()

        assert isinstance(mityl.support_action, SupportAction)
        assert isinstance(mityl.air_dash, AirDash)
