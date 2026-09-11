from typing import override, ClassVar
from pydantic import Field
from enum import StrEnum

from core.types import (
    DamageTag,
    ModifierType,
    SpecialAttribute,
    Doll,
    FortificationLevel,
    StatType,
    SummonedUnit,
)
from core.buffs import Buff, MAX_TILE_ASCENSION_LEVEL
from core.combat import DamageInstance, CombatAction, SoppoDamageCalculationStrategy


class HuntingFang(CombatAction):
    """Soppo basic attack."""

    @override
    def execute(self, in_feral_form: bool = False) -> DamageInstance:
        label: str = (
            "Hunting Fang (Freeze)" if not in_feral_form else "Hunting Fang (Burn)"
        )
        base_potency: int = 80
        tags: set[DamageTag] = {
            DamageTag.ACTIVE,
            DamageTag.BASIC,
            DamageTag.MEDIUM_AMMO,
            DamageTag.TARGETED,
            DamageTag.FREEZE,
            DamageTag.PHASE,
        }

        # If in Mad Dog Mode, deals Burn damage instead.
        if in_feral_form:
            tags.remove(DamageTag.FREEZE)
            tags.add(DamageTag.BURN)

        return DamageInstance(
            label=label,
            base_potency=base_potency,
            tags=tags,
            group_name="Hunting Fang",
            damage_calculation_strategy=SoppoDamageCalculationStrategy(),
        )


class ViciousBite(CombatAction):
    """Soppo S1."""

    @override
    def execute(self, in_feral_form: bool = False) -> DamageInstance:
        label: str = (
            "Vicious Bite (Freeze)" if not in_feral_form else "Vicious Bite (Burn)"
        )
        base_potency: int = 80
        tags: set[DamageTag] = {
            DamageTag.ACTIVE,
            DamageTag.MEDIUM_AMMO,
            DamageTag.AREA_OF_EFFECT,
            DamageTag.FREEZE,
            DamageTag.PHASE,
        }

        # If in Mad Dog Mode, deals Burn damage instead.
        if in_feral_form:
            tags.remove(DamageTag.FREEZE)
            tags.add(DamageTag.BURN)

        return DamageInstance(
            label=label,
            base_potency=base_potency,
            tags=tags,
            group_name="Vicious Bite",
            damage_calculation_strategy=SoppoDamageCalculationStrategy(),
        )


class ViciousBiteV1(CombatAction):
    """Soppo S1 (V1)."""

    @override
    def execute(self, in_feral_form: bool = False) -> DamageInstance:
        label: str = (
            "Vicious Bite (Freeze)" if not in_feral_form else "Vicious Bite (Burn)"
        )
        base_potency: int = 130
        tags: set[DamageTag] = {
            DamageTag.ACTIVE,
            DamageTag.MEDIUM_AMMO,
            DamageTag.AREA_OF_EFFECT,
            DamageTag.FREEZE,
            DamageTag.PHASE,
        }

        # If in Mad Dog Mode, deals Burn damage instead.
        if in_feral_form:
            tags.remove(DamageTag.FREEZE)
            tags.add(DamageTag.BURN)

        return DamageInstance(
            label=label,
            base_potency=base_potency,
            tags=tags,
            group_name="Vicious Bite",
            damage_calculation_strategy=SoppoDamageCalculationStrategy(),
        )


class LunarHowlTileTargetType(StrEnum):
    """The type of tile Soppo leaps to for Lunar Howl."""

    FROST = "Frost"
    INCINERATION = "Incineration"
    SMOLDERING_SUSPIRE = "Smoldering Suspire"


class LunarHowl(CombatAction):
    """Soppo S2."""

    @override
    def execute(
        self,
        tile_target: LunarHowlTileTargetType,
        in_feral_form: bool = False,
    ) -> DamageInstance:
        label: str = "Lunar Howl"
        base_potency: int = 0
        tags: set[DamageTag] = {
            DamageTag.ACTIVE,
            DamageTag.CONFECTANCE,
            DamageTag.TARGETED,
            DamageTag.PHASE,
        }

        # This component of the skill doesn't exist until the V2 upgrade.

        return DamageInstance(
            label=label,
            base_potency=base_potency,
            tags=tags,
            group_name="Lunar Howl",
            damage_calculation_strategy=SoppoDamageCalculationStrategy(),
        )


class LunarHowlV2(CombatAction):
    """Soppo S2 (V2)."""

    @override
    def execute(
        self, tile_target: LunarHowlTileTargetType, in_feral_form: bool = False
    ) -> DamageInstance:
        label: str = (
            "Lunar Howl (Freeze)"
            if tile_target == LunarHowlTileTargetType.FROST
            else "Lunar Howl (Burn)"
        )
        base_potency: int = 80
        tags: set[DamageTag] = {
            DamageTag.ACTIVE,
            DamageTag.CONFECTANCE,
            DamageTag.TARGETED,
            DamageTag.PHASE,
        }

        # If the tile targeted is a Frost tile, deals Freeze damage. If the tile targeted is an Incineration tile,
        # deals Burn damage. If the tile targeted is a Smoldering Suspire tile, deals both Freeze and Burn damage.
        # (Just create a second damage instance with the other element in this case.)
        match tile_target:
            case LunarHowlTileTargetType.FROST:
                tags.add(DamageTag.FREEZE)
            case LunarHowlTileTargetType.INCINERATION:
                tags.add(DamageTag.BURN)
            case LunarHowlTileTargetType.SMOLDERING_SUSPIRE:
                # Smoldering Suspire applies both elements in-game; model this as two separate
                # action instances (one Frost-targeted and one Incineration-targeted).
                pass

        return DamageInstance(
            label=label,
            base_potency=base_potency,
            tags=tags,
            group_name="Lunar Howl",
            damage_calculation_strategy=SoppoDamageCalculationStrategy(),
        )


class LunarHowlFormSwap(CombatAction):
    """Component of Soppo S2 when Soppo is already in Mad Dog Mode on use."""

    @override
    def execute(
        self,
        in_feral_form: bool = False,
        num_targets: int = 1,
        target_tile_ascension_level: int = 1,
    ) -> DamageInstance:
        label: str = "Lunar Howl (Form Swap)"
        tags: set[DamageTag] = {
            DamageTag.ACTIVE,
            DamageTag.CONFECTANCE,
            DamageTag.AREA_OF_EFFECT,
            DamageTag.BURN,
            DamageTag.PHASE,
        }

        # Only deals damage if Soppo is already in Mad Dog Mode
        # Evenly distributed among all targets within the area.
        base_potency: int = 120 if in_feral_form else 0
        if num_targets > 1:
            base_potency = base_potency // num_targets

        return DamageInstance(
            label=label,
            base_potency=base_potency,
            tags=tags,
            group_name="Lunar Howl (Form Swap)",
            damage_calculation_strategy=SoppoDamageCalculationStrategy(),
        )


class LunarHowlFormSwapV3(CombatAction):
    """Component of Soppo S2 when Soppo is already in Mad Dog Mode on use."""

    @override
    def execute(
        self,
        in_feral_form: bool = False,
        num_targets: int = 1,
        target_tile_ascension_level: int = 1,
    ) -> DamageInstance:
        label: str = "Lunar Howl (Form Swap)"
        tags: set[DamageTag] = {
            DamageTag.ACTIVE,
            DamageTag.CONFECTANCE,
            DamageTag.AREA_OF_EFFECT,
            DamageTag.BURN,
            DamageTag.PHASE,
        }

        # Only deals damage if Soppo is already in Mad Dog Mode
        # Evenly distributed among all targets within the area.
        base_potency: int = 150 if in_feral_form else 0

        # If the target is on a Level 1 tile, damage multiplier is increased by 10% with an additional 10% for each tile ascension.
        bonus_potency_per_tile_ascension_level: int = 10

        if target_tile_ascension_level > 0:
            base_potency += (
                min(MAX_TILE_ASCENSION_LEVEL, target_tile_ascension_level)
                * bonus_potency_per_tile_ascension_level
            )

        if num_targets > 1:
            base_potency = base_potency // num_targets

        return DamageInstance(
            label=label,
            base_potency=base_potency,
            tags=tags,
            group_name="Lunar Howl (Form Swap)",
            damage_calculation_strategy=SoppoDamageCalculationStrategy(),
        )


class FatalPounceActive(CombatAction):
    """Soppo Ultimate (active component)."""

    @override
    def execute(
        self,
        stacks_of_prey_mark: int = 0,
        target_is_on_phase_tile: bool = False,
        confectance_index: int = 4,
    ) -> DamageInstance:
        label: str = f"Fatal Pounce ({stacks_of_prey_mark} Hunting Mark)"
        tags: set[DamageTag] = {
            DamageTag.ACTIVE,
            DamageTag.FREEZE,
            DamageTag.CONFECTANCE,
            DamageTag.PHASE,
            DamageTag.MEDIUM_AMMO,
            DamageTag.AREA_OF_EFFECT,
            DamageTag.ULTIMATE,
        }

        potency_per_prey_mark: int = 30
        base_potency: int = potency_per_prey_mark * stacks_of_prey_mark

        # If the attack hits an enemy on a Phase tile, deals an additional Freeze damage equal to 50% of attack to it.
        # Just add this to the base potency.
        if target_is_on_phase_tile:
            base_potency += 50

        return DamageInstance(
            label=label,
            base_potency=base_potency,
            tags=tags,
            group_name="Fatal Pounce",
        )


class FatalPounceActiveV5(CombatAction):
    """Soppo Ultimate (active component)."""

    @override
    def execute(
        self,
        stacks_of_prey_mark: int = 0,
        target_is_on_phase_tile: bool = False,
        confectance_index: int = 4,
    ) -> DamageInstance:
        label: str = f"Fatal Pounce ({stacks_of_prey_mark} Hunting Mark)"
        tags: set[DamageTag] = {
            DamageTag.ACTIVE,
            DamageTag.FREEZE,
            DamageTag.CONFECTANCE,
            DamageTag.PHASE,
            DamageTag.MEDIUM_AMMO,
            DamageTag.AREA_OF_EFFECT,
            DamageTag.ULTIMATE,
        }

        potency_per_prey_mark: int = 50
        base_potency: int = potency_per_prey_mark * stacks_of_prey_mark

        # If the attack hits an enemy on a Phase tile, deals an additional Freeze damage equal to 50% of attack to it.
        # Just add this to the base potency.
        if target_is_on_phase_tile:
            base_potency += 50

        # Consumes all Confectance Index, increasing damage multiplier by 5% for each
        potency_per_confectance_index: int = 5
        if confectance_index > 0:
            base_potency += confectance_index * potency_per_confectance_index

        return DamageInstance(
            label=label,
            base_potency=base_potency,
            tags=tags,
            group_name="Fatal Pounce",
        )


class FatalPouncePassive(CombatAction):
    """Soppo Ultimate (passive component)."""

    @override
    def execute(self) -> DamageInstance:
        base_potency: int = 30
        label: str = "Fatal Pounce (Passive)"
        tags: set[DamageTag] = {
            DamageTag.PASSIVE,
            DamageTag.FREEZE,
            DamageTag.PHASE,
            DamageTag.MEDIUM_AMMO,
            DamageTag.TARGETED,
            DamageTag.INTERCEPTION,
        }

        return DamageInstance(
            label=label,
            base_potency=base_potency,
            tags=tags,
            group_name="Fatal Pounce (passive)",
        )


class FatalPouncePassiveV5(CombatAction):
    """Soppo Ultimate (passive component)."""

    @override
    def execute(self) -> DamageInstance:
        base_potency: int = 60
        label: str = "Fatal Pounce (Passive)"
        tags: set[DamageTag] = {
            DamageTag.PASSIVE,
            DamageTag.FREEZE,
            DamageTag.PHASE,
            DamageTag.MEDIUM_AMMO,
            DamageTag.TARGETED,
            DamageTag.INTERCEPTION,
        }

        return DamageInstance(
            label=label,
            base_potency=base_potency,
            tags=tags,
            group_name="Fatal Pounce (passive)",
        )


class Soppo(Doll):
    """Soppo."""

    name: str = "Soppo"
    irrelevant_damage_tags: ClassVar[set[DamageTag]] = set(
        [
            DamageTag.PHYSICAL,
            DamageTag.CORROSION,
            DamageTag.HYDRO,
            DamageTag.ELECTRIC,
            DamageTag.MELEE,
            DamageTag.LIGHT_AMMO,
            DamageTag.HEAVY_AMMO,
            DamageTag.SHOTGUN_AMMO,
            DamageTag.SUPPORT_ACTION,
            DamageTag.COUNTERATTACK,
            DamageTag.FIXED,
            DamageTag.PHYSICAL_SUMMON,
        ]
    )

    hunting_fang: CombatAction = Field(default_factory=HuntingFang)
    vicious_bite: CombatAction = Field(default_factory=ViciousBite)
    lunar_howl: CombatAction = Field(default_factory=LunarHowl)
    lunar_howl_form_swap: CombatAction = Field(default_factory=LunarHowlFormSwap)
    fatal_pounce_active: CombatAction = Field(default_factory=FatalPounceActive)
    fatal_pounce_passive: CombatAction = Field(default_factory=FatalPouncePassive)

    def set_to_v0(self) -> None:
        """Sets Fortification Level to Segment00."""
        self.hunting_fang = HuntingFang()
        self.vicious_bite = ViciousBite()
        self.lunar_howl = LunarHowl()
        self.lunar_howl_form_swap = LunarHowlFormSwap()
        self.fatal_pounce_active = FatalPounceActive()
        self.fatal_pounce_passive = FatalPouncePassive()

    def set_to_v1(self) -> None:
        """Sets Fortification Level to Segment01."""
        self.set_to_v0()

        self.vicious_bite: CombatAction = ViciousBiteV1()

    def set_to_v2(self) -> None:
        """Sets Fortification Level to Segment02."""
        self.set_to_v1()

        self.lunar_howl: CombatAction = LunarHowlV2()

    def set_to_v3(self) -> None:
        """Sets Fortification Level to Segment03."""
        self.set_to_v2()

        self.lunar_howl_form_swap: CombatAction = LunarHowlFormSwapV3()

    def set_to_v5(self) -> None:
        """Sets Fortification Level to Segment05."""
        self.set_to_v3()

        self.fatal_pounce_active: CombatAction = FatalPounceActiveV5()
        self.fatal_pounce_passive: CombatAction = FatalPouncePassiveV5()

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
                self.set_to_v3()
            case FortificationLevel.SEGMENT05:
                self.set_to_v5()
            case FortificationLevel.SEGMENT06:
                self.set_to_v5()
