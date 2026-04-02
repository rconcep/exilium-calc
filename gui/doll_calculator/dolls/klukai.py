from nicegui import ui

from gui.templates.doll_calculator_page import DollCalculatorPage, ModelAssumption
from gui.templates.rotation_planner import RotationPlanner
from typing import Any, cast, override
from core.types import (
    StatType,
    FortificationLevel,
    SpecialAttribute,
    DamageTag,
)
from core.dolls import klukai


sample_rotation: dict[int, list[dict]] = {
    1: [
        {
            "name": "Devastating Drift",
            "number_targets_hit": 1,
            "target_is_boss": True,
            "has_fixed_key_2": True,
            "has_fixed_key_5": False,
        },
        {"name": "Corrosive Infusion", "stacks": 2},
        {"name": "Toxic Infiltration"},
        {
            "name": "Devastating Drift",
            "number_targets_hit": 1,
            "target_is_boss": True,
            "has_fixed_key_2": True,
            "has_fixed_key_5": False,
        },
        {"name": "Corrosive Infusion", "stacks": 3},
        {"name": "Toxic Infiltration"},
        {"name": "Corrosive Infusion", "stacks": 3},
    ],
    2: [
        {
            "name": "Devastating Drift",
            "number_targets_hit": 1,
            "target_is_boss": True,
            "has_fixed_key_2": True,
            "has_fixed_key_5": False,
        },
        {"name": "Corrosive Infusion", "stacks": 6},
        {"name": "Toxic Infiltration"},
        {
            "name": "Devastating Drift",
            "number_targets_hit": 1,
            "target_is_boss": True,
            "has_fixed_key_2": True,
            "has_fixed_key_5": False,
        },
        {"name": "Corrosive Infusion", "stacks": 7},
        {"name": "Toxic Infiltration"},
        {"name": "Corrosive Infusion", "stacks": 7},
    ],
    3: [
        {
            "name": "Devastating Drift",
            "number_targets_hit": 1,
            "target_is_boss": True,
            "has_fixed_key_2": True,
            "has_fixed_key_5": False,
        },
        {"name": "Corrosive Infusion", "stacks": 10},
        {"name": "Toxic Infiltration"},
        {
            "name": "Devastating Drift",
            "number_targets_hit": 1,
            "target_is_boss": True,
            "has_fixed_key_2": True,
            "has_fixed_key_5": False,
        },
        {"name": "Corrosive Infusion", "stacks": 11},
        {"name": "Toxic Infiltration"},
        {"name": "Corrosive Infusion", "stacks": 11},
    ],
    4: [
        {
            "name": "Devastating Drift",
            "number_targets_hit": 1,
            "target_is_boss": True,
            "has_fixed_key_2": True,
            "has_fixed_key_5": False,
        },
        {"name": "Corrosive Infusion", "stacks": 14},
        {"name": "Toxic Infiltration"},
        {
            "name": "Devastating Drift",
            "number_targets_hit": 1,
            "target_is_boss": True,
            "has_fixed_key_2": True,
            "has_fixed_key_5": False,
        },
        {"name": "Corrosive Infusion", "stacks": 15},
        {"name": "Toxic Infiltration"},
        {"name": "Corrosive Infusion", "stacks": 15},
    ],
    5: [
        {
            "name": "Devastating Drift",
            "number_targets_hit": 1,
            "target_is_boss": True,
            "has_fixed_key_2": True,
            "has_fixed_key_5": False,
        },
        {"name": "Corrosive Infusion", "stacks": 15},
        {"name": "Toxic Infiltration"},
        {
            "name": "Devastating Drift",
            "number_targets_hit": 1,
            "target_is_boss": True,
            "has_fixed_key_2": True,
            "has_fixed_key_5": False,
        },
        {"name": "Corrosive Infusion", "stacks": 15},
        {"name": "Toxic Infiltration"},
        {"name": "Corrosive Infusion", "stacks": 15},
    ],
    6: [
        {
            "name": "Devastating Drift",
            "number_targets_hit": 1,
            "target_is_boss": True,
            "has_fixed_key_2": True,
            "has_fixed_key_5": False,
        },
        {"name": "Corrosive Infusion", "stacks": 15},
        {"name": "Toxic Infiltration"},
        {
            "name": "Devastating Drift",
            "number_targets_hit": 1,
            "target_is_boss": True,
            "has_fixed_key_2": True,
            "has_fixed_key_5": False,
        },
        {"name": "Corrosive Infusion", "stacks": 15},
        {"name": "Toxic Infiltration"},
        {"name": "Corrosive Infusion", "stacks": 15},
    ],
    7: [
        {
            "name": "Devastating Drift",
            "number_targets_hit": 1,
            "target_is_boss": True,
            "has_fixed_key_2": True,
            "has_fixed_key_5": False,
        },
        {"name": "Corrosive Infusion", "stacks": 15},
        {"name": "Toxic Infiltration"},
        {
            "name": "Devastating Drift",
            "number_targets_hit": 1,
            "target_is_boss": True,
            "has_fixed_key_2": True,
            "has_fixed_key_5": False,
        },
        {"name": "Corrosive Infusion", "stacks": 15},
        {"name": "Toxic Infiltration"},
        {"name": "Corrosive Infusion", "stacks": 15},
    ],
}


class Klukai(DollCalculatorPage):
    """Page for Klukai."""

    def __init__(self):
        super().__init__()

        self.doll = klukai.Klukai()
        self.doll.set_fortification_level(FortificationLevel.SEGMENT06)
        self.doll_subtitle: str = """Burst Damage / Corrosion

            Sentinel / Corrosion"""
        self.dandegate_link: str = "https://www.dandegate.net/dolls/klukai"
        self.doll_portrait: str = "resources/klukai.webp"

    @override
    def update_doll_abilities(self) -> None:
        doll = cast(klukai.Klukai, self.doll)

        self.option_config: dict[str, dict[str, Any]] = {
            "Swift Strike": {
                "fields": [],
                "function": doll.swift_strike.execute,
            },
            "Pinpoint Detonation": {
                "fields": [],
                "function": doll.pinpoint_detonation_first.execute,
            },
            "Pinpoint Detonation (2nd)": {
                "fields": [
                    {
                        "key": "stacks_corrosion_infusion",
                        "type": "select",
                        "label": "Corrosive Infusion Stacks",
                        "options": [n for n in range(16)],
                        "default": 15,
                    },
                ],
                "function": doll.pinpoint_detonation_second.execute,
            },
            "Overpowering Corrosion": {
                "fields": [
                    {
                        "key": "target_has_toxic_infiltration",
                        "type": "checkbox",
                        "label": "Target Has Toxic Infiltration",
                        "default": True,
                    },
                ],
                "function": doll.overpowering_corrosion.execute,
            },
            "Devastating Drift": {
                "fields": [
                    {
                        "key": "number_targets_hit",
                        "type": "number",
                        "label": "Targets Hit",
                        "default": 1,
                    },
                    {
                        "key": "target_is_boss",
                        "type": "checkbox",
                        "label": "Target is a Boss",
                        "default": True,
                    },
                    {
                        "key": "has_fixed_key_2",
                        "type": "checkbox",
                        "label": "Fixed Key 2 - One Fell Swoop",
                        "default": True,
                    },
                    {
                        "key": "has_fixed_key_5",
                        "type": "checkbox",
                        "label": "Fixed Key 5 - Limit Break",
                        "default": False,
                    },
                ],
                "function": doll.devastating_drift.execute,
            },
            "Corrosive Infusion": {
                "fields": [
                    {
                        "key": "stacks",
                        "type": "select",
                        "label": "Corrosive Infusion Stacks",
                        "options": [n for n in range(16)],
                        "default": 15,
                    },
                ],
                "function": doll.corrosive_infusion.execute,
            },
            "Toxic Infiltration": {
                "fields": [],
                "function": doll.toxic_infiltration.execute,
            },
        }

    @override
    def set_initial_values(self) -> None:
        self.doll.initial_stats.basic_attributes[StatType.ATTACK] = 4210
        self.doll.initial_stats.basic_attributes[StatType.CRIT_RATE] = 80
        self.doll.initial_stats.basic_attributes[StatType.CRIT_DAMAGE] = 150

        # Attachments, common keys, imagoform, specialized traits
        self.doll.additive_modifiers.special_attributes[
            SpecialAttribute.DAMAGE_BOOST
        ].set_multiplier(DamageTag.ALL, 7)

        self.doll.additive_modifiers.special_attributes[
            SpecialAttribute.DAMAGE_BOOST
        ].set_multiplier(DamageTag.CORROSION, 20)

        self.doll.additive_modifiers.special_attributes[
            SpecialAttribute.DAMAGE_BOOST
        ].set_multiplier(DamageTag.PHASE, 15)

        self.doll.additive_modifiers.special_attributes[
            SpecialAttribute.DAMAGE_BOOST
        ].set_multiplier(DamageTag.ULTIMATE, 12)

        self.doll.additive_modifiers.special_attributes[
            SpecialAttribute.DAMAGE_BOOST
        ].set_multiplier(DamageTag.PASSIVE, 8)

        self.doll.additive_modifiers.special_attributes[
            SpecialAttribute.CRITICAL_DAMAGE
        ].set_multiplier(DamageTag.ALL, 3)

        self.doll.multiplicative_modifiers.basic_attributes[StatType.ATTACK] = 11

    @override
    def get_model_assumptions(self) -> list[ModelAssumption]:
        return [
            ModelAssumption(
                icon="key",
                description="Sample rotation assumes Fixed Key 1 - Deadly Entwine is active.",
                link_label="Dandegate",
                link_target="https://www.dandegate.net/dolls/klukai/keys/fixed-key-1-deadly-entwine",
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
