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
from core.buffs import Buff
from core.combat import DamageInstance, CombatAction

# Expansion Key - Lioness' Determination
# For every 1 point of Confectance Index consumed during this turn, increase
# attack by 5% up to a maximum of 30%.
LIONESS_DETERMINATION_ATTACK_BOOST_PER_CI: int = 5
LIONESS_DETERMINATION_MAX_ATTACK_BOOST: int = 30


class TerritoryAwareness(CombatAction):
    """Lenna Basic Attack."""

    @override
    def execute(self, follows_leaping_pursuit: bool) -> DamageInstance:
        label: str = "Territory Awareness"
        base_potency: int = 80

        tags: set[DamageTag] = {
            DamageTag.ACTIVE,
            DamageTag.BASIC,
            DamageTag.LIGHT_AMMO,
            DamageTag.TARGETED,
            DamageTag.PHYSICAL,
        }

        buffs_before: list[Buff] = []

        # Expansion Key - Lioness' Determination
        # After using active skill Leaping Pursuit, increase the damage multiplier of the next
        # active skill used during Extra Command by 100%.
        if follows_leaping_pursuit:
            base_potency += 100

            # Expansion Key - Lioness' Determination
            # For every 1 point of Confectance Index consumed during this turn, increase
            # attack by 5% up to a maximum of 30%.
            # Since this skill can't be enhanced by consuming CI, if it follows Leaping Pursuit
            # which we assume is enhanced, we infer that 3 points of CI were consumed this turn.
            attack_boost_from_ci = min(
                3 * LIONESS_DETERMINATION_ATTACK_BOOST_PER_CI,
                LIONESS_DETERMINATION_MAX_ATTACK_BOOST,
            )

            buffs_before.append(
                Buff(
                    attack_boost_from_ci,
                    ModifierType.MULTIPLICATIVE,
                    StatType.ATTACK,
                    DamageTag.ALL,
                )
            )

        return DamageInstance(
            label=label,
            base_potency=base_potency,
            tags=tags,
            group_name="Territory Awareness",
            buffs_before=buffs_before,
        )


class WildExtinction(CombatAction):
    """Lenna S1."""

    @override
    def execute(
        self, confectance_index: int, follows_leaping_pursuit: bool
    ) -> DamageInstance:
        label: str = "Wild Extinction"
        base_potency: int = 120
        tags: set[DamageTag] = {
            DamageTag.ACTIVE,
            DamageTag.ELECTRIC,
            DamageTag.PHASE,
            DamageTag.LIGHT_AMMO,
            DamageTag.TARGETED,
        }

        buffs_before: list[Buff] = []
        confectance_index_cost: int = 3

        # If the user's Confectance Index is greater than or equal to 3 points before skill activation
        # consumes 3 points of Confectance Index to enhance the skill, increasing damage dealt by 30%.
        if confectance_index >= confectance_index_cost:
            buffs_before.append(
                Buff(
                    30,
                    ModifierType.ADDITIVE,
                    SpecialAttribute.DAMAGE_BOOST,
                    DamageTag.ALL,
                )
            )

        # Expansion Key - Lioness' Determination
        # After using active skill Leaping Pursuit, increase the damage multiplier of the next
        # active skill used during Extra Command by 100%.
        if follows_leaping_pursuit:
            base_potency += 100

            # Expansion Key - Lioness' Determination
            # For every 1 point of Confectance Index consumed during this turn, increase
            # attack by 5% up to a maximum of 30%.
            # If this follows Leaping Pursuit
            # which we assume is enhanced, we infer that 6 points of CI were consumed this turn.
            confectance_index_consumed: int = 3

            if confectance_index >= confectance_index_cost:
                confectance_index_consumed += confectance_index_cost

            attack_boost_from_ci = min(
                confectance_index_consumed * LIONESS_DETERMINATION_ATTACK_BOOST_PER_CI,
                LIONESS_DETERMINATION_MAX_ATTACK_BOOST,
            )

            buffs_before.append(
                Buff(
                    attack_boost_from_ci,
                    ModifierType.MULTIPLICATIVE,
                    StatType.ATTACK,
                    DamageTag.ALL,
                )
            )

        return DamageInstance(
            label=label,
            base_potency=base_potency,
            tags=tags,
            group_name="Wild Extinction",
            buffs_before=buffs_before,
        )


class WildExtinctionV2(CombatAction):
    """Lenna S1 (V2)."""

    @override
    def execute(
        self, confectance_index: int, follows_leaping_pursuit: bool
    ) -> DamageInstance:
        label: str = "Wild Extinction"
        base_potency: int = 120
        tags: set[DamageTag] = {
            DamageTag.ACTIVE,
            DamageTag.ELECTRIC,
            DamageTag.PHASE,
            DamageTag.LIGHT_AMMO,
            DamageTag.TARGETED,
        }

        buffs_before: list[Buff] = []
        confectance_index_cost: int = 3

        # If the user's Confectance Index is greater than or equal to 3 points before skill activation
        # consumes 3 points of Confectance Index to enhance the skill, increasing damage dealt by 30%.
        if confectance_index >= confectance_index_cost:
            buffs_before.append(
                Buff(
                    50,
                    ModifierType.ADDITIVE,
                    SpecialAttribute.DAMAGE_BOOST,
                    DamageTag.ALL,
                )
            )

        # Expansion Key - Lioness' Determination
        # After using active skill Leaping Pursuit, increase the damage multiplier of the next
        # active skill used during Extra Command by 100%.
        if follows_leaping_pursuit:
            base_potency += 100

            # Expansion Key - Lioness' Determination
            # For every 1 point of Confectance Index consumed during this turn, increase
            # attack by 5% up to a maximum of 30%.
            # If this follows Leaping Pursuit
            # which we assume is enhanced, we infer that 6 points of CI were consumed this turn.
            confectance_index_consumed: int = 3

            if confectance_index >= confectance_index_cost:
                confectance_index_consumed += confectance_index_cost

            attack_boost_from_ci = min(
                confectance_index_consumed * LIONESS_DETERMINATION_ATTACK_BOOST_PER_CI,
                LIONESS_DETERMINATION_MAX_ATTACK_BOOST,
            )

            buffs_before.append(
                Buff(
                    attack_boost_from_ci,
                    ModifierType.MULTIPLICATIVE,
                    StatType.ATTACK,
                    DamageTag.ALL,
                )
            )

        return DamageInstance(
            label=label,
            base_potency=base_potency,
            tags=tags,
            group_name="Wild Extinction",
            buffs_before=buffs_before,
        )


class WildExtinctionV6(CombatAction):
    """Lenna S1 (V6)."""

    @override
    def execute(
        self, confectance_index: int, follows_leaping_pursuit: bool
    ) -> DamageInstance:
        label: str = "Wild Extinction"
        base_potency: int = 120
        tags: set[DamageTag] = {
            DamageTag.ACTIVE,
            DamageTag.ELECTRIC,
            DamageTag.PHASE,
            DamageTag.LIGHT_AMMO,
            DamageTag.TARGETED,
        }

        buffs_before: list[Buff] = []
        confectance_index_cost: int = 3

        # If the user's Confectance Index is greater than or equal to 3 points before skill activation
        # consumes 3 points of Confectance Index to enhance the skill, increasing damage dealt by 30%.

        # V6 Electric Arc enhancement: Consuming Confectance Index makes the attack deal 20% more damage.
        if confectance_index >= confectance_index_cost:
            buffs_before.append(
                Buff(
                    70,
                    ModifierType.ADDITIVE,
                    SpecialAttribute.DAMAGE_BOOST,
                    DamageTag.ALL,
                )
            )

        # Expansion Key - Lioness' Determination
        # After using active skill Leaping Pursuit, increase the damage multiplier of the next
        # active skill used during Extra Command by 100%.
        if follows_leaping_pursuit:
            base_potency += 100

            # Expansion Key - Lioness' Determination
            # For every 1 point of Confectance Index consumed during this turn, increase
            # attack by 5% up to a maximum of 30%.
            # If this follows Leaping Pursuit
            # which we assume is enhanced, we infer that 6 points of CI were consumed this turn.
            confectance_index_consumed: int = 3

            if confectance_index >= confectance_index_cost:
                confectance_index_consumed += confectance_index_cost

            attack_boost_from_ci = min(
                confectance_index_consumed * LIONESS_DETERMINATION_ATTACK_BOOST_PER_CI,
                LIONESS_DETERMINATION_MAX_ATTACK_BOOST,
            )

            buffs_before.append(
                Buff(
                    attack_boost_from_ci,
                    ModifierType.MULTIPLICATIVE,
                    StatType.ATTACK,
                    DamageTag.ALL,
                )
            )

        return DamageInstance(
            label=label,
            base_potency=base_potency,
            tags=tags,
            group_name="Wild Extinction",
            buffs_before=buffs_before,
        )


class LeapingPursuit(CombatAction):
    """Lenna S2."""

    @override
    def execute(self, confectance_index: int) -> DamageInstance:
        label: str = "Leaping Pursuit"
        base_potency: int = 30
        tags: set[DamageTag] = {
            DamageTag.ACTIVE,
            DamageTag.PHYSICAL,
            DamageTag.LIGHT_AMMO,
            DamageTag.TARGETED,
        }

        buffs_before: list[Buff] = []
        confectance_index_cost: int = 3

        # Expansion Key - Lioness' Determination
        # For every 1 point of Confectance Index consumed during this turn, increase
        # attack by 5% up to a maximum of 30%.
        confectance_index_consumed: int = 0
        if confectance_index >= confectance_index_cost:
            confectance_index_consumed += confectance_index_cost

            attack_boost_from_ci = min(
                confectance_index_consumed * LIONESS_DETERMINATION_ATTACK_BOOST_PER_CI,
                LIONESS_DETERMINATION_MAX_ATTACK_BOOST,
            )

            buffs_before.append(
                Buff(
                    attack_boost_from_ci,
                    ModifierType.MULTIPLICATIVE,
                    StatType.ATTACK,
                    DamageTag.ALL,
                )
            )

        return DamageInstance(
            label=label,
            base_potency=base_potency,
            tags=tags,
            group_name="Leaping Pursuit",
            buffs_before=buffs_before,
        )


class LeapingPursuitV6(CombatAction):
    """Lenna S2 (V6)."""

    @override
    def execute(self, confectance_index: int) -> DamageInstance:
        label: str = "Leaping Pursuit"
        base_potency: int = 30
        tags: set[DamageTag] = {
            DamageTag.ACTIVE,
            DamageTag.PHYSICAL,
            DamageTag.LIGHT_AMMO,
            DamageTag.TARGETED,
        }

        buffs_before: list[Buff] = []

        # V6 Electric Arc enhancement: Consuming Confectance Index makes the attack deal 20% more damage.
        if confectance_index >= 3:
            buffs_before.append(
                Buff(
                    20,
                    ModifierType.ADDITIVE,
                    SpecialAttribute.DAMAGE_BOOST,
                    DamageTag.ALL,
                )
            )

        confectance_index_cost: int = 3

        # Expansion Key - Lioness' Determination
        # For every 1 point of Confectance Index consumed during this turn, increase
        # attack by 5% up to a maximum of 30%.
        confectance_index_consumed: int = 0
        if confectance_index >= confectance_index_cost:
            confectance_index_consumed += confectance_index_cost

            attack_boost_from_ci = min(
                confectance_index_consumed * LIONESS_DETERMINATION_ATTACK_BOOST_PER_CI,
                LIONESS_DETERMINATION_MAX_ATTACK_BOOST,
            )

            buffs_before.append(
                Buff(
                    attack_boost_from_ci,
                    ModifierType.MULTIPLICATIVE,
                    StatType.ATTACK,
                    DamageTag.ALL,
                )
            )

        return DamageInstance(
            label=label,
            base_potency=base_potency,
            tags=tags,
            group_name="Leaping Pursuit",
            buffs_before=buffs_before,
        )


class HuntingStrategy(CombatAction):
    """Lenna Ultimate."""

    @override
    def execute(
        self, confectance_index: int, follows_leaping_pursuit: bool
    ) -> DamageInstance:
        label: str = "Hunting Strategy"
        base_potency: int = 80
        tags: set[DamageTag] = {
            DamageTag.ACTIVE,
            DamageTag.ELECTRIC,
            DamageTag.PHASE,
            DamageTag.ULTIMATE,
            DamageTag.AREA_OF_EFFECT,
        }

        buffs_before: list[Buff] = []

        # Expansion Key - Lioness' Determination
        # After using active skill Leaping Pursuit, increase the damage multiplier of the next
        # active skill used during Extra Command by 100%.
        if follows_leaping_pursuit:
            base_potency += 100

            # Expansion Key - Lioness' Determination
            # For every 1 point of Confectance Index consumed during this turn, increase
            # attack by 5% up to a maximum of 30%.
            # If this follows Leaping Pursuit
            # which we assume is enhanced, we infer that 6 points of CI were consumed this turn.
            confectance_index_consumed: int = 3
            confectance_index_cost: int = 3

            if confectance_index >= confectance_index_cost:
                confectance_index_consumed += confectance_index_cost

            attack_boost_from_ci = min(
                confectance_index_consumed * LIONESS_DETERMINATION_ATTACK_BOOST_PER_CI,
                LIONESS_DETERMINATION_MAX_ATTACK_BOOST,
            )

            buffs_before.append(
                Buff(
                    attack_boost_from_ci,
                    ModifierType.MULTIPLICATIVE,
                    StatType.ATTACK,
                    DamageTag.ALL,
                )
            )

        return DamageInstance(
            label=label,
            base_potency=base_potency,
            tags=tags,
            group_name="Hunting Strategy",
            buffs_before=buffs_before,
        )


class HuntingStrategyV6(CombatAction):
    """Lenna Ultimate (V6)."""

    @override
    def execute(
        self, confectance_index: int, follows_leaping_pursuit: bool
    ) -> DamageInstance:
        label: str = "Hunting Strategy"
        base_potency: int = 80
        tags: set[DamageTag] = {
            DamageTag.ACTIVE,
            DamageTag.ELECTRIC,
            DamageTag.PHASE,
            DamageTag.ULTIMATE,
            DamageTag.AREA_OF_EFFECT,
        }

        buffs_before: list[Buff] = []
        confectance_index_cost: int = 3

        # V6 Electric Arc enhancement: Consuming Confectance Index makes the attack deal 20% more damage.
        if confectance_index >= confectance_index_cost:
            buffs_before.append(
                Buff(
                    20,
                    ModifierType.ADDITIVE,
                    SpecialAttribute.DAMAGE_BOOST,
                    DamageTag.ALL,
                )
            )

        # Expansion Key - Lioness' Determination
        # After using active skill Leaping Pursuit, increase the damage multiplier of the next
        # active skill used during Extra Command by 100%.
        if follows_leaping_pursuit:
            base_potency += 100

            # Expansion Key - Lioness' Determination
            # For every 1 point of Confectance Index consumed during this turn, increase
            # attack by 5% up to a maximum of 30%.
            # If this follows Leaping Pursuit
            # which we assume is enhanced, we infer that 6 points of CI were consumed this turn.
            confectance_index_consumed: int = 3

            if confectance_index >= confectance_index_cost:
                confectance_index_consumed += confectance_index_cost

            attack_boost_from_ci = min(
                confectance_index_consumed * LIONESS_DETERMINATION_ATTACK_BOOST_PER_CI,
                LIONESS_DETERMINATION_MAX_ATTACK_BOOST,
            )

            buffs_before.append(
                Buff(
                    attack_boost_from_ci,
                    ModifierType.MULTIPLICATIVE,
                    StatType.ATTACK,
                    DamageTag.ALL,
                )
            )

        return DamageInstance(
            label=label,
            base_potency=base_potency,
            tags=tags,
            group_name="Hunting Strategy",
            buffs_before=buffs_before,
        )


class Lenna(Doll):
    """Lenna."""

    name: str = "Lenna"
    irrelevant_damage_tags: ClassVar[set[DamageTag]] = set(
        [
            DamageTag.CORROSION,
            DamageTag.BURN,
            DamageTag.HYDRO,
            DamageTag.FREEZE,
            DamageTag.MEDIUM_AMMO,
            DamageTag.HEAVY_AMMO,
            DamageTag.SHOTGUN_AMMO,
            DamageTag.SUPPORT_ACTION,
            DamageTag.INTERCEPTION,
            DamageTag.COUNTERATTACK,
            DamageTag.PHYSICAL_SUMMON,
            DamageTag.FIXED,
        ]
    )

    territory_awareness: CombatAction = Field(default_factory=TerritoryAwareness)
    wild_extinction: CombatAction = Field(default_factory=WildExtinction)
    leaping_pursuit: CombatAction = Field(default_factory=LeapingPursuit)
    hunting_strategy: CombatAction = Field(default_factory=HuntingStrategy)

    def set_to_v0(self) -> None:
        """Sets Fortification Level to Segment00."""
        self.territory_awareness = TerritoryAwareness()
        self.wild_extinction = WildExtinction()
        self.leaping_pursuit = LeapingPursuit()
        self.hunting_strategy = HuntingStrategy()

    def set_to_v2(self) -> None:
        """Sets Fortification Level to Segment01."""
        self.set_to_v0()

        self.wild_extinction = WildExtinctionV2()

    def set_to_v6(self) -> None:
        """Sets Fortification Level to Segment02."""
        self.set_to_v2()

        # V6 versions assume Electric Arc is active, allowing consumption of CI to
        # increase damage.
        self.wild_extinction = WildExtinctionV6()
        self.leaping_pursuit = LeapingPursuitV6()
        self.hunting_strategy = HuntingStrategyV6()

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
                self.set_to_v2()
            case FortificationLevel.SEGMENT04:
                self.set_to_v2()
            case FortificationLevel.SEGMENT05:
                self.set_to_v2()
            case FortificationLevel.SEGMENT06:
                self.set_to_v6()
