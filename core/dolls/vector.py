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
from core.combat import DamageInstance, CombatAction, FixedDamageInstance


class DepressiveMentality(CombatAction):
    """Vector Basic Attack."""

    @override
    def execute(self) -> DamageInstance:
        label: str = "Depressive Mentality"
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
            group_name="Depressive Mentality",
        )


class DeadEndMeltdown(CombatAction):
    """Vector S1."""

    @override
    def execute(self) -> DamageInstance:
        label: str = "Dead End Meltdown"
        base_potency: int = 120
        tags: set[DamageTag] = {
            DamageTag.ACTIVE,
            DamageTag.BURN,
            DamageTag.PHASE,
            DamageTag.TARGETED,
            DamageTag.LIGHT_AMMO,
        }

        return DamageInstance(
            label=label,
            base_potency=base_potency,
            tags=tags,
            group_name="Dead End Meltdown",
        )


class DeadEndMeltdownFixed(CombatAction):
    """Vector S1 with fixed potency."""

    @override
    def execute(self) -> DamageInstance:
        label: str = "Dead End Meltdown (Fixed)"
        base_potency: int = 50

        return FixedDamageInstance(
            label=label,
            base_potency=base_potency,
            group_name="Dead End Meltdown (Fixed)",
        )


class DeadEndMeltdownV3(CombatAction):
    """Vector S1 (V3)."""

    @override
    def execute(self) -> DamageInstance:
        label: str = "Dead End Meltdown"
        base_potency: int = 150
        tags: set[DamageTag] = {
            DamageTag.ACTIVE,
            DamageTag.BURN,
            DamageTag.PHASE,
            DamageTag.TARGETED,
            DamageTag.LIGHT_AMMO,
        }

        return DamageInstance(
            label=label,
            base_potency=base_potency,
            tags=tags,
            group_name="Dead End Meltdown",
        )


class DeadEndMeltdownFixedV3(CombatAction):
    """Vector S1 with fixed potency."""

    @override
    def execute(self) -> DamageInstance:
        label: str = "Dead End Meltdown (Fixed)"
        base_potency: int = 80

        return FixedDamageInstance(
            label=label,
            base_potency=base_potency,
            group_name="Dead End Meltdown (Fixed)",
        )


class PortentOfDoom(CombatAction):
    """Vector S2."""

    @override
    def execute(self) -> DamageInstance:
        label: str = "Portent of Doom"
        base_potency: int = 100
        tags: set[DamageTag] = {
            DamageTag.ACTIVE,
            DamageTag.BURN,
            DamageTag.PHASE,
            DamageTag.TARGETED,
        }

        return DamageInstance(
            label=label,
            base_potency=base_potency,
            tags=tags,
            group_name="Portent of Doom",
        )


class PortentOfDoomV4(CombatAction):
    """Vector S2."""

    @override
    def execute(self) -> DamageInstance:
        label: str = "Portent of Doom"
        base_potency: int = 130
        tags: set[DamageTag] = {
            DamageTag.ACTIVE,
            DamageTag.BURN,
            DamageTag.PHASE,
            DamageTag.TARGETED,
        }

        return DamageInstance(
            label=label,
            base_potency=base_potency,
            tags=tags,
            group_name="Portent of Doom",
        )


class SearingFinale(CombatAction):
    """Vector Ultimate."""

    @override
    def execute(self) -> DamageInstance:
        label: str = "Searing Finale"
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
            group_name="Searing Finale",
        )


class EmergencySupport(CombatAction):
    """Support action when an enemy is inflicted with Overburn. Granted by Fixed Key 6 - Negative Motivation."""

    @override
    def execute(self) -> DamageInstance:
        label: str = "Emergency Support"
        base_potency: int = 60

        tags: set[DamageTag] = {
            DamageTag.PASSIVE,
            DamageTag.SUPPORT_ACTION,
            DamageTag.PHASE,
            DamageTag.BURN,
            DamageTag.LIGHT_AMMO,
            DamageTag.TARGETED,
        }

        return DamageInstance(
            label=label,
            base_potency=base_potency,
            tags=tags,
            group_name="Emergency Support",
        )


class OverheatCombustion(CombatAction):
    """Fixed damage effect from Overheat Combustion debuff. Triggered up on application and the beginning of the holder's turn. Damage instance is the same for both triggers."""

    @override
    def execute(
        self,
    ) -> DamageInstance:
        label: str = "Overheat Combustion"
        base_potency: int = 20

        return FixedDamageInstance(
            label=label,
            base_potency=base_potency,
            group_name="Overheat Combustion",
        )


class OverheatCombustionV5(CombatAction):
    """Fixed damage effect from Overheat Combustion debuff. Triggered up on application and the beginning of the holder's turn. Damage instance is the same for both triggers."""

    @override
    def execute(
        self,
    ) -> DamageInstance:
        label: str = "Overheat Combustion"
        base_potency: int = 30

        return FixedDamageInstance(
            label=label,
            base_potency=base_potency,
            group_name="Overheat Combustion",
        )


class Vector(Doll):
    """Vector."""

    name: str = "Vector"
    irrelevant_damage_tags: ClassVar[set[DamageTag]] = set(
        [
            DamageTag.CORROSION,
            DamageTag.ELECTRIC,
            DamageTag.HYDRO,
            DamageTag.FREEZE,
            DamageTag.MEDIUM_AMMO,
            DamageTag.HEAVY_AMMO,
            DamageTag.SHOTGUN_AMMO,
            DamageTag.MELEE,
            DamageTag.INTERCEPTION,
            DamageTag.COUNTERATTACK,
            DamageTag.PHYSICAL_SUMMON,
        ]
    )

    depressive_mentality: CombatAction = Field(default_factory=DepressiveMentality)
    dead_end_meltdown: CombatAction = Field(default_factory=DeadEndMeltdown)
    dead_end_meltdown_fixed: CombatAction = Field(default_factory=DeadEndMeltdownFixed)
    portent_of_doom: CombatAction = Field(default_factory=PortentOfDoom)
    searing_finale: CombatAction = Field(default_factory=SearingFinale)
    emergency_support: CombatAction = Field(default_factory=EmergencySupport)
    overheat_combustion: CombatAction = Field(default_factory=OverheatCombustion)

    def set_to_v0(self) -> None:
        """Sets Fortification Level to Segment00."""
        self.depressive_mentality: CombatAction = DepressiveMentality()
        self.dead_end_meltdown: CombatAction = DeadEndMeltdown()
        self.dead_end_meltdown_fixed: CombatAction = DeadEndMeltdownFixed()
        self.portent_of_doom: CombatAction = PortentOfDoom()
        self.searing_finale: CombatAction = SearingFinale()
        self.emergency_support: CombatAction = EmergencySupport()
        self.overheat_combustion: CombatAction = OverheatCombustion()

        # Passive: Perception Block
        # At the start of the turn, if Confectance Index is at maximum, Vector consumes all
        # points of Confectance Index to increase attack by 10% until the end of the round.
        # Assume it is always active for simplicity.
        self.multiplicative_modifiers.basic_attributes[StatType.ATTACK] = 10

    def set_to_v3(self) -> None:
        """Sets Fortification Level to Segment03."""
        self.set_to_v0()

        self.dead_end_meltdown: CombatAction = DeadEndMeltdownV3()
        self.dead_end_meltdown_fixed: CombatAction = DeadEndMeltdownFixedV3()

    def set_to_v4(self) -> None:
        """Sets Fortification Level to Segment04."""
        self.set_to_v3()

        self.portent_of_doom: CombatAction = PortentOfDoomV4()

    def set_to_v5(self) -> None:
        """Sets Fortification Level to Segment05."""
        self.set_to_v4()

        self.overheat_combustion: CombatAction = OverheatCombustionV5()

        # Passive: Perception Block
        # At the start of the turn, if Confectance Index is at maximum, Vector consumes all
        # points of Confectance Index to increase attack by 10% until the end of the round.
        # At the start of the turn, for each point of Confectance Index above the maximum,
        # further increases the attack by 10%, up to 20%.
        # Assume it is always active for simplicity.
        self.multiplicative_modifiers.basic_attributes[StatType.ATTACK] = 20

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
