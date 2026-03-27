"""Core module for Exilium Calc.

Public API:
- types: Type definitions (Unit, StatType, DamageTag, etc.)
- stat_serializer: Unit stats serialization/deserialization
- buffs: Buff system
- combat: Combat mechanics
"""

from .stat_serializer import StatsSerializer, SerializationError
from .types import (
    DamageTag,
    DamageTagMultipliers,
    DefenseIgnoreMultipliers,
    FinalStatModifiers,
    FortificationLevel,
    IncreasedCriticalDamageMultipliers,
    IncreasedDamageMultipliers,
    ModifierType,
    SpecialAttribute,
    StatSheet,
    StatType,
    Unit,
)

__all__ = [
    # Serialization
    "StatsSerializer",
    "SerializationError",
    # Types
    "Unit",
    "StatSheet",
    "FinalStatModifiers",
    "StatType",
    "SpecialAttribute",
    "DamageTag",
    "DamageTagMultipliers",
    "IncreasedDamageMultipliers",
    "IncreasedCriticalDamageMultipliers",
    "DefenseIgnoreMultipliers",
    "ModifierType",
    "FortificationLevel",
]
