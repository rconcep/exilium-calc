from nicegui import ui

from gui.templates.doll_calculator_page import DollCalculatorPage, ModelAssumption
from gui.templates.rotation_planner import RotationPlanner
from typing import Any, override
from core.types import StatType, FortificationLevel, SpecialAttribute, DamageTag
from core.dolls import ots_14

_t1: list[dict[str, Any]] = [
    {"name": "Total Suppression", "is_in_demolition_mode": False},
]

_t2: list[dict[str, Any]] = [
    {"name": "Critical Splash", "previous_uses": 0},
    {
        "name": "Overload Pulse",
        "accumulated_damage": 1800000,
        "uses_of_critical_splash": 0,
    },
    {"name": "Critical Splash", "previous_uses": 1},
    {
        "name": "Overload Pulse",
        "accumulated_damage": 1800000,
        "uses_of_critical_splash": 1,
    },
    {"name": "Critical Splash", "previous_uses": 2},
    {
        "name": "Overload Pulse",
        "accumulated_damage": 1800000,
        "uses_of_critical_splash": 2,
    },
    {"name": "Critical Splash", "previous_uses": 3},
    {
        "name": "Overload Pulse",
        "accumulated_damage": 1800000,
        "uses_of_critical_splash": 3,
    },
    {"name": "Critical Splash", "previous_uses": 4},
    {
        "name": "Overload Pulse",
        "accumulated_damage": 1800000,
        "uses_of_critical_splash": 4,
    },
    {"name": "Critical Splash", "previous_uses": 5},
    {
        "name": "Overload Pulse",
        "accumulated_damage": 1800000,
        "uses_of_critical_splash": 5,
    },
    {"name": "Critical Splash", "previous_uses": 6},
    {
        "name": "Overload Pulse",
        "accumulated_damage": 1800000,
        "uses_of_critical_splash": 6,
    },
]

sample_rotation: dict[int, list[dict]] = {
    1: _t1,
    2: _t1,
    3: _t1,
    4: _t1,
    5: _t1,
    6: _t1,
    7: _t2,
}


class OTs14(DollCalculatorPage):
    """Page for OTs-14."""

    def __init__(self):
        super().__init__()

        self.doll: ots_14.OTs14 = ots_14.OTs14()
        self.doll.set_fortification_level(FortificationLevel.SEGMENT06)
        self.doll_subtitle: str = """Burst / Fixed-Damage Follow-up

            Sentinel / Omni"""
        self.dandegate_link: str = "https://www.dandegate.net/dolls/ots-14"
        self.doll_portrait: str = "resources/ots-14.webp"

    @override
    def update_doll_abilities(self) -> None:
        self.option_config: dict[str, dict[str, Any]] = {
            "Combat Instinct": {
                "fields": [],
                "function": self.doll.combat_instinct.execute,
            },
            "Critical Splash": {
                "fields": [
                    {
                        "key": "previous_uses",
                        "type": "number",
                        "label": "Previous Critical Splash Uses",
                        "default": 0,
                    },
                ],
                "function": self.doll.critical_splash.execute,
            },
            "Overload Pulse": {
                "fields": [
                    {
                        "key": "accumulated_damage",
                        "type": "number",
                        "label": "Accumulated Damage",
                        "default": 0,
                    },
                    {
                        "key": "uses_of_critical_splash",
                        "type": "number",
                        "label": "Uses of Critical Splash",
                        "default": 0,
                    },
                ],
                "function": self.doll.overload_pulse.execute,
            },
            "Total Suppression": {
                "fields": [
                    {
                        "key": "is_in_demolition_mode",
                        "type": "checkbox",
                        "label": "Demolition Mode",
                        "default": True,
                    },
                ],
                "function": self.doll.total_suppression.execute,
            },
        }

    @override
    def set_initial_values(self) -> None:
        self.doll.initial_stats.basic_attributes[StatType.ATTACK] = 4400

        # Base + Universal Keys + Weapon Attachment
        self.doll.initial_stats.basic_attributes[StatType.CRIT_RATE] = 80

        # Base + Universal Keys + Signature Weapon + Weapon Attachment
        self.doll.initial_stats.basic_attributes[StatType.CRIT_DAMAGE] = 120 + 25 + 15
        self.doll.initial_stats.basic_attributes[StatType.HEALTH] = 4400

        # Attachments, common keys, imagoform, specialized traits

        # imagoform: 12
        # CQC elite: 0.4
        # Imagoform (Shoot): 4+3
        self.doll.additive_modifiers.special_attributes[
            SpecialAttribute.DAMAGE_BOOST
        ].set_multiplier(DamageTag.ALL, 12 + 0.4 + 4 + 3)

        # Imagoform (sprout): 5
        self.doll.additive_modifiers.special_attributes[
            SpecialAttribute.DAMAGE_BOOST
        ].set_multiplier(DamageTag.OMNI, 5)

        # Attachment: 20
        self.doll.additive_modifiers.special_attributes[
            SpecialAttribute.DAMAGE_BOOST
        ].set_multiplier(DamageTag.PHASE, 20)

        # Signature: 20
        # Imagoform (embryo): 8
        self.doll.additive_modifiers.special_attributes[
            SpecialAttribute.DAMAGE_BOOST
        ].set_multiplier(DamageTag.ACTIVE, 20 + 8)

        # Imagoform (shoot): 10
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

        # imagoform: 8
        # attack boost: 3.6
        # Support Imagoform: 3
        self.doll.multiplicative_modifiers.basic_attributes[StatType.ATTACK] = (
            8 + 3.6 + 3
        )

        # Common Key: 10
        self.doll.additive_modifiers.special_attributes[
            SpecialAttribute.DAMAGE_BOOST
        ].set_multiplier(DamageTag.FIXED, 10)

    @override
    def get_model_assumptions(self) -> list[ModelAssumption]:
        return [
            ModelAssumption(
                icon="warning",
                description="The base potency of the fixed damage from consuming Overload Pulse is implemented as the portion of accumulated damage stored. This causes it to be overrepresented in potency contexts compared to OTs-14's other abilities that scale with her attack.",
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
