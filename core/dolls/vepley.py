from pydantic import Field
from typing import override, ClassVar

from core.types import (
    DamageTag,
    ModifierType,
    StatType,
    SpecialAttribute,
    Doll,
    FortificationLevel,
    SummonedUnit,
)
from core.buffs import Buff, Debuff, VulnerableII, Overzealous
from core.combat import DamageInstance, CombatAction


class LiveInteraction(CombatAction):
    """Vepley Basic Attack."""

    @override
    def execute(self) -> DamageInstance:
        label: str = "Live Interaction"
        base_potency: int = 80
        tags: set[DamageTag] = {
            DamageTag.ACTIVE,
            DamageTag.BASIC,
            DamageTag.SHOTGUN_AMMO,
            DamageTag.TARGETED,
            DamageTag.PHYSICAL,
        }

        return DamageInstance(
            label=label,
            base_potency=base_potency,
            tags=tags,
            group_name="Live Interaction",
        )


class AllOutPerformance(CombatAction):
    """Vepley S1 — AoE attack.

    Expansion Key (Idol Steps) applies Stun and Vulnerable II. The Idol Talent
    passive (+20% damage) and Expansion Key conditional defense ignore (+15%)
    are applied via the HAS_MOVEMENT_DEBUFF tag set in Vepley's initial_stats.
    """

    @override
    def execute(self) -> DamageInstance:
        label: str = "All Out Performance"
        base_potency: int = 75
        tags: set[DamageTag] = {
            DamageTag.ACTIVE,
            DamageTag.SHOTGUN_AMMO,
            DamageTag.AREA_OF_EFFECT,
            DamageTag.PHYSICAL,
        }

        return DamageInstance(
            label=label,
            base_potency=base_potency,
            tags=tags,
            group_name="All Out Performance",
            debuffs_before=[VulnerableII()],
        )


class ExclusiveStage(CombatAction):
    """Vepley S2."""

    @override
    def execute(self) -> DamageInstance:
        label: str = "Exclusive Stage"
        base_potency: int = 150
        tags: set[DamageTag] = {
            DamageTag.ACTIVE,
            DamageTag.TARGETED,
            DamageTag.PHYSICAL,
        }

        return DamageInstance(
            label=label,
            base_potency=base_potency,
            tags=tags,
            group_name="Exclusive Stage",
        )


class ExclusiveStageV2(CombatAction):
    """Vepley S2 (V2): critical rate +100% vs movement-debuffed targets."""

    @override
    def execute(self) -> DamageInstance:
        label: str = "Exclusive Stage"
        base_potency: int = 150
        tags: set[DamageTag] = {
            DamageTag.ACTIVE,
            DamageTag.TARGETED,
            DamageTag.PHYSICAL,
        }

        return DamageInstance(
            label=label,
            base_potency=base_potency,
            tags=tags,
            group_name="Exclusive Stage",
            buffs_before=[
                Buff(
                    value=100,
                    modifier_type=ModifierType.ADDITIVE,
                    stat_type=StatType.CRIT_RATE,
                    tag=DamageTag.HAS_MOVEMENT_DEBUFF,
                )
            ],
        )


class InfectiousEnthusiasm(CombatAction):
    """Vepley Ultimate (V0-V2).

    At V3+, Overzealous is applied before the attack (applied after at V0–V2).
    This version is used for V0-V2 and does not apply debuffs before.
    """

    @override
    def execute(self) -> DamageInstance:
        label: str = "Infectious Enthusiasm"
        base_potency: int = 100
        tags: set[DamageTag] = {
            DamageTag.ACTIVE,
            DamageTag.AREA_OF_EFFECT,
            DamageTag.ULTIMATE,
            DamageTag.PHYSICAL,
        }

        return DamageInstance(
            label=label,
            base_potency=base_potency,
            tags=tags,
            group_name="Infectious Enthusiasm",
        )


class InfectiousEnthusiasmV3(CombatAction):
    """Vepley Ultimate (V3+).

    V3 upgrade: Overzealous is applied before the attack.
    """

    @override
    def execute(self) -> DamageInstance:
        label: str = "Infectious Enthusiasm"
        base_potency: int = 100
        tags: set[DamageTag] = {
            DamageTag.ACTIVE,
            DamageTag.AREA_OF_EFFECT,
            DamageTag.ULTIMATE,
            DamageTag.PHYSICAL,
        }

        return DamageInstance(
            label=label,
            base_potency=base_potency,
            tags=tags,
            group_name="Infectious Enthusiasm",
            debuffs_before=[Overzealous()],
        )


class Vepley(Doll):
    """Vepley — Physical Vanguard. Expansion Key (Idol Steps) assumed active."""

    name: str = "Vepley"
    irrelevant_damage_tags: ClassVar[set[DamageTag]] = set(
        [
            DamageTag.PHASE,
            DamageTag.CORROSION,
            DamageTag.FREEZE,
            DamageTag.HYDRO,
            DamageTag.BURN,
            DamageTag.ELECTRIC,
            DamageTag.MELEE,
            DamageTag.LIGHT_AMMO,
            DamageTag.MEDIUM_AMMO,
            DamageTag.HEAVY_AMMO,
            DamageTag.PASSIVE,
            DamageTag.SUPPORT_ACTION,
            DamageTag.INTERCEPTION,
            DamageTag.COUNTERATTACK,
            DamageTag.PHYSICAL_SUMMON,
        ]
    )

    live_interaction: CombatAction = Field(default_factory=LiveInteraction)
    all_out_performance: CombatAction = Field(default_factory=AllOutPerformance)
    exclusive_stage: CombatAction = Field(default_factory=ExclusiveStage)
    infectious_enthusiasm: CombatAction = Field(default_factory=InfectiousEnthusiasm)

    def set_to_v0(self) -> None:
        """Sets Fortification Level to Segment00."""
        self.live_interaction = LiveInteraction()
        self.all_out_performance = AllOutPerformance()
        self.exclusive_stage = ExclusiveStage()
        self.infectious_enthusiasm = InfectiousEnthusiasm()

        # Expansion Key — Idol Steps: all attacks ignore 15% of target's defense
        self.initial_stats.special_attributes[
            SpecialAttribute.DEFENSE_IGNORE
        ].set_multiplier(DamageTag.ALL, 15)

        # Expansion Key conditional: ignore an additional 15% when target has movement debuffs
        self.initial_stats.special_attributes[
            SpecialAttribute.DEFENSE_IGNORE
        ].set_multiplier(DamageTag.HAS_MOVEMENT_DEBUFF, 15)

        # Idol Talent passive: damage to targets with movement debuffs increased by 20%
        self.initial_stats.special_attributes[
            SpecialAttribute.DAMAGE_BOOST
        ].set_multiplier(DamageTag.HAS_MOVEMENT_DEBUFF, 20)

    def set_to_v2(self) -> None:
        """Sets Fortification Level to Segment02."""
        self.set_to_v0()

        # V2 upgrade: Exclusive Stage gains +100% crit rate when target has movement debuffs
        self.exclusive_stage = ExclusiveStageV2()

    def set_to_v3(self) -> None:
        """Sets Fortification Level to Segment03.

        V3 upgrade: Infectious Enthusiasm applies Overzealous before the attack.
        No additional action needed — HAS_MOVEMENT_DEBUFF in initial_stats covers
        the passive bonuses at all fortification levels.
        """
        self.set_to_v2()

        # V3 upgrade: Infectious Enthusiasm applies Overzealous before the attack
        self.infectious_enthusiasm = InfectiousEnthusiasmV3()

    @override
    def set_fortification_level(self, level: FortificationLevel) -> None:
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
                self.set_to_v3()
            case FortificationLevel.SEGMENT05:
                self.set_to_v3()
            case FortificationLevel.SEGMENT06:
                self.set_to_v3()

    def get_sample_data(self) -> list[DamageInstance]:
        """Returns a sample single target rotation."""
        return [
            self.infectious_enthusiasm.execute(),
            self.exclusive_stage.execute(),
            self.all_out_performance.execute(),
            self.infectious_enthusiasm.execute(),
            self.exclusive_stage.execute(),
            self.infectious_enthusiasm.execute(),
            self.exclusive_stage.execute(),
        ]
