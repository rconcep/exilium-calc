from typing import Any, cast, override

from nicegui import ui

from core.dolls import basti
from core.types import DamageTag, FortificationLevel, SpecialAttribute, StatType
from gui.templates.doll_calculator_page import DollCalculatorPage, ModelAssumption
from gui.templates.rotation_planner import RotationPlanner

_t1 = [
    {
        "name": "Self-Destruct (Cutie)",
    },
    {
        "name": "Self-Destruct (Cutie)",
    },
    {
        "name": "Self-Destruct (Cutie)",
    },
    {
        "name": "Candy-Coated Carnage",
        "number_of_targets_hit": 1,
    },
    {
        "name": "Grudge",
    },
    {
        "name": "Grudge",
    },
    {
        "name": "Grudge",
    },
]

_t2 = [
    {
        "name": "Self-Destruct (Cutie)",
    },
    {
        "name": "Self-Destruct (Cutie)",
    },
    {
        "name": "Self-Destruct (Cutie)",
    },
]


sample_rotation: dict[int, list[dict]] = {
    1: _t1,
    2: _t2,
    3: _t1,
    4: _t2,
    5: _t1,
    6: _t2,
    7: _t1,
}


class Basti(DollCalculatorPage):
    """Page for Basti."""

    def __init__(self):
        super().__init__()

        self.doll = basti.Basti()
        self.doll.set_fortification_level(FortificationLevel.SEGMENT06)
        self.doll_subtitle: str = """Summon / Transfer / Tile

            Support / Corrosion"""
        self.dandegate_link: str = "https://www.dandegate.net/dolls/basti"
        self.doll_portrait: str = "resources/basti.webp"

    @override
    def update_doll_abilities(self) -> None:
        doll = cast(basti.Basti, self.doll)

        self.option_config: dict[str, dict[str, Any]] = {
            "Wildcat Impulse": {
                "fields": [],
                "function": doll.wildcat_impulse.execute,
            },
            "Self-Destruct (Cutie)": {
                "fields": [],
                "function": doll.self_destruct.execute,
            },
            "Candy-Coated Carnage": {
                "fields": [
                    {
                        "key": "number_of_targets_hit",
                        "type": "select",
                        "label": "Targets Hit",
                        "default": 1,
                        "options": [n for n in range(1, 6)],
                    },
                ],
                "function": doll.candy_coated_carnage.execute,
            },
            "Grudge": {
                "fields": [],
                "function": doll.grudge.execute,
            },
        }

        self.add_elemental_tile_actions_for_element(
            self.option_config,
            DamageTag.CORROSION,
        )

    @override
    def set_initial_values(self) -> None:
        doll = cast(basti.Basti, self.doll)

        doll.initial_stats.basic_attributes[StatType.ATTACK] = 3800
        doll.initial_stats.basic_attributes[StatType.CRIT_RATE] = 75
        doll.initial_stats.basic_attributes[StatType.CRIT_DAMAGE] = 150

        doll.additive_modifiers.special_attributes[
            SpecialAttribute.DAMAGE_BOOST
        ].set_multiplier(DamageTag.ALL, 20)
        doll.additive_modifiers.special_attributes[
            SpecialAttribute.DAMAGE_BOOST
        ].set_multiplier(DamageTag.CORROSION, 30)
        doll.additive_modifiers.special_attributes[
            SpecialAttribute.DAMAGE_BOOST
        ].set_multiplier(DamageTag.PHASE, 15)

        doll.multiplicative_modifiers.basic_attributes[StatType.ATTACK] = 8

    def get_default_damage_calculator_buffs(self) -> list[dict[str, Any]]:
        return [
            {"name": "Attack Up II"},
            {
                "name": "Energy Drink (Basti)",
                "stacks": 5,
                "basti_fortification_level": FortificationLevel.SEGMENT06,
            },
            {
                "name": "Insignia of Camaraderie (Basti)",
                "basti_fortification_level": FortificationLevel.SEGMENT06,
            },
            {
                "name": "Cutie Detonation (Basti)",
                "cuties_detonated": 18,
                "basti_fortification_level": FortificationLevel.SEGMENT06,
            },
        ]

    def get_default_damage_calculator_debuffs(self) -> list[dict[str, Any]]:
        return [
            {"name": "Defense Down II"},
            {"name": "Toxin Inundation"},
            {
                "name": "Scribbled Funny Face (Basti)",
                "basti_fortification_level": FortificationLevel.SEGMENT06,
            },
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
            self.rotation_planner = RotationPlanner(options_config=self.option_config)
            self.rotation_planner.set_data(sample_rotation)
