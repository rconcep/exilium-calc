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

    def test_calculate_adjusted_potency(self):
        """ """
        label: str = "Unity: Enhanced"
        base_potency: float = 30.0
        tags: set[DamageTag] = {
            DamageTag.PASSIVE,
            DamageTag.TARGETED,
            DamageTag.FREEZE,
            DamageTag.PASSIVE,
        }
        di: DamageInstance = DamageInstance(
            label=label, base_potency=base_potency, tags=tags
        )

        mult: IncreasedDamageMultipliers = IncreasedDamageMultipliers()
        mult.set_multiplier(DamageTag.SUPPORT_ACTION, 25)
        mult.set_multiplier(DamageTag.FREEZE, 20)
        mult.set_multiplier(DamageTag.PASSIVE, 15)
        mult.set_multiplier(DamageTag.AREA_OF_EFFECT, 7)

        assert pytest.approx(base_potency * 1.35) == di.calculate_adjusted_potency(mult)

        label: str = "Howling Cyclone"
        base_potency: float = 474.0
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

        assert pytest.approx(base_potency * 1.27) == di.calculate_adjusted_potency(mult)


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
            label,
            base_potency,
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

        mult: IncreasedDamageMultipliers = IncreasedDamageMultipliers()
        mult.set_multiplier(DamageTag.FREEZE, 21.4)
        mult.set_multiplier(DamageTag.ULTIMATE, 10.4)
        mult.set_multiplier(DamageTag.AREA_OF_EFFECT, 30)

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
            label,
            base_potency,
            tags=tags,
            debuffs_before=[
                debuff,
            ],
        )
        di.calculate_adjusted_potency(mult)

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
        di: DamageInstance = DamageInstance(label, base_potency, tags=tags)

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
        di = DamageInstance("", 80, tags={DamageTag.PHYSICAL})

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
        di: DamageInstance = DamageInstance(label, base_potency, tags=tags)

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
        di: DamageInstance = DamageInstance(label, base_potency, tags=tags)

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
