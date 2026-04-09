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
from core.dolls import jiangyu


sample_rotation: dict[int, list[dict]] = {
    1: [
        {"name": "Thunderclap"},
        {"name": "Rolling Thunder"},
        {"name": "Interception"},
        {"name": "Interception"},
        {"name": "Support Action", "target_is_in_stability_break": False},
        {"name": "Support Action", "target_is_in_stability_break": False},
        {"name": "Support Action", "target_is_in_stability_break": False},
        {"name": "Urge to Perform"},
    ],
    2: [
        {"name": "Lightning Smash"},
        {"name": "Lightning Smash"},
        {"name": "Interception"},
        {"name": "Interception"},
        {"name": "Support Action", "target_is_in_stability_break": True},
        {"name": "Support Action", "target_is_in_stability_break": True},
        {"name": "Support Action", "target_is_in_stability_break": True},
    ],
    3: [
        {"name": "Thunderclap"},
        {"name": "Rolling Thunder"},
        {"name": "Interception"},
        {"name": "Interception"},
        {"name": "Support Action", "target_is_in_stability_break": False},
        {"name": "Support Action", "target_is_in_stability_break": False},
        {"name": "Support Action", "target_is_in_stability_break": False},
        {"name": "Urge to Perform"},
    ],
    4: [
        {"name": "Lightning Smash"},
        {"name": "Lightning Smash"},
        {"name": "Interception"},
        {"name": "Interception"},
        {"name": "Support Action", "target_is_in_stability_break": True},
        {"name": "Support Action", "target_is_in_stability_break": True},
        {"name": "Support Action", "target_is_in_stability_break": True},
    ],
    5: [
        {"name": "Thunderclap"},
        {"name": "Rolling Thunder"},
        {"name": "Interception"},
        {"name": "Interception"},
        {"name": "Support Action", "target_is_in_stability_break": False},
        {"name": "Support Action", "target_is_in_stability_break": False},
        {"name": "Support Action", "target_is_in_stability_break": False},
        {"name": "Urge to Perform"},
    ],
    6: [
        {"name": "Lightning Smash"},
        {"name": "Lightning Smash"},
        {"name": "Interception"},
        {"name": "Interception"},
        {"name": "Support Action", "target_is_in_stability_break": True},
        {"name": "Support Action", "target_is_in_stability_break": True},
        {"name": "Support Action", "target_is_in_stability_break": True},
    ],
    7: [
        {"name": "Thunderclap"},
        {"name": "Rolling Thunder"},
        {"name": "Interception"},
        {"name": "Interception"},
        {"name": "Support Action", "target_is_in_stability_break": False},
        {"name": "Support Action", "target_is_in_stability_break": False},
        {"name": "Support Action", "target_is_in_stability_break": False},
        {"name": "Urge to Perform"},
    ],
}


class Jiangyu(DollCalculatorPage):
    """Page for Jiangyu."""

    def __init__(self):
        super().__init__()

        self.doll = jiangyu.Jiangyu()
        self.doll.set_fortification_level(FortificationLevel.SEGMENT06)
        self.doll_subtitle: str = """Stability DMG / Mapwide Buffs / Assist

            Support / Electric"""
        self.dandegate_link: str = "https://www.dandegate.net/dolls/jiangyu"
        self.doll_portrait: str = "resources/jiangyu.webp"

    @override
    def update_doll_abilities(self) -> None:
        doll = cast(jiangyu.Jiangyu, self.doll)

        self.option_config: dict[str, dict[str, Any]] = {
            "Form Intention Fist": {
                "fields": [],
                "function": doll.form_intention_fist.execute,
            },
            "Thunderclap": {
                "fields": [],
                "function": doll.thunderclap.execute,
            },
            "Lightning Smash": {
                "fields": [],
                "function": doll.lightning_smash.execute,
            },
            "Rolling Thunder": {
                "fields": [],
                "function": doll.rolling_thunder.execute,
            },
            "Interception": {
                "fields": [],
                "function": doll.interception.execute,
            },
            "Support Action": {
                "fields": [
                    {
                        "key": "target_is_in_stability_break",
                        "type": "checkbox",
                        "label": "Target is in Stability Break",
                        "default": True,
                    },
                ],
                "function": doll.support_action.execute,
            },
            "Urge to Perform": {
                "fields": [],
                "function": doll.urge_to_perform.execute,
            },
        }

    @override
    def set_initial_values(self) -> None:
        self.doll.initial_stats.basic_attributes[StatType.ATTACK] = 3821
        self.doll.initial_stats.basic_attributes[StatType.HEALTH] = 4881
        self.doll.initial_stats.basic_attributes[StatType.CRIT_RATE] = 94.5
        self.doll.initial_stats.basic_attributes[StatType.CRIT_DAMAGE] = 179.5

        # Key: 7
        # Imagoform - Shoot: 4
        self.doll.additive_modifiers.special_attributes[
            SpecialAttribute.DAMAGE_BOOST
        ].set_multiplier(DamageTag.ALL, 11)

        # Leaping Tiger: 5
        # Attachments: 20
        # Andoris Aglaea: 10
        # Imagoform - Embryo: 3
        # Imagoform - Sprout: 5
        self.doll.additive_modifiers.special_attributes[
            SpecialAttribute.DAMAGE_BOOST
        ].set_multiplier(DamageTag.ELECTRIC, 43)

        # Leaping Tiger: 10 + 6*2
        # Key: 10
        self.doll.additive_modifiers.special_attributes[
            SpecialAttribute.DAMAGE_BOOST
        ].set_multiplier(DamageTag.PHASE, 32)

        # Key: 10
        # Follow-up Strike: 1
        self.doll.additive_modifiers.special_attributes[
            SpecialAttribute.DAMAGE_BOOST
        ].set_multiplier(DamageTag.STABILITY_BROKEN, 11)

        # Smite Boost: 4
        self.doll.additive_modifiers.special_attributes[
            SpecialAttribute.CRITICAL_DAMAGE
        ].set_multiplier(DamageTag.ALL, 4)

        # Electric Smite: 1
        self.doll.additive_modifiers.special_attributes[
            SpecialAttribute.CRITICAL_DAMAGE
        ].set_multiplier(DamageTag.ELECTRIC, 1)

        # Imagoform - Bud: 4
        # Attack Unity: 1
        # Fighting Spirit: 1.8
        self.doll.multiplicative_modifiers.basic_attributes[StatType.ATTACK] = 6.8

        # Ichor Conversion: 0.8% of Initial Max HP
        self.doll.additive_modifiers.basic_attributes[StatType.ATTACK] = (
            0.008 * self.doll.initial_stats.basic_attributes[StatType.HEALTH]
        )

    def get_default_damage_calculator_buffs(self) -> list[dict[str, Any]]:
        return [
            {"name": "Attack Up II"},
            {
                "name": "Chi (Jiangyu)",
                "jiangyu_fortification_level": FortificationLevel.SEGMENT06,
            },
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
        ]

    def get_default_damage_calculator_debuffs(self) -> list[dict[str, Any]]:
        return [
            {"name": "Defense Down II"},
            {
                "name": "Voltage Sag",
                "stacks": 3,
                "jiangyu_fortification_level": FortificationLevel.SEGMENT06,
            },
        ]

    @override
    def get_model_assumptions(self) -> list[ModelAssumption]:
        return [
            ModelAssumption(
                icon="key",
                description="Expansion Key - Urge to Perform is active.",
                link_label="Dandegate",
                link_target="https://www.dandegate.net/dolls/jiangyu/keys/expansion-key-urge-to-perform",
            ),
            ModelAssumption(
                icon="bolt",
                description="Lightning Smash assumes the target has Voltage Sag.",
            ),
            ModelAssumption(
                icon="sports_kabaddi",
                description="Sample rotation assumes Stability Break on odd turns and all Support Actions/Interceptions are activated.",
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
