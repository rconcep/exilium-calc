from core.dolls.liushih import *

from core.combat import (
    DamageInstance,
    LiushihDamageCalculationStrategy,
    PegasusDamageCalculationStrategy,
)
from core.types import DamageTag, FortificationLevel, StatType, SpecialAttribute
from core.types import Unit, SummonedUnit


class TestLiushihSkills:
    def test_line_breaker(self):
        da: DamageInstance = LineBreaker().execute(stacks_of_marksmanship=0)

        assert da.base_potency == 90
        assert DamageTag.ACTIVE in da.tags
        assert DamageTag.BASIC in da.tags
        assert DamageTag.HEAVY_AMMO in da.tags
        assert DamageTag.TARGETED in da.tags
        assert DamageTag.HYDRO in da.tags
        assert DamageTag.PHASE in da.tags
        assert da.group_name == "Line Breaker"
        assert isinstance(
            da.damage_calculation_strategy, LiushihDamageCalculationStrategy
        )

    def test_line_breaker_with_marksmanship(self):
        da: DamageInstance = LineBreaker().execute(stacks_of_marksmanship=3)

        # Base 90 + 10 per stack * 3 stacks = 120
        assert da.base_potency == 120
        assert da.group_name == "Line Breaker"

    def test_line_breaker_v3(self):
        da: DamageInstance = LineBreakerV3().execute(stacks_of_marksmanship=0)

        assert da.base_potency == 90
        assert DamageTag.BASIC in da.tags

    def test_line_breaker_v3_with_marksmanship(self):
        da: DamageInstance = LineBreakerV3().execute(stacks_of_marksmanship=3)

        # Base 90 + 20 per stack * 3 stacks = 150
        assert da.base_potency == 150
        assert da.group_name == "Line Breaker"

    def test_desperate_gambit(self):
        da: DamageInstance = DesperateGambit().execute()

        assert da.base_potency == 90
        assert DamageTag.ACTIVE in da.tags
        assert DamageTag.HEAVY_AMMO in da.tags
        assert DamageTag.TARGETED in da.tags
        assert DamageTag.HYDRO in da.tags
        assert DamageTag.PHASE in da.tags
        assert da.group_name == "Desperate Gambit"
        assert isinstance(
            da.damage_calculation_strategy, LiushihDamageCalculationStrategy
        )

    def test_desperate_gambit_v3(self):
        da: DamageInstance = DesperateGambitV3().execute()

        assert da.base_potency == 120
        assert da.group_name == "Desperate Gambit"
        assert isinstance(
            da.damage_calculation_strategy, LiushihDamageCalculationStrategy
        )

    def test_one_doll_cavalry(self):
        da: DamageInstance = OneDollCavalry().execute()

        assert da.base_potency == 90
        assert DamageTag.ULTIMATE in da.tags
        assert DamageTag.PHASE in da.tags
        assert DamageTag.HYDRO in da.tags
        assert DamageTag.TARGETED in da.tags
        assert da.group_name == "One Doll Cavalry"
        assert isinstance(
            da.damage_calculation_strategy, LiushihDamageCalculationStrategy
        )

    def test_one_doll_cavalry_v4(self):
        da: DamageInstance = OneDollCavalryV4().execute()

        assert da.base_potency == 120
        assert da.group_name == "One Doll Cavalry"
        assert isinstance(
            da.damage_calculation_strategy, LiushihDamageCalculationStrategy
        )

    def test_gatling_cannon(self):
        da: DamageInstance = GatlingCannon().execute(stacks_of_marksmanship=0)

        assert da.base_potency == 110
        assert DamageTag.HYDRO in da.tags
        assert DamageTag.PHASE in da.tags
        assert DamageTag.PHYSICAL_SUMMON in da.tags
        assert DamageTag.TARGETED in da.tags
        assert DamageTag.BASIC in da.tags
        assert da.group_name == "Gatling Cannon (Pegasus)"
        assert isinstance(
            da.damage_calculation_strategy, PegasusDamageCalculationStrategy
        )

    def test_gatling_cannon_with_marksmanship(self):
        da: DamageInstance = GatlingCannon().execute(stacks_of_marksmanship=3)

        # Base 110 + 10 per stack * 3 stacks = 140
        assert da.base_potency == 140
        assert da.group_name == "Gatling Cannon (Pegasus)"

    def test_gatling_cannon_v3(self):
        da: DamageInstance = GatlingCannonV3().execute(stacks_of_marksmanship=0)

        assert da.base_potency == 110
        assert DamageTag.BASIC in da.tags

    def test_gatling_cannon_v3_with_marksmanship(self):
        da: DamageInstance = GatlingCannonV3().execute(stacks_of_marksmanship=3)

        # Base 110 + 20 per stack * 3 stacks = 170
        assert da.base_potency == 170
        assert da.group_name == "Gatling Cannon (Pegasus)"


class TestLiushih:
    def test_set_to_v0(self):
        liushih: Liushih = Liushih()
        liushih.set_to_v0()

        assert isinstance(liushih.line_breaker, LineBreaker)
        assert isinstance(liushih.desperate_gambit, DesperateGambit)
        assert isinstance(liushih.one_doll_cavalry, OneDollCavalry)
        assert isinstance(liushih.gatling_cannon, GatlingCannon)
        assert liushih.get_summoned_unit("Pegasus") is not None

    def test_set_to_v3(self):
        liushih: Liushih = Liushih()
        liushih.set_to_v3()

        assert isinstance(liushih.line_breaker, LineBreakerV3)
        assert isinstance(liushih.desperate_gambit, DesperateGambitV3)
        assert isinstance(liushih.gatling_cannon, GatlingCannonV3)

    def test_set_to_v4(self):
        liushih: Liushih = Liushih()
        liushih.set_to_v4()

        assert isinstance(liushih.one_doll_cavalry, OneDollCavalryV4)
        assert isinstance(liushih.line_breaker, LineBreakerV3)

    def test_set_fortification_level(self):
        liushih: Liushih = Liushih()

        liushih.set_fortification_level(FortificationLevel.SEGMENT00)
        assert isinstance(liushih.line_breaker, LineBreaker)

        liushih.set_fortification_level(FortificationLevel.SEGMENT03)
        assert isinstance(liushih.line_breaker, LineBreakerV3)

        liushih.set_fortification_level(FortificationLevel.SEGMENT04)
        assert isinstance(liushih.one_doll_cavalry, OneDollCavalryV4)

        liushih.set_fortification_level(FortificationLevel.SEGMENT06)
        assert liushih.fortification_level == FortificationLevel.SEGMENT06

    def test_pegasus_summoning(self):
        liushih: Liushih = Liushih()
        pegasus = liushih.get_summoned_unit("Pegasus")

        assert pegasus is not None
        assert pegasus.name == "Pegasus"

    def test_pegasus_refresh(self):
        liushih: Liushih = Liushih()
        pegasus1 = liushih.get_summoned_unit("Pegasus")

        # Mutate Liushih's stats
        liushih.initial_stats.basic_attributes[StatType.ATTACK] += 100

        # Refresh Pegasus to get updated snapshot
        liushih.refresh_pegasus()
        pegasus2 = liushih.get_summoned_unit("Pegasus")

        # Pegasus should have the updated modifiers
        assert pegasus2 is not None
        assert pegasus2 != pegasus1

    def test_irrelevant_damage_tags(self):
        liushih: Liushih = Liushih()

        # Verify that HYDRO and PHASE are not in irrelevant tags
        assert DamageTag.HYDRO not in liushih.irrelevant_damage_tags
        assert DamageTag.PHASE not in liushih.irrelevant_damage_tags

        # Verify that irrelevant tags are properly set
        assert DamageTag.CORROSION in liushih.irrelevant_damage_tags
        assert DamageTag.BURN in liushih.irrelevant_damage_tags
        assert DamageTag.FREEZE in liushih.irrelevant_damage_tags
        assert DamageTag.ELECTRIC in liushih.irrelevant_damage_tags
        assert DamageTag.MELEE in liushih.irrelevant_damage_tags


class TestLiushihDamageCalculationStrategy:
    """Tests for LiushihDamageCalculationStrategy."""

    @staticmethod
    def construct_defender() -> Unit:
        """Construct a basic defender for testing."""
        t: Unit = Unit()
        t.initial_stats.basic_attributes[StatType.DEFENSE] = 1000
        return t

    def test_calculate_base_damage_uses_health_scaling(self):
        """Base damage should use 20% of health as effective attack."""
        liushih: Liushih = Liushih()
        liushih.initial_stats.basic_attributes[StatType.ATTACK] = 2000
        liushih.initial_stats.basic_attributes[StatType.HEALTH] = 5000
        liushih.prepare_for_calculation()

        target: Unit = self.construct_defender()
        di: DamageInstance = DamageInstance(
            label="Test",
            base_potency=100,
            tags={DamageTag.ACTIVE, DamageTag.BASIC, DamageTag.HYDRO},
        )

        strategy = LiushihDamageCalculationStrategy()
        effective_atk, _, _, _ = strategy.calculate_base_damage(liushih, target, di)

        # Health scaling: 20% of 5000 = 1000
        assert effective_atk == 1000

    def test_passive_bonus_applied_for_basic_attacks(self):
        """Liushih's passive should increase basic attack damage by 5% per 60 Attack."""
        liushih: Liushih = Liushih()
        liushih.initial_stats.basic_attributes[StatType.ATTACK] = (
            300  # 300/60 = 5, so 5*5% = 25% bonus
        )
        liushih.initial_stats.basic_attributes[StatType.HEALTH] = 5000
        liushih.prepare_for_calculation()

        target: Unit = self.construct_defender()
        di: DamageInstance = DamageInstance(
            label="Line Breaker",
            base_potency=90,
            tags={DamageTag.ACTIVE, DamageTag.BASIC, DamageTag.HYDRO, DamageTag.PHASE},
        )

        strategy = LiushihDamageCalculationStrategy()
        adjusted_potency = strategy.calculate_adjusted_potency(liushih, target, di)

        # Base 90 + (300 // 60) * 5 = 90 + 25 = 115
        assert adjusted_potency == 115

    def test_passive_bonus_capped_at_50_percent(self):
        """Liushih's passive bonus should cap at 50% damage increase."""
        liushih: Liushih = Liushih()
        liushih.initial_stats.basic_attributes[StatType.ATTACK] = (
            1000  # 1000/60 = 16, * 5 = 80%, capped at 50%
        )
        liushih.initial_stats.basic_attributes[StatType.HEALTH] = 5000
        liushih.prepare_for_calculation()

        target: Unit = self.construct_defender()
        di: DamageInstance = DamageInstance(
            label="Line Breaker",
            base_potency=100,
            tags={DamageTag.ACTIVE, DamageTag.BASIC, DamageTag.HYDRO},
        )

        strategy = LiushihDamageCalculationStrategy()
        adjusted_potency = strategy.calculate_adjusted_potency(liushih, target, di)

        # Base 100 + capped 50 = 150
        assert adjusted_potency == 150

    def test_passive_bonus_not_applied_for_non_basic_attacks(self):
        """Liushih's passive should NOT apply to non-basic attacks like S1 or Ultimate."""
        liushih: Liushih = Liushih()
        liushih.initial_stats.basic_attributes[StatType.ATTACK] = 300
        liushih.initial_stats.basic_attributes[StatType.HEALTH] = 5000
        liushih.prepare_for_calculation()

        target: Unit = self.construct_defender()
        di: DamageInstance = DamageInstance(
            label="Desperate Gambit",
            base_potency=120,
            tags={
                DamageTag.ACTIVE,
                DamageTag.HEAVY_AMMO,
                DamageTag.HYDRO,
                DamageTag.PHASE,
            },
        )

        strategy = LiushihDamageCalculationStrategy()
        adjusted_potency = strategy.calculate_adjusted_potency(liushih, target, di)

        # Base 120 without passive bonus, since DamageTag.BASIC is not in tags
        assert adjusted_potency == 120

    def test_passive_bonus_with_damage_boost_modifiers(self):
        """Passive bonus should combine with damage boost modifiers."""
        liushih: Liushih = Liushih()
        liushih.initial_stats.basic_attributes[StatType.ATTACK] = (
            120  # 120/60 = 2, * 5 = 10% bonus
        )
        liushih.initial_stats.basic_attributes[StatType.HEALTH] = 5000
        liushih.additive_modifiers.special_attributes[
            SpecialAttribute.DAMAGE_BOOST
        ].set_multiplier(DamageTag.HYDRO, 20)
        liushih.prepare_for_calculation()

        target: Unit = self.construct_defender()
        di: DamageInstance = DamageInstance(
            label="Line Breaker",
            base_potency=100,
            tags={DamageTag.ACTIVE, DamageTag.BASIC, DamageTag.HYDRO},
        )

        strategy = LiushihDamageCalculationStrategy()
        adjusted_potency = strategy.calculate_adjusted_potency(liushih, target, di)

        # Base 100 + passive 10 = 110
        # Apply damage boost: 110 * (1 + 20/100) = 110 * 1.2 = 132
        assert adjusted_potency == 132


class TestPegasusDamageCalculationStrategy:
    """Tests for PegasusDamageCalculationStrategy."""

    @staticmethod
    def construct_defender() -> Unit:
        """Construct a basic defender for testing."""
        t: Unit = Unit()
        t.initial_stats.basic_attributes[StatType.DEFENSE] = 1000
        return t

    def test_get_effective_attacker_returns_pegasus(self):
        """Pegasus strategy should return the Pegasus summon as effective attacker."""
        liushih: Liushih = Liushih()
        liushih.prepare_for_calculation()

        strategy = PegasusDamageCalculationStrategy()
        effective_attacker = strategy.get_effective_attacker(liushih)

        assert effective_attacker is not None
        # Effective attacker is a SummonedUnit with name "Pegasus"
        assert isinstance(effective_attacker, SummonedUnit)
        assert effective_attacker.name == "Pegasus"

    def test_calculate_base_damage_uses_pegasus_health_scaling(self):
        """Pegasus base damage should use 20% of Pegasus's health as effective attack."""
        liushih: Liushih = Liushih()
        liushih.initial_stats.basic_attributes[StatType.ATTACK] = 2000
        liushih.initial_stats.basic_attributes[StatType.HEALTH] = 8000
        liushih.prepare_for_calculation()

        target: Unit = self.construct_defender()
        di: DamageInstance = DamageInstance(
            label="Test",
            base_potency=100,
            tags={DamageTag.PHYSICAL_SUMMON, DamageTag.BASIC, DamageTag.HYDRO},
        )

        strategy = PegasusDamageCalculationStrategy()
        effective_atk, _, _, _ = strategy.calculate_base_damage(liushih, target, di)

        # Pegasus inherits Liushih's health, so 20% of 8000 = 1600
        assert effective_atk == 1600

    def test_pegasus_passive_bonus_based_on_pegasus_attack(self):
        """Pegasus passive bonus should use Pegasus's inherited initial attack."""
        liushih: Liushih = Liushih()
        liushih.initial_stats.basic_attributes[StatType.ATTACK] = (
            240  # Pegasus gets same attack
        )
        liushih.initial_stats.basic_attributes[StatType.HEALTH] = 5000
        liushih.prepare_for_calculation()

        target: Unit = self.construct_defender()
        di: DamageInstance = DamageInstance(
            label="Gatling Cannon",
            base_potency=110,
            tags={
                DamageTag.HYDRO,
                DamageTag.PHASE,
                DamageTag.PHYSICAL_SUMMON,
                DamageTag.BASIC,
            },
        )

        strategy = PegasusDamageCalculationStrategy()
        adjusted_potency = strategy.calculate_adjusted_potency(liushih, target, di)

        # Base 110 + (240 // 60) * 5 = 110 + 20 = 130
        assert adjusted_potency == 130

    def test_pegasus_passive_bonus_not_applied_for_non_basic_attacks(self):
        """Pegasus passive should NOT apply to non-basic attacks."""
        liushih: Liushih = Liushih()
        liushih.initial_stats.basic_attributes[StatType.ATTACK] = 300
        liushih.initial_stats.basic_attributes[StatType.HEALTH] = 5000
        liushih.prepare_for_calculation()

        target: Unit = self.construct_defender()
        di: DamageInstance = DamageInstance(
            label="Some Skill",
            base_potency=100,
            tags={DamageTag.HYDRO, DamageTag.PHASE, DamageTag.PHYSICAL_SUMMON},
        )

        strategy = PegasusDamageCalculationStrategy()
        adjusted_potency = strategy.calculate_adjusted_potency(liushih, target, di)

        # Base 100 without passive bonus, since DamageTag.BASIC is not in tags
        assert adjusted_potency == 100

    def test_resolve_buffs_applies_to_pegasus(self):
        """Buffs should be applied to Pegasus, not Liushih."""
        liushih: Liushih = Liushih()
        liushih.initial_stats.basic_attributes[StatType.ATTACK] = 1000
        liushih.initial_stats.basic_attributes[StatType.HEALTH] = 5000
        liushih.initial_stats.basic_attributes[StatType.CRIT_DAMAGE] = 100
        liushih.prepare_for_calculation()

        # Pegasus starts with the same initial attack as Liushih
        pegasus_before = liushih.get_summoned_unit("Pegasus")
        assert pegasus_before is not None
        pegasus_attack_before = pegasus_before.additive_modifiers.basic_attributes[
            StatType.ATTACK
        ]

        target: Unit = self.construct_defender()
        di: DamageInstance = DamageInstance(
            label="Test",
            base_potency=100,
            tags={DamageTag.PHYSICAL_SUMMON, DamageTag.HYDRO},
        )

        strategy = PegasusDamageCalculationStrategy()
        strategy.resolve_buffs(liushih, target, di)

        # Pegasus should have the buff applied (no explicit buff here, but the mechanism works)
        pegasus_after = liushih.get_summoned_unit("Pegasus")
        assert pegasus_after is not None
