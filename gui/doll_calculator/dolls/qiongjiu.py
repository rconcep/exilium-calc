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
from core.dolls import qiongjiu


sample_rotation: dict[int, list[dict]] = {
    1: [
        {"name": "Support Action", "has_expansion_key": True},
        {"name": "Support Action", "has_expansion_key": True},
        {"name": "Support Action", "has_expansion_key": True},
        {"name": "Support Action", "has_expansion_key": True},
        {"name": "Support Action", "has_expansion_key": True},
        {"name": "Support Action", "has_expansion_key": True},
    ],
    2: [
        {"name": "Support Action", "has_expansion_key": True},
        {"name": "Support Action", "has_expansion_key": True},
        {"name": "Support Action", "has_expansion_key": True},
        {"name": "Support Action", "has_expansion_key": True},
        {"name": "Support Action", "has_expansion_key": True},
        {"name": "Support Action", "has_expansion_key": True},
    ],
    3: [
        {"name": "Support Action", "has_expansion_key": True},
        {"name": "Support Action", "has_expansion_key": True},
        {"name": "Support Action", "has_expansion_key": True},
        {"name": "Support Action", "has_expansion_key": True},
        {"name": "Support Action", "has_expansion_key": True},
        {"name": "Support Action", "has_expansion_key": True},
    ],
    4: [
        {"name": "Support Action", "has_expansion_key": True},
        {"name": "Support Action", "has_expansion_key": True},
        {"name": "Support Action", "has_expansion_key": True},
        {"name": "Support Action", "has_expansion_key": True},
        {"name": "Support Action", "has_expansion_key": True},
        {"name": "Support Action", "has_expansion_key": True},
    ],
    5: [
        {"name": "Support Action", "has_expansion_key": True},
        {"name": "Support Action", "has_expansion_key": True},
        {"name": "Support Action", "has_expansion_key": True},
        {"name": "Support Action", "has_expansion_key": True},
        {"name": "Support Action", "has_expansion_key": True},
        {"name": "Support Action", "has_expansion_key": True},
    ],
    6: [
        {"name": "Support Action", "has_expansion_key": True},
        {"name": "Support Action", "has_expansion_key": True},
        {"name": "Support Action", "has_expansion_key": True},
        {"name": "Support Action", "has_expansion_key": True},
        {"name": "Support Action", "has_expansion_key": True},
        {"name": "Support Action", "has_expansion_key": True},
    ],
    7: [
        {"name": "Support Action", "has_expansion_key": True},
        {"name": "Support Action", "has_expansion_key": True},
        {"name": "Support Action", "has_expansion_key": True},
        {"name": "Support Action", "has_expansion_key": True},
        {"name": "Support Action", "has_expansion_key": True},
        {"name": "Support Action", "has_expansion_key": True},
    ],
}


class Qiongjiu(DollCalculatorPage):
    """Page for Qiongjiu."""

    def __init__(self):
        super().__init__()

        self.doll = qiongjiu.Qiongjiu()
        self.doll.set_fortification_level(FortificationLevel.SEGMENT06)
        self.doll_subtitle: str = """Sustained Damage / Assist

            Sentinel / Burn"""
        self.dandegate_link: str = "https://www.dandegate.net/dolls/qiongjiu"
        self.doll_portrait: str = "resources/qiongjiu.webp"

    @override
    def update_doll_abilities(self) -> None:
        doll = cast(qiongjiu.Qiongjiu, self.doll)

        self.option_config: dict[str, dict[str, Any]] = {
            "Fuse": {
                "fields": [],
                "function": doll.fuse.execute,
            },
            "Common Rail": {
                "fields": [],
                "function": doll.common_rail.execute,
            },
            "Guide to Victory": {
                "fields": [
                    {
                        "key": "target_has_overburn",
                        "type": "checkbox",
                        "label": "Target inflicted with Overburn",
                        "default": True,
                    },
                    {
                        "key": "has_fixed_key_4",
                        "type": "checkbox",
                        "label": "Fixed Key 4 - Point of Vulnerability",
                        "default": False,
                    },
                    {
                        "key": "is_secondary_target",
                        "type": "checkbox",
                        "label": "Target beyond the first",
                        "default": False,
                    },
                ],
                "function": doll.guide_to_victory.execute,
            },
            "Support Action": {
                "fields": [
                    {
                        "key": "has_expansion_key",
                        "type": "checkbox",
                        "label": "Expansion Key - Ruined Gem",
                        "default": True,
                    },
                ],
                "function": doll.support_action.execute,
            },
        }

    @override
    def set_initial_values(self) -> None:
        doll = cast(qiongjiu.Qiongjiu, self.doll)

        doll.initial_stats.basic_attributes[StatType.ATTACK] = 4210
        doll.initial_stats.basic_attributes[StatType.CRIT_RATE] = 80
        doll.initial_stats.basic_attributes[StatType.CRIT_DAMAGE] = 150

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
        ].set_multiplier(DamageTag.SUPPORT_ACTION, 10)

        doll.additive_modifiers.special_attributes[
            SpecialAttribute.DAMAGE_BOOST
        ].set_multiplier(DamageTag.PASSIVE, 25)

        doll.additive_modifiers.special_attributes[
            SpecialAttribute.DAMAGE_BOOST
        ].set_multiplier(DamageTag.ONLY_HIT_ONE_TARGET, 12)

        doll.additive_modifiers.special_attributes[
            SpecialAttribute.CRITICAL_DAMAGE
        ].set_multiplier(DamageTag.ALL, 3)

        doll.multiplicative_modifiers.basic_attributes[StatType.ATTACK] = 11

    def get_default_damage_calculator_buffs(self) -> list[dict[str, Any]]:
        return [
            {"name": "Blazing Assault II"},
            {
                "name": "Accelerant (Vector)",
                "vector_fortification_level": FortificationLevel.SEGMENT06,
                "number_of_burn_buffs": 3,
            },
            {"name": "Support Boost II"},
        ]

    def get_default_damage_calculator_debuffs(self) -> list[dict[str, Any]]:
        return [
            {"name": "Defense Down II"},
            {"name": "Vulnerable II"},
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
                icon="local_fire_department",
                description="Sample rotation assumes V1+ Vector to raise number of Support Actions.",
            ),
            ModelAssumption(
                icon="local_fire_department",
                description="Assumes target has Burn debuffs.",
            ),
            ModelAssumption(
                icon="key",
                description="Expansion Key - Ruined Gem is active.",
                link_label="Dandegate",
                link_target="https://www.dandegate.net/dolls/qiongjiu/keys/expansion-key-ruined-gem",
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
