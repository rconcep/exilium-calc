import pytest

from core.combat import *
from core.combat import _calculate_effective_and_negative_defense


class TestDamageInstance:
    """ """

    def test_default_constructor(self):
        """ """
        label: str = "Ultra Shot"
        base_potency: float = 188.0
        di: DamageInstance = DamageInstance(label=label, base_potency=base_potency)

        assert di.label == label
        assert di.base_potency == base_potency
        assert di.adjusted_potency == 0
        assert len(di.tags) == 0

    def test_tags(self):
        """ """
        label: str = "Ultra Shot"
        base_potency: float = 188.0
        tags: set[DamageTag] = {
            DamageTag.PASSIVE,
            DamageTag.SUPPORT_ACTION,
            DamageTag.TARGETED,
            DamageTag.FREEZE,
            DamageTag.PASSIVE,
        }
        di: DamageInstance = DamageInstance(
            label=label, base_potency=base_potency, tags=tags
        )

        assert DamageTag.PASSIVE in di.tags
        assert DamageTag.BURN not in di.tags


class TestSumDamageInstances:
    """ """

    @staticmethod
    def construct_sample_container() -> list[DamageInstance]:
        """ """
        damage_instances: list[DamageInstance] = [
            DamageInstance(
                label="Ultra Shot",
                base_potency=80.0,
                tags={DamageTag.TARGETED, DamageTag.FREEZE, DamageTag.ACTIVE},
                adjusted_potency=111.0,
            ),
            DamageInstance(
                label="Unity",
                base_potency=30.0,
                tags={
                    DamageTag.TARGETED,
                    DamageTag.FREEZE,
                    DamageTag.PASSIVE,
                    DamageTag.PASSIVE,
                },
                adjusted_potency=52.0,
            ),
            DamageInstance(
                label="Howling Cyclone",
                base_potency=474.0,
                tags={
                    DamageTag.AREA_OF_EFFECT,
                    DamageTag.FREEZE,
                    DamageTag.CONFECTANCE,
                    DamageTag.ULTIMATE,
                },
                adjusted_potency=556.0,
            ),
        ]

        return damage_instances

    def test_empty_containers(self):
        """ """
        combined_di: DamageInstance = sum_damage_instances([], DamageTag.CORROSION)
        assert combined_di.base_potency == 0
        assert combined_di.adjusted_potency == 0

    def test_nonempty_container(self):
        """ """
        damage_instances: list[DamageInstance] = (
            TestSumDamageInstances.construct_sample_container()
        )

        combined_di: DamageInstance = sum_damage_instances(
            damage_instances, DamageTag.CORROSION
        )
        assert combined_di.adjusted_potency == 0

        combined_di: DamageInstance = sum_damage_instances(
            damage_instances, DamageTag.FREEZE
        )
        assert combined_di.adjusted_potency == pytest.approx(556 + 52 + 111)

        combined_di: DamageInstance = sum_damage_instances(
            damage_instances, DamageTag.AREA_OF_EFFECT
        )
        assert combined_di.base_potency == pytest.approx(474)

    def test_do_exclude(self):
        """ """
        damage_instances: list[DamageInstance] = (
            TestSumDamageInstances.construct_sample_container()
        )

        combined_di: DamageInstance = sum_damage_instances(
            damage_instances, DamageTag.AREA_OF_EFFECT, do_exclude=True
        )
        assert combined_di.adjusted_potency == pytest.approx(52 + 111)


class TestDamageCalculationStrategy:

    @staticmethod
    def construct_attacker() -> Unit:
        g: Unit = Unit()
        g.initial_stats.basic_attributes[StatType.ATTACK] = 5429
        g.initial_stats.basic_attributes[StatType.CRIT_DAMAGE] = 156.9

        mult: IncreasedDamageMultipliers = IncreasedDamageMultipliers()
        mult.set_multiplier(DamageTag.FREEZE, 21.4)
        mult.set_multiplier(DamageTag.ULTIMATE, 10.4)
        mult.set_multiplier(DamageTag.AREA_OF_EFFECT, 30)

        g.initial_stats.special_attributes[SpecialAttribute.DAMAGE_BOOST] = mult

        return g

    @staticmethod
    def construct_defender() -> Unit:
        t: Unit = Unit()
        t.initial_stats.basic_attributes[StatType.DEFENSE] = 5000
        t.initial_stats.basic_attributes[StatType.STABILITY_DAMAGE_REDUCTION] = 60

        return t

    @staticmethod
    def construct_doll_attacker(level: FortificationLevel) -> Doll:
        class DummyDoll(Doll):
            def set_fortification_level(self, level: FortificationLevel) -> None:
                self.fortification_level = level

        d: Doll = DummyDoll()
        d.initial_stats.basic_attributes[StatType.ATTACK] = 5429
        d.initial_stats.basic_attributes[StatType.CRIT_DAMAGE] = 156.9
        d.set_fortification_level(level)

        return d

    @staticmethod
    def construct_doll_with_simulacrum(
        level: FortificationLevel,
        doll_attack: float = 1000,
        doll_health: float = 3000,
        summon_attack: float = 5000,
        summon_health: float = 2400,
    ) -> Doll:
        class DummyDoll(Doll):
            def set_fortification_level(self, level: FortificationLevel) -> None:
                self.fortification_level = level

        d: Doll = DummyDoll()
        d.initial_stats.basic_attributes[StatType.ATTACK] = doll_attack
        d.initial_stats.basic_attributes[StatType.HEALTH] = doll_health
        d.initial_stats.basic_attributes[StatType.CRIT_DAMAGE] = 100
        d.set_fortification_level(level)

        summon = PhysicalSummonedUnit(name="Simulacrum")
        summon.initial_stats.basic_attributes[StatType.ATTACK] = summon_attack
        summon.initial_stats.basic_attributes[StatType.HEALTH] = summon_health
        summon.initial_stats.basic_attributes[StatType.CRIT_DAMAGE] = 100

        d.summoned_units.append(summon)
        return d

    @staticmethod
    def construct_doll_with_named_summon(
        summon_name: str,
        level: FortificationLevel = FortificationLevel.SEGMENT00,
        doll_attack: float = 1000,
        summon_attack: float = 5000,
    ) -> Doll:
        class DummyDoll(Doll):
            def set_fortification_level(self, level: FortificationLevel) -> None:
                self.fortification_level = level

        d: Doll = DummyDoll()
        d.initial_stats.basic_attributes[StatType.ATTACK] = doll_attack
        d.set_fortification_level(level)

        summon = SummonedUnit(name=summon_name)
        summon.initial_stats.basic_attributes[StatType.ATTACK] = summon_attack
        d.summoned_units.append(summon)

        return d

    def test_resolve_buffs(self):
        g = TestDamageCalculationStrategy.construct_attacker()
        t = TestDamageCalculationStrategy.construct_defender()

        label: str = "Howling Cyclone"
        base_potency: float = 150.0
        tags: set[DamageTag] = {
            DamageTag.ACTIVE,
            DamageTag.AREA_OF_EFFECT,
            DamageTag.FREEZE,
            DamageTag.CONFECTANCE,
            DamageTag.ULTIMATE,
        }

        di: DamageInstance = DamageInstance(
            label=label, base_potency=base_potency, tags=tags
        )

        buff: Buff = Buff(
            value=10,
            modifier_type=ModifierType.MULTIPLICATIVE,
            stat_type=StatType.ATTACK,
        )
        debuff: Debuff = Debuff(
            value=-30,
            modifier_type=ModifierType.MULTIPLICATIVE,
            stat_type=StatType.DEFENSE,
        )

        StandardDamageCalculationStrategy().resolve_buffs(
            g,
            t,
            di,
            buffs_before=[
                buff,
            ],
            debuffs_before=[
                debuff,
            ],
        )

        assert g.multiplicative_modifiers.basic_attributes[StatType.ATTACK] == 10
        assert t.multiplicative_modifiers.basic_attributes[StatType.DEFENSE] == -30

    def test_standard_base_damage(self):
        g = TestDamageCalculationStrategy.construct_attacker()
        t = TestDamageCalculationStrategy.construct_defender()

        label: str = "Howling Cyclone"
        base_potency: float = 150.0
        tags: set[DamageTag] = {
            DamageTag.ACTIVE,
            DamageTag.AREA_OF_EFFECT,
            DamageTag.FREEZE,
            DamageTag.CONFECTANCE,
            DamageTag.ULTIMATE,
        }

        di: DamageInstance = DamageInstance(
            label=label, base_potency=base_potency, tags=tags
        )

        buff: Buff = Buff(
            value=10,
            modifier_type=ModifierType.MULTIPLICATIVE,
            stat_type=StatType.ATTACK,
        )
        debuff: Debuff = Debuff(
            value=-30,
            modifier_type=ModifierType.MULTIPLICATIVE,
            stat_type=StatType.DEFENSE,
        )

        StandardDamageCalculationStrategy().resolve_buffs(
            g,
            t,
            di,
            buffs_before=[
                buff,
            ],
            debuffs_before=[
                debuff,
            ],
        )

        _, _, _, term = StandardDamageCalculationStrategy().calculate_base_damage(
            g, t, di
        )

        assert term == pytest.approx(3765.199)

    def test_standard_base_damage_uses_conditional_attack_modifiers(self):
        g = TestDamageCalculationStrategy.construct_attacker()
        t = TestDamageCalculationStrategy.construct_defender()
        g.initial_stats.conditional_basic_attributes[StatType.ATTACK].set_multiplier(
            DamageTag.FREEZE, 200
        )

        freeze_di = DamageInstance(
            label="",
            base_potency=100,
            tags={DamageTag.PHYSICAL, DamageTag.FREEZE},
        )
        burn_di = DamageInstance(
            label="",
            base_potency=100,
            tags={DamageTag.PHYSICAL, DamageTag.BURN},
        )

        freeze_atk, _, _, _ = StandardDamageCalculationStrategy().calculate_base_damage(
            g, t, freeze_di
        )
        burn_atk, _, _, _ = StandardDamageCalculationStrategy().calculate_base_damage(
            g, t, burn_di
        )

        assert freeze_atk == pytest.approx(burn_atk + 200)

    def test_resolve_buffs_supports_tagged_basic_stat_buffs(self):
        g = TestDamageCalculationStrategy.construct_attacker()
        t = TestDamageCalculationStrategy.construct_defender()
        di = DamageInstance(label="", base_potency=100, tags={DamageTag.FREEZE})

        buff = Buff(
            value=12,
            modifier_type=ModifierType.MULTIPLICATIVE,
            stat_type=StatType.ATTACK,
            tag=DamageTag.FREEZE,
        )

        StandardDamageCalculationStrategy().resolve_buffs(
            g,
            t,
            di,
            buffs_before=[buff],
        )

        assert g.multiplicative_modifiers.basic_attributes[StatType.ATTACK] == 0
        assert g.multiplicative_modifiers.conditional_basic_attributes[
            StatType.ATTACK
        ].get_multiplier(DamageTag.FREEZE) == pytest.approx(12)

    def test_calculate_damage_uses_conditional_crit_rate(self):
        g = TestDamageCalculationStrategy.construct_attacker()
        t = TestDamageCalculationStrategy.construct_defender()

        g.initial_stats.basic_attributes[StatType.CRIT_RATE] = 0
        g.initial_stats.basic_attributes[StatType.CRIT_DAMAGE] = 200
        g.initial_stats.conditional_basic_attributes[StatType.CRIT_RATE].set_multiplier(
            DamageTag.HAS_MOVEMENT_DEBUFF, 100
        )

        di = DamageInstance(
            label="",
            base_potency=100,
            tags={DamageTag.PHYSICAL},
        )

        summary = StandardDamageCalculationStrategy().calculate_damage(
            attacker=g,
            target=t,
            damage_instance=di,
        )

        assert summary.critical_rate == pytest.approx(1.0)
        assert summary.expected_damage == pytest.approx(summary.critical_damage)

    def test_resolve_defense_shredding(self):
        di: DamageInstance = DamageInstance(
            label="", base_potency=100, tags={DamageTag.FREEZE}
        )
        negative_def: float = 25
        assert resolve_reversed_assault(di, negative_def) == pytest.approx(0)

        di.tags = {DamageTag.PHYSICAL}
        assert resolve_reversed_assault(di, negative_def) == pytest.approx(25 * 0.5)

        negative_def: float = -25
        assert resolve_reversed_assault(di, negative_def) == pytest.approx(0)

        negative_def: float = 125
        assert resolve_reversed_assault(di, negative_def) == pytest.approx(125 * 0.75)

        negative_def: float = 255
        assert resolve_reversed_assault(di, negative_def) == pytest.approx(255 * 1)

        negative_def: float = 302
        assert resolve_reversed_assault(di, negative_def) == pytest.approx(302 * 1.5)

    def test_buffs_before(self):
        g = TestDamageCalculationStrategy.construct_attacker()
        t = TestDamageCalculationStrategy.construct_defender()

        label: str = "Howling Cyclone"
        base_potency: float = 150.0
        tags: set[DamageTag] = {
            DamageTag.ACTIVE,
            DamageTag.AREA_OF_EFFECT,
            DamageTag.FREEZE,
            DamageTag.CONFECTANCE,
            DamageTag.ULTIMATE,
        }

        # buff: increase attack by 10%
        buff: Buff = Buff(
            value=10,
            modifier_type=ModifierType.MULTIPLICATIVE,
            stat_type=StatType.ATTACK,
        )

        di: DamageInstance = DamageInstance(
            label=label,
            base_potency=base_potency,
            tags=tags,
            buffs_before=[
                buff,
            ],
        )

        assert StandardDamageCalculationStrategy().calculate_damage(
            attacker=g,
            target=t,
            damage_instance=di,
            is_stability_broken=True,
            phase_weaknesses_exploited=0,
        ).non_critical_damage == pytest.approx(7888.837)

    def test_debuffs_before(self):
        g = TestDamageCalculationStrategy.construct_attacker()
        t = TestDamageCalculationStrategy.construct_defender()

        label: str = "Howling Cyclone"
        base_potency: float = 150.0
        tags: set[DamageTag] = {
            DamageTag.ACTIVE,
            DamageTag.AREA_OF_EFFECT,
            DamageTag.FREEZE,
            DamageTag.CONFECTANCE,
            DamageTag.ULTIMATE,
        }

        # debuff: lower def by 30%
        debuff: Debuff = Debuff(
            value=-30,
            modifier_type=ModifierType.MULTIPLICATIVE,
            stat_type=StatType.DEFENSE,
        )

        di: DamageInstance = DamageInstance(
            label=label,
            base_potency=base_potency,
            tags=tags,
            debuffs_before=[
                debuff,
            ],
        )

        assert StandardDamageCalculationStrategy().calculate_damage(
            attacker=g,
            target=t,
            damage_instance=di,
            is_stability_broken=True,
            phase_weaknesses_exploited=0,
        ).non_critical_damage == pytest.approx(8011.367)

    def test_ignore_defense(self):
        g = TestDamageCalculationStrategy.construct_attacker()
        t = TestDamageCalculationStrategy.construct_defender()

        label: str = "Howling Cyclone"
        base_potency: float = 150.0
        tags: set[DamageTag] = {
            DamageTag.ACTIVE,
            DamageTag.AREA_OF_EFFECT,
            DamageTag.FREEZE,
            DamageTag.CONFECTANCE,
            DamageTag.ULTIMATE,
        }
        di: DamageInstance = DamageInstance(
            label=label, base_potency=base_potency, tags=tags
        )

        # get relevant parameters
        g.initial_stats.special_attributes[
            SpecialAttribute.DEFENSE_IGNORE
        ].set_multiplier(DamageTag.LIGHT_AMMO, 50)
        assert g.initial_stats.special_attributes[
            SpecialAttribute.DEFENSE_IGNORE
        ].get_total_multiplier(tags) == pytest.approx(0)

        assert StandardDamageCalculationStrategy().calculate_damage(
            g, t, di, True, 0
        ).non_critical_damage == pytest.approx(6859.095)

        g.initial_stats.special_attributes[
            SpecialAttribute.DEFENSE_IGNORE
        ].set_multiplier(DamageTag.FREEZE, 50)
        assert g.initial_stats.special_attributes[
            SpecialAttribute.DEFENSE_IGNORE
        ].get_total_multiplier(tags) == pytest.approx(50)

        assert StandardDamageCalculationStrategy().calculate_damage(
            g, t, di, True, 0
        ).non_critical_damage == pytest.approx(9021.755)

        # 100% ignore
        g.initial_stats.special_attributes[
            SpecialAttribute.DEFENSE_IGNORE
        ].set_multiplier(DamageTag.FREEZE, 100)
        assert g.initial_stats.special_attributes[
            SpecialAttribute.DEFENSE_IGNORE
        ].get_total_multiplier(tags) == pytest.approx(100)

        assert StandardDamageCalculationStrategy().calculate_damage(
            g, t, di, True, 0
        ).non_critical_damage == pytest.approx(13176.183)

        # >100% ignore
        g.initial_stats.special_attributes[
            SpecialAttribute.DEFENSE_IGNORE
        ].set_multiplier(DamageTag.FREEZE, 120)
        assert (
            g.initial_stats.special_attributes[
                SpecialAttribute.DEFENSE_IGNORE
            ].get_total_multiplier(tags)
            > 100
        )

        assert StandardDamageCalculationStrategy().calculate_damage(
            g, t, di, True, 0
        ).non_critical_damage == pytest.approx(13176.183)

    def test_resolve_increased_damage_taken(self):
        g = TestDamageCalculationStrategy.construct_attacker()
        t = TestDamageCalculationStrategy.construct_defender()
        di = DamageInstance(label="", base_potency=80, tags={DamageTag.PHYSICAL})
        di.tags.add(DamageTag.ALL)

        t.initial_stats.special_attributes[
            SpecialAttribute.INCREASE_DAMAGE_TAKEN
        ].set_multiplier(DamageTag.PHYSICAL, 30)
        t.initial_stats.special_attributes[
            SpecialAttribute.INCREASE_DAMAGE_TAKEN
        ].set_multiplier(DamageTag.BURN, 30)
        t.initial_stats.special_attributes[
            SpecialAttribute.INCREASE_DAMAGE_TAKEN
        ].set_multiplier(DamageTag.ALL, 20)

        assert (
            StandardDamageCalculationStrategy().resolve_increased_damage_taken(t, di)
            == 50
        )

    def test_stability_damage_reduction(self):
        g = TestDamageCalculationStrategy.construct_attacker()
        t = TestDamageCalculationStrategy.construct_defender()

        label: str = "Howling Cyclone"
        base_potency: float = 150.0
        tags: set[DamageTag] = {
            DamageTag.ACTIVE,
            DamageTag.AREA_OF_EFFECT,
            DamageTag.FREEZE,
            DamageTag.CONFECTANCE,
            DamageTag.ULTIMATE,
        }
        di: DamageInstance = DamageInstance(
            label=label, base_potency=base_potency, tags=tags
        )

        assert StandardDamageCalculationStrategy().calculate_damage(
            attacker=g,
            target=t,
            damage_instance=di,
            is_stability_broken=False,
            phase_weaknesses_exploited=0,
        ).non_critical_damage == pytest.approx(2743.637)

    def test_phase_weaknesses_exploited(self):
        g = TestDamageCalculationStrategy.construct_attacker()
        t = TestDamageCalculationStrategy.construct_defender()

        label: str = "Howling Cyclone"
        base_potency: float = 150.0
        tags: set[DamageTag] = {
            DamageTag.ACTIVE,
            DamageTag.AREA_OF_EFFECT,
            DamageTag.FREEZE,
            DamageTag.CONFECTANCE,
            DamageTag.ULTIMATE,
        }
        di: DamageInstance = DamageInstance(
            label=label, base_potency=base_potency, tags=tags
        )

        assert StandardDamageCalculationStrategy().calculate_damage(
            attacker=g,
            target=t,
            damage_instance=di,
            is_stability_broken=True,
            phase_weaknesses_exploited=1,
        ).non_critical_damage == pytest.approx(7545.004)
        assert StandardDamageCalculationStrategy().calculate_damage(
            attacker=g,
            target=t,
            damage_instance=di,
            is_stability_broken=True,
            phase_weaknesses_exploited=2,
        ).non_critical_damage == pytest.approx(8230.914)

    def test_lainie_resolve_buffs_adds_crit_rate_from_health(self):
        t = TestDamageCalculationStrategy.construct_defender()
        di = DamageInstance(label="", base_potency=100, tags={DamageTag.PHYSICAL})

        g_v0 = TestDamageCalculationStrategy.construct_doll_attacker(
            FortificationLevel.SEGMENT00
        )
        g_v3 = TestDamageCalculationStrategy.construct_doll_attacker(
            FortificationLevel.SEGMENT03
        )
        g_v0.initial_stats.basic_attributes[StatType.HEALTH] = 3000
        g_v3.initial_stats.basic_attributes[StatType.HEALTH] = 3000

        LainieDamageCalculationStrategy().resolve_buffs(g_v0, t, di)
        LainieDamageCalculationStrategy().resolve_buffs(g_v3, t, di)

        # V0 uses 12 health per 0.1 crit chance, capped at 30
        assert g_v0.additive_modifiers.basic_attributes[
            StatType.CRIT_RATE
        ] == pytest.approx(25)
        # V3 uses 6 health per 0.1 crit chance, capped at 60
        assert g_v3.additive_modifiers.basic_attributes[
            StatType.CRIT_RATE
        ] == pytest.approx(50)

    def test_simulacrum_base_damage_uses_simulacrum_attack(self):
        g = TestDamageCalculationStrategy.construct_doll_with_simulacrum(
            FortificationLevel.SEGMENT00,
            doll_attack=1000,
            summon_attack=5000,
        )
        t = TestDamageCalculationStrategy.construct_defender()
        di = DamageInstance(label="", base_potency=100, tags={DamageTag.PHYSICAL})

        effective_atk, _, _, _ = (
            SimulacrumDamageCalculationStrategy().calculate_base_damage(g, t, di)
        )

        assert effective_atk == pytest.approx(5000)

    def test_simulacrum_resolve_buffs_applies_passive_to_summon(self):
        g = TestDamageCalculationStrategy.construct_doll_with_simulacrum(
            FortificationLevel.SEGMENT03,
            summon_health=2400,
        )
        t = TestDamageCalculationStrategy.construct_defender()
        di = DamageInstance(label="", base_potency=100, tags={DamageTag.PHYSICAL})

        summon = g.get_summoned_unit("Simulacrum")
        assert isinstance(summon, PhysicalSummonedUnit)

        SimulacrumDamageCalculationStrategy().resolve_buffs(g, t, di)

        # 2400 / 6 * 0.1 = 40 at V3
        assert summon.additive_modifiers.basic_attributes[
            StatType.CRIT_RATE
        ] == pytest.approx(40)
        assert g.additive_modifiers.basic_attributes[
            StatType.CRIT_RATE
        ] == pytest.approx(0)

    def test_qiuhua_resolve_buffs_converts_crit_rate_overflow_at_v2(self):
        g = TestDamageCalculationStrategy.construct_doll_attacker(
            FortificationLevel.SEGMENT02
        )
        t = TestDamageCalculationStrategy.construct_defender()
        g.initial_stats.basic_attributes[StatType.CRIT_RATE] = 135
        di = DamageInstance(label="", base_potency=100, tags={DamageTag.BURN})

        QiuhuaDamageCalculationStrategy().resolve_buffs(g, t, di)

        assert g.additive_modifiers.special_attributes[
            SpecialAttribute.CRITICAL_DAMAGE
        ].get_multiplier(DamageTag.ALL) == pytest.approx(35)

    def test_qiuhua_resolve_buffs_no_overflow_at_v2(self):
        g = TestDamageCalculationStrategy.construct_doll_attacker(
            FortificationLevel.SEGMENT02
        )
        t = TestDamageCalculationStrategy.construct_defender()
        g.initial_stats.basic_attributes[StatType.CRIT_RATE] = 100
        di = DamageInstance(label="", base_potency=100, tags={DamageTag.BURN})

        QiuhuaDamageCalculationStrategy().resolve_buffs(g, t, di)

        assert g.additive_modifiers.special_attributes[
            SpecialAttribute.CRITICAL_DAMAGE
        ].get_multiplier(DamageTag.ALL) == pytest.approx(0)

    def test_qiuhua_resolve_buffs_adds_burn_attack_boost_at_v3(self):
        g = TestDamageCalculationStrategy.construct_doll_attacker(
            FortificationLevel.SEGMENT03
        )
        t = TestDamageCalculationStrategy.construct_defender()
        g.initial_stats.basic_attributes[StatType.CRIT_RATE] = 100
        di = DamageInstance(label="", base_potency=100, tags={DamageTag.BURN})

        QiuhuaDamageCalculationStrategy().resolve_buffs(g, t, di)

        assert g.multiplicative_modifiers.conditional_basic_attributes[
            StatType.ATTACK
        ].get_multiplier(DamageTag.BURN) == pytest.approx(30)

    def test_qiuhua_resolve_buffs_ignores_non_doll_attackers(self):
        g = Unit()
        t = TestDamageCalculationStrategy.construct_defender()
        g.initial_stats.basic_attributes[StatType.CRIT_RATE] = 135
        di = DamageInstance(label="", base_potency=100, tags={DamageTag.BURN})

        QiuhuaDamageCalculationStrategy().resolve_buffs(g, t, di)

        assert g.additive_modifiers.special_attributes[
            SpecialAttribute.CRITICAL_DAMAGE
        ].get_multiplier(DamageTag.ALL) == pytest.approx(0)
        assert g.multiplicative_modifiers.conditional_basic_attributes[
            StatType.ATTACK
        ].get_multiplier(DamageTag.BURN) == pytest.approx(0)

    def test_simulacrum_strategy_raises_when_summon_missing(self):
        g = TestDamageCalculationStrategy.construct_doll_attacker(
            FortificationLevel.SEGMENT00
        )
        t = TestDamageCalculationStrategy.construct_defender()
        di = DamageInstance(label="", base_potency=100, tags={DamageTag.PHYSICAL})

        with pytest.raises(ValueError, match="Simulacrum summon is required"):
            SimulacrumDamageCalculationStrategy().calculate_base_damage(g, t, di)

        with pytest.raises(ValueError, match="Simulacrum summon is required"):
            SimulacrumDamageCalculationStrategy().resolve_buffs(g, t, di)

        with pytest.raises(ValueError, match="Simulacrum summon is required"):
            SimulacrumDamageCalculationStrategy().get_bonus_damage(g, t, di)

    def test_kulich_base_damage_uses_kulich_attack(self):
        g = TestDamageCalculationStrategy.construct_doll_with_named_summon(
            summon_name="Kulich",
            doll_attack=1000,
            summon_attack=5000,
        )
        t = TestDamageCalculationStrategy.construct_defender()
        di = DamageInstance(label="", base_potency=100, tags={DamageTag.PHYSICAL})

        effective_atk, _, _, _ = (
            KulichDamageCalculationStrategy().calculate_base_damage(g, t, di)
        )

        assert effective_atk == pytest.approx(5000)

    def test_kulich_resolve_buffs_applies_to_kulich_summon(self):
        g = TestDamageCalculationStrategy.construct_doll_with_named_summon(
            summon_name="Kulich"
        )
        t = TestDamageCalculationStrategy.construct_defender()
        di = DamageInstance(label="", base_potency=100, tags={DamageTag.PHYSICAL})
        summon = g.get_summoned_unit("Kulich")
        assert isinstance(summon, SummonedUnit)

        buff = Buff(
            value=10,
            modifier_type=ModifierType.MULTIPLICATIVE,
            stat_type=StatType.ATTACK,
        )

        KulichDamageCalculationStrategy().resolve_buffs(g, t, di, buffs_before=[buff])

        assert summon.multiplicative_modifiers.basic_attributes[StatType.ATTACK] == 10
        assert g.multiplicative_modifiers.basic_attributes[StatType.ATTACK] == 0

    def test_kulich_strategy_raises_when_summon_missing(self):
        g = TestDamageCalculationStrategy.construct_doll_attacker(
            FortificationLevel.SEGMENT00
        )
        t = TestDamageCalculationStrategy.construct_defender()
        di = DamageInstance(label="", base_potency=100, tags={DamageTag.PHYSICAL})

        with pytest.raises(ValueError, match="Kulich summon is required"):
            KulichDamageCalculationStrategy().calculate_base_damage(g, t, di)

        with pytest.raises(ValueError, match="Kulich summon is required"):
            KulichDamageCalculationStrategy().resolve_buffs(g, t, di)

    def test_simulacrum_calculate_damage_uses_summon_crit_stats(self):
        """Full calculate_damage regression: crit rate/dmg written by the passive
        must be read from the summon, not the Doll owner."""
        # Doll owner has no crit rate of its own
        g = TestDamageCalculationStrategy.construct_doll_with_simulacrum(
            FortificationLevel.SEGMENT03,
            doll_attack=5429,
            doll_health=0,  # no passive contribution
            summon_attack=5429,
            summon_health=3000,  # passive adds 50% crit at V3 (3000/6*0.1 = 50)
        )
        # Give the summon 200% crit damage so critical_damage = 2 * non_critical_damage,
        # making expected_damage meaningfully larger than non_critical_damage at 50% crit rate.
        g.get_summoned_unit("Simulacrum").initial_stats.basic_attributes[
            StatType.CRIT_DAMAGE
        ] = 200

        t = TestDamageCalculationStrategy.construct_defender()
        di = DamageInstance(
            label="",
            base_potency=100,
            tags={DamageTag.PHYSICAL},
        )

        import copy

        summary = SimulacrumDamageCalculationStrategy().calculate_damage(
            attacker=copy.deepcopy(g),
            target=copy.deepcopy(t),
            damage_instance=di,
        )

        # Effective crit rate must come from the summon (50%), not the owner (0%)
        assert summary.critical_rate == pytest.approx(0.50)
        # With 200% crit_damage and 50% crit_rate: expected = 1.5 * non_critical
        assert summary.expected_damage == pytest.approx(
            1.5 * summary.non_critical_damage
        )

    def test_simulacrum_calculate_damage_doll_owner_crit_stats_not_used(self):
        """Doll owner crit rate must NOT bleed into the Simulacrum damage path."""
        # Give the owner 100 % crit rate but the summon has none
        doll_with_summon = TestDamageCalculationStrategy.construct_doll_with_simulacrum(
            FortificationLevel.SEGMENT00,
            doll_attack=5429,
            doll_health=0,
            summon_attack=5429,
            summon_health=0,
        )
        doll_with_summon.initial_stats.basic_attributes[StatType.CRIT_RATE] = 100

        t = TestDamageCalculationStrategy.construct_defender()
        di = DamageInstance(
            label="",
            base_potency=100,
            tags={DamageTag.PHYSICAL},
        )

        import copy

        summary = SimulacrumDamageCalculationStrategy().calculate_damage(
            attacker=copy.deepcopy(doll_with_summon),
            target=copy.deepcopy(t),
            damage_instance=di,
        )

        # Summon has 0 crit rate, so effective crit rate must be 0
        assert summary.critical_rate == pytest.approx(0.0)
        assert summary.expected_damage == pytest.approx(summary.non_critical_damage)

    def test_yoohee_resolve_buffs_applies_v6_passive_and_super_resolution(self):
        g = TestDamageCalculationStrategy.construct_doll_attacker(
            FortificationLevel.SEGMENT06
        )
        t = TestDamageCalculationStrategy.construct_defender()
        di = DamageInstance(label="", base_potency=100, tags={DamageTag.PHYSICAL})

        buff = Buff(
            value=12,
            modifier_type=ModifierType.MULTIPLICATIVE,
            stat_type=StatType.ATTACK,
        )
        debuff = Debuff(
            value=-20,
            modifier_type=ModifierType.MULTIPLICATIVE,
            stat_type=StatType.DEFENSE,
        )

        YooheeDamageCalculationStrategy().resolve_buffs(
            g,
            t,
            di,
            buffs_before=[buff],
            debuffs_before=[debuff],
        )

        assert g.initial_stats.special_attributes[
            SpecialAttribute.CRITICAL_DAMAGE
        ].get_multiplier(DamageTag.ALL) == pytest.approx(10)
        assert g.multiplicative_modifiers.basic_attributes[StatType.ATTACK] == (
            pytest.approx(57)
        )
        assert t.multiplicative_modifiers.basic_attributes[StatType.DEFENSE] == (
            pytest.approx(-20)
        )

    def test_yoohee_resolve_buffs_does_not_apply_passive_below_v6(self):
        g = TestDamageCalculationStrategy.construct_doll_attacker(
            FortificationLevel.SEGMENT05
        )
        t = TestDamageCalculationStrategy.construct_defender()
        di = DamageInstance(label="", base_potency=100, tags={DamageTag.PHYSICAL})

        YooheeDamageCalculationStrategy().resolve_buffs(g, t, di)

        assert g.initial_stats.special_attributes[
            SpecialAttribute.CRITICAL_DAMAGE
        ].get_multiplier(DamageTag.ALL) == pytest.approx(0)
        assert g.multiplicative_modifiers.basic_attributes[StatType.ATTACK] == (
            pytest.approx(0)
        )

    def test_yoohee_resolve_buffs_does_not_apply_passive_to_non_doll(self):
        g = TestDamageCalculationStrategy.construct_attacker()
        t = TestDamageCalculationStrategy.construct_defender()
        di = DamageInstance(label="", base_potency=100, tags={DamageTag.PHYSICAL})

        YooheeDamageCalculationStrategy().resolve_buffs(g, t, di)

        assert g.initial_stats.special_attributes[
            SpecialAttribute.CRITICAL_DAMAGE
        ].get_multiplier(DamageTag.ALL) == pytest.approx(0)
        assert g.multiplicative_modifiers.basic_attributes[StatType.ATTACK] == (
            pytest.approx(0)
        )

    def test_sextans_resolve_buffs_applies_overflow_crit_rate_bonuses_at_v0(self):
        g = TestDamageCalculationStrategy.construct_doll_attacker(
            FortificationLevel.SEGMENT00
        )
        t = TestDamageCalculationStrategy.construct_defender()
        g.initial_stats.basic_attributes[StatType.CRIT_RATE] = 140
        di = DamageInstance(label="", base_potency=100, tags={DamageTag.MELEE})

        SextansDamageCalculationStrategy().resolve_buffs(g, t, di)

        # V0 cap is 30, even with 40 overflow crit rate.
        assert g.multiplicative_modifiers.basic_attributes[StatType.ATTACK] == (
            pytest.approx(30)
        )
        assert g.additive_modifiers.special_attributes[
            SpecialAttribute.CRITICAL_DAMAGE
        ].get_multiplier(DamageTag.ALL) == pytest.approx(30)

    def test_sextans_resolve_buffs_uses_higher_overflow_cap_at_v3(self):
        g = TestDamageCalculationStrategy.construct_doll_attacker(
            FortificationLevel.SEGMENT03
        )
        t = TestDamageCalculationStrategy.construct_defender()
        g.initial_stats.basic_attributes[StatType.CRIT_RATE] = 140
        di = DamageInstance(label="", base_potency=100, tags={DamageTag.MELEE})

        SextansDamageCalculationStrategy().resolve_buffs(g, t, di)

        # V3 cap is 45, so 40 overflow applies in full.
        assert g.multiplicative_modifiers.basic_attributes[StatType.ATTACK] == (
            pytest.approx(40)
        )
        assert g.additive_modifiers.special_attributes[
            SpecialAttribute.CRITICAL_DAMAGE
        ].get_multiplier(DamageTag.ALL) == pytest.approx(40)

    def test_sextans_resolve_buffs_always_adds_melee_damage_boost_for_doll(self):
        g = TestDamageCalculationStrategy.construct_doll_attacker(
            FortificationLevel.SEGMENT00
        )
        t = TestDamageCalculationStrategy.construct_defender()
        di = DamageInstance(label="", base_potency=100, tags={DamageTag.MELEE})

        SextansDamageCalculationStrategy().resolve_buffs(g, t, di)

        assert g.additive_modifiers.special_attributes[
            SpecialAttribute.DAMAGE_BOOST
        ].get_multiplier(DamageTag.MELEE) == pytest.approx(10)

    def test_sextans_resolve_buffs_ignores_non_doll_attackers(self):
        g = Unit()
        t = TestDamageCalculationStrategy.construct_defender()
        g.initial_stats.basic_attributes[StatType.CRIT_RATE] = 180
        di = DamageInstance(label="", base_potency=100, tags={DamageTag.MELEE})

        SextansDamageCalculationStrategy().resolve_buffs(g, t, di)

        assert g.multiplicative_modifiers.basic_attributes[StatType.ATTACK] == (
            pytest.approx(0)
        )
        assert g.additive_modifiers.special_attributes[
            SpecialAttribute.CRITICAL_DAMAGE
        ].get_multiplier(DamageTag.ALL) == pytest.approx(0)
        assert g.additive_modifiers.special_attributes[
            SpecialAttribute.DAMAGE_BOOST
        ].get_multiplier(DamageTag.MELEE) == pytest.approx(0)


class TestLainieBonusDamageCalculations:
    @staticmethod
    def construct_unit_for_bonus_damage(
        *,
        health: float,
        damage_boost_physical: float = 0,
        defense_ignore_physical: float = 0,
    ) -> Unit:
        u = Unit()
        u.initial_stats.basic_attributes[StatType.HEALTH] = health
        u.initial_stats.special_attributes[
            SpecialAttribute.DAMAGE_BOOST
        ].set_multiplier(DamageTag.PHYSICAL, damage_boost_physical)
        u.initial_stats.special_attributes[
            SpecialAttribute.DEFENSE_IGNORE
        ].set_multiplier(DamageTag.PHYSICAL, defense_ignore_physical)

        return u

    def test_get_health_conversion_rate_by_fortification(self):
        assert LainieBonusDamageCalculations.get_health_conversion_rate(
            FortificationLevel.SEGMENT00
        ) == pytest.approx(0.1)
        assert LainieBonusDamageCalculations.get_health_conversion_rate(
            FortificationLevel.SEGMENT03
        ) == pytest.approx(0.2)
        assert LainieBonusDamageCalculations.get_health_conversion_rate(
            FortificationLevel.SEGMENT05
        ) == pytest.approx(0.3)

    @pytest.mark.parametrize(
        "health,fortification_level,damage_boost_physical,defense_ignore_physical,tags,expected_bonus_damage",
        [
            # Baseline: no damage boost, no reversed-assault bias
            (
                4611,
                FortificationLevel.SEGMENT00,
                2.5,
                99.9,
                {DamageTag.PHYSICAL},
                472.6,
            ),
            (
                4990,
                FortificationLevel.SEGMENT00,
                2.5,
                99.9,
                {DamageTag.PHYSICAL},
                511.5,
            ),
            # High defense ignore intended to trigger reversed-assault bias path
            (
                3775,
                FortificationLevel.SEGMENT00,
                7.5,
                233,
                {DamageTag.PHYSICAL},
                1508.1,
            ),
            (
                4217,
                FortificationLevel.SEGMENT00,
                7.5,
                233,
                {DamageTag.PHYSICAL},
                1599.7,
            ),
            (
                4606,
                FortificationLevel.SEGMENT00,
                7.5,
                233,
                {DamageTag.PHYSICAL},
                1680.4,
            ),
            # More increased damage
            (
                4650,
                FortificationLevel.SEGMENT00,
                42.4,
                233,
                {DamageTag.PHYSICAL},
                1973.9,
            ),
            (
                4813,
                FortificationLevel.SEGMENT00,
                42.4,
                233,
                {DamageTag.PHYSICAL},
                2013.4,
            ),
            (
                5077,
                FortificationLevel.SEGMENT00,
                42.4,
                233,
                {DamageTag.PHYSICAL},
                2077.4,
            ),
        ],
    )
    def test_get_bonus_damage_from_unit_reference_cases(
        self,
        health: float,
        fortification_level: FortificationLevel,
        damage_boost_physical: float,
        defense_ignore_physical: float,
        tags: set[DamageTag],
        expected_bonus_damage: float | None,
    ):
        if expected_bonus_damage is None:
            pytest.skip("Populate expected_bonus_damage from your validated test data")

        unit = self.construct_unit_for_bonus_damage(
            health=health,
            damage_boost_physical=damage_boost_physical,
            defense_ignore_physical=defense_ignore_physical,
        )
        target = TestDamageCalculationStrategy.construct_defender()
        di = DamageInstance(label="", base_potency=100, tags=tags)

        _, negative_def = _calculate_effective_and_negative_defense(
            attacker=unit,
            target=target,
            damage_instance=di,
        )

        bonus_increased_damage = resolve_reversed_assault(di, negative_def)
        unit.additive_modifiers.special_attributes[
            SpecialAttribute.DAMAGE_BOOST
        ].add_to_multiplier(DamageTag.PHYSICAL, bonus_increased_damage)

        actual = LainieBonusDamageCalculations.get_bonus_damage_from_unit(
            unit=unit,
            fortification_level=fortification_level,
            target=target,
            damage_instance=di,
        )

        assert actual == pytest.approx(expected_bonus_damage, rel=1e-3)


class TestFixedDamageInstance:
    """Tests for FixedDamageInstance and fixed damage calculation behavior."""

    def test_fixed_damage_instance_has_fixed_tag_by_default(self):
        """FixedDamageInstance should automatically include the FIXED tag."""
        fdi = FixedDamageInstance(label="Test Fixed", base_potency=100)

        assert DamageTag.FIXED in fdi.tags
        assert fdi.label == "Test Fixed"
        assert fdi.base_potency == 100
        assert fdi.group_name == "Fixed Damage"

    def test_fixed_damage_ignores_target_defense(self):
        """Fixed damage should deal full damage regardless of target defense."""
        attacker = TestDamageCalculationStrategy.construct_attacker()
        target_no_def = Unit()
        target_no_def.initial_stats.basic_attributes[StatType.ATTACK] = 5429
        target_high_def = Unit()
        target_high_def.initial_stats.basic_attributes[StatType.DEFENSE] = 10000

        di = FixedDamageInstance(label="Fixed Damage", base_potency=100)
        strat = StandardDamageCalculationStrategy()

        damage_no_def = strat.calculate_damage(
            attacker, target_no_def, di
        ).non_critical_damage
        damage_high_def = strat.calculate_damage(
            attacker, target_high_def, di
        ).non_critical_damage

        assert damage_no_def == pytest.approx(damage_high_def)

    def test_fixed_damage_scales_with_attacker_attack(self):
        """Fixed damage should scale with attacker's Attack stat."""
        target = TestDamageCalculationStrategy.construct_defender()
        di = FixedDamageInstance(label="Fixed Damage", base_potency=100)
        strat = StandardDamageCalculationStrategy()

        # Attacker with 1000 Attack
        attacker_low = Unit()
        attacker_low.initial_stats.basic_attributes[StatType.ATTACK] = 1000

        # Attacker with 5000 Attack
        attacker_high = Unit()
        attacker_high.initial_stats.basic_attributes[StatType.ATTACK] = 5000

        damage_low = strat.calculate_damage(
            attacker_low, target, di
        ).non_critical_damage
        damage_high = strat.calculate_damage(
            attacker_high, target, di
        ).non_critical_damage

        assert damage_low < damage_high
        assert damage_low == pytest.approx(1000)
        assert damage_high == pytest.approx(5000)

    def test_fixed_damage_cannot_critically_hit(self):
        """Fixed damage should never critical hit."""
        attacker = TestDamageCalculationStrategy.construct_attacker()
        attacker.initial_stats.basic_attributes[StatType.CRIT_RATE] = (
            100  # Guaranteed crit
        )
        target = TestDamageCalculationStrategy.construct_defender()

        di = FixedDamageInstance(label="Fixed Damage", base_potency=100)
        strat = StandardDamageCalculationStrategy()

        summary = strat.calculate_damage(attacker, target, di)

        assert summary.critical_rate == pytest.approx(0)
        assert summary.critical_damage == pytest.approx(summary.non_critical_damage)
        assert summary.expected_damage == pytest.approx(summary.non_critical_damage)

    def test_fixed_damage_ignores_stability_damage_reduction(self):
        """Fixed damage should not be reduced by target's stability damage reduction."""
        attacker = TestDamageCalculationStrategy.construct_attacker()
        target = TestDamageCalculationStrategy.construct_defender()
        target.initial_stats.basic_attributes[StatType.STABILITY_DAMAGE_REDUCTION] = 60

        di = FixedDamageInstance(label="Fixed Damage", base_potency=100)
        strat = StandardDamageCalculationStrategy()

        # Fixed damage with stability broken
        damage_broken = strat.calculate_damage(
            attacker, target, di, is_stability_broken=True
        ).non_critical_damage
        # Fixed damage with stability not broken
        damage_not_broken = strat.calculate_damage(
            attacker, target, di, is_stability_broken=False
        ).non_critical_damage

        assert damage_broken == pytest.approx(damage_not_broken)

    def test_fixed_damage_ignores_phase_weaknesses(self):
        """Fixed damage should not benefit from phase weakness multipliers."""
        attacker = TestDamageCalculationStrategy.construct_attacker()
        target = TestDamageCalculationStrategy.construct_defender()

        di = FixedDamageInstance(label="Fixed Damage", base_potency=100)
        strat = StandardDamageCalculationStrategy()

        # Fixed damage with no phase weaknesses
        damage_no_weakness = strat.calculate_damage(
            attacker, target, di, phase_weaknesses_exploited=0
        ).non_critical_damage
        # Fixed damage with max phase weaknesses
        damage_with_weakness = strat.calculate_damage(
            attacker, target, di, phase_weaknesses_exploited=2
        ).non_critical_damage

        assert damage_no_weakness == pytest.approx(damage_with_weakness)

    def test_fixed_damage_ignores_damage_boost_modifiers(self):
        """Fixed damage should not be affected by damage boost modifiers."""
        attacker = TestDamageCalculationStrategy.construct_attacker()
        target = TestDamageCalculationStrategy.construct_defender()

        # Create fixed damage instance with ALL tag to make sure boosts would apply if not ignored
        di = FixedDamageInstance(label="Fixed Damage", base_potency=100)
        di.tags.add(DamageTag.ALL)

        strat = StandardDamageCalculationStrategy()

        # Calculate base damage
        damage_before = strat.calculate_damage(attacker, target, di).non_critical_damage

        # Add massive damage boost modifiers
        attacker.additive_modifiers.special_attributes[
            SpecialAttribute.DAMAGE_BOOST
        ].set_multiplier(DamageTag.ALL, 500)

        damage_after = strat.calculate_damage(attacker, target, di).non_critical_damage

        # Damage should remain the same (damage boosts ignored for fixed damage)
        assert damage_before == pytest.approx(damage_after)

    def test_fixed_damage_ignores_increased_damage_taken(self):
        """Fixed damage should not be affected by target's increased damage taken."""
        attacker = TestDamageCalculationStrategy.construct_attacker()
        target = TestDamageCalculationStrategy.construct_defender()

        di = FixedDamageInstance(label="Fixed Damage", base_potency=100)
        strat = StandardDamageCalculationStrategy()

        damage_before = strat.calculate_damage(attacker, target, di).non_critical_damage

        # Add massive increased damage taken
        target.initial_stats.special_attributes[
            SpecialAttribute.INCREASE_DAMAGE_TAKEN
        ].set_multiplier(DamageTag.ALL, 200)

        damage_after = strat.calculate_damage(attacker, target, di).non_critical_damage

        # Damage should remain the same
        assert damage_before == pytest.approx(damage_after)

    def test_fixed_damage_with_buffs_and_debuffs(self):
        """Fixed damage should scale with Attack buffs, but not with damage boost modifiers."""
        attacker = TestDamageCalculationStrategy.construct_attacker()
        target = TestDamageCalculationStrategy.construct_defender()

        di = FixedDamageInstance(label="Fixed Damage", base_potency=100)
        strat = StandardDamageCalculationStrategy()

        buff = Buff(
            value=50,
            modifier_type=ModifierType.ADDITIVE,
            stat_type=StatType.ATTACK,
        )
        debuff = Debuff(
            value=-30,
            modifier_type=ModifierType.MULTIPLICATIVE,
            stat_type=StatType.DEFENSE,
        )

        damage = strat.calculate_damage(
            attacker, target, di, buffs_before=[buff], debuffs_before=[debuff]
        ).non_critical_damage

        # Buffs and debuffs should be applied
        assert attacker.additive_modifiers.basic_attributes[StatType.ATTACK] == 50
        assert target.multiplicative_modifiers.basic_attributes[StatType.DEFENSE] == -30

        # Fixed damage scales with Attack buffs (5429 + 50 attack buff = 5479 damage)
        assert damage == pytest.approx(5479)


class TestFayeDamageCalculationStrategy:
    """Tests for FayeDamageCalculationStrategy and Faye's passive/Expansion Key effects."""

    def test_faye_non_doll_attacker_no_bonuses(self):
        """Non-Doll attackers should not receive Faye's passive bonuses."""
        attacker = TestDamageCalculationStrategy.construct_attacker()
        target = TestDamageCalculationStrategy.construct_defender()

        di = DamageInstance(label="Test", base_potency=100, tags={DamageTag.PHYSICAL})
        strat = FayeDamageCalculationStrategy()

        strat.resolve_buffs(attacker, target, di)

        # No modifiers should be applied to non-Doll attacker
        assert attacker.multiplicative_modifiers.basic_attributes[StatType.ATTACK] == 0
        assert (
            attacker.additive_modifiers.special_attributes[
                SpecialAttribute.DEFENSE_IGNORE
            ].get_total_multiplier({DamageTag.PHYSICAL})
            == 0
        )

    def test_faye_doll_v0_applies_rend_and_gash_bonuses(self):
        """Faye V0 should apply Rend defense ignore (16%) and Gash bonuses (50% defense ignore + 15% Attack)."""
        attacker = TestDamageCalculationStrategy.construct_doll_attacker(
            FortificationLevel.SEGMENT00
        )
        target = TestDamageCalculationStrategy.construct_defender()

        di = DamageInstance(label="Test", base_potency=100, tags={DamageTag.ALL})
        strat = FayeDamageCalculationStrategy()

        strat.resolve_buffs(attacker, target, di)

        # Rend stacks: 8 stacks * 2% per stack = 16%
        # Gash: 50%
        # Total: 66% defense ignore
        total_defense_ignore = attacker.additive_modifiers.special_attributes[
            SpecialAttribute.DEFENSE_IGNORE
        ].get_total_multiplier({DamageTag.ALL})
        assert total_defense_ignore == pytest.approx(66)

        # Attack multiplier from Gash
        assert attacker.multiplicative_modifiers.basic_attributes[
            StatType.ATTACK
        ] == pytest.approx(15)

    def test_faye_doll_v1_increases_rend_per_stack(self):
        """Faye V1+ should use 4% defense ignore per Rend stack instead of 2%."""
        attacker = TestDamageCalculationStrategy.construct_doll_attacker(
            FortificationLevel.SEGMENT01
        )
        target = TestDamageCalculationStrategy.construct_defender()

        di = DamageInstance(label="Test", base_potency=100, tags={DamageTag.ALL})
        strat = FayeDamageCalculationStrategy()

        strat.resolve_buffs(attacker, target, di)

        # Rend stacks: 8 stacks * 4% per stack = 32%
        # Gash: 50%
        # Total: 82% defense ignore
        total_defense_ignore = attacker.additive_modifiers.special_attributes[
            SpecialAttribute.DEFENSE_IGNORE
        ].get_total_multiplier({DamageTag.ALL})
        assert total_defense_ignore == pytest.approx(82)

    def test_faye_doll_v3_increases_rend_per_stack(self):
        """Faye V3+ should still use 4% defense ignore per Rend stack."""
        attacker = TestDamageCalculationStrategy.construct_doll_attacker(
            FortificationLevel.SEGMENT03
        )
        target = TestDamageCalculationStrategy.construct_defender()

        di = DamageInstance(label="Test", base_potency=100, tags={DamageTag.ALL})
        strat = FayeDamageCalculationStrategy()

        strat.resolve_buffs(attacker, target, di)

        # Rend stacks: 8 stacks * 4% per stack = 32%
        # Gash: 50%
        # Total: 82% defense ignore
        total_defense_ignore = attacker.additive_modifiers.special_attributes[
            SpecialAttribute.DEFENSE_IGNORE
        ].get_total_multiplier({DamageTag.ALL})
        assert total_defense_ignore == pytest.approx(82)

    def test_faye_damage_with_full_bonuses_v0(self):
        """Verify Faye V0 damage calculation includes all bonuses."""
        attacker = TestDamageCalculationStrategy.construct_doll_attacker(
            FortificationLevel.SEGMENT00
        )
        target = TestDamageCalculationStrategy.construct_defender()

        di = DamageInstance(
            label="Test",
            base_potency=100,
            tags={DamageTag.PHYSICAL, DamageTag.ALL},
        )
        strat = FayeDamageCalculationStrategy()

        summary = strat.calculate_damage(attacker, target, di)

        # Damage should reflect the 66% defense ignore and 15% attack boost
        # Original attack: 5429
        # With 15% multiplier: 5429 * 1.15 = 6243.35
        # Defense: 5000, Attack: 6243.35
        # With 66% defense ignore: effective_def = max(0, 5000 * (1 - 0.66)) = 1700
        # term1 = 6243.35 / (1 + 1700/6243.35) = ~2677.47
        # potency multiplier: 1 + 0 = 1
        # damage: 1 * 2677.47 = 2677.47

        assert summary.non_critical_damage > 0
        assert summary.effective_attack == pytest.approx(6243.35)

    def test_faye_damage_with_full_bonuses_v1(self):
        """Verify Faye V1+ damage calculation uses increased rend defense ignore."""
        attacker = TestDamageCalculationStrategy.construct_doll_attacker(
            FortificationLevel.SEGMENT01
        )
        target = TestDamageCalculationStrategy.construct_defender()

        di = DamageInstance(
            label="Test",
            base_potency=100,
            tags={DamageTag.PHYSICAL, DamageTag.ALL},
        )
        strat = FayeDamageCalculationStrategy()

        summary = strat.calculate_damage(attacker, target, di)

        # Damage should reflect the 82% defense ignore (higher than V0)
        # With 82% defense ignore: effective_def = max(0, 5000 * (1 - 0.82)) = 900
        assert summary.effective_defense == pytest.approx(900)

    def test_faye_defense_ignore_stacks_with_tags(self):
        """Faye's defense ignore should apply to ALL damage types."""
        attacker = TestDamageCalculationStrategy.construct_doll_attacker(
            FortificationLevel.SEGMENT00
        )
        target = TestDamageCalculationStrategy.construct_defender()

        di_physical = DamageInstance(
            label="Test", base_potency=100, tags={DamageTag.PHYSICAL, DamageTag.ALL}
        )
        di_melee = DamageInstance(
            label="Test", base_potency=100, tags={DamageTag.MELEE, DamageTag.ALL}
        )

        strat = FayeDamageCalculationStrategy()

        strat.resolve_buffs(attacker, target, di_physical)

        # Both physical and melee should get the ALL tag defense ignore
        physical_ignore = attacker.additive_modifiers.special_attributes[
            SpecialAttribute.DEFENSE_IGNORE
        ].get_total_multiplier({DamageTag.PHYSICAL, DamageTag.ALL})

        melee_ignore = attacker.additive_modifiers.special_attributes[
            SpecialAttribute.DEFENSE_IGNORE
        ].get_total_multiplier({DamageTag.MELEE, DamageTag.ALL})

        assert physical_ignore == pytest.approx(66)
        assert melee_ignore == pytest.approx(66)


class TestHelenDamageCalculationStrategy:
    """Tests for HelenDamageCalculationStrategy."""

    @staticmethod
    def construct_helen_attacker(
        level: FortificationLevel,
        initial_defense: float = 2000,
        initial_attack: float = 3000,
    ) -> Doll:
        class DummyDoll(Doll):
            def set_fortification_level(self, level: FortificationLevel) -> None:
                self.fortification_level = level

        d: Doll = DummyDoll()
        d.initial_stats.basic_attributes[StatType.ATTACK] = initial_attack
        d.initial_stats.basic_attributes[StatType.DEFENSE] = initial_defense
        d.initial_stats.basic_attributes[StatType.CRIT_DAMAGE] = 150
        d.set_fortification_level(level)
        return d

    def test_resolve_buffs_applies_30_percent_defense_boost(self):
        g = self.construct_helen_attacker(FortificationLevel.SEGMENT00)
        t = TestDamageCalculationStrategy.construct_defender()
        di = DamageInstance(label="", base_potency=100, tags={DamageTag.FREEZE})

        HelenDamageCalculationStrategy().resolve_buffs(g, t, di)

        assert g.multiplicative_modifiers.basic_attributes[
            StatType.DEFENSE
        ] == pytest.approx(30)

    def test_resolve_buffs_applies_30_percent_health_boost(self):
        g = self.construct_helen_attacker(FortificationLevel.SEGMENT00)
        t = TestDamageCalculationStrategy.construct_defender()
        di = DamageInstance(label="", base_potency=100, tags={DamageTag.FREEZE})

        HelenDamageCalculationStrategy().resolve_buffs(g, t, di)

        assert g.multiplicative_modifiers.basic_attributes[
            StatType.HEALTH
        ] == pytest.approx(30)

    def test_resolve_buffs_v0_adds_attack_from_defense_at_15_percent(self):
        # effective defense = 2000 * (1 + 30/100) = 2600
        # attack from defense = 2600 * 0.15 = 390
        g = self.construct_helen_attacker(
            FortificationLevel.SEGMENT00, initial_defense=2000
        )
        t = TestDamageCalculationStrategy.construct_defender()
        di = DamageInstance(label="", base_potency=100, tags={DamageTag.FREEZE})

        HelenDamageCalculationStrategy().resolve_buffs(g, t, di)

        assert g.additive_modifiers.basic_attributes[StatType.ATTACK] == pytest.approx(
            390
        )

    def test_resolve_buffs_v1_adds_attack_from_defense_at_15_percent(self):
        # Same rate as V0
        g = self.construct_helen_attacker(
            FortificationLevel.SEGMENT01, initial_defense=2000
        )
        t = TestDamageCalculationStrategy.construct_defender()
        di = DamageInstance(label="", base_potency=100, tags={DamageTag.FREEZE})

        HelenDamageCalculationStrategy().resolve_buffs(g, t, di)

        assert g.additive_modifiers.basic_attributes[StatType.ATTACK] == pytest.approx(
            390
        )

    def test_resolve_buffs_v2_adds_attack_from_defense_at_30_percent(self):
        # effective defense = 2000 * 1.3 = 2600
        # attack from defense = 2600 * 0.30 = 780
        g = self.construct_helen_attacker(
            FortificationLevel.SEGMENT02, initial_defense=2000
        )
        t = TestDamageCalculationStrategy.construct_defender()
        di = DamageInstance(label="", base_potency=100, tags={DamageTag.FREEZE})

        HelenDamageCalculationStrategy().resolve_buffs(g, t, di)

        assert g.additive_modifiers.basic_attributes[StatType.ATTACK] == pytest.approx(
            780
        )

    def test_resolve_buffs_v5_adds_attack_from_defense_at_30_percent(self):
        # Same rate as V2
        g = self.construct_helen_attacker(
            FortificationLevel.SEGMENT05, initial_defense=2000
        )
        t = TestDamageCalculationStrategy.construct_defender()
        di = DamageInstance(label="", base_potency=100, tags={DamageTag.FREEZE})

        HelenDamageCalculationStrategy().resolve_buffs(g, t, di)

        assert g.additive_modifiers.basic_attributes[StatType.ATTACK] == pytest.approx(
            780
        )

    def test_resolve_buffs_v6_adds_attack_from_defense_at_70_percent(self):
        # effective defense = 2000 * 1.3 = 2600
        # attack from defense = 2600 * 0.70 = 1820
        g = self.construct_helen_attacker(
            FortificationLevel.SEGMENT06, initial_defense=2000
        )
        t = TestDamageCalculationStrategy.construct_defender()
        di = DamageInstance(label="", base_potency=100, tags={DamageTag.FREEZE})

        HelenDamageCalculationStrategy().resolve_buffs(g, t, di)

        assert g.additive_modifiers.basic_attributes[StatType.ATTACK] == pytest.approx(
            1820
        )

    def test_resolve_buffs_conversion_includes_30_percent_defense_buff(self):
        """Defense conversion is calculated after applying the 30% defense boost."""
        # initial_defense=1000: effective = 1000 * 1.3 = 1300, V6 conversion = 1300 * 0.70 = 910
        g = self.construct_helen_attacker(
            FortificationLevel.SEGMENT06, initial_defense=1000
        )
        t = TestDamageCalculationStrategy.construct_defender()
        di = DamageInstance(label="", base_potency=100, tags={DamageTag.FREEZE})

        HelenDamageCalculationStrategy().resolve_buffs(g, t, di)

        assert g.additive_modifiers.basic_attributes[StatType.ATTACK] == pytest.approx(
            910
        )

    def test_resolve_buffs_ignores_non_doll_attacker(self):
        g = TestDamageCalculationStrategy.construct_attacker()
        t = TestDamageCalculationStrategy.construct_defender()
        di = DamageInstance(label="", base_potency=100, tags={DamageTag.FREEZE})

        HelenDamageCalculationStrategy().resolve_buffs(g, t, di)

        assert g.multiplicative_modifiers.basic_attributes[
            StatType.DEFENSE
        ] == pytest.approx(0)
        assert g.multiplicative_modifiers.basic_attributes[
            StatType.HEALTH
        ] == pytest.approx(0)
        assert g.additive_modifiers.basic_attributes[StatType.ATTACK] == pytest.approx(
            0
        )

    def test_calculate_damage_v0_effective_attack_includes_defense_conversion(self):
        """Full calculate_damage: effective attack must reflect 15% of (defense * 1.3)."""
        import copy

        g = self.construct_helen_attacker(
            FortificationLevel.SEGMENT00,
            initial_attack=3000,
            initial_defense=2000,
        )
        t = TestDamageCalculationStrategy.construct_defender()
        di = DamageInstance(label="", base_potency=100, tags={DamageTag.FREEZE})

        summary = HelenDamageCalculationStrategy().calculate_damage(
            attacker=copy.deepcopy(g),
            target=copy.deepcopy(t),
            damage_instance=di,
        )

        # effective attack = initial_attack + attack_from_defense = 3000 + 390 = 3390
        assert summary.effective_attack == pytest.approx(3390)

    def test_calculate_damage_v6_effective_attack_includes_defense_conversion(self):
        """Full calculate_damage V6: effective attack must reflect 70% of (defense * 1.3)."""
        import copy

        g = self.construct_helen_attacker(
            FortificationLevel.SEGMENT06,
            initial_attack=3000,
            initial_defense=2000,
        )
        t = TestDamageCalculationStrategy.construct_defender()
        di = DamageInstance(label="", base_potency=100, tags={DamageTag.FREEZE})

        summary = HelenDamageCalculationStrategy().calculate_damage(
            attacker=copy.deepcopy(g),
            target=copy.deepcopy(t),
            damage_instance=di,
        )

        # effective attack = 3000 + 1820 = 4820
        assert summary.effective_attack == pytest.approx(4820)
