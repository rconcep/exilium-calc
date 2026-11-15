from nicegui import ui

from gui.templates.doll_calculator_page import DollCalculatorPage, ModelAssumption
from gui.templates.rotation_planner import RotationPlanner
from typing import Any, override
from core.types import StatType, FortificationLevel, DamageTag, SpecialAttribute
from core.dolls import tololo


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
            "Call of the Stars (Geostationary Satellite)": {
                "fields": [
                    {
                        "key": "stacks_of_observation_advantage",
                        "type": "select",
                        "options": [0, 1, 2, 3],
                        "label": "Stacks of Observation Advantage",
                        "default": 3,
                    },
                ],
                "function": self.doll.call_of_the_stars.execute,
            },
        }

    @override
    def set_initial_values(self) -> None:
        self.doll.initial_stats.basic_attributes[StatType.ATTACK] = 4830
        self.doll.initial_stats.basic_attributes[StatType.CRIT_RATE] = 81
        self.doll.initial_stats.basic_attributes[StatType.CRIT_DAMAGE] = 154.5

        # imagoform: 5+12
        # summon boost: 20
        self.doll.additive_modifiers.special_attributes[
            SpecialAttribute.DAMAGE_BOOST
        ].set_multiplier(DamageTag.ALL, 17 + 20)

        # weapon: 15
        # imagoform: 5
        # freeze boost: 1.5
        # Freeze Unity: 0.9
        # Dushevnaya Imagoform (Bud): 3
        self.doll.additive_modifiers.special_attributes[
            SpecialAttribute.DAMAGE_BOOST
        ].set_multiplier(DamageTag.HYDRO, 15 + 5 + 1.5 + 0.9 + 3)

        # keys: 20
        self.doll.additive_modifiers.special_attributes[
            SpecialAttribute.DAMAGE_BOOST
        ].set_multiplier(DamageTag.PHASE, 20)

        # summon boost: 20
        # keys: 10
        self.doll.additive_modifiers.special_attributes[
            SpecialAttribute.DAMAGE_BOOST
        ].set_multiplier(DamageTag.PHYSICAL_SUMMON, 20 + 10)

        # imagoform: 10
        self.doll.additive_modifiers.special_attributes[
            SpecialAttribute.DAMAGE_BOOST
        ].set_multiplier(DamageTag.STABILITY_BROKEN, 10)

        self.doll.refresh_geostationary_satellite()

    @override
    def get_model_assumptions(self) -> list[ModelAssumption]:
        return [
            ModelAssumption(
                icon="water_drop",
                description="Sample rotation assumes Springfield support with Shared Telepathy and that a phase weakness is exploited for Black Hole Inversion.",
            ),
            ModelAssumption(
                icon="key",
                description="Expansion Key 2 - Captured Starlight is active.",
                link_label="Dandegate",
                link_target="https://www.dandegate.net/dolls/tololo/keys/expansion-key-2-captured-starlight",
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
