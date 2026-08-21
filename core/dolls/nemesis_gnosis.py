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


class Starfall(CombatAction):
    """Nemesis: Gnosis basic attack."""

    @override
    def execute(self) -> DamageInstance:
        label: str = "Starfall"
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
            buffs_before=[],
            group_name="Starfall",
        )


class CalamityResonance(CombatAction):
    """Nemesis: Gnosis S1."""

    @override
    def execute(self) -> DamageInstance:
        label: str = "Calamity Resonance"
        base_potency: int = 80
        tags: set[DamageTag] = {
            DamageTag.ACTIVE,
            DamageTag.HEAVY_AMMO,
            DamageTag.TARGETED,
            DamageTag.CORROSION,
        }

        return DamageInstance(
            label=label,
            base_potency=base_potency,
            tags=tags,
            group_name="Calamity Resonance",
            buffs_before=[],
        )


class PrismaticRefraction(CombatAction):
    """Nemesis: Gnosis S2."""

    @override
    def execute(
        self,
        has_first_prophecy: bool,
        has_second_prophecy: bool,
        has_no_allies_nearby: bool,
    ) -> DamageInstance:
        label: str = "Prismatic Refraction"
        base_potency: int = 120
        tags: set[DamageTag] = {
            DamageTag.ACTIVE,
            DamageTag.HEAVY_AMMO,
            DamageTag.TARGETED,
            DamageTag.CORROSION,
        }

        buffs_before: list[Buff] = []

        if has_first_prophecy:
            base_potency += 20

        # Damage dealt is increased by 20% when no ally units are within 4 tiles around her
        if has_second_prophecy and has_no_allies_nearby:
            buffs_before.append(
                Buff(
                    20,
                    modifier_type=ModifierType.ADDITIVE,
                    stat_type=SpecialAttribute.DAMAGE_BOOST,
                    tag=DamageTag.ALL,
                ),
            )

        return DamageInstance(
            label=label,
            base_potency=base_potency,
            tags=tags,
            group_name="Prismatic Refraction",
            buffs_before=buffs_before,
        )


class PrismaticRefractionV4(CombatAction):
    """Nemesis: Gnosis S2 (V4)."""

    @override
    def execute(
        self,
        has_first_prophecy: bool,
        has_second_prophecy: bool,
        has_no_allies_nearby: bool,
    ) -> DamageInstance:
        label: str = "Prismatic Refraction"
        base_potency: int = 120
        tags: set[DamageTag] = {
            DamageTag.ACTIVE,
            DamageTag.HEAVY_AMMO,
            DamageTag.TARGETED,
            DamageTag.CORROSION,
        }

        buffs_before: list[Buff] = []

        if has_first_prophecy:
            base_potency += 40

        # Damage dealt is increased by 40% when no ally units are within 4 tiles around her
        if has_second_prophecy and has_no_allies_nearby:
            buffs_before.append(
                Buff(
                    40,
                    modifier_type=ModifierType.ADDITIVE,
                    stat_type=SpecialAttribute.DAMAGE_BOOST,
                    tag=DamageTag.ALL,
                ),
            )

        return DamageInstance(
            label=label,
            base_potency=base_potency,
            tags=tags,
            group_name="Prismatic Refraction",
            buffs_before=buffs_before,
        )


class FatesReprise(CombatAction):
    """Nemesis: Gnosis Ultimate."""

    @override
    def execute(
        self,
        confectance_index_consumed: int,
        has_fifth_prophecy: bool,
        has_sixth_prophecy: bool,
    ) -> DamageInstance:
        label: str = f"Fate's Reprise ({confectance_index_consumed})"
        base_potency: int = 140
        tags: set[DamageTag] = {
            DamageTag.ACTIVE,
            DamageTag.CORROSION,
            DamageTag.HEAVY_AMMO,
            DamageTag.AREA_OF_EFFECT,
            DamageTag.CONFECTANCE,
            DamageTag.ULTIMATE,
        }

        buffs_before: list[Buff] = []

        damage_multiplier_per_confectance_index: int = 10
        maximum_confectance_index_consumed: int = 6
        base_potency += (
            min(max(0, confectance_index_consumed), maximum_confectance_index_consumed)
            * damage_multiplier_per_confectance_index
        )

        damage_boost_per_confectance_index: int = 10
        if has_sixth_prophecy:
            buffs_before.append(
                Buff(
                    value=min(
                        max(0, confectance_index_consumed),
                        maximum_confectance_index_consumed,
                    )
                    * damage_boost_per_confectance_index,
                    modifier_type=ModifierType.ADDITIVE,
                    stat_type=SpecialAttribute.DAMAGE_BOOST,
                    tag=DamageTag.ALL,
                )
            )

        # The additional damage instance dealt to enemy targets around the center target (excluding the center target)
        # is not modeled here because it excludes the center target.

        return DamageInstance(
            label=label,
            base_potency=base_potency,
            tags=tags,
            group_name="Fate's Reprise",
            buffs_before=buffs_before,
        )


class FatesRepriseV2(CombatAction):
    """Nemesis: Gnosis Ultimate (V2)."""

    @override
    def execute(
        self,
        confectance_index_consumed: int,
        has_fifth_prophecy: bool,
        has_sixth_prophecy: bool,
    ) -> DamageInstance:
        label: str = f"Fate's Reprise ({confectance_index_consumed})"
        base_potency: int = 140
        tags: set[DamageTag] = {
            DamageTag.ACTIVE,
            DamageTag.CORROSION,
            DamageTag.HEAVY_AMMO,
            DamageTag.AREA_OF_EFFECT,
            DamageTag.CONFECTANCE,
            DamageTag.ULTIMATE,
        }

        buffs_before: list[Buff] = []

        damage_multiplier_per_confectance_index: int = 10
        maximum_confectance_index_consumed: int = 6
        base_potency += (
            min(max(0, confectance_index_consumed), maximum_confectance_index_consumed)
            * damage_multiplier_per_confectance_index
        )

        damage_boost_per_confectance_index: int = 10
        if has_sixth_prophecy:
            buffs_before.append(
                Buff(
                    value=min(
                        max(0, confectance_index_consumed),
                        maximum_confectance_index_consumed,
                    )
                    * damage_boost_per_confectance_index,
                    modifier_type=ModifierType.ADDITIVE,
                    stat_type=SpecialAttribute.DAMAGE_BOOST,
                    tag=DamageTag.ALL,
                )
            )

        # The additional damage instance dealt to enemy targets around the center target (excluding the center target)
        # is not modeled here because it excludes the center target.

        if has_fifth_prophecy:
            buffs_before.append(
                Buff(
                    value=50,
                    modifier_type=ModifierType.ADDITIVE,
                    stat_type=SpecialAttribute.DAMAGE_BOOST,
                    tag=DamageTag.ALL,
                )
            )

        return DamageInstance(
            label=label,
            base_potency=base_potency,
            tags=tags,
            group_name="Fate's Reprise",
            buffs_before=buffs_before,
        )


class SupportAction(CombatAction):
    """Support Action from Doomguide."""

    @override
    def execute(self, has_verdict_privilege: bool) -> DamageInstance:
        base_potency: int = 60
        label: str = "Support Action"
        tags: set[DamageTag] = {
            DamageTag.PASSIVE,
            DamageTag.SUPPORT_ACTION,
            DamageTag.HEAVY_AMMO,
            DamageTag.TARGETED,
            DamageTag.CORROSION,
            DamageTag.PHASE,
        }

        if has_verdict_privilege:
            base_potency += 30

        return DamageInstance(
            label=label,
            base_potency=base_potency,
            tags=tags,
            group_name="Support Action",
        )


class SupportActionV1(CombatAction):
    """Support Action from Doomguide (V1)."""

    @override
    def execute(self, has_verdict_privilege: bool) -> DamageInstance:
        base_potency: int = 110
        label: str = "Support Action"
        tags: set[DamageTag] = {
            DamageTag.PASSIVE,
            DamageTag.SUPPORT_ACTION,
            DamageTag.HEAVY_AMMO,
            DamageTag.TARGETED,
            DamageTag.CORROSION,
            DamageTag.PHASE,
        }

        if has_verdict_privilege:
            base_potency += 30

        return DamageInstance(
            label=label,
            base_potency=base_potency,
            tags=tags,
            group_name="Support Action",
        )


class SupportActionV5(CombatAction):
    """Support Action from Doomguide (V5)."""

    @override
    def execute(self, has_verdict_privilege: bool) -> DamageInstance:
        base_potency: int = 110
        label: str = "Support Action"
        tags: set[DamageTag] = {
            DamageTag.PASSIVE,
            DamageTag.SUPPORT_ACTION,
            DamageTag.HEAVY_AMMO,
            DamageTag.TARGETED,
            DamageTag.CORROSION,
            DamageTag.PHASE,
        }

        if has_verdict_privilege:
            base_potency += 40

        return DamageInstance(
            label=label,
            base_potency=base_potency,
            tags=tags,
            group_name="Support Action",
        )


class ThirdProphecy(CombatAction):
    """Damage instance triggered when Nemesis: Gnosis deals targeted damage and the target does not die
    while she has Third Prophecy: Cataclysm."""

    @override
    def execute(self, triggered_out_of_turn: bool) -> DamageInstance:
        base_potency: int = 60
        label: str = "Third Prophecy"
        tags: set[DamageTag] = {
            DamageTag.PASSIVE,
            DamageTag.AREA_OF_EFFECT,
            DamageTag.CORROSION,
            DamageTag.PHASE,
        }

        if triggered_out_of_turn:
            tags.add(DamageTag.SUPPORT_ACTION)

        return DamageInstance(
            label=label,
            base_potency=base_potency,
            tags=tags,
            group_name="Third Prophecy",
        )


class ThirdProphecyV5(CombatAction):
    """Damage instance triggered when Nemesis: Gnosis deals targeted damage and the target does not die
    while she has Third Prophecy: Cataclysm."""

    @override
    def execute(self, triggered_out_of_turn: bool) -> DamageInstance:
        base_potency: int = 80
        label: str = "Third Prophecy"
        tags: set[DamageTag] = {
            DamageTag.PASSIVE,
            DamageTag.AREA_OF_EFFECT,
            DamageTag.CORROSION,
            DamageTag.PHASE,
        }

        if triggered_out_of_turn:
            tags.add(DamageTag.SUPPORT_ACTION)

        return DamageInstance(
            label=label,
            base_potency=base_potency,
            tags=tags,
            group_name="Third Prophecy",
        )


class NemesisGnosis(Doll):
    """Nemesis: Gnosis."""

    name: str = "Nemesis: Gnosis"
    irrelevant_damage_tags: ClassVar[set[DamageTag]] = set(
        [
            DamageTag.HYDRO,
            DamageTag.BURN,
            DamageTag.ELECTRIC,
            DamageTag.FREEZE,
            DamageTag.MELEE,
            DamageTag.LIGHT_AMMO,
            DamageTag.MEDIUM_AMMO,
            DamageTag.SHOTGUN_AMMO,
            DamageTag.INTERCEPTION,
            DamageTag.COUNTERATTACK,
            DamageTag.PHYSICAL_SUMMON,
            DamageTag.FIXED,
        ]
    )

    starfall: CombatAction = Field(default_factory=Starfall)
    calamity_resonance: CombatAction = Field(default_factory=CalamityResonance)
    prismatic_refraction: CombatAction = Field(default_factory=PrismaticRefraction)
    fates_reprise: CombatAction = Field(default_factory=FatesReprise)
    support_action: CombatAction = Field(default_factory=SupportAction)
    third_prophecy: CombatAction = Field(default_factory=ThirdProphecy)

    def set_to_v0(self) -> None:
        """Sets Fortification Level to Segment00."""
        self.starfall = Starfall()
        self.calamity_resonance = CalamityResonance()
        self.prismatic_refraction = PrismaticRefraction()
        self.fates_reprise = FatesReprise()
        self.support_action = SupportAction()
        self.third_prophecy = ThirdProphecy()

    def set_to_v1(self) -> None:
        """Sets Fortification Level to Segment01."""
        self.set_to_v0()

        self.support_action = SupportActionV1()

    def set_to_v2(self) -> None:
        """Sets Fortification Level to Segment02."""
        self.set_to_v1()

        self.fates_reprise = FatesRepriseV2()

    def set_to_v4(self) -> None:
        """Sets Fortification Level to Segment04."""
        self.set_to_v2()

        self.prismatic_refraction = PrismaticRefractionV4()

    def set_to_v5(self) -> None:
        """Sets Fortification Level to Segment05."""
        self.set_to_v4()

        self.third_prophecy = ThirdProphecyV5()
        self.support_action = SupportActionV5()

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
                self.set_to_v4()
            case FortificationLevel.SEGMENT05:
                self.set_to_v5()
            case FortificationLevel.SEGMENT06:
                self.set_to_v5()
