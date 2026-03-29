from nicegui import ui

from gui.templates.doll_calculator_page import DollCalculatorPage, ModelAssumption
from gui.templates.rotation_planner import RotationPlanner
from typing import Any, override
from core.types import StatType, FortificationLevel
from core.dolls import tololo


sample_rotation: dict[int, list[dict]] = {
    1: [
        {"name": "Morte Lumina", "number_of_active_buffs": 3},
        {"name": "Supernova Impact", "number_of_active_buffs": 3},
        {"name": "Black Hole Inversion"},
    ],
    2: [
        {"name": "Morte Lumina", "number_of_active_buffs": 3},
        {"name": "Supernova Impact", "number_of_active_buffs": 3},
        {"name": "Black Hole Inversion"},
    ],
    3: [
        {"name": "Morte Lumina", "number_of_active_buffs": 3},
        {"name": "Supernova Impact", "number_of_active_buffs": 3},
        {"name": "Black Hole Inversion"},
    ],
    4: [
        {"name": "Morte Lumina", "number_of_active_buffs": 3},
        {"name": "Supernova Impact", "number_of_active_buffs": 3},
        {"name": "Black Hole Inversion"},
    ],
    5: [
        {"name": "Morte Lumina", "number_of_active_buffs": 3},
        {"name": "Supernova Impact", "number_of_active_buffs": 3},
        {"name": "Black Hole Inversion"},
    ],
    6: [
        {"name": "Morte Lumina", "number_of_active_buffs": 3},
        {"name": "Supernova Impact", "number_of_active_buffs": 3},
        {"name": "Black Hole Inversion"},
    ],
    7: [
        {"name": "Morte Lumina", "number_of_active_buffs": 3},
        {"name": "Supernova Impact", "number_of_active_buffs": 3},
        {"name": "Morte Lumina", "number_of_active_buffs": 3},
    ],
}


class Tololo(DollCalculatorPage):
    """ """

    def __init__(self):
        super().__init__()

        self.doll: tololo.Tololo = tololo.Tololo()
        self.doll.set_fortification_level(FortificationLevel.SEGMENT06)
        self.doll_subtitle: str = """Single Target Burst / Extra Action

            Sentinel / Hydro"""
        self.dandegate_link: str = "https://www.dandegate.net/dolls/tololo"
        self.doll_portrait: str = "resources/tololo.webp"

    @override
    def update_doll_abilities(self) -> None:
        self.option_config: dict[str, dict[str, Any]] = {
            "Meteor": {"fields": [], "function": self.doll.meteor.execute},
            "Black Hole Inversion": {
                "fields": [],
                "function": self.doll.black_hole_inversion.execute,
            },
            "Supernova Impact": {
                "fields": [
                    {
                        "key": "number_of_active_buffs",
                        "type": "number",
                        "label": "Number of Active Buffs",
                        "default": 3,
                    },
                ],
                "function": self.doll.supernova_impact.execute,
            },
            "Morte Lumina": {
                "fields": [
                    {
                        "key": "number_of_active_buffs",
                        "type": "number",
                        "label": "Number of Active Buffs",
                        "default": 3,
                    },
                ],
                "function": self.doll.morte_lumina.execute,
            },
        }

    @override
    def set_initial_values(self) -> None:
        self.doll.initial_stats.basic_attributes[StatType.ATTACK] = 5429
        self.doll.initial_stats.basic_attributes[StatType.CRIT_RATE] = 78.9
        self.doll.initial_stats.basic_attributes[StatType.CRIT_DAMAGE] = 156.9

    @override
    def get_model_assumptions(self) -> list[ModelAssumption]:
        return [
            ModelAssumption(
                icon="water_drop",
                description="Sample rotation assumes Springfield support with Shared Telepathy and that a phase weakness is exploited for Black Hole Inversion.",
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
