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
from core.buffs import Buff, Debuff
from core.combat import DamageInstance, CombatAction, LoreleyDamageCalculationStrategy


class PunishmentPrelude(CombatAction):
    """Loreley Basic Attack."""

    @override
    def execute(self) -> DamageInstance:
        label: str = "Punishment Prelude"
        base_potency: int = 80

        tags: set[DamageTag] = {
            DamageTag.ACTIVE,
            DamageTag.BASIC,
            DamageTag.HEAVY_AMMO,
            DamageTag.TARGETED,
            DamageTag.PHYSICAL,
        }

        return DamageInstance(
            label=label,
            base_potency=base_potency,
            tags=tags,
            group_name="Punishment Prelude",
            damage_calculation_strategy=LoreleyDamageCalculationStrategy(),
        )


class SearingBrand(CombatAction):
    """Loreley S1."""

    @override
    def execute(
        self, has_glowing_embers: bool, target_on_burn_tile: bool
    ) -> DamageInstance:
        label: str = "Searing Brand"
        base_potency: int = 130
        tags: set[DamageTag] = {
            DamageTag.ACTIVE,
            DamageTag.BURN,
            DamageTag.PHASE,
            DamageTag.TARGETED,
            DamageTag.HEAVY_AMMO,
        }

        # If user has Glowing Embers, double the damage multiplier
        if has_glowing_embers:
            base_potency *= 2

        return DamageInstance(
            label=label,
            base_potency=base_potency,
            tags=tags,
            group_name="Searing Brand",
            damage_calculation_strategy=LoreleyDamageCalculationStrategy(),
        )


class SearingBrandV5(CombatAction):
    """Loreley S1 (V5)."""

    @override
    def execute(
        self, has_glowing_embers: bool, target_on_burn_tile: bool
    ) -> DamageInstance:
        label: str = "Searing Brand"
        base_potency: int = 130
        tags: set[DamageTag] = {
            DamageTag.ACTIVE,
            DamageTag.BURN,
            DamageTag.PHASE,
            DamageTag.TARGETED,
            DamageTag.HEAVY_AMMO,
        }
        buffs_before: list[Buff] = []

        # If user has Glowing Embers, double the damage multiplier
        if has_glowing_embers:
            base_potency *= 2

        # Ignores 30% of defense
        buffs_before.append(
            Buff(
                value=30,
                modifier_type=ModifierType.ADDITIVE,
                stat_type=SpecialAttribute.DEFENSE_IGNORE,
                tag=DamageTag.ALL,
            )
        )

        # If target is on a burn tile, increase damage dealt by 60%
        if target_on_burn_tile:
            buffs_before.append(
                Buff(
                    value=60,
                    modifier_type=ModifierType.ADDITIVE,
                    stat_type=SpecialAttribute.DAMAGE_BOOST,
                    tag=DamageTag.ALL,
                )
            )

        return DamageInstance(
            label=label,
            base_potency=base_potency,
            tags=tags,
            group_name="Searing Brand",
            buffs_before=buffs_before,
            damage_calculation_strategy=LoreleyDamageCalculationStrategy(),
        )


class RedBoundDeclaration(CombatAction):
    """Loreley S2."""

    @override
    def execute(
        self,
        has_glowing_embers: bool,
        number_of_targets: int,
        number_of_burn_buffs: int,
    ) -> DamageInstance:
        label: str = "Red-Bound Declaration"
        base_potency: float = 120
        tags: set[DamageTag] = {
            DamageTag.ACTIVE,
            DamageTag.BURN,
            DamageTag.PHASE,
            DamageTag.AREA_OF_EFFECT,
        }

        # If user has Glowing Embers, the damage is not split
        if not has_glowing_embers and number_of_targets > 1:
            base_potency = base_potency / number_of_targets

        return DamageInstance(
            label=label,
            base_potency=base_potency,
            tags=tags,
            group_name="Red-Bound Declaration",
            damage_calculation_strategy=LoreleyDamageCalculationStrategy(),
        )


class RedBoundDeclarationV4(CombatAction):
    """Loreley S2 (V4)."""

    @override
    def execute(
        self,
        has_glowing_embers: bool,
        number_of_targets: int,
        number_of_burn_buffs: int,
    ) -> DamageInstance:
        label: str = "Red-Bound Declaration"
        base_potency: float = 150
        tags: set[DamageTag] = {
            DamageTag.ACTIVE,
            DamageTag.BURN,
            DamageTag.PHASE,
            DamageTag.AREA_OF_EFFECT,
        }

        buffs_before: list[Buff] = []

        # If user has Glowing Embers, the damage is not split
        if not has_glowing_embers and number_of_targets > 1:
            base_potency = base_potency / number_of_targets

        # Every Burn buff increases damage dealt by 10%, up to a maximum of 40%
        damage_boost_per_buff: int = 10
        burn_buff_bonus = min(number_of_burn_buffs * damage_boost_per_buff, 40)
        buffs_before.append(
            Buff(
                value=burn_buff_bonus,
                modifier_type=ModifierType.ADDITIVE,
                stat_type=SpecialAttribute.DAMAGE_BOOST,
                tag=DamageTag.ALL,
            )
        )

        return DamageInstance(
            label=label,
            base_potency=base_potency,
            tags=tags,
            group_name="Red-Bound Declaration",
            buffs_before=buffs_before,
            damage_calculation_strategy=LoreleyDamageCalculationStrategy(),
        )


class DolorousGrace(CombatAction):
    """Loreley Ultimate."""

    @override
    def execute(self) -> DamageInstance:
        label: str = "Dolorous Grace"
        base_potency: int = 60
        tags: set[DamageTag] = {
            DamageTag.ACTIVE,
            DamageTag.BURN,
            DamageTag.PHASE,
            DamageTag.ULTIMATE,
            DamageTag.AREA_OF_EFFECT,
        }

        return DamageInstance(
            label=label,
            base_potency=base_potency,
            tags=tags,
            group_name="Dolorous Grace",
            damage_calculation_strategy=LoreleyDamageCalculationStrategy(),
        )


class WhippoorwillPulse(CombatAction):
    """Action from Ranger Mk.II triggered by Loreley."""

    @override
    def execute(self) -> DamageInstance:
        label: str = "Whippoorwill Pulse"
        base_potency: int = 40
        tags: set[DamageTag] = {
            DamageTag.PASSIVE,
            DamageTag.BURN,
            DamageTag.PHASE,
            DamageTag.ULTIMATE,
            DamageTag.AREA_OF_EFFECT,
        }

        return DamageInstance(
            label=label,
            base_potency=base_potency,
            tags=tags,
            group_name="Whippoorwill Pulse",
            damage_calculation_strategy=LoreleyDamageCalculationStrategy(),
        )


class WhippoorwillPulseV3(CombatAction):
    """Action from Ranger Mk.II triggered by Loreley."""

    @override
    def execute(self) -> DamageInstance:
        label: str = "Whippoorwill Pulse"
        base_potency: int = 80
        tags: set[DamageTag] = {
            DamageTag.PASSIVE,
            DamageTag.BURN,
            DamageTag.PHASE,
            DamageTag.ULTIMATE,
            DamageTag.AREA_OF_EFFECT,
        }

        return DamageInstance(
            label=label,
            base_potency=base_potency,
            tags=tags,
            group_name="Whippoorwill Pulse",
            damage_calculation_strategy=LoreleyDamageCalculationStrategy(),
        )


class Loreley(Doll):
    """Loreley."""

    name: str = "Loreley"
    irrelevant_damage_tags: ClassVar[set[DamageTag]] = set(
        [
            DamageTag.CORROSION,
            DamageTag.ELECTRIC,
            DamageTag.HYDRO,
            DamageTag.FREEZE,
            DamageTag.MEDIUM_AMMO,
            DamageTag.LIGHT_AMMO,
            DamageTag.SHOTGUN_AMMO,
            DamageTag.MELEE,
            DamageTag.SUPPORT_ACTION,
            DamageTag.INTERCEPTION,
            DamageTag.COUNTERATTACK,
            DamageTag.PHYSICAL_SUMMON,
            DamageTag.FIXED,
        ]
    )

    punishment_prelude: CombatAction = Field(default_factory=PunishmentPrelude)
    searing_brand: CombatAction = Field(default_factory=SearingBrand)
    red_bound_declaration: CombatAction = Field(default_factory=RedBoundDeclaration)
    dolorous_grace: CombatAction = Field(default_factory=DolorousGrace)
    whippoorwill_pulse: CombatAction = Field(default_factory=WhippoorwillPulse)

    def set_to_v0(self) -> None:
        """Sets Fortification Level to Segment00."""
        self.punishment_prelude: CombatAction = PunishmentPrelude()
        self.searing_brand: CombatAction = SearingBrand()
        self.red_bound_declaration: CombatAction = RedBoundDeclaration()
        self.dolorous_grace: CombatAction = DolorousGrace()
        self.whippoorwill_pulse: CombatAction = WhippoorwillPulse()

    def set_to_v3(self) -> None:
        """Sets Fortification Level to Segment03."""
        self.set_to_v0()

        self.whippoorwill_pulse: CombatAction = WhippoorwillPulseV3()

    def set_to_v4(self) -> None:
        """Sets Fortification Level to Segment04."""
        self.set_to_v3()

        self.red_bound_declaration: CombatAction = RedBoundDeclarationV4()

    def set_to_v5(self) -> None:
        """Sets Fortification Level to Segment05."""
        self.set_to_v4()

        self.searing_brand: CombatAction = SearingBrandV5()

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
                self.set_to_v3()
            case FortificationLevel.SEGMENT04:
                self.set_to_v4()
            case FortificationLevel.SEGMENT05:
                self.set_to_v5()
            case FortificationLevel.SEGMENT06:
                self.set_to_v5()
