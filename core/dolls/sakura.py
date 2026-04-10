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
from core.combat import DamageInstance, CombatAction


class SakuraChime(CombatAction):
    """Sakura Basic Attack."""

    @override
    def execute(self) -> DamageInstance:
        label: str = "Sakura Chime"
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
            group_name="Sakura Chime",
        )


class FallingBlossom(CombatAction):
    """Sakura S1."""

    @override
    def execute(self) -> DamageInstance:
        label: str = "Falling Blossom"
        base_potency: int = 60
        tags: set[DamageTag] = {
            DamageTag.ACTIVE,
            DamageTag.BURN,
            DamageTag.PHASE,
            DamageTag.AREA_OF_EFFECT,
            DamageTag.CONFECTANCE,
        }

        return DamageInstance(
            label=label,
            base_potency=base_potency,
            tags=tags,
            group_name="Falling Blossom",
        )


class FallingBlossomV2(CombatAction):
    """Sakura S1 (V2)."""

    @override
    def execute(self) -> DamageInstance:
        label: str = "Falling Blossom"
        base_potency: int = 75
        tags: set[DamageTag] = {
            DamageTag.ACTIVE,
            DamageTag.BURN,
            DamageTag.PHASE,
            DamageTag.AREA_OF_EFFECT,
            DamageTag.CONFECTANCE,
        }

        return DamageInstance(
            label=label,
            base_potency=base_potency,
            tags=tags,
            group_name="Falling Blossom",
        )


class MisfortuneDelivery(CombatAction):
    """Sakura S2."""

    @override
    def execute(self) -> DamageInstance:
        label: str = "Misfortune Delivery"
        base_potency: int = 130
        tags: set[DamageTag] = {
            DamageTag.ACTIVE,
            DamageTag.BURN,
            DamageTag.PHASE,
            DamageTag.LIGHT_AMMO,
            DamageTag.TARGETED,
            DamageTag.CONFECTANCE,
        }

        return DamageInstance(
            label=label,
            base_potency=base_potency,
            tags=tags,
            group_name="Misfortune Delivery",
        )


class GrandIsekaiAdventure(CombatAction):
    """Sakura Ultimate."""

    @override
    def execute(self) -> DamageInstance:
        label: str = "Grand Isekai Adventure"
        base_potency: int = 90
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
            group_name="Grand Isekai Adventure",
        )


class GrandIsekaiAdventureV5(CombatAction):
    """Sakura Ultimate."""

    @override
    def execute(self) -> DamageInstance:
        label: str = "Grand Isekai Adventure"
        base_potency: int = 120
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
            group_name="Grand Isekai Adventure",
        )


class SakuraMark(CombatAction):
    """Sakura mark effect. Triggers when the holder takes Burn damage."""

    @override
    def execute(
        self, target_has_bad_luck: bool, target_is_on_burn_tile: bool
    ) -> DamageInstance:
        label: str = "Sakura Mark"
        base_potency: int = 60

        tags: set[DamageTag] = {
            DamageTag.PASSIVE,
            DamageTag.BURN,
            DamageTag.PHASE,
            DamageTag.AREA_OF_EFFECT,
        }

        buffs_before: list[Buff] = []
        debuffs_before: list[Debuff] = []

        # Bad Luck: Damage taken from Sakura Mark is increased by 10%
        if target_has_bad_luck:
            debuffs_before.append(
                Debuff(
                    value=10,
                    modifier_type=ModifierType.ADDITIVE,
                    stat_type=SpecialAttribute.INCREASE_DAMAGE_TAKEN,
                    tag=DamageTag.ALL,
                )
            )

        return DamageInstance(
            label=label,
            base_potency=base_potency,
            tags=tags,
            group_name="Sakura Mark",
            debuffs_before=debuffs_before,
            buffs_before=buffs_before,
        )


class SakuraMarkV1(CombatAction):
    """Sakura mark effect. Triggers when the holder takes Burn damage."""

    @override
    def execute(
        self, target_has_bad_luck: bool, target_is_on_burn_tile: bool
    ) -> DamageInstance:
        label: str = "Sakura Mark"
        base_potency: int = 90

        tags: set[DamageTag] = {
            DamageTag.PASSIVE,
            DamageTag.BURN,
            DamageTag.PHASE,
            DamageTag.AREA_OF_EFFECT,
        }

        buffs_before: list[Buff] = []
        debuffs_before: list[Debuff] = []

        # Bad Luck: Damage taken from Sakura Mark is increased by 10%
        if target_has_bad_luck:
            debuffs_before.append(
                Debuff(
                    value=10,
                    modifier_type=ModifierType.ADDITIVE,
                    stat_type=SpecialAttribute.INCREASE_DAMAGE_TAKEN,
                    tag=DamageTag.ALL,
                )
            )

        # If the target is on a burn tile, the damage dealt by Sakura Mark is increased by 30%
        if target_is_on_burn_tile:
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
            group_name="Sakura Mark",
            debuffs_before=debuffs_before,
            buffs_before=buffs_before,
        )


class SakuraMarkV3(CombatAction):
    """Sakura mark effect. Triggers when the holder takes Burn damage."""

    @override
    def execute(
        self, target_has_bad_luck: bool, target_is_on_burn_tile: bool
    ) -> DamageInstance:
        label: str = "Sakura Mark"
        base_potency: int = 90

        tags: set[DamageTag] = {
            DamageTag.PASSIVE,
            DamageTag.BURN,
            DamageTag.PHASE,
            DamageTag.AREA_OF_EFFECT,
        }

        buffs_before: list[Buff] = []
        debuffs_before: list[Debuff] = []

        # Bad Luck: Damage taken from Sakura Mark is increased by 10%
        if target_has_bad_luck:
            debuffs_before.append(
                Debuff(
                    value=10,
                    modifier_type=ModifierType.ADDITIVE,
                    stat_type=SpecialAttribute.INCREASE_DAMAGE_TAKEN,
                    tag=DamageTag.ALL,
                )
            )

        # If the target is on a burn tile, the damage dealt by Sakura Mark is increased by 30%
        if target_is_on_burn_tile:
            buffs_before.append(
                Buff(
                    value=30,
                    modifier_type=ModifierType.ADDITIVE,
                    stat_type=SpecialAttribute.DAMAGE_BOOST,
                    tag=DamageTag.ALL,
                )
            )

        # When Sakura Mark deals damage, it ignores 15% of the target's defense.
        buffs_before.append(
            Buff(
                value=15,
                modifier_type=ModifierType.ADDITIVE,
                stat_type=SpecialAttribute.DEFENSE_IGNORE,
                tag=DamageTag.ALL,
            )
        )

        return DamageInstance(
            label=label,
            base_potency=base_potency,
            tags=tags,
            group_name="Sakura Mark",
            debuffs_before=debuffs_before,
            buffs_before=buffs_before,
        )


class SakuraMarkV4(CombatAction):
    """Sakura mark effect. Triggers when the holder takes Burn damage."""

    @override
    def execute(
        self, target_has_bad_luck: bool, target_is_on_burn_tile: bool
    ) -> DamageInstance:
        label: str = "Sakura Mark"
        base_potency: int = 90

        tags: set[DamageTag] = {
            DamageTag.PASSIVE,
            DamageTag.BURN,
            DamageTag.PHASE,
            DamageTag.AREA_OF_EFFECT,
        }

        buffs_before: list[Buff] = []
        debuffs_before: list[Debuff] = []

        # Bad Luck: Damage taken from Sakura Mark is increased by 30%
        if target_has_bad_luck:
            debuffs_before.append(
                Debuff(
                    value=30,
                    modifier_type=ModifierType.ADDITIVE,
                    stat_type=SpecialAttribute.INCREASE_DAMAGE_TAKEN,
                    tag=DamageTag.ALL,
                )
            )

        # If the target is on a burn tile, the damage dealt by Sakura Mark is increased by 30%
        if target_is_on_burn_tile:
            buffs_before.append(
                Buff(
                    value=30,
                    modifier_type=ModifierType.ADDITIVE,
                    stat_type=SpecialAttribute.DAMAGE_BOOST,
                    tag=DamageTag.ALL,
                )
            )

        # When Sakura Mark deals damage, it ignores 15% of the target's defense.
        buffs_before.append(
            Buff(
                value=15,
                modifier_type=ModifierType.ADDITIVE,
                stat_type=SpecialAttribute.DEFENSE_IGNORE,
                tag=DamageTag.ALL,
            )
        )

        return DamageInstance(
            label=label,
            base_potency=base_potency,
            tags=tags,
            group_name="Sakura Mark",
            debuffs_before=debuffs_before,
            buffs_before=buffs_before,
        )


class Sakura(Doll):
    """Sakura."""

    name: str = "Sakura"
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
            DamageTag.SUPPORT_ACTION,
            DamageTag.INTERCEPTION,
            DamageTag.COUNTERATTACK,
            DamageTag.PHYSICAL_SUMMON,
            DamageTag.FIXED,
        ]
    )

    sakura_chime: CombatAction = Field(default_factory=SakuraChime)
    falling_blossom: CombatAction = Field(default_factory=FallingBlossom)
    misfortune_delivery: CombatAction = Field(default_factory=MisfortuneDelivery)
    grand_isekai_adventure: CombatAction = Field(default_factory=GrandIsekaiAdventure)
    sakura_mark: CombatAction = Field(default_factory=SakuraMark)

    def set_to_v0(self) -> None:
        """Sets Fortification Level to Segment00."""
        self.sakura_chime: CombatAction = SakuraChime()
        self.falling_blossom: CombatAction = FallingBlossom()
        self.misfortune_delivery: CombatAction = MisfortuneDelivery()
        self.grand_isekai_adventure: CombatAction = GrandIsekaiAdventure()
        self.sakura_mark: CombatAction = SakuraMark()

    def set_to_v1(self) -> None:
        """Sets Fortification Level to Segment01."""
        self.set_to_v0()

        self.sakura_mark: CombatAction = SakuraMarkV1()

    def set_to_v2(self) -> None:
        """Sets Fortification Level to Segment02."""
        self.set_to_v0()

        self.falling_blossom: CombatAction = FallingBlossomV2()

    def set_to_v3(self) -> None:
        """Sets Fortification Level to Segment03."""
        self.set_to_v2()

        self.sakura_mark: CombatAction = SakuraMarkV3()

    def set_to_v4(self) -> None:
        """Sets Fortification Level to Segment04."""
        self.set_to_v3()

        self.sakura_mark: CombatAction = SakuraMarkV4()

    def set_to_v5(self) -> None:
        """Sets Fortification Level to Segment05."""
        self.set_to_v4()

        self.grand_isekai_adventure: CombatAction = GrandIsekaiAdventureV5()

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
