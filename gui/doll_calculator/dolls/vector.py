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
