from pydantic import Field
from typing import override, ClassVar

from core.types import (
    DamageTag,
    ModifierType,
    StatType,
    SpecialAttribute,
    Doll,
    FortificationLevel,
    SummonedUnit,
)
from core.buffs import Buff
from core.combat import DamageInstance, CombatAction, YooheeDamageCalculationStrategy


class RhythmicPulse(CombatAction):
    """Yoohee Basic Attack."""

    @override
    def execute(self) -> DamageInstance:
        label: str = "Rhythmic Pulse"
        base_potency: int = 80
        tags: set[DamageTag] = {
            DamageTag.ACTIVE,
            DamageTag.BASIC,
            DamageTag.MEDIUM_AMMO,
            DamageTag.TARGETED,
            DamageTag.PHYSICAL,
        }

        return DamageInstance(
            label=label,
            base_potency=base_potency,
            tags=tags,
            group_name="Rhythmic Pulse",
            damage_calculation_strategy=YooheeDamageCalculationStrategy(),
        )


class Improv(CombatAction):
    """Yoohee S1."""

    @override
    def execute(
        self,
        confectance_index_spent: int,
        stacks_fantastic_conception: int,
        has_fixed_key_1: bool = True,
    ) -> DamageInstance:
        label: str = "Improv"
        base_potency: int = 120
        tags: set[DamageTag] = {
            DamageTag.ACTIVE,
            DamageTag.CONFECTANCE,
            DamageTag.TARGETED,
            DamageTag.PHYSICAL,
            DamageTag.MEDIUM_AMMO,
        }

        buffs_before: list[Buff] = []

        confectance_index_threshold: int = 3

        if confectance_index_spent >= confectance_index_threshold:
            buffs_before.append(
                Buff(
                    value=30,
                    modifier_type=ModifierType.ADDITIVE,
                    stat_type=SpecialAttribute.DEFENSE_IGNORE,
                    tag=DamageTag.ALL,
                )
            )

            # Fixed Key 1: Effort and Returns
            if has_fixed_key_1:
                buffs_before.append(
                    Buff(
                        value=5,
                        modifier_type=ModifierType.ADDITIVE,
                        stat_type=SpecialAttribute.CRITICAL_DAMAGE,
                        tag=DamageTag.ALL,
                    )
                )

        # Fantastic Conception only at V4+

        return DamageInstance(
            label=label,
            base_potency=base_potency,
            tags=tags,
            group_name="Improv",
            buffs_before=buffs_before,
            damage_calculation_strategy=YooheeDamageCalculationStrategy(),
        )


class ImprovV4(CombatAction):
    """Yoohee S1 (V4)."""

    @override
    def execute(
        self,
        confectance_index_spent: int,
        stacks_fantastic_conception: int,
        has_fixed_key_1: bool = True,
    ) -> DamageInstance:
        label: str = "Improv"
        base_potency: int = 180
        tags: set[DamageTag] = {
            DamageTag.ACTIVE,
            DamageTag.CONFECTANCE,
            DamageTag.TARGETED,
            DamageTag.PHYSICAL,
            DamageTag.MEDIUM_AMMO,
        }

        buffs_before: list[Buff] = []

        confectance_index_threshold: int = 3

        if confectance_index_spent >= confectance_index_threshold:
            buffs_before.append(
                Buff(
                    value=30,
                    modifier_type=ModifierType.ADDITIVE,
                    stat_type=SpecialAttribute.DEFENSE_IGNORE,
                    tag=DamageTag.ALL,
                )
            )

            # Fixed Key 1: Effort and Returns
            if has_fixed_key_1:
                buffs_before.append(
                    Buff(
                        value=5,
                        modifier_type=ModifierType.ADDITIVE,
                        stat_type=SpecialAttribute.CRITICAL_DAMAGE,
                        tag=DamageTag.ALL,
                    )
                )

        critical_rate_per_stack: int = 15
        defense_ignore_per_stack: int = 10
        max_stacks_fantastic_conception: int = 3

        if stacks_fantastic_conception > 0:
            buffs_before.append(
                Buff(
                    value=critical_rate_per_stack
                    * min(stacks_fantastic_conception, max_stacks_fantastic_conception),
                    modifier_type=ModifierType.ADDITIVE,
                    stat_type=StatType.CRIT_RATE,
                    tag=DamageTag.ALL,
                )
            )

            buffs_before.append(
                Buff(
                    value=defense_ignore_per_stack
                    * min(stacks_fantastic_conception, max_stacks_fantastic_conception),
                    modifier_type=ModifierType.ADDITIVE,
                    stat_type=SpecialAttribute.DEFENSE_IGNORE,
                    tag=DamageTag.ALL,
                )
            )

        return DamageInstance(
            label=label,
            base_potency=base_potency,
            tags=tags,
            group_name="Improv",
            buffs_before=buffs_before,
            damage_calculation_strategy=YooheeDamageCalculationStrategy(),
        )


class SoulOfDance(CombatAction):
    """Yoohee S2."""

    @override
    def execute(self) -> DamageInstance:
        label: str = "Soul of Dance"
        base_potency: int = 80
        tags: set[DamageTag] = {
            DamageTag.ACTIVE,
            DamageTag.AREA_OF_EFFECT,
            DamageTag.PHYSICAL,
            DamageTag.MEDIUM_AMMO,
        }

        return DamageInstance(
            label=label,
            base_potency=base_potency,
            tags=tags,
            group_name="Soul of Dance",
            damage_calculation_strategy=YooheeDamageCalculationStrategy(),
        )


class SoulOfDanceV5(CombatAction):
    """Yoohee S2."""

    @override
    def execute(self) -> DamageInstance:
        label: str = "Soul of Dance"
        base_potency: int = 130
        tags: set[DamageTag] = {
            DamageTag.ACTIVE,
            DamageTag.AREA_OF_EFFECT,
            DamageTag.PHYSICAL,
            DamageTag.MEDIUM_AMMO,
        }

        return DamageInstance(
            label=label,
            base_potency=base_potency,
            tags=tags,
            group_name="Soul of Dance",
            damage_calculation_strategy=YooheeDamageCalculationStrategy(),
        )


class Yoohee(Doll):
    """Yoohee."""

    name: str = "Yoohee"
    irrelevant_damage_tags: ClassVar[set[DamageTag]] = set(
        [
            DamageTag.PHASE,
            DamageTag.CORROSION,
            DamageTag.FREEZE,
            DamageTag.HYDRO,
            DamageTag.BURN,
            DamageTag.ELECTRIC,
            DamageTag.LIGHT_AMMO,
            DamageTag.HEAVY_AMMO,
            DamageTag.SHOTGUN_AMMO,
            DamageTag.SUPPORT_ACTION,
            DamageTag.INTERCEPTION,
            DamageTag.COUNTERATTACK,
        ]
    )

    rhythmic_pulse: CombatAction = Field(default_factory=RhythmicPulse)
    improv: CombatAction = Field(default_factory=Improv)
    soul_of_dance: CombatAction = Field(default_factory=SoulOfDance)

    def set_to_v0(self) -> None:
        """Sets Fortification Level to Segment00."""
        self.rhythmic_pulse: CombatAction = RhythmicPulse()
        self.improv: CombatAction = Improv()
        self.soul_of_dance: CombatAction = SoulOfDance()

        # Expansion Key: Flawless Dance Moves
        # At the start of battle, for each physical-element allied unit on the
        # battlefield, Physical damage dealt by all allied units is increased
        # by 3%, up to a maximum of 15%. (Assume 5 allies for max bonus)
        self.initial_stats.special_attributes[
            SpecialAttribute.DAMAGE_BOOST
        ].set_multiplier(DamageTag.PHYSICAL, 15)

    def set_to_v4(self) -> None:
        """Sets Fortification Level to Segment04."""
        self.set_to_v0()

        self.improv: CombatAction = ImprovV4()

    def set_to_v5(self) -> None:
        """Sets Fortification Level to Segment05."""
        self.set_to_v4()

        self.soul_of_dance: CombatAction = SoulOfDanceV5()

    def set_to_v6(self) -> None:
        """Sets Fortification Level to Segment06."""
        self.set_to_v5()

    @override
    def set_fortification_level(self, level: FortificationLevel):
        self.fortification_level = level
        match level:
            case FortificationLevel.SEGMENT00:
                self.set_to_v0()
            case FortificationLevel.SEGMENT01:
                self.set_to_v0()
            case FortificationLevel.SEGMENT02:
                self.set_to_v0()
            case FortificationLevel.SEGMENT03:
                self.set_to_v0()
            case FortificationLevel.SEGMENT04:
                self.set_to_v4()
            case FortificationLevel.SEGMENT05:
                self.set_to_v5()
            case FortificationLevel.SEGMENT06:
                self.set_to_v6()

    def get_sample_data(self) -> list[DamageInstance]:
        """Returns a sample single target rotation."""
        rotation_data: list[DamageInstance] = [
            # Turn 1
            # Best Dancer trigger
            self.improv.execute(
                confectance_index_spent=3,
                stacks_fantastic_conception=0,
                has_fixed_key_1=True,
            ),
            self.improv.execute(
                confectance_index_spent=3,
                stacks_fantastic_conception=0,
                has_fixed_key_1=True,
            ),
            # Turn 2
            self.improv.execute(
                confectance_index_spent=3,
                stacks_fantastic_conception=3,
                has_fixed_key_1=True,
            ),
            # Turn 3
            self.improv.execute(
                confectance_index_spent=3,
                stacks_fantastic_conception=2,
                has_fixed_key_1=True,
            ),
            self.improv.execute(
                confectance_index_spent=3,
                stacks_fantastic_conception=2,
                has_fixed_key_1=True,
            ),
            # Turn 4
            self.improv.execute(
                confectance_index_spent=3,
                stacks_fantastic_conception=3,
                has_fixed_key_1=True,
            ),
            self.improv.execute(
                confectance_index_spent=3,
                stacks_fantastic_conception=3,
                has_fixed_key_1=True,
            ),
            # Turn 5
            self.improv.execute(
                confectance_index_spent=3,
                stacks_fantastic_conception=3,
                has_fixed_key_1=True,
            ),
            # Turn 6
            self.improv.execute(
                confectance_index_spent=3,
                stacks_fantastic_conception=2,
                has_fixed_key_1=True,
            ),
            self.improv.execute(
                confectance_index_spent=3,
                stacks_fantastic_conception=2,
                has_fixed_key_1=True,
            ),
            # Turn 7
            self.improv.execute(
                confectance_index_spent=3,
                stacks_fantastic_conception=3,
                has_fixed_key_1=True,
            ),
            self.improv.execute(
                confectance_index_spent=3,
                stacks_fantastic_conception=3,
                has_fixed_key_1=True,
            ),
        ]

        return rotation_data
