from nicegui import ui

from gui.templates.doll_calculator_page import DollCalculatorPage, ModelAssumption
from gui.templates.rotation_planner import RotationPlanner
from typing import Any, cast, override
from core.types import DamageTag, FortificationLevel, SpecialAttribute, StatType
from core.dolls import dushevnaya


sample_rotation: dict[int, list[dict]] = {
    1: [
        {"name": "Support Action"},
        {"name": "Support Action"},
        {"name": "Support Action"},
    ],
    2: [
        {
            "name": "Hero's Code",
            "stacks_of_ices_grace": 4,
            "target_on_freeze_tile": True,
            "has_fixed_key_1": False,
        },
        {"name": "Support Action"},
        {"name": "Support Action"},
        {"name": "Support Action"},
    ],
    3: [
        {"name": "Marzanna's Sanction", "is_enhanced": False},
        {"name": "Marzanna's Sanction", "is_enhanced": True},
    ],
    4: [
        {"name": "Support Action"},
        {"name": "Support Action"},
        {"name": "Support Action"},
    ],
    5: [
        {
            "name": "Hero's Code",
            "stacks_of_ices_grace": 4,
            "target_on_freeze_tile": True,
            "has_fixed_key_1": False,
        },
        {"name": "Support Action"},
        {"name": "Support Action"},
        {"name": "Support Action"},
    ],
    6: [
        {"name": "Marzanna's Sanction", "is_enhanced": False},
        {"name": "Marzanna's Sanction", "is_enhanced": True},
    ],
    7: [
        {"name": "Support Action"},
        {"name": "Support Action"},
        {"name": "Support Action"},
    ],
}


class Dushevnaya(DollCalculatorPage):
    """Page for Dushevnaya."""

    def __init__(self):
        super().__init__()

        self.doll = dushevnaya.Dushevnaya()
        self.doll.set_fortification_level(FortificationLevel.SEGMENT06)
        self.doll_subtitle: str = """Mapwide Buffs / Tile / Assist

            Support / Freeze"""
        self.dandegate_link: str = "https://www.dandegate.net/dolls/dushevnaya"
        self.doll_portrait: str = "resources/dushevnaya.webp"

    @override
    def update_doll_abilities(self) -> None:
        doll = cast(dushevnaya.Dushevnaya, self.doll)

        self.option_config: dict[str, dict[str, Any]] = {
            "Daybreak": {
                "fields": [],
                "function": doll.daybreak.execute,
            },
            "Hero's Code": {
                "fields": [
                    {
                        "key": "stacks_of_ices_grace",
                        "type": "number",
                        "label": "Ice's Grace stacks",
                        "default": 4,
                    },
                    {
                        "key": "target_on_freeze_tile",
                        "type": "checkbox",
                        "label": "Target is on allied Freeze tile",
                        "default": True,
                    },
                    {
                        "key": "has_fixed_key_1",
                        "type": "checkbox",
                        "label": "Fixed Key 1 - Lance of Longinus",
                        "default": False,
                    },
                ],
                "function": doll.heros_code.execute,
            },
            "Marzanna's Sanction": {
                "fields": [
                    {
                        "key": "is_enhanced",
                        "type": "checkbox",
                        "label": "Enhanced",
                        "default": False,
                    },
                ],
                "function": doll.marzannas_sanction.execute,
            },
            "Support Action": {
                "fields": [],
                "function": doll.support_action.execute,
            },
        }

    @override
    def set_initial_values(self) -> None:
        doll = cast(dushevnaya.Dushevnaya, self.doll)

        doll.initial_stats.basic_attributes[StatType.ATTACK] = 4300
        doll.initial_stats.basic_attributes[StatType.CRIT_RATE] = 78
        doll.initial_stats.basic_attributes[StatType.CRIT_DAMAGE] = 150

        doll.additive_modifiers.special_attributes[
            SpecialAttribute.DAMAGE_BOOST
        ].set_multiplier(DamageTag.ALL, 25)
        doll.additive_modifiers.special_attributes[
            SpecialAttribute.DAMAGE_BOOST
        ].set_multiplier(DamageTag.FREEZE, 25)
        doll.additive_modifiers.special_attributes[
            SpecialAttribute.DAMAGE_BOOST
        ].set_multiplier(DamageTag.PHASE, 15)
        doll.additive_modifiers.special_attributes[
            SpecialAttribute.DAMAGE_BOOST
        ].set_multiplier(DamageTag.TARGETED, 5)

        doll.multiplicative_modifiers.basic_attributes[StatType.ATTACK] = 8

    def get_default_damage_calculator_buffs(self) -> list[dict[str, Any]]:
        return [
            {"name": "Attack Up II"},
            {
                "name": "Brumal Barrier (Alva)",
                "alva_fortification_level": FortificationLevel.SEGMENT05,
                "shield_size": 9000,
            },
            {
                "name": "Glacial Domain (Dushevnaya)",
                "dushevnaya_fortification_level": FortificationLevel.SEGMENT06,
            },
            {
                "name": "Arctic Benediction",
                "dushevnaya_fortification_level": FortificationLevel.SEGMENT01,
            },
        ]

    def get_default_damage_calculator_debuffs(self) -> list[dict[str, Any]]:
        return [
            {"name": "Defense Down II"},
            {
                "name": "Hypothermia",
                "alva_fortification_level": FortificationLevel.SEGMENT05,
            },
            {
                "name": "Frostbite",
            },
        ]

    @override
    def get_model_assumptions(self) -> list[ModelAssumption]:
        return [
            ModelAssumption(
                icon="key",
                description="Expansion Key - Wintersong of the Hero is active, so Dushevnaya's targeted damage is treated as Freeze damage.",
                link_label="Dandegate",
                link_target="https://www.dandegate.net/dolls/dushevnaya/keys/expansion-key-wintersong-of-the-hero",
            ),
            ModelAssumption(
                icon="key",
                description="Fixed Key 2 - Adventurer's Will is active.",
                link_label="Dandegate",
                link_target="https://www.dandegate.net/dolls/dushevnaya/keys/fixed-key-2-adventurer-s-will",
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
