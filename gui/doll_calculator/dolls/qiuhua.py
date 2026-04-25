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
from core.dolls import qiuhua


sample_rotation: dict[int, list[dict]] = {
    1: [
        {"name": "Emergency Support"},
        {"name": "Emergency Support"},
        {"name": "Emergency Support"},
        {"name": "Emergency Support"},
        {"name": "Soaring Leap"},
        {"name": "Boil and Reduce", "confectance_index_spent": 6},
        {"name": "Scorch Mark", "stacks": 40},
        {"name": "Scorch Mark", "stacks": 40},
    ],
    2: [
        {"name": "Emergency Support"},
        {"name": "Emergency Support"},
        {"name": "Emergency Support"},
        {"name": "Emergency Support"},
        {
            "name": "Searing Sizzle",
            "target_is_within_4_tiles": True,
            "target_has_scorch_mark": True,
        },
    ],
    3: [
        {"name": "Emergency Support"},
        {"name": "Emergency Support"},
        {"name": "Emergency Support"},
        {"name": "Emergency Support"},
        {"name": "Soaring Leap"},
        {"name": "Boil and Reduce", "confectance_index_spent": 6},
        {"name": "Scorch Mark", "stacks": 40},
        {"name": "Scorch Mark", "stacks": 40},
    ],
    4: [
        {"name": "Emergency Support"},
        {"name": "Emergency Support"},
        {"name": "Emergency Support"},
        {"name": "Emergency Support"},
        {
            "name": "Searing Sizzle",
            "target_is_within_4_tiles": True,
            "target_has_scorch_mark": True,
        },
    ],
    5: [
        {"name": "Emergency Support"},
        {"name": "Emergency Support"},
        {"name": "Emergency Support"},
        {"name": "Emergency Support"},
        {"name": "Soaring Leap"},
        {"name": "Boil and Reduce", "confectance_index_spent": 6},
        {"name": "Scorch Mark", "stacks": 40},
        {"name": "Scorch Mark", "stacks": 40},
    ],
    6: [
        {"name": "Emergency Support"},
        {"name": "Emergency Support"},
        {"name": "Emergency Support"},
        {"name": "Emergency Support"},
        {
            "name": "Searing Sizzle",
            "target_is_within_4_tiles": True,
            "target_has_scorch_mark": True,
        },
    ],
    7: [
        {"name": "Emergency Support"},
        {"name": "Emergency Support"},
        {"name": "Emergency Support"},
        {"name": "Emergency Support"},
        {"name": "Soaring Leap"},
        {"name": "Boil and Reduce", "confectance_index_spent": 6},
        {"name": "Scorch Mark", "stacks": 40},
        {"name": "Scorch Mark", "stacks": 40},
    ],
}


class Qiuhua(DollCalculatorPage):
    """Page for Qiuhua."""

    def __init__(self):
        super().__init__()

        self.doll = qiuhua.Qiuhua()
        self.doll.set_fortification_level(FortificationLevel.SEGMENT06)
        self.doll_subtitle: str = """Mixed Damage / Stack / Assist

            Vanguard / Burn"""
        self.dandegate_link: str = "https://www.dandegate.net/dolls/qiuhua"
        self.doll_portrait: str = "resources/qiuhua.webp"

    @override
    def update_doll_abilities(self) -> None:
        doll = cast(qiuhua.Qiuhua, self.doll)

        self.option_config: dict[str, dict[str, Any]] = {
            "Trailblaze": {
                "fields": [],
                "function": doll.trailblaze.execute,
            },
            "Searing Sizzle": {
                "fields": [
                    {
                        "key": "target_is_within_4_tiles",
                        "type": "checkbox",
                        "label": "Target Within 4 Tiles",
                        "default": True,
                    },
                    {
                        "key": "target_has_scorch_mark",
                        "type": "checkbox",
                        "label": "Target Has Scorch Mark",
                        "default": True,
                    },
                ],
                "function": doll.searing_sizzle.execute,
            },
            "Soaring Leap": {
                "fields": [],
                "function": doll.soaring_leap.execute,
            },
            "Boil and Reduce": {
                "fields": [
                    {
                        "key": "confectance_index_spent",
                        "type": "select",
                        "label": "Confectance Index Spent",
                        "default": 6,
                        "options": [n for n in range(7)],
                    },
                ],
                "function": doll.boil_and_reduce.execute,
            },
            "Scorch Mark": {
                "fields": [
                    {
                        "key": "stacks",
                        "type": "number",
                        "label": "Scorch Mark Stacks",
                        "default": 40,
                    },
                ],
                "function": doll.scorch_mark.execute,
            },
            "Emergency Support": {
                "fields": [],
                "function": doll.emergency_support.execute,
            },
        }

    @override
    def set_initial_values(self) -> None:
        self.doll.initial_stats.basic_attributes[StatType.ATTACK] = 4210
        self.doll.initial_stats.basic_attributes[StatType.CRIT_RATE] = 86
        self.doll.initial_stats.basic_attributes[StatType.CRIT_DAMAGE] = 150

        # Attachments, common keys, imagoform, specialized traits
        self.doll.additive_modifiers.special_attributes[
            SpecialAttribute.DAMAGE_BOOST
        ].set_multiplier(DamageTag.ALL, 18)

        self.doll.additive_modifiers.special_attributes[
            SpecialAttribute.DAMAGE_BOOST
        ].set_multiplier(DamageTag.BURN, 24)

        self.doll.additive_modifiers.special_attributes[
            SpecialAttribute.DAMAGE_BOOST
        ].set_multiplier(DamageTag.PHASE, 15)

        self.doll.additive_modifiers.special_attributes[
            SpecialAttribute.DAMAGE_BOOST
        ].set_multiplier(DamageTag.PASSIVE, 8)

        self.doll.additive_modifiers.special_attributes[
            SpecialAttribute.CRITICAL_DAMAGE
        ].set_multiplier(DamageTag.ALL, 3)

        self.doll.additive_modifiers.special_attributes[
            SpecialAttribute.CRITICAL_DAMAGE
        ].set_multiplier(DamageTag.BURN, 8)

        self.doll.multiplicative_modifiers.basic_attributes[StatType.ATTACK] = 11

    def get_default_damage_calculator_buffs(self) -> list[dict[str, Any]]:
        return [
            {"name": "Blazing Assault II"},
            {
                "name": "Accelerant (Vector)",
                "vector_fortification_level": FortificationLevel.SEGMENT06,
                "number_of_burn_buffs": 3,
            },
            {"name": "Wok Hei (Qiuhua)", "stacks": 4},
        ]

    def get_default_damage_calculator_debuffs(self) -> list[dict[str, Any]]:
        return [
            {"name": "Defense Down II"},
            {"name": "Vulnerable II"},
            {
                "name": "Overheat Combustion",
                "vector_fortification_level": FortificationLevel.SEGMENT06,
            },
            {"name": "Conflagration"},
            {
                "name": "Smolder",
                "vector_fortification_level": FortificationLevel.SEGMENT06,
                "number_of_burn_debuffs": 4,
            },
        ]

    @override
    def get_model_assumptions(self) -> list[ModelAssumption]:
        return [
            ModelAssumption(
                icon="key",
                description="Expansion Key - Sizzling Stir-Fry is active.",
                link_label="Dandegate",
                link_target="https://www.dandegate.net/dolls/qiuhua/keys/expansion-key-sizzling-stir-fry",
            ),
            ModelAssumption(
                icon="local_fire_department",
                description="The % Attack buff from V3 Passive currently assumes 30 Scorch Mark stacks.",
            ),
            ModelAssumption(
                icon="key",
                description="Sample rotation assumes Fixed Key 1 - Meal Prep is active.",
                link_label="Dandegate",
                link_target="https://www.dandegate.net/dolls/qiuhua/keys/fixed-key-1-meal-prep",
            ),
            ModelAssumption(
                icon="key",
                description="Sample rotation assumes Fixed Key 2 - Roaring Stove is active.",
                link_label="Dandegate",
                link_target="https://www.dandegate.net/dolls/qiuhua/keys/fixed-key-2-roaring-stove",
            ),
            ModelAssumption(
                icon="local_fire_department",
                description="Sample rotation assumes V1+ Vector for additional Emergency Support actions.",
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
