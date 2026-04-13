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
from core.combat import (
    DamageInstance,
    CombatAction,
    FixedDamageInstance,
    BelkaDamageCalculationStrategy,
)


ACTIVE_ENGAGEMENT_BUFF: int = 30
ACTIVE_ENGAGEMENT_BUFF_V5: int = 40


class NutcrackerShell(CombatAction):
    """Belka basic attack."""

    @override
    def execute(self, has_active_engagement: bool = False) -> DamageInstance:
        label: str = "Nutcracker Shell"
        base_potency: int = 80
        tags: set[DamageTag] = {
            DamageTag.ACTIVE,
            DamageTag.BASIC,
            DamageTag.MEDIUM_AMMO,
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
            group_name="Nutcracker Shell",
            buffs_before=buffs_before,
            damage_calculation_strategy=BelkaDamageCalculationStrategy(),
        )


class SylvanVault(CombatAction):
    """Belka S1."""

    @override
    def execute(
        self,
        has_active_engagement: bool,
        number_positive_charge_on_field: int,
        number_negative_charge_on_field: int,
        target_is_boss_with_negative_charge: bool,
    ) -> DamageInstance:
        label: str = "Sylvan Vault"
        base_potency: int = 130
        tags: set[DamageTag] = {
            DamageTag.ACTIVE,
            DamageTag.CONFECTANCE,
            DamageTag.MEDIUM_AMMO,
            DamageTag.TARGETED,
            DamageTag.ELECTRIC,  # Expansion Key - Squirrel's Awakening changes this to Electric; no need to be conditional on Active Engagement
            DamageTag.PHASE,
        }

        buffs_before: list[Buff] = []

        if has_active_engagement:
            buffs_before.append(
                Buff(
                    ACTIVE_ENGAGEMENT_BUFF,
                    ModifierType.ADDITIVE,
                    SpecialAttribute.DAMAGE_BOOST,
                    DamageTag.ALL,
                )
            )

        # The damage dealt by this attack is increased by (3% x the number of Negative Charge) on the battlefield, to a maximum increase of 15%.
        # If the target is a boss unit which has Negative Charge, the damage dealt is directly increased by 15%.
        maximum_damage_boost_from_negative_charge: int = 15
        damage_boost_per_negative_charge: int = 3
        if target_is_boss_with_negative_charge:
            buffs_before.append(
                Buff(
                    maximum_damage_boost_from_negative_charge,
                    ModifierType.ADDITIVE,
                    SpecialAttribute.DAMAGE_BOOST,
                    DamageTag.ALL,
                )
            )
        elif number_negative_charge_on_field > 0:
            buffs_before.append(
                Buff(
                    min(
                        number_negative_charge_on_field
                        * damage_boost_per_negative_charge,
                        maximum_damage_boost_from_negative_charge,
                    ),
                    ModifierType.ADDITIVE,
                    SpecialAttribute.DAMAGE_BOOST,
                    DamageTag.ALL,
                )
            )

        # Expansion Key - Squirrel's Awakening: Increase the critical damage of this attack by 5% for each Positive Charge on the field, up to 25%.
        critical_damage_per_positive_charge: int = 5
        maximum_critical_damage_from_positive_charge: int = 25
        if number_positive_charge_on_field > 0:
            buffs_before.append(
                Buff(
                    min(
                        number_positive_charge_on_field
                        * critical_damage_per_positive_charge,
                        maximum_critical_damage_from_positive_charge,
                    ),
                    ModifierType.ADDITIVE,
                    SpecialAttribute.CRITICAL_DAMAGE,
                    DamageTag.ALL,
                )
            )

        return DamageInstance(
            label=label,
            base_potency=base_potency,
            tags=tags,
            group_name="Sylvan Vault",
            buffs_before=buffs_before,
            damage_calculation_strategy=BelkaDamageCalculationStrategy(),
        )


class SylvanVaultV5(CombatAction):
    """Belka S1 (V5)."""

    @override
    def execute(
        self,
        has_active_engagement: bool,
        number_positive_charge_on_field: int,
        number_negative_charge_on_field: int,
        target_is_boss_with_negative_charge: bool,
    ) -> DamageInstance:
        label: str = "Sylvan Vault"
        base_potency: int = 130
        tags: set[DamageTag] = {
            DamageTag.ACTIVE,
            DamageTag.CONFECTANCE,
            DamageTag.MEDIUM_AMMO,
            DamageTag.TARGETED,
            DamageTag.ELECTRIC,  # Expansion Key - Squirrel's Awakening changes this to Electric; no need to be conditional on Active Engagement
            DamageTag.PHASE,
        }

        buffs_before: list[Buff] = []

        if has_active_engagement:
            buffs_before.append(
                Buff(
                    ACTIVE_ENGAGEMENT_BUFF,
                    ModifierType.ADDITIVE,
                    SpecialAttribute.DAMAGE_BOOST,
                    DamageTag.ALL,
                )
            )

        # The damage dealt by this attack is increased by (6% x the number of Negative Charge) on the battlefield, to a maximum increase of 30%.
        # If the target is a boss unit which has Negative Charge, the damage dealt is directly increased by 30%.
        maximum_damage_boost_from_negative_charge: int = 30
        damage_boost_per_negative_charge: int = 6
        if target_is_boss_with_negative_charge:
            buffs_before.append(
                Buff(
                    maximum_damage_boost_from_negative_charge,
                    ModifierType.ADDITIVE,
                    SpecialAttribute.DAMAGE_BOOST,
                    DamageTag.ALL,
                )
            )
        elif number_negative_charge_on_field > 0:
            buffs_before.append(
                Buff(
                    min(
                        number_negative_charge_on_field
                        * damage_boost_per_negative_charge,
                        maximum_damage_boost_from_negative_charge,
                    ),
                    ModifierType.ADDITIVE,
                    SpecialAttribute.DAMAGE_BOOST,
                    DamageTag.ALL,
                )
            )

        # Expansion Key - Squirrel's Awakening: Increase the critical damage of this attack by 5% for each Positive Charge on the field, up to 25%.
        critical_damage_per_positive_charge: int = 5
        maximum_critical_damage_from_positive_charge: int = 25
        if number_positive_charge_on_field > 0:
            buffs_before.append(
                Buff(
                    min(
                        number_positive_charge_on_field
                        * critical_damage_per_positive_charge,
                        maximum_critical_damage_from_positive_charge,
                    ),
                    ModifierType.ADDITIVE,
                    SpecialAttribute.CRITICAL_DAMAGE,
                    DamageTag.ALL,
                )
            )

        # The critical damage dealt by this attack is increased by 30%.
        buffs_before.append(
            Buff(
                30,
                ModifierType.ADDITIVE,
                SpecialAttribute.CRITICAL_DAMAGE,
                DamageTag.ALL,
            )
        )

        return DamageInstance(
            label=label,
            base_potency=base_potency,
            tags=tags,
            group_name="Sylvan Vault",
            buffs_before=buffs_before,
            damage_calculation_strategy=BelkaDamageCalculationStrategy(),
        )


class CracklingCore(CombatAction):
    """Belka S2."""

    @override
    def execute(
        self,
        has_active_engagement: bool,
        mobility_expended: int,
        has_fixed_key_4: bool,
        target_has_negative_charge: bool,
    ) -> DamageInstance:
        label: str = "Crackling Core"
        base_potency: int = 130
        tags: set[DamageTag] = {
            DamageTag.ACTIVE,
            DamageTag.MEDIUM_AMMO,
            DamageTag.TARGETED,
            DamageTag.ELECTRIC,
            DamageTag.PHASE,
        }

        buffs_before: list[Buff] = []

        if has_active_engagement:
            buffs_before.append(
                Buff(
                    ACTIVE_ENGAGEMENT_BUFF,
                    ModifierType.ADDITIVE,
                    SpecialAttribute.DAMAGE_BOOST,
                    DamageTag.ALL,
                )
            )

        damage_multiplier_per_mobility_expended: int = 5

        # Expansion Key - Squirrel's Awakening: If movement point expended is less than 10, damage will be calculated as if 10 movement points were expended.
        effective_mobility_expended: int = max(mobility_expended, 10)
        base_potency += (
            effective_mobility_expended * damage_multiplier_per_mobility_expended
        )

        # Fixed Key 4 - Raised Tail: When using this skill to attack an enemy with Negative Charge, Belka's attack is increased by 10%.
        if has_fixed_key_4 and target_has_negative_charge:
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
            group_name="Crackling Core",
            buffs_before=buffs_before,
            damage_calculation_strategy=BelkaDamageCalculationStrategy(),
        )


class CracklingCoreV1(CombatAction):
    """Belka S2 (V1)."""

    @override
    def execute(
        self,
        has_active_engagement: bool,
        mobility_expended: int,
        has_fixed_key_4: bool,
        target_has_negative_charge: bool,
    ) -> DamageInstance:
        label: str = "Crackling Core"
        base_potency: int = 130
        tags: set[DamageTag] = {
            DamageTag.ACTIVE,
            DamageTag.MEDIUM_AMMO,
            DamageTag.TARGETED,
            DamageTag.ELECTRIC,
            DamageTag.PHASE,
        }

        buffs_before: list[Buff] = []

        if has_active_engagement:
            buffs_before.append(
                Buff(
                    ACTIVE_ENGAGEMENT_BUFF,
                    ModifierType.ADDITIVE,
                    SpecialAttribute.DAMAGE_BOOST,
                    DamageTag.ALL,
                )
            )

        damage_multiplier_per_mobility_expended: int = 8

        # Expansion Key - Squirrel's Awakening: If movement point expended is less than 10, damage will be calculated as if 10 movement points were expended.
        effective_mobility_expended: int = max(mobility_expended, 10)
        base_potency += (
            effective_mobility_expended * damage_multiplier_per_mobility_expended
        )

        # Fixed Key 4 - Raised Tail: When using this skill to attack an enemy with Negative Charge, Belka's attack is increased by 10%.
        if has_fixed_key_4 and target_has_negative_charge:
            buffs_before.append(
                Buff(
                    10,
                    ModifierType.MULTIPLICATIVE,
                    StatType.ATTACK,
                    DamageTag.ALL,
                )
            )

        # Damage dealt to enemies with Negative Charge is increased by 15%.
        if target_has_negative_charge:
            buffs_before.append(
                Buff(
                    15,
                    ModifierType.ADDITIVE,
                    SpecialAttribute.DAMAGE_BOOST,
                    DamageTag.ALL,
                )
            )

        return DamageInstance(
            label=label,
            base_potency=base_potency,
            tags=tags,
            group_name="Crackling Core",
            buffs_before=buffs_before,
            damage_calculation_strategy=BelkaDamageCalculationStrategy(),
        )


class LeapingArc(CombatAction):
    """Belka Ultimate."""

    @override
    def execute(
        self,
        mobility_expended: int,
        number_of_electric_debuffs_on_target: int,
    ) -> DamageInstance:
        label: str = "Leaping Arc"
        base_potency: int = 160
        tags: set[DamageTag] = {
            DamageTag.ACTIVE,
            DamageTag.MEDIUM_AMMO,
            DamageTag.TARGETED,
            DamageTag.ELECTRIC,
            DamageTag.PHASE,
        }

        buffs_before: list[Buff] = []

        damage_multiplier_per_mobility_expended: int = 5

        # Expansion Key - Squirrel's Awakening: If movement point expended is less than 10, damage will be calculated as if 10 movement points were expended.
        effective_mobility_expended: int = max(mobility_expended, 10)
        base_potency += (
            effective_mobility_expended * damage_multiplier_per_mobility_expended
        )

        return DamageInstance(
            label=label,
            base_potency=base_potency,
            tags=tags,
            group_name="Leaping Arc",
            buffs_before=buffs_before,
            damage_calculation_strategy=BelkaDamageCalculationStrategy(),
        )


class LeapingArcV6(CombatAction):
    """Belka Ultimate (V6)."""

    @override
    def execute(
        self,
        mobility_expended: int,
        number_of_electric_debuffs_on_target: int,
    ) -> DamageInstance:
        label: str = "Leaping Arc"
        base_potency: int = 160
        tags: set[DamageTag] = {
            DamageTag.ACTIVE,
            DamageTag.MEDIUM_AMMO,
            DamageTag.TARGETED,
            DamageTag.ELECTRIC,
            DamageTag.PHASE,
        }

        buffs_before: list[Buff] = []

        # If the target has 2 or more Electric debuffs, critical damage increases by 30%.
        if number_of_electric_debuffs_on_target >= 2:
            buffs_before.append(
                Buff(
                    30,
                    ModifierType.ADDITIVE,
                    SpecialAttribute.CRITICAL_DAMAGE,
                    DamageTag.ALL,
                )
            )

        damage_multiplier_per_mobility_expended: int = 10

        # Expansion Key - Squirrel's Awakening: If movement point expended is less than 10, damage will be calculated as if 10 movement points were expended.
        effective_mobility_expended: int = max(mobility_expended, 10)
        base_potency += (
            effective_mobility_expended * damage_multiplier_per_mobility_expended
        )

        return DamageInstance(
            label=label,
            base_potency=base_potency,
            tags=tags,
            group_name="Leaping Arc",
            buffs_before=buffs_before,
            damage_calculation_strategy=BelkaDamageCalculationStrategy(),
        )


class ContinualRelease(CombatAction):
    """Damage effect from this buff granted by Leaping Arc."""

    @override
    def execute(self) -> DamageInstance:
        label: str = "Continual Release"
        base_potency: int = 80
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
            group_name="Continual Release",
            damage_calculation_strategy=BelkaDamageCalculationStrategy(),
        )


class ContinualReleaseV6(CombatAction):
    """Damage effect from this buff granted by Leaping Arc (V6)."""

    @override
    def execute(self) -> DamageInstance:
        label: str = "Continual Release"
        base_potency: int = 110
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
            group_name="Continual Release",
            damage_calculation_strategy=BelkaDamageCalculationStrategy(),
        )


class OverflowingElectrons(CombatAction):
    """Effect triggered when the target of Continual Release is the same as that of Leaping Arc. Only available at V2."""

    @override
    def execute(self) -> DamageInstance:
        label: str = "Overflowing Electrons"
        base_potency: int = 0

        return FixedDamageInstance(
            label=label,
            base_potency=base_potency,
            group_name="Overflowing Electrons",
        )


class OverflowingElectronsV2(CombatAction):
    """Effect triggered when the target of Continual Release is the same as that of Leaping Arc."""

    @override
    def execute(self) -> DamageInstance:
        label: str = "Overflowing Electrons"
        base_potency: int = 100

        return FixedDamageInstance(
            label=label,
            base_potency=base_potency,
            group_name="Overflowing Electrons",
        )


class Belka(Doll):
    """Belka."""

    name: str = "Belka"
    irrelevant_damage_tags: ClassVar[set[DamageTag]] = set(
        [
            DamageTag.CORROSION,
            DamageTag.FREEZE,
            DamageTag.HYDRO,
            DamageTag.BURN,
            DamageTag.MELEE,
            DamageTag.LIGHT_AMMO,
            DamageTag.HEAVY_AMMO,
            DamageTag.SHOTGUN_AMMO,
            DamageTag.SUPPORT_ACTION,
            DamageTag.INTERCEPTION,
            DamageTag.COUNTERATTACK,
            DamageTag.AREA_OF_EFFECT,
        ]
    )

    nutcracker_shell: CombatAction = Field(default_factory=NutcrackerShell)
    sylvan_vault: CombatAction = Field(default_factory=SylvanVault)
    crackling_core: CombatAction = Field(default_factory=CracklingCore)
    leaping_arc: CombatAction = Field(default_factory=LeapingArc)
    continual_release: CombatAction = Field(default_factory=ContinualRelease)
    overflowing_electrons: CombatAction = Field(default_factory=OverflowingElectrons)

    def set_to_v0(self) -> None:
        """Sets Fortification Level to Segment00."""
        self.nutcracker_shell = NutcrackerShell()
        self.sylvan_vault = SylvanVault()
        self.crackling_core = CracklingCore()
        self.leaping_arc = LeapingArc()
        self.continual_release = ContinualRelease()
        self.overflowing_electrons = OverflowingElectrons()

    def set_to_v1(self) -> None:
        """Sets Fortification Level to Segment01."""
        self.set_to_v0()

        self.crackling_core = CracklingCoreV1()

    def set_to_v2(self) -> None:
        """Sets Fortification Level to Segment02."""
        self.set_to_v1()

        self.overflowing_electrons = OverflowingElectronsV2()

    def set_to_v5(self) -> None:
        """Sets Fortification Level to Segment05."""
        self.set_to_v2()

        self.sylvan_vault = SylvanVaultV5()

    def set_to_v6(self) -> None:
        """Sets Fortification Level to Segment06."""
        self.set_to_v5()

        self.leaping_arc = LeapingArcV6()
        self.continual_release = ContinualReleaseV6()

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
