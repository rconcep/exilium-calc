from core.combat import DamageInstance, UllridDamageCalculationStrategy
from core.dolls.ullrid import *
from core.types import (
    DamageTag,
    FortificationLevel,
    ModifierType,
    SpecialAttribute,
    StatType,
    Unit,
)


class TestUllridSkills:
    def test_warning_shot(self):
        warning_shot: DamageInstance = WarningShot().execute()

        assert warning_shot.base_potency == 80
        assert DamageTag.BASIC in warning_shot.tags
        assert DamageTag.ACTIVE in warning_shot.tags
        assert warning_shot.group_name == "Warning Shot"
        assert isinstance(
            warning_shot.damage_calculation_strategy,
            UllridDamageCalculationStrategy,
        )

    def test_blade_whirlwind(self):
        blade_whirlwind: DamageInstance = BladeWhirlwind().execute(
            attacking_same_target_within_one_action=True
        )

        assert blade_whirlwind.base_potency == 90
        assert DamageTag.CONFECTANCE in blade_whirlwind.tags
        assert blade_whirlwind.buffs_before == []

    def test_blade_whirlwind_v1_same_target(self):
        blade_whirlwind: DamageInstance = BladeWhirlwindV1().execute(
            attacking_same_target_within_one_action=True
        )

        assert len(blade_whirlwind.buffs_before) == 1
        assert blade_whirlwind.buffs_before[0].value == 30
        assert blade_whirlwind.buffs_before[0].modifier_type == ModifierType.ADDITIVE
        assert (
            blade_whirlwind.buffs_before[0].stat_type
            == SpecialAttribute.DAMAGE_BOOST
        )
        assert blade_whirlwind.buffs_before[0].tag == DamageTag.CONFECTANCE

    def test_blade_whirlwind_v1_different_target(self):
        blade_whirlwind: DamageInstance = BladeWhirlwindV1().execute(
            attacking_same_target_within_one_action=False
        )

        assert blade_whirlwind.buffs_before == []

    def test_determined_pursuit(self):
        determined_pursuit: DamageInstance = DeterminedPursuit().execute()

        assert determined_pursuit.base_potency == 90
        assert DamageTag.PASSIVE in determined_pursuit.tags
        assert determined_pursuit.group_name == "Determined Pursuit"
        assert len(determined_pursuit.buffs_before) == 1
        assert determined_pursuit.buffs_before[0].value == 30

    def test_hidden_pursuit_v6_missing_health_scaling(self):
        hidden_pursuit: DamageInstance = HiddenPursuitV6().execute(
            stacks_of_hunters_talent=6,
            percent_target_missing_health=37,
        )

        assert hidden_pursuit.base_potency == 180
        assert len(hidden_pursuit.buffs_before) == 2
        assert hidden_pursuit.buffs_before[0].value == 60
        assert hidden_pursuit.buffs_before[0].tag == DamageTag.ULTIMATE
        assert hidden_pursuit.buffs_before[1].value == 18
        assert hidden_pursuit.buffs_before[1].modifier_type == ModifierType.MULTIPLICATIVE
        assert hidden_pursuit.buffs_before[1].stat_type == StatType.ATTACK

    def test_lacerating_wound(self):
        lacerating_wound: DamageInstance = LaceratingWound().execute(
            original_damage_instance_potency=90
        )

        assert lacerating_wound.base_potency == 36
        assert DamageTag.PASSIVE in lacerating_wound.tags
        assert lacerating_wound.group_name == "Lacerating Wound"


class TestUllrid:
    def test_set_to_v0(self):
        ullrid: Ullrid = Ullrid()
        ullrid.set_to_v0()

        assert isinstance(ullrid.blade_whirlwind, BladeWhirlwind)
        assert isinstance(ullrid.hidden_pursuit, HiddenPursuit)

    def test_set_to_v1(self):
        ullrid: Ullrid = Ullrid()
        ullrid.set_to_v1()

        assert isinstance(ullrid.blade_whirlwind, BladeWhirlwindV1)
        assert isinstance(ullrid.hidden_pursuit, HiddenPursuit)

    def test_set_to_v4(self):
        ullrid: Ullrid = Ullrid()
        ullrid.set_to_v4()

        assert isinstance(ullrid.blade_whirlwind, BladeWhirlwindV1)
        assert isinstance(ullrid.hidden_pursuit, HiddenPursuitV4)

    def test_set_to_v6(self):
        ullrid: Ullrid = Ullrid()
        ullrid.set_to_v6()

        assert isinstance(ullrid.blade_whirlwind, BladeWhirlwindV1)
        assert isinstance(ullrid.hidden_pursuit, HiddenPursuitV6)

    def test_set_to_fortification_level(self):
        ullrid: Ullrid = Ullrid()
        ullrid.set_fortification_level(FortificationLevel.SEGMENT06)

        assert ullrid.fortification_level == FortificationLevel.SEGMENT06
        assert isinstance(ullrid.blade_whirlwind, BladeWhirlwindV1)
        assert isinstance(ullrid.hidden_pursuit, HiddenPursuitV6)


class TestUllridDamageCalculationStrategy:
    def test_resolve_buffs_v5_applies_hunters_talent_and_optical_camouflage(self):
        attacker: Ullrid = Ullrid()
        attacker.set_fortification_level(FortificationLevel.SEGMENT05)
        attacker.initial_stats.basic_attributes[StatType.CRIT_RATE] = 130

        target: Unit = Unit()
        damage_instance: DamageInstance = DamageInstance(
            label="Blade Whirlwind",
            base_potency=100,
            tags={DamageTag.PHYSICAL, DamageTag.MELEE},
        )

        UllridDamageCalculationStrategy().resolve_buffs(
            attacker=attacker,
            target=target,
            damage_instance=damage_instance,
        )

        assert attacker.multiplicative_modifiers.basic_attributes[StatType.ATTACK] == 20
        assert (
            attacker.additive_modifiers.special_attributes[
                SpecialAttribute.CRITICAL_DAMAGE
            ].get_multiplier(DamageTag.ALL)
            == 9
        )
        assert (
            attacker.additive_modifiers.special_attributes[
                SpecialAttribute.DAMAGE_BOOST
            ].get_multiplier(DamageTag.MELEE)
            == 10
        )

    def test_resolve_buffs_without_crit_overflow_adds_no_crit_damage(self):
        attacker: Ullrid = Ullrid()
        attacker.set_fortification_level(FortificationLevel.SEGMENT00)
        attacker.initial_stats.basic_attributes[StatType.CRIT_RATE] = 100

        target: Unit = Unit()
        damage_instance: DamageInstance = DamageInstance(
            label="Warning Shot",
            base_potency=80,
            tags={DamageTag.PHYSICAL, DamageTag.LIGHT_AMMO},
        )

        UllridDamageCalculationStrategy().resolve_buffs(
            attacker=attacker,
            target=target,
            damage_instance=damage_instance,
        )

        assert (
            attacker.additive_modifiers.special_attributes[
                SpecialAttribute.CRITICAL_DAMAGE
            ].get_multiplier(DamageTag.ALL)
            == 0
        )
        assert attacker.multiplicative_modifiers.basic_attributes[StatType.ATTACK] == 0
