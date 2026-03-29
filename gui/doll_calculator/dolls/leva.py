from nicegui import ui

from gui.templates.doll_calculator_page import DollCalculatorPage, ModelAssumption
from gui.templates.rotation_planner import RotationPlanner
from typing import Any, override
from core.types import (
    DamageTag,
    StatType,
    FortificationLevel,
    SpecialAttribute,
    ModifierType,
)
from core.dolls import leva


sample_rotation: dict[int, list[dict]] = {
    1: [
        {"name": "Emergency Support"},
        {"name": "Overclocking Strike", "excess_stability_damage": 8},
        {"name": "Emergency Support"},
        {"name": "Overclocking Strike", "excess_stability_damage": 8},
        {"name": "Emergency Support"},
        {"name": "Overclocking Strike", "excess_stability_damage": 8},
        {"name": "Emergency Support"},
        {"name": "Overclocking Strike", "excess_stability_damage": 8},
        {"name": "Quantum Calculation"},
        {"name": "Overclocking Strike", "excess_stability_damage": 8},
        {"name": "Superconductive Strike", "superconductive_code_consumed": 4},
        {"name": "Overclocking Strike", "excess_stability_damage": 15},
    ],
    2: [
        {"name": "Emergency Support"},
        {"name": "Overclocking Strike", "excess_stability_damage": 8},
        {"name": "Emergency Support"},
        {"name": "Overclocking Strike", "excess_stability_damage": 8},
        {"name": "Emergency Support"},
        {"name": "Overclocking Strike", "excess_stability_damage": 8},
        {"name": "Emergency Support"},
        {"name": "Overclocking Strike", "excess_stability_damage": 8},
        {"name": "Ordered Disruption", "target_has_negative_charge": True},
        {"name": "Overclocking Strike", "excess_stability_damage": 9},
        {"name": "Superconductive Strike", "superconductive_code_consumed": 4},
        {"name": "Overclocking Strike", "excess_stability_damage": 15},
    ],
    3: [
        {"name": "Emergency Support"},
        {"name": "Overclocking Strike", "excess_stability_damage": 8},
        {"name": "Emergency Support"},
        {"name": "Overclocking Strike", "excess_stability_damage": 8},
        {"name": "Emergency Support"},
        {"name": "Overclocking Strike", "excess_stability_damage": 8},
        {"name": "Emergency Support"},
        {"name": "Overclocking Strike", "excess_stability_damage": 8},
        {"name": "Quantum Calculation"},
        {"name": "Overclocking Strike", "excess_stability_damage": 8},
        {"name": "Superconductive Strike", "superconductive_code_consumed": 4},
        {"name": "Overclocking Strike", "excess_stability_damage": 15},
    ],
    4: [
        {"name": "Emergency Support"},
        {"name": "Overclocking Strike", "excess_stability_damage": 8},
        {"name": "Emergency Support"},
        {"name": "Overclocking Strike", "excess_stability_damage": 8},
        {"name": "Emergency Support"},
        {"name": "Overclocking Strike", "excess_stability_damage": 8},
        {"name": "Emergency Support"},
        {"name": "Overclocking Strike", "excess_stability_damage": 8},
        {"name": "Ordered Disruption", "target_has_negative_charge": True},
        {"name": "Overclocking Strike", "excess_stability_damage": 9},
        {"name": "Superconductive Strike", "superconductive_code_consumed": 4},
        {"name": "Overclocking Strike", "excess_stability_damage": 15},
    ],
    5: [
        {"name": "Emergency Support"},
        {"name": "Overclocking Strike", "excess_stability_damage": 8},
        {"name": "Emergency Support"},
        {"name": "Overclocking Strike", "excess_stability_damage": 8},
        {"name": "Emergency Support"},
        {"name": "Overclocking Strike", "excess_stability_damage": 8},
        {"name": "Emergency Support"},
        {"name": "Overclocking Strike", "excess_stability_damage": 8},
        {"name": "Quantum Calculation"},
        {"name": "Overclocking Strike", "excess_stability_damage": 8},
        {"name": "Superconductive Strike", "superconductive_code_consumed": 4},
        {"name": "Overclocking Strike", "excess_stability_damage": 15},
    ],
    6: [
        {"name": "Emergency Support"},
        {"name": "Overclocking Strike", "excess_stability_damage": 8},
        {"name": "Emergency Support"},
        {"name": "Overclocking Strike", "excess_stability_damage": 8},
        {"name": "Emergency Support"},
        {"name": "Overclocking Strike", "excess_stability_damage": 8},
        {"name": "Emergency Support"},
        {"name": "Overclocking Strike", "excess_stability_damage": 8},
        {"name": "Ordered Disruption", "target_has_negative_charge": True},
        {"name": "Overclocking Strike", "excess_stability_damage": 9},
        {"name": "Superconductive Strike", "superconductive_code_consumed": 4},
        {"name": "Overclocking Strike", "excess_stability_damage": 15},
    ],
    7: [
        {"name": "Emergency Support"},
        {"name": "Overclocking Strike", "excess_stability_damage": 8},
        {"name": "Emergency Support"},
        {"name": "Overclocking Strike", "excess_stability_damage": 8},
        {"name": "Emergency Support"},
        {"name": "Overclocking Strike", "excess_stability_damage": 8},
        {"name": "Emergency Support"},
        {"name": "Overclocking Strike", "excess_stability_damage": 8},
        {"name": "Quantum Calculation"},
        {"name": "Overclocking Strike", "excess_stability_damage": 8},
        {"name": "Superconductive Strike", "superconductive_code_consumed": 4},
        {"name": "Overclocking Strike", "excess_stability_damage": 15},
    ],
}


class Leva(DollCalculatorPage):
    """Page for Leva."""

    def __init__(self):
        super().__init__()

        self.doll: leva.Leva = leva.Leva()
        self.doll.set_fortification_level(FortificationLevel.SEGMENT06)
        self.doll_subtitle: str = """Single Target Burst / Break Conversion

            Sentinel / Electric"""
        self.dandegate_link: str = "https://www.dandegate.net/dolls/leva"
        self.doll_portrait: str = "resources/leva.webp"

    @override
    def update_doll_abilities(self) -> None:
        self.option_config: dict[str, dict[str, Any]] = {
            "Dangerous Smile": {
                "fields": [
                    {},
                ],
                "function": self.doll.dangerous_smile.execute,
            },
            "Rational Suppression": {
                "fields": [],
                "function": self.doll.rational_suppression.execute,
            },
            "Ordered Disruption": {
                "fields": [
                    {
                        "key": "target_has_negative_charge",
                        "type": "checkbox",
                        "label": "Target has Negative Charge",
                        "default": True,
                    },
                ],
                "function": self.doll.ordered_disruption.execute,
            },
            "Quantum Calculation": {
                "fields": [],
                "function": self.doll.quantum_calculation.execute,
            },
            "Superconductive Strike": {
                "fields": [
                    {
                        "key": "superconductive_code_consumed",
                        "type": "select",
                        "label": "Superconductive Code consumed",
                        "options": [n for n in range(1, 5)],
                        "default": 4,
                    },
                ],
                "function": self.doll.superconductive_strike.execute,
            },
            "Emergency Support": {
                "fields": [],
                "function": self.doll.emergency_support.execute,
            },
            "Overclocking Strike": {
                "fields": [
                    {
                        "key": "excess_stability_damage",
                        "type": "number",
                        "label": "Excess Stability Damage",
                        "default": 8,
                    },
                ],
                "function": self.doll.overclocking_strike.execute,
            },
        }

    @override
    def set_initial_values(self) -> None:
        self.doll.initial_stats.basic_attributes[StatType.ATTACK] = 4749
        self.doll.initial_stats.basic_attributes[StatType.CRIT_RATE] = 99.5
        self.doll.initial_stats.basic_attributes[StatType.CRIT_DAMAGE] = 154.5

        # Attachments, common keys, imagoform, specialized traits
        self.doll.additive_modifiers.special_attributes[
            SpecialAttribute.DAMAGE_BOOST
        ].set_multiplier(DamageTag.ELECTRIC, 78.9)
        self.doll.additive_modifiers.special_attributes[
            SpecialAttribute.DAMAGE_BOOST
        ].set_multiplier(DamageTag.PHASE, 20)
        self.doll.additive_modifiers.special_attributes[
            SpecialAttribute.DAMAGE_BOOST
        ].set_multiplier(DamageTag.STABILITY_BROKEN, 21)
        self.doll.additive_modifiers.special_attributes[
            SpecialAttribute.DAMAGE_BOOST
        ].set_multiplier(DamageTag.ALL, 17.4)
        self.doll.additive_modifiers.special_attributes[
            SpecialAttribute.DAMAGE_BOOST
        ].set_multiplier(DamageTag.BOSS, 5.5)

        self.doll.additive_modifiers.special_attributes[
            SpecialAttribute.CRITICAL_DAMAGE
        ].set_multiplier(DamageTag.BOSS, 5)
        self.doll.additive_modifiers.special_attributes[
            SpecialAttribute.CRITICAL_DAMAGE
        ].set_multiplier(DamageTag.ELECTRIC, 0.4)

        # Imagoform
        self.doll.multiplicative_modifiers.basic_attributes[StatType.ATTACK] = 11.6

    @override
    def get_model_assumptions(self) -> list[ModelAssumption]:
        return [
            ModelAssumption(
                icon="bolt",
                description="Leva is assumed to have Positive Charge for the purpose of her passive. At V6, she is also assumed to have reached 4 stacks of Superconductive Code.",
            ),
            ModelAssumption(
                icon="key",
                description="Expansion Key - Electric Espionage is active. It is assumed that there are 5 Electric Dolls on the field and that she is attacking a target with Negative Charge in Stability Break.",
                link_label="Dandegate",
                link_target="https://www.dandegate.net/dolls/leva/keys/expansion-key-phantom-electric-spy",
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
