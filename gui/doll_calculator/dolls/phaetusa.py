from typing import Any, cast, override

from nicegui import ui

from core.dolls import phaetusa
from core.types import DamageTag, FortificationLevel, SpecialAttribute, StatType
from gui.templates.doll_calculator_page import DollCalculatorPage, ModelAssumption
from gui.templates.rotation_planner import RotationPlanner


sample_rotation: dict[int, list[dict[str, Any]]] = {
    1: [
        {
            "name": "Twofold Rapture",
            "has_blood_oath": True,
            "stacks_of_blade_resonance": 1,
        },
        {
            "name": "Lacerating Wound",
            "original_damage_instance_potency": 680,
        },
        {"name": "Support Action"},
        {
            "name": "Lacerating Wound",
            "original_damage_instance_potency": 120,
        },
        {"name": "Support Action"},
        {
            "name": "Lacerating Wound",
            "original_damage_instance_potency": 120,
        },
        {"name": "Support Action"},
        {
            "name": "Lacerating Wound",
            "original_damage_instance_potency": 120,
        },
    ],
    2: [
        {
            "name": "Twofold Rapture",
            "has_blood_oath": True,
            "stacks_of_blade_resonance": 2,
        },
        {
            "name": "Lacerating Wound",
            "original_damage_instance_potency": 1080,
        },
        {"name": "Support Action"},
        {
            "name": "Lacerating Wound",
            "original_damage_instance_potency": 120,
        },
        {"name": "Support Action"},
        {
            "name": "Lacerating Wound",
            "original_damage_instance_potency": 120,
        },
        {"name": "Support Action"},
        {
            "name": "Lacerating Wound",
            "original_damage_instance_potency": 120,
        },
    ],
    3: [
        {
            "name": "Dual-Winged Descent",
            "has_blood_oath": False,
        },
        {"name": "Support Action"},
        {
            "name": "Lacerating Wound",
            "original_damage_instance_potency": 120,
        },
        {"name": "Support Action"},
        {
            "name": "Lacerating Wound",
            "original_damage_instance_potency": 120,
        },
        {"name": "Support Action"},
        {
            "name": "Lacerating Wound",
            "original_damage_instance_potency": 120,
        },
    ],
    4: [
        {
            "name": "Twofold Rapture",
            "has_blood_oath": True,
            "stacks_of_blade_resonance": 3,
        },
        {
            "name": "Lacerating Wound",
            "original_damage_instance_potency": 1520,
        },
        {"name": "Support Action"},
        {
            "name": "Lacerating Wound",
            "original_damage_instance_potency": 120,
        },
        {"name": "Support Action"},
        {
            "name": "Lacerating Wound",
            "original_damage_instance_potency": 120,
        },
        {"name": "Support Action"},
        {
            "name": "Lacerating Wound",
            "original_damage_instance_potency": 120,
        },
    ],
    5: [
        {
            "name": "Twofold Rapture",
            "has_blood_oath": True,
            "stacks_of_blade_resonance": 2,
        },
        {
            "name": "Lacerating Wound",
            "original_damage_instance_potency": 1080,
        },
        {"name": "Support Action"},
        {
            "name": "Lacerating Wound",
            "original_damage_instance_potency": 120,
        },
        {"name": "Support Action"},
        {
            "name": "Lacerating Wound",
            "original_damage_instance_potency": 120,
        },
        {"name": "Support Action"},
        {
            "name": "Lacerating Wound",
            "original_damage_instance_potency": 120,
        },
    ],
    6: [
        {
            "name": "Dual-Winged Descent",
            "has_blood_oath": False,
        },
        {"name": "Support Action"},
        {
            "name": "Lacerating Wound",
            "original_damage_instance_potency": 120,
        },
        {"name": "Support Action"},
        {
            "name": "Lacerating Wound",
            "original_damage_instance_potency": 120,
        },
        {"name": "Support Action"},
        {
            "name": "Lacerating Wound",
            "original_damage_instance_potency": 120,
        },
    ],
    7: [
        {
            "name": "Twofold Rapture",
            "has_blood_oath": True,
            "stacks_of_blade_resonance": 3,
        },
        {
            "name": "Lacerating Wound",
            "original_damage_instance_potency": 1520,
        },
        {"name": "Support Action"},
        {
            "name": "Lacerating Wound",
            "original_damage_instance_potency": 120,
        },
        {"name": "Support Action"},
        {
            "name": "Lacerating Wound",
            "original_damage_instance_potency": 120,
        },
        {"name": "Support Action"},
        {
            "name": "Lacerating Wound",
            "original_damage_instance_potency": 120,
        },
    ],
}


class Phaetusa(DollCalculatorPage):
    """Page for Phaetusa."""

    def __init__(self):
        super().__init__()

        self.doll = phaetusa.Phaetusa()
        self.doll.set_fortification_level(FortificationLevel.SEGMENT06)
        self.doll_subtitle: str = """Blade Combo / Corrosion Damage / Follow-up

            Sentinel / Corrosion"""
        self.dandegate_link: str = "https://www.dandegate.net/dolls/phaetusa"
        self.doll_portrait: str = "resources/phaetusa.webp"

    @override
    def update_doll_abilities(self) -> None:
        doll = cast(phaetusa.Phaetusa, self.doll)

        self.option_config = {
            "One Strike, Two Cuts": {
                "fields": [
                    {
                        "key": "has_blood_oath",
                        "type": "checkbox",
                        "label": "Blood Oath active",
                        "default": False,
                    },
                ],
                "function": doll.one_strike_two_cuts.execute,
            },
            "Dual-Winged Descent": {
                "fields": [
                    {
                        "key": "has_blood_oath",
                        "type": "checkbox",
                        "label": "Blood Oath active",
                        "default": False,
                    },
                ],
                "function": doll.dual_winged_descent.execute,
            },
            "Twofold Rapture": {
                "fields": [
                    {
                        "key": "has_blood_oath",
                        "type": "checkbox",
                        "label": "Blood Oath active",
                        "default": True,
                    },
                    {
                        "key": "stacks_of_blade_resonance",
                        "type": "select",
                        "label": "Blade Resonance stacks",
                        "default": 3,
                        "options": [n for n in range(4)],
                    },
                ],
                "function": doll.twofold_rapture.execute,
            },
            "Support Action": {
                "fields": [],
                "function": doll.support_action.execute,
            },
            "Lacerating Wound": {
                "fields": [
                    {
                        "key": "original_damage_instance_potency",
                        "type": "number",
                        "label": "Original Damage Potency",
                        "default": 120,
                    },
                ],
                "function": doll.lacerating_wound.execute,
            },
        }

    @override
    def set_initial_values(self) -> None:
        doll = cast(phaetusa.Phaetusa, self.doll)

        doll.initial_stats.basic_attributes[StatType.ATTACK] = 4700
        doll.initial_stats.basic_attributes[StatType.CRIT_RATE] = 80
        doll.initial_stats.basic_attributes[StatType.CRIT_DAMAGE] = 150

        doll.additive_modifiers.special_attributes[
            SpecialAttribute.DAMAGE_BOOST
        ].set_multiplier(DamageTag.ALL, 32)
        doll.additive_modifiers.special_attributes[
            SpecialAttribute.DAMAGE_BOOST
        ].set_multiplier(DamageTag.MELEE, 36)
        doll.additive_modifiers.special_attributes[
            SpecialAttribute.DAMAGE_BOOST
        ].set_multiplier(DamageTag.CORROSION, 15)

    def get_default_damage_calculator_buffs(self) -> list[dict[str, Any]]:
        return [
            {"name": "Attack Up II"},
            {
                "name": "Reversion (Phaetusa)",
                "phaetusa_fortification_level": FortificationLevel.SEGMENT06,
            },
            {
                "name": "Overwrite Trap (Phaetusa)",
                "uses_of_replication_trap": 6,
                "phaetusa_fortification_level": FortificationLevel.SEGMENT06,
            },
            {
                "name": "Dream Guardian",
            },
            {
                "name": "Nightmare Form",
                "mechty_fortification_level": FortificationLevel.SEGMENT06,
            },
        ]

    def get_default_damage_calculator_debuffs(self) -> list[dict[str, Any]]:
        return [
            {"name": "Defense Down II"},
            {
                "name": "Corrosive Infusion (Klukai)",
                "stacks": 15,
                "klukai_fortification_level": FortificationLevel.SEGMENT06,
            },
            {"name": "Toxin Inundation"},
            {"name": "Acid Corrosion II"},
        ]

    @override
    def get_model_assumptions(self) -> list[ModelAssumption]:
        return [
            ModelAssumption(
                icon="content_cut",
                description="Lacerating Wound is modeled as 40% of the configured original potency.",
            ),
            ModelAssumption(
                icon="content_cut",
                description="Sample rotation assumes all Support Actions are used each turn and that Synchrony is used after the uses of Overwrite Trap that generate an additional stack of Blade Resonance to gain Reversion from Synchrony.",
            ),
        ]

    @override
    def get_rotation_planner(self) -> None:
        with ui.card().classes("w-full h-full"):

            def update_all():
                self.damage_instances = self.rotation_planner.get_all_actions()
                self.stats_update_callback(None)  # type: ignore

            ui.button("Update", on_click=update_all).classes("w-full")
            self.rotation_planner = RotationPlanner(options_config=self.option_config)
            self.rotation_planner.set_data(sample_rotation)
