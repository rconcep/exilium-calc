from typing import override, ClassVar
from pydantic import Field

from core.types import (
    DamageTag,
    StatType,
    SpecialAttribute,
    ModifierType,
    Doll,
    FortificationLevel,
    SummonedUnit,
)
from core.buffs import Buff
from core.combat import DamageInstance, CombatAction


ACTIVE_ENGAGEMENT_BUFF: int = 30
ACTIVE_ENGAGEMENT_BUFF_V5: int = 40


class PatrolTime(CombatAction):
    """Mosin-Nagant basic attack."""

    @override
    def execute(self, has_active_engagement: bool = False) -> DamageInstance:
        label: str = "Patrol Time"
        base_potency: int = 80
        tags: set[DamageTag] = {
            DamageTag.ACTIVE,
            DamageTag.BASIC,
            DamageTag.HEAVY_AMMO,
            DamageTag.TARGETED,
        }

        buffs_before: list[Buff] = []

        if has_active_engagement:
            tags.add(DamageTag.ELECTRIC)
            tags.add(DamageTag.PHASE)
            buffs_before.append(
                Buff(
                    ACTIVE_ENGAGEMENT_BUFF,
                    ModifierType.ADDITIVE,
                    SpecialAttribute.DAMAGE_BOOST,
                    DamageTag.ELECTRIC,
                )
            )
        else:
            tags.add(DamageTag.PHYSICAL)

        return DamageInstance(
            label=label,
            base_potency=base_potency,
            tags=tags,
            group_name="Patrol Time",
            buffs_before=buffs_before,
        )


class TargetVictory(CombatAction):
    """Mosin-Nagant S1."""

    @override
    def execute(self, has_active_engagement: bool = False) -> DamageInstance:
        label: str = "Patrol Time"
        base_potency: int = 130
        tags: set[DamageTag] = {
            DamageTag.ACTIVE,
            DamageTag.CONFECTANCE,
            DamageTag.HEAVY_AMMO,
            DamageTag.TARGETED,
        }

        buffs_before: list[Buff] = []

        if has_active_engagement:
            tags.add(DamageTag.ELECTRIC)
            tags.add(DamageTag.PHASE)
            buffs_before.append(
                Buff(
                    ACTIVE_ENGAGEMENT_BUFF,
                    ModifierType.ADDITIVE,
                    SpecialAttribute.DAMAGE_BOOST,
                    DamageTag.ELECTRIC,
                )
            )
        else:
            tags.add(DamageTag.PHYSICAL)

        return DamageInstance(
            label=label,
            base_potency=base_potency,
            tags=tags,
            group_name="Target Victory",
            buffs_before=buffs_before,
        )


class DeclarationOfVictory(CombatAction):
    """Mosin-Nagant Ultimate."""

    @override
    def execute(self, has_active_engagement: bool = False) -> DamageInstance:
        label: str = "Declaration of Victory"
        base_potency: int = 180
        tags: set[DamageTag] = {
            DamageTag.ACTIVE,
            DamageTag.TARGETED,
            DamageTag.HEAVY_AMMO,
            DamageTag.ULTIMATE,
            DamageTag.CONFECTANCE,
        }

        buffs_before: list[Buff] = []

        if has_active_engagement:
            tags.add(DamageTag.ELECTRIC)
            tags.add(DamageTag.PHASE)
            buffs_before.append(
                Buff(
                    ACTIVE_ENGAGEMENT_BUFF,
                    ModifierType.ADDITIVE,
                    SpecialAttribute.DAMAGE_BOOST,
                    DamageTag.ELECTRIC,
                )
            )
        else:
            tags.add(DamageTag.PHYSICAL)

        return DamageInstance(
            label=label,
            base_potency=base_potency,
            tags=tags,
            group_name="Declaration of Victory",
            buffs_before=buffs_before,
        )


class SupportAction(CombatAction):
    """Support action."""

    @override
    def execute(self, has_active_engagement: bool = False) -> DamageInstance:
        label: str = "Support Action"
        base_potency: int = 80
        tags: set[DamageTag] = {
            DamageTag.PASSIVE,
            DamageTag.SUPPORT_ACTION,
            DamageTag.HEAVY_AMMO,
            DamageTag.TARGETED,
        }

        buffs_before: list[Buff] = []

        if has_active_engagement:
            tags.add(DamageTag.ELECTRIC)
            tags.add(DamageTag.PHASE)
            buffs_before.append(
                Buff(
                    ACTIVE_ENGAGEMENT_BUFF,
                    ModifierType.ADDITIVE,
                    SpecialAttribute.DAMAGE_BOOST,
                    DamageTag.ELECTRIC,
                )
            )
        else:
            tags.add(DamageTag.PHYSICAL)

        return DamageInstance(
            label=label,
            base_potency=base_potency,
            tags=tags,
            group_name="Support Action",
            buffs_before=buffs_before,
        )


class PatrolTimeV5(CombatAction):
    """Mosin-Nagant basic attack (V5)."""

    @override
    def execute(self, has_active_engagement: bool = False) -> DamageInstance:
        label: str = "Patrol Time"
        base_potency: int = 80
        tags: set[DamageTag] = {
            DamageTag.ACTIVE,
            DamageTag.BASIC,
            DamageTag.HEAVY_AMMO,
            DamageTag.TARGETED,
        }

        buffs_before: list[Buff] = []

        if has_active_engagement:
            tags.add(DamageTag.ELECTRIC)
            tags.add(DamageTag.PHASE)
            buffs_before.append(
                Buff(
                    ACTIVE_ENGAGEMENT_BUFF_V5,
                    ModifierType.ADDITIVE,
                    SpecialAttribute.DAMAGE_BOOST,
                    DamageTag.ELECTRIC,
                )
            )
        else:
            tags.add(DamageTag.PHYSICAL)

        return DamageInstance(
            label=label,
            base_potency=base_potency,
            tags=tags,
            group_name="Patrol Time",
            buffs_before=buffs_before,
        )


class TargetVictoryV5(CombatAction):
    """Mosin-Nagant S1 (V5)."""

    @override
    def execute(self, has_active_engagement: bool = False) -> DamageInstance:
        label: str = "Patrol Time"
        base_potency: int = 130
        tags: set[DamageTag] = {
            DamageTag.ACTIVE,
            DamageTag.CONFECTANCE,
            DamageTag.HEAVY_AMMO,
            DamageTag.TARGETED,
        }

        buffs_before: list[Buff] = []

        if has_active_engagement:
            tags.add(DamageTag.ELECTRIC)
            tags.add(DamageTag.PHASE)
            buffs_before.append(
                Buff(
                    ACTIVE_ENGAGEMENT_BUFF,
                    ModifierType.ADDITIVE,
                    SpecialAttribute.DAMAGE_BOOST,
                    DamageTag.ELECTRIC,
                )
            )
        else:
            tags.add(DamageTag.PHYSICAL)

        return DamageInstance(
            label=label,
            base_potency=base_potency,
            tags=tags,
            group_name="Target Victory",
            buffs_before=buffs_before,
        )


class DeclarationOfVictoryV5(CombatAction):
    """Mosin-Nagant Ultimate (V5)."""

    @override
    def execute(self, has_active_engagement: bool = False) -> DamageInstance:
        label: str = "Declaration of Victory"
        base_potency: int = 180
        tags: set[DamageTag] = {
            DamageTag.ACTIVE,
            DamageTag.TARGETED,
            DamageTag.HEAVY_AMMO,
            DamageTag.ULTIMATE,
            DamageTag.CONFECTANCE,
        }

        buffs_before: list[Buff] = []

        if has_active_engagement:
            tags.add(DamageTag.ELECTRIC)
            tags.add(DamageTag.PHASE)
            buffs_before.append(
                Buff(
                    ACTIVE_ENGAGEMENT_BUFF,
                    ModifierType.ADDITIVE,
                    SpecialAttribute.DAMAGE_BOOST,
                    DamageTag.ELECTRIC,
                )
            )
        else:
            tags.add(DamageTag.PHYSICAL)

        return DamageInstance(
            label=label,
            base_potency=base_potency,
            tags=tags,
            group_name="Declaration of Victory",
            buffs_before=buffs_before,
        )


class SupportActionV5(CombatAction):
    """Support action (V5)."""

    @override
    def execute(self, has_active_engagement: bool = False) -> DamageInstance:
        label: str = "Support Action"
        base_potency: int = 80
        tags: set[DamageTag] = {
            DamageTag.PASSIVE,
            DamageTag.SUPPORT_ACTION,
            DamageTag.HEAVY_AMMO,
            DamageTag.TARGETED,
        }

        buffs_before: list[Buff] = []

        if has_active_engagement:
            tags.add(DamageTag.ELECTRIC)
            tags.add(DamageTag.PHASE)
            buffs_before.append(
                Buff(
                    ACTIVE_ENGAGEMENT_BUFF,
                    ModifierType.ADDITIVE,
                    SpecialAttribute.DAMAGE_BOOST,
                    DamageTag.ELECTRIC,
                )
            )
        else:
            tags.add(DamageTag.PHYSICAL)

        return DamageInstance(
            label=label,
            base_potency=base_potency,
            tags=tags,
            group_name="Support Action",
            buffs_before=buffs_before,
        )


class MosinNagant(Doll):
    """Mosin-Nagant."""

    name: str = "Mosin-Nagant"
    irrelevant_damage_tags: ClassVar[set[DamageTag]] = set(
        [
            DamageTag.CORROSION,
            DamageTag.FREEZE,
            DamageTag.HYDRO,
            DamageTag.BURN,
            DamageTag.MELEE,
            DamageTag.LIGHT_AMMO,
            DamageTag.MEDIUM_AMMO,
            DamageTag.SHOTGUN_AMMO,
            DamageTag.INTERCEPTION,
            DamageTag.COUNTERATTACK,
            DamageTag.AREA_OF_EFFECT,
        ]
    )

    patrol_time: CombatAction = Field(default_factory=PatrolTime)
    target_victory: CombatAction = Field(default_factory=TargetVictory)
    declaration_of_victory: CombatAction = Field(default_factory=DeclarationOfVictory)
    support_action: CombatAction = Field(default_factory=SupportAction)

    def set_to_v0(self) -> None:
        """Sets Fortification Level to Segment00."""
        self.patrol_time: CombatAction = PatrolTime()
        self.target_victory: CombatAction = TargetVictory()
        self.declaration_of_victory: CombatAction = DeclarationOfVictory()
        self.support_action: CombatAction = SupportAction()

    def set_to_v5(self) -> None:
        """Sets Fortification Level to Segment05."""
        self.set_to_v0()

        self.patrol_time: CombatAction = PatrolTimeV5()
        self.target_victory: CombatAction = TargetVictoryV5()
        self.declaration_of_victory: CombatAction = DeclarationOfVictoryV5()
        self.support_action: CombatAction = SupportActionV5()

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
                self.set_to_v0()
            case FortificationLevel.SEGMENT05:
                self.set_to_v5()
            case FortificationLevel.SEGMENT06:
                self.set_to_v5()

    def get_sample_data(self) -> list[DamageInstance]:
        """Returns a sample single target rotation."""
        rotation_data: list[DamageInstance] = [
            # Turn 1
            self.support_action.execute(has_active_engagement=True),
            self.support_action.execute(has_active_engagement=True),
            self.support_action.execute(has_active_engagement=True),
            self.declaration_of_victory.execute(has_active_engagement=True),
            # Turn 2
            self.support_action.execute(has_active_engagement=True),
            self.support_action.execute(has_active_engagement=True),
            self.support_action.execute(has_active_engagement=True),
            self.declaration_of_victory.execute(has_active_engagement=True),
            # Turn 3
            self.support_action.execute(has_active_engagement=True),
            self.support_action.execute(has_active_engagement=True),
            self.support_action.execute(has_active_engagement=True),
            self.declaration_of_victory.execute(has_active_engagement=True),
            # Turn 4
            self.support_action.execute(has_active_engagement=True),
            self.support_action.execute(has_active_engagement=True),
            self.support_action.execute(has_active_engagement=True),
            self.declaration_of_victory.execute(has_active_engagement=True),
            # Turn 5
            self.support_action.execute(has_active_engagement=True),
            self.support_action.execute(has_active_engagement=True),
            self.support_action.execute(has_active_engagement=True),
            self.declaration_of_victory.execute(has_active_engagement=True),
            # Turn 6
            self.support_action.execute(has_active_engagement=True),
            self.support_action.execute(has_active_engagement=True),
            self.support_action.execute(has_active_engagement=True),
            self.declaration_of_victory.execute(has_active_engagement=True),
            # Turn 7
            self.support_action.execute(has_active_engagement=True),
            self.support_action.execute(has_active_engagement=True),
            self.support_action.execute(has_active_engagement=True),
            self.declaration_of_victory.execute(has_active_engagement=True),
        ]

        return rotation_data
