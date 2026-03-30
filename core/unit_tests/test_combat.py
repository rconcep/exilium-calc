import pytest

from core.combat import *


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

        assert summary.effective_critical_rate == pytest.approx(1.0)
        assert summary.expected_damage == pytest.approx(summary.critical_damage)

    def test_resolve_defense_shredding(self):
        di: DamageInstance = DamageInstance(
            label="", base_potency=100, tags={DamageTag.FREEZE}
        )
        negative_def: float = 25
        assert StandardDamageCalculationStrategy().resolve_reversed_assault(
            di, negative_def
        ) == pytest.approx(0)

        di.tags = {DamageTag.PHYSICAL}
        assert StandardDamageCalculationStrategy().resolve_reversed_assault(
            di, negative_def
        ) == pytest.approx(25 * 0.5)

        negative_def: float = -25
        assert StandardDamageCalculationStrategy().resolve_reversed_assault(
            di, negative_def
        ) == pytest.approx(0)

        negative_def: float = 125
        assert StandardDamageCalculationStrategy().resolve_reversed_assault(
            di, negative_def
        ) == pytest.approx(125 * 0.75)

        negative_def: float = 255
        assert StandardDamageCalculationStrategy().resolve_reversed_assault(
            di, negative_def
        ) == pytest.approx(255 * 1)

        negative_def: float = 302
        assert StandardDamageCalculationStrategy().resolve_reversed_assault(
            di, negative_def
        ) == pytest.approx(302 * 1.5)

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

    def test_lainie_adjusted_potency_scales_with_fortification_when_defense_zero(self):
        t: Unit = Unit()
        t.initial_stats.basic_attributes[StatType.DEFENSE] = 0
        di = DamageInstance(label="", base_potency=100, tags={DamageTag.PHYSICAL})

        g_v0 = TestDamageCalculationStrategy.construct_doll_attacker(
            FortificationLevel.SEGMENT00
        )
        g_v3 = TestDamageCalculationStrategy.construct_doll_attacker(
            FortificationLevel.SEGMENT03
        )
        g_v5 = TestDamageCalculationStrategy.construct_doll_attacker(
            FortificationLevel.SEGMENT05
        )
        g_v0.initial_stats.basic_attributes[StatType.HEALTH] = 1000
        g_v3.initial_stats.basic_attributes[StatType.HEALTH] = 1000
        g_v5.initial_stats.basic_attributes[StatType.HEALTH] = 1000

        strat = LainieDamageCalculationStrategy()
        p0 = strat.calculate_adjusted_potency(g_v0, t, di)
        p3 = strat.calculate_adjusted_potency(g_v3, t, di)
        p5 = strat.calculate_adjusted_potency(g_v5, t, di)

        assert p0 == pytest.approx(200)
        assert p3 == pytest.approx(300)
        assert p5 == pytest.approx(400)

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

    def test_simulacrum_adjusted_potency_scales_with_fortification_when_defense_zero(
        self,
    ):
        g_v0 = TestDamageCalculationStrategy.construct_doll_with_simulacrum(
            FortificationLevel.SEGMENT00,
            summon_health=1000,
        )
        g_v3 = TestDamageCalculationStrategy.construct_doll_with_simulacrum(
            FortificationLevel.SEGMENT03,
            summon_health=1000,
        )
        g_v5 = TestDamageCalculationStrategy.construct_doll_with_simulacrum(
            FortificationLevel.SEGMENT05,
            summon_health=1000,
        )
        t: Unit = Unit()
        t.initial_stats.basic_attributes[StatType.DEFENSE] = 0
        di = DamageInstance(label="", base_potency=100, tags={DamageTag.PHYSICAL})

        strat = SimulacrumDamageCalculationStrategy()
        p0 = strat.calculate_adjusted_potency(g_v0, t, di)
        p3 = strat.calculate_adjusted_potency(g_v3, t, di)
        p5 = strat.calculate_adjusted_potency(g_v5, t, di)

        assert p0 == pytest.approx(200)
        assert p3 == pytest.approx(300)
        assert p5 == pytest.approx(400)

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
            SimulacrumDamageCalculationStrategy().calculate_adjusted_potency(g, t, di)

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
        assert summary.effective_critical_rate == pytest.approx(0.50)
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
        assert summary.effective_critical_rate == pytest.approx(0.0)
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
