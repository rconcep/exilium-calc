from nicegui import ui

from gui.templates.doll_calculator_page import DollCalculatorPage, ModelAssumption
from gui.templates.rotation_planner import RotationPlanner
from typing import Any, cast, override
from core.types import FortificationLevel, StatType
from core.dolls import welrod

# Sample rotation intentionally left blank for now.
sample_rotation: dict[int, list[dict]] = {}


class Welrod(DollCalculatorPage):
    """Page for Welrod."""

    def __init__(self):
        super().__init__()

        self.doll: welrod.Welrod = welrod.Welrod()
        self.doll.set_fortification_level(FortificationLevel.SEGMENT06)
        self.doll_subtitle: str = """AoE Damage / Crowd Control / Delayed Damage

            Bulwark / Corrosion"""
        self.dandegate_link: str = "https://www.dandegate.net/dolls/welrod"
        self.doll_portrait: str = "resources/welrod.webp"

    @override
    def update_doll_abilities(self) -> None:
        doll = cast(welrod.Welrod, self.doll)

        self.option_config: dict[str, dict[str, Any]] = {
            "Hushed Erasure": {
                "fields": [],
                "function": doll.hushed_erasure.execute,
            },
            "Joint Investigation": {
                "fields": [],
                "function": doll.joint_investigation.execute,
            },
            "Subjective Sanction": {
                "fields": [],
                "function": doll.subjective_sanction.execute,
            },
            "Judgement Blast": {
                "fields": [
                    {
                        "key": "instances_of_damage_taken",
                        "label": "Instances of Damage Taken",
                        "type": "number",
                        "default": 2,
                    },
                    {
                        "key": "number_of_targets_hit",
                        "label": "Number of Targets Hit",
                        "type": "number",
                        "default": 1,
                    },
                ],
                "function": doll.judgement_blast.execute,
            },
            "Iniquity's Retribution": {
                "fields": [
                    {
                        "key": "detectives_immunity_accumulated_damage",
                        "label": "Detective's Immunity Accumulated Damage",
                        "type": "number",
                        "default": 10000,
                    },
                ],
                "function": doll.iniquity_retribution.execute,
            },
            "Case Controller": {
                "fields": [
                    {
                        "key": "detectives_immunity_accumulated_damage",
                        "label": "Detective's Immunity Accumulated Damage",
                        "type": "number",
                        "default": 10000,
                    },
                ],
                "function": doll.case_controller.execute,
            },
            "Suspect": {
                "fields": [],
                "function": doll.suspect.execute,
            },
        }

    @override
    def set_initial_values(self) -> None:
        self.doll.initial_stats.basic_attributes[StatType.ATTACK] = 3800
        self.doll.initial_stats.basic_attributes[StatType.HEALTH] = 6000
        self.doll.initial_stats.basic_attributes[StatType.CRIT_RATE] = 25
        self.doll.initial_stats.basic_attributes[StatType.CRIT_DAMAGE] = 125

    @override
    def get_model_assumptions(self) -> list[ModelAssumption]:
        return [
            ModelAssumption(
                icon="health_and_safety",
                description="Welrod's passive's critical rate reduction and max HP increase are applied automatically.",
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
