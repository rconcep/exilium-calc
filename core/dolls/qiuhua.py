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
from core.buffs import Buff
from core.combat import DamageInstance, CombatAction, QiuhuaDamageCalculationStrategy


class Trailblaze(CombatAction):
    """Qiuhua Basic Attack."""

    @override
    def execute(self) -> DamageInstance:
        label: str = "Trailblaze"
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
            group_name="Trailblaze",
            damage_calculation_strategy=QiuhuaDamageCalculationStrategy(),
        )


class SearingSizzle(CombatAction):
    """Qiuhua S1."""

    @override
    def execute(
        self, target_is_within_4_tiles: bool, target_has_scorch_mark: bool
    ) -> DamageInstance:
        label: str = "Searing Sizzle"
        base_potency: int = 120
        tags: set[DamageTag] = {
            DamageTag.ACTIVE,
            DamageTag.BURN,
            DamageTag.PHASE,
            DamageTag.TARGETED,
            DamageTag.SHOTGUN_AMMO,
            DamageTag.CONFECTANCE,
        }

        buffs_before: list[Buff] = []

        if target_is_within_4_tiles:
            buffs_before.append(
                Buff(
                    5,
                    ModifierType.ADDITIVE,
                    SpecialAttribute.DAMAGE_BOOST,
                    DamageTag.ALL,
                )
            )

        return DamageInstance(
            label=label,
            base_potency=base_potency,
            tags=tags,
            group_name="Searing Sizzle",
            buffs_before=buffs_before,
            damage_calculation_strategy=QiuhuaDamageCalculationStrategy(),
        )


class SearingSizzleV5(CombatAction):
    """Qiuhua S1 (V5)."""

    @override
    def execute(
        self, target_is_within_4_tiles: bool, target_has_scorch_mark: bool
    ) -> DamageInstance:
        label: str = "Searing Sizzle"
        base_potency: int = 120
        tags: set[DamageTag] = {
            DamageTag.ACTIVE,
            DamageTag.BURN,
            DamageTag.PHASE,
            DamageTag.TARGETED,
            DamageTag.SHOTGUN_AMMO,
            DamageTag.CONFECTANCE,
        }

        buffs_before: list[Buff] = []

        if target_has_scorch_mark:
            buffs_before.append(
                Buff(
                    30,
                    ModifierType.ADDITIVE,
                    SpecialAttribute.DAMAGE_BOOST,
                    DamageTag.ALL,
                )
            )

        if target_is_within_4_tiles:
            buffs_before.append(
                Buff(
                    15,
                    ModifierType.ADDITIVE,
                    SpecialAttribute.DAMAGE_BOOST,
                    DamageTag.ALL,
                )
            )

        return DamageInstance(
            label=label,
            base_potency=base_potency,
            tags=tags,
            group_name="Searing Sizzle",
            buffs_before=buffs_before,
            damage_calculation_strategy=QiuhuaDamageCalculationStrategy(),
        )


class SoaringLeap(CombatAction):
    """Qiuhua S2."""

    @override
    def execute(self) -> DamageInstance:
        label: str = "Soaring Leap"
        base_potency: int = 30
        tags: set[DamageTag] = {
            DamageTag.ACTIVE,
            DamageTag.BURN,
            DamageTag.PHASE,
            DamageTag.LIGHT_AMMO,
            DamageTag.TARGETED,
        }

        return DamageInstance(
            label=label,
            base_potency=base_potency,
            tags=tags,
            group_name="Soaring Leap",
            damage_calculation_strategy=QiuhuaDamageCalculationStrategy(),
        )


class SoaringLeapV4(CombatAction):
    """Qiuhua S2 (V4)."""

    @override
    def execute(self) -> DamageInstance:
        label: str = "Soaring Leap"
        base_potency: int = 80
        tags: set[DamageTag] = {
            DamageTag.ACTIVE,
            DamageTag.BURN,
            DamageTag.PHASE,
            DamageTag.LIGHT_AMMO,
            DamageTag.TARGETED,
        }

        return DamageInstance(
            label=label,
            base_potency=base_potency,
            tags=tags,
            group_name="Soaring Leap",
            damage_calculation_strategy=QiuhuaDamageCalculationStrategy(),
        )


class BoilAndReduce(CombatAction):
    """Qiuhua Ultimate."""

    @override
    def execute(self, confectance_index_spent: int) -> DamageInstance:
        label: str = "Boil and Reduce"
        base_potency: int = 90
        tags: set[DamageTag] = {
            DamageTag.ACTIVE,
            DamageTag.BURN,
            DamageTag.PHASE,
            DamageTag.ULTIMATE,
            DamageTag.AREA_OF_EFFECT,
            DamageTag.CONFECTANCE,
        }

        potency_per_confectance_index: int = 5
        base_potency += potency_per_confectance_index * confectance_index_spent

        return DamageInstance(
            label=label,
            base_potency=base_potency,
            tags=tags,
            group_name="Boil and Reduce",
            damage_calculation_strategy=QiuhuaDamageCalculationStrategy(),
        )


class BoilAndReduceV6(CombatAction):
    """Qiuhua Ultimate."""

    @override
    def execute(self, confectance_index_spent: int) -> DamageInstance:
        label: str = "Boil and Reduce"
        base_potency: int = 90
        tags: set[DamageTag] = {
            DamageTag.ACTIVE,
            DamageTag.BURN,
            DamageTag.PHASE,
            DamageTag.ULTIMATE,
            DamageTag.AREA_OF_EFFECT,
            DamageTag.CONFECTANCE,
        }

        potency_per_confectance_index: int = 5
        base_potency += potency_per_confectance_index * confectance_index_spent

        return DamageInstance(
            label=label,
            base_potency=base_potency,
            tags=tags,
            group_name="Boil and Reduce",
            buffs_before=[
                Buff(
                    15,
                    ModifierType.ADDITIVE,
                    SpecialAttribute.DAMAGE_BOOST,
                    DamageTag.ONLY_HIT_ONE_TARGET,
                )
            ],
            damage_calculation_strategy=QiuhuaDamageCalculationStrategy(),
        )


class ScorchMark(CombatAction):
    """Qiuhua debuff effect applied by Ultimate. Triggers at the end of the holder's turn."""

    @override
    def execute(self, stacks: int) -> DamageInstance:
        label: str = f"Scorch Mark ({stacks} stacks)"
        base_potency: int = 0
        potency_per_stack: int = 7
        maximum_stacks: int = 12
        base_potency += potency_per_stack * min(stacks, maximum_stacks)

        tags: set[DamageTag] = {
            DamageTag.PASSIVE,
            DamageTag.BURN,
            DamageTag.PHASE,
            DamageTag.TARGETED,
        }

        return DamageInstance(
            label=label,
            base_potency=base_potency,
            tags=tags,
            group_name="Scorch Mark",
            damage_calculation_strategy=QiuhuaDamageCalculationStrategy(),
        )


class ScorchMarkV3(CombatAction):
    """Qiuhua debuff effect applied by Ultimate (V3). Triggers at the end of the holder's turn."""

    @override
    def execute(self, stacks: int) -> DamageInstance:
        label: str = f"Scorch Mark ({stacks} stacks)"
        base_potency: int = 0
        potency_per_stack: int = 7
        base_potency += potency_per_stack * stacks

        tags: set[DamageTag] = {
            DamageTag.PASSIVE,
            DamageTag.BURN,
            DamageTag.PHASE,
            DamageTag.TARGETED,
        }

        return DamageInstance(
            label=label,
            base_potency=base_potency,
            tags=tags,
            group_name="Scorch Mark",
            damage_calculation_strategy=QiuhuaDamageCalculationStrategy(),
        )


class ScorchMarkV6(CombatAction):
    """Qiuhua debuff effect applied by Ultimate (V6). Triggers at the end of the holder's turn."""

    @override
    def execute(self, stacks: int) -> DamageInstance:
        label: str = f"Scorch Mark ({stacks} stacks)"
        base_potency: int = 0
        potency_per_stack: int = 10
        base_potency += potency_per_stack * stacks

        tags: set[DamageTag] = {
            DamageTag.PASSIVE,
            DamageTag.BURN,
            DamageTag.PHASE,
            DamageTag.TARGETED,
        }

        return DamageInstance(
            label=label,
            base_potency=base_potency,
            tags=tags,
            group_name="Scorch Mark",
            damage_calculation_strategy=QiuhuaDamageCalculationStrategy(),
        )


class EmergencySupport(CombatAction):
    """Support action when Negative Charge is applied to an enemy."""

    @override
    def execute(self) -> DamageInstance:
        label: str = "Emergency Support"
        base_potency: int = 60

        tags: set[DamageTag] = {
            DamageTag.PASSIVE,
            DamageTag.SUPPORT_ACTION,
            DamageTag.PHASE,
            DamageTag.BURN,
            DamageTag.SHOTGUN_AMMO,
            DamageTag.TARGETED,
        }

        return DamageInstance(
            label=label,
            base_potency=base_potency,
            tags=tags,
            group_name="Emergency Support",
            damage_calculation_strategy=QiuhuaDamageCalculationStrategy(),
        )


class Qiuhua(Doll):
    """Qiuhua."""

    name: str = "Qiuhua"
    irrelevant_damage_tags: ClassVar[set[DamageTag]] = set(
        [
            DamageTag.CORROSION,
            DamageTag.ELECTRIC,
            DamageTag.HYDRO,
            DamageTag.FREEZE,
            DamageTag.MEDIUM_AMMO,
            DamageTag.HEAVY_AMMO,
            DamageTag.MELEE,
            DamageTag.INTERCEPTION,
            DamageTag.COUNTERATTACK,
            DamageTag.PHYSICAL_SUMMON,
        ]
    )

    trailblaze: CombatAction = Field(default_factory=Trailblaze)
    searing_sizzle: CombatAction = Field(
        default_factory=SearingSizzle,
    )
    soaring_leap: CombatAction = Field(
        default_factory=SoaringLeap,
    )
    boil_and_reduce: CombatAction = Field(
        default_factory=BoilAndReduce,
    )
    scorch_mark: CombatAction = Field(
        default_factory=ScorchMark,
    )
    emergency_support: CombatAction = Field(
        default_factory=EmergencySupport,
    )

    def set_to_v0(self) -> None:
        """Sets Fortification Level to Segment00."""
        self.trailblaze: CombatAction = Trailblaze()
        self.searing_sizzle: CombatAction = SearingSizzle()
        self.soaring_leap: CombatAction = SoaringLeap()
        self.boil_and_reduce: CombatAction = BoilAndReduce()
        self.scorch_mark: CombatAction = ScorchMark()
        self.emergency_support: CombatAction = EmergencySupport()

        # Passive: Burn damage dealt is increased by 5% when there are no
        # other allied Dolls within 2 tiles of Qiuhua (assumed)
        self.initial_stats.special_attributes[
            SpecialAttribute.DAMAGE_BOOST
        ].set_multiplier(
            DamageTag.BURN,
            5,
        )

        # Critical hit rate is increased by 30% when dealing Burn damage
        # to targets with Scorch Mark (assumed)
        self.initial_stats.conditional_basic_attributes[
            StatType.CRIT_RATE
        ].set_multiplier(
            DamageTag.BURN,
            30,
        )

    def set_to_v2(self) -> None:
        """Sets Fortification Level to Segment02."""
        self.set_to_v0()

        # Increase burn damage dealt to 15% (no longer conditional on no
        # allies within 2 tiles)
        self.initial_stats.special_attributes[
            SpecialAttribute.DAMAGE_BOOST
        ].set_multiplier(
            DamageTag.BURN,
            15,
        )

    def set_to_v3(self) -> None:
        """Sets Fortification Level to Segment03."""
        self.set_to_v2()

        self.scorch_mark: CombatAction = ScorchMarkV3()

    def set_to_v4(self) -> None:
        """Sets Fortification Level to Segment04."""
        self.set_to_v3()

        self.soaring_leap: CombatAction = SoaringLeapV4()

    def set_to_v5(self) -> None:
        """Sets Fortification Level to Segment05."""
        self.set_to_v4()

        self.searing_sizzle: CombatAction = SearingSizzleV5()

    def set_to_v6(self) -> None:
        """Sets Fortification Level to Segment06."""
        self.set_to_v5()

        self.boil_and_reduce: CombatAction = BoilAndReduceV6()
        self.scorch_mark: CombatAction = ScorchMarkV6()

    @override
    def set_fortification_level(self, level: FortificationLevel):
        self.fortification_level = level
        match level:
            case FortificationLevel.SEGMENT00:
                self.set_to_v0()
            case FortificationLevel.SEGMENT01:
                self.set_to_v0()
            case FortificationLevel.SEGMENT02:
                self.set_to_v2()
            case FortificationLevel.SEGMENT03:
                self.set_to_v3()
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
        ]

        return rotation_data
