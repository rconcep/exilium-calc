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
from core.combat import (
    DamageInstance,
    CombatAction,
    FixedDamageInstance,
    WelrodStandardDamageCalculationStrategy,
    WelrodSubjectiveSanctionDamageCalculationStrategy,
    WelrodIniquityRetributionDamageCalculationStrategy,
)


class HushedErasure(CombatAction):
    """Welrod Basic Attack."""

    @override
    def execute(self) -> DamageInstance:
        label: str = "Hushed Erasure"
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
            group_name="Hushed Erasure",
            damage_calculation_strategy=WelrodStandardDamageCalculationStrategy(),
        )


class JointInvestigation(CombatAction):
    """Welrod S1."""

    @override
    def execute(
        self,
    ) -> DamageInstance:
        label: str = "Joint Investigation"
        base_potency: int = 100
        tags: set[DamageTag] = {
            DamageTag.ACTIVE,
            DamageTag.CORROSION,
            DamageTag.PHASE,
            DamageTag.AREA_OF_EFFECT,
        }

        return DamageInstance(
            label=label,
            base_potency=base_potency,
            tags=tags,
            group_name="Joint Investigation",
            damage_calculation_strategy=WelrodStandardDamageCalculationStrategy(),
        )


class SubjectiveSanction(CombatAction):
    """Welrod S2."""

    @override
    def execute(
        self,
    ) -> DamageInstance:
        label: str = "Subjective Sanction"
        base_potency: int = 100
        tags: set[DamageTag] = {
            DamageTag.ACTIVE,
            DamageTag.CORROSION,
            DamageTag.PHASE,
            DamageTag.AREA_OF_EFFECT,
        }

        # For every 1% increase in max HP compared to initial HP, the damage multiplier
        # is increased by 1%, up to 60%.

        return DamageInstance(
            label=label,
            base_potency=base_potency,
            tags=tags,
            group_name="Subjective Sanction",
            damage_calculation_strategy=WelrodSubjectiveSanctionDamageCalculationStrategy(
                1, 60
            ),
        )


class SubjectiveSanctionV4(CombatAction):
    """Welrod S2 (V4)."""

    @override
    def execute(
        self,
    ) -> DamageInstance:
        label: str = "Subjective Sanction"
        base_potency: int = 120
        tags: set[DamageTag] = {
            DamageTag.ACTIVE,
            DamageTag.CORROSION,
            DamageTag.PHASE,
            DamageTag.TARGETED,
            DamageTag.CONFECTANCE,
        }

        # For every 1% increase in max HP compared to initial HP, the damage multiplier
        # is increased by 1.5%, up to 150%.

        return DamageInstance(
            label=label,
            base_potency=base_potency,
            tags=tags,
            group_name="Subjective Sanction",
            damage_calculation_strategy=WelrodSubjectiveSanctionDamageCalculationStrategy(
                1.5, 150
            ),
        )


class JudgementBlast(CombatAction):
    """Welrod ultimate."""

    @override
    def execute(
        self,
        instances_of_damage_taken: int,
        number_of_targets_hit: int,
    ) -> DamageInstance:
        label: str = "Judgement Blast"
        base_potency: int = 100
        tags: set[DamageTag] = {
            DamageTag.ACTIVE,
            DamageTag.CORROSION,
            DamageTag.PHASE,
            DamageTag.AREA_OF_EFFECT,
            DamageTag.ULTIMATE,
        }

        return DamageInstance(
            label=label,
            base_potency=base_potency,
            tags=tags,
            group_name="Judgement Blast",
            damage_calculation_strategy=WelrodStandardDamageCalculationStrategy(),
        )


class JudgementBlastV3(CombatAction):
    """Welrod ultimate (V3)."""

    @override
    def execute(
        self,
        instances_of_damage_taken: int,
        number_of_targets_hit: int,
    ) -> DamageInstance:
        label: str = "Judgement Blast"
        base_potency: int = 120
        tags: set[DamageTag] = {
            DamageTag.ACTIVE,
            DamageTag.CORROSION,
            DamageTag.PHASE,
            DamageTag.AREA_OF_EFFECT,
            DamageTag.ULTIMATE,
        }

        return DamageInstance(
            label=label,
            base_potency=base_potency,
            tags=tags,
            group_name="Judgement Blast",
            damage_calculation_strategy=WelrodStandardDamageCalculationStrategy(),
        )


class JudgementBlastV5(CombatAction):
    """Welrod ultimate (V5)."""

    @override
    def execute(
        self,
        instances_of_damage_taken: int,
        number_of_targets_hit: int,
    ) -> DamageInstance:
        label: str = "Judgement Blast"
        base_potency: int = 120
        tags: set[DamageTag] = {
            DamageTag.ACTIVE,
            DamageTag.CORROSION,
            DamageTag.PHASE,
            DamageTag.AREA_OF_EFFECT,
            DamageTag.ULTIMATE,
        }

        buffs_before: list[Buff] = []

        # For every instance of damage taken, damage dealt is increased by 40%, up to 80%.
        damage_boost_per_instance_of_damage_taken: int = 40
        max_damage_boost: int = 80
        buffs_before.append(
            Buff(
                min(
                    max(0, instances_of_damage_taken)
                    * damage_boost_per_instance_of_damage_taken,
                    max_damage_boost,
                ),
                ModifierType.ADDITIVE,
                SpecialAttribute.DAMAGE_BOOST,
                DamageTag.ALL,
            )
        )

        # For every enemy unit hit, the damage dealt is increased by 20%, up to 100%.
        damage_boost_per_target_hit: int = 20
        max_damage_boost_from_targets: int = 100
        buffs_before.append(
            Buff(
                min(
                    max(0, number_of_targets_hit) * damage_boost_per_target_hit,
                    max_damage_boost_from_targets,
                ),
                ModifierType.ADDITIVE,
                SpecialAttribute.DAMAGE_BOOST,
                DamageTag.ALL,
            )
        )

        return DamageInstance(
            label=label,
            base_potency=base_potency,
            tags=tags,
            group_name="Judgement Blast",
            buffs_before=buffs_before,
            damage_calculation_strategy=WelrodStandardDamageCalculationStrategy(),
        )


class IniquityRetributionAction(CombatAction):
    """Damage dealt by Welrod upon application of Iniquity's Retribution or at the
    end of the debuff holder's action.
    """

    @override
    def execute(self, detectives_immunity_accumulated_damage) -> DamageInstance:
        label: str = "Iniquity's Retribution"
        base_potency: int = 100
        tags: set[DamageTag] = {
            DamageTag.PASSIVE,
            DamageTag.CORROSION,
            DamageTag.PHASE,
            DamageTag.AREA_OF_EFFECT,
        }

        return DamageInstance(
            label=label,
            base_potency=base_potency,
            tags=tags,
            group_name="Iniquity's Retribution",
            damage_calculation_strategy=WelrodIniquityRetributionDamageCalculationStrategy(
                detectives_immunity_accumulated_damage, 0.25, 0.15
            ),
        )


class IniquityRetributionActionV3(CombatAction):
    """Damage dealt by Welrod upon application of Iniquity's Retribution or at the
    end of the debuff holder's action.
    """

    @override
    def execute(self, detectives_immunity_accumulated_damage) -> DamageInstance:
        label: str = "Iniquity's Retribution"
        base_potency: int = 100
        tags: set[DamageTag] = {
            DamageTag.PASSIVE,
            DamageTag.CORROSION,
            DamageTag.PHASE,
            DamageTag.AREA_OF_EFFECT,
        }

        return DamageInstance(
            label=label,
            base_potency=base_potency,
            tags=tags,
            group_name="Iniquity's Retribution",
            damage_calculation_strategy=WelrodIniquityRetributionDamageCalculationStrategy(
                detectives_immunity_accumulated_damage, 0.50, 0.30
            ),
        )


class SuspectAction(CombatAction):
    """Damage dealt by Welrod at the end of the debuff holder's action.
    This is the version based on the debuff holder being a Boss, not
    the version that deals damage based on the holder's max HP.
    """

    @override
    def execute(self) -> DamageInstance:
        label: str = "Suspect"
        base_potency: int = 180

        return FixedDamageInstance(
            label=label,
            base_potency=base_potency,
            group_name="Suspect",
            damage_calculation_strategy=WelrodStandardDamageCalculationStrategy(),
        )


class SuspectActionV5(CombatAction):
    """Damage dealt by Welrod at the end of the debuff holder's action.
    This is the version based on the debuff holder being a Boss, not
    the version that deals damage based on the holder's max HP.
    """

    @override
    def execute(self) -> DamageInstance:
        label: str = "Suspect"
        base_potency: int = 360

        return FixedDamageInstance(
            label=label,
            base_potency=base_potency,
            group_name="Suspect",
            damage_calculation_strategy=WelrodStandardDamageCalculationStrategy(),
        )


class CaseControllerEndOfAction(CombatAction):
    """Damage dealt by Welrod at the end of her action or another allied Doll's action (V2)
    as part of her passive."""

    @override
    def execute(self, detectives_immunity_accumulated_damage) -> DamageInstance:
        label: str = "Case Controller"
        base_potency: int = 100
        tags: set[DamageTag] = {
            DamageTag.PASSIVE,
            DamageTag.CORROSION,
            DamageTag.PHASE,
            DamageTag.AREA_OF_EFFECT,
        }

        return DamageInstance(
            label=label,
            base_potency=base_potency,
            tags=tags,
            group_name="Case Controller",
            damage_calculation_strategy=WelrodIniquityRetributionDamageCalculationStrategy(
                detectives_immunity_accumulated_damage, 0.30, 0
            ),
        )


class Welrod(Doll):
    """Welrod."""

    name: str = "Welrod"
    irrelevant_damage_tags: ClassVar[set[DamageTag]] = set(
        [
            DamageTag.ELECTRIC,
            DamageTag.BURN,
            DamageTag.HYDRO,
            DamageTag.FREEZE,
            DamageTag.MEDIUM_AMMO,
            DamageTag.HEAVY_AMMO,
            DamageTag.SHOTGUN_AMMO,
            DamageTag.INTERCEPTION,
            DamageTag.COUNTERATTACK,
            DamageTag.SUPPORT_ACTION,
        ]
    )

    hushed_erasure: CombatAction = Field(default_factory=HushedErasure)
    joint_investigation: CombatAction = Field(default_factory=JointInvestigation)
    subjective_sanction: CombatAction = Field(default_factory=SubjectiveSanction)
    iniquity_retribution: CombatAction = Field(
        default_factory=IniquityRetributionAction
    )
    suspect: CombatAction = Field(default_factory=SuspectAction)
    judgement_blast: CombatAction = Field(default_factory=JudgementBlast)
    case_controller: CombatAction = Field(default_factory=CaseControllerEndOfAction)

    def set_to_v0(self) -> None:
        """Sets Fortification Level to Segment00."""
        self.hushed_erasure = HushedErasure()
        self.joint_investigation = JointInvestigation()
        self.subjective_sanction = SubjectiveSanction()
        self.iniquity_retribution = IniquityRetributionAction()
        self.suspect = SuspectAction()
        self.judgement_blast = JudgementBlast()
        self.case_controller = CaseControllerEndOfAction()

    def set_to_v3(self) -> None:
        """Sets Fortification Level to Segment03."""
        self.set_to_v0()
        self.judgement_blast = JudgementBlastV3()
        self.iniquity_retribution = IniquityRetributionActionV3()

    def set_to_v4(self) -> None:
        """Sets Fortification Level to Segment04."""
        self.set_to_v3()
        self.subjective_sanction = SubjectiveSanctionV4()

    def set_to_v5(self) -> None:
        """Sets Fortification Level to Segment05."""
        self.set_to_v4()
        self.judgement_blast = JudgementBlastV5()
        self.suspect = SuspectActionV5()

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
                self.set_to_v5()
