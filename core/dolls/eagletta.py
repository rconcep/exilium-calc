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
from core.buffs import Buff
from core.combat import DamageInstance, CombatAction


class RendingTalons(CombatAction):
    """Eagletta basic attack while in Heavy Talons stance."""

    @override
    def execute(self, feathers_of_war_expended: int) -> DamageInstance:
        label: str = f"Rending Talons ({feathers_of_war_expended} Feathers)"
        base_potency: int = 60
        tags: set[DamageTag] = {
            DamageTag.ACTIVE,
            DamageTag.BASIC,
            DamageTag.MELEE,
            DamageTag.TARGETED,
            DamageTag.FREEZE,
            DamageTag.PHASE,
        }

        buffs_before: list[Buff] = []

        # Ignores 5% of the target's defense.
        buffs_before.append(
            Buff(
                value=5,
                modifier_type=ModifierType.ADDITIVE,
                stat_type=SpecialAttribute.DEFENSE_IGNORE,
                tag=DamageTag.ALL,
            )
        )

        # Heavy Talons stance effect: for each point of Feathers of War expended in the current round,
        # the damage multiplier is increased by 5%.
        potency_per_feather_expended: int = 5
        base_potency += potency_per_feather_expended * max(0, feathers_of_war_expended)

        return DamageInstance(
            label=label,
            base_potency=base_potency,
            tags=tags,
            group_name="Rending Talons",
            buffs_before=buffs_before,
        )


class RendingTalonsV2(CombatAction):
    """Eagletta basic attack while in Heavy Talons stance (V2)."""

    @override
    def execute(self, feathers_of_war_expended: int) -> DamageInstance:
        label: str = f"Rending Talons ({feathers_of_war_expended} Feathers)"
        base_potency: int = 80
        tags: set[DamageTag] = {
            DamageTag.ACTIVE,
            DamageTag.BASIC,
            DamageTag.MELEE,
            DamageTag.TARGETED,
            DamageTag.FREEZE,
            DamageTag.PHASE,
        }

        buffs_before: list[Buff] = []

        # Ignores 5% of the target's defense.
        buffs_before.append(
            Buff(
                value=5,
                modifier_type=ModifierType.ADDITIVE,
                stat_type=SpecialAttribute.DEFENSE_IGNORE,
                tag=DamageTag.ALL,
            )
        )

        # Heavy Talons stance effect: for each point of Feathers of War expended in the current round,
        # the damage multiplier is increased by 5%.
        potency_per_feather_expended: int = 5
        base_potency += potency_per_feather_expended * max(0, feathers_of_war_expended)

        return DamageInstance(
            label=label,
            base_potency=base_potency,
            tags=tags,
            group_name="Rending Talons",
            buffs_before=buffs_before,
        )


class RendingTalonsV6(CombatAction):
    """Eagletta basic attack while in Heavy Talons stance (V6)."""

    @override
    def execute(self, feathers_of_war_expended: int) -> DamageInstance:
        label: str = f"Rending Talons ({feathers_of_war_expended} Feathers)"
        base_potency: int = 80
        tags: set[DamageTag] = {
            DamageTag.ACTIVE,
            DamageTag.BASIC,
            DamageTag.MELEE,
            DamageTag.TARGETED,
            DamageTag.FREEZE,
            DamageTag.PHASE,
        }

        buffs_before: list[Buff] = []

        # Ignores 10% of the target's defense.
        buffs_before.append(
            Buff(
                value=10,
                modifier_type=ModifierType.ADDITIVE,
                stat_type=SpecialAttribute.DEFENSE_IGNORE,
                tag=DamageTag.ALL,
            )
        )

        # Heavy Talons stance effect: for each point of Feathers of War expended in the current round,
        # the damage multiplier is increased by 10%.
        potency_per_feather_expended: int = 10
        base_potency += potency_per_feather_expended * max(0, feathers_of_war_expended)

        return DamageInstance(
            label=label,
            base_potency=base_potency,
            tags=tags,
            group_name="Rending Talons",
            buffs_before=buffs_before,
        )


class SwiftEagleStrike(CombatAction):
    """Eagletta basic attack while in Eagle Strike stance."""

    @override
    def execute(self) -> DamageInstance:
        label: str = "Swift Eagle Strike"
        base_potency: int = 100
        tags: set[DamageTag] = {
            DamageTag.ACTIVE,
            DamageTag.BASIC,
            DamageTag.LIGHT_AMMO,
            DamageTag.TARGETED,
            DamageTag.FREEZE,
            DamageTag.PHASE,
        }

        buffs_before: list[Buff] = []

        # The damage dealt is increased by 15%.
        buffs_before.append(
            Buff(
                value=15,
                modifier_type=ModifierType.ADDITIVE,
                stat_type=SpecialAttribute.DAMAGE_BOOST,
                tag=DamageTag.ALL,
            )
        )

        # And critical damage is increased by 5%.
        buffs_before.append(
            Buff(
                value=5,
                modifier_type=ModifierType.ADDITIVE,
                stat_type=SpecialAttribute.CRITICAL_DAMAGE,
                tag=DamageTag.ALL,
            )
        )

        return DamageInstance(
            label=label,
            base_potency=base_potency,
            tags=tags,
            group_name="Swift Eagle Strike",
            buffs_before=buffs_before,
        )


class SwiftEagleStrikeV2(CombatAction):
    """Eagletta basic attack while in Eagle Strike stance (V2)."""

    @override
    def execute(self) -> DamageInstance:
        label: str = "Swift Eagle Strike"
        base_potency: int = 120
        tags: set[DamageTag] = {
            DamageTag.ACTIVE,
            DamageTag.BASIC,
            DamageTag.LIGHT_AMMO,
            DamageTag.TARGETED,
            DamageTag.FREEZE,
            DamageTag.PHASE,
        }

        buffs_before: list[Buff] = []

        # The damage dealt is increased by 25%.
        buffs_before.append(
            Buff(
                value=25,
                modifier_type=ModifierType.ADDITIVE,
                stat_type=SpecialAttribute.DAMAGE_BOOST,
                tag=DamageTag.ALL,
            )
        )

        # And critical damage is increased by 10%.
        buffs_before.append(
            Buff(
                value=10,
                modifier_type=ModifierType.ADDITIVE,
                stat_type=SpecialAttribute.CRITICAL_DAMAGE,
                tag=DamageTag.ALL,
            )
        )

        return DamageInstance(
            label=label,
            base_potency=base_potency,
            tags=tags,
            group_name="Swift Eagle Strike",
            buffs_before=buffs_before,
        )


class SwiftEagleStrikeV6(CombatAction):
    """Eagletta basic attack while in Eagle Strike stance (V6)."""

    @override
    def execute(self) -> DamageInstance:
        label: str = "Swift Eagle Strike"
        base_potency: int = 150
        tags: set[DamageTag] = {
            DamageTag.ACTIVE,
            DamageTag.BASIC,
            DamageTag.LIGHT_AMMO,
            DamageTag.TARGETED,
            DamageTag.FREEZE,
            DamageTag.PHASE,
        }

        buffs_before: list[Buff] = []

        # The damage dealt is increased by 40%.
        buffs_before.append(
            Buff(
                value=40,
                modifier_type=ModifierType.ADDITIVE,
                stat_type=SpecialAttribute.DAMAGE_BOOST,
                tag=DamageTag.ALL,
            )
        )

        # And critical damage is increased by 15%.
        buffs_before.append(
            Buff(
                value=15,
                modifier_type=ModifierType.ADDITIVE,
                stat_type=SpecialAttribute.CRITICAL_DAMAGE,
                tag=DamageTag.ALL,
            )
        )

        return DamageInstance(
            label=label,
            base_potency=base_potency,
            tags=tags,
            group_name="Swift Eagle Strike",
            buffs_before=buffs_before,
        )


class StoopStrike(CombatAction):
    """Eagletta S2."""

    @override
    def execute(self) -> DamageInstance:
        label: str = "Stoop Strike"
        base_potency: int = 100
        tags: set[DamageTag] = {
            DamageTag.ACTIVE,
            DamageTag.LIGHT_AMMO,
            DamageTag.TARGETED,
            DamageTag.FREEZE,
            DamageTag.PHASE,
        }

        return DamageInstance(
            label=label,
            base_potency=base_potency,
            tags=tags,
            group_name="Stoop Strike",
        )


class StoopStrikeV3(CombatAction):
    """Eagletta S2 (V3)."""

    @override
    def execute(self) -> DamageInstance:
        label: str = "Stoop Strike"
        base_potency: int = 120
        tags: set[DamageTag] = {
            DamageTag.ACTIVE,
            DamageTag.LIGHT_AMMO,
            DamageTag.TARGETED,
            DamageTag.FREEZE,
            DamageTag.PHASE,
        }

        return DamageInstance(
            label=label,
            base_potency=base_potency,
            tags=tags,
            group_name="Stoop Strike",
        )


class FeatherstormFeast(CombatAction):
    """Eagletta Ultimate."""

    @override
    def execute(
        self,
        feathers_of_war_expended: int,
        triggered_by_swift_eagle_strike: bool,
    ) -> DamageInstance:
        label: str = f"Featherstorm Feast ({feathers_of_war_expended} Feathers)"
        base_potency: int = 120
        tags: set[DamageTag] = {
            DamageTag.ACTIVE,
            DamageTag.FREEZE,
            DamageTag.PHASE,
            DamageTag.LIGHT_AMMO,
            DamageTag.TARGETED,
            DamageTag.ULTIMATE,
        }

        if triggered_by_swift_eagle_strike:
            # Considered a basic attack (TODO: still Ultimate or?)
            tags.add(DamageTag.BASIC)

        buffs_before: list[Buff] = []

        # Expends all Feathers of War, applying different effects based on the number of feathers expended.
        # TODO: Not sure if the effects are cumulative. Since they don't overlap, will assume they are cumulative.
        if feathers_of_war_expended > 0:
            # 1 Feather: damage dealt is increased by 20%.
            buffs_before.append(
                Buff(
                    20,
                    ModifierType.ADDITIVE,
                    SpecialAttribute.DAMAGE_BOOST,
                    DamageTag.ALL,
                )
            )

        if feathers_of_war_expended > 1:
            # 2 Feathers: critical damage is increased by 35% and
            # stability damage dealt is increased by 4 points. (not modeled)
            buffs_before.append(
                Buff(
                    35,
                    ModifierType.ADDITIVE,
                    SpecialAttribute.CRITICAL_DAMAGE,
                    DamageTag.ALL,
                )
            )

        if feathers_of_war_expended > 2:
            # 3 Feathers: damage multiplier is increased by 50% and
            # attack is increased by 10%.
            base_potency += 50
            buffs_before.append(
                Buff(
                    10,
                    ModifierType.MULTIPLICATIVE,
                    StatType.ATTACK,
                    DamageTag.ALL,
                )
            )

        return DamageInstance(
            label=label,
            base_potency=base_potency,
            tags=tags,
            group_name="Featherstorm Feast",
            buffs_before=buffs_before,
        )


class FeatherstormFeastV4(CombatAction):
    """Eagletta Ultimate (V4)."""

    @override
    def execute(
        self,
        feathers_of_war_expended: int,
        triggered_by_swift_eagle_strike: bool,
    ) -> DamageInstance:
        label: str = f"Featherstorm Feast ({feathers_of_war_expended} Feathers)"
        base_potency: int = 120
        tags: set[DamageTag] = {
            DamageTag.ACTIVE,
            DamageTag.FREEZE,
            DamageTag.PHASE,
            DamageTag.LIGHT_AMMO,
            DamageTag.TARGETED,
            DamageTag.ULTIMATE,
        }

        if triggered_by_swift_eagle_strike:
            # Considered a basic attack (TODO: still Ultimate or?)
            tags.add(DamageTag.BASIC)

        buffs_before: list[Buff] = []

        # Expends all Feathers of War, applying different effects based on the number of feathers expended.
        # TODO: Not sure if the effects are cumulative. Since they don't overlap, will assume they are cumulative.
        if feathers_of_war_expended > 0:
            # 1 Feather: damage dealt is increased by 30%.
            buffs_before.append(
                Buff(
                    30,
                    ModifierType.ADDITIVE,
                    SpecialAttribute.DAMAGE_BOOST,
                    DamageTag.ALL,
                )
            )

        if feathers_of_war_expended > 1:
            # 2 Feathers: critical damage is increased by 45% and
            # stability damage dealt is increased by 4 points. (not modeled)
            buffs_before.append(
                Buff(
                    45,
                    ModifierType.ADDITIVE,
                    SpecialAttribute.CRITICAL_DAMAGE,
                    DamageTag.ALL,
                )
            )

        if feathers_of_war_expended > 2:
            # 3 Feathers: damage multiplier is increased by 80% and
            # attack is increased by 20%.
            base_potency += 80
            buffs_before.append(
                Buff(
                    20,
                    ModifierType.MULTIPLICATIVE,
                    StatType.ATTACK,
                    DamageTag.ALL,
                )
            )

        return DamageInstance(
            label=label,
            base_potency=base_potency,
            tags=tags,
            group_name="Featherstorm Feast",
            buffs_before=buffs_before,
        )


class FeatherstormFeastV6(CombatAction):
    """Eagletta Ultimate (V6)."""

    @override
    def execute(
        self,
        feathers_of_war_expended: int,
        triggered_by_swift_eagle_strike: bool,
    ) -> DamageInstance:
        label: str = f"Featherstorm Feast ({feathers_of_war_expended} Feathers)"
        base_potency: int = 120
        tags: set[DamageTag] = {
            DamageTag.ACTIVE,
            DamageTag.FREEZE,
            DamageTag.PHASE,
            DamageTag.LIGHT_AMMO,
            DamageTag.TARGETED,
            DamageTag.ULTIMATE,
        }

        if triggered_by_swift_eagle_strike:
            # Considered a basic attack (TODO: still Ultimate or?)
            tags.add(DamageTag.BASIC)

        buffs_before: list[Buff] = []

        # Expends all Feathers of War, applying different effects based on the number of feathers expended.
        # TODO: Not sure if the effects are cumulative. Since they don't overlap, will assume they are cumulative.
        if feathers_of_war_expended > 0:
            # 1 Feather: damage dealt is increased by 30%.
            buffs_before.append(
                Buff(
                    30,
                    ModifierType.ADDITIVE,
                    SpecialAttribute.DAMAGE_BOOST,
                    DamageTag.ALL,
                )
            )

        if feathers_of_war_expended > 1:
            # 2 Feathers: critical damage is increased by 45% and
            # stability damage dealt is increased by 4 points. (not modeled)
            buffs_before.append(
                Buff(
                    45,
                    ModifierType.ADDITIVE,
                    SpecialAttribute.CRITICAL_DAMAGE,
                    DamageTag.ALL,
                )
            )

        if feathers_of_war_expended > 2:
            # 3 Feathers: damage multiplier is increased by 80% and
            # attack is increased by 20%.
            # TODO: V6: "passive effect added": When the Ultimate skill expends 3 points of
            # Feathers of War, the damage multiplier is increased by 30%.
            base_potency += 80 + 30
            buffs_before.append(
                Buff(
                    20,
                    ModifierType.MULTIPLICATIVE,
                    StatType.ATTACK,
                    DamageTag.ALL,
                )
            )

        return DamageInstance(
            label=label,
            base_potency=base_potency,
            tags=tags,
            group_name="Featherstorm Feast",
            buffs_before=buffs_before,
        )


class Predation(CombatAction):
    """Eagletta passive skill that performs a Lock on Attack when triggered."""

    @override
    def execute(
        self, in_heavy_talons_stance: bool, feathers_of_war_expended: int
    ) -> DamageInstance:
        base_potency: int = 60
        label: str = f"Predation ({feathers_of_war_expended} Feathers)"
        tags: set[DamageTag] = {
            DamageTag.PASSIVE,
            DamageTag.FREEZE,
            DamageTag.PHASE,
        }

        buffs_before: list[Buff] = []

        if in_heavy_talons_stance:
            # Ignores 5% of the target's defense.
            buffs_before.append(
                Buff(
                    value=5,
                    modifier_type=ModifierType.ADDITIVE,
                    stat_type=SpecialAttribute.DEFENSE_IGNORE,
                    tag=DamageTag.ALL,
                )
            )

            # For each point of Feathers of War expended in the current round,
            # the damage multiplier is increased by 5%.
            potency_per_feather_expended: int = 5
            base_potency += potency_per_feather_expended * max(
                0, feathers_of_war_expended
            )

        return DamageInstance(
            label=label,
            base_potency=base_potency,
            tags=tags,
            group_name="Predation",
            buffs_before=buffs_before,
        )


class PredationV2(CombatAction):
    """Eagletta passive skill that performs a Lock on Attack when triggered."""

    @override
    def execute(
        self, in_heavy_talons_stance: bool, feathers_of_war_expended: int
    ) -> DamageInstance:
        base_potency: int = 80
        label: str = f"Predation ({feathers_of_war_expended} Feathers)"
        tags: set[DamageTag] = {
            DamageTag.PASSIVE,
            DamageTag.FREEZE,
            DamageTag.PHASE,
        }

        buffs_before: list[Buff] = []

        if in_heavy_talons_stance:
            # Ignores 5% of the target's defense.
            buffs_before.append(
                Buff(
                    value=5,
                    modifier_type=ModifierType.ADDITIVE,
                    stat_type=SpecialAttribute.DEFENSE_IGNORE,
                    tag=DamageTag.ALL,
                )
            )

            # For each point of Feathers of War expended in the current round,
            # the damage multiplier is increased by 5%.
            potency_per_feather_expended: int = 5
            base_potency += potency_per_feather_expended * max(
                0, feathers_of_war_expended
            )

        return DamageInstance(
            label=label,
            base_potency=base_potency,
            tags=tags,
            group_name="Predation",
            buffs_before=buffs_before,
        )


class PredationV6(CombatAction):
    """Eagletta passive skill that performs a Lock on Attack when triggered."""

    @override
    def execute(
        self, in_heavy_talons_stance: bool, feathers_of_war_expended: int
    ) -> DamageInstance:
        base_potency: int = 80
        label: str = f"Predation ({feathers_of_war_expended} Feathers)"
        tags: set[DamageTag] = {
            DamageTag.PASSIVE,
            DamageTag.FREEZE,
            DamageTag.PHASE,
        }

        buffs_before: list[Buff] = []

        if in_heavy_talons_stance:
            # Ignores 10% of the target's defense.
            buffs_before.append(
                Buff(
                    value=10,
                    modifier_type=ModifierType.ADDITIVE,
                    stat_type=SpecialAttribute.DEFENSE_IGNORE,
                    tag=DamageTag.ALL,
                )
            )

            # For each point of Feathers of War expended in the current round,
            # the damage multiplier is increased by 10%.
            potency_per_feather_expended: int = 10
            base_potency += potency_per_feather_expended * max(
                0, feathers_of_war_expended
            )

        return DamageInstance(
            label=label,
            base_potency=base_potency,
            tags=tags,
            group_name="Predation",
            buffs_before=buffs_before,
        )


class Eagletta(Doll):
    """Eagletta."""

    name: str = "Eagletta"
    irrelevant_damage_tags: ClassVar[set[DamageTag]] = set(
        [
            DamageTag.PHYSICAL,
            DamageTag.CORROSION,
            DamageTag.HYDRO,
            DamageTag.ELECTRIC,
            DamageTag.BURN,
            DamageTag.MEDIUM_AMMO,
            DamageTag.HEAVY_AMMO,
            DamageTag.SHOTGUN_AMMO,
            DamageTag.SUPPORT_ACTION,
            DamageTag.COUNTERATTACK,
            DamageTag.INTERCEPTION,
            DamageTag.FIXED,
            DamageTag.PHYSICAL_SUMMON,
        ]
    )

    rending_talons: CombatAction = Field(default_factory=RendingTalons)
    swift_eagle_strike: CombatAction = Field(default_factory=SwiftEagleStrike)
    stoop_strike: CombatAction = Field(default_factory=StoopStrike)
    featherstorm_feast: CombatAction = Field(default_factory=FeatherstormFeast)
    predation: CombatAction = Field(default_factory=Predation)

    def set_to_v0(self) -> None:
        """Sets Fortification Level to Segment00."""
        self.rending_talons = RendingTalons()
        self.swift_eagle_strike = SwiftEagleStrike()
        self.stoop_strike = StoopStrike()
        self.featherstorm_feast = FeatherstormFeast()
        self.predation = Predation()

    def set_to_v2(self) -> None:
        """Sets Fortification Level to Segment02."""
        self.set_to_v0()

        self.rending_talons: CombatAction = RendingTalonsV2()
        self.swift_eagle_strike: CombatAction = SwiftEagleStrikeV2()
        self.predation: CombatAction = PredationV2()

    def set_to_v3(self) -> None:
        """Sets Fortification Level to Segment03."""
        self.set_to_v2()

        self.stoop_strike: CombatAction = StoopStrikeV3()

    def set_to_v4(self) -> None:
        """Sets Fortification Level to Segment04."""
        self.set_to_v3()

        self.featherstorm_feast: CombatAction = FeatherstormFeastV4()

    def set_to_v6(self) -> None:
        """Sets Fortification Level to Segment06."""
        self.set_to_v4()

        self.rending_talons: CombatAction = RendingTalonsV6()
        self.swift_eagle_strike: CombatAction = SwiftEagleStrikeV6()
        self.featherstorm_feast: CombatAction = FeatherstormFeastV6()
        self.predation: CombatAction = PredationV6()

    @override
    def set_fortification_level(self, level: FortificationLevel):
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
                self.set_to_v4()
            case FortificationLevel.SEGMENT05:
                self.set_to_v4()
            case FortificationLevel.SEGMENT06:
                self.set_to_v6()
