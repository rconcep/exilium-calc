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


class LoneWolfTerritory(CombatAction):
    """Makiatto basic attack."""

    @override
    def execute(self, has_active_engagement: bool = False) -> DamageInstance:
        label: str = "Lone Wolf Territory"
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
            group_name="Lone Wolf Territory",
        )


class ColdPrecisionShot(CombatAction):
    """Makiatto S1 (first hit)."""

    @override
    def execute(self) -> DamageInstance:
        label: str = "Cold Precision Shot"
        base_potency: int = 160
        tags: set[DamageTag] = {
            DamageTag.ACTIVE,
            DamageTag.CONFECTANCE,
            DamageTag.HEAVY_AMMO,
            DamageTag.TARGETED,
            DamageTag.FREEZE,
            DamageTag.PHASE,
        }

        buffs_before: list[Buff] = [
            Buff(
                30,
                ModifierType.ADDITIVE,
                SpecialAttribute.CRITICAL_DAMAGE,
                DamageTag.ALL,
            )
        ]

        return DamageInstance(
            label=label,
            base_potency=base_potency,
            tags=tags,
            group_name="Cold Precision Shot",
            buffs_before=buffs_before,
        )


class ColdPrecisionShotV1(CombatAction):
    """Makiatto S1 (V1) (first hit)."""

    @override
    def execute(self) -> DamageInstance:
        label: str = "Cold Precision Shot"
        base_potency: int = 100
        tags: set[DamageTag] = {
            DamageTag.ACTIVE,
            DamageTag.CONFECTANCE,
            DamageTag.HEAVY_AMMO,
            DamageTag.TARGETED,
            DamageTag.FREEZE,
            DamageTag.PHASE,
        }

        return DamageInstance(
            label=label,
            base_potency=base_potency,
            tags=tags,
            group_name="Cold Precision Shot",
        )


class ColdPrecisionShotSecond(CombatAction):
    """Makiatto S1 (second hit doesn't exist)."""

    @override
    def execute(self, first_hit_was_critical: bool = False) -> DamageInstance:
        label: str = "Cold Precision Shot"
        base_potency: int = 0
        tags: set[DamageTag] = set()

        return DamageInstance(
            label=label,
            base_potency=base_potency,
            tags=tags,
            group_name="Cold Precision Shot",
        )


class ColdPrecisionShotSecondV1(CombatAction):
    """Makiatto S1 (V1) (second hit)."""

    @override
    def execute(self, first_hit_was_critical: bool = False) -> DamageInstance:
        label: str = "Cold Precision Shot"
        base_potency: int = 100
        tags: set[DamageTag] = {
            DamageTag.ACTIVE,
            DamageTag.CONFECTANCE,
            DamageTag.HEAVY_AMMO,
            DamageTag.TARGETED,
            DamageTag.FREEZE,
            DamageTag.PHASE,
        }

        buffs_before: list[Buff] = []

        if first_hit_was_critical:
            buffs_before.append(
                Buff(
                    80,
                    ModifierType.ADDITIVE,
                    SpecialAttribute.CRITICAL_DAMAGE,
                    DamageTag.ALL,
                )
            )
            buffs_before.append(
                Buff(
                    100,
                    ModifierType.ADDITIVE,
                    StatType.CRIT_RATE,
                )
            )

        return DamageInstance(
            label=label,
            base_potency=base_potency,
            tags=tags,
            group_name="Cold Precision Shot",
            buffs_before=buffs_before,
        )


class ProfessionalTactics(CombatAction):
    """Makiatto S2."""

    @override
    def execute(self) -> DamageInstance:
        label: str = "Professional Tactics"
        base_potency: int = 130
        tags: set[DamageTag] = {
            DamageTag.ACTIVE,
            DamageTag.PHYSICAL,
            DamageTag.HEAVY_AMMO,
            DamageTag.TARGETED,
        }

        return DamageInstance(
            label=label,
            base_potency=base_potency,
            tags=tags,
            group_name="Professional Tactics",
        )


class Interception(CombatAction):
    """Interception from Alert status."""

    @override
    def execute(self) -> DamageInstance:
        label: str = "Interception"
        base_potency: int = 90
        tags: set[DamageTag] = {
            DamageTag.PASSIVE,
            DamageTag.INTERCEPTION,
            DamageTag.HEAVY_AMMO,
            DamageTag.TARGETED,
            DamageTag.FREEZE,
            DamageTag.PHASE,
        }

        return DamageInstance(
            label=label,
            base_potency=base_potency,
            tags=tags,
            group_name="Interception",
        )


class Makiatto(Doll):
    """Makiatto."""

    name: str = "Makiatto"
    irrelevant_damage_tags: ClassVar[set[DamageTag]] = set(
        [
            DamageTag.CORROSION,
            DamageTag.HYDRO,
            DamageTag.BURN,
            DamageTag.ELECTRIC,
            DamageTag.MELEE,
            DamageTag.LIGHT_AMMO,
            DamageTag.MEDIUM_AMMO,
            DamageTag.SHOTGUN_AMMO,
            DamageTag.SUPPORT_ACTION,
            DamageTag.COUNTERATTACK,
            DamageTag.AREA_OF_EFFECT,
            DamageTag.ULTIMATE,
        ]
    )

    lone_wolf_territory: CombatAction = Field(default_factory=LoneWolfTerritory)
    professional_tactics: CombatAction = Field(default_factory=ProfessionalTactics)
    cold_precision_shot_first: CombatAction = Field(default_factory=ColdPrecisionShot)
    cold_precision_shot_second: CombatAction = Field(
        default_factory=ColdPrecisionShotSecond
    )
    interception: CombatAction = Field(default_factory=Interception)

    def set_to_v0(self) -> None:
        """Sets Fortification Level to Segment00."""
        self.lone_wolf_territory: CombatAction = LoneWolfTerritory()
        self.professional_tactics: CombatAction = ProfessionalTactics()
        self.cold_precision_shot_first: CombatAction = ColdPrecisionShot()
        self.cold_precision_shot_second: CombatAction = ColdPrecisionShotSecond()
        self.interception: CombatAction = Interception()

        # Passive: Battlefield Insight
        self.additive_modifiers.basic_attributes[StatType.CRIT_RATE] = 40
        self.additive_modifiers.special_attributes[
            SpecialAttribute.CRITICAL_DAMAGE
        ].set_multiplier(DamageTag.ALL, -10)

        # When attacking a target with Frigid
        self.additive_modifiers.special_attributes[
            SpecialAttribute.DAMAGE_BOOST
        ].set_multiplier(DamageTag.ALL, 30)

        # Expansion Key: Sniper's Lock
        self.additive_modifiers.special_attributes[
            SpecialAttribute.CRITICAL_DAMAGE
        ].set_multiplier(DamageTag.INTERCEPTION, 30)

    def set_to_v1(self) -> None:
        """Sets Fortification Level to Segment01."""
        self.set_to_v0()

        self.cold_precision_shot_first: CombatAction = ColdPrecisionShotV1()
        self.cold_precision_shot_second: CombatAction = ColdPrecisionShotSecondV1()

    def set_to_v5(self) -> None:
        """Sets Fortification Level to Segment05."""
        self.set_to_v1()

        # When dealing Freeze damage to an enemy target with Frozen or Frigid, increases ... damage dealt by 30%.
        # Does not stack with the Lvl 1 effect.
        self.additive_modifiers.special_attributes[
            SpecialAttribute.DAMAGE_BOOST
        ].set_multiplier(DamageTag.ALL, 0)

        self.additive_modifiers.special_attributes[
            SpecialAttribute.DAMAGE_BOOST
        ].set_multiplier(DamageTag.FREEZE, 30)

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
                self.set_to_v1()
            case FortificationLevel.SEGMENT04:
                self.set_to_v1()
            case FortificationLevel.SEGMENT05:
                self.set_to_v5()
            case FortificationLevel.SEGMENT06:
                self.set_to_v5()

    def get_sample_data(self) -> list[DamageInstance]:
        """Returns a sample single target rotation."""
        rotation_data: list[DamageInstance] = [
            # Turn 1
            self.cold_precision_shot_first.execute(),
            self.cold_precision_shot_second.execute(first_hit_was_critical=True),
            self.interception.execute(),
            self.interception.execute(),
            self.interception.execute(),
            self.interception.execute(),
            # Turn 2
            self.cold_precision_shot_first.execute(),
            self.cold_precision_shot_second.execute(first_hit_was_critical=True),
            self.interception.execute(),
            self.interception.execute(),
            self.interception.execute(),
            self.interception.execute(),
            # Turn 3
            self.cold_precision_shot_first.execute(),
            self.cold_precision_shot_second.execute(first_hit_was_critical=True),
            # Turn 4
            self.cold_precision_shot_first.execute(),
            self.cold_precision_shot_second.execute(first_hit_was_critical=True),
            self.interception.execute(),
            self.interception.execute(),
            self.interception.execute(),
            self.interception.execute(),
            # Turn 5
            self.cold_precision_shot_first.execute(),
            self.cold_precision_shot_second.execute(first_hit_was_critical=True),
            self.interception.execute(),
            self.interception.execute(),
            self.interception.execute(),
            self.interception.execute(),
            # Turn 6
            self.cold_precision_shot_first.execute(),
            self.cold_precision_shot_second.execute(first_hit_was_critical=True),
            # Turn 7
            self.cold_precision_shot_first.execute(),
            self.cold_precision_shot_second.execute(first_hit_was_critical=True),
            self.interception.execute(),
            self.interception.execute(),
            self.interception.execute(),
            self.interception.execute(),
        ]

        return rotation_data
