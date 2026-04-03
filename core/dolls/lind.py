from typing import override, ClassVar
from pydantic import Field

from core.types import (
    DamageTag,
    StatType,
    SpecialAttribute,
    ModifierType,
    FortificationLevel,
    Doll,
    SummonedUnit,
)
from core.buffs import Buff, Debuff, DefenseDownII
from core.combat import DamageInstance, CombatAction, LindDamageCalculationStrategy


class RepulsiveShot(CombatAction):
    """Lind Basic Attack."""

    @override
    def execute(self) -> DamageInstance:
        label: str = "Repulsive Shot"
        base_potency: int = 80

        tags: set[DamageTag] = {
            DamageTag.ACTIVE,
            DamageTag.BASIC,
            DamageTag.SHOTGUN_AMMO,
            DamageTag.TARGETED,
            DamageTag.PHYSICAL,
        }

        return DamageInstance(
            label=label,
            base_potency=base_potency,
            tags=tags,
            group_name="Repulsive Shot",
            damage_calculation_strategy=LindDamageCalculationStrategy(),
        )


class RepulsiveShotV2(CombatAction):
    """Lind Basic Attack (V2)."""

    @override
    def execute(self, is_glucose_overload_followup: bool = False) -> DamageInstance:
        label: str = "Repulsive Shot"
        base_potency: int = 80

        tags: set[DamageTag] = {
            DamageTag.ACTIVE,
            DamageTag.BASIC,
            DamageTag.SHOTGUN_AMMO,
            DamageTag.TARGETED,
            DamageTag.PHYSICAL,
        }

        buffs_before: list[Buff] = []
        if is_glucose_overload_followup:
            buffs_before.append(
                Buff(
                    value=15,
                    modifier_type=ModifierType.ADDITIVE,
                    stat_type=SpecialAttribute.DAMAGE_BOOST,
                    tag=DamageTag.ACTIVE,
                )
            )

        return DamageInstance(
            label=label,
            base_potency=base_potency,
            tags=tags,
            group_name="Repulsive Shot",
            buffs_before=buffs_before,
            damage_calculation_strategy=LindDamageCalculationStrategy(),
        )


class AssaultSpray(CombatAction):
    """Lind S1."""

    @override
    def execute(self, number_of_debuffs_on_target: int) -> DamageInstance:
        label: str = "Assault Spray"
        base_potency: int = 100
        tags: set[DamageTag] = {
            DamageTag.ACTIVE,
            DamageTag.CORROSION,
            DamageTag.PHASE,
            DamageTag.AREA_OF_EFFECT,
            DamageTag.SHOTGUN_AMMO,
        }
        damage_boost_per_debuff: int = 5
        maximum_debuffs_for_damage_boost: int = 6

        buffs_before: list[Buff] = []
        buffs_before.append(
            Buff(
                value=damage_boost_per_debuff
                * min(number_of_debuffs_on_target, maximum_debuffs_for_damage_boost),
                modifier_type=ModifierType.ADDITIVE,
                stat_type=SpecialAttribute.DAMAGE_BOOST,
                tag=DamageTag.ALL,
            )
        )

        return DamageInstance(
            label=label,
            base_potency=base_potency,
            tags=tags,
            group_name="Assault Spray",
            buffs_before=buffs_before,
            damage_calculation_strategy=LindDamageCalculationStrategy(),
        )


class AssaultSprayV2(CombatAction):
    """Lind S1 (V2)."""

    @override
    def execute(
        self,
        number_of_debuffs_on_target: int,
        is_glucose_overload_followup: bool = False,
    ) -> DamageInstance:
        label: str = "Assault Spray"
        base_potency: int = 100
        tags: set[DamageTag] = {
            DamageTag.ACTIVE,
            DamageTag.CORROSION,
            DamageTag.PHASE,
            DamageTag.AREA_OF_EFFECT,
            DamageTag.SHOTGUN_AMMO,
        }
        damage_boost_per_debuff: int = 5
        maximum_debuffs_for_damage_boost: int = 6

        buffs_before: list[Buff] = []
        buffs_before.append(
            Buff(
                value=damage_boost_per_debuff
                * min(number_of_debuffs_on_target, maximum_debuffs_for_damage_boost),
                modifier_type=ModifierType.ADDITIVE,
                stat_type=SpecialAttribute.DAMAGE_BOOST,
                tag=DamageTag.ALL,
            )
        )

        if is_glucose_overload_followup:
            buffs_before.append(
                Buff(
                    value=15,
                    modifier_type=ModifierType.ADDITIVE,
                    stat_type=SpecialAttribute.DAMAGE_BOOST,
                    tag=DamageTag.ACTIVE,
                )
            )

        return DamageInstance(
            label=label,
            base_potency=base_potency,
            tags=tags,
            group_name="Assault Spray",
            buffs_before=buffs_before,
            damage_calculation_strategy=LindDamageCalculationStrategy(),
        )


class AssaultSprayV4(CombatAction):
    """Lind S1 (V4)."""

    @override
    def execute(
        self,
        number_of_debuffs_on_target: int,
        is_glucose_overload_followup: bool = False,
    ) -> DamageInstance:
        label: str = "Assault Spray"
        base_potency: int = 100
        tags: set[DamageTag] = {
            DamageTag.ACTIVE,
            DamageTag.CORROSION,
            DamageTag.PHASE,
            DamageTag.AREA_OF_EFFECT,
            DamageTag.SHOTGUN_AMMO,
        }
        damage_boost_per_debuff: int = 10
        maximum_debuffs_for_damage_boost: int = 6

        buffs_before: list[Buff] = []
        buffs_before.append(
            Buff(
                value=damage_boost_per_debuff
                * min(number_of_debuffs_on_target, maximum_debuffs_for_damage_boost),
                modifier_type=ModifierType.ADDITIVE,
                stat_type=SpecialAttribute.DAMAGE_BOOST,
                tag=DamageTag.ALL,
            )
        )

        if is_glucose_overload_followup:
            buffs_before.append(
                Buff(
                    value=15,
                    modifier_type=ModifierType.ADDITIVE,
                    stat_type=SpecialAttribute.DAMAGE_BOOST,
                    tag=DamageTag.ACTIVE,
                )
            )

        return DamageInstance(
            label=label,
            base_potency=base_potency,
            tags=tags,
            group_name="Assault Spray",
            buffs_before=buffs_before,
            damage_calculation_strategy=LindDamageCalculationStrategy(),
        )


class OverwhelmingBurst(CombatAction):
    """Lind S2."""

    @override
    def execute(
        self,
        has_fixed_key_4: bool,
        is_confectance_index_at_maximum: bool,
        stacks_of_candyglaze: int,
    ) -> DamageInstance:
        label: str = f"Overwhelming Burst ({stacks_of_candyglaze})"
        base_potency: int = 100
        tags: set[DamageTag] = {
            DamageTag.ACTIVE,
            DamageTag.CORROSION,
            DamageTag.PHASE,
            DamageTag.SHOTGUN_AMMO,
            DamageTag.CONFECTANCE,
            DamageTag.AREA_OF_EFFECT,
        }

        buffs_before: list[Buff] = []

        if is_confectance_index_at_maximum:
            multiplier_per_stack: int = 5
            max_stacks_of_candyglaze: int = 30
            base_potency += multiplier_per_stack * min(
                stacks_of_candyglaze, max_stacks_of_candyglaze
            )

        # Fixed Key 4 - Civilized Judgement: +30 damage boost for hitting only 1 target
        if has_fixed_key_4:
            buffs_before.append(
                Buff(
                    value=30,
                    modifier_type=ModifierType.ADDITIVE,
                    stat_type=SpecialAttribute.DAMAGE_BOOST,
                    tag=DamageTag.ONLY_HIT_ONE_TARGET,
                )
            )

        return DamageInstance(
            label=label,
            base_potency=base_potency,
            tags=tags,
            group_name="Overwhelming Burst",
            buffs_before=buffs_before,
            damage_calculation_strategy=LindDamageCalculationStrategy(),
        )


class OverwhelmingBurstV2(CombatAction):
    """Lind S2 (V2)."""

    @override
    def execute(
        self,
        has_fixed_key_4: bool,
        is_confectance_index_at_maximum: bool,
        stacks_of_candyglaze: int,
        is_glucose_overload_followup: bool = False,
    ) -> DamageInstance:
        label: str = f"Overwhelming Burst ({stacks_of_candyglaze})"
        base_potency: int = 100
        tags: set[DamageTag] = {
            DamageTag.ACTIVE,
            DamageTag.CORROSION,
            DamageTag.PHASE,
            DamageTag.SHOTGUN_AMMO,
            DamageTag.CONFECTANCE,
            DamageTag.AREA_OF_EFFECT,
        }

        buffs_before: list[Buff] = []

        if is_confectance_index_at_maximum:
            multiplier_per_stack: int = 5
            max_stacks_of_candyglaze: int = 30
            base_potency += multiplier_per_stack * min(
                stacks_of_candyglaze, max_stacks_of_candyglaze
            )

        # Fixed Key 4 - Civilized Judgement: +30 damage boost for hitting only 1 target
        if has_fixed_key_4:
            buffs_before.append(
                Buff(
                    value=30,
                    modifier_type=ModifierType.ADDITIVE,
                    stat_type=SpecialAttribute.DAMAGE_BOOST,
                    tag=DamageTag.ONLY_HIT_ONE_TARGET,
                )
            )

        if is_glucose_overload_followup:
            buffs_before.append(
                Buff(
                    value=15,
                    modifier_type=ModifierType.ADDITIVE,
                    stat_type=SpecialAttribute.DAMAGE_BOOST,
                    tag=DamageTag.ACTIVE,
                )
            )

        return DamageInstance(
            label=label,
            base_potency=base_potency,
            tags=tags,
            group_name="Overwhelming Burst",
            buffs_before=buffs_before,
            damage_calculation_strategy=LindDamageCalculationStrategy(),
        )


class OverwhelmingBurstV5(CombatAction):
    """Lind S2 (V5)."""

    @override
    def execute(
        self,
        has_fixed_key_4: bool,
        is_confectance_index_at_maximum: bool,
        stacks_of_candyglaze: int,
        is_glucose_overload_followup: bool = False,
    ) -> DamageInstance:
        label: str = f"Overwhelming Burst ({stacks_of_candyglaze})"
        base_potency: int = 120
        tags: set[DamageTag] = {
            DamageTag.ACTIVE,
            DamageTag.CORROSION,
            DamageTag.PHASE,
            DamageTag.SHOTGUN_AMMO,
            DamageTag.CONFECTANCE,
            DamageTag.AREA_OF_EFFECT,
        }

        buffs_before: list[Buff] = []

        if is_confectance_index_at_maximum:
            multiplier_per_stack: int = 10
            max_stacks_of_candyglaze: int = 30
            base_potency += multiplier_per_stack * min(
                stacks_of_candyglaze, max_stacks_of_candyglaze
            )

            buffs_before.append(
                Buff(
                    value=20,
                    modifier_type=ModifierType.ADDITIVE,
                    stat_type=StatType.CRIT_DAMAGE,
                    tag=DamageTag.ALL,
                )
            )

        # Fixed Key 4 - Civilized Judgement: +30 damage boost for hitting only 1 target
        if has_fixed_key_4:
            buffs_before.append(
                Buff(
                    value=30,
                    modifier_type=ModifierType.ADDITIVE,
                    stat_type=SpecialAttribute.DAMAGE_BOOST,
                    tag=DamageTag.ONLY_HIT_ONE_TARGET,
                )
            )

        if is_glucose_overload_followup:
            buffs_before.append(
                Buff(
                    value=15,
                    modifier_type=ModifierType.ADDITIVE,
                    stat_type=SpecialAttribute.DAMAGE_BOOST,
                    tag=DamageTag.ACTIVE,
                )
            )

        return DamageInstance(
            label=label,
            base_potency=base_potency,
            tags=tags,
            group_name="Overwhelming Burst",
            buffs_before=buffs_before,
            damage_calculation_strategy=LindDamageCalculationStrategy(),
        )


class Honeytrap(CombatAction):
    """Support Action from Honeytrap debuff."""

    @override
    def execute(self) -> DamageInstance:
        label: str = "Honeytrap"
        base_potency: int = 80

        tags: set[DamageTag] = {
            DamageTag.PASSIVE,
            DamageTag.CORROSION,
            DamageTag.PHASE,
            DamageTag.AREA_OF_EFFECT,
        }

        return DamageInstance(
            label=label,
            base_potency=base_potency,
            tags=tags,
            group_name="Honeytrap",
            damage_calculation_strategy=LindDamageCalculationStrategy(),
        )


class HoneytrapV3(CombatAction):
    """Support Action from Honeytrap debuff (V3)."""

    @override
    def execute(self) -> DamageInstance:
        label: str = "Honeytrap"
        base_potency: int = 120

        tags: set[DamageTag] = {
            DamageTag.PASSIVE,
            DamageTag.CORROSION,
            DamageTag.PHASE,
            DamageTag.AREA_OF_EFFECT,
        }

        return DamageInstance(
            label=label,
            base_potency=base_potency,
            tags=tags,
            group_name="Honeytrap",
            buffs_before=[
                Buff(
                    value=15,
                    modifier_type=ModifierType.ADDITIVE,
                    stat_type=StatType.CRIT_DAMAGE,
                    tag=DamageTag.ALL,
                )
            ],
            damage_calculation_strategy=LindDamageCalculationStrategy(),
        )


class Lind(Doll):
    """Lind."""

    name: str = "Lind"
    irrelevant_damage_tags: ClassVar[set[DamageTag]] = set(
        [
            DamageTag.BURN,
            DamageTag.ELECTRIC,
            DamageTag.HYDRO,
            DamageTag.FREEZE,
            DamageTag.LIGHT_AMMO,
            DamageTag.MEDIUM_AMMO,
            DamageTag.HEAVY_AMMO,
            DamageTag.MELEE,
            DamageTag.INTERCEPTION,
            DamageTag.COUNTERATTACK,
            DamageTag.PHYSICAL_SUMMON,
        ]
    )

    repulsive_shot: CombatAction = Field(default_factory=RepulsiveShot)
    assault_spray: CombatAction = Field(default_factory=AssaultSpray)
    overwhelming_burst: CombatAction = Field(default_factory=OverwhelmingBurst)
    honeytrap: CombatAction = Field(default_factory=Honeytrap)

    def set_to_v0(self) -> None:
        """Sets Fortification Level to Segment00."""
        self.repulsive_shot = RepulsiveShot()
        self.assault_spray = AssaultSpray()
        self.overwhelming_burst = OverwhelmingBurst()
        self.honeytrap = Honeytrap()

    def set_to_v1(self) -> None:
        """Sets Fortification Level to Segment01."""
        self.set_to_v0()

    def set_to_v2(self) -> None:
        """Sets Fortification Level to Segment02."""
        self.set_to_v1()

        self.repulsive_shot: CombatAction = RepulsiveShotV2()
        self.assault_spray: CombatAction = AssaultSprayV2()
        self.overwhelming_burst: CombatAction = OverwhelmingBurstV2()

    def set_to_v3(self) -> None:
        """Sets Fortification Level to Segment03."""
        self.set_to_v2()

        self.honeytrap: CombatAction = HoneytrapV3()

    def set_to_v4(self) -> None:
        """Sets Fortification Level to Segment04."""
        self.set_to_v3()

        self.assault_spray: CombatAction = AssaultSprayV4()

    def set_to_v5(self) -> None:
        """Sets Fortification Level to Segment05."""
        self.set_to_v4()

        self.overwhelming_burst: CombatAction = OverwhelmingBurstV5()

    @override
    def set_fortification_level(self, level: FortificationLevel):
        self.fortification_level = level
        match level:
            case FortificationLevel.SEGMENT00:
                self.set_to_v0()
            case FortificationLevel.SEGMENT01:
                self.set_to_v1()
            case FortificationLevel.SEGMENT02:
                self.set_to_v2()
            case FortificationLevel.SEGMENT03:
                self.set_to_v3()
            case FortificationLevel.SEGMENT04:
                self.set_to_v4()
            case FortificationLevel.SEGMENT05:
                self.set_to_v5()
            case FortificationLevel.SEGMENT06:
                self.set_to_v5()
