from nicegui import ui

from gui.templates.doll_calculator_page import DollCalculatorPage, ModelAssumption
from gui.templates.rotation_planner import RotationPlanner
from typing import Any, override
from core.types import (
    StatType,
    FortificationLevel,
    SpecialAttribute,
    DamageTag,
)
from core.dolls import robella

sample_rotation: dict[int, list[dict]] = {
    1: [
        {"name": "Unity: Enhanced"},
        {"name": "Unity: Enhanced"},
        {"name": "Unity: Enhanced"},
        {"name": "Unity: Enhanced"},
        {"name": "Unity: Enhanced"},
        {
            "name": "Frigid Infiltration: Enhanced",
            "sense_weakness_stacks": 0,
            "inspection_stacks": 6,
        },
    ],
    2: [
        {"name": "Howling Cyclone", "sense_weakness_stacks": 6},
        {"name": "Unity: Enhanced"},
        {"name": "Unity: Enhanced"},
        {"name": "Unity: Enhanced"},
        {"name": "Unity: Enhanced"},
        {
            "name": "Frigid Infiltration: Enhanced",
            "sense_weakness_stacks": 6,
            "inspection_stacks": 6,
        },
    ],
    3: [
        {"name": "Ultra Shot", "sense_weakness_stacks": 12},
        {"name": "Unity: Enhanced"},
        {"name": "Unity: Enhanced"},
        {"name": "Unity: Enhanced"},
        {"name": "Unity: Enhanced"},
        {
            "name": "Frigid Infiltration: Enhanced",
            "sense_weakness_stacks": 12,
            "inspection_stacks": 6,
        },
    ],
    4: [
        {"name": "Howling Cyclone", "sense_weakness_stacks": 18},
        {"name": "Unity: Enhanced"},
        {"name": "Unity: Enhanced"},
        {"name": "Unity: Enhanced"},
        {"name": "Unity: Enhanced"},
        {"name": "Unity: Enhanced"},
        {
            "name": "Frigid Infiltration: Enhanced",
            "sense_weakness_stacks": 18,
            "inspection_stacks": 6,
        },
    ],
    5: [
        {"name": "Unity: Enhanced"},
        {"name": "Unity: Enhanced"},
        {"name": "Unity: Enhanced"},
        {"name": "Unity: Enhanced"},
        {
            "name": "Frigid Infiltration: Enhanced",
            "sense_weakness_stacks": 24,
            "inspection_stacks": 6,
        },
    ],
    6: [
        {"name": "Howling Cyclone", "sense_weakness_stacks": 30},
        {"name": "Unity: Enhanced"},
        {"name": "Unity: Enhanced"},
        {"name": "Unity: Enhanced"},
        {"name": "Unity: Enhanced"},
        {
            "name": "Frigid Infiltration: Enhanced",
            "sense_weakness_stacks": 30,
            "inspection_stacks": 6,
        },
    ],
    7: [
        {"name": "Howling Cyclone", "sense_weakness_stacks": 36},
        {"name": "Unity: Enhanced"},
        {"name": "Unity: Enhanced"},
        {"name": "Unity: Enhanced"},
        {"name": "Unity: Enhanced"},
        {
            "name": "Frigid Infiltration: Enhanced",
            "sense_weakness_stacks": 36,
            "inspection_stacks": 6,
        },
    ],
}


class Robella(DollCalculatorPage):
    """Page for Robella."""

    def __init__(self):
        super().__init__()

        self.doll: robella.Robella = robella.Robella()
        self.doll.set_fortification_level(FortificationLevel.SEGMENT06)
        self.doll_subtitle: str = """Burst Damage / Pursuit

            Sentinel / Freeze"""
        self.dandegate_link: str = "https://www.dandegate.net/dolls/robella"
        self.doll_portrait: str = "resources/robella.webp"

    @override
    def update_doll_abilities(self) -> None:
        self.option_config: dict[str, dict[str, Any]] = {
            "Ultra Shot": {
                "fields": [
                    {
                        "key": "sense_weakness_stacks",
                        "type": "number",
                        "label": "Sense Weakness Stacks",
                        "default": 0,
                    },
                ],
                "function": self.doll.ultra_shot.execute,
            },
            "Unity": {"fields": [], "function": self.doll.unity.execute},
            "Unity: Enhanced": {
                "fields": [],
                "function": self.doll.unity_enhanced.execute,
            },
            "Frigid Infiltration": {
                "fields": [
                    {
                        "key": "inspection_stacks",
                        "type": "number",
                        "label": "Inspection Stacks",
                        "default": 6,
                    },
                    {
                        "key": "sense_weakness_stacks",
                        "type": "number",
                        "label": "Sense Weakness Stacks",
                        "default": 0,
                    },
                ],
                "function": self.doll.frigid_infiltration.execute,
            },
            "Frigid Infiltration: Enhanced": {
                "fields": [
                    {
                        "key": "inspection_stacks",
                        "type": "number",
                        "label": "Inspection Stacks",
                        "default": 6,
                    },
                    {
                        "key": "sense_weakness_stacks",
                        "type": "number",
                        "label": "Sense Weakness Stacks",
                        "default": 0,
                    },
                ],
                "function": self.doll.frigid_infiltration_enhanced.execute,
            },
            "Howling Cyclone": {
                "fields": [
                    {
                        "key": "sense_weakness_stacks",
                        "type": "number",
                        "label": "Sense Weakness Stacks",
                        "default": 0,
                    },
                ],
                "function": self.doll.howling_cyclone.execute,
            },
        }

        self.add_elemental_tile_actions_for_element(
            self.option_config,
            DamageTag.FREEZE,
        )

    @override
    def set_initial_values(self) -> None:
        self.doll.initial_stats.basic_attributes[StatType.ATTACK] = 4830
        self.doll.initial_stats.basic_attributes[StatType.CRIT_RATE] = 81
        self.doll.initial_stats.basic_attributes[StatType.CRIT_DAMAGE] = 154.5

        # Attachments, common keys, imagoform, specialized traits

        # imagoform: 5+12
        # CQC elite: 0.4
        # Alva 6P33: 10
        # Imagoform (Shoot): 4+3
        # Dushevnaya Expansion Key: 10
        # Dushevnaya Passive: 10
        self.doll.additive_modifiers.special_attributes[
            SpecialAttribute.DAMAGE_BOOST
        ].set_multiplier(DamageTag.ALL, 17 + 0.4 + 10 + 4 + 3 + 10 + 10)

        # weapon: 15
        # attachment: 20
        # imagoform: 5
        # freeze boost: 1.5
        # Alva Brumal Barrier: <Alva Attack>*2/1000*1.5 = 11.4 at 3800 attack
        # Alva Covering Mode: 20
        # Freeze Unity: 0.9
        # Dushevnaya Expansion Key: 15+10
        # Dushevnaya Eulogistic Verse: 10
        # Dushevnaya Passive: 10
        # Dushevnaya Imagoform (Bud): 3
        self.doll.additive_modifiers.special_attributes[
            SpecialAttribute.DAMAGE_BOOST
        ].set_multiplier(
            DamageTag.FREEZE, 15 + 20 + 5 + 1.5 + 11.4 + 20 + 0.9 + 15 + 10 + 10 + 3
        )

        # keys: 30
        self.doll.additive_modifiers.special_attributes[
            SpecialAttribute.DAMAGE_BOOST
        ].set_multiplier(DamageTag.PHASE, 30)

        # weapon: 14
        # raid stance: 1
        self.doll.additive_modifiers.special_attributes[
            SpecialAttribute.DAMAGE_BOOST
        ].set_multiplier(DamageTag.PASSIVE, 14 + 1)

        # imagoform: 10
        self.doll.additive_modifiers.special_attributes[
            SpecialAttribute.DAMAGE_BOOST
        ].set_multiplier(DamageTag.STABILITY_BROKEN, 10)

        # thronebreaker: 5
        self.doll.additive_modifiers.special_attributes[
            SpecialAttribute.DAMAGE_BOOST
        ].set_multiplier(DamageTag.BOSS, 5)

        # smite boost: 2.4
        self.doll.additive_modifiers.special_attributes[
            SpecialAttribute.CRITICAL_DAMAGE
        ].set_multiplier(DamageTag.ALL, 2.4)

        # ambush mastery: 0.2
        self.doll.additive_modifiers.special_attributes[
            SpecialAttribute.CRITICAL_DAMAGE
        ].set_multiplier(DamageTag.PASSIVE, 0.2)

        # Alva 6P33: 10
        self.doll.additive_modifiers.special_attributes[
            SpecialAttribute.CRITICAL_DAMAGE
        ].set_multiplier(DamageTag.FREEZE, 10)

        # imagoform: 8
        # attack boost: 3.6
        # Alva Imagoform: 3
        self.doll.multiplicative_modifiers.basic_attributes[StatType.ATTACK] = (
            8 + 3.6 + 3
        )

    def get_default_damage_calculator_buffs(self) -> list[dict[str, Any]]:
        return [
            {"name": "Attack Up II"},
            {
                "name": "Brumal Barrier (Alva)",
                "alva_fortification_level": FortificationLevel.SEGMENT05,
                "shield_size": 9000,
            },
            {
                "name": "Radiant Rise (Robella)",
                "fortification_level": FortificationLevel.SEGMENT06,
            },
            {
                "name": "Light of Bond",
                "target_ally_initial_attack": 4000,
            },
            {
                "name": "Sense Weakness (Robella)",
                "stacks": 6,
            },
            {"name": "Covering Mode (Alva)"},
        ]

    def get_default_damage_calculator_debuffs(self) -> list[dict[str, Any]]:
        return [
            {"name": "Defense Down II"},
            {
                "name": "Hypothermia",
                "alva_fortification_level": FortificationLevel.SEGMENT05,
            },
            {
                "name": "Frostbite",
            },
        ]

    @override
    def get_model_assumptions(self) -> list[ModelAssumption]:
        return [
            ModelAssumption(
                icon="ac_unit",
                description="Sample rotation assumes Alva is V2+ (for confectance index gain) and is the Light of Bond recipient, performing an active attack or interception to proc each Unity: Enhanced instance.",
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
