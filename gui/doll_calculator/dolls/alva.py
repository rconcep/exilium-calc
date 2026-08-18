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
from core.dolls import alva

sample_rotation: dict[int, list[dict]] = {
    1: [
        {"name": "Frosted Echo", "confectance_index": 6},
        {"name": "Nix Requiem", "confectance_index": 6},
        {"name": "Interception"},
        {"name": "Interception"},
        {"name": "Interception"},
        {"name": "Hoarfrost Break"},
    ],
    2: [
        {"name": "Nix Requiem", "confectance_index": 6},
        {"name": "Interception"},
        {"name": "Interception"},
        {"name": "Interception"},
        {"name": "Hoarfrost Break"},
    ],
    3: [
        {"name": "Nix Requiem", "confectance_index": 6},
        {"name": "Interception"},
        {"name": "Interception"},
        {"name": "Interception"},
        {"name": "Hoarfrost Break"},
    ],
    4: [
        {"name": "Frosted Echo", "confectance_index": 6},
        {"name": "Nix Requiem", "confectance_index": 6},
        {"name": "Interception"},
        {"name": "Interception"},
        {"name": "Interception"},
        {"name": "Hoarfrost Break"},
    ],
    5: [
        {"name": "Nix Requiem", "confectance_index": 6},
        {"name": "Interception"},
        {"name": "Interception"},
        {"name": "Interception"},
        {"name": "Hoarfrost Break"},
    ],
    6: [
        {"name": "Nix Requiem", "confectance_index": 6},
        {"name": "Interception"},
        {"name": "Interception"},
        {"name": "Interception"},
        {"name": "Hoarfrost Break"},
    ],
    7: [
        {"name": "Frosted Echo", "confectance_index": 6},
        {"name": "Nix Requiem", "confectance_index": 6},
        {"name": "Interception"},
        {"name": "Interception"},
        {"name": "Interception"},
        {"name": "Hoarfrost Break"},
    ],
}


class Alva(DollCalculatorPage):
    """Page for Alva."""

    def __init__(self):
        super().__init__()

        self.doll = alva.Alva()
        self.doll.set_fortification_level(FortificationLevel.SEGMENT06)
        self.doll_subtitle: str = """Shield / Shield Damage Increase / First Strike

            Support / Freeze"""
        self.dandegate_link: str = "https://www.dandegate.net/dolls/alva"
        self.doll_portrait: str = "resources/alva.webp"

    @override
    def update_doll_abilities(self) -> None:
        doll = cast(alva.Alva, self.doll)

        self.option_config: dict[str, dict[str, Any]] = {
            "Laceration": {
                "fields": [],
                "function": doll.laceration.execute,
            },
            "Snow Wolf's Heart": {
                "fields": [],
                "function": doll.snow_wolfs_heart.execute,
            },
            "Frosted Echo": {
                "fields": [
                    {
                        "key": "confectance_index",
                        "type": "select",
                        "label": "Confectance Index",
                        "default": 6,
                        "options": [n for n in range(7)],
                    },
                ],
                "function": doll.frosted_echo.execute,
            },
            "Hoarfrost Break": {
                "fields": [],
                "function": doll.hoarfrost_break.execute,
            },
            "Nix Requiem": {
                "fields": [
                    {
                        "key": "confectance_index",
                        "type": "select",
                        "label": "Confectance Index",
                        "default": 6,
                        "options": [n for n in range(7)],
                    },
                ],
                "function": doll.nix_requiem.execute,
            },
            "Interception": {
                "fields": [],
                "function": doll.interception.execute,
            },
        }

        self.add_elemental_tile_actions_for_element(
            self.option_config,
            DamageTag.FREEZE,
        )

    @override
    def set_initial_values(self) -> None:
        self.doll.initial_stats.basic_attributes[StatType.ATTACK] = 3800
        self.doll.initial_stats.basic_attributes[StatType.CRIT_RATE] = 80
        self.doll.initial_stats.basic_attributes[StatType.CRIT_DAMAGE] = 150

        self.doll.additive_modifiers.special_attributes[
            SpecialAttribute.DAMAGE_BOOST
        ].set_multiplier(DamageTag.ALL, 35)
        self.doll.additive_modifiers.special_attributes[
            SpecialAttribute.DAMAGE_BOOST
        ].set_multiplier(DamageTag.FREEZE, 35)
        self.doll.additive_modifiers.special_attributes[
            SpecialAttribute.DAMAGE_BOOST
        ].set_multiplier(DamageTag.PHASE, 30)

        self.doll.multiplicative_modifiers.basic_attributes[StatType.ATTACK] = 8

    def get_default_damage_calculator_buffs(self) -> list[dict[str, Any]]:
        return [
            {"name": "Attack Up II"},
            {
                "name": "Brumal Barrier (Alva)",
                "alva_fortification_level": FortificationLevel.SEGMENT05,
                "shield_size": 9000,
            },
            {
                "name": "Late Bloomer (Alva)",
                "stacks_of_battle_prep_consumed": 6,
            },
            {"name": "Covering Mode (Alva)"},
            {"name": "Unity: Enhanced", "robella_initial_attack": 4800},
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
                icon="visibility",
                description="Covering Mode is always active (for the critical hit rate buff).",
            ),
            ModelAssumption(
                icon="shield",
                description="Hoarfrost Break (the attack triggered when Hoarfrost shield is broken) assumes the maximum shield size.",
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
