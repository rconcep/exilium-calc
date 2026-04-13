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
from core.dolls import belka


_t1 = [
    {
        "name": "Leaping Arc",
        "mobility_expended": 10,
        "number_of_electric_debuffs_on_target": 2,
    },
    {"name": "Continual Release"},
    {"name": "Overflowing Electrons"},
]

_t2 = [
    {
        "name": "Crackling Core",
        "has_active_engagement": True,
        "mobility_expended": 10,
        "has_fixed_key_4": True,
        "target_has_negative_charge": True,
    },
    {"name": "Continual Release"},
    {
        "name": "Sylvan Vault",
        "has_active_engagement": True,
        "number_positive_charge_on_field": 5,
        "number_negative_charge_on_field": 1,
        "target_is_boss_with_negative_charge": True,
    },
    {"name": "Continual Release"},
]

_t4 = [
    {
        "name": "Crackling Core",
        "has_active_engagement": True,
        "mobility_expended": 10,
        "has_fixed_key_4": True,
        "target_has_negative_charge": True,
    },
    {
        "name": "Sylvan Vault",
        "has_active_engagement": True,
        "number_positive_charge_on_field": 5,
        "number_negative_charge_on_field": 1,
        "target_is_boss_with_negative_charge": True,
    },
]

sample_rotation: dict[int, list[dict]] = {
    1: _t1,
    2: _t2,
    3: _t2,
    4: _t4,
    5: _t1,
    6: _t2,
    7: _t2,
}


class Belka(DollCalculatorPage):
    """Page for Belka."""

    def __init__(self):
        super().__init__()

        self.doll = belka.Belka()
        self.doll.set_fortification_level(FortificationLevel.SEGMENT06)
        self.doll_subtitle: str = """Single Target Burst / Charge

            Vanguard / Electric"""
        self.dandegate_link: str = "https://www.dandegate.net/dolls/belka"
        self.doll_portrait: str = "resources/belka.webp"

    @override
    def update_doll_abilities(self) -> None:
        doll = cast(belka.Belka, self.doll)

        self.option_config: dict[str, dict[str, Any]] = {
            "Nutcracker Shell": {
                "fields": [
                    {
                        "key": "has_active_engagement",
                        "type": "checkbox",
                        "label": "Active Engagement",
                        "default": True,
                    },
                ],
                "function": doll.nutcracker_shell.execute,
            },
            "Crackling Core": {
                "fields": [
                    {
                        "key": "has_active_engagement",
                        "type": "checkbox",
                        "label": "Active Engagement",
                        "default": True,
                    },
                    {
                        "key": "mobility_expended",
                        "type": "number",
                        "label": "Mobility Expended",
                        "default": 10,
                    },
                    {
                        "key": "has_fixed_key_4",
                        "type": "checkbox",
                        "label": "Fixed Key 4 - Raised Tail",
                        "default": True,
                    },
                    {
                        "key": "target_has_negative_charge",
                        "type": "checkbox",
                        "label": "Target has Negative Charge",
                        "default": True,
                    },
                ],
                "function": doll.crackling_core.execute,
            },
            "Sylvan Vault": {
                "fields": [
                    {
                        "key": "has_active_engagement",
                        "type": "checkbox",
                        "label": "Active Engagement",
                        "default": True,
                    },
                    {
                        "key": "number_positive_charge_on_field",
                        "type": "select",
                        "label": "Positive Charges on Field",
                        "options": [n for n in range(6)],
                        "default": 5,
                    },
                    {
                        "key": "number_negative_charge_on_field",
                        "type": "select",
                        "label": "Negative Charges on Field",
                        "options": [n for n in range(6)],
                        "default": 1,
                    },
                    {
                        "key": "target_is_boss_with_negative_charge",
                        "type": "checkbox",
                        "label": "Target is a Boss with Negative Charge",
                        "default": True,
                    },
                ],
                "function": doll.sylvan_vault.execute,
            },
            "Leaping Arc": {
                "fields": [
                    {
                        "key": "mobility_expended",
                        "type": "number",
                        "label": "Mobility Expended",
                        "default": 10,
                    },
                    {
                        "key": "number_of_electric_debuffs_on_target",
                        "type": "select",
                        "label": "Electric Debuffs on Target",
                        "options": [n for n in range(5)],
                        "default": 2,
                    },
                ],
                "function": doll.leaping_arc.execute,
            },
            "Continual Release": {
                "fields": [],
                "function": doll.continual_release.execute,
            },
            "Overflowing Electrons": {
                "fields": [],
                "function": doll.overflowing_electrons.execute,
            },
        }

    @override
    def set_initial_values(self) -> None:
        doll = cast(belka.Belka, self.doll)

        doll.initial_stats.basic_attributes[StatType.ATTACK] = 4210
        doll.initial_stats.basic_attributes[StatType.CRIT_RATE] = 80
        doll.initial_stats.basic_attributes[StatType.CRIT_DAMAGE] = 150

        # Attachments, common keys, imagoform, specialized traits
        doll.additive_modifiers.special_attributes[
            SpecialAttribute.DAMAGE_BOOST
        ].set_multiplier(DamageTag.ALL, 7)

        doll.additive_modifiers.special_attributes[
            SpecialAttribute.DAMAGE_BOOST
        ].set_multiplier(DamageTag.ELECTRIC, 20)

        doll.additive_modifiers.special_attributes[
            SpecialAttribute.DAMAGE_BOOST
        ].set_multiplier(DamageTag.PHASE, 15)

        doll.additive_modifiers.special_attributes[
            SpecialAttribute.DAMAGE_BOOST
        ].set_multiplier(DamageTag.TARGETED, 2.5)

        doll.multiplicative_modifiers.basic_attributes[StatType.ATTACK] = 11

    def get_default_damage_calculator_buffs(self) -> list[dict[str, Any]]:
        return [
            {"name": "Attack Up II"},
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
            {
                "name": "Stored Charge (Belka)",
                "belka_fortification_level": FortificationLevel.SEGMENT06,
                "stacks": 10,
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
                description="Expansion Key - Squirrel's Awakening is active.",
                link_label="Dandegate",
                link_target="https://www.dandegate.net/dolls/belka/keys/expansion-key-squirrel-s-awakening",
            ),
            ModelAssumption(
                icon="bolt",
                description="Allies are assumed to have applied 6 stacks of Negative Charge, granting Belka the maximum +30% Critical Rate bonus from her passive. Additionally, the target is assumed to have Negative Charge.",
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
