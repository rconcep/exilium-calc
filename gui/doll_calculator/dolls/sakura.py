from nicegui import ui

from gui.templates.doll_calculator_page import DollCalculatorPage, ModelAssumption
from gui.templates.rotation_planner import RotationPlanner
from typing import Any, cast, override
from core.types import DamageTag, FortificationLevel, SpecialAttribute, StatType
from core.dolls import sakura


sample_rotation: dict[int, list[dict]] = {
    1: [
        {
            "name": "Falling Blossom",
        },
        {
            "name": "Grand Isekai Adventure",
        },
        {
            "name": "Sakura Mark",
            "target_has_bad_luck": True,
            "target_is_on_burn_tile": True,
        },
        {
            "name": "Sakura Mark",
            "target_has_bad_luck": True,
            "target_is_on_burn_tile": True,
        },
        {
            "name": "Sakura Mark",
            "target_has_bad_luck": True,
            "target_is_on_burn_tile": True,
        },
    ],
    2: [
        {
            "name": "Misfortune Delivery",
        },
        {
            "name": "Sakura Mark",
            "target_has_bad_luck": True,
            "target_is_on_burn_tile": True,
        },
        {
            "name": "Sakura Mark",
            "target_has_bad_luck": True,
            "target_is_on_burn_tile": True,
        },
        {
            "name": "Sakura Mark",
            "target_has_bad_luck": True,
            "target_is_on_burn_tile": True,
        },
    ],
    3: [
        {"name": "Falling Blossom"},
        {"name": "Misfortune Delivery"},
        {
            "name": "Sakura Mark",
            "target_has_bad_luck": True,
            "target_is_on_burn_tile": True,
        },
        {
            "name": "Sakura Mark",
            "target_has_bad_luck": True,
            "target_is_on_burn_tile": True,
        },
        {
            "name": "Sakura Mark",
            "target_has_bad_luck": True,
            "target_is_on_burn_tile": True,
        },
    ],
    4: [
        {
            "name": "Grand Isekai Adventure",
        },
        {
            "name": "Sakura Mark",
            "target_has_bad_luck": True,
            "target_is_on_burn_tile": True,
        },
        {
            "name": "Sakura Mark",
            "target_has_bad_luck": True,
            "target_is_on_burn_tile": True,
        },
        {
            "name": "Sakura Mark",
            "target_has_bad_luck": True,
            "target_is_on_burn_tile": True,
        },
    ],
    5: [
        {"name": "Falling Blossom"},
        {"name": "Misfortune Delivery"},
        {
            "name": "Sakura Mark",
            "target_has_bad_luck": True,
            "target_is_on_burn_tile": True,
        },
        {
            "name": "Sakura Mark",
            "target_has_bad_luck": True,
            "target_is_on_burn_tile": True,
        },
        {
            "name": "Sakura Mark",
            "target_has_bad_luck": True,
            "target_is_on_burn_tile": True,
        },
    ],
    6: [
        {"name": "Misfortune Delivery"},
        {
            "name": "Sakura Mark",
            "target_has_bad_luck": True,
            "target_is_on_burn_tile": True,
        },
        {
            "name": "Sakura Mark",
            "target_has_bad_luck": True,
            "target_is_on_burn_tile": True,
        },
        {
            "name": "Sakura Mark",
            "target_has_bad_luck": True,
            "target_is_on_burn_tile": True,
        },
    ],
    7: [
        {
            "name": "Falling Blossom",
        },
        {
            "name": "Grand Isekai Adventure",
        },
        {
            "name": "Sakura Mark",
            "target_has_bad_luck": True,
            "target_is_on_burn_tile": True,
        },
        {
            "name": "Sakura Mark",
            "target_has_bad_luck": True,
            "target_is_on_burn_tile": True,
        },
        {
            "name": "Sakura Mark",
            "target_has_bad_luck": True,
            "target_is_on_burn_tile": True,
        },
    ],
}


class Sakura(DollCalculatorPage):
    """Page for Sakura."""

    def __init__(self):
        super().__init__()

        self.doll = sakura.Sakura()
        self.doll.set_fortification_level(FortificationLevel.SEGMENT06)
        self.doll_subtitle: str = """AoE Damage / Agile Combat

            Vanguard / Burn"""
        self.dandegate_link: str = "https://www.dandegate.net/dolls/sakura"
        self.doll_portrait: str = "resources/sakura.webp"

    @override
    def update_doll_abilities(self) -> None:
        doll = cast(sakura.Sakura, self.doll)

        self.option_config: dict[str, dict[str, Any]] = {
            "Sakura Chime": {
                "fields": [],
                "function": doll.sakura_chime.execute,
            },
            "Falling Blossom": {
                "fields": [],
                "function": doll.falling_blossom.execute,
            },
            "Misfortune Delivery": {
                "fields": [],
                "function": doll.misfortune_delivery.execute,
            },
            "Grand Isekai Adventure": {
                "fields": [],
                "function": doll.grand_isekai_adventure.execute,
            },
            "Sakura Mark": {
                "fields": [
                    {
                        "key": "target_has_bad_luck",
                        "type": "checkbox",
                        "label": "Target has Bad Luck",
                        "default": True,
                    },
                    {
                        "key": "target_is_on_burn_tile",
                        "type": "checkbox",
                        "label": "Target is on Burn Tile",
                        "default": True,
                    },
                ],
                "function": doll.sakura_mark.execute,
            },
        }

    @override
    def set_initial_values(self) -> None:
        self.doll.initial_stats.basic_attributes[StatType.ATTACK] = 4600
        self.doll.initial_stats.basic_attributes[StatType.CRIT_RATE] = 80
        self.doll.initial_stats.basic_attributes[StatType.CRIT_DAMAGE] = 170

        self.doll.additive_modifiers.special_attributes[
            SpecialAttribute.DAMAGE_BOOST
        ].set_multiplier(DamageTag.ALL, 30)
        self.doll.additive_modifiers.special_attributes[
            SpecialAttribute.DAMAGE_BOOST
        ].set_multiplier(DamageTag.BURN, 70)
        self.doll.additive_modifiers.special_attributes[
            SpecialAttribute.DAMAGE_BOOST
        ].set_multiplier(DamageTag.PHASE, 30)

        self.doll.multiplicative_modifiers.basic_attributes[StatType.ATTACK] = 11.8

    def get_default_damage_calculator_buffs(self) -> list[dict[str, Any]]:
        return [
            {"name": "Attack Up II"},
            {
                "name": "Good Luck (Sakura)",
                "sakura_fortification_level": FortificationLevel.SEGMENT06,
            },
        ]

    def get_default_damage_calculator_debuffs(self) -> list[dict[str, Any]]:
        return [
            {"name": "Defense Down II"},
        ]

    @override
    def get_model_assumptions(self) -> list[ModelAssumption]:
        return []

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
