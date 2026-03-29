from core.buffs import Buff
from core.combat import DamageInstance, YooheeDamageCalculationStrategy
from core.dolls.yoohee import *
from core.types import (
    DamageTag,
    FortificationLevel,
    ModifierType,
    SpecialAttribute,
    StatType,
)


class TestYooheeSkills:
    def test_rhythmic_pulse(self):
        rhythmic_pulse: DamageInstance = RhythmicPulse().execute()

        assert rhythmic_pulse.base_potency == 80
        assert DamageTag.BASIC in rhythmic_pulse.tags
        assert DamageTag.TARGETED in rhythmic_pulse.tags
        assert rhythmic_pulse.group_name == "Rhythmic Pulse"
        assert isinstance(
            rhythmic_pulse.damage_calculation_strategy,
            YooheeDamageCalculationStrategy,
        )

    def test_improv_without_extra_confectance(self):
        improv: DamageInstance = Improv().execute(
            confectance_index_spent=2,
            stacks_fantastic_conception=0,
            has_fixed_key_1=True,
        )

        assert improv.base_potency == 120
        assert DamageTag.CONFECTANCE in improv.tags
        assert improv.buffs_before == []
        assert improv.group_name == "Improv"

    def test_improv_with_extra_confectance_and_fixed_key(self):
        improv: DamageInstance = Improv().execute(
            confectance_index_spent=3,
            stacks_fantastic_conception=0,
            has_fixed_key_1=True,
        )

        assert improv.base_potency == 120
        assert improv.buffs_before == [
            Buff(
                value=30,
                modifier_type=ModifierType.ADDITIVE,
                stat_type=SpecialAttribute.DEFENSE_IGNORE,
                tag=DamageTag.ALL,
            ),
            Buff(
                value=5,
                modifier_type=ModifierType.ADDITIVE,
                stat_type=SpecialAttribute.CRITICAL_DAMAGE,
                tag=DamageTag.ALL,
            ),
        ]

    def test_improv_v4_caps_fantastic_conception_stacks(self):
        improv: DamageInstance = ImprovV4().execute(
            confectance_index_spent=3,
            stacks_fantastic_conception=5,
            has_fixed_key_1=True,
        )

        assert improv.base_potency == 180
        assert improv.buffs_before == [
            Buff(
                value=30,
                modifier_type=ModifierType.ADDITIVE,
                stat_type=SpecialAttribute.DEFENSE_IGNORE,
                tag=DamageTag.ALL,
            ),
            Buff(
                value=5,
                modifier_type=ModifierType.ADDITIVE,
                stat_type=SpecialAttribute.CRITICAL_DAMAGE,
                tag=DamageTag.ALL,
            ),
            Buff(
                value=45,
                modifier_type=ModifierType.ADDITIVE,
                stat_type=StatType.CRIT_RATE,
                tag=DamageTag.ALL,
            ),
            Buff(
                value=30,
                modifier_type=ModifierType.ADDITIVE,
                stat_type=SpecialAttribute.DEFENSE_IGNORE,
                tag=DamageTag.ALL,
            ),
        ]

    def test_soul_of_dance(self):
        soul_of_dance: DamageInstance = SoulOfDance().execute()

        assert soul_of_dance.base_potency == 80
        assert DamageTag.AREA_OF_EFFECT in soul_of_dance.tags
        assert soul_of_dance.group_name == "Soul of Dance"

    def test_soul_of_dance_v5(self):
        soul_of_dance: DamageInstance = SoulOfDanceV5().execute()

        assert soul_of_dance.base_potency == 130
        assert DamageTag.AREA_OF_EFFECT in soul_of_dance.tags


class TestYoohee:
    def test_set_to_v0(self):
        yoohee: Yoohee = Yoohee()
        yoohee.set_to_v0()

        assert isinstance(yoohee.rhythmic_pulse, RhythmicPulse)
        assert isinstance(yoohee.improv, Improv)
        assert isinstance(yoohee.soul_of_dance, SoulOfDance)
        assert (
            yoohee.initial_stats.special_attributes[
                SpecialAttribute.DAMAGE_BOOST
            ].get_multiplier(DamageTag.PHYSICAL)
            == 15
        )

    def test_set_to_v4(self):
        yoohee: Yoohee = Yoohee()
        yoohee.set_to_v4()

        assert isinstance(yoohee.improv, ImprovV4)
        assert isinstance(yoohee.soul_of_dance, SoulOfDance)

    def test_set_to_v5(self):
        yoohee: Yoohee = Yoohee()
        yoohee.set_to_v5()

        assert isinstance(yoohee.improv, ImprovV4)
        assert isinstance(yoohee.soul_of_dance, SoulOfDanceV5)

    def test_set_to_v6(self):
        yoohee: Yoohee = Yoohee()
        yoohee.set_to_v6()

        assert isinstance(yoohee.improv, ImprovV4)
        assert isinstance(yoohee.soul_of_dance, SoulOfDanceV5)

    def test_set_to_fortification_level(self):
        yoohee: Yoohee = Yoohee()
        yoohee.set_fortification_level(FortificationLevel.SEGMENT06)

        assert yoohee.fortification_level == FortificationLevel.SEGMENT06
        assert isinstance(yoohee.improv, ImprovV4)
        assert isinstance(yoohee.soul_of_dance, SoulOfDanceV5)
