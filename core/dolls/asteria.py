from typing import override, ClassVar
from pydantic import Field

from core.types import (
    DamageTag,
    ModifierType,
    SpecialAttribute,
    Doll,
    FortificationLevel,
    StatType,
    SummonedUnit,
)
from core.buffs import Buff
from core.combat import DamageInstance, CombatAction


class SilentTrigger(CombatAction):
    """Asteria basic attack."""

    @override
    def execute(self) -> DamageInstance:
        label: str = "Silent Trigger"
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
            group_name="Silent Trigger",
        )


class DemolitionReckoning(CombatAction):
    """Asteria S2."""

    @override
    def execute(self) -> DamageInstance:
        label: str = "Demolition Reckoning"
        base_potency: int = 80
        tags: set[DamageTag] = {
            DamageTag.ACTIVE,
            DamageTag.MEDIUM_AMMO,
            DamageTag.AREA_OF_EFFECT,
            DamageTag.CONFECTANCE,
            DamageTag.PHYSICAL,
        }

        return DamageInstance(
            label=label,
            base_potency=base_potency,
            tags=tags,
            group_name="Demolition Reckoning",
        )


class RailgunJudgement(CombatAction):
    """Asteria Ultimate."""

    @override
    def execute(
        self,
        has_fixed_key_6: bool,
        stacks_of_absolution: int,
    ) -> DamageInstance:
        label: str = "Railgun Judgement"
        base_potency: int = 240
        tags: set[DamageTag] = {
            DamageTag.ACTIVE,
            DamageTag.MEDIUM_AMMO,
            DamageTag.PHYSICAL,
            DamageTag.AREA_OF_EFFECT,
            DamageTag.ULTIMATE,
        }

        buffs_before: list[Buff] = []

        if has_fixed_key_6:
            tags.add(DamageTag.MELEE)
        else:
            tags.add(DamageTag.MEDIUM_AMMO)

        # Ignores 100% of the target's defense.
        buffs_before.append(
            Buff(
                100,
                ModifierType.ADDITIVE,
                SpecialAttribute.DEFENSE_IGNORE,
                DamageTag.ALL,
            ),
        )

        return DamageInstance(
            label=label,
            base_potency=base_potency,
            tags=tags,
            group_name="Railgun Judgement",
            buffs_before=buffs_before,
        )


class RailgunJudgementV1(CombatAction):
    """Asteria Ultimate (V1)."""

    @override
    def execute(
        self,
        has_fixed_key_6: bool,
        stacks_of_absolution: int,
    ) -> DamageInstance:
        label: str = "Railgun Judgement"
        base_potency: int = 300
        tags: set[DamageTag] = {
            DamageTag.ACTIVE,
            DamageTag.MEDIUM_AMMO,
            DamageTag.PHYSICAL,
            DamageTag.AREA_OF_EFFECT,
            DamageTag.ULTIMATE,
        }

        buffs_before: list[Buff] = []

        if has_fixed_key_6:
            tags.add(DamageTag.MELEE)
        else:
            tags.add(DamageTag.MEDIUM_AMMO)

        # Ignores 200% of the target's defense.
        buffs_before.append(
            Buff(
                200,
                ModifierType.ADDITIVE,
                SpecialAttribute.DEFENSE_IGNORE,
                DamageTag.ALL,
            ),
        )

        return DamageInstance(
            label=label,
            base_potency=base_potency,
            tags=tags,
            group_name="Railgun Judgement",
            buffs_before=buffs_before,
        )


class RailgunJudgementV6(CombatAction):
    """Asteria Ultimate (V6)."""

    @override
    def execute(
        self,
        has_fixed_key_6: bool,
        stacks_of_absolution: int,
    ) -> DamageInstance:
        label: str = "Railgun Judgement"
        base_potency: int = 300
        tags: set[DamageTag] = {
            DamageTag.ACTIVE,
            DamageTag.PHYSICAL,
            DamageTag.AREA_OF_EFFECT,
            DamageTag.ULTIMATE,
        }

        buffs_before: list[Buff] = []

        if has_fixed_key_6:
            tags.add(DamageTag.MELEE)
        else:
            tags.add(DamageTag.MEDIUM_AMMO)

        # Ignores 200% of the target's defense.
        buffs_before.append(
            Buff(
                200,
                ModifierType.ADDITIVE,
                SpecialAttribute.DEFENSE_IGNORE,
                DamageTag.ALL,
            ),
        )

        # For each stack of Absolution that the target has, the damage multiplier is increased by 50%.
        potency_per_stack: int = 50
        maximum_stacks: int = 6
        if stacks_of_absolution > 0:
            stacks_to_consider: int = min(max(0, stacks_of_absolution), maximum_stacks)
            potency_increase: int = potency_per_stack * stacks_to_consider
            base_potency += potency_increase

        return DamageInstance(
            label=label,
            base_potency=base_potency,
            tags=tags,
            group_name="Railgun Judgement",
            buffs_before=buffs_before,
        )


class BladeOfSin(CombatAction):
    """Passive Lock-On Attack granted by the Crime and Punishment buff.
    Triggers:
    * After dealing Physical damage
    * At the end of the turn (to the nearest target)
    * After an ally is attacked (to the attacker)

    Each trigger method can trigger up to 1 time per turn.
    """

    @override
    def execute(self, stacks_of_absolution: int) -> DamageInstance:
        label: str = "Blade of Sin"
        base_potency: int = 80
        tags: set[DamageTag] = {
            DamageTag.PASSIVE,
            DamageTag.MELEE,
            DamageTag.TARGETED,
            DamageTag.PHYSICAL,
        }

        buffs_before: list[Buff] = []

        return DamageInstance(
            label=label,
            base_potency=base_potency,
            tags=tags,
            group_name="Blade of Sin",
            buffs_before=buffs_before,
        )


class BladeOfSinV3(CombatAction):
    """Passive Lock-On Attack granted by the Crime and Punishment buff.
    Triggers:
    * After dealing Physical damage
    * At the end of the turn (to the nearest target)
    * After an ally is attacked (to the attacker)

    No limit on triggers from dealing Physical damage but can only trigger once per unit per turn.
    Otherwise, each trigger method can trigger up to 1 time per turn.
    """

    @override
    def execute(self, stacks_of_absolution: int) -> DamageInstance:
        label: str = "Blade of Sin"
        base_potency: int = 100
        tags: set[DamageTag] = {
            DamageTag.PASSIVE,
            DamageTag.MELEE,
            DamageTag.TARGETED,
            DamageTag.PHYSICAL,
        }

        buffs_before: list[Buff] = []

        # Ignores 50% of the target's defense when attacking.
        buffs_before.append(
            Buff(
                50,
                ModifierType.ADDITIVE,
                SpecialAttribute.DEFENSE_IGNORE,
                DamageTag.ALL,
            ),
        )

        return DamageInstance(
            label=label,
            base_potency=base_potency,
            tags=tags,
            group_name="Blade of Sin",
            buffs_before=buffs_before,
        )


class BladeOfSinV6(CombatAction):
    """Passive Lock-On Attack granted by the Crime and Punishment buff.
    Triggers:
    * After dealing Physical damage
    * At the end of the turn (to the nearest target)
    * After an ally is attacked (to the attacker)

    No limit on triggers from dealing Physical damage but can only trigger once per unit per turn.
    Otherwise, each trigger method can trigger up to 1 time per turn.
    """

    @override
    def execute(self, stacks_of_absolution: int) -> DamageInstance:
        label: str = "Blade of Sin"
        base_potency: int = 100
        tags: set[DamageTag] = {
            DamageTag.PASSIVE,
            DamageTag.MELEE,
            DamageTag.TARGETED,
            DamageTag.PHYSICAL,
        }

        buffs_before: list[Buff] = []

        # Ignores 50% of the target's defense when attacking.
        buffs_before.append(
            Buff(
                50,
                ModifierType.ADDITIVE,
                SpecialAttribute.DEFENSE_IGNORE,
                DamageTag.ALL,
            ),
        )

        # For each stack of Absolution that the target has, the damage multiplier is increased by 50%.
        potency_per_stack: int = 50
        maximum_stacks: int = 6
        if stacks_of_absolution > 0:
            stacks_to_consider: int = min(max(0, stacks_of_absolution), maximum_stacks)
            potency_increase: int = potency_per_stack * stacks_to_consider
            base_potency += potency_increase

        return DamageInstance(
            label=label,
            base_potency=base_potency,
            tags=tags,
            group_name="Blade of Sin",
            buffs_before=buffs_before,
        )


class Asteria(Doll):
    """Asteria."""

    name: str = "Asteria"
    irrelevant_damage_tags: ClassVar[set[DamageTag]] = set(
        [
            DamageTag.CORROSION,
            DamageTag.HYDRO,
            DamageTag.BURN,
            DamageTag.ELECTRIC,
            DamageTag.FREEZE,
            DamageTag.PHASE,
            DamageTag.LIGHT_AMMO,
            DamageTag.HEAVY_AMMO,
            DamageTag.SHOTGUN_AMMO,
            DamageTag.SUPPORT_ACTION,
            DamageTag.INTERCEPTION,
            DamageTag.COUNTERATTACK,
            DamageTag.PHYSICAL_SUMMON,
            DamageTag.FIXED,
        ]
    )

    silent_trigger: CombatAction = Field(default_factory=SilentTrigger)
    demolition_reckoning: CombatAction = Field(default_factory=DemolitionReckoning)
    railgun_judgement: CombatAction = Field(default_factory=RailgunJudgement)
    blade_of_sin: CombatAction = Field(default_factory=BladeOfSin)

    def set_to_v0(self) -> None:
        """Sets Fortification Level to Segment00."""
        self.silent_trigger = SilentTrigger()
        self.demolition_reckoning = DemolitionReckoning()
        self.railgun_judgement = RailgunJudgement()
        self.blade_of_sin = BladeOfSin()

    def set_to_v1(self) -> None:
        """Sets Fortification Level to Segment01."""
        self.set_to_v0()

        self.railgun_judgement = RailgunJudgementV1()

    def set_to_v3(self) -> None:
        """Sets Fortification Level to Segment03."""
        self.set_to_v1()

        self.blade_of_sin = BladeOfSinV3()

    def set_to_v6(self) -> None:
        """Sets Fortification Level to Segment06."""
        self.set_to_v3()

        self.railgun_judgement = RailgunJudgementV6()
        self.blade_of_sin = BladeOfSinV6()

    @override
    def set_fortification_level(self, level: FortificationLevel):
        self.fortification_level = level
        match level:
            case FortificationLevel.SEGMENT00:
                self.set_to_v0()
            case FortificationLevel.SEGMENT01:
                self.set_to_v1()
            case FortificationLevel.SEGMENT02:
                self.set_to_v1()
            case FortificationLevel.SEGMENT03:
                self.set_to_v3()
            case FortificationLevel.SEGMENT04:
                self.set_to_v3()
            case FortificationLevel.SEGMENT05:
                self.set_to_v3()
            case FortificationLevel.SEGMENT06:
                self.set_to_v6()
