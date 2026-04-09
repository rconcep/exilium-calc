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


class FormIntentionFist(CombatAction):
    """Jiangyu basic attack."""

    @override
    def execute(self) -> DamageInstance:
        label: str = "Form Intention Fist"
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
            group_name="Form Intention Fist",
        )


class Thunderclap(CombatAction):
    """Jiangyu S1."""

    @override
    def execute(self) -> DamageInstance:
        label: str = "Thunderclap"
        base_potency: int = 90
        tags: set[DamageTag] = {
            DamageTag.ACTIVE,
            DamageTag.MELEE,
            DamageTag.AREA_OF_EFFECT,
            DamageTag.ELECTRIC,
            DamageTag.PHASE,
        }

        return DamageInstance(
            label=label,
            base_potency=base_potency,
            tags=tags,
            group_name="Thunderclap",
        )


class ThunderclapV4(CombatAction):
    """Jiangyu S1 (V4)."""

    @override
    def execute(self) -> DamageInstance:
        label: str = "Thunderclap"
        base_potency: int = 90
        tags: set[DamageTag] = {
            DamageTag.ACTIVE,
            DamageTag.MELEE,
            DamageTag.AREA_OF_EFFECT,
            DamageTag.ELECTRIC,
            DamageTag.PHASE,
        }

        return DamageInstance(
            label=label,
            base_potency=base_potency,
            tags=tags,
            group_name="Thunderclap",
        )


class LightningSmash(CombatAction):
    """Jiangyu S2."""

    @override
    def execute(self) -> DamageInstance:
        base_potency: int = 110
        label: str = "Lightning Smash"
        tags: set[DamageTag] = {
            DamageTag.ACTIVE,
            DamageTag.TARGETED,
            DamageTag.ELECTRIC,
            DamageTag.PHASE,
        }

        return DamageInstance(
            label=label,
            base_potency=base_potency,
            tags=tags,
            group_name="Lightning Smash",
        )


class LightningSmashV3(CombatAction):
    """Jiangyu S2 (V3)."""

    @override
    def execute(self) -> DamageInstance:
        base_potency: int = 140
        label: str = "Lightning Smash"
        tags: set[DamageTag] = {
            DamageTag.ACTIVE,
            DamageTag.TARGETED,
            DamageTag.ELECTRIC,
            DamageTag.PHASE,
        }

        # Damage dealt against targets afflicted with Voltage Sag is increased by 30%.
        # Assuming Voltage Sag is always active since it's a core part of Jiangyu's kit and is easy to maintain uptime on.
        buffs_before: list[Buff] = [
            Buff(
                value=30,
                modifier_type=ModifierType.ADDITIVE,
                stat_type=SpecialAttribute.DAMAGE_BOOST,
                tag=DamageTag.ALL,
            ),
        ]

        return DamageInstance(
            label=label,
            base_potency=base_potency,
            tags=tags,
            group_name="Lightning Smash",
            buffs_before=buffs_before,
        )


class LightningSmashV5(CombatAction):
    """Jiangyu S2 (V5)."""

    @override
    def execute(self) -> DamageInstance:
        base_potency: int = 140
        label: str = "Lightning Smash"
        tags: set[DamageTag] = {
            DamageTag.ACTIVE,
            DamageTag.TARGETED,
            DamageTag.ELECTRIC,
            DamageTag.PHASE,
        }

        # If the target is in Stability Break, Jiangyu performs an additional attack.
        # Model this by an additional CombatAction rather than doubling the potency.

        # Damage dealt against targets afflicted with Voltage Sag is increased by 30%.
        # Assuming Voltage Sag is always active since it's a core part of Jiangyu's kit and is easy to maintain uptime on.
        buffs_before: list[Buff] = [
            Buff(
                value=30,
                modifier_type=ModifierType.ADDITIVE,
                stat_type=SpecialAttribute.DAMAGE_BOOST,
                tag=DamageTag.ALL,
            ),
        ]

        return DamageInstance(
            label=label,
            base_potency=base_potency,
            tags=tags,
            group_name="Lightning Smash",
            buffs_before=buffs_before,
        )


class RollingThunder(CombatAction):
    """Jiangyu Ultimate."""

    @override
    def execute(self) -> DamageInstance:
        base_potency: int = 130
        label: str = "Rolling Thunder"
        tags: set[DamageTag] = {
            DamageTag.ACTIVE,
            DamageTag.ELECTRIC,
            DamageTag.PHASE,
            DamageTag.MEDIUM_AMMO,
            DamageTag.TARGETED,
            DamageTag.ULTIMATE,
        }

        return DamageInstance(
            label=label,
            base_potency=base_potency,
            tags=tags,
            group_name="Rolling Thunder",
        )


class Interception(CombatAction):
    """Interception granted by Fixed Key 2 - Intercepting Fist."""

    @override
    def execute(self) -> DamageInstance:
        label: str = "Interception"
        base_potency: int = 60
        tags: set[DamageTag] = {
            DamageTag.PASSIVE,
            DamageTag.INTERCEPTION,
            DamageTag.MEDIUM_AMMO,
            DamageTag.TARGETED,
            DamageTag.ELECTRIC,
            DamageTag.PHASE,
        }

        return DamageInstance(
            label=label,
            base_potency=base_potency,
            tags=tags,
            group_name="Interception",
        )


class SupportAction(CombatAction):
    """Support Action from Grand Aura passive."""

    @override
    def execute(self, target_is_in_stability_break: bool) -> DamageInstance:
        label: str = "Support Action"
        tags: set[DamageTag] = {
            DamageTag.PASSIVE,
            DamageTag.SUPPORT_ACTION,
            DamageTag.MEDIUM_AMMO,
            DamageTag.TARGETED,
            DamageTag.ELECTRIC,
            DamageTag.PHASE,
        }

        if target_is_in_stability_break:
            base_potency: int = 75
        else:
            base_potency: int = 45

        return DamageInstance(
            label=label,
            base_potency=base_potency,
            tags=tags,
            group_name="Support Action",
        )


class UrgeToPerform(CombatAction):
    """Damage from Expansion Key - Urge to Perform, the attack triggered when an enemy enters Stability Break."""

    @override
    def execute(self) -> DamageInstance:
        label: str = "Urge to Perform"
        base_potency: int = 90
        tags: set[DamageTag] = {
            DamageTag.PASSIVE,
            DamageTag.TARGETED,
            DamageTag.ELECTRIC,
            DamageTag.PHASE,
        }

        return DamageInstance(
            label=label,
            base_potency=base_potency,
            tags=tags,
            group_name="Urge to Perform",
        )


class Jiangyu(Doll):
    """Jiangyu."""

    name: str = "Jiangyu"
    irrelevant_damage_tags: ClassVar[set[DamageTag]] = set(
        [
            DamageTag.CORROSION,
            DamageTag.HYDRO,
            DamageTag.BURN,
            DamageTag.FREEZE,
            DamageTag.LIGHT_AMMO,
            DamageTag.HEAVY_AMMO,
            DamageTag.SHOTGUN_AMMO,
            DamageTag.COUNTERATTACK,
            DamageTag.FIXED,
            DamageTag.PHYSICAL_SUMMON,
        ]
    )

    form_intention_fist: CombatAction = Field(default_factory=FormIntentionFist)
    thunderclap: CombatAction = Field(default_factory=Thunderclap)
    lightning_smash: CombatAction = Field(default_factory=LightningSmash)
    rolling_thunder: CombatAction = Field(default_factory=RollingThunder)
    interception: CombatAction = Field(default_factory=Interception)
    support_action: CombatAction = Field(default_factory=SupportAction)
    urge_to_perform: CombatAction = Field(default_factory=UrgeToPerform)

    def set_to_v0(self) -> None:
        """Sets Fortification Level to Segment00."""
        self.form_intention_fist: CombatAction = FormIntentionFist()
        self.thunderclap: CombatAction = Thunderclap()
        self.lightning_smash: CombatAction = LightningSmash()
        self.rolling_thunder: CombatAction = RollingThunder()
        self.interception: CombatAction = Interception()
        self.support_action: CombatAction = SupportAction()
        self.urge_to_perform: CombatAction = UrgeToPerform()

    def set_to_v3(self) -> None:
        """Sets Fortification Level to Segment01."""
        self.set_to_v0()

        self.lightning_smash: CombatAction = LightningSmashV3()

    def set_to_v4(self) -> None:
        """Sets Fortification Level to Segment02."""
        self.set_to_v3()

        self.thunderclap: CombatAction = ThunderclapV4()

    def set_to_v5(self) -> None:
        """Sets Fortification Level to Segment05."""
        self.set_to_v4()

        self.lightning_smash: CombatAction = LightningSmashV5()

    def set_to_v6(self) -> None:
        """Sets Fortification Level to Segment06."""
        self.set_to_v5()

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
                self.set_to_v6()
