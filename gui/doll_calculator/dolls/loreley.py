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
from core.dolls import loreley

_t1: list[dict[str, Any]] = [
    {"name": "Agony's Grace"},
    {"name": "Phosphor Pulse"},
    {"name": "Phosphor Pulse"},
    {
        "name": "Scorching Brand",
        "has_blazing_embers": False,
        "target_on_burn_tile": True,
    },
    {"name": "Phosphor Pulse"},
]

_t2: list[dict[str, Any]] = [
    {
        "name": "Crimson Binding Decree",
        "has_blazing_embers": False,
        "number_of_targets": 1,
        "number_of_burn_buffs": 4,
    },
    {"name": "Phosphor Pulse"},
    {
        "name": "Scorching Brand",
        "has_blazing_embers": True,
        "target_on_burn_tile": True,
    },
    {"name": "Phosphor Pulse"},
    {"name": "Phosphor Pulse"},
]

_t4: list[dict[str, Any]] = [
    {"name": "Agony's Grace"},
    {"name": "Phosphor Pulse"},
    {"name": "Phosphor Pulse"},
    {
        "name": "Scorching Brand",
        "has_blazing_embers": True,
        "target_on_burn_tile": True,
    },
    {"name": "Phosphor Pulse"},
]

sample_rotation: dict[int, list[dict]] = {
    1: _t1,
    2: _t2,
    3: _t2,
    4: _t4,
    5: _t2,
    6: _t2,
    7: _t4,
}


class Loreley(DollCalculatorPage):
    """Page for Loreley."""

    def __init__(self):
        super().__init__()

        self.doll = loreley.Loreley()
        self.doll.set_fortification_level(FortificationLevel.SEGMENT06)
        self.doll_subtitle: str = """AoE / Tile / Support

            Support / Burn"""
        self.dandegate_link: str = "https://www.dandegate.net/dolls/loreley"
        self.doll_portrait: str = "resources/loreley.webp"

    @override
    def update_doll_abilities(self) -> None:
        doll = cast(loreley.Loreley, self.doll)

        self.option_config: dict[str, dict[str, Any]] = {
            "Punishment Prelude": {
                "fields": [],
                "function": doll.punishment_prelude.execute,
            },
            "Scorching Brand": {
                "fields": [
                    {
                        "key": "has_blazing_embers",
                        "type": "checkbox",
                        "label": "Blazing Embers",
                        "default": True,
                    },
                    {
                        "key": "target_on_burn_tile",
                        "type": "checkbox",
                        "label": "Target on Burn tile",
                        "default": True,
                    },
                ],
                "function": doll.scorching_brand.execute,
            },
            "Crimson Binding Decree": {
                "fields": [
                    {
                        "key": "has_blazing_embers",
                        "type": "checkbox",
                        "label": "Blazing Embers",
                        "default": True,
                    },
                    {
                        "key": "number_of_targets",
                        "type": "number",
                        "label": "Number of targets",
                        "default": 1,
                    },
                    {
                        "key": "number_of_burn_buffs",
                        "type": "number",
                        "label": "Number of Burn buffs",
                        "default": 3,
                    },
                ],
                "function": doll.crimson_binding_decree.execute,
            },
            "Agony's Grace": {
                "fields": [],
                "function": doll.agonys_grace.execute,
            },
            "Phosphor Pulse": {
                "fields": [],
                "function": doll.phosphor_pulse.execute,
            },
        }

    @override
    def set_initial_values(self) -> None:
        doll = cast(loreley.Loreley, self.doll)

        doll.initial_stats.basic_attributes[StatType.ATTACK] = 3895
        doll.initial_stats.basic_attributes[StatType.HEALTH] = 4390
        doll.initial_stats.basic_attributes[StatType.CRIT_RATE] = 73.6
        doll.initial_stats.basic_attributes[StatType.CRIT_DAMAGE] = 135

        # Banshee's Whisper: 10 + 2.5
        # Key: 7
        # Key: 7
        # Imagoform Shoot: 4
        doll.additive_modifiers.special_attributes[
            SpecialAttribute.DAMAGE_BOOST
        ].set_multiplier(DamageTag.ALL, 30.5)

        # Banshee's Whisper: 10
        # Imagoform Embryo: 3
        # Imagoform Sprout: 5
        # Burn Unity: 0.9
        # Burn Boost: 0.8
        doll.additive_modifiers.special_attributes[
            SpecialAttribute.DAMAGE_BOOST
        ].set_multiplier(DamageTag.BURN, 19.7)

        # Attachment: 15
        doll.additive_modifiers.special_attributes[
            SpecialAttribute.DAMAGE_BOOST
        ].set_multiplier(DamageTag.PHASE, 15)

        # Pinpoint Specialization: 2.5
        doll.additive_modifiers.special_attributes[
            SpecialAttribute.DAMAGE_BOOST
        ].set_multiplier(DamageTag.TARGETED, 2.5)

        # Banshee's Whisper: 5
        doll.additive_modifiers.special_attributes[
            SpecialAttribute.DAMAGE_BOOST
        ].set_multiplier(DamageTag.SUPPORT_ACTION, 5)

        # Follow-up Strike: 0.5
        doll.additive_modifiers.special_attributes[
            SpecialAttribute.DAMAGE_BOOST
        ].set_multiplier(DamageTag.STABILITY_BROKEN, 0.5)

        # Burning Smite: 0.6
        doll.additive_modifiers.special_attributes[
            SpecialAttribute.CRITICAL_DAMAGE
        ].set_multiplier(DamageTag.BURN, 0.6)

        # Imagoform Bud: 4
        # Attack Unity: 1
        # Fighting Spirit: 1.8
        # Attack Boost: 2
        doll.multiplicative_modifiers.basic_attributes[StatType.ATTACK] = 6.8

        # Ichor Conversion: 0.4%
        doll.additive_modifiers.basic_attributes[StatType.ATTACK] = (
            0.004 * doll.initial_stats.basic_attributes[StatType.HEALTH]
        )

    def get_default_damage_calculator_buffs(self) -> list[dict[str, Any]]:
        return [
            {"name": "Blazing Assault II"},
            {
                "name": "Blazing Embers",
                "loreley_fortification_level": FortificationLevel.SEGMENT06,
                "stack": 6,
            },
            {
                "name": "Scorchflame (Loreley)",
                "loreley_fortification_level": FortificationLevel.SEGMENT06,
            },
        ]

    def get_default_damage_calculator_debuffs(self) -> list[dict[str, Any]]:
        return [
            {"name": "Defense Down II"},
            {"name": "Conflagration"},
            {"name": "Hunter-Type II"},
        ]

    @override
    def get_model_assumptions(self) -> list[ModelAssumption]:
        return [
            ModelAssumption(
                icon="local_fire_department",
                description="The damage boost and critical damage boost for each Phosphor Pulse triggered at V3+ is maxed.",
            ),
            ModelAssumption(
                icon="groups",
                description="The attack boost from Passive - Queen's Gift at V6 for each Burn-type Doll present is maxed out at 30%.",
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
