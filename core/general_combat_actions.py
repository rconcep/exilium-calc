import inspect
from typing import Any, Callable, override, ClassVar, final
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
from core.buffs import Buff, MAX_TILE_ASCENSION_LEVEL
from core.combat import DamageInstance, FixedDamageInstance, CombatAction


def _coerce_damage_tag(element: DamageTag | str) -> DamageTag:
    """Normalizes a user-provided element value into a DamageTag."""
    if isinstance(element, DamageTag):
        return element
    return DamageTag(element)


def get_elemental_tile_actions_for_element(
    element: DamageTag | str,
) -> dict[str, Callable[..., DamageInstance]]:
    """Returns the elemental tile action constructors associated with an element.

    This includes both standalone elemental tiles and the relevant polyphase tiles that
    share the requested element tag, such as Burn / Freeze / Corrosion / Hydro / Electric.
    """
    normalized_element: DamageTag = _coerce_damage_tag(element)

    elemental_actions: dict[DamageTag, dict[str, Callable[..., DamageInstance]]] = {
        DamageTag.BURN: {
            "Scalding Vapors Tile (Burn)": ScaldingVaporsTileBurn().execute,
            "Venomfire Tile (Turn End)": VenomfireTileTurnEnd().execute,
            "Venomfire Tile (Triggered)": VenomfireTileTriggered().execute,
            "Smoldering Suspire Tile (Burn)": SmolderingSuspireTileBurn().execute,
        },
        DamageTag.FREEZE: {
            "Smoldering Suspire Tile (Freeze)": SmolderingSuspireTileFreeze().execute,
        },
        DamageTag.CORROSION: {
            "Toxic Mist Tile": ToxicMistTile().execute,
            "Venomfire Tile (Turn End)": VenomfireTileTurnEnd().execute,
            "Venomfire Tile (Triggered)": VenomfireTileTriggered().execute,
            "Toxic Quagmire Tile": ToxicQuagmireTile().execute,
            "Radiant Energy Tile (Turn End)": RadiantEnergyTileTurnEnd().execute,
            "Radiant Energy Tile (Triggered)": RadiantEnergyTileTriggered().execute,
        },
        DamageTag.HYDRO: {
            "Scalding Vapors Tile (Hydro)": ScaldingVaporsTileHydro().execute,
            "Toxic Quagmire Tile": ToxicQuagmireTile().execute,
            "Thunderpool Tile": ThunderpoolTile().execute,
            "Blitz Link": BlitzLink().execute,
        },
        DamageTag.ELECTRIC: {
            "Voltage Tile": VoltageTile().execute,
            "Thunderpool Tile": ThunderpoolTile().execute,
            "Radiant Energy Tile (Triggered)": RadiantEnergyTileTriggered().execute,
            "Blitz Link": BlitzLink().execute,
        },
    }

    if normalized_element not in elemental_actions:
        raise ValueError(f"Unsupported elemental tile tag: {normalized_element}")

    return dict(elemental_actions[normalized_element])


def get_elemental_tile_option_config(
    element: DamageTag | str,
) -> dict[str, dict[str, Any]]:
    """Builds a standard option_config payload for all tile actions tied to an element."""
    config: dict[str, dict[str, Any]] = {}

    for action_name, action_fn in get_elemental_tile_actions_for_element(
        element
    ).items():
        params = inspect.signature(action_fn).parameters
        fields: list[dict[str, Any]] = []

        if "tile_ascension_level" in params:
            fields.append(
                {
                    "key": "tile_ascension_level",
                    "type": "select",
                    "label": "Tile Ascension Level",
                    "default": 1,
                    "options": [n for n in range(0, 4)],
                }
            )

        if "damage_taken_is_electric_or_hydro" in params:
            fields.append(
                {
                    "key": "damage_taken_is_electric_or_hydro",
                    "type": "checkbox",
                    "label": "Damage Taken is Electric/Hydro",
                    "default": False,
                }
            )

        if "is_large_target" in params:
            fields.append(
                {
                    "key": "is_large_target",
                    "type": "checkbox",
                    "label": "Large Target",
                    "default": False,
                }
            )

        if "number_of_bounces" in params:
            fields.append(
                {
                    "key": "number_of_bounces",
                    "type": "number",
                    "label": "Bounces",
                    "default": 0,
                }
            )

        config[action_name] = {
            "fields": fields,
            "function": action_fn,
        }

    return config


# Base elemental tiles
class ToxicMistTile(CombatAction):
    """Base Corrosion tile - the fixed damage dealt to units remaining in the tile at the end of their action.
    Includes the higher ascension level tiles that are named slightly differently.
    """

    @override
    def execute(self, tile_ascension_level: int) -> DamageInstance:
        label: str = f"Toxic Mist Tile (Level {tile_ascension_level})"
        base_potency: int = 50

        match tile_ascension_level:
            case 1:
                base_potency = 50
            case 2:
                base_potency = 150
            case 3:
                base_potency = 300
            case _:
                raise ValueError(
                    f"Invalid tile ascension level: {tile_ascension_level}"
                )

        return FixedDamageInstance(
            label=label,
            base_potency=base_potency,
            group_name="Toxic Mist Tile",
        )


class VoltageTile(CombatAction):
    """Base Electric tile - the fixed damage dealt to unit when they take AoE damage while on the tile.
    Includes the higher ascension level tiles that are named slightly differently.
    """

    @override
    def execute(
        self,
        tile_ascension_level: int,
        damage_taken_is_electric_or_hydro: bool,
        is_large_target: bool,
    ) -> DamageInstance:
        label: str = f"Voltage Tile (Level {tile_ascension_level})"
        base_potency: int = 30

        if damage_taken_is_electric_or_hydro:
            base_potency = 60

        # Deals 2x damage to large targets
        if is_large_target:
            base_potency = int(base_potency * 2)

        return FixedDamageInstance(
            label=label,
            base_potency=base_potency,
            group_name="Voltage Tile",
        )


# Polyphase Fusion tiles
class ScaldingVaporsTileBase(CombatAction):
    """Polyphase tile (Burn+Hydro) - the damage dealt to units in the area when the tile is generated.
    The tile activation applies both Burn and Hydro damage - this base class should not be used;
    instead, use one instance each of the ScaldingVaporsTileBurn and ScaldingVaporsTileHydro classes,
    which will apply the appropriate damage tags.
    """

    @override
    def execute(self, tile_ascension_level: int) -> DamageInstance:
        label: str = f"Scalding Vapors Tile (Level {tile_ascension_level})"
        base_potency: int = 10

        match tile_ascension_level:
            case 1:
                base_potency = 10
            case 2:
                base_potency = 15
            case 3:
                base_potency = 20
            case _:
                raise ValueError(
                    f"Invalid tile ascension level: {tile_ascension_level}"
                )

        tags: set[DamageTag] = {
            DamageTag.PHASE,
        }

        return DamageInstance(
            label=label,
            base_potency=base_potency,
            tags=tags,
            group_name="Scalding Vapors Tile",
        )


class ScaldingVaporsTileBurn(ScaldingVaporsTileBase):
    """Polyphase tile (Burn+Hydro) - the Burn damage dealt to units in the area when the tile is generated."""

    @final
    def execute(self, tile_ascension_level: int) -> DamageInstance:
        damage_instance: DamageInstance = super().execute(tile_ascension_level)
        damage_instance.tags.add(DamageTag.BURN)
        return damage_instance


class ScaldingVaporsTileHydro(ScaldingVaporsTileBase):
    """Polyphase tile (Burn+Hydro) - the Hydro damage dealt to units in the area when the tile is generated."""

    @final
    def execute(self, tile_ascension_level: int) -> DamageInstance:
        damage_instance: DamageInstance = super().execute(tile_ascension_level)
        damage_instance.tags.add(DamageTag.HYDRO)
        return damage_instance


class VenomfireTileTurnEnd(CombatAction):
    """Polyphase tile (Burn+Corrosion) - the fixed damage dealt to units that remain in the area at the end of their
    turn.
    This is distinct from the fixed damage dealt when units take Burn or Corrosion damage while in the area.
    """

    @override
    def execute(self, tile_ascension_level: int) -> DamageInstance:
        label: str = f"Venomfire Tile (Turn End) (Level {tile_ascension_level})"
        base_potency: int = 50

        match tile_ascension_level:
            case 1:
                base_potency = 50
            case 2:
                base_potency = 150
            case 3:
                base_potency = 300
            case _:
                raise ValueError(
                    f"Invalid tile ascension level: {tile_ascension_level}"
                )

        return FixedDamageInstance(
            label=label,
            base_potency=base_potency,
            group_name="Venomfire Tile",
        )


class VenomfireTileTriggered(CombatAction):
    """Polyphase tile (Burn+Corrosion) - the fixed damage dealt to units that take Burn or Corrosion damage while in the area.
    This is distinct from the fixed damage dealt when units remain in the area at the end of their turn.
    """

    @override
    def execute(self, tile_ascension_level: int) -> DamageInstance:
        label: str = f"Venomfire Tile (Triggered) (Level {tile_ascension_level})"
        base_potency: int = 10

        match tile_ascension_level:
            case 1:
                base_potency = 10
            case 2:
                base_potency = 25
            case 3:
                base_potency = 25
            case _:
                raise ValueError(
                    f"Invalid tile ascension level: {tile_ascension_level}"
                )

        return FixedDamageInstance(
            label=label,
            base_potency=base_potency,
            group_name="Venomfire Tile",
        )


class SmolderingSuspireTileBase(CombatAction):
    """Polyphase tile (Burn+Freeze) - the damage dealt to units in the area when the tile is generated.
    The tile activation applies both Burn and Freeze damage - this base class should not be used;
    instead, use one instance each of the SmolderingSuspireTileBurn and SmolderingSuspireTileFreeze classes,
    which will apply the appropriate damage tags.
    """

    @override
    def execute(self, tile_ascension_level: int) -> DamageInstance:
        label: str = f"Smoldering Suspire Tile (Level {tile_ascension_level})"
        base_potency: int = 50

        match tile_ascension_level:
            case 1:
                base_potency = 50
            case 2:
                base_potency = 75
            case 3:
                base_potency = 100
            case _:
                raise ValueError(
                    f"Invalid tile ascension level: {tile_ascension_level}"
                )

        tags: set[DamageTag] = {
            DamageTag.PHASE,
        }

        return DamageInstance(
            label=label,
            base_potency=base_potency,
            tags=tags,
            group_name="Smoldering Suspire Tile",
        )


class SmolderingSuspireTileBurn(SmolderingSuspireTileBase):
    """Polyphase tile (Burn+Freeze) - the Burn damage dealt to units in the area when the tile is generated."""

    @final
    def execute(self, tile_ascension_level: int) -> DamageInstance:
        damage_instance: DamageInstance = super().execute(tile_ascension_level)
        damage_instance.tags.add(DamageTag.BURN)
        return damage_instance


class SmolderingSuspireTileFreeze(SmolderingSuspireTileBase):
    """Polyphase tile (Burn+Freeze) - the Freeze damage dealt to units in the area when the tile is generated."""

    @final
    def execute(self, tile_ascension_level: int) -> DamageInstance:
        damage_instance: DamageInstance = super().execute(tile_ascension_level)
        damage_instance.tags.add(DamageTag.FREEZE)
        return damage_instance


class ToxicQuagmireTile(CombatAction):
    """Polyphase tile (Corrosion+Hydro) - the fixed damage dealt to units that remain in the area at the end of their
    turn.
    """

    @override
    def execute(self, tile_ascension_level: int) -> DamageInstance:
        label: str = f"Toxic Quagmire Tile (Level {tile_ascension_level})"
        base_potency: int = 50

        match tile_ascension_level:
            case 1:
                base_potency = 50
            case 2:
                base_potency = 150
            case 3:
                base_potency = 300
            case _:
                raise ValueError(
                    f"Invalid tile ascension level: {tile_ascension_level}"
                )

        return FixedDamageInstance(
            label=label,
            base_potency=base_potency,
            group_name="Toxic Quagmire Tile",
        )


class ThunderpoolTile(CombatAction):
    """Polyphase tile (Electric+Hydro) - the fixed damage dealt to unit when they take AoE damage while on the tile.
    This is distinct from Blitz Link that is performed when units end their turn while on the tile.
    """

    @override
    def execute(
        self,
        tile_ascension_level: int,
        damage_taken_is_electric_or_hydro: bool,
        is_large_target: bool,
    ) -> DamageInstance:
        label: str = f"Thunderpool Tile (Level {tile_ascension_level})"
        base_potency: int = 30

        if damage_taken_is_electric_or_hydro:
            base_potency = 60

        # Deals 2x damage to large targets
        if is_large_target:
            base_potency = int(base_potency * 2)

        return FixedDamageInstance(
            label=label,
            base_potency=base_potency,
            group_name="Thunderpool Tile",
        )


class BlitzLink(CombatAction):
    """Action performed when units end their turn while on a Thunderpool tile."""

    @override
    def execute(
        self, tile_ascension_level: int, number_of_bounces: int
    ) -> DamageInstance:
        label: str = f"Blitz Link (Level {tile_ascension_level})"
        tags: set[DamageTag] = {
            DamageTag.PHASE,
            DamageTag.ELECTRIC,
        }
        base_potency: int = 30
        max_bounces: int = 2
        potency_per_bounce: int = 5

        match tile_ascension_level:
            case 1:
                base_potency = 30
                max_bounces = 2
            case 2:
                base_potency = 40
                max_bounces = 3
            case 3:
                base_potency = 50
                max_bounces = 4
            case _:
                raise ValueError(
                    f"Invalid tile ascension level: {tile_ascension_level}"
                )

        base_potency += min(max(0, number_of_bounces), max_bounces) * potency_per_bounce

        return DamageInstance(
            label=label,
            base_potency=base_potency,
            tags=tags,
            group_name="Blitz Link",
        )


class RadiantEnergyTileTurnEnd(CombatAction):
    """Polyphase tile (Electric+Corrosion) - the fixed damage dealt to units that remain in the area at the end of their
    turn.
    This is distinct from the fixed damage dealt when units take Electric or Hydro damage while in the area.
    """

    @override
    def execute(self, tile_ascension_level: int) -> DamageInstance:
        label: str = f"Radiant Energy Tile (Level {tile_ascension_level})"
        base_potency: int = 50

        match tile_ascension_level:
            case 1:
                base_potency = 50
            case 2:
                base_potency = 150
            case 3:
                base_potency = 300
            case _:
                raise ValueError(
                    f"Invalid tile ascension level: {tile_ascension_level}"
                )

        return FixedDamageInstance(
            label=label,
            base_potency=base_potency,
            group_name="Radiant Energy Tile",
        )


class RadiantEnergyTileTriggered(CombatAction):
    """Polyphase tile (Electric+Corrosion) - the fixed damage dealt to unit when they take AoE damage while on the tile."""

    @override
    def execute(
        self,
        tile_ascension_level: int,
        damage_taken_is_electric_or_hydro: bool,
        is_large_target: bool,
    ) -> DamageInstance:
        label: str = f"Radiant Energy Tile (Level {tile_ascension_level})"
        base_potency: int = 30

        if damage_taken_is_electric_or_hydro:
            base_potency = 60

        # Deals 2x damage to large targets
        if is_large_target:
            base_potency = int(base_potency * 2)

        return FixedDamageInstance(
            label=label,
            base_potency=base_potency,
            group_name="Radiant Energy Tile",
        )
