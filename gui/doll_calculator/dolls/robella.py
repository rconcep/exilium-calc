from nicegui import ui

from gui.templates.doll_calculator_page import DollCalculatorPage
from gui.templates.rotation_planner import RotationPlanner
from typing import Any, override
from core.types import StatType, FortificationLevel
from core.dolls import robella


sample_rotation: dict[int, list[dict]] = {
    1: [
        {"name": "Unity: Enhanced"},
        {"name": "Unity: Enhanced"},
        {"name": "Unity: Enhanced"},
        {"name": "Unity: Enhanced"},
        {"name": "Unity: Enhanced"},
        {
            "name": "Frigid Infiltration: Enhanced",
            "sense_weakness_stacks": 0,
            "inspection_stacks": 6,
        },
    ],
    2: [
        {"name": "Howling Cyclone", "sense_weakness_stacks": 6},
        {"name": "Unity: Enhanced"},
        {"name": "Unity: Enhanced"},
        {"name": "Unity: Enhanced"},
        {"name": "Unity: Enhanced"},
        {"name": "Unity: Enhanced"},
        {
            "name": "Frigid Infiltration: Enhanced",
            "sense_weakness_stacks": 6,
            "inspection_stacks": 6,
        },
    ],
    3: [
        {"name": "Ultra Shot", "sense_weakness_stacks": 12},
        {"name": "Unity: Enhanced"},
        {"name": "Unity: Enhanced"},
        {"name": "Unity: Enhanced"},
        {"name": "Unity: Enhanced"},
        {
            "name": "Frigid Infiltration: Enhanced",
            "sense_weakness_stacks": 12,
            "inspection_stacks": 6,
        },
    ],
    4: [
        {"name": "Howling Cyclone", "sense_weakness_stacks": 18},
        {"name": "Unity: Enhanced"},
        {"name": "Unity: Enhanced"},
        {"name": "Unity: Enhanced"},
        {"name": "Unity: Enhanced"},
        {"name": "Unity: Enhanced"},
        {
            "name": "Frigid Infiltration: Enhanced",
            "sense_weakness_stacks": 18,
            "inspection_stacks": 6,
        },
    ],
    5: [
        {"name": "Unity: Enhanced"},
        {"name": "Unity: Enhanced"},
        {"name": "Unity: Enhanced"},
        {"name": "Unity: Enhanced"},
        {
            "name": "Frigid Infiltration: Enhanced",
            "sense_weakness_stacks": 24,
            "inspection_stacks": 6,
        },
    ],
    6: [
        {"name": "Howling Cyclone", "sense_weakness_stacks": 30},
        {"name": "Unity: Enhanced"},
        {"name": "Unity: Enhanced"},
        {"name": "Unity: Enhanced"},
        {"name": "Unity: Enhanced"},
        {
            "name": "Frigid Infiltration: Enhanced",
            "sense_weakness_stacks": 30,
            "inspection_stacks": 6,
        },
    ],
    7: [
        {"name": "Howling Cyclone", "sense_weakness_stacks": 36},
        {"name": "Unity: Enhanced"},
        {"name": "Unity: Enhanced"},
        {"name": "Unity: Enhanced"},
        {"name": "Unity: Enhanced"},
        {
            "name": "Frigid Infiltration: Enhanced",
            "sense_weakness_stacks": 36,
            "inspection_stacks": 6,
        },
    ],
}


class Robella(DollCalculatorPage):
    """Page for Robella."""

    def __init__(self):
        super().__init__()

        self.doll: robella.Robella = robella.Robella()
        self.doll.set_fortification_level(FortificationLevel.SEGMENT06)
        self.doll_subtitle: str = """Burst Damage / Pursuit

            Sentinel / Freeze"""
        self.dandegate_link: str = "https://www.dandegate.net/dolls/robella"
        self.doll_portrait: str = (
            "resources/robella.webp"
        )

    @override
    def update_doll_abilities(self) -> None:
        self.option_config: dict[str, dict[str, Any]] = {
            "Ultra Shot": {
                "fields": [
                    {
                        "key": "sense_weakness_stacks",
                        "type": "number",
                        "label": "Sense Weakness Stacks",
                        "default": 0,
                    },
                ],
                "function": self.doll.ultra_shot.execute,
            },
            "Unity": {"fields": [], "function": self.doll.unity.execute},
            "Unity: Enhanced": {
                "fields": [],
                "function": self.doll.unity_enhanced.execute,
            },
            "Frigid Infiltration": {
                "fields": [
                    {
                        "key": "inspection_stacks",
                        "type": "number",
                        "label": "Inspection Stacks",
                        "default": 6,
                    },
                    {
                        "key": "sense_weakness_stacks",
                        "type": "number",
                        "label": "Sense Weakness Stacks",
                        "default": 0,
                    },
                ],
                "function": self.doll.frigid_infiltration.execute,
            },
            "Frigid Infiltration: Enhanced": {
                "fields": [
                    {
                        "key": "inspection_stacks",
                        "type": "number",
                        "label": "Inspection Stacks",
                        "default": 6,
                    },
                    {
                        "key": "sense_weakness_stacks",
                        "type": "number",
                        "label": "Sense Weakness Stacks",
                        "default": 0,
                    },
                ],
                "function": self.doll.frigid_infiltration_enhanced.execute,
            },
            "Howling Cyclone": {
                "fields": [
                    {
                        "key": "sense_weakness_stacks",
                        "type": "number",
                        "label": "Sense Weakness Stacks",
                        "default": 0,
                    },
                ],
                "function": self.doll.howling_cyclone.execute,
            },
        }

    @override
    def set_initial_values(self) -> None:
        self.doll.initial_stats.basic_attributes[StatType.ATTACK] = 4830
        self.doll.initial_stats.basic_attributes[StatType.CRIT_RATE] = 78.9
        self.doll.initial_stats.basic_attributes[StatType.CRIT_DAMAGE] = 156.9

    @override
    def revision_history(self) -> None:
        with ui.timeline(side="right"):
            ui.timeline_entry("", title="Initial version", subtitle="March 03, 2026")

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
