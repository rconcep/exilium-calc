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
from core.combat import DamageInstance, CombatAction


class Playtime(CombatAction):
    """Lewis Basic Attack."""

    @override
    def execute(self) -> DamageInstance:
        label: str = "Playtime"
        base_potency: int = 80
        tags: set[DamageTag] = {
            DamageTag.ACTIVE,
            DamageTag.BASIC,
            DamageTag.HEAVY_AMMO,
            DamageTag.TARGETED,
            DamageTag.PHYSICAL,
        }

        return DamageInstance(
            label=label, base_potency=base_potency, tags=tags, group_name="Playtime"
        )


class BadGuyCleanup(CombatAction):
    """Lewis S1."""

    @override
    def execute(self) -> DamageInstance:
        label: str = "Bad Guy Cleanup"
        base_potency: int = 80
        tags: set[DamageTag] = {
            DamageTag.ACTIVE,
            DamageTag.AREA_OF_EFFECT,
            DamageTag.BURN,
        }

        # TODO: Overburn 10%

        return DamageInstance(
            label=label,
            base_potency=base_potency,
            tags=tags,
            group_name="Bad Guy Cleanup",
        )


class BadGuyCleanupV4(CombatAction):
    """Lewis S1 (V4)."""

    @override
    def execute(self) -> DamageInstance:
        label: str = "Bad Guy Cleanup"
        base_potency: int = 120
        tags: set[DamageTag] = {
            DamageTag.ACTIVE,
            DamageTag.AREA_OF_EFFECT,
            DamageTag.BURN,
        }

        # TODO: Implement +10% damage per burn debuff on target

        return DamageInstance(
            label=label,
            base_potency=base_potency,
            tags=tags,
            group_name="Bad Guy Cleanup",
        )


class SurprisingFunball(CombatAction):
    """Lewis S2."""

    @override
    def execute(self) -> DamageInstance:
        label: str = "Surprising Funball"
        base_potency: int = 140
        tags: set[DamageTag] = {
            DamageTag.ACTIVE,
            DamageTag.TARGETED,
            DamageTag.BURN,
            DamageTag.HEAVY_AMMO,
        }

        # TODO: 30% fixed damage, 2 stacks Tin Soldier's order

        return DamageInstance(
            label=label,
            base_potency=base_potency,
            tags=tags,
            group_name="Surprising Funball",
        )


class SurprisingFunballV3(CombatAction):
    """Lewis S2 (V3)."""

    @override
    def execute(self) -> DamageInstance:
        label: str = "Surprising Funball"
        base_potency: int = 160
        tags: set[DamageTag] = {
            DamageTag.ACTIVE,
            DamageTag.TARGETED,
            DamageTag.BURN,
            DamageTag.HEAVY_AMMO,
        }

        return DamageInstance(
            label=label,
            base_potency=base_potency,
            tags=tags,
            group_name="Surprising Funball",
        )


class ToyCarnival(CombatAction):
    """Lewis Ultimate."""

    @override
    def execute(
        self, cumulative_tin_soldier_ranks: int, highest_rank_tin_soldier: int
    ) -> DamageInstance:
        potency_per_soldier_rank: int = 15
        label: str = "Toy Carnival"
        base_potency: int = (
            180 + cumulative_tin_soldier_ranks * potency_per_soldier_rank
        )
        tags: set[DamageTag] = {
            DamageTag.ACTIVE,
            DamageTag.TARGETED,
            DamageTag.BURN,
            DamageTag.HEAVY_AMMO,
            DamageTag.ULTIMATE,
            DamageTag.CONFECTANCE,
        }

        buff: Buff = Buff(
            5 * cumulative_tin_soldier_ranks, ModifierType.ADDITIVE, StatType.CRIT_RATE
        )

        return DamageInstance(
            label=label,
            base_potency=base_potency,
            tags=tags,
            group_name="Toy Carnival",
            buffs_before=[
                buff,
            ],
        )


class ToyCarnivalV2(CombatAction):
    """Lewis Ultimate (V2)."""

    @override
    def execute(
        self, cumulative_tin_soldier_ranks: int, highest_rank_tin_soldier: int
    ) -> DamageInstance:
        potency_per_soldier_rank: int = 15
        label: str = "Toy Carnival"
        base_potency: int = (
            180 + cumulative_tin_soldier_ranks * potency_per_soldier_rank
        )
        tags: set[DamageTag] = {
            DamageTag.ACTIVE,
            DamageTag.TARGETED,
            DamageTag.BURN,
            DamageTag.HEAVY_AMMO,
            DamageTag.ULTIMATE,
            DamageTag.CONFECTANCE,
        }

        if highest_rank_tin_soldier == 3:
            base_potency += 20

        buffs_before: list[Buff] = []
        buffs_before.append(
            Buff(
                5 * cumulative_tin_soldier_ranks,
                ModifierType.ADDITIVE,
                StatType.CRIT_RATE,
            )
        )

        if highest_rank_tin_soldier >= 1:
            buffs_before.append(
                Buff(
                    20,
                    ModifierType.ADDITIVE,
                    SpecialAttribute.DAMAGE_BOOST,
                    DamageTag.ALL,
                )
            )

        return DamageInstance(
            label=label,
            base_potency=base_potency,
            tags=tags,
            group_name="Toy Carnival",
            buffs_before=buffs_before,
        )


class ToyCarnivalV5(CombatAction):
    """Lewis Ultimate (V5)."""

    @override
    def execute(
        self, cumulative_tin_soldier_ranks: int, highest_rank_tin_soldier: int
    ) -> DamageInstance:
        potency_per_soldier_rank: int = 10
        label: str = "Toy Carnival"
        base_potency: int = (
            180 + cumulative_tin_soldier_ranks * potency_per_soldier_rank
        )
        tags: set[DamageTag] = {
            DamageTag.ACTIVE,
            DamageTag.TARGETED,
            DamageTag.BURN,
            DamageTag.HEAVY_AMMO,
            DamageTag.ULTIMATE,
            DamageTag.CONFECTANCE,
        }

        if highest_rank_tin_soldier == 3:
            base_potency += 20

        buffs_before: list[Buff] = []
        buffs_before.append(
            Buff(
                5 * cumulative_tin_soldier_ranks,
                ModifierType.ADDITIVE,
                StatType.CRIT_RATE,
            )
        )
        buffs_before.append(
            Buff(
                5 * cumulative_tin_soldier_ranks,
                ModifierType.ADDITIVE,
                StatType.CRIT_DAMAGE,
            )
        )

        if highest_rank_tin_soldier >= 1:
            buffs_before.append(
                Buff(
                    20,
                    ModifierType.ADDITIVE,
                    SpecialAttribute.DAMAGE_BOOST,
                    DamageTag.ALL,
                )
            )

        return DamageInstance(
            label=label,
            base_potency=base_potency,
            tags=tags,
            group_name="Toy Carnival",
            buffs_before=buffs_before,
        )


class VolleyFire(CombatAction):
    """Attack from Tin Soldier."""

    @override
    def execute(
        self, tin_soldier_rank: int, has_tin_soldiers_order: bool
    ) -> DamageInstance:
        potency_per_soldier_rank: int = 10
        label: str = f"Volley Fire (Rank {tin_soldier_rank})"
        base_potency: int = 100 + tin_soldier_rank * potency_per_soldier_rank
        tags: set[DamageTag] = {DamageTag.PASSIVE, DamageTag.TARGETED, DamageTag.BURN}

        if has_tin_soldiers_order:
            base_potency += 30

        return DamageInstance(
            label=label, base_potency=base_potency, tags=tags, group_name="Volley Fire"
        )


class VolleyFireV1(CombatAction):
    """Attack from Tin Soldier (V1)."""

    @override
    def execute(
        self, tin_soldier_rank: int, has_tin_soldiers_order: bool = False
    ) -> DamageInstance:
        potency_per_soldier_rank: int = 10
        label: str = f"Volley Fire (Rank {tin_soldier_rank})"
        base_potency: int = 120 + tin_soldier_rank * potency_per_soldier_rank
        tags: set[DamageTag] = {DamageTag.PASSIVE, DamageTag.TARGETED, DamageTag.BURN}

        if has_tin_soldiers_order:
            base_potency += 30

        # TODO: Trigger Overburn one time per Rank

        return DamageInstance(
            label=label, base_potency=base_potency, tags=tags, group_name="Volley Fire"
        )


class VolleyFireV3(CombatAction):
    """Attack from Tin Soldier (V3)."""

    @override
    def execute(
        self, tin_soldier_rank: int, has_tin_soldiers_order: bool = False
    ) -> DamageInstance:
        potency_per_soldier_rank: int = 10
        label: str = f"Volley Fire (Rank {tin_soldier_rank})"
        base_potency: int = 120 + tin_soldier_rank * potency_per_soldier_rank
        tags: set[DamageTag] = {DamageTag.PASSIVE, DamageTag.TARGETED, DamageTag.BURN}

        if has_tin_soldiers_order:
            base_potency += 50

        # TODO: Trigger Overburn one time per Rank

        return DamageInstance(
            label=label, base_potency=base_potency, tags=tags, group_name="Volley Fire"
        )


class Lewis(Doll):
    """Lewis."""

    name: str = "Lewis"
    irrelevant_damage_tags: ClassVar[set[DamageTag]] = set(
        [
            DamageTag.CORROSION,
            DamageTag.FREEZE,
            DamageTag.HYDRO,
            DamageTag.ELECTRIC,
            DamageTag.MELEE,
            DamageTag.LIGHT_AMMO,
            DamageTag.MEDIUM_AMMO,
            DamageTag.SHOTGUN_AMMO,
            DamageTag.SUPPORT_ACTION,
            DamageTag.INTERCEPTION,
            DamageTag.COUNTERATTACK,
        ]
    )

    playtime: CombatAction = Field(default_factory=Playtime)
    bad_guy_cleanup: CombatAction = Field(default_factory=BadGuyCleanup)
    surprising_funball: CombatAction = Field(default_factory=SurprisingFunball)
    toy_carnival: CombatAction = Field(default_factory=ToyCarnival)
    volley_fire: CombatAction = Field(default_factory=VolleyFire)

    def set_to_v0(self) -> None:
        """Sets Fortification Level to Segment00."""
        self.playtime: CombatAction = Playtime()
        self.bad_guy_cleanup: CombatAction = BadGuyCleanup()
        self.surprising_funball: CombatAction = SurprisingFunball()
        self.toy_carnival: CombatAction = ToyCarnival()
        self.volley_fire: CombatAction = VolleyFire()

    def set_to_v1(self) -> None:
        """Sets Fortification Level to Segment01."""
        self.set_to_v0()

        self.volley_fire: CombatAction = VolleyFireV1()

    def set_to_v2(self) -> None:
        """Sets Fortification Level to Segment02."""
        self.set_to_v1()

        self.toy_carnival: CombatAction = ToyCarnivalV2()

    def set_to_v3(self) -> None:
        """Sets Fortification Level to Segment03."""
        self.set_to_v2()

        self.surprising_funball: CombatAction = SurprisingFunballV3()
        self.volley_fire: CombatAction = VolleyFireV3()

    def set_to_v4(self) -> None:
        """Sets Fortification Level to Segment04."""
        self.set_to_v3()

        self.bad_guy_cleanup: CombatAction = BadGuyCleanupV4()

    def set_to_v5(self) -> None:
        """Sets Fortification Level to Segment05."""
        self.set_to_v4()

        self.toy_carnival: CombatAction = ToyCarnivalV5()

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
                self.set_to_v4()
            case FortificationLevel.SEGMENT05:
                self.set_to_v5()
            case FortificationLevel.SEGMENT06:
                self.set_to_v5()

    def get_sample_data(self) -> list[DamageInstance]:
        """Returns a sample single target rotation."""
        rotation_data: list[DamageInstance] = [
            # Turn 1
            self.surprising_funball.execute(),
            self.volley_fire.execute(tin_soldier_rank=2, has_tin_soldiers_order=True),
            self.volley_fire.execute(tin_soldier_rank=2, has_tin_soldiers_order=True),
            self.volley_fire.execute(tin_soldier_rank=2, has_tin_soldiers_order=False),
            self.volley_fire.execute(tin_soldier_rank=2, has_tin_soldiers_order=False),
            # Turn 2
            self.volley_fire.execute(tin_soldier_rank=3, has_tin_soldiers_order=False),
            self.volley_fire.execute(tin_soldier_rank=3, has_tin_soldiers_order=False),
            self.volley_fire.execute(tin_soldier_rank=3, has_tin_soldiers_order=False),
            self.volley_fire.execute(tin_soldier_rank=3, has_tin_soldiers_order=False),
            self.volley_fire.execute(tin_soldier_rank=3, has_tin_soldiers_order=False),
            self.toy_carnival.execute(
                cumulative_tin_soldier_ranks=6, highest_rank_tin_soldier=3
            ),
            # Turn 3
            self.surprising_funball.execute(),
            self.volley_fire.execute(tin_soldier_rank=3, has_tin_soldiers_order=True),
            self.volley_fire.execute(tin_soldier_rank=3, has_tin_soldiers_order=True),
            self.volley_fire.execute(tin_soldier_rank=3, has_tin_soldiers_order=False),
            self.volley_fire.execute(tin_soldier_rank=3, has_tin_soldiers_order=False),
            # Turn 4
            self.volley_fire.execute(tin_soldier_rank=3, has_tin_soldiers_order=False),
            self.volley_fire.execute(tin_soldier_rank=3, has_tin_soldiers_order=False),
            self.volley_fire.execute(tin_soldier_rank=3, has_tin_soldiers_order=False),
            self.volley_fire.execute(tin_soldier_rank=3, has_tin_soldiers_order=False),
            self.volley_fire.execute(tin_soldier_rank=3, has_tin_soldiers_order=False),
            self.toy_carnival.execute(
                cumulative_tin_soldier_ranks=6, highest_rank_tin_soldier=3
            ),
            # Turn 5
            self.surprising_funball.execute(),
            self.volley_fire.execute(tin_soldier_rank=3, has_tin_soldiers_order=True),
            self.volley_fire.execute(tin_soldier_rank=3, has_tin_soldiers_order=True),
            self.volley_fire.execute(tin_soldier_rank=3, has_tin_soldiers_order=False),
            self.volley_fire.execute(tin_soldier_rank=3, has_tin_soldiers_order=False),
            # Turn 6
            self.volley_fire.execute(tin_soldier_rank=3, has_tin_soldiers_order=False),
            self.volley_fire.execute(tin_soldier_rank=3, has_tin_soldiers_order=False),
            self.volley_fire.execute(tin_soldier_rank=3, has_tin_soldiers_order=False),
            self.volley_fire.execute(tin_soldier_rank=3, has_tin_soldiers_order=False),
            self.volley_fire.execute(tin_soldier_rank=3, has_tin_soldiers_order=False),
            self.toy_carnival.execute(
                cumulative_tin_soldier_ranks=6, highest_rank_tin_soldier=3
            ),
            # Turn 7
            self.surprising_funball.execute(),
            self.volley_fire.execute(tin_soldier_rank=3, has_tin_soldiers_order=True),
            self.volley_fire.execute(tin_soldier_rank=3, has_tin_soldiers_order=True),
            self.volley_fire.execute(tin_soldier_rank=3, has_tin_soldiers_order=False),
            self.volley_fire.execute(tin_soldier_rank=3, has_tin_soldiers_order=False),
        ]

        return rotation_data
