from nicegui import ui

from gui.templates.doll_calculator_page import DollCalculatorPage, ModelAssumption
from gui.templates.rotation_planner import RotationPlanner
from typing import Any, cast, override
from core.types import (
    FortificationLevel,
    StatType,
    SpecialAttribute,
    DamageTag,
)
from core.dolls import sextans


_t1: list[dict[str, Any]] = [
    # Passive: Start with 5 stacks of Coagulation.
    {"name": "Midnight Vesper", "stacks_of_coagulation": 5},
    {"name": "Lacerating Wound", "original_damage_instance_potency": 120 + 5 * 10},
    {"name": "Death Knell", "stacks_of_coagulation": 5},
    # Death Knell: Sextans gains 1 stack of Coagulation. For each Level of the target (Normal, Elite, Boss), gain 1 additional stack of Coagulation.
    # Assuming target is a Boss, total Coagulation stacks is 5 (initial) + 1 (Death Knell) + 3 (Boss) = 9 stacks.
    {"name": "Lacerating Wound", "original_damage_instance_potency": 120 + 5 * 10},
    # Target now has Blood Kiss from Midnight Vesper, so Death Knell will trigger Blood Kiss.
    {"name": "Blood Kiss", "multiplier_of_death_knell": 120 + 5 * 10},
    {"name": "Lacerating Wound", "original_damage_instance_potency": 120 + 5 * 10},
    # Death Knell: When the skill hits an enemy target, Blood Insignia is triggered. After using the skill, Sextans gains 2 stacks
    # of Coagulation.
    {
        "name": "Blood Insignia",
        "stacks_of_coagulation": 9,
        "previous_triggers_this_round": 0,
    },
    {"name": "Lacerating Wound", "original_damage_instance_potency": 90 + 9 * 4},
    # Blood Insignia triggers when allied units (excluding Sextans) attack with a blade:
    # Assume:
    # 4x from Ullrid
    # 4x from Phaetusa
    {
        "name": "Blood Insignia",
        "stacks_of_coagulation": 11,
        "previous_triggers_this_round": 1,
    },
    {
        "name": "Lacerating Wound",
        "original_damage_instance_potency": 90 + 11 * 4 - 1 * 20,
    },
    {
        "name": "Blood Insignia",
        "stacks_of_coagulation": 11,
        "previous_triggers_this_round": 2,
    },
    {
        "name": "Lacerating Wound",
        "original_damage_instance_potency": 90 + 11 * 4 - 2 * 20,
    },
    {
        "name": "Blood Insignia",
        "stacks_of_coagulation": 11,
        "previous_triggers_this_round": 3,
    },
    {
        "name": "Lacerating Wound",
        "original_damage_instance_potency": 90 + 11 * 4 - 3 * 20,
    },
    {
        "name": "Blood Insignia",
        "stacks_of_coagulation": 11,
        "previous_triggers_this_round": 4,
    },
    {
        "name": "Lacerating Wound",
        "original_damage_instance_potency": 90 + 11 * 4 - 4 * 20,
    },
    {
        "name": "Blood Insignia",
        "stacks_of_coagulation": 11,
        "previous_triggers_this_round": 5,
    },
    {
        "name": "Lacerating Wound",
        "original_damage_instance_potency": 90 + 11 * 4 - 5 * 20,
    },
    {
        "name": "Blood Insignia",
        "stacks_of_coagulation": 11,
        "previous_triggers_this_round": 6,
    },
    # Minimum potency of Blood Insignia is 30, so Lacerating Wound potency will be 30 at this point.
    {"name": "Lacerating Wound", "original_damage_instance_potency": 30},
    {
        "name": "Blood Insignia",
        "stacks_of_coagulation": 11,
        "previous_triggers_this_round": 7,
    },
    {"name": "Lacerating Wound", "original_damage_instance_potency": 30},
    {
        "name": "Blood Insignia",
        "stacks_of_coagulation": 11,
        "previous_triggers_this_round": 8,
    },
    {"name": "Lacerating Wound", "original_damage_instance_potency": 30},
]

_t2: list[dict[str, Any]] = [
    {"name": "Sanctuary Lauds", "stacks_of_coagulation": 11},
    {"name": "Lacerating Wound", "original_damage_instance_potency": 90 + 11 * 10},
    {"name": "Death Knell", "stacks_of_coagulation": 11},
    # Death Knell: Sextans gains 1 stack of Coagulation. For each Level of the target (Normal, Elite, Boss), gain 1 additional stack of Coagulation.
    # Assuming target is a Boss, total Coagulation stacks is 11 (initial) + 1 (Death Knell) + 3 (Boss) = 15 stacks.
    {"name": "Lacerating Wound", "original_damage_instance_potency": 90 + 11 * 10},
    # Target now has Blood Kiss from Sanctuary Lauds, so Death Knell will trigger Blood Kiss.
    {"name": "Blood Kiss", "multiplier_of_death_knell": 120 + 11 * 10},
    {"name": "Lacerating Wound", "original_damage_instance_potency": 120 + 11 * 10},
    # Death Knell: When the skill hits an enemy target, Blood Insignia is triggered. After using the skill, Sextans gains 2 stacks
    # of Coagulation.
    {
        "name": "Blood Insignia",
        "stacks_of_coagulation": 15,
        "previous_triggers_this_round": 0,
    },
    {"name": "Lacerating Wound", "original_damage_instance_potency": 90 + 15 * 4},
    # Passive - Requiem: When an enemy unit dies or is in Stability Break,Sextans gains 1 stack of Coagulation.
    # For each Level of the target (Normal, Elite, Boss), gain 1 additional stack of Coagulation.
    # Assume Boss is in Stability Break now, so increment the Coagulation stack count by 4 (1 for the passive trigger and 3 for the Boss level).
    # Total Coagulation stacks is 17 (initial) + 1 (Death Knell) + 3 (Boss) = 21 stacks.
    # Blood Insignia triggers when allied units (excluding Sextans) attack with a blade:
    # Assume:
    # 4x from Ullrid
    # 4x from Phaetusa
    {
        "name": "Blood Insignia",
        "stacks_of_coagulation": 21,
        "previous_triggers_this_round": 1,
    },
    {
        "name": "Lacerating Wound",
        "original_damage_instance_potency": 90 + 21 * 4 - 1 * 20,
    },
    {
        "name": "Blood Insignia",
        "stacks_of_coagulation": 21,
        "previous_triggers_this_round": 2,
    },
    {
        "name": "Lacerating Wound",
        "original_damage_instance_potency": 90 + 21 * 4 - 2 * 20,
    },
    {
        "name": "Blood Insignia",
        "stacks_of_coagulation": 21,
        "previous_triggers_this_round": 3,
    },
    {
        "name": "Lacerating Wound",
        "original_damage_instance_potency": 90 + 21 * 4 - 3 * 20,
    },
    {
        "name": "Blood Insignia",
        "stacks_of_coagulation": 21,
        "previous_triggers_this_round": 4,
    },
    {
        "name": "Lacerating Wound",
        "original_damage_instance_potency": 90 + 21 * 4 - 4 * 20,
    },
    {
        "name": "Blood Insignia",
        "stacks_of_coagulation": 21,
        "previous_triggers_this_round": 5,
    },
    {
        "name": "Lacerating Wound",
        "original_damage_instance_potency": 90 + 21 * 4 - 5 * 20,
    },
    {
        "name": "Blood Insignia",
        "stacks_of_coagulation": 21,
        "previous_triggers_this_round": 6,
    },
    {
        "name": "Lacerating Wound",
        "original_damage_instance_potency": 90 + 21 * 4 - 6 * 20,
    },
    {
        "name": "Blood Insignia",
        "stacks_of_coagulation": 21,
        "previous_triggers_this_round": 7,
    },
    {
        "name": "Lacerating Wound",
        "original_damage_instance_potency": 90 + 21 * 4 - 7 * 20,
    },
    {
        "name": "Blood Insignia",
        "stacks_of_coagulation": 21,
        "previous_triggers_this_round": 8,
    },
    # Minimum potency of Blood Insignia is 30, so Lacerating Wound potency will be 30 at this point.
    {
        "name": "Lacerating Wound",
        "original_damage_instance_potency": 90 + 21 * 4 - 8 * 20,
    },
]


_t3: list[dict[str, Any]] = [
    # Passive: Starts with 21 stacks of Coagulation from previous turn.
    {"name": "Midnight Vesper", "stacks_of_coagulation": 21},
    {"name": "Lacerating Wound", "original_damage_instance_potency": 120 + 21 * 10},
    {"name": "Death Knell", "stacks_of_coagulation": 21},
    # Death Knell: Sextans gains 1 stack of Coagulation. For each Level of the target (Normal, Elite, Boss), gain 1 additional stack of Coagulation.
    # Assuming target is a Boss, total Coagulation stacks is 21 (initial) + 1 (Death Knell) + 3 (Boss) = 25 stacks.
    {"name": "Lacerating Wound", "original_damage_instance_potency": 120 + 21 * 10},
    # Target has Blood Kiss from the previous Sanctuary Lauds turn, so Death Knell triggers Blood Kiss.
    {"name": "Blood Kiss", "multiplier_of_death_knell": 120 + 21 * 10},
    {"name": "Lacerating Wound", "original_damage_instance_potency": 120 + 21 * 10},
    # Death Knell: When the skill hits an enemy target, Blood Insignia is triggered. After using the skill, Sextans gains 2 stacks
    # of Coagulation → 27 stacks.
    {
        "name": "Blood Insignia",
        "stacks_of_coagulation": 25,
        "previous_triggers_this_round": 0,
    },
    {"name": "Lacerating Wound", "original_damage_instance_potency": 90 + 25 * 4},
    # Blood Insignia triggers when allied units (excluding Sextans) attack with a blade:
    # Assume:
    # 4x from Ullrid
    # 4x from Phaetusa
    {
        "name": "Blood Insignia",
        "stacks_of_coagulation": 27,
        "previous_triggers_this_round": 1,
    },
    {
        "name": "Lacerating Wound",
        "original_damage_instance_potency": 90 + 27 * 4 - 1 * 20,
    },
    {
        "name": "Blood Insignia",
        "stacks_of_coagulation": 27,
        "previous_triggers_this_round": 2,
    },
    {
        "name": "Lacerating Wound",
        "original_damage_instance_potency": 90 + 27 * 4 - 2 * 20,
    },
    {
        "name": "Blood Insignia",
        "stacks_of_coagulation": 27,
        "previous_triggers_this_round": 3,
    },
    {
        "name": "Lacerating Wound",
        "original_damage_instance_potency": 90 + 27 * 4 - 3 * 20,
    },
    {
        "name": "Blood Insignia",
        "stacks_of_coagulation": 27,
        "previous_triggers_this_round": 4,
    },
    {
        "name": "Lacerating Wound",
        "original_damage_instance_potency": 90 + 27 * 4 - 4 * 20,
    },
    {
        "name": "Blood Insignia",
        "stacks_of_coagulation": 27,
        "previous_triggers_this_round": 5,
    },
    {
        "name": "Lacerating Wound",
        "original_damage_instance_potency": 90 + 27 * 4 - 5 * 20,
    },
    {
        "name": "Blood Insignia",
        "stacks_of_coagulation": 27,
        "previous_triggers_this_round": 6,
    },
    {
        "name": "Lacerating Wound",
        "original_damage_instance_potency": 90 + 27 * 4 - 6 * 20,
    },
    {
        "name": "Blood Insignia",
        "stacks_of_coagulation": 27,
        "previous_triggers_this_round": 7,
    },
    {
        "name": "Lacerating Wound",
        "original_damage_instance_potency": 90 + 27 * 4 - 7 * 20,
    },
]

_t4: list[dict[str, Any]] = [
    {"name": "Sanctuary Lauds", "stacks_of_coagulation": 27},
    {"name": "Lacerating Wound", "original_damage_instance_potency": 90 + 27 * 10},
    {"name": "Death Knell", "stacks_of_coagulation": 27},
    # Death Knell: Sextans gains 1 stack of Coagulation. For each Level of the target (Normal, Elite, Boss), gain 1 additional stack of Coagulation.
    # Assuming target is a Boss, total Coagulation stacks is 27 (initial) + 1 (Death Knell) + 3 (Boss) = 31 stacks.
    {"name": "Lacerating Wound", "original_damage_instance_potency": 90 + 27 * 10},
    # Target now has Blood Kiss from Sanctuary Lauds, so Death Knell will trigger Blood Kiss.
    {"name": "Blood Kiss", "multiplier_of_death_knell": 120 + 27 * 10},
    {"name": "Lacerating Wound", "original_damage_instance_potency": 120 + 27 * 10},
    # Death Knell: When the skill hits an enemy target, Blood Insignia is triggered. After using the skill, Sextans gains 2 stacks
    # of Coagulation.
    {
        "name": "Blood Insignia",
        "stacks_of_coagulation": 31,
        "previous_triggers_this_round": 0,
    },
    {"name": "Lacerating Wound", "original_damage_instance_potency": 90 + 31 * 4},
    # Passive - Requiem: When an enemy unit dies or is in Stability Break, Sextans gains 1 stack of Coagulation.
    # For each Level of the target (Normal, Elite, Boss), gain 1 additional stack of Coagulation.
    # Assume Boss is in Stability Break now, so increment the Coagulation stack count by 4 (1 for the passive trigger and 3 for the Boss level).
    # Total Coagulation stacks is 31 (after Death Knell hit) + 2 (Death Knell completion) + 4 (Stability Break passive) = 37 stacks.
    # Blood Insignia triggers when allied units (excluding Sextans) attack with a blade:
    # Assume:
    # 4x from Ullrid
    # 4x from Phaetusa
    {
        "name": "Blood Insignia",
        "stacks_of_coagulation": 37,
        "previous_triggers_this_round": 1,
    },
    {
        "name": "Lacerating Wound",
        "original_damage_instance_potency": 90 + 37 * 4 - 1 * 20,
    },
    {
        "name": "Blood Insignia",
        "stacks_of_coagulation": 37,
        "previous_triggers_this_round": 2,
    },
    {
        "name": "Lacerating Wound",
        "original_damage_instance_potency": 90 + 37 * 4 - 2 * 20,
    },
    {
        "name": "Blood Insignia",
        "stacks_of_coagulation": 37,
        "previous_triggers_this_round": 3,
    },
    {
        "name": "Lacerating Wound",
        "original_damage_instance_potency": 90 + 37 * 4 - 3 * 20,
    },
    {
        "name": "Blood Insignia",
        "stacks_of_coagulation": 37,
        "previous_triggers_this_round": 4,
    },
    {
        "name": "Lacerating Wound",
        "original_damage_instance_potency": 90 + 37 * 4 - 4 * 20,
    },
    {
        "name": "Blood Insignia",
        "stacks_of_coagulation": 37,
        "previous_triggers_this_round": 5,
    },
    {
        "name": "Lacerating Wound",
        "original_damage_instance_potency": 90 + 37 * 4 - 5 * 20,
    },
    {
        "name": "Blood Insignia",
        "stacks_of_coagulation": 37,
        "previous_triggers_this_round": 6,
    },
    {
        "name": "Lacerating Wound",
        "original_damage_instance_potency": 90 + 37 * 4 - 6 * 20,
    },
    {
        "name": "Blood Insignia",
        "stacks_of_coagulation": 37,
        "previous_triggers_this_round": 7,
    },
    {
        "name": "Lacerating Wound",
        "original_damage_instance_potency": 90 + 37 * 4 - 7 * 20,
    },
    {
        "name": "Blood Insignia",
        "stacks_of_coagulation": 37,
        "previous_triggers_this_round": 8,
    },
    {
        "name": "Lacerating Wound",
        "original_damage_instance_potency": 90 + 37 * 4 - 8 * 20,
    },
]

_t5: list[dict[str, Any]] = [
    # Passive: Starts with 37 stacks of Coagulation from previous turn.
    {"name": "Midnight Vesper", "stacks_of_coagulation": 37},
    {"name": "Lacerating Wound", "original_damage_instance_potency": 120 + 37 * 10},
    {"name": "Death Knell", "stacks_of_coagulation": 37},
    # Death Knell: Sextans gains 1 stack of Coagulation. For each Level of the target (Normal, Elite, Boss), gain 1 additional stack of Coagulation.
    # Assuming target is a Boss, total Coagulation stacks is 37 (initial) + 1 (Death Knell) + 3 (Boss) = 41 stacks.
    {"name": "Lacerating Wound", "original_damage_instance_potency": 120 + 37 * 10},
    # Target has Blood Kiss from the previous Sanctuary Lauds turn, so Death Knell triggers Blood Kiss.
    {"name": "Blood Kiss", "multiplier_of_death_knell": 120 + 37 * 10},
    {"name": "Lacerating Wound", "original_damage_instance_potency": 120 + 37 * 10},
    # Death Knell: When the skill hits an enemy target, Blood Insignia is triggered. After using the skill, Sextans gains 2 stacks
    # of Coagulation → 43 stacks.
    {
        "name": "Blood Insignia",
        "stacks_of_coagulation": 41,
        "previous_triggers_this_round": 0,
    },
    {"name": "Lacerating Wound", "original_damage_instance_potency": 90 + 41 * 4},
    # Blood Insignia triggers when allied units (excluding Sextans) attack with a blade:
    # Assume:
    # 4x from Ullrid
    # 4x from Phaetusa
    {
        "name": "Blood Insignia",
        "stacks_of_coagulation": 43,
        "previous_triggers_this_round": 1,
    },
    {
        "name": "Lacerating Wound",
        "original_damage_instance_potency": 90 + 43 * 4 - 1 * 20,
    },
    {
        "name": "Blood Insignia",
        "stacks_of_coagulation": 43,
        "previous_triggers_this_round": 2,
    },
    {
        "name": "Lacerating Wound",
        "original_damage_instance_potency": 90 + 43 * 4 - 2 * 20,
    },
    {
        "name": "Blood Insignia",
        "stacks_of_coagulation": 43,
        "previous_triggers_this_round": 3,
    },
    {
        "name": "Lacerating Wound",
        "original_damage_instance_potency": 90 + 43 * 4 - 3 * 20,
    },
    {
        "name": "Blood Insignia",
        "stacks_of_coagulation": 43,
        "previous_triggers_this_round": 4,
    },
    {
        "name": "Lacerating Wound",
        "original_damage_instance_potency": 90 + 43 * 4 - 4 * 20,
    },
    {
        "name": "Blood Insignia",
        "stacks_of_coagulation": 43,
        "previous_triggers_this_round": 5,
    },
    {
        "name": "Lacerating Wound",
        "original_damage_instance_potency": 90 + 43 * 4 - 5 * 20,
    },
    {
        "name": "Blood Insignia",
        "stacks_of_coagulation": 43,
        "previous_triggers_this_round": 6,
    },
    {
        "name": "Lacerating Wound",
        "original_damage_instance_potency": 90 + 43 * 4 - 6 * 20,
    },
    {
        "name": "Blood Insignia",
        "stacks_of_coagulation": 43,
        "previous_triggers_this_round": 7,
    },
    {
        "name": "Lacerating Wound",
        "original_damage_instance_potency": 90 + 43 * 4 - 7 * 20,
    },
]

_t6: list[dict[str, Any]] = [
    {"name": "Sanctuary Lauds", "stacks_of_coagulation": 43},
    {"name": "Lacerating Wound", "original_damage_instance_potency": 90 + 43 * 10},
    {"name": "Death Knell", "stacks_of_coagulation": 43},
    # Death Knell: Sextans gains 1 stack of Coagulation. For each Level of the target (Normal, Elite, Boss), gain 1 additional stack of Coagulation.
    # Assuming target is a Boss, total Coagulation stacks is 43 (initial) + 1 (Death Knell) + 3 (Boss) = 47 stacks.
    {"name": "Lacerating Wound", "original_damage_instance_potency": 90 + 43 * 10},
    # Target now has Blood Kiss from Sanctuary Lauds, so Death Knell will trigger Blood Kiss.
    {"name": "Blood Kiss", "multiplier_of_death_knell": 120 + 43 * 10},
    {"name": "Lacerating Wound", "original_damage_instance_potency": 120 + 43 * 10},
    # Death Knell: When the skill hits an enemy target, Blood Insignia is triggered. After using the skill, Sextans gains 2 stacks
    # of Coagulation.
    {
        "name": "Blood Insignia",
        "stacks_of_coagulation": 47,
        "previous_triggers_this_round": 0,
    },
    {"name": "Lacerating Wound", "original_damage_instance_potency": 90 + 47 * 4},
    # Passive - Requiem: When an enemy unit dies or is in Stability Break, Sextans gains 1 stack of Coagulation.
    # For each Level of the target (Normal, Elite, Boss), gain 1 additional stack of Coagulation.
    # Assume Boss is in Stability Break now, so increment the Coagulation stack count by 4 (1 for the passive trigger and 3 for the Boss level).
    # Total Coagulation stacks is 47 (after Death Knell hit) + 2 (Death Knell completion) + 4 (Stability Break passive) = 53 stacks.
    # Blood Insignia triggers when allied units (excluding Sextans) attack with a blade:
    # Assume:
    # 4x from Ullrid
    # 4x from Phaetusa
    {
        "name": "Blood Insignia",
        "stacks_of_coagulation": 53,
        "previous_triggers_this_round": 1,
    },
    {
        "name": "Lacerating Wound",
        "original_damage_instance_potency": 90 + 53 * 4 - 1 * 20,
    },
    {
        "name": "Blood Insignia",
        "stacks_of_coagulation": 53,
        "previous_triggers_this_round": 2,
    },
    {
        "name": "Lacerating Wound",
        "original_damage_instance_potency": 90 + 53 * 4 - 2 * 20,
    },
    {
        "name": "Blood Insignia",
        "stacks_of_coagulation": 53,
        "previous_triggers_this_round": 3,
    },
    {
        "name": "Lacerating Wound",
        "original_damage_instance_potency": 90 + 53 * 4 - 3 * 20,
    },
    {
        "name": "Blood Insignia",
        "stacks_of_coagulation": 53,
        "previous_triggers_this_round": 4,
    },
    {
        "name": "Lacerating Wound",
        "original_damage_instance_potency": 90 + 53 * 4 - 4 * 20,
    },
    {
        "name": "Blood Insignia",
        "stacks_of_coagulation": 53,
        "previous_triggers_this_round": 5,
    },
    {
        "name": "Lacerating Wound",
        "original_damage_instance_potency": 90 + 53 * 4 - 5 * 20,
    },
    {
        "name": "Blood Insignia",
        "stacks_of_coagulation": 53,
        "previous_triggers_this_round": 6,
    },
    {
        "name": "Lacerating Wound",
        "original_damage_instance_potency": 90 + 53 * 4 - 6 * 20,
    },
    {
        "name": "Blood Insignia",
        "stacks_of_coagulation": 53,
        "previous_triggers_this_round": 7,
    },
    {
        "name": "Lacerating Wound",
        "original_damage_instance_potency": 90 + 53 * 4 - 7 * 20,
    },
    {
        "name": "Blood Insignia",
        "stacks_of_coagulation": 53,
        "previous_triggers_this_round": 8,
    },
    {
        "name": "Lacerating Wound",
        "original_damage_instance_potency": 90 + 53 * 4 - 8 * 20,
    },
]

_t7: list[dict[str, Any]] = [
    # Passive: Starts with 53 stacks of Coagulation from previous turn.
    {"name": "Midnight Vesper", "stacks_of_coagulation": 53},
    {"name": "Lacerating Wound", "original_damage_instance_potency": 120 + 53 * 10},
    {"name": "Death Knell", "stacks_of_coagulation": 53},
    # Death Knell: Sextans gains 1 stack of Coagulation. For each Level of the target (Normal, Elite, Boss), gain 1 additional stack of Coagulation.
    # Assuming target is a Boss, total Coagulation stacks is 53 (initial) + 1 (Death Knell) + 3 (Boss) = 57 stacks.
    {"name": "Lacerating Wound", "original_damage_instance_potency": 120 + 53 * 10},
    # Target has Blood Kiss from the previous Sanctuary Lauds turn, so Death Knell triggers Blood Kiss.
    {"name": "Blood Kiss", "multiplier_of_death_knell": 120 + 53 * 10},
    {"name": "Lacerating Wound", "original_damage_instance_potency": 120 + 53 * 10},
    # Death Knell: When the skill hits an enemy target, Blood Insignia is triggered. After using the skill, Sextans gains 2 stacks
    # of Coagulation → 59 stacks.
    {
        "name": "Blood Insignia",
        "stacks_of_coagulation": 57,
        "previous_triggers_this_round": 0,
    },
    {"name": "Lacerating Wound", "original_damage_instance_potency": 90 + 57 * 4},
    # Blood Insignia triggers when allied units (excluding Sextans) attack with a blade:
    # Assume:
    # 4x from Ullrid
    # 4x from Phaetusa
    {
        "name": "Blood Insignia",
        "stacks_of_coagulation": 59,
        "previous_triggers_this_round": 1,
    },
    {
        "name": "Lacerating Wound",
        "original_damage_instance_potency": 90 + 59 * 4 - 1 * 20,
    },
    {
        "name": "Blood Insignia",
        "stacks_of_coagulation": 59,
        "previous_triggers_this_round": 2,
    },
    {
        "name": "Lacerating Wound",
        "original_damage_instance_potency": 90 + 59 * 4 - 2 * 20,
    },
    {
        "name": "Blood Insignia",
        "stacks_of_coagulation": 59,
        "previous_triggers_this_round": 3,
    },
    {
        "name": "Lacerating Wound",
        "original_damage_instance_potency": 90 + 59 * 4 - 3 * 20,
    },
    {
        "name": "Blood Insignia",
        "stacks_of_coagulation": 59,
        "previous_triggers_this_round": 4,
    },
    {
        "name": "Lacerating Wound",
        "original_damage_instance_potency": 90 + 59 * 4 - 4 * 20,
    },
    {
        "name": "Blood Insignia",
        "stacks_of_coagulation": 59,
        "previous_triggers_this_round": 5,
    },
    {
        "name": "Lacerating Wound",
        "original_damage_instance_potency": 90 + 59 * 4 - 5 * 20,
    },
    {
        "name": "Blood Insignia",
        "stacks_of_coagulation": 59,
        "previous_triggers_this_round": 6,
    },
    {
        "name": "Lacerating Wound",
        "original_damage_instance_potency": 90 + 59 * 4 - 6 * 20,
    },
    {
        "name": "Blood Insignia",
        "stacks_of_coagulation": 59,
        "previous_triggers_this_round": 7,
    },
    {
        "name": "Lacerating Wound",
        "original_damage_instance_potency": 90 + 59 * 4 - 7 * 20,
    },
]


sample_rotation: dict[int, list[dict]] = {
    1: _t1,
    2: _t2,
    3: _t3,
    4: _t4,
    5: _t5,
    6: _t6,
    7: _t7,
}


class Sextans(DollCalculatorPage):
    """Page for Sextans."""

    def __init__(self):
        super().__init__()

        self.doll = sextans.Sextans()
        self.doll.set_fortification_level(FortificationLevel.SEGMENT06)
        self.doll_subtitle: str = """Melee / Tile / Blade Support

            Support / Electric"""
        self.dandegate_link: str = "https://www.dandegate.net/dolls/sextans"
        self.doll_portrait: str = "resources/sextans.webp"

    @override
    def update_doll_abilities(self) -> None:
        doll = cast(sextans.Sextans, self.doll)
        blood_kiss = sextans.BloodKiss()

        self.option_config: dict[str, dict[str, Any]] = {
            "Dreamscape Garrote": {
                "fields": [],
                "function": doll.dreamscape_garrote.execute,
            },
            "Sanctuary Lauds": {
                "fields": [
                    {
                        "key": "stacks_of_coagulation",
                        "type": "number",
                        "label": "Coagulation stacks",
                        "default": 15,
                    },
                ],
                "function": doll.sanctuary_lauds.execute,
            },
            "Death Knell": {
                "fields": [
                    {
                        "key": "stacks_of_coagulation",
                        "type": "number",
                        "label": "Coagulation stacks",
                        "default": 15,
                    },
                ],
                "function": doll.death_knell.execute,
            },
            "Midnight Vesper": {
                "fields": [
                    {
                        "key": "stacks_of_coagulation",
                        "type": "number",
                        "label": "Coagulation stacks",
                        "default": 15,
                    },
                ],
                "function": doll.midnight_vesper.execute,
            },
            "Blood Insignia": {
                "fields": [
                    {
                        "key": "stacks_of_coagulation",
                        "type": "number",
                        "label": "Coagulation stacks",
                        "default": 15,
                    },
                    {
                        "key": "previous_triggers_this_round",
                        "type": "number",
                        "label": "Previous Triggers This Round",
                        "default": 0,
                    },
                ],
                "function": doll.blood_insignia.execute,
            },
            "Blood Kiss": {
                "fields": [
                    {
                        "key": "multiplier_of_death_knell",
                        "type": "number",
                        "label": "Triggering Death Knell Multiplier",
                        "default": 240,
                    },
                ],
                "function": blood_kiss.execute,
            },
            "Lacerating Wound": {
                "fields": [
                    {
                        "key": "original_damage_instance_potency",
                        "type": "number",
                        "label": "Original Damage Multiplier",
                        "default": 100,
                    },
                ],
                "function": doll.lacerating_wound.execute,
            },
        }

    @override
    def set_initial_values(self) -> None:
        doll = cast(sextans.Sextans, self.doll)

        doll.initial_stats.basic_attributes[StatType.ATTACK] = 4000
        doll.initial_stats.basic_attributes[StatType.CRIT_RATE] = 80
        doll.initial_stats.basic_attributes[StatType.CRIT_DAMAGE] = 150

        # Baseline non-innate modifiers used for quick comparisons.
        doll.additive_modifiers.special_attributes[
            SpecialAttribute.DAMAGE_BOOST
        ].set_multiplier(DamageTag.ALL, 12 + 0.4 + 4 + 3)

        doll.additive_modifiers.special_attributes[
            SpecialAttribute.DAMAGE_BOOST
        ].set_multiplier(DamageTag.ELECTRIC, 5 + 1.5 + 0.9)

        doll.additive_modifiers.special_attributes[
            SpecialAttribute.DAMAGE_BOOST
        ].set_multiplier(DamageTag.PHASE, 15)

        doll.additive_modifiers.special_attributes[
            SpecialAttribute.DAMAGE_BOOST
        ].set_multiplier(DamageTag.MELEE, 24)

        doll.additive_modifiers.special_attributes[
            SpecialAttribute.CRITICAL_DAMAGE
        ].set_multiplier(DamageTag.ALL, 2.4)

        doll.multiplicative_modifiers.basic_attributes[StatType.ATTACK] = 8 + 3.6

    def get_default_damage_calculator_buffs(self) -> list[dict[str, Any]]:
        return [
            {"name": "Attack Up II"},
            {
                "name": "Positive Charge",
                "target_has_negative_charge": True,
            },
            {
                "name": "Power Surge",
                "stacks": 3,
                "jiangyu_fortification_level": FortificationLevel.SEGMENT06,
                "target_voltage_sag_stacks": 3,
            },
            {"name": "Electric Boost II"},
            {
                "name": "Coagulation (Sextans)",
                "sextans_fortification_level": FortificationLevel.SEGMENT06,
                "stacks": 15,
            },
            {
                "name": "Holy Blood Mark (Melee) (Sextans)",
                "sextans_fortification_level": FortificationLevel.SEGMENT06,
                "stacks_of_coagulation": 15,
            },
        ]

    def get_default_damage_calculator_debuffs(self) -> list[dict[str, Any]]:
        return [
            {"name": "Defense Down II"},
            {
                "name": "Voltage Sag",
                "stacks": 3,
                "jiangyu_fortification_level": FortificationLevel.SEGMENT06,
            },
            {
                "name": "Scarlet Insignia (Sextans)",
                "stacks": 3,
                "sextans_fortification_level": FortificationLevel.SEGMENT06,
            },
        ]

    @override
    def get_model_assumptions(self) -> list[ModelAssumption]:
        return [
            ModelAssumption(
                icon="auto_graph",
                description="Critical rate overflow scaling from Coagulation and Requiem's melee damage bonus are applied in Damage Calculator.",
            ),
            ModelAssumption(
                icon="carpenter",
                description="Passive's effect of increasing damage dealt by all Dolls wielding blades is automatically applied in Damage Calculator. However, the damage increase effect when Confectance Index is full is not applied by default.",
            ),
            ModelAssumption(
                icon="bloodtype",
                description="Sample rotation assumes 8 triggers of Blood Insignia from allied units.",
            ),
        ]

    @override
    def get_rotation_planner(self) -> None:
        with ui.card().classes("w-full h-full"):

            def update_all():
                self.damage_instances = self.rotation_planner.get_all_actions()
                self.stats_update_callback(None)  # type: ignore

            ui.button("Update", on_click=update_all).classes("w-full")
            self.rotation_planner: RotationPlanner = RotationPlanner(
                options_config=self.option_config
            )
            self.rotation_planner.set_data(sample_rotation)
