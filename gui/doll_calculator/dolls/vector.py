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
from core.dolls import vector
from core.combat import Overburn


sample_rotation: dict[int, list[dict]] = {
    1: [
        {"name": "Searing Finale"},
        {"name": "Dead End Meltdown"},
        {"name": "Dead End Meltdown (Fixed)"},
        {"name": "Emergency Support"},
        {"name": "Emergency Support"},
        {"name": "Emergency Support"},
        {"name": "Overheat Combustion"},
        {"name": "Overheat Combustion"},
        {"name": "Overburn"},
        {"name": "Overburn"},
    ],
    2: [
        {"name": "Portent of Doom"},
        {"name": "Emergency Support"},
        {"name": "Emergency Support"},
        {"name": "Emergency Support"},
        {"name": "Overheat Combustion"},
        {"name": "Overheat Combustion"},
        {"name": "Overburn"},
    ],
    3: [
        {"name": "Searing Finale"},
        {"name": "Dead End Meltdown"},
        {"name": "Dead End Meltdown (Fixed)"},
        {"name": "Emergency Support"},
        {"name": "Emergency Support"},
        {"name": "Emergency Support"},
        {"name": "Overheat Combustion"},
        {"name": "Overheat Combustion"},
        {"name": "Overburn"},
        {"name": "Overburn"},
    ],
    4: [
        {"name": "Portent of Doom"},
        {"name": "Emergency Support"},
        {"name": "Emergency Support"},
        {"name": "Emergency Support"},
        {"name": "Overheat Combustion"},
        {"name": "Overheat Combustion"},
        {"name": "Overburn"},
    ],
    5: [
        {"name": "Searing Finale"},
        {"name": "Dead End Meltdown"},
        {"name": "Dead End Meltdown (Fixed)"},
        {"name": "Emergency Support"},
        {"name": "Emergency Support"},
        {"name": "Emergency Support"},
        {"name": "Overheat Combustion"},
        {"name": "Overheat Combustion"},
        {"name": "Overburn"},
        {"name": "Overburn"},
    ],
    6: [
        {"name": "Portent of Doom"},
        {"name": "Emergency Support"},
        {"name": "Emergency Support"},
        {"name": "Emergency Support"},
        {"name": "Overheat Combustion"},
        {"name": "Overheat Combustion"},
        {"name": "Overburn"},
    ],
    7: [
        {"name": "Searing Finale"},
        {"name": "Dead End Meltdown"},
        {"name": "Dead End Meltdown (Fixed)"},
        {"name": "Emergency Support"},
        {"name": "Emergency Support"},
        {"name": "Emergency Support"},
        {"name": "Overheat Combustion"},
        {"name": "Overheat Combustion"},
        {"name": "Overburn"},
        {"name": "Overburn"},
    ],
}


class Vector(DollCalculatorPage):
    """Page for Vector."""

    def __init__(self):
        super().__init__()

        self.doll = vector.Vector()
        self.doll.set_fortification_level(FortificationLevel.SEGMENT06)
        self.doll_subtitle: str = """Fixed Damage / Tile / Buff

            Support / Burn"""
        self.dandegate_link: str = "https://www.dandegate.net/dolls/vector"
        self.doll_portrait: str = "resources/vector.webp"

    @override
    def update_doll_abilities(self) -> None:
        doll = cast(vector.Vector, self.doll)

        self.option_config: dict[str, dict[str, Any]] = {
            "Depressive Mentality": {
                "fields": [],
                "function": doll.depressive_mentality.execute,
            },
            "Dead End Meltdown": {
                "fields": [],
                "function": doll.dead_end_meltdown.execute,
            },
            "Dead End Meltdown (Fixed)": {
                "fields": [],
                "function": doll.dead_end_meltdown_fixed.execute,
            },
            "Portent of Doom": {
                "fields": [],
                "function": doll.portent_of_doom.execute,
            },
            "Searing Finale": {
                "fields": [],
                "function": doll.searing_finale.execute,
            },
            "Emergency Support": {
                "fields": [],
                "function": doll.emergency_support.execute,
            },
            "Overheat Combustion": {
                "fields": [],
                "function": doll.overheat_combustion.execute,
            },
            "Overburn": {
                "fields": [],
                "function": Overburn().execute,
            },
        }

    @override
    def set_initial_values(self) -> None:
        doll = cast(vector.Vector, self.doll)

        doll.initial_stats.basic_attributes[StatType.ATTACK] = 3895
        doll.initial_stats.basic_attributes[StatType.CRIT_RATE] = 73.6
        doll.initial_stats.basic_attributes[StatType.CRIT_DAMAGE] = 135

        # Attachments, common keys, imagoform, specialized traits
        doll.additive_modifiers.special_attributes[
            SpecialAttribute.DAMAGE_BOOST
        ].set_multiplier(DamageTag.ALL, 7)

        doll.additive_modifiers.special_attributes[
            SpecialAttribute.DAMAGE_BOOST
        ].set_multiplier(DamageTag.BURN, 20)

        doll.additive_modifiers.special_attributes[
            SpecialAttribute.DAMAGE_BOOST
        ].set_multiplier(DamageTag.PHASE, 15)

        doll.additive_modifiers.special_attributes[
            SpecialAttribute.DAMAGE_BOOST
        ].set_multiplier(DamageTag.PASSIVE, 10)

        doll.additive_modifiers.special_attributes[
            SpecialAttribute.DAMAGE_BOOST
        ].set_multiplier(DamageTag.SUPPORT_ACTION, 10)

        doll.additive_modifiers.special_attributes[
            SpecialAttribute.CRITICAL_DAMAGE
        ].set_multiplier(DamageTag.ALL, 3)

        doll.multiplicative_modifiers.basic_attributes[StatType.ATTACK] = 7

    def get_default_damage_calculator_buffs(self) -> list[dict[str, Any]]:
        return [
            {"name": "Blazing Assault II"},
            {
                "name": "Accelerant (Vector)",
                "vector_fortification_level": FortificationLevel.SEGMENT06,
                "number_of_burn_buffs": 3,
            },
            {
                "name": "Apathetic Resistance (Vector)",
                "vector_fortification_level": FortificationLevel.SEGMENT06,
            },
        ]

    def get_default_damage_calculator_debuffs(self) -> list[dict[str, Any]]:
        return [
            {"name": "Defense Down II"},
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
                description="Sample rotation assumes Expansion Key - Depression Empathy is active.",
                link_label="Dandegate",
                link_target="https://www.dandegate.net/dolls/vector/keys/expansion-key-depression-empathy",
            ),
            ModelAssumption(
                icon="local_fire_department",
                description="The attack buff conditional on having maximum/excess Confectance Index from the passive Perception Block is active.",
                link_label="Dandegate",
                link_target="https://www.dandegate.net/dolls/vector/skills/perception-block",
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
