"""
Unit tests for stat serialization feature.

Tests cover:
- Basic serialization/deserialization round-trip
- Enum name-based serialization for future proofing
- Graceful handling of unknown enum values
- File I/O operations
- Metadata handling
"""

import json
import tempfile
from pathlib import Path
from unittest import TestCase

from core.types import (
    DamageTag,
    DamageTagMultipliers,
    SpecialAttribute,
    StatSheet,
    StatType,
    Unit,
)
from core.stat_serializer import StatsSerializer, SerializationError


class TestStatsSerializer(TestCase):
    """Test serialization and deserialization of Unit stats."""

    def setUp(self):
        """Create a test unit with sample stats."""
        self.unit = Unit()

        # Set initial stats
        self.unit.initial_stats.basic_attributes[StatType.ATTACK] = 100.0
        self.unit.initial_stats.basic_attributes[StatType.DEFENSE] = 50.0
        self.unit.initial_stats.basic_attributes[StatType.HEALTH] = 200.0
        self.unit.initial_stats.special_attributes[
            SpecialAttribute.DAMAGE_BOOST
        ].set_multiplier(DamageTag.PHYSICAL, 10.0)
        self.unit.initial_stats.special_attributes[
            SpecialAttribute.DAMAGE_BOOST
        ].set_multiplier(DamageTag.ALL, 5.0)

        # Set additive modifiers
        self.unit.additive_modifiers.basic_attributes[StatType.ATTACK] = 20.0
        self.unit.additive_modifiers.basic_attributes[StatType.CRIT_RATE] = 15.0
        self.unit.additive_modifiers.special_attributes[
            SpecialAttribute.CRITICAL_DAMAGE
        ].set_multiplier(DamageTag.MELEE, 25.0)

        # Set multiplicative modifiers
        self.unit.multiplicative_modifiers.basic_attributes[StatType.ATTACK] = 10.0
        self.unit.multiplicative_modifiers.special_attributes[
            SpecialAttribute.DAMAGE_BOOST
        ].set_multiplier(DamageTag.PHYSICAL, 5.0)

    def test_serialize_basic_attributes(self):
        """Test serialization of basic attributes preserves values."""
        serialized = StatsSerializer.serialize_unit_stats(self.unit)

        self.assertEqual(
            serialized["initial_stats"]["basic_attributes"][StatType.ATTACK.name],
            100.0,
        )
        self.assertEqual(
            serialized["initial_stats"]["basic_attributes"][StatType.DEFENSE.name],
            50.0,
        )

    def test_serialize_special_attributes(self):
        """Test serialization of special attributes with damage tags."""
        serialized = StatsSerializer.serialize_unit_stats(self.unit)

        damage_boost = serialized["initial_stats"]["special_attributes"][
            SpecialAttribute.DAMAGE_BOOST.name
        ]
        self.assertEqual(damage_boost[DamageTag.PHYSICAL.name], 10.0)
        self.assertEqual(damage_boost[DamageTag.ALL.name], 5.0)

    def test_round_trip_serialization(self):
        """Test that serialization and deserialization preserves data."""
        # Serialize
        data = StatsSerializer.serialize_unit_stats(
            self.unit, doll_name="TestDoll", notes="Test notes"
        )

        # Deserialize
        loaded_unit, metadata = StatsSerializer.deserialize_unit_stats(data)

        # Verify basic attributes
        self.assertEqual(
            loaded_unit.initial_stats.basic_attributes[StatType.ATTACK],
            self.unit.initial_stats.basic_attributes[StatType.ATTACK],
        )
        self.assertEqual(
            loaded_unit.additive_modifiers.basic_attributes[StatType.ATTACK],
            self.unit.additive_modifiers.basic_attributes[StatType.ATTACK],
        )

        # Verify special attributes
        self.assertEqual(
            loaded_unit.initial_stats.special_attributes[
                SpecialAttribute.DAMAGE_BOOST
            ].get_multiplier(DamageTag.PHYSICAL),
            self.unit.initial_stats.special_attributes[
                SpecialAttribute.DAMAGE_BOOST
            ].get_multiplier(DamageTag.PHYSICAL),
        )

        # Verify metadata
        self.assertEqual(metadata["doll_name"], "TestDoll")
        self.assertEqual(metadata["notes"], "Test notes")
        self.assertEqual(metadata["version"], "1.0")

    def test_enum_names_used_in_serialization(self):
        """Test that enum NAMES (not values) are used in serialization."""
        data = StatsSerializer.serialize_unit_stats(self.unit)

        # Check that enum names appear in the JSON
        basic_attrs = data["initial_stats"]["basic_attributes"]
        self.assertIn(StatType.ATTACK.name, basic_attrs)
        self.assertIn(StatType.DEFENSE.name, basic_attrs)

        # Verify enum values don't appear
        self.assertNotIn(StatType.ATTACK.value, basic_attrs)
        self.assertNotIn(StatType.DEFENSE.value, basic_attrs)

    def test_unknown_enum_gracefully_skipped(self):
        """Test that unknown enum values are skipped with warnings.

        This simulates future enum expansions where new values might appear
        in old save files.
        """
        data = StatsSerializer.serialize_unit_stats(self.unit)

        # Inject an unknown enum name
        data["initial_stats"]["basic_attributes"]["FUTURE_UNKNOWN_STAT"] = 99.0

        # This should not raise an error
        loaded_unit, _ = StatsSerializer.deserialize_unit_stats(data)

        # The unknown value should be skipped, but other values preserved
        self.assertEqual(
            loaded_unit.initial_stats.basic_attributes[StatType.ATTACK], 100.0
        )

    def test_unknown_special_attribute_gracefully_skipped(self):
        """Unknown special attribute keys should be ignored, not crash loading.

        This mirrors real uploaded JSON that may contain newer attributes,
        such as INCREASE_DAMAGE_TAKEN, while the running app has older enums.
        """
        data = StatsSerializer.serialize_unit_stats(self.unit)

        data["initial_stats"]["special_attributes"]["INCREASE_DAMAGE_TAKEN"] = {
            DamageTag.ALL.name: 12.3
        }

        loaded_unit, _ = StatsSerializer.deserialize_unit_stats(data)

        # Existing known values must still load correctly.
        self.assertEqual(
            loaded_unit.initial_stats.special_attributes[
                SpecialAttribute.DAMAGE_BOOST
            ].get_multiplier(DamageTag.PHYSICAL),
            self.unit.initial_stats.special_attributes[
                SpecialAttribute.DAMAGE_BOOST
            ].get_multiplier(DamageTag.PHYSICAL),
        )

    def test_file_save_and_load(self):
        """Test saving and loading from files."""
        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = Path(tmpdir) / "unit_stats.json"

            # Save
            StatsSerializer.save_to_file(
                self.unit, filepath, doll_name="TestDoll", notes="Saved from test"
            )

            # Verify file exists and is valid JSON
            self.assertTrue(filepath.exists())
            with open(filepath) as f:
                data = json.load(f)
            self.assertIn("metadata", data)
            self.assertIn("initial_stats", data)

            # Load
            loaded_unit, metadata = StatsSerializer.load_from_file(filepath)

            # Verify
            self.assertEqual(
                loaded_unit.initial_stats.basic_attributes[StatType.ATTACK],
                self.unit.initial_stats.basic_attributes[StatType.ATTACK],
            )
            self.assertEqual(metadata["doll_name"], "TestDoll")

    def test_string_serialization(self):
        """Test serialization to and from strings."""
        # Serialize to string
        json_string = StatsSerializer.save_to_string(self.unit, doll_name="TestDoll")

        # Verify it's valid JSON
        data = json.loads(json_string)
        self.assertIn("metadata", data)

        # Deserialize from string
        loaded_unit, metadata = StatsSerializer.load_from_string(json_string)

        # Verify
        self.assertEqual(
            loaded_unit.initial_stats.basic_attributes[StatType.ATTACK],
            self.unit.initial_stats.basic_attributes[StatType.ATTACK],
        )
        self.assertEqual(metadata["doll_name"], "TestDoll")

    def test_invalid_json_handling(self):
        """Test that invalid JSON raises appropriate error."""
        with self.assertRaises(SerializationError):
            StatsSerializer.load_from_string("not valid json")

    def test_missing_file_handling(self):
        """Test that missing file raises appropriate error."""
        with self.assertRaises(FileNotFoundError):
            StatsSerializer.load_from_file(Path("/nonexistent/path/file.json"))

    def test_all_stat_types_preserved(self):
        """Test that all StatType values are preserved through serialization."""
        # Set all stat types to unique values
        for stat in StatType:
            self.unit.initial_stats.basic_attributes[stat] = float(hash(stat) % 100)

        # Serialize and deserialize
        data = StatsSerializer.serialize_unit_stats(self.unit)
        loaded_unit, _ = StatsSerializer.deserialize_unit_stats(data)

        # Verify all stats are preserved
        for stat in StatType:
            self.assertEqual(
                loaded_unit.initial_stats.basic_attributes[stat],
                self.unit.initial_stats.basic_attributes[stat],
            )

    def test_all_damage_tags_preserved(self):
        """Test that all DamageTag values are preserved through serialization."""
        damage_boost = self.unit.initial_stats.special_attributes[
            SpecialAttribute.DAMAGE_BOOST
        ]

        # Set all damage tags to unique values
        for tag in DamageTag:
            damage_boost.set_multiplier(tag, float(hash(tag) % 100))

        # Serialize and deserialize
        data = StatsSerializer.serialize_unit_stats(self.unit)
        loaded_unit, _ = StatsSerializer.deserialize_unit_stats(data)

        # Verify all tags are preserved
        loaded_damage_boost = loaded_unit.initial_stats.special_attributes[
            SpecialAttribute.DAMAGE_BOOST
        ]
        for tag in DamageTag:
            self.assertEqual(
                loaded_damage_boost.get_multiplier(tag),
                damage_boost.get_multiplier(tag),
            )

    def test_metadata_preserved(self):
        """Test that all metadata is preserved."""
        doll_name = "Leva"
        notes = "High attack configuration with physical boost"

        data = StatsSerializer.serialize_unit_stats(
            self.unit, doll_name=doll_name, notes=notes
        )
        loaded_unit, metadata = StatsSerializer.deserialize_unit_stats(data)

        self.assertEqual(metadata["doll_name"], doll_name)
        self.assertEqual(metadata["notes"], notes)
        self.assertIn("timestamp", metadata)
        self.assertEqual(metadata["version"], "1.0")

    def test_empty_unit_serialization(self):
        """Test serialization of an empty Unit with default values."""
        empty_unit = Unit()

        data = StatsSerializer.serialize_unit_stats(empty_unit)
        loaded_unit, _ = StatsSerializer.deserialize_unit_stats(data)

        # All basic attributes should be 0
        for stat in StatType:
            self.assertEqual(loaded_unit.initial_stats.basic_attributes[stat], 0)


if __name__ == "__main__":
    import unittest

    unittest.main()
