from typing import Any, override, ClassVar
from pydantic import Field

from core.types import (
    DamageTag,
    StatType,
    SpecialAttribute,
    ModifierType,
    Doll,
    FortificationLevel,
    SummonedUnit,
    PhysicalSummonedUnit,
)
from core.buffs import Buff
from core.combat import (
    DamageInstance,
    CombatAction,
    SextansDamageCalculationStrategy,
)


MAX_STACKS_OF_RIGOR_SANGUIS: int = 15  # No known cap
POTENCY_PER_STACK_OF_RIGOR_SANGUIS: int = 10


class DreamscapeFinale(CombatAction):
    """Sextans Basic Attack."""

    @override
    def execute(self) -> DamageInstance:
        label: str = "Dreamscape Finale"
        base_potency: int = 80

        tags: set[DamageTag] = {
            DamageTag.ACTIVE,
            DamageTag.BASIC,
            DamageTag.MELEE,
            DamageTag.TARGETED,
            DamageTag.PHYSICAL,
        }

        return DamageInstance(
            label=label,
            base_potency=base_potency,
            tags=tags,
            group_name="Dreamscape Finale",
            damage_calculation_strategy=SextansDamageCalculationStrategy(),
        )


class SanctuaryLauds(CombatAction):
    """Sextans S1."""

    @override
    def execute(self, stacks_of_rigor_sanguis: int) -> DamageInstance:
        label: str = f"Sanctuary Lauds ({stacks_of_rigor_sanguis}x)"
        base_potency: int = 90

        tags: set[DamageTag] = {
            DamageTag.ACTIVE,
            DamageTag.ELECTRIC,
            DamageTag.PHASE,
            DamageTag.MELEE,
            DamageTag.AREA_OF_EFFECT,
        }

        base_potency += (
            min(stacks_of_rigor_sanguis, MAX_STACKS_OF_RIGOR_SANGUIS)
            * POTENCY_PER_STACK_OF_RIGOR_SANGUIS
        )

        return DamageInstance(
            label=label,
            base_potency=base_potency,
            tags=tags,
            group_name="Sanctuary Lauds",
            damage_calculation_strategy=SextansDamageCalculationStrategy(),
        )


class DeathKnell(CombatAction):
    """Sextans S2."""

    @override
    def execute(self, stacks_of_rigor_sanguis: int) -> DamageInstance:
        label: str = f"Death Knell ({stacks_of_rigor_sanguis}x)"
        base_potency: int = 90

        tags: set[DamageTag] = {
            DamageTag.ACTIVE,
            DamageTag.ELECTRIC,
            DamageTag.PHASE,
            DamageTag.MELEE,
            DamageTag.AREA_OF_EFFECT,
        }

        base_potency += (
            min(stacks_of_rigor_sanguis, MAX_STACKS_OF_RIGOR_SANGUIS)
            * POTENCY_PER_STACK_OF_RIGOR_SANGUIS
        )

        return DamageInstance(
            label=label,
            base_potency=base_potency,
            tags=tags,
            group_name="Death Knell",
            damage_calculation_strategy=SextansDamageCalculationStrategy(),
        )


class DeathKnellV5(CombatAction):
    """Sextans S2 (V5)."""

    @override
    def execute(self, stacks_of_rigor_sanguis: int) -> DamageInstance:
        label: str = f"Death Knell ({stacks_of_rigor_sanguis}x)"
        base_potency: int = 120

        tags: set[DamageTag] = {
            DamageTag.ACTIVE,
            DamageTag.ELECTRIC,
            DamageTag.PHASE,
            DamageTag.MELEE,
            DamageTag.AREA_OF_EFFECT,
        }

        base_potency += (
            min(stacks_of_rigor_sanguis, MAX_STACKS_OF_RIGOR_SANGUIS)
            * POTENCY_PER_STACK_OF_RIGOR_SANGUIS
        )

        return DamageInstance(
            label=label,
            base_potency=base_potency,
            tags=tags,
            group_name="Death Knell",
            damage_calculation_strategy=SextansDamageCalculationStrategy(),
        )


class BloodKiss(CombatAction):
    """Additional instance of damage when Death Knell is used on a target afflicted with Blood Kiss."""

    @override
    def execute(self, multiplier_of_death_knell: int) -> DamageInstance:
        label: str = f"Blood Kiss ({multiplier_of_death_knell}%)"
        base_potency: int = multiplier_of_death_knell

        tags: set[DamageTag] = {
            DamageTag.PASSIVE,
            DamageTag.ELECTRIC,
            DamageTag.PHASE,
            DamageTag.MELEE,
        }

        return DamageInstance(
            label=label,
            base_potency=base_potency,
            tags=tags,
            group_name="Blood Kiss",
            damage_calculation_strategy=SextansDamageCalculationStrategy(),
        )


class MidnightVespers(CombatAction):
    """Sextans Ultimate."""

    @override
    def execute(self, stacks_of_rigor_sanguis: int) -> DamageInstance:
        label: str = f"Midnight Vespers ({stacks_of_rigor_sanguis}x)"
        base_potency: int = 120

        tags: set[DamageTag] = {
            DamageTag.ACTIVE,
            DamageTag.ELECTRIC,
            DamageTag.PHASE,
            DamageTag.MELEE,
            DamageTag.AREA_OF_EFFECT,
            DamageTag.ULTIMATE,
        }

        buffs_before: list[Buff] = []

        base_potency += (
            min(stacks_of_rigor_sanguis, MAX_STACKS_OF_RIGOR_SANGUIS)
            * POTENCY_PER_STACK_OF_RIGOR_SANGUIS
        )

        return DamageInstance(
            label=label,
            base_potency=base_potency,
            tags=tags,
            group_name="Midnight Vespers",
            buffs_before=buffs_before,
            damage_calculation_strategy=SextansDamageCalculationStrategy(),
        )


class LaceratingWound(CombatAction):
    """Effect from Lacerating Wound debuff applied from Midnight Vespers.
    When taking damage, if the attacker used a blade, take an additional instance of damage equal to 40% of the original damage.
    Modeled as a separate instance taking in the original damage instance potency and using 40% of it.
    """

    @override
    def execute(self, original_damage_instance_potency: int) -> DamageInstance:
        label: str = f"Lacerating Wound ({original_damage_instance_potency}%)"
        base_potency: int = int(original_damage_instance_potency * 0.4)

        tags: set[DamageTag] = {
            DamageTag.PASSIVE,
            DamageTag.MELEE,
            DamageTag.ELECTRIC,
            DamageTag.PHASE,
        }

        return DamageInstance(
            label=label,
            base_potency=base_potency,
            tags=tags,
            group_name="Lacerating Wound",
        )


class SanguineEmblem(CombatAction):
    """Effect when allied units other than Sextans attacks with a blade; consumes 1 point of Confectance Index."""

    @override
    def execute(
        self, stacks_of_rigor_sanguis: int, previous_triggers_this_round: int
    ) -> DamageInstance:
        label: str = f"Sanguine Emblem ({stacks_of_rigor_sanguis}x)"
        base_potency: int = 60

        tags: set[DamageTag] = {
            DamageTag.PASSIVE,
            DamageTag.ELECTRIC,
            DamageTag.PHASE,
            DamageTag.MELEE,
        }

        # for each stack of Rigor Sanguis, increase the damage multiplier of this effect by 3%
        potency_per_stack_of_rigor_sanguis: int = 3
        base_potency += max(0, stacks_of_rigor_sanguis) * potency_per_stack_of_rigor_sanguis

        # if this effect is triggered multiple times within a round, decrease the damage
        # multiplier of this effect by 20%, down to a minimum of 30%.
        if previous_triggers_this_round > 0:
            reduction_per_trigger: int = 20
            minimum_potency: int = 30
            base_potency = max(
                minimum_potency,
                base_potency - previous_triggers_this_round * reduction_per_trigger,
            )

        return DamageInstance(
            label=label,
            base_potency=base_potency,
            tags=tags,
            group_name="Sanguine Emblem",
        )


class SanguineEmblemV3(CombatAction):
    """Effect when allied units other than Sextans attacks with a blade; consumes 1 point of Confectance Index."""

    @override
    def execute(
        self, stacks_of_rigor_sanguis: int, previous_triggers_this_round: int
    ) -> DamageInstance:
        label: str = f"Sanguine Emblem ({stacks_of_rigor_sanguis}x)"
        base_potency: int = 60

        tags: set[DamageTag] = {
            DamageTag.PASSIVE,
            DamageTag.ELECTRIC,
            DamageTag.PHASE,
            DamageTag.MELEE,
        }

        # for each stack of Rigor Sanguis, increase the damage multiplier of this effect by 3%
        potency_per_stack_of_rigor_sanguis: int = 4
        base_potency += max(0, stacks_of_rigor_sanguis) * potency_per_stack_of_rigor_sanguis

        # if this effect is triggered multiple times within a round, decrease the damage
        # multiplier of this effect by 20%, down to a minimum of 30%.
        if previous_triggers_this_round > 0:
            reduction_per_trigger: int = 20
            minimum_potency: int = 30
            base_potency = max(
                minimum_potency,
                base_potency - previous_triggers_this_round * reduction_per_trigger,
            )

        return DamageInstance(
            label=label,
            base_potency=base_potency,
            tags=tags,
            group_name="Sanguine Emblem",
        )


class SanguineEmblemV6(CombatAction):
    """Effect when allied units other than Sextans attacks with a blade"""

    @override
    def execute(
        self, stacks_of_rigor_sanguis: int, previous_triggers_this_round: int
    ) -> DamageInstance:
        label: str = f"Sanguine Emblem ({stacks_of_rigor_sanguis}x)"
        base_potency: int = 90

        tags: set[DamageTag] = {
            DamageTag.PASSIVE,
            DamageTag.ELECTRIC,
            DamageTag.PHASE,
            DamageTag.MELEE,
        }

        buffs_before: list[Buff] = []

        buffs_before.append(
            Buff(
                30,
                ModifierType.ADDITIVE,
                SpecialAttribute.DEFENSE_IGNORE,
                DamageTag.ALL,
            ),
        )

        # for each stack of Rigor Sanguis, increase the damage multiplier of this effect by 3%
        potency_per_stack_of_rigor_sanguis: int = 4
        base_potency += max(0, stacks_of_rigor_sanguis) * potency_per_stack_of_rigor_sanguis

        # if this effect is triggered multiple times within a round, decrease the damage
        # multiplier of this effect by 20%, down to a minimum of 30%.
        if previous_triggers_this_round > 0:
            reduction_per_trigger: int = 20
            minimum_potency: int = 30
            base_potency = max(
                minimum_potency,
                base_potency - previous_triggers_this_round * reduction_per_trigger,
            )

        return DamageInstance(
            label=label,
            base_potency=base_potency,
            tags=tags,
            group_name="Sanguine Emblem",
            buffs_before=buffs_before,
        )


class Sextans(Doll):
    """Sextans."""

    name: str = "Sextans"
    irrelevant_damage_tags: ClassVar[set[DamageTag]] = set(
        [
            DamageTag.BURN,
            DamageTag.FREEZE,
            DamageTag.HYDRO,
            DamageTag.CORROSION,
            DamageTag.LIGHT_AMMO,
            DamageTag.MEDIUM_AMMO,
            DamageTag.HEAVY_AMMO,
            DamageTag.SHOTGUN_AMMO,
            DamageTag.SUPPORT_ACTION,
            DamageTag.COUNTERATTACK,
            DamageTag.INTERCEPTION,
            DamageTag.FIXED,
            DamageTag.PHYSICAL_SUMMON,
            DamageTag.CONFECTANCE,
        ]
    )

    dreamscape_finale: CombatAction = Field(default_factory=DreamscapeFinale)
    sanctuary_lauds: CombatAction = Field(default_factory=SanctuaryLauds)
    death_knell: CombatAction = Field(default_factory=DeathKnell)
    midnight_vespers: CombatAction = Field(default_factory=MidnightVespers)
    sanguine_emblem: CombatAction = Field(default_factory=SanguineEmblem)
    lacerating_wound: CombatAction = Field(default_factory=LaceratingWound)

    def set_to_v0(self) -> None:
        """Sets Fortification Level to Segment00."""
        self.dreamscape_finale = DreamscapeFinale()
        self.sanctuary_lauds = SanctuaryLauds()
        self.death_knell = DeathKnell()
        self.midnight_vespers = MidnightVespers()
        self.sanguine_emblem = SanguineEmblem()
        self.lacerating_wound = LaceratingWound()

    def set_to_v3(self) -> None:
        """Sets Fortification Level to Segment03."""
        self.set_to_v0()

        self.sanguine_emblem = SanguineEmblemV3()

    def set_to_v5(self) -> None:
        """Sets Fortification Level to Segment05."""
        self.set_to_v3()

        self.death_knell = DeathKnellV5()

    def set_to_v6(self) -> None:
        """Sets Fortification Level to Segment06."""
        self.set_to_v5()

        self.sanguine_emblem = SanguineEmblemV6()

    @override
    def set_fortification_level(self, level: FortificationLevel) -> None:
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
                self.set_to_v3()
            case FortificationLevel.SEGMENT05:
                self.set_to_v5()
            case FortificationLevel.SEGMENT06:
                self.set_to_v6()
