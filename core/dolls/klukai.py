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
from core.combat import DamageInstance, CombatAction, KlukaiDamageCalculationStrategy


class SwiftStrike(CombatAction):
    """Klukai Basic Attack."""

    @override
    def execute(self) -> DamageInstance:
        label: str = "Swift Strike"
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
            group_name="Swift Strike",
            damage_calculation_strategy=KlukaiDamageCalculationStrategy(),
        )


class PinpointDetonationFirst(CombatAction):
    """Klukai S1 (first hit)."""

    @override
    def execute(self) -> DamageInstance:
        label: str = "Pinpoint Detonation"
        base_potency: int = 80
        tags: set[DamageTag] = {
            DamageTag.ACTIVE,
            DamageTag.CORROSION,
            DamageTag.PHASE,
            DamageTag.AREA_OF_EFFECT,
            DamageTag.MEDIUM_AMMO,
            DamageTag.CONFECTANCE,
        }

        return DamageInstance(
            label=label,
            base_potency=base_potency,
            tags=tags,
            group_name="Pinpoint Detonation",
            damage_calculation_strategy=KlukaiDamageCalculationStrategy(),
        )


class PinpointDetonationFirstV4(CombatAction):
    """Klukai S1 (first hit, V4)."""

    @override
    def execute(self) -> DamageInstance:
        label: str = "Pinpoint Detonation"
        base_potency: int = 100
        tags: set[DamageTag] = {
            DamageTag.ACTIVE,
            DamageTag.CORROSION,
            DamageTag.PHASE,
            DamageTag.AREA_OF_EFFECT,
            DamageTag.MEDIUM_AMMO,
            DamageTag.CONFECTANCE,
        }

        return DamageInstance(
            label=label,
            base_potency=base_potency,
            tags=tags,
            group_name="Pinpoint Detonation",
            damage_calculation_strategy=KlukaiDamageCalculationStrategy(),
        )


class PinpointDetonationSecond(CombatAction):
    """Klukai S1 (second hit)."""

    @override
    def execute(self, stacks_corrosion_infusion: int) -> DamageInstance:
        label: str = "Pinpoint Detonation (2nd)"
        base_potency: int = 60
        tags: set[DamageTag] = {
            DamageTag.ACTIVE,
            DamageTag.CORROSION,
            DamageTag.PHASE,
            DamageTag.AREA_OF_EFFECT,
            DamageTag.MEDIUM_AMMO,
            DamageTag.CONFECTANCE,
        }

        return DamageInstance(
            label=label,
            base_potency=base_potency,
            tags=tags,
            group_name="Pinpoint Detonation",
            damage_calculation_strategy=KlukaiDamageCalculationStrategy(),
        )


class PinpointDetonationSecondV4(CombatAction):
    """Klukai S1 (second hit, V4)."""

    @override
    def execute(self, stacks_corrosion_infusion: int) -> DamageInstance:
        label: str = "Pinpoint Detonation (2nd)"
        base_potency: int = 60
        tags: set[DamageTag] = {
            DamageTag.ACTIVE,
            DamageTag.CORROSION,
            DamageTag.PHASE,
            DamageTag.AREA_OF_EFFECT,
            DamageTag.MEDIUM_AMMO,
            DamageTag.CONFECTANCE,
        }

        multiplier_per_stack: int = 5
        base_potency += multiplier_per_stack * stacks_corrosion_infusion

        return DamageInstance(
            label=label,
            base_potency=base_potency,
            tags=tags,
            group_name="Pinpoint Detonation",
            damage_calculation_strategy=KlukaiDamageCalculationStrategy(),
        )


class OverpoweringCorrosion(CombatAction):
    """Klukai S2."""

    @override
    def execute(self, target_has_toxic_infiltration: bool) -> DamageInstance:
        label: str = "Overpowering Corrosion"
        base_potency: int = 90
        tags: set[DamageTag] = {
            DamageTag.ACTIVE,
            DamageTag.CORROSION,
            DamageTag.PHASE,
            DamageTag.AREA_OF_EFFECT,
        }

        buffs_before: list[Buff] = []

        if target_has_toxic_infiltration:
            buffs_before.append(
                Buff(
                    value=15,
                    modifier_type=ModifierType.ADDITIVE,
                    stat_type=SpecialAttribute.DAMAGE_BOOST,
                    tag=DamageTag.ALL,
                )
            )

        return DamageInstance(
            label=label,
            base_potency=base_potency,
            tags=tags,
            group_name="Overpowering Corrosion",
            buffs_before=buffs_before,
            damage_calculation_strategy=KlukaiDamageCalculationStrategy(),
        )


class OverpoweringCorrosionV1(CombatAction):
    """Klukai S2, V1."""

    @override
    def execute(self, target_has_toxic_infiltration: bool) -> DamageInstance:
        label: str = "Overpowering Corrosion"
        base_potency: int = 90
        tags: set[DamageTag] = {
            DamageTag.ACTIVE,
            DamageTag.CORROSION,
            DamageTag.PHASE,
            DamageTag.AREA_OF_EFFECT,
        }

        buffs_before: list[Buff] = []

        if target_has_toxic_infiltration:
            buffs_before.append(
                Buff(
                    value=30,
                    modifier_type=ModifierType.ADDITIVE,
                    stat_type=SpecialAttribute.DAMAGE_BOOST,
                    tag=DamageTag.ALL,
                )
            )

        return DamageInstance(
            label=label,
            base_potency=base_potency,
            tags=tags,
            group_name="Overpowering Corrosion",
            buffs_before=buffs_before,
            damage_calculation_strategy=KlukaiDamageCalculationStrategy(),
        )


class OverpoweringCorrosionV5(CombatAction):
    """Klukai S2, V5."""

    @override
    def execute(self, target_has_toxic_infiltration: bool) -> DamageInstance:
        label: str = "Overpowering Corrosion"
        base_potency: int = 110
        tags: set[DamageTag] = {
            DamageTag.ACTIVE,
            DamageTag.CORROSION,
            DamageTag.PHASE,
            DamageTag.AREA_OF_EFFECT,
        }

        buffs_before: list[Buff] = []

        if target_has_toxic_infiltration:
            buffs_before.append(
                Buff(
                    value=30,
                    modifier_type=ModifierType.ADDITIVE,
                    stat_type=SpecialAttribute.DAMAGE_BOOST,
                    tag=DamageTag.ALL,
                )
            )

        return DamageInstance(
            label=label,
            base_potency=base_potency,
            tags=tags,
            group_name="Overpowering Corrosion",
            buffs_before=buffs_before,
            damage_calculation_strategy=KlukaiDamageCalculationStrategy(),
        )


class DevastatingDrift(CombatAction):
    """Klukai Ultimate."""

    @override
    def execute(
        self,
        number_targets_hit: int,
        target_is_boss: bool,
        has_fixed_key_2: bool,
        has_fixed_key_5: bool,
    ) -> DamageInstance:
        label: str = "Devastating Drift"
        base_potency: int = 100
        tags: set[DamageTag] = {
            DamageTag.ACTIVE,
            DamageTag.CORROSION,
            DamageTag.PHASE,
            DamageTag.ULTIMATE,
            DamageTag.AREA_OF_EFFECT,
        }

        buffs_before: list[Buff] = []

        if has_fixed_key_2:
            buffs_before.append(
                Buff(
                    value=30,
                    modifier_type=ModifierType.ADDITIVE,
                    stat_type=SpecialAttribute.DAMAGE_BOOST,
                    tag=DamageTag.ONLY_HIT_ONE_TARGET,
                )
            )

        # Increase damage dealt by 10% per tile of AOE reduced. At this level, this is 5->3 => 2 tiles reduced => 20% damage boost
        if has_fixed_key_5:
            buffs_before.append(
                Buff(
                    value=20,
                    modifier_type=ModifierType.ADDITIVE,
                    stat_type=SpecialAttribute.DAMAGE_BOOST,
                    tag=DamageTag.ALL,
                )
            )

        return DamageInstance(
            label=label,
            base_potency=base_potency,
            tags=tags,
            group_name="Devastating Drift",
            buffs_before=buffs_before,
            damage_calculation_strategy=KlukaiDamageCalculationStrategy(),
        )


class DevastatingDriftV3(CombatAction):
    """Klukai Ultimate (V3)."""

    @override
    def execute(
        self,
        number_targets_hit: int,
        target_is_boss: bool,
        has_fixed_key_2: bool,
        has_fixed_key_5: bool,
    ) -> DamageInstance:
        label: str = "Devastating Drift"
        base_potency: int = 100
        tags: set[DamageTag] = {
            DamageTag.ACTIVE,
            DamageTag.CORROSION,
            DamageTag.PHASE,
            DamageTag.ULTIMATE,
            DamageTag.AREA_OF_EFFECT,
        }

        buffs_before: list[Buff] = []
        debuffs_before: list[Debuff] = []

        # If the Ultimate skill hits only 1 target, increases damage dealt by 30%.
        if has_fixed_key_2:
            buffs_before.append(
                Buff(
                    value=30,
                    modifier_type=ModifierType.ADDITIVE,
                    stat_type=SpecialAttribute.DAMAGE_BOOST,
                    tag=DamageTag.ONLY_HIT_ONE_TARGET,
                )
            )

        # Increase damage dealt by 10% per tile of AOE reduced. At this level, this is 5->3 => 2 tiles reduced => 20% damage boost
        if has_fixed_key_5:
            buffs_before.append(
                Buff(
                    value=20,
                    modifier_type=ModifierType.ADDITIVE,
                    stat_type=SpecialAttribute.DAMAGE_BOOST,
                    tag=DamageTag.ALL,
                )
            )

        # For each enemy hit, increases damage dealt by an additional 10%, up to a maximum of 50%.
        # If a Boss is hit, this increase will be immediately raised to the maximum value of 50%.
        damage_boost_per_target_hit: int = 10
        maximum_targets_for_damage_boost: int = 5

        if target_is_boss:
            boost_from_targets_hit: int = 50
        else:
            boost_from_targets_hit = damage_boost_per_target_hit * min(
                number_targets_hit, maximum_targets_for_damage_boost
            )

        buffs_before.append(
            Buff(
                value=boost_from_targets_hit,
                modifier_type=ModifierType.ADDITIVE,
                stat_type=SpecialAttribute.DAMAGE_BOOST,
                tag=DamageTag.ALL,
            )
        )

        # Before attacking, applies Defense Down II and Toxic Infiltration
        debuffs_before.append(DefenseDownII())
        debuffs_before.append(
            Debuff(
                value=30,
                modifier_type=ModifierType.ADDITIVE,
                stat_type=SpecialAttribute.INCREASE_DAMAGE_TAKEN,
                tag=DamageTag.ACTIVE,
            )
        )

        return DamageInstance(
            label=label,
            base_potency=base_potency,
            tags=tags,
            group_name="Devastating Drift",
            buffs_before=buffs_before,
            debuffs_before=debuffs_before,
            damage_calculation_strategy=KlukaiDamageCalculationStrategy(),
        )


class DevastatingDriftV6(CombatAction):
    """Klukai Ultimate (V6)."""

    @override
    def execute(
        self,
        number_targets_hit: int,
        target_is_boss: bool,
        has_fixed_key_2: bool,
        has_fixed_key_5: bool,
    ) -> DamageInstance:
        label: str = "Devastating Drift"
        base_potency: int = 100
        tags: set[DamageTag] = {
            DamageTag.ACTIVE,
            DamageTag.CORROSION,
            DamageTag.PHASE,
            DamageTag.ULTIMATE,
            DamageTag.AREA_OF_EFFECT,
        }

        buffs_before: list[Buff] = []
        debuffs_before: list[Debuff] = []

        # If the Ultimate skill hits only 1 target, increases damage dealt by 30%.
        if has_fixed_key_2:
            buffs_before.append(
                Buff(
                    value=30,
                    modifier_type=ModifierType.ADDITIVE,
                    stat_type=SpecialAttribute.DAMAGE_BOOST,
                    tag=DamageTag.ONLY_HIT_ONE_TARGET,
                )
            )

        # Increase damage dealt by 10% per tile of AOE reduced. At this level, this is 7->3 => 4 tiles reduced => 40% damage boost
        if has_fixed_key_5:
            buffs_before.append(
                Buff(
                    value=40,
                    modifier_type=ModifierType.ADDITIVE,
                    stat_type=SpecialAttribute.DAMAGE_BOOST,
                    tag=DamageTag.ALL,
                )
            )

        # For each enemy hit, increases damage dealt by an additional 10%, up to a maximum of 50%.
        # If a Boss is hit, this increase will be immediately raised to the maximum value of 50%.
        damage_boost_per_target_hit: int = 10
        maximum_targets_for_damage_boost: int = 5

        if target_is_boss:
            boost_from_targets_hit: int = 50
        else:
            boost_from_targets_hit = damage_boost_per_target_hit * min(
                number_targets_hit, maximum_targets_for_damage_boost
            )

        buffs_before.append(
            Buff(
                value=boost_from_targets_hit,
                modifier_type=ModifierType.ADDITIVE,
                stat_type=SpecialAttribute.DAMAGE_BOOST,
                tag=DamageTag.ALL,
            )
        )

        # Before attacking, applies Defense Down II and Toxic Infiltration
        debuffs_before.append(DefenseDownII())

        return DamageInstance(
            label=label,
            base_potency=base_potency,
            tags=tags,
            group_name="Devastating Drift",
            buffs_before=buffs_before,
            debuffs_before=debuffs_before,
            damage_calculation_strategy=KlukaiDamageCalculationStrategy(),
        )


class CorrosiveInfusion(CombatAction):
    """Stacking debuff effect applied by Klukai. Triggers at the end of the holder's turn."""

    @override
    def execute(self, stacks: int) -> DamageInstance:
        label: str = f"Corrosive Infusion ({stacks} stacks)"
        base_potency: int = 0
        potency_per_stack: int = 12
        maximum_stacks: int = 10
        base_potency += potency_per_stack * min(stacks, maximum_stacks)

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
            group_name="Corrosive Infusion",
            damage_calculation_strategy=KlukaiDamageCalculationStrategy(),
        )


class CorrosiveInfusionV2(CombatAction):
    """Stacking debuff effect applied by Klukai. Triggers at the end of the holder's turn."""

    @override
    def execute(self, stacks: int) -> DamageInstance:
        label: str = f"Corrosive Infusion ({stacks} stacks)"
        base_potency: int = 0
        potency_per_stack: int = 12
        defense_down_per_stack: int = -1
        maximum_stacks: int = 15
        base_potency += potency_per_stack * min(stacks, maximum_stacks)

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
            group_name="Corrosive Infusion",
            debuffs_before=[
                Debuff(
                    value=defense_down_per_stack * min(stacks, maximum_stacks),
                    modifier_type=ModifierType.MULTIPLICATIVE,
                    stat_type=StatType.DEFENSE,
                    tag=DamageTag.ALL,
                )
            ],
            damage_calculation_strategy=KlukaiDamageCalculationStrategy(),
        )


class ToxicInfiltration(CombatAction):
    """Debuff effect applied by Klukai. Triggers at the end of the holder's turn and on death.
    Damage is the "on-death" effect (which can be triggered).
    """

    @override
    def execute(self) -> DamageInstance:
        label: str = "Toxic Infiltration"
        base_potency: int = 60

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
            group_name="Toxic Infiltration",
            damage_calculation_strategy=KlukaiDamageCalculationStrategy(),
        )


class ToxicInfiltrationV1(CombatAction):
    """Debuff effect applied by Klukai. Triggers at the end of the holder's turn and on death.
    Damage is the "on-death" effect (which can be triggered).
    """

    @override
    def execute(self) -> DamageInstance:
        label: str = "Toxic Infiltration"
        base_potency: int = 60

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
            group_name="Toxic Infiltration",
            damage_calculation_strategy=KlukaiDamageCalculationStrategy(),
        )


class ToxicInfiltrationV5(CombatAction):
    """Debuff effect applied by Klukai. Triggers at the end of the holder's turn and on death.
    Damage is the "on-death" effect (which can be triggered).
    """

    @override
    def execute(self) -> DamageInstance:
        label: str = "Toxic Infiltration"
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
            group_name="Toxic Infiltration",
            damage_calculation_strategy=KlukaiDamageCalculationStrategy(),
        )


class Klukai(Doll):
    """Klukai."""

    name: str = "Klukai"
    irrelevant_damage_tags: ClassVar[set[DamageTag]] = set(
        [
            DamageTag.BURN,
            DamageTag.ELECTRIC,
            DamageTag.HYDRO,
            DamageTag.FREEZE,
            DamageTag.LIGHT_AMMO,
            DamageTag.SHOTGUN_AMMO,
            DamageTag.HEAVY_AMMO,
            DamageTag.MELEE,
            DamageTag.INTERCEPTION,
            DamageTag.COUNTERATTACK,
            DamageTag.PHYSICAL_SUMMON,
        ]
    )

    swift_strike: CombatAction = Field(default_factory=SwiftStrike)
    pinpoint_detonation_first: CombatAction = Field(
        default_factory=PinpointDetonationFirst
    )
    pinpoint_detonation_second: CombatAction = Field(
        default_factory=PinpointDetonationSecond
    )
    overpowering_corrosion: CombatAction = Field(default_factory=OverpoweringCorrosion)
    devastating_drift: CombatAction = Field(default_factory=DevastatingDrift)
    corrosive_infusion: CombatAction = Field(default_factory=CorrosiveInfusion)
    toxic_infiltration: CombatAction = Field(default_factory=ToxicInfiltration)

    def set_to_v0(self) -> None:
        """Sets Fortification Level to Segment00."""
        self.swift_strike: CombatAction = SwiftStrike()
        self.pinpoint_detonation_first: CombatAction = PinpointDetonationFirst()
        self.pinpoint_detonation_second: CombatAction = PinpointDetonationSecond()
        self.overpowering_corrosion: CombatAction = OverpoweringCorrosion()
        self.devastating_drift: CombatAction = DevastatingDrift()
        self.corrosive_infusion: CombatAction = CorrosiveInfusion()
        self.toxic_infiltration: CombatAction = ToxicInfiltration()

    def set_to_v1(self) -> None:
        """Sets Fortification Level to Segment01."""
        self.set_to_v0()

        self.overpowering_corrosion: CombatAction = OverpoweringCorrosionV1()
        self.toxic_infiltration: CombatAction = ToxicInfiltrationV1()

    def set_to_v2(self) -> None:
        """Sets Fortification Level to Segment02."""
        self.set_to_v1()

        self.corrosive_infusion: CombatAction = CorrosiveInfusionV2()

    def set_to_v3(self) -> None:
        """Sets Fortification Level to Segment03."""
        self.set_to_v2()

        self.devastating_drift: CombatAction = DevastatingDriftV3()

    def set_to_v4(self) -> None:
        """Sets Fortification Level to Segment04."""
        self.set_to_v3()

        self.pinpoint_detonation_first: CombatAction = PinpointDetonationFirstV4()
        self.pinpoint_detonation_second: CombatAction = PinpointDetonationSecondV4()

    def set_to_v5(self) -> None:
        """Sets Fortification Level to Segment05."""
        self.set_to_v4()

        self.overpowering_corrosion: CombatAction = OverpoweringCorrosionV5()
        self.toxic_infiltration: CombatAction = ToxicInfiltrationV5()

    def set_to_v6(self) -> None:
        """Sets Fortification Level to Segment06."""
        self.set_to_v5()

        self.devastating_drift: CombatAction = DevastatingDriftV6()

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
                self.set_to_v6()
