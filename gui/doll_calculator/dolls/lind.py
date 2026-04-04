from typing import Any, override
from core.types import DamageTag, FortificationLevel, SpecialAttribute, StatType
from core.dolls import lind
from gui.templates.doll_calculator_page import DollCalculatorPage, ModelAssumption
from gui.templates.rotation_planner import RotationPlanner
from nicegui import ui

sample_rotation: dict[int, list[dict]] = {
    1: [
        {
            "name": "Overwhelming Burst",
            "has_fixed_key_4": True,
            "is_confectance_index_at_maximum": True,
            "stacks_of_candyglaze": 10,
            "is_glucose_overload_followup": True,
        },
        {
            "name": "Honeytrap",
        },
    ],
    2: [
        {
            "name": "Overwhelming Burst",
            "has_fixed_key_4": True,
            "is_confectance_index_at_maximum": True,
            "stacks_of_candyglaze": 20,
            "is_glucose_overload_followup": True,
        },
        {
            "name": "Honeytrap",
        },
    ],
    3: [
        {
            "name": "Overwhelming Burst",
            "has_fixed_key_4": True,
            "is_confectance_index_at_maximum": True,
            "stacks_of_candyglaze": 30,
            "is_glucose_overload_followup": True,
        },
        {
            "name": "Honeytrap",
        },
    ],
    4: [
        {
            "name": "Overwhelming Burst",
            "has_fixed_key_4": True,
            "is_confectance_index_at_maximum": True,
            "stacks_of_candyglaze": 30,
            "is_glucose_overload_followup": True,
        },
        {
            "name": "Honeytrap",
        },
    ],
    5: [
        {
            "name": "Overwhelming Burst",
            "has_fixed_key_4": True,
            "is_confectance_index_at_maximum": True,
            "stacks_of_candyglaze": 30,
            "is_glucose_overload_followup": True,
        },
        {
            "name": "Honeytrap",
        },
    ],
    6: [
        {
            "name": "Overwhelming Burst",
            "has_fixed_key_4": True,
            "is_confectance_index_at_maximum": True,
            "stacks_of_candyglaze": 30,
            "is_glucose_overload_followup": True,
        },
        {
            "name": "Honeytrap",
        },
    ],
    7: [
        {
            "name": "Overwhelming Burst",
            "has_fixed_key_4": True,
            "is_confectance_index_at_maximum": True,
            "stacks_of_candyglaze": 30,
            "is_glucose_overload_followup": True,
        },
        {
            "name": "Honeytrap",
        },
    ],
}


class Lind(DollCalculatorPage):
    """Page for Lind."""

    def __init__(self):
        super().__init__()

        self.doll: lind.Lind = lind.Lind()
        self.doll.set_fortification_level(FortificationLevel.SEGMENT05)
        self.doll_subtitle: str = """AoE Damage / Debuff / Trigger / Stack

            Supporter / Shotgun"""
        self.dandegate_link: str = "https://www.dandegate.net/dolls/lind"
        self.doll_portrait: str = "resources/lind.webp"

    @override
    def update_doll_abilities(self) -> None:
        self.option_config: dict[str, dict[str, Any]] = {
            "Repulsive Shot": {
                "fields": [
                    {
                        "key": "is_glucose_overload_followup",
                        "type": "checkbox",
                        "label": "Glucose Overload Followup",
                        "default": False,
                    },
                ],
                "function": self.doll.repulsive_shot.execute,
            },
            "Assault Spray": {
                "fields": [
                    {
                        "key": "number_of_debuffs_on_target",
                        "type": "select",
                        "options": [n for n in range(0, 7)],
                        "label": "Debuffs on Target",
                        "default": 6,
                    },
                    {
                        "key": "is_glucose_overload_followup",
                        "type": "checkbox",
                        "label": "Glucose Overload Followup",
                        "default": True,
                    },
                ],
                "function": self.doll.assault_spray.execute,
            },
            "Overwhelming Burst": {
                "fields": [
                    {
                        "key": "has_fixed_key_4",
                        "type": "checkbox",
                        "label": "Fixed Key 4 - Civilized Judgement",
                        "default": True,
                    },
                    {
                        "key": "is_confectance_index_at_maximum",
                        "type": "checkbox",
                        "label": "Confectance Index at Maximum",
                        "default": True,
                    },
                    {
                        "key": "stacks_of_candyglaze",
                        "type": "select",
                        "options": [n for n in range(0, 31)],
                        "label": "Candyglaze Stacks",
                        "default": 30,
                    },
                    {
                        "key": "is_glucose_overload_followup",
                        "type": "checkbox",
                        "label": "Glucose Overload Followup",
                        "default": True,
                    },
                ],
                "function": self.doll.overwhelming_burst.execute,
            },
            "Honeytrap": {
                "fields": [],
                "function": self.doll.honeytrap.execute,
            },
        }

    @override
    def set_initial_values(self) -> None:
        self.doll.initial_stats.basic_attributes[StatType.ATTACK] = 4700
        self.doll.initial_stats.basic_attributes[StatType.CRIT_RATE] = 90.0
        self.doll.initial_stats.basic_attributes[StatType.CRIT_DAMAGE] = 175.0

        # Preset build assumptions (attachments, keys, imagoform, and traits).
        # ALL damage boost from equipment and passive abilities
        self.doll.additive_modifiers.special_attributes[
            SpecialAttribute.DAMAGE_BOOST
        ].set_multiplier(DamageTag.ALL, 60)

        # CORROSION damage boost from specialized attachments/traits
        self.doll.additive_modifiers.special_attributes[
            SpecialAttribute.DAMAGE_BOOST
        ].set_multiplier(DamageTag.CORROSION, 55)

        # Attack multiplier from team composition
        self.doll.multiplicative_modifiers.basic_attributes[StatType.ATTACK] = 11.6

    def get_default_damage_calculator_buffs(self) -> list[dict[str, Any]]:
        """Returns curated buff selections used to pre-populate the Damage Calculator."""
        return [
            {
                "name": "Candyglaze (Lind)",
                "stacks": 30,
                "lind_fortification_level": FortificationLevel.SEGMENT06,
            },
        ]

    @override
    def get_model_assumptions(self) -> list[ModelAssumption]:
        return [
            ModelAssumption(
                icon="rule",
                description="Assumes bonuses from Ketoacidemia are maxed out regarding amount of debuffs.",
            ),
            ModelAssumption(
                icon="rule",
                description="Corrosion debuff triggering from Glucose Overload is not modeled.",
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
