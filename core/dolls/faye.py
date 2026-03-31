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
from core.combat import (
    DamageInstance,
    CombatAction,
    FayeDamageCalculationStrategy,
    FixedDamageInstance,
)


class PracticeShot(CombatAction):
    """Faye Basic Attack."""

    @override
    def execute(self) -> DamageInstance:
        label: str = "Practice Shot"
        base_potency: int = 80
        tags: set[DamageTag] = {
            DamageTag.ACTIVE,
            DamageTag.BASIC,
            DamageTag.LIGHT_AMMO,
            DamageTag.TARGETED,
            DamageTag.PHYSICAL,
        }

        return DamageInstance(
            label=label,
            base_potency=base_potency,
            tags=tags,
            group_name="Practice Shot",
        )


class RuinousWhirl(CombatAction):
    """Faye S1."""

    @override
    def execute(self, has_fixed_key_2: bool) -> DamageInstance:
        label: str = "Ruinous Whirl"
        base_potency: int = 80
        tags: set[DamageTag] = {
            DamageTag.ACTIVE,
            DamageTag.MELEE,
            DamageTag.AREA_OF_EFFECT,
            DamageTag.PHYSICAL,
            DamageTag.CONFECTANCE,
        }

        buffs_before: list[Buff] = []

        # Fixed Key 2 - All-In Slash increases damage dealt by 20% if only one target is hit.
        if has_fixed_key_2:
            buffs_before.append(
                Buff(
                    value=20,
                    modifier_type=ModifierType.ADDITIVE,
                    stat_type=SpecialAttribute.DAMAGE_BOOST,
                    tag=DamageTag.ONLY_HIT_ONE_TARGET,
                )
            )

        return DamageInstance(
            label=label,
            base_potency=base_potency,
            tags=tags,
            group_name="Ruinous Whirl",
            buffs_before=buffs_before,
            damage_calculation_strategy=FayeDamageCalculationStrategy(),
        )


class RuinousWhirlV5(CombatAction):
    """Faye S1 (V5)."""

    @override
    def execute(self, has_fixed_key_2: bool) -> DamageInstance:
        label: str = "Ruinous Whirl"
        base_potency: int = 100
        tags: set[DamageTag] = {
            DamageTag.ACTIVE,
            DamageTag.MELEE,
            DamageTag.AREA_OF_EFFECT,
            DamageTag.PHYSICAL,
            DamageTag.CONFECTANCE,
        }

        buffs_before: list[Buff] = []

        # Fixed Key 2 - All-In Slash increases damage dealt by 20% if only one target is hit.
        if has_fixed_key_2:
            buffs_before.append(
                Buff(
                    value=20,
                    modifier_type=ModifierType.ADDITIVE,
                    stat_type=SpecialAttribute.DAMAGE_BOOST,
                    tag=DamageTag.ONLY_HIT_ONE_TARGET,
                )
            )

        return DamageInstance(
            label=label,
            base_potency=base_potency,
            tags=tags,
            group_name="Ruinous Whirl",
            buffs_before=buffs_before,
            damage_calculation_strategy=FayeDamageCalculationStrategy(),
        )


class FissionedFirelight(CombatAction):
    """Faye S2."""

    @override
    def execute(self) -> DamageInstance:
        label: str = "Fissioned Firelight"
        base_potency: int = 120
        tags: set[DamageTag] = {
            DamageTag.ACTIVE,
            DamageTag.TARGETED,
            DamageTag.LIGHT_AMMO,
            DamageTag.PHYSICAL,
        }

        return DamageInstance(
            label=label,
            base_potency=base_potency,
            tags=tags,
            group_name="Fissioned Firelight",
            damage_calculation_strategy=FayeDamageCalculationStrategy(),
        )


class FissionedFirelightV2(CombatAction):
    """Faye S2 (V2)."""

    @override
    def execute(self) -> DamageInstance:
        label: str = "Fissioned Firelight"
        base_potency: int = 140
        tags: set[DamageTag] = {
            DamageTag.ACTIVE,
            DamageTag.TARGETED,
            DamageTag.LIGHT_AMMO,
            DamageTag.PHYSICAL,
        }

        return DamageInstance(
            label=label,
            base_potency=base_potency,
            tags=tags,
            group_name="Fissioned Firelight",
            damage_calculation_strategy=FayeDamageCalculationStrategy(),
        )


class NoSurvivors(CombatAction):
    """Faye Ultimate."""

    @override
    def execute(self, stacks_of_rend: int) -> DamageInstance:
        label: str = "No Survivors"
        base_potency: int = 160
        tags: set[DamageTag] = {
            DamageTag.ACTIVE,
            DamageTag.TARGETED,
            DamageTag.LIGHT_AMMO,
            DamageTag.ULTIMATE,
            DamageTag.PHYSICAL,
        }

        buffs_before: list[Buff] = []

        rend_stacks_threshold: int = 6

        if stacks_of_rend >= rend_stacks_threshold:
            buffs_before.append(
                Buff(
                    value=120,
                    modifier_type=ModifierType.ADDITIVE,
                    stat_type=SpecialAttribute.DAMAGE_BOOST,
                    tag=DamageTag.ALL,
                )
            )

        return DamageInstance(
            label=label,
            base_potency=base_potency,
            tags=tags,
            group_name="No Survivors",
            buffs_before=buffs_before,
            damage_calculation_strategy=FayeDamageCalculationStrategy(),
        )


class NoSurvivorsV6(CombatAction):
    """Faye Ultimate (V6)."""

    @override
    def execute(self, stacks_of_rend: int) -> DamageInstance:
        label: str = "No Survivors"
        base_potency: int = 160
        tags: set[DamageTag] = {
            DamageTag.ACTIVE,
            DamageTag.TARGETED,
            DamageTag.LIGHT_AMMO,
            DamageTag.ULTIMATE,
            DamageTag.PHYSICAL,
        }

        buffs_before: list[Buff] = []

        rend_stacks_threshold: int = 6
        damage_boost_per_stack: int = 20
        crit_rate_per_stack: int = 5
        crit_dmg_per_stack: int = 2

        if stacks_of_rend >= rend_stacks_threshold:
            buffs_before.append(
                Buff(
                    value=stacks_of_rend * damage_boost_per_stack,
                    modifier_type=ModifierType.ADDITIVE,
                    stat_type=SpecialAttribute.DAMAGE_BOOST,
                    tag=DamageTag.ALL,
                )
            )

            buffs_before.append(
                Buff(
                    value=stacks_of_rend * crit_rate_per_stack,
                    modifier_type=ModifierType.ADDITIVE,
                    stat_type=StatType.CRIT_RATE,
                    tag=DamageTag.ALL,
                )
            )

            buffs_before.append(
                Buff(
                    value=stacks_of_rend * crit_dmg_per_stack,
                    modifier_type=ModifierType.ADDITIVE,
                    stat_type=StatType.CRIT_DAMAGE,
                    tag=DamageTag.ALL,
                )
            )

        return DamageInstance(
            label=label,
            base_potency=base_potency,
            tags=tags,
            group_name="No Survivors",
            buffs_before=buffs_before,
            damage_calculation_strategy=FayeDamageCalculationStrategy(),
        )


class Gash(CombatAction):
    """Fixed damage effect from Gash."""

    @override
    def execute(self, stacks_of_gash: int) -> FixedDamageInstance:
        label: str = "Gash (Fixed)"
        potency_per_stack: int = 8

        return FixedDamageInstance(
            base_potency=stacks_of_gash * potency_per_stack,
            label=label,
            group_name="Gash (Fixed)",
        )


class TomahawkThrow(CombatAction):
    """Tomahawk thrown according to Faye's passive Tomahawk Combo."""

    @override
    def execute(self) -> DamageInstance:
        label: str = "Tomahawk Throw"
        base_potency: int = 80
        tags: set[DamageTag] = {
            DamageTag.PASSIVE,
            DamageTag.AREA_OF_EFFECT,
            DamageTag.PHYSICAL,
        }

        return DamageInstance(
            label=label,
            base_potency=base_potency,
            tags=tags,
            group_name="Tomahawk Combo",
            damage_calculation_strategy=FayeDamageCalculationStrategy(),
        )


class AxeWhirl(CombatAction):
    """Axe Whirl according to Faye's passive Tomahawk Combo."""

    @override
    def execute(self) -> DamageInstance:
        label: str = "Axe Whirl"
        base_potency: int = 60
        tags: set[DamageTag] = {
            DamageTag.PASSIVE,
            DamageTag.AREA_OF_EFFECT,
            DamageTag.PHYSICAL,
        }

        return DamageInstance(
            label=label,
            base_potency=base_potency,
            tags=tags,
            group_name="Tomahawk Combo",
            damage_calculation_strategy=FayeDamageCalculationStrategy(),
        )


class AxeWhirlV3(CombatAction):
    """Axe Whirl according to Faye's passive Tomahawk Combo (V3)."""

    @override
    def execute(self) -> DamageInstance:
        label: str = "Axe Whirl"
        base_potency: int = 60
        tags: set[DamageTag] = {
            DamageTag.PASSIVE,
            DamageTag.AREA_OF_EFFECT,
            DamageTag.PHYSICAL,
        }

        return DamageInstance(
            label=label,
            base_potency=base_potency,
            tags=tags,
            group_name="Tomahawk Combo",
            buffs_before=[
                Buff(
                    value=30,
                    modifier_type=ModifierType.ADDITIVE,
                    stat_type=SpecialAttribute.DAMAGE_BOOST,
                    tag=DamageTag.ALL,
                )
            ],
            damage_calculation_strategy=FayeDamageCalculationStrategy(),
        )


class Faye(Doll):
    """Faye."""

    name: str = "Faye"
    irrelevant_damage_tags: ClassVar[set[DamageTag]] = set(
        [
            DamageTag.PHASE,
            DamageTag.CORROSION,
            DamageTag.FREEZE,
            DamageTag.HYDRO,
            DamageTag.BURN,
            DamageTag.ELECTRIC,
            DamageTag.SHOTGUN_AMMO,
            DamageTag.MEDIUM_AMMO,
            DamageTag.HEAVY_AMMO,
            DamageTag.SUPPORT_ACTION,
            DamageTag.INTERCEPTION,
            DamageTag.COUNTERATTACK,
            DamageTag.PHYSICAL_SUMMON,
        ]
    )

    practice_shot: CombatAction = Field(default_factory=PracticeShot)
    ruinous_whirl: CombatAction = Field(default_factory=RuinousWhirl)
    fissioned_firelight: CombatAction = Field(default_factory=FissionedFirelight)
    no_survivors: CombatAction = Field(default_factory=NoSurvivors)
    gash: CombatAction = Field(default_factory=Gash)
    tomahawk_throw: CombatAction = Field(default_factory=TomahawkThrow)
    axe_whirl: CombatAction = Field(default_factory=AxeWhirl)

    def set_to_v0(self) -> None:
        """Sets Fortification Level to Segment00."""
        self.practice_shot = PracticeShot()
        self.ruinous_whirl = RuinousWhirl()
        self.fissioned_firelight = FissionedFirelight()
        self.no_survivors = NoSurvivors()
        self.gash = Gash()
        self.tomahawk_throw = TomahawkThrow()
        self.axe_whirl = AxeWhirl()

    def set_to_v2(self) -> None:
        """Sets Fortification Level to Segment02."""
        self.set_to_v0()

        self.fissioned_firelight = FissionedFirelightV2()

    def set_to_v3(self) -> None:
        """Sets Fortification Level to Segment03."""
        self.set_to_v2()

        self.axe_whirl = AxeWhirlV3()

    def set_to_v5(self) -> None:
        """Sets Fortification Level to Segment05."""
        self.set_to_v3()

        self.ruinous_whirl = RuinousWhirlV5()

    def set_to_v6(self) -> None:
        """Sets Fortification Level to Segment06."""
        self.set_to_v5()

        self.no_survivors = NoSurvivorsV6()

    @override
    def set_fortification_level(self, level: FortificationLevel) -> None:
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
                self.set_to_v3()
            case FortificationLevel.SEGMENT05:
                self.set_to_v5()
            case FortificationLevel.SEGMENT06:
                self.set_to_v6()
