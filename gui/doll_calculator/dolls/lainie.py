from nicegui import ui

from gui.templates.doll_calculator_page import DollCalculatorPage
from gui.templates.rotation_planner import RotationPlanner
from typing import Any, override
from core.types import FortificationLevel, StatType, Unit
from core.dolls import lainie


sample_rotation: dict[int, list[dict]] = {}


class Lainie(DollCalculatorPage):
    """Page for Lainie."""

    def __init__(self):
        super().__init__()

        self._lainie: lainie.Lainie = lainie.Lainie()
        self.doll = self._lainie
        self.doll.set_fortification_level(FortificationLevel.SEGMENT06)
        self.doll_subtitle: str = """Summon Damage / Defense Ignore

            Sentinel / Physical"""
        self.dandegate_link: str = "https://www.dandegate.net/dolls/lainie"
        self.doll_portrait: str = "resources/lainie.webp"

    @override
    def update_doll_abilities(self) -> None:
        self.option_config: dict[str, dict[str, Any]] = {
            "Victory Protocol": {
                "fields": [],
                "function": self._lainie.victory_protocol.execute,
            },
            "Combat Algorithm": {
                "fields": [
                    {
                        "key": "target_has_nonpositive_defense",
                        "type": "checkbox",
                        "label": "Target has non-positive defense",
                        "default": False,
                    },
                ],
                "function": self._lainie.combat_algorithm.execute,
            },
            "Computational Crush": {
                "fields": [],
                "function": self._lainie.computational_crush.execute,
            },
            "Phantom Barrage": {
                "fields": [],
                "function": self._lainie.phantom_barrage.execute,
            },
            "Offense Simulation": {
                "fields": [
                    {
                        "key": "number_of_targets",
                        "type": "number",
                        "label": "Number of targets",
                        "default": 1,
                    },
                    {
                        "key": "hit_same_target_as_combat_algorithm",
                        "type": "checkbox",
                        "label": "Hit same target as Combat Algorithm",
                        "default": True,
                    },
                ],
                "function": self._lainie.offense_simulation.execute,
            },
            "Cognition Overclock": {
                "fields": [],
                "function": self._lainie.cognition_overclock.execute,
            },
        }

    @override
    def set_initial_values(self) -> None:
        self.doll.initial_stats.basic_attributes[StatType.ATTACK] = 4200
        self.doll.initial_stats.basic_attributes[StatType.CRIT_RATE] = 80
        self.doll.initial_stats.basic_attributes[StatType.CRIT_DAMAGE] = 150
        self.doll.initial_stats.basic_attributes[StatType.HEALTH] = 3200
        # Sync the Simulacrum now that real stats are in place.
        self._lainie.refresh_simulacrum()

    @override
    def stats_update_callback(self, update: ui.number) -> None:  # type: ignore[override]
        # Keep the Simulacrum's snapshot current before deepcopy is taken
        # for every damage calculation inside the parent's callback.
        self._lainie.refresh_simulacrum()
        super().stats_update_callback(update)

    @override
    def revision_history(self) -> None:
        with ui.timeline(side="right"):
            ui.timeline_entry("", title="Initial version", subtitle="March 27, 2026")

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
