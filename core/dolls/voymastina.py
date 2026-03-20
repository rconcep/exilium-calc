from dataclasses import dataclass, field
from typing import override, ClassVar

from core.types import DamageTag, ModifierType, StatType, SpecialAttribute, Doll, FortificationLevel
from core.buffs import Buff, Debuff, Crumble, DefenseDownII
from core.combat import DamageInstance, CombatAction


class DreadUltimatum(CombatAction):
    """Voymastina Basic Attack."""

    @override
    def execute(self) -> DamageInstance:
        label: str = "Dread Ultimatum"
        base_potency: int = 80
        tags: set[DamageTag] = {
            DamageTag.ACTIVE,
            DamageTag.BASIC,
            DamageTag.MEDIUM_AMMO,
            DamageTag.TARGETED,
            DamageTag.PHYSICAL,
        }

        return DamageInstance(label, base_potency, tags, group_name="Basic")


class SiriusFallPassive(CombatAction):
    """Passive effect of Sirius Fall (support action)."""

    @override
    def execute(self, has_fixed_key_4: bool = True) -> DamageInstance:
        label: str = "Sirius Fall (Support)"
        base_potency: int = 100
        tags: set[DamageTag] = {
            DamageTag.PASSIVE,
            DamageTag.SUPPORT_ACTION,
            DamageTag.AREA_OF_EFFECT,
            DamageTag.PHYSICAL,
        }

        buffs_before: list[Buff] = []
        if has_fixed_key_4:
            buffs_before.append(
                Buff(
                    value=20,
                    modifier_type=ModifierType.ADDITIVE,
                    stat_type=SpecialAttribute.DAMAGE_BOOST,
                    tag=DamageTag.ALL,
                )
            )

        return DamageInstance(
            label,
            base_potency,
            tags,
            group_name="Sirius Fall (passive)",
            buffs_before=buffs_before,
        )


class SiriusFallPassiveV1(CombatAction):
    """Passive effect of Sirius Fall (support action) (V1)."""

    @override
    def execute(self, has_fixed_key_4: bool = True) -> DamageInstance:
        label: str = "Sirius Fall (Support)"
        base_potency: int = 150
        tags: set[DamageTag] = {
            DamageTag.PASSIVE,
            DamageTag.SUPPORT_ACTION,
            DamageTag.AREA_OF_EFFECT,
            DamageTag.PHYSICAL,
        }

        buffs_before: list[Buff] = []
        if has_fixed_key_4:
            buffs_before.append(
                Buff(
                    value=20,
                    modifier_type=ModifierType.ADDITIVE,
                    stat_type=SpecialAttribute.DAMAGE_BOOST,
                    tag=DamageTag.ALL,
                )
            )

        return DamageInstance(
            label,
            base_potency,
            tags,
            group_name="Sirius Fall (passive)",
            buffs_before=buffs_before,
        )


class SiriusFallActive(CombatAction):
    """Active effect of Sirius Fall."""

    @override
    def execute(self, has_fixed_key_4: bool = True) -> DamageInstance:
        label: str = "Sirius Fall"
        base_potency: int = 120
        tags: set[DamageTag] = {
            DamageTag.ACTIVE,
            DamageTag.AREA_OF_EFFECT,
            DamageTag.PHYSICAL,
        }

        buffs_before: list[Buff] = []
        if has_fixed_key_4:
            buffs_before.append(
                Buff(
                    value=20,
                    modifier_type=ModifierType.ADDITIVE,
                    stat_type=SpecialAttribute.DAMAGE_BOOST,
                    tag=DamageTag.ALL,
                )
            )

        return DamageInstance(
            label,
            base_potency,
            tags,
            group_name="Sirius Fall (active)",
            buffs_before=buffs_before,
        )


class SiriusFallActiveV1(CombatAction):
    """Active effect of Sirius Fall (V1)."""

    @override
    def execute(self, has_fixed_key_4: bool = True) -> DamageInstance:
        label: str = "Sirius Fall"
        base_potency: int = 180
        tags: set[DamageTag] = {
            DamageTag.ACTIVE,
            DamageTag.AREA_OF_EFFECT,
            DamageTag.PHYSICAL,
        }

        buffs_before: list[Buff] = []
        if has_fixed_key_4:
            buffs_before.append(
                Buff(
                    value=20,
                    modifier_type=ModifierType.ADDITIVE,
                    stat_type=SpecialAttribute.DAMAGE_BOOST,
                    tag=DamageTag.ALL,
                )
            )

        return DamageInstance(
            label,
            base_potency,
            tags,
            group_name="Sirius Fall (active)",
            buffs_before=buffs_before,
        )


class EyeOfTheWhiteMastiffPassive(CombatAction):
    """Passive effect of Eye of the White Mastiff (at the start of battle)."""

    @override
    def execute(self) -> DamageInstance:
        label: str = "Eye of the White Mastiff (Passive)"
        base_potency: int = 100
        tags: set[DamageTag] = {
            DamageTag.PASSIVE,
            DamageTag.PHYSICAL,
            DamageTag.TARGETED,
        }

        return DamageInstance(
            label, base_potency, tags, group_name="Eye of the White Mastiff (passive)"
        )


class EyeOfTheWhiteMastiffPassiveV3(CombatAction):
    """Passive effect of Eye of the White Mastiff (at the start of battle) (V3)."""

    @override
    def execute(self) -> DamageInstance:
        label: str = "Eye of the White Mastiff (Passive)"
        base_potency: int = 300
        tags: set[DamageTag] = {
            DamageTag.PASSIVE,
            DamageTag.PHYSICAL,
            DamageTag.TARGETED,
        }

        return DamageInstance(
            label, base_potency, tags, group_name="Eye of the White Mastiff (passive)"
        )


class LockOnAttackV3(CombatAction):
    """Passive effect of Wolf Eye System from Eye of the White Mastiff (interception-like) (V3)."""

    @override
    def execute(self) -> DamageInstance:
        label: str = "Lock-On Attack"
        base_potency: int = 130
        tags: set[DamageTag] = {
            DamageTag.PASSIVE,
            DamageTag.PHYSICAL,
            DamageTag.AREA_OF_EFFECT,
        }

        return DamageInstance(label, base_potency, tags, group_name="Lock-On Attack")


class LockOnAttack(CombatAction):
    """Passive effect of Wolf's Eye System from Eye of the White Mastiff (interception-like)."""

    @override
    def execute(self) -> DamageInstance:
        label: str = "Lock-On Attack"
        base_potency: int = 80
        tags: set[DamageTag] = {
            DamageTag.PASSIVE,
            DamageTag.PHYSICAL,
            DamageTag.AREA_OF_EFFECT,
        }

        return DamageInstance(label, base_potency, tags, group_name="Lock-On Attack")


class PileBunkerPassive(CombatAction):
    """Passive effect of Pile Bunker (support)."""

    @override
    def execute(self) -> DamageInstance:
        label: str = "Pile Bunker (Passive)"
        base_potency: int = 150

        tags: set[DamageTag] = {
            DamageTag.PASSIVE,
            DamageTag.SUPPORT_ACTION,
            DamageTag.PHYSICAL,
            DamageTag.TARGETED,
            DamageTag.MELEE,
        }

        return DamageInstance(
            label, base_potency, tags, group_name="Pile Bunker (passive)"
        )


class PileBunkerPassiveV2(CombatAction):
    """Passive effect of Pile Bunker (support) (V2)."""

    @override
    def execute(self) -> DamageInstance:
        label: str = "Pile Bunker (Passive)"
        base_potency: int = 150

        tags: set[DamageTag] = {
            DamageTag.PASSIVE,
            DamageTag.SUPPORT_ACTION,
            DamageTag.PHYSICAL,
            DamageTag.TARGETED,
            DamageTag.MELEE,
        }

        buffs_before: list[Buff] = []
        buffs_before.append(
            Buff(
                value=10,
                modifier_type=ModifierType.MULTIPLICATIVE,
                stat_type=StatType.ATTACK,
            )
        )

        return DamageInstance(
            label,
            base_potency,
            tags,
            group_name="Pile Bunker (passive)",
            buffs_before=buffs_before,
            debuffs_before=[
                Crumble(),
            ],
        )


class PileBunkerPassiveV5(CombatAction):
    """Passive effect of Pile Bunker (support) (V5)."""

    @override
    def execute(self) -> DamageInstance:
        label: str = "Pile Bunker (Passive)"
        base_potency: int = 150

        tags: set[DamageTag] = {
            DamageTag.PASSIVE,
            DamageTag.SUPPORT_ACTION,
            DamageTag.PHYSICAL,
            DamageTag.TARGETED,
            DamageTag.MELEE,
            DamageTag.ULTIMATE,
        }

        buffs_before: list[Buff] = []
        buffs_before.append(
            Buff(
                value=10,
                modifier_type=ModifierType.MULTIPLICATIVE,
                stat_type=StatType.ATTACK,
            )
        )

        debuffs_before: list[Debuff] = []
        debuffs_before.append(DefenseDownII())
        debuffs_before.append(Crumble())

        return DamageInstance(
            label,
            base_potency,
            tags,
            group_name="Pile Bunker (passive)",
            buffs_before=buffs_before,
            debuffs_before=debuffs_before,
        )


class PileBunkerActive(CombatAction):
    """Voymastina Ultimate."""

    @override
    def execute(self, has_activated_fixed_key_6: bool = False) -> DamageInstance:
        label: str = "Pile Bunker"
        base_potency: int = 200

        tags: set[DamageTag] = {
            DamageTag.ACTIVE,
            DamageTag.PHYSICAL,
            DamageTag.AREA_OF_EFFECT,
            DamageTag.MELEE,
            DamageTag.ULTIMATE,
        }

        buffs_before: list[Buff] = []
        if has_activated_fixed_key_6:
            buffs_before.append(
                Buff(
                    value=15,
                    modifier_type=ModifierType.ADDITIVE,
                    stat_type=SpecialAttribute.DAMAGE_BOOST,
                    tag=DamageTag.ULTIMATE,
                )
            )

        return DamageInstance(
            label, base_potency, tags, group_name="Pile Bunker (active)"
        )


class PileBunkerActiveV2(CombatAction):
    """Voymastina Ultimate (V2)."""

    @override
    def execute(self, has_activated_fixed_key_6: bool = False) -> DamageInstance:
        label: str = "Pile Bunker"
        base_potency: int = 300

        tags: set[DamageTag] = {
            DamageTag.ACTIVE,
            DamageTag.PHYSICAL,
            DamageTag.AREA_OF_EFFECT,
            DamageTag.MELEE,
            DamageTag.ULTIMATE,
        }

        buffs_before: list[Buff] = []
        if has_activated_fixed_key_6:
            buffs_before.append(
                Buff(
                    value=15,
                    modifier_type=ModifierType.ADDITIVE,
                    stat_type=SpecialAttribute.DAMAGE_BOOST,
                    tag=DamageTag.ULTIMATE,
                )
            )

        buffs_before.append(
            Buff(
                value=10,
                modifier_type=ModifierType.MULTIPLICATIVE,
                stat_type=StatType.ATTACK,
            )
        )

        return DamageInstance(
            label,
            base_potency,
            tags,
            group_name="Pile Bunker (active)",
            buffs_before=buffs_before,
            debuffs_before=[
                Crumble(),
            ],
        )


class PileBunkerActiveV5(CombatAction):
    """Voymastina Ultimate (V5)."""

    @override
    def execute(self, has_activated_fixed_key_6: bool = False) -> DamageInstance:
        label: str = "Pile Bunker"
        base_potency: int = 300

        tags: set[DamageTag] = {
            DamageTag.ACTIVE,
            DamageTag.PHYSICAL,
            DamageTag.AREA_OF_EFFECT,
            DamageTag.MELEE,
            DamageTag.ULTIMATE,
        }

        buffs_before: list[Buff] = []
        if has_activated_fixed_key_6:
            buffs_before.append(
                Buff(
                    value=15,
                    modifier_type=ModifierType.ADDITIVE,
                    stat_type=SpecialAttribute.DAMAGE_BOOST,
                    tag=DamageTag.ULTIMATE,
                )
            )

        buffs_before.append(
            Buff(
                value=10,
                modifier_type=ModifierType.MULTIPLICATIVE,
                stat_type=StatType.ATTACK,
            )
        )

        debuffs_before: list[Debuff] = []
        debuffs_before.append(DefenseDownII())
        debuffs_before.append(Crumble())

        return DamageInstance(
            label,
            base_potency,
            tags,
            group_name="Pile Bunker (active)",
            buffs_before=buffs_before,
            debuffs_before=debuffs_before,
        )


@dataclass
class Voymastina(Doll):
    """Voymastina."""
    name: str = "Voymastina"
    irrelevant_damage_tags: ClassVar[set[DamageTag]] = set(
        [
            DamageTag.PHASE,
            DamageTag.CORROSION,
            DamageTag.FREEZE,
            DamageTag.HYDRO,
            DamageTag.BURN,
            DamageTag.ELECTRIC,
            DamageTag.LIGHT_AMMO,
            DamageTag.HEAVY_AMMO,
            DamageTag.SHOTGUN_AMMO,
            DamageTag.COUNTERATTACK,
        ]
    )

    dread_ultimatum: CombatAction = field(default_factory=DreadUltimatum)
    sirius_fall_passive: CombatAction = field(default_factory=SiriusFallPassive)
    sirius_fall_active: CombatAction = field(default_factory=SiriusFallActive)
    eye_of_the_white_mastiff_passive: CombatAction = field(
        default_factory=EyeOfTheWhiteMastiffPassive
    )
    lockon_attack: CombatAction = field(default_factory=LockOnAttack)
    pile_bunker_passive: CombatAction = field(default_factory=PileBunkerPassive)
    pile_bunker_active: CombatAction = field(default_factory=PileBunkerActive)

    def set_to_v0(self) -> None:
        """Sets Fortification Level to Segment00."""
        self.dread_ultimatum: CombatAction = DreadUltimatum()
        self.sirius_fall_passive: CombatAction = SiriusFallPassive()
        self.sirius_fall_active: CombatAction = SiriusFallActive()
        self.eye_of_the_white_mastiff_passive: CombatAction = (
            EyeOfTheWhiteMastiffPassive()
        )
        self.lockon_attack: CombatAction = LockOnAttack()
        self.pile_bunker_passive: CombatAction = PileBunkerPassive()
        self.pile_bunker_active: CombatAction = PileBunkerActive()

    def set_to_v1(self) -> None:
        """Sets Fortification Level to Segment01."""
        self.set_to_v0()

        self.sirius_fall_passive: CombatAction = SiriusFallPassiveV1()
        self.sirius_fall_active: CombatAction = SiriusFallActiveV1()

    def set_to_v2(self) -> None:
        """Sets Fortification Level to Segment02."""
        self.set_to_v1()

        self.pile_bunker_passive: CombatAction = PileBunkerPassiveV2()
        self.pile_bunker_active: CombatAction = PileBunkerActiveV2()

    def set_to_v3(self) -> None:
        """Sets Fortification Level to Segment03."""
        self.set_to_v0()

        self.eye_of_the_white_mastiff_passive: CombatAction = (
            EyeOfTheWhiteMastiffPassiveV3()
        )
        self.lockon_attack: CombatAction = LockOnAttackV3()

    def set_to_v5(self) -> None:
        """Sets Fortification Level to Segment05."""
        self.set_to_v3()

        self.pile_bunker_passive: CombatAction = PileBunkerPassiveV5()
        self.pile_bunker_active: CombatAction = PileBunkerActiveV5()

    def set_to_v6(self) -> None:
        """Sets Fortification Level to Segment06."""
        self.set_to_v5()

        self.initial_stats.special_attributes[
            SpecialAttribute.DEFENSE_IGNORE
        ].set_multiplier(DamageTag.PHYSICAL, 125)

    @override
    def set_fortification_level(self, level: FortificationLevel):
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
                self.set_to_v3()
            case FortificationLevel.SEGMENT05:
                self.set_to_v5()
            case FortificationLevel.SEGMENT06:
                self.set_to_v6()

    def get_sample_data(self) -> list[DamageInstance]:
        """Returns a sample single target rotation."""
        rotation_data: list[DamageInstance] = [
            # Turn 1
            self.eye_of_the_white_mastiff_passive.execute(),
            self.sirius_fall_passive.execute(),
            self.pile_bunker_passive.execute(),
            self.lockon_attack.execute(),
            self.sirius_fall_active.execute(),
            # Turn 2
            self.sirius_fall_passive.execute(),
            self.pile_bunker_passive.execute(),
            self.lockon_attack.execute(),
            self.pile_bunker_active.execute(),
            # Turn 3
            self.sirius_fall_passive.execute(),  # Hunting Rhythm = 5
            self.pile_bunker_passive.execute(),
            self.lockon_attack.execute(),
            self.sirius_fall_active.execute(),
            # Turn 4
            self.eye_of_the_white_mastiff_passive.execute(),
            self.sirius_fall_passive.execute(),
            self.pile_bunker_passive.execute(),
            self.lockon_attack.execute(),
            self.pile_bunker_active.execute(),
            # Turn 5
            self.sirius_fall_passive.execute(),
            self.pile_bunker_passive.execute(),
            self.lockon_attack.execute(),
            self.sirius_fall_active.execute(),
            # Turn 6
            self.sirius_fall_passive.execute(),
            self.pile_bunker_passive.execute(),
            self.lockon_attack.execute(),
            self.pile_bunker_active.execute(),
            # Turn 7
            self.sirius_fall_passive.execute(),
            self.pile_bunker_passive.execute(),
            self.lockon_attack.execute(),
            self.sirius_fall_active.execute(),
        ]

        return rotation_data
