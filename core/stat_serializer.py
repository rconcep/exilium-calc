"""
Serialization and deserialization of Unit stats with future-proof enum handling.

This module provides functionality to save and load Unit stats (initial_stats,
additive_modifiers, multiplicative_modifiers) to/from JSON files. It is designed
to handle enum expansions gracefully:
- Uses enum NAMES (not values) for serialization, making it resilient to enum value changes
- Skips unknown enum values during deserialization with warnings
- Supports versioning for future migrations
"""

from __future__ import annotations

import json
import logging
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any, Dict, Optional

from pydantic import BaseModel

from .types import (
    DamageTag,
    DamageTagMultipliers,
    FinalStatModifiers,
    SpecialAttribute,
    StatSheet,
    StatType,
    Unit,
)

logger = logging.getLogger(__name__)


class SerializationError(Exception):
    """Raised when serialization/deserialization fails."""

    pass


class UnitStatsSnapshot(BaseModel):
    """Metadata wrapper for saved unit stats."""

    version: str = "1.0"
    timestamp: str
    doll_name: Optional[str] = None
    notes: Optional[str] = None


class StatsSerializer:
    """Handles serialization and deserialization of Unit stats.

    Key design decisions for enum resilience:
    - Enums are serialized using their NAMES, not values
    - Unknown enum values are skipped during deserialization with warnings
    - Future enum additions won't break existing save files
    """

    CURRENT_VERSION = "1.0"

    @staticmethod
    def _enum_to_dict(enum_obj: Enum) -> str:
        """Convert enum to its name for serialization."""
        return enum_obj.name

    @staticmethod
    def _dict_to_enum(enum_class, enum_name: str) -> Optional[Enum]:
        """Convert enum name back to enum instance, returning None if not found."""
        try:
            return enum_class[enum_name]
        except KeyError:
            logger.warning(
                f"Unknown {enum_class.__name__}: '{enum_name}' - skipping. "
                f"This may occur if the application was updated. "
                f"Available values: {[e.name for e in enum_class]}"
            )
            return None

    @staticmethod
    def serialize_damage_tag_multipliers(
        multipliers: DamageTagMultipliers,
    ) -> Dict[str, float]:
        """Serialize DamageTagMultipliers to dict with enum names as keys."""
        return {
            StatsSerializer._enum_to_dict(tag): value
            for tag, value in multipliers.multipliers.items()
        }

    @staticmethod
    def deserialize_damage_tag_multipliers(
        data: Dict[str, float],
    ) -> DamageTagMultipliers:
        """Deserialize DamageTagMultipliers from dict with enum names as keys."""
        multipliers = DamageTagMultipliers()
        for tag_name, value in data.items():
            tag = StatsSerializer._dict_to_enum(DamageTag, tag_name)
            if tag is not None:
                multipliers.set_multiplier(tag, value)
        return multipliers

    @staticmethod
    def serialize_stat_sheet(sheet: StatSheet) -> Dict[str, Any]:
        """Serialize StatSheet to dict."""
        return {
            "basic_attributes": {
                StatsSerializer._enum_to_dict(stat): value
                for stat, value in sheet.basic_attributes.items()
            },
            "special_attributes": {
                StatsSerializer._enum_to_dict(
                    attr
                ): StatsSerializer.serialize_damage_tag_multipliers(multipliers)
                for attr, multipliers in sheet.special_attributes.items()
            },
        }

    @staticmethod
    def deserialize_stat_sheet(data: Dict[str, Any]) -> StatSheet:
        """Deserialize StatSheet from dict, skipping unknown enums gracefully."""
        sheet = StatSheet()
        sheet.basic_attributes = {}
        sheet.special_attributes = {}

        # Deserialize basic attributes
        if "basic_attributes" in data:
            for stat_name, value in data["basic_attributes"].items():
                stat = StatsSerializer._dict_to_enum(StatType, stat_name)
                if stat is not None:
                    sheet.basic_attributes[stat] = value

        # Deserialize special attributes
        if "special_attributes" in data:
            for attr_name, multipliers_data in data["special_attributes"].items():
                attr = StatsSerializer._dict_to_enum(SpecialAttribute, attr_name)
                if attr is not None:
                    sheet.special_attributes[attr] = (
                        StatsSerializer.deserialize_damage_tag_multipliers(
                            multipliers_data
                        )
                    )

        # Fill in missing values with defaults
        for stat in StatType:
            if stat not in sheet.basic_attributes:
                sheet.basic_attributes[stat] = 0

        for attr in SpecialAttribute:
            if attr not in sheet.special_attributes:
                sheet.special_attributes[attr] = DamageTagMultipliers()
                sheet.special_attributes[attr].multipliers = {
                    tag: 0 for tag in DamageTag
                }

        return sheet

    @staticmethod
    def serialize_unit_stats(
        unit: Unit,
        doll_name: Optional[str] = None,
        notes: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Serialize Unit stats to a dictionary.

        Args:
            unit: The Unit to serialize
            doll_name: Optional name of the doll for reference
            notes: Optional notes about the configuration

        Returns:
            Dictionary with version, timestamp, and serialized stats
        """
        return {
            "metadata": {
                "version": StatsSerializer.CURRENT_VERSION,
                "timestamp": datetime.now().isoformat(),
                "doll_name": doll_name,
                "notes": notes,
            },
            "initial_stats": StatsSerializer.serialize_stat_sheet(unit.initial_stats),
            "additive_modifiers": StatsSerializer.serialize_stat_sheet(
                unit.additive_modifiers
            ),
            "multiplicative_modifiers": StatsSerializer.serialize_stat_sheet(
                unit.multiplicative_modifiers
            ),
        }

    @staticmethod
    def deserialize_unit_stats(data: Dict[str, Any]) -> tuple[Unit, Dict[str, Any]]:
        """Deserialize Unit stats from a dictionary.

        Gracefully handles unknown enums by skipping them with warnings.

        Args:
            data: Dictionary with serialized unit stats (from serialize_unit_stats)

        Returns:
            Tuple of (Unit, metadata_dict) where metadata contains version, timestamp, etc.

        Raises:
            SerializationError: If data format is invalid
        """
        try:
            metadata = data.get("metadata", {})
            version = metadata.get("version", "1.0")

            # Version validation
            if version != StatsSerializer.CURRENT_VERSION:
                logger.warning(
                    f"Loading stats from version {version}, current version is {StatsSerializer.CURRENT_VERSION}. "
                    f"Some data may be incompatible."
                )

            unit = Unit()
            unit.initial_stats = StatsSerializer.deserialize_stat_sheet(
                data.get("initial_stats", {})
            )
            unit.additive_modifiers = StatsSerializer.deserialize_stat_sheet(
                data.get("additive_modifiers", {})
            )
            unit.multiplicative_modifiers = StatsSerializer.deserialize_stat_sheet(
                data.get("multiplicative_modifiers", {})
            )

            return unit, metadata

        except Exception as e:
            raise SerializationError(
                f"Failed to deserialize unit stats: {str(e)}"
            ) from e

    @staticmethod
    def save_to_file(
        unit: Unit,
        filepath: str | Path,
        doll_name: Optional[str] = None,
        notes: Optional[str] = None,
    ) -> None:
        """Save Unit stats to a JSON file.

        Args:
            unit: The Unit to save
            filepath: Path where the JSON file will be saved
            doll_name: Optional name of the doll for reference
            notes: Optional notes about the configuration

        Raises:
            SerializationError: If save operation fails
        """
        try:
            filepath = Path(filepath)
            filepath.parent.mkdir(parents=True, exist_ok=True)

            data = StatsSerializer.serialize_unit_stats(unit, doll_name, notes)

            with open(filepath, "w") as f:
                json.dump(data, f, indent=2)

            logger.info(f"Saved unit stats to {filepath}")

        except Exception as e:
            raise SerializationError(
                f"Failed to save stats to {filepath}: {str(e)}"
            ) from e

    @staticmethod
    def load_from_file(filepath: str | Path) -> tuple[Unit, Dict[str, Any]]:
        """Load Unit stats from a JSON file.

        Args:
            filepath: Path to the JSON file

        Returns:
            Tuple of (Unit, metadata_dict) where metadata contains version, timestamp, etc.

        Raises:
            SerializationError: If load operation fails
        """
        try:
            filepath = Path(filepath)

            if not filepath.exists():
                raise FileNotFoundError(f"Stats file not found: {filepath}")

            with open(filepath, "r") as f:
                data = json.load(f)

            unit, metadata = StatsSerializer.deserialize_unit_stats(data)
            logger.info(f"Loaded unit stats from {filepath}")
            return unit, metadata

        except FileNotFoundError:
            raise
        except json.JSONDecodeError as e:
            raise SerializationError(f"Invalid JSON in {filepath}: {str(e)}") from e
        except Exception as e:
            raise SerializationError(
                f"Failed to load stats from {filepath}: {str(e)}"
            ) from e

    @staticmethod
    def save_to_string(
        unit: Unit,
        doll_name: Optional[str] = None,
        notes: Optional[str] = None,
    ) -> str:
        """Serialize Unit stats to a JSON string.

        Args:
            unit: The Unit to serialize
            doll_name: Optional name of the doll for reference
            notes: Optional notes about the configuration

        Returns:
            JSON string representation of the unit stats
        """
        data = StatsSerializer.serialize_unit_stats(unit, doll_name, notes)
        return json.dumps(data, indent=2)

    @staticmethod
    def load_from_string(json_string: str) -> tuple[Unit, Dict[str, Any]]:
        """Deserialize Unit stats from a JSON string.

        Args:
            json_string: JSON string containing unit stats

        Returns:
            Tuple of (Unit, metadata_dict)

        Raises:
            SerializationError: If deserialization fails
        """
        try:
            data = json.loads(json_string)
            return StatsSerializer.deserialize_unit_stats(data)
        except json.JSONDecodeError as e:
            raise SerializationError(f"Invalid JSON: {str(e)}") from e
