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
from core.dolls import daiyan


sample_rotation: dict[int, list[dict]] = {
    1: [
        {"name": "Ethereal Resonance", "did_not_intercept_last_round": False},
        {"name": "Flowing Melody of the Clouds", "stacks_of_permanent_tuning": 1},
    ],
    2: [
        {"name": "Ethereal Resonance", "did_not_intercept_last_round": True},
        {"name": "Flowing Melody of the Clouds", "stacks_of_permanent_tuning": 4},
    ],
    3: [
        {"name": "Ethereal Resonance", "did_not_intercept_last_round": True},
        {"name": "Flowing Melody of the Clouds", "stacks_of_permanent_tuning": 6},
    ],
    4: [
        {"name": "Ethereal Resonance", "did_not_intercept_last_round": True},
        {"name": "Flowing Melody of the Clouds", "stacks_of_permanent_tuning": 6},
    ],
    5: [
        {"name": "Ethereal Resonance", "did_not_intercept_last_round": True},
        {"name": "Flowing Melody of the Clouds", "stacks_of_permanent_tuning": 6},
    ],
    6: [
        {"name": "Ethereal Resonance", "did_not_intercept_last_round": True},
        {"name": "Flowing Melody of the Clouds", "stacks_of_permanent_tuning": 6},
    ],
    7: [
        {"name": "Ethereal Resonance", "did_not_intercept_last_round": True},
        {"name": "Flowing Melody of the Clouds", "stacks_of_permanent_tuning": 6},
    ],
}


class Daiyan(DollCalculatorPage):
    """Page for Daiyan."""

    def __init__(self):
        super().__init__()

        self.doll: daiyan.Daiyan = daiyan.Daiyan()
        self.doll.set_fortification_level(FortificationLevel.SEGMENT06)
        self.doll_subtitle: str = """Single Target / Interception

            Sentinel / Physical"""
        self.dandegate_link: str = "https://www.dandegate.net/dolls/daiyan"
        self.doll_portrait: str = "resources/daiyan.webp"

    @override
    def update_doll_abilities(self) -> None:
        self.option_config: dict[str, dict[str, Any]] = {
            "Plucking Strings": {
                "fields": [
                    {
                        "key": "did_not_intercept_last_round",
                        "type": "checkbox",
                        "label": "Did not Intercept last round",
                        "default": True,
                    },
                ],
                "function": self.doll.plucking_strings.execute,
            },
            "Absolute Tuning": {
                "fields": [
                    {
                        "key": "did_not_intercept_last_round",
                        "type": "checkbox",
                        "label": "Did not Intercept last round",
                        "default": True,
                    },
                ],
                "function": self.doll.absolute_tuning.execute,
            },
            "Ethereal Resonance": {
                "fields": [
                    {
                        "key": "did_not_intercept_last_round",
                        "type": "checkbox",
                        "label": "Did not Intercept last round",
                        "default": True,
                    },
                ],
                "function": self.doll.ethereal_resonance.execute,
            },
            "Interception": {
                "fields": [
                    {
                        "key": "stacks_of_tuning",
                        "type": "select",
                        "options": [n for n in range(0, 11)],
                        "label": "Stacks of Tuning",
                        "default": 6,
                    },
                ],
                "function": self.doll.interception.execute,
            },
            "Flowing Melody of the Clouds": {
                "fields": [
                    {
                        "key": "stacks_of_permanent_tuning",
                        "type": "select",
                        "options": [n for n in range(0, 7)],
                        "label": "Stacks of Permanent Tuning",
                        "default": 6,
                    },
                ],
                "function": self.doll.flowing_melody_of_the_clouds.execute,
            },
        }

    @override
    def set_initial_values(self) -> None:
        self.doll.initial_stats.basic_attributes[StatType.ATTACK] = 3000
        self.doll.initial_stats.basic_attributes[StatType.CRIT_RATE] = 70
        self.doll.initial_stats.basic_attributes[StatType.CRIT_DAMAGE] = 182.8

        # imagoform, common keys
        self.doll.additive_modifiers.special_attributes[
            SpecialAttribute.DAMAGE_BOOST
        ].set_multiplier(DamageTag.ALL, 17)

        # weapon, attachments
        self.doll.additive_modifiers.special_attributes[
            SpecialAttribute.DAMAGE_BOOST
        ].set_multiplier(DamageTag.PHYSICAL, 26.4)

        self.doll.additive_modifiers.special_attributes[
            SpecialAttribute.DAMAGE_BOOST
        ].set_multiplier(DamageTag.INTERCEPTION, 8)

        self.doll.additive_modifiers.special_attributes[
            SpecialAttribute.CRITICAL_DAMAGE
        ].set_multiplier(DamageTag.PHYSICAL, 0.4)

        self.doll.additive_modifiers.special_attributes[
            SpecialAttribute.CRITICAL_DAMAGE
        ].set_multiplier(DamageTag.BOSS, 3)

        self.doll.additive_modifiers.special_attributes[
            SpecialAttribute.CRITICAL_DAMAGE
        ].set_multiplier(DamageTag.TARGETED, 5)

        self.doll.additive_modifiers.special_attributes[
            SpecialAttribute.CRITICAL_DAMAGE
        ].set_multiplier(DamageTag.ALL, 2.4)

        self.doll.additive_modifiers.special_attributes[
            SpecialAttribute.DEFENSE_IGNORE
        ].set_multiplier(DamageTag.PHYSICAL, 10)

        self.doll.multiplicative_modifiers.basic_attributes[StatType.ATTACK] = 14.6

    def get_default_damage_calculator_buffs(self) -> list[dict[str, Any]]:
        return [
            {"name": "Attack Up II"},
            {"name": "Never Give Up (Yoohee)", "stacks": 4},
            {"name": "Graceful Spin (Yoohee)"},
            {"name": "Preshow Warmup (Yoohee)"},
            {"name": "Tuning (Daiyan)", "stacks": 3},
            {"name": "Permanent Tuning (Daiyan)", "stacks": 6},
        ]

    def get_default_damage_calculator_debuffs(self) -> list[dict[str, Any]]:
        return [
            {"name": "Defense Down II"},
            {
                "name": "Precognition Foresight (Lainie)",
                "lainie_fortification_level": FortificationLevel.SEGMENT03,
            },
            {
                "name": "Precognition Awareness (Simulacrum)",
                "lainie_fortification_level": FortificationLevel.SEGMENT03,
            },
        ]

    @override
    def get_model_assumptions(self) -> list[ModelAssumption]:
        return [
            ModelAssumption(
                icon="key",
                description="Expansion Key - Flowing Melody of the Clouds Tiers 1 and 2 are active.",
            ),
            ModelAssumption(
                icon="layers",
                description="Sample rotation assumes Interception is never performed.",
            ),
            ModelAssumption(
                icon="wb_cloudy",
                description="The action Flowing Melody of the Clouds refers to the additional attack after the Ultimate granted by the Expansion Key (Tier 2).",
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
