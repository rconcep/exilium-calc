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


# Analysis Score
# V1: When dealing damage, for every 10% of the target's Analysis Score, critical damage is increased by 5%. (Passive)
# Innate: When Cheyanne attacks, if the target's Analysis Score is >= 50%, critical damage is increased by 30%. If < 50%, critical damage is increased by 10%
def get_analysis_score_buff(analysis_score: int) -> Buff:
    """Returns the critical damage buff corresponding to the effect of Analysis Score.

    Arguments:
        analysis_score: The target's Analysis Score as a percentage (0-100).
    """
    return Buff(
        value=30 if analysis_score >= 50 else 10,
        modifier_type=ModifierType.ADDITIVE,
        stat_type=SpecialAttribute.CRITICAL_DAMAGE,
        tag=DamageTag.ALL,
    )


def get_analysis_score_buffV1(analysis_score: int) -> Buff:
    """Returns the critical damage buff corresponding to the effect of Analysis Score
    in addition to the effect from Cheyanne's passive.

    Arguments:
        analysis_score: The target's Analysis Score as a percentage (0-100).
    """
    passive_buff_value: int = (analysis_score // 10) * 5

    return Buff(
        value=(30 if analysis_score >= 50 else 10) + passive_buff_value,
        modifier_type=ModifierType.ADDITIVE,
        stat_type=SpecialAttribute.CRITICAL_DAMAGE,
        tag=DamageTag.ALL,
    )


class DefinitelyNot360NoScope(CombatAction):
    """Cheyanne basic attack."""

    @override
    def execute(self, analysis_score: int) -> DamageInstance:
        label: str = "Definitely Not 360 NoScope"
        base_potency: int = 80
        tags: set[DamageTag] = {
            DamageTag.ACTIVE,
            DamageTag.BASIC,
            DamageTag.HEAVY_AMMO,
            DamageTag.TARGETED,
            DamageTag.PHYSICAL,
        }

        analysis_score_buff: Buff = get_analysis_score_buff(analysis_score)

        return DamageInstance(
            label=label,
            base_potency=base_potency,
            tags=tags,
            buffs_before=[analysis_score_buff],
            group_name="Definitely Not 360 NoScope",
        )


class DefinitelyNot360NoScopeV1(CombatAction):
    """Cheyanne basic attack (V1)."""

    @override
    def execute(self, analysis_score: int) -> DamageInstance:
        label: str = "Definitely Not 360 NoScope"
        base_potency: int = 80
        tags: set[DamageTag] = {
            DamageTag.ACTIVE,
            DamageTag.BASIC,
            DamageTag.HEAVY_AMMO,
            DamageTag.TARGETED,
            DamageTag.PHYSICAL,
        }

        analysis_score_buff: Buff = get_analysis_score_buffV1(analysis_score)

        return DamageInstance(
            label=label,
            base_potency=base_potency,
            tags=tags,
            buffs_before=[analysis_score_buff],
            group_name="Definitely Not 360 NoScope",
        )


class FocusedPursuit(CombatAction):
    """Cheyanne S2."""

    @override
    def execute(self, analysis_score: int) -> DamageInstance:
        label: str = "Focused Pursuit"
        base_potency: int = 80
        tags: set[DamageTag] = {
            DamageTag.ACTIVE,
            DamageTag.HEAVY_AMMO,
            DamageTag.TARGETED,
            DamageTag.PHYSICAL,
        }

        analysis_score_buff: Buff = get_analysis_score_buff(analysis_score)

        return DamageInstance(
            label=label,
            base_potency=base_potency,
            tags=tags,
            group_name="Focused Pursuit",
            buffs_before=[analysis_score_buff],
        )


class FocusedPursuitV1(CombatAction):
    """Cheyanne S2 (V1)."""

    @override
    def execute(self, analysis_score: int) -> DamageInstance:
        label: str = "Focused Pursuit"
        base_potency: int = 80
        tags: set[DamageTag] = {
            DamageTag.ACTIVE,
            DamageTag.HEAVY_AMMO,
            DamageTag.TARGETED,
            DamageTag.PHYSICAL,
        }

        analysis_score_buff: Buff = get_analysis_score_buffV1(analysis_score)

        return DamageInstance(
            label=label,
            base_potency=base_potency,
            tags=tags,
            group_name="Focused Pursuit",
            buffs_before=[analysis_score_buff],
        )


class Heavenpierce(CombatAction):
    """Cheyanne Ultimate."""

    @override
    def execute(
        self,
        target_has_bullseye: bool,
        few_enemies_with_low_analysis_score: bool,
        stacks_of_prepared_stance: int,
    ) -> DamageInstance:
        label: str = "Heavenpierce"
        base_potency: int = 200
        tags: set[DamageTag] = {
            DamageTag.ACTIVE,
            DamageTag.PHYSICAL,
            DamageTag.HEAVY_AMMO,
            DamageTag.TARGETED,
            DamageTag.CONFECTANCE,
            DamageTag.ULTIMATE,
        }

        buffs_before: list[Buff] = []

        # Resets the target's Analysis Score to 100%
        reset_analysis_score: int = 100
        analysis_score_buff: Buff = get_analysis_score_buff(reset_analysis_score)
        buffs_before.append(analysis_score_buff)

        # If the target has Bullseye, then the critical damage is increased by 30%.
        if target_has_bullseye:
            buffs_before.append(
                Buff(
                    value=30,
                    modifier_type=ModifierType.ADDITIVE,
                    stat_type=SpecialAttribute.CRITICAL_DAMAGE,
                    tag=DamageTag.ALL,
                )
            )

        return DamageInstance(
            label=label,
            base_potency=base_potency,
            tags=tags,
            group_name="Heavenpierce",
            buffs_before=buffs_before,
        )


class HeavenpierceV1(CombatAction):
    """Cheyanne Ultimate (V1)."""

    @override
    def execute(
        self,
        target_has_bullseye: bool,
        few_enemies_with_low_analysis_score: bool,
        stacks_of_prepared_stance: int,
    ) -> DamageInstance:
        label: str = "Heavenpierce"
        base_potency: int = 200
        tags: set[DamageTag] = {
            DamageTag.ACTIVE,
            DamageTag.PHYSICAL,
            DamageTag.HEAVY_AMMO,
            DamageTag.TARGETED,
            DamageTag.CONFECTANCE,
            DamageTag.ULTIMATE,
        }

        buffs_before: list[Buff] = []

        # Resets the target's Analysis Score to 100%
        reset_analysis_score: int = 100
        analysis_score_buff: Buff = get_analysis_score_buffV1(reset_analysis_score)
        buffs_before.append(analysis_score_buff)

        # If the target has Bullseye, then the critical damage is increased by 30%.
        if target_has_bullseye:
            buffs_before.append(
                Buff(
                    value=30,
                    modifier_type=ModifierType.ADDITIVE,
                    stat_type=SpecialAttribute.CRITICAL_DAMAGE,
                    tag=DamageTag.ALL,
                )
            )

        return DamageInstance(
            label=label,
            base_potency=base_potency,
            tags=tags,
            group_name="Heavenpierce",
            buffs_before=buffs_before,
        )


class HeavenpierceV2(CombatAction):
    """Cheyanne Ultimate (V2)."""

    @override
    def execute(
        self,
        target_has_bullseye: bool,
        few_enemies_with_low_analysis_score: bool,
        stacks_of_prepared_stance: int,
    ) -> DamageInstance:
        label: str = "Heavenpierce"
        base_potency: int = 280
        tags: set[DamageTag] = {
            DamageTag.ACTIVE,
            DamageTag.PHYSICAL,
            DamageTag.HEAVY_AMMO,
            DamageTag.TARGETED,
            DamageTag.CONFECTANCE,
            DamageTag.ULTIMATE,
        }

        buffs_before: list[Buff] = []

        # Resets the target's Analysis Score to 100%
        reset_analysis_score: int = 100
        analysis_score_buff: Buff = get_analysis_score_buffV1(reset_analysis_score)
        buffs_before.append(analysis_score_buff)

        # If the target has Bullseye, then the critical damage is increased by 30% and 50% of their defense is ignored.
        if target_has_bullseye:
            buffs_before.append(
                Buff(
                    value=30,
                    modifier_type=ModifierType.ADDITIVE,
                    stat_type=SpecialAttribute.CRITICAL_DAMAGE,
                    tag=DamageTag.ALL,
                )
            )

            buffs_before.append(
                Buff(
                    value=50,
                    modifier_type=ModifierType.ADDITIVE,
                    stat_type=SpecialAttribute.DEFENSE_IGNORE,
                    tag=DamageTag.ALL,
                )
            )

        return DamageInstance(
            label=label,
            base_potency=base_potency,
            tags=tags,
            group_name="Heavenpierce",
            buffs_before=buffs_before,
        )


class HeavenpierceV5(CombatAction):
    """Cheyanne Ultimate (V5)."""

    @override
    def execute(
        self,
        target_has_bullseye: bool,
        few_enemies_with_low_analysis_score: bool,
        stacks_of_prepared_stance: int,
    ) -> DamageInstance:
        label: str = "Heavenpierce"
        base_potency: int = 330
        tags: set[DamageTag] = {
            DamageTag.ACTIVE,
            DamageTag.PHYSICAL,
            DamageTag.HEAVY_AMMO,
            DamageTag.TARGETED,
            DamageTag.CONFECTANCE,
            DamageTag.ULTIMATE,
        }

        # If there are 3 or less enemies on the field with Analysis Score less than 50%, the damage multiplier is increased to 380%.
        if few_enemies_with_low_analysis_score:
            base_potency = 380

        buffs_before: list[Buff] = []

        # Resets the target's Analysis Score to 100%
        reset_analysis_score: int = 100
        analysis_score_buff: Buff = get_analysis_score_buffV1(reset_analysis_score)
        buffs_before.append(analysis_score_buff)

        # If the target has Bullseye, then the critical damage is increased by 30% and 50% of their defense is ignored.
        if target_has_bullseye:
            buffs_before.append(
                Buff(
                    value=30,
                    modifier_type=ModifierType.ADDITIVE,
                    stat_type=SpecialAttribute.CRITICAL_DAMAGE,
                    tag=DamageTag.ALL,
                )
            )

            buffs_before.append(
                Buff(
                    value=50,
                    modifier_type=ModifierType.ADDITIVE,
                    stat_type=SpecialAttribute.DEFENSE_IGNORE,
                    tag=DamageTag.ALL,
                )
            )

        return DamageInstance(
            label=label,
            base_potency=base_potency,
            tags=tags,
            group_name="Heavenpierce",
            buffs_before=buffs_before,
        )


class HeavenpierceV6(CombatAction):
    """Cheyanne Ultimate (V6)."""

    @override
    def execute(
        self,
        target_has_bullseye: bool,
        few_enemies_with_low_analysis_score: bool,
        stacks_of_prepared_stance: int,
    ) -> DamageInstance:
        label: str = "Heavenpierce"
        base_potency: int = 330
        tags: set[DamageTag] = {
            DamageTag.ACTIVE,
            DamageTag.PHYSICAL,
            DamageTag.HEAVY_AMMO,
            DamageTag.TARGETED,
            DamageTag.CONFECTANCE,
            DamageTag.ULTIMATE,
        }

        # If there are 3 or less enemies on the field with Analysis Score less than 50%, the damage multiplier is increased to 380%.
        if few_enemies_with_low_analysis_score:
            base_potency = 380

        # For each stack of Prepared Stance, increases damage multiplier by 80%. (Up to 3 stacks)
        max_stacks_of_prepared_stance: int = 3
        potency_per_stack_of_prepared_stance: int = 80

        if stacks_of_prepared_stance > 0:
            base_potency += potency_per_stack_of_prepared_stance * min(
                stacks_of_prepared_stance, max_stacks_of_prepared_stance
            )

        buffs_before: list[Buff] = []

        # Resets the target's Analysis Score to 100%
        reset_analysis_score: int = 100
        analysis_score_buff: Buff = get_analysis_score_buffV1(reset_analysis_score)
        buffs_before.append(analysis_score_buff)

        # If the target has Bullseye, then the critical damage is increased by 30% and 50% of their defense is ignored.
        if target_has_bullseye:
            buffs_before.append(
                Buff(
                    value=30,
                    modifier_type=ModifierType.ADDITIVE,
                    stat_type=SpecialAttribute.CRITICAL_DAMAGE,
                    tag=DamageTag.ALL,
                )
            )

            buffs_before.append(
                Buff(
                    value=50,
                    modifier_type=ModifierType.ADDITIVE,
                    stat_type=SpecialAttribute.DEFENSE_IGNORE,
                    tag=DamageTag.ALL,
                )
            )

        return DamageInstance(
            label=label,
            base_potency=base_potency,
            tags=tags,
            group_name="Heavenpierce",
            buffs_before=buffs_before,
        )


class DeliberateAction(CombatAction):
    """Passive attack from Cheyanne. Triggered when an enemy completes its turn or when an enemy with
    Bullseye ends its turn and Cheyanne has Fixed Key 6 - Full Attention equipped."""

    @override
    def execute(self, analysis_score: int) -> DamageInstance:
        label: str = "Deliberate Action"
        base_potency: int = 120
        tags: set[DamageTag] = {
            DamageTag.PASSIVE,
            DamageTag.HEAVY_AMMO,
            DamageTag.TARGETED,
            DamageTag.PHYSICAL,
        }

        buffs_before: list[Buff] = []

        # If the target has an Analysis Score of 50% or greater, then the damage multiplier is increased to 180%.
        if analysis_score >= 50:
            base_potency = 180

        analysis_score_buff: Buff = get_analysis_score_buff(analysis_score)
        buffs_before.append(analysis_score_buff)

        return DamageInstance(
            label=label,
            base_potency=base_potency,
            tags=tags,
            group_name="Deliberate Action",
            buffs_before=buffs_before,
        )


class DeliberateActionV1(CombatAction):
    """Passive attack from Cheyanne. Triggered when an enemy completes its turn or when an enemy with
    Bullseye ends its turn and Cheyanne has Fixed Key 6 - Full Attention equipped."""

    @override
    def execute(self, analysis_score: int) -> DamageInstance:
        label: str = "Deliberate Action"
        base_potency: int = 120
        tags: set[DamageTag] = {
            DamageTag.PASSIVE,
            DamageTag.HEAVY_AMMO,
            DamageTag.TARGETED,
            DamageTag.PHYSICAL,
        }

        buffs_before: list[Buff] = []

        # If the target has an Analysis Score of 50% or greater, then the damage multiplier is increased to 180%.
        if analysis_score >= 50:
            base_potency = 180

        analysis_score_buff: Buff = get_analysis_score_buffV1(analysis_score)
        buffs_before.append(analysis_score_buff)

        return DamageInstance(
            label=label,
            base_potency=base_potency,
            tags=tags,
            group_name="Deliberate Action",
            buffs_before=buffs_before,
        )


class DeliberateActionV6(CombatAction):
    """Passive attack from Cheyanne. Triggered when an enemy completes its turn or when an enemy with
    Bullseye ends its turn and Cheyanne has Fixed Key 6 - Full Attention equipped."""

    @override
    def execute(self, analysis_score: int) -> DamageInstance:
        label: str = "Deliberate Action"
        base_potency: int = 160
        tags: set[DamageTag] = {
            DamageTag.PASSIVE,
            DamageTag.HEAVY_AMMO,
            DamageTag.TARGETED,
            DamageTag.PHYSICAL,
        }

        buffs_before: list[Buff] = []

        # If the target has an Analysis Score of 50% or greater, then the damage multiplier is increased to 220%.
        if analysis_score >= 50:
            base_potency = 220

        analysis_score_buff: Buff = get_analysis_score_buffV1(analysis_score)
        buffs_before.append(analysis_score_buff)

        return DamageInstance(
            label=label,
            base_potency=base_potency,
            tags=tags,
            group_name="Deliberate Action",
            buffs_before=buffs_before,
        )


class Cheyanne(Doll):
    """Cheyanne."""

    name: str = "Cheyanne"
    irrelevant_damage_tags: ClassVar[set[DamageTag]] = set(
        [
            DamageTag.CORROSION,
            DamageTag.HYDRO,
            DamageTag.BURN,
            DamageTag.ELECTRIC,
            DamageTag.FREEZE,
            DamageTag.PHASE,
            DamageTag.MELEE,
            DamageTag.LIGHT_AMMO,
            DamageTag.MEDIUM_AMMO,
            DamageTag.SHOTGUN_AMMO,
            DamageTag.SUPPORT_ACTION,
            DamageTag.INTERCEPTION,
            DamageTag.COUNTERATTACK,
            DamageTag.AREA_OF_EFFECT,
            DamageTag.ULTIMATE,
            DamageTag.PHYSICAL_SUMMON,
            DamageTag.FIXED,
        ]
    )

    definitely_not_360_noscope: CombatAction = DefinitelyNot360NoScope()
    focused_pursuit: CombatAction = FocusedPursuit()
    heavenpierce: CombatAction = Heavenpierce()
    deliberate_action: CombatAction = DeliberateAction()

    def set_to_v0(self) -> None:
        """Sets Fortification Level to Segment00."""
        self.definitely_not_360_noscope = DefinitelyNot360NoScope()
        self.focused_pursuit = FocusedPursuit()
        self.heavenpierce = Heavenpierce()
        self.deliberate_action = DeliberateAction()

    def set_to_v1(self) -> None:
        """Sets Fortification Level to Segment01."""
        self.set_to_v0()

        self.definitely_not_360_noscope = DefinitelyNot360NoScopeV1()
        self.focused_pursuit = FocusedPursuitV1()
        self.heavenpierce = HeavenpierceV1()
        self.deliberate_action = DeliberateActionV1()

    def set_to_v2(self) -> None:
        """Sets Fortification Level to Segment02."""
        self.set_to_v1()

        self.heavenpierce = HeavenpierceV2()

    def set_to_v5(self) -> None:
        """Sets Fortification Level to Segment05."""
        self.set_to_v2()

        self.heavenpierce = HeavenpierceV5()

    def set_to_v6(self) -> None:
        """Sets Fortification Level to Segment06."""
        self.set_to_v5()

        self.heavenpierce = HeavenpierceV6()
        self.deliberate_action = DeliberateActionV6()

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
                self.set_to_v2()
            case FortificationLevel.SEGMENT04:
                self.set_to_v2()
            case FortificationLevel.SEGMENT05:
                self.set_to_v5()
            case FortificationLevel.SEGMENT06:
                self.set_to_v6()
