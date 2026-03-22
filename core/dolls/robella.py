from typing import override, ClassVar
from dataclasses import dataclass, field

from core.types import DamageTag, FortificationLevel, Doll
from core.buffs import Buff
from core.combat import DamageInstance, CombatAction


class UltraShot(CombatAction):
    """Robella Basic Attack."""

    @override
    def execute(self, sense_weakness_stacks: int = 0) -> DamageInstance:
        potency_per_sense_weakness: int = 9
        label: str = f"Ultra Shot ({sense_weakness_stacks} Sense Weakness)"
        base_potency: int = 80 + potency_per_sense_weakness * min(
            sense_weakness_stacks, Robella.sense_weakness_stack_cap
        )
        tags: set[DamageTag] = {
            DamageTag.ACTIVE,
            DamageTag.BASIC,
            DamageTag.LIGHT_AMMO,
            DamageTag.TARGETED,
        }

        sense_weakness_threshold: int = 2
        if sense_weakness_stacks > sense_weakness_threshold:
            tags.update({DamageTag.FREEZE, DamageTag.PHASE})
        else:
            tags.add(DamageTag.PHYSICAL)

        return DamageInstance(label, base_potency, tags, group_name="Ultra Shot")


class UltraShotV6(CombatAction):
    """Robella Basic Attack (V6)."""

    @override
    def execute(self, sense_weakness_stacks: int = 0) -> DamageInstance:
        potency_per_sense_weakness: int = 9
        label: str = f"Ultra Shot ({sense_weakness_stacks} Sense Weakness)"
        base_potency: int = 80 + potency_per_sense_weakness * sense_weakness_stacks
        tags: set[DamageTag] = {
            DamageTag.ACTIVE,
            DamageTag.BASIC,
            DamageTag.LIGHT_AMMO,
            DamageTag.TARGETED,
        }

        buffs_before: list[Buff] = []

        sense_weakness_threshold: int = 2
        if sense_weakness_stacks > sense_weakness_threshold:
            tags.update({DamageTag.FREEZE, DamageTag.PHASE})
        else:
            tags.add(DamageTag.PHYSICAL)

        return DamageInstance(
            label,
            base_potency,
            tags,
            group_name="Ultra Shot",
            buffs_before=buffs_before,
        )


class Unity(CombatAction):
    """Effect when the allied unit with Unity from Light of Bond uses a skill
    or performs an interception.
    """

    @override
    def execute(self) -> DamageInstance:
        label: str = "Unity"
        base_potency: int = 20
        tags: set[DamageTag] = {
            DamageTag.PASSIVE,
            DamageTag.PHASE,
            DamageTag.FREEZE,
            DamageTag.TARGETED,
        }

        return DamageInstance(label, base_potency, tags, group_name="Unity")


class UnityEnhanced(CombatAction):
    """Effect when allied unit with Unity: Enhanced from Light of Bond uses a skill or
    performs an interception.
    """

    @override
    def execute(self) -> DamageInstance:
        label: str = "Unity: Enhanced"
        base_potency: int = 30
        tags: set[DamageTag] = {
            DamageTag.PASSIVE,
            DamageTag.PHASE,
            DamageTag.FREEZE,
            DamageTag.TARGETED,
        }

        return DamageInstance(label, base_potency, tags, group_name="Unity")


class FrigidInfiltration(CombatAction):
    """Effect when a target with Inspection from Robella ends its action within range."""

    @override
    def execute(
        self, inspection_stacks: int, sense_weakness_stacks: int = 0
    ) -> DamageInstance:
        potency_per_inspection: int = 3
        label: str = f"Frigid Infiltration ({inspection_stacks} Inspection)"
        base_potency: int = 150 + potency_per_inspection * inspection_stacks

        tags: set[DamageTag] = {
            DamageTag.PASSIVE,
            DamageTag.PHASE,
            DamageTag.FREEZE,
            DamageTag.TARGETED,
        }

        return DamageInstance(
            label, base_potency, tags, group_name="Frigid Infiltration"
        )


class FrigidInfiltrationV3(CombatAction):
    """Effect when a target with Inspection from Robella (V3) ends its action within range."""

    @override
    def execute(
        self, inspection_stacks: int, sense_weakness_stacks: int = 0
    ) -> DamageInstance:
        potency_per_inspection: int = 3
        label: str = f"Frigid Infiltration ({inspection_stacks} Inspection)"
        base_potency: int = 150 + potency_per_inspection * inspection_stacks

        base_potency_enhancement_threshold: int = 5
        base_potency_enhancement: int = 30
        if sense_weakness_stacks > base_potency_enhancement_threshold:
            base_potency += base_potency_enhancement

        tags: set[DamageTag] = {
            DamageTag.PASSIVE,
            DamageTag.PHASE,
            DamageTag.FREEZE,
            DamageTag.TARGETED,
        }

        return DamageInstance(
            label, base_potency, tags, group_name="Frigid Infiltration"
        )


class FrigidInfiltrationEnhanced(CombatAction):
    """Effect when a target with Inspection: Enhanced from Robella ends its action within range."""

    @override
    def execute(
        self, inspection_stacks: int, sense_weakness_stacks: int = 0
    ) -> DamageInstance:
        potency_per_inspection: int = 9
        label: str = f"Frigid Infiltration: Enhanced ({inspection_stacks} Inspection)"
        base_potency: int = 150 + potency_per_inspection * inspection_stacks

        tags: set[DamageTag] = {
            DamageTag.PASSIVE,
            DamageTag.PHASE,
            DamageTag.FREEZE,
            DamageTag.TARGETED,
        }

        return DamageInstance(
            label, base_potency, tags, group_name="Frigid Infiltration"
        )


class FrigidInfiltrationEnhancedV3(CombatAction):
    """Effect when a target with Inspection: Enhanced from Robella (V3) ends its action within range."""

    @override
    def execute(
        self, inspection_stacks: int, sense_weakness_stacks: int = 0
    ) -> DamageInstance:
        potency_per_inspection: int = 9
        label: str = f"Frigid Infiltration: Enhanced ({inspection_stacks} Inspection)"
        base_potency: int = 150 + potency_per_inspection * inspection_stacks

        base_potency_enhancement_threshold: int = 5
        base_potency_enhancement: int = 30
        if sense_weakness_stacks > base_potency_enhancement_threshold:
            base_potency += base_potency_enhancement

        tags: set[DamageTag] = {
            DamageTag.PASSIVE,
            DamageTag.PHASE,
            DamageTag.FREEZE,
            DamageTag.TARGETED,
        }

        return DamageInstance(
            label, base_potency, tags, group_name="Frigid Infiltration"
        )


class HowlingCyclone(CombatAction):
    """Robella Ultimate."""

    @override
    def execute(self, sense_weakness_stacks: int = 0) -> DamageInstance:
        potency_per_sense_weakness: int = 9
        label: str = f"Howling Cyclone ({sense_weakness_stacks} Sense Weakness)"
        base_potency: int = 120
        tags: set[DamageTag] = {
            DamageTag.ACTIVE,
            DamageTag.ULTIMATE,
            DamageTag.AREA_OF_EFFECT,
            DamageTag.FREEZE,
            DamageTag.PHASE,
            DamageTag.CONFECTANCE,
        }

        return DamageInstance(label, base_potency, tags, group_name="Howling Cyclone")


class HowlingCycloneV4(CombatAction):
    """Robella Ultimate (V4)."""

    @override
    def execute(self, sense_weakness_stacks: int = 0) -> DamageInstance:
        potency_per_sense_weakness: int = 9
        label: str = f"Howling Cyclone ({sense_weakness_stacks} Sense Weakness)"
        base_potency: int = 150
        tags: set[DamageTag] = {
            DamageTag.ACTIVE,
            DamageTag.ULTIMATE,
            DamageTag.AREA_OF_EFFECT,
            DamageTag.FREEZE,
            DamageTag.PHASE,
            DamageTag.CONFECTANCE,
        }

        base_potency += potency_per_sense_weakness * min(
            sense_weakness_stacks, Robella.sense_weakness_stack_cap
        )

        return DamageInstance(label, base_potency, tags, group_name="Howling Cyclone")


class HowlingCycloneV6(CombatAction):
    """Robella Ultimate (V6)."""

    @override
    def execute(self, sense_weakness_stacks: int = 0) -> DamageInstance:
        potency_per_sense_weakness: int = 9
        label: str = f"Howling Cyclone ({sense_weakness_stacks} Sense Weakness)"
        base_potency: int = 150
        tags: set[DamageTag] = {
            DamageTag.ACTIVE,
            DamageTag.ULTIMATE,
            DamageTag.AREA_OF_EFFECT,
            DamageTag.FREEZE,
            DamageTag.PHASE,
            DamageTag.CONFECTANCE,
        }

        base_potency += potency_per_sense_weakness * sense_weakness_stacks

        return DamageInstance(label, base_potency, tags, group_name="Howling Cyclone")


@dataclass
class Robella(Doll):
    """Robella."""
    name: str = "Robella"
    irrelevant_damage_tags: ClassVar[set[DamageTag]] = set(
        [
            DamageTag.CORROSION,
            DamageTag.BURN,
            DamageTag.HYDRO,
            DamageTag.ELECTRIC,
            DamageTag.MELEE,
            DamageTag.MEDIUM_AMMO,
            DamageTag.HEAVY_AMMO,
            DamageTag.SHOTGUN_AMMO,
            DamageTag.SUPPORT_ACTION,
            DamageTag.INTERCEPTION,
            DamageTag.COUNTERATTACK,
            DamageTag.AREA_OF_EFFECT,
        ]
    )
    sense_weakness_stack_cap: ClassVar[int] = 10

    ultra_shot: CombatAction = field(default_factory=UltraShot)
    unity: CombatAction = field(default_factory=Unity)
    unity_enhanced: CombatAction = field(default_factory=UnityEnhanced)
    frigid_infiltration: CombatAction = field(default_factory=FrigidInfiltration)
    frigid_infiltration_enhanced: CombatAction = field(
        default_factory=FrigidInfiltrationEnhanced
    )
    howling_cyclone: CombatAction = field(default_factory=HowlingCyclone)

    def set_to_v0(self) -> None:
        """Sets Fortification Level to Segment00."""
        self.ultra_shot: CombatAction = UltraShot()
        self.unity: CombatAction = Unity()
        self.unity_enhanced: CombatAction = UnityEnhanced()
        self.frigid_infiltration: CombatAction = FrigidInfiltration()
        self.frigid_infiltration_enhanced: CombatAction = FrigidInfiltrationEnhanced()
        self.howling_cyclone: CombatAction = HowlingCyclone()

    def set_to_v3(self) -> None:
        """Sets Fortification Level to Segment03."""
        self.set_to_v0()

        self.frigid_infiltration: CombatAction = FrigidInfiltrationV3()
        self.frigid_infiltration_enhanced: CombatAction = FrigidInfiltrationEnhancedV3()

    def set_to_v4(self) -> None:
        """Sets Fortification Level to Segment04."""
        self.set_to_v3()

        self.howling_cyclone: CombatAction = HowlingCycloneV4()

    def set_to_v6(self) -> None:
        """Sets Fortification Level to Segment06."""
        self.set_to_v4()

        self.ultra_shot: CombatAction = UltraShotV6()
        self.howling_cyclone: CombatAction = HowlingCycloneV6()

    @override
    def set_fortification_level(self, level: FortificationLevel):
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
                self.set_to_v4()
            case FortificationLevel.SEGMENT06:
                self.set_to_v6()

    def get_sample_data(self) -> list[DamageInstance]:
        """Returns a sample single target rotation."""
        rotation_data: list[DamageInstance] = [
            # Turn 1
            self.unity_enhanced.execute(),  # Alva S2
            self.unity_enhanced.execute(),  # Alva Ult
            self.unity_enhanced.execute(),  # Interception x3
            self.unity_enhanced.execute(),
            self.unity_enhanced.execute(),
            self.frigid_infiltration_enhanced.execute(
                inspection_stacks=6, sense_weakness_stacks=0
            ),
            # Turn 2
            self.howling_cyclone.execute(6),
            self.unity_enhanced.execute(),  # Alva Ult
            self.unity_enhanced.execute(),  # Interception x3
            self.unity_enhanced.execute(),
            self.unity_enhanced.execute(),
            self.frigid_infiltration_enhanced.execute(
                inspection_stacks=6, sense_weakness_stacks=6
            ),
            # Turn 3
            self.ultra_shot.execute(12),
            self.unity_enhanced.execute(),  # Alva Ult
            self.unity_enhanced.execute(),  # Interception x3
            self.unity_enhanced.execute(),
            self.unity_enhanced.execute(),
            self.frigid_infiltration_enhanced.execute(
                inspection_stacks=6, sense_weakness_stacks=12
            ),
            # Turn 4
            self.howling_cyclone.execute(18),
            self.unity_enhanced.execute(),  # Alva S2
            self.unity_enhanced.execute(),  # Alva Ult
            self.unity_enhanced.execute(),  # Interception x3
            self.unity_enhanced.execute(),
            self.unity_enhanced.execute(),
            self.frigid_infiltration_enhanced.execute(
                inspection_stacks=6, sense_weakness_stacks=18
            ),
            # Turn 5
            self.unity_enhanced.execute(),  # Alva Ult
            self.unity_enhanced.execute(),  # Interception x3
            self.unity_enhanced.execute(),
            self.unity_enhanced.execute(),
            self.frigid_infiltration_enhanced.execute(
                inspection_stacks=6, sense_weakness_stacks=24
            ),
            # Turn 6
            self.howling_cyclone.execute(30),
            self.unity_enhanced.execute(),  # Alva Ult
            self.unity_enhanced.execute(),  # Interception x3
            self.unity_enhanced.execute(),
            self.unity_enhanced.execute(),
            self.frigid_infiltration_enhanced.execute(
                inspection_stacks=6, sense_weakness_stacks=30
            ),
            # Turn 7
            self.howling_cyclone.execute(36),
            self.unity_enhanced.execute(),  # Alva S2
            self.unity_enhanced.execute(),  # Alva Ult
            self.unity_enhanced.execute(),  # Interception x3
            self.unity_enhanced.execute(),
            self.unity_enhanced.execute(),
            self.frigid_infiltration_enhanced.execute(
                inspection_stacks=6, sense_weakness_stacks=36
            ),
        ]

        return rotation_data
