from nicegui import ui

from gui.templates.doll_calculator_page import DollCalculatorPage, ModelAssumption
from gui.templates.rotation_planner import RotationPlanner
from typing import Any, override
from core.types import (
    StatType,
    FortificationLevel,
    SpecialAttribute,
    DamageTag,
)
from core.dolls import koleda

sample_rotation: dict[int, list[dict]] = {
    1: [],  # Rotation left blank as requested
    2: [],
    3: [],
    4: [],
}


class Koleda(DollCalculatorPage):
    """Koleda doll calculator page."""

    def __init__(self):
        super().__init__()

        self.doll: koleda.Koleda = koleda.Koleda()
        self.doll.set_fortification_level(FortificationLevel.SEGMENT06)
        self.doll_subtitle: str = """Burst Damage / Summon

            Sentinel / Hydro"""
        self.dandegate_link: str = "https://www.dandegate.net/dolls/koleda"
        self.doll_portrait: str = "resources/koleda.webp"

    @override
    def update_doll_abilities(self) -> None:
        self.option_config: dict[str, dict[str, Any]] = {
            "Predator Instinct": {
                "fields": [],
                "function": self.doll.predator_instinct.execute,
            },
            "Snow Wolf's Eye": {
                "fields": [
                    {
                        "key": "stacks_of_upshift",
                        "type": "select",
                        "label": "Stacks of Upshift",
                        "options": list(range(0, 6)),
                        "default": 5,
                    },
                ],
                "function": self.doll.snow_wolfs_eye.execute,
            },
            "Let's Go for a Drift! (Sinveiler)": {
                "fields": [
                    {
                        "key": "gear",
                        "type": "select",
                        "label": "Sinveiler Gear",
                        "options": [
                            koleda.SinveilerGear.P,
                            koleda.SinveilerGear.N,
                            koleda.SinveilerGear.D,
                            koleda.SinveilerGear.S,
                            koleda.SinveilerGear.S_PLUS,
                        ],
                        "default": koleda.SinveilerGear.D,
                    },
                ],
                "function": self.doll.lets_go_for_a_drift.execute,
            },
            "Let's Go Full Speed! (Sinveiler)": {
                "fields": [
                    {
                        "key": "gear",
                        "type": "select",
                        "label": "Sinveiler Gear",
                        "options": [
                            koleda.SinveilerGear.P,
                            koleda.SinveilerGear.N,
                            koleda.SinveilerGear.D,
                            koleda.SinveilerGear.S,
                            koleda.SinveilerGear.S_PLUS,
                        ],
                        "default": koleda.SinveilerGear.D,
                    },
                ],
                "function": self.doll.lets_go_full_speed.execute,
            },
            "Let's Go Full Speed! (Pursuit) (Sinveiler)": {
                "fields": [
                    {
                        "key": "gear",
                        "type": "select",
                        "label": "Sinveiler Gear",
                        "options": [
                            koleda.SinveilerGear.P,
                            koleda.SinveilerGear.N,
                            koleda.SinveilerGear.D,
                            koleda.SinveilerGear.S,
                            koleda.SinveilerGear.S_PLUS,
                        ],
                        "default": koleda.SinveilerGear.D,
                    },
                ],
                "function": self.doll.lets_go_full_speed_pursuit.execute,
            },
            "Kinetic Release (Sinveiler)": {
                "fields": [
                    {
                        "key": "gear",
                        "type": "select",
                        "label": "Sinveiler Gear",
                        "options": [
                            koleda.SinveilerGear.P,
                            koleda.SinveilerGear.N,
                            koleda.SinveilerGear.D,
                            koleda.SinveilerGear.S,
                            koleda.SinveilerGear.S_PLUS,
                        ],
                        "default": koleda.SinveilerGear.S,
                    },
                ],
                "function": self.doll.kinetic_release.execute,
            },
            "Kinetic Release+ (Sinveiler)": {
                "fields": [
                    {
                        "key": "gear",
                        "type": "select",
                        "label": "Sinveiler Gear",
                        "options": [
                            koleda.SinveilerGear.P,
                            koleda.SinveilerGear.N,
                            koleda.SinveilerGear.D,
                            koleda.SinveilerGear.S,
                            koleda.SinveilerGear.S_PLUS,
                        ],
                        "default": koleda.SinveilerGear.S_PLUS,
                    },
                ],
                "function": self.doll.kinetic_release_plus.execute,
            },
        }

        self.add_elemental_tile_actions_for_element(
            self.option_config,
            DamageTag.HYDRO,
        )

    @override
    def set_initial_values(self) -> None:
        # Sample stats copied from Nikketa
        self.doll.initial_stats.basic_attributes[StatType.ATTACK] = 4830
        self.doll.initial_stats.basic_attributes[StatType.CRIT_RATE] = 81
        self.doll.initial_stats.basic_attributes[StatType.CRIT_DAMAGE] = 154.5

        # imagoform: 5+12
        # CQC elite: 0.4
        # Alva 6P33: 10
        # Imagoform (Shoot): 4+3
        self.doll.additive_modifiers.special_attributes[
            SpecialAttribute.DAMAGE_BOOST
        ].set_multiplier(DamageTag.ALL, 17 + 0.4 + 10 + 4 + 3)

        # weapon: 15
        # attachment: 20
        # imagoform: 5
        # freeze boost: 1.5
        # Freeze Unity: 0.9
        # Dushevnaya Imagoform (Bud): 3
        self.doll.additive_modifiers.special_attributes[
            SpecialAttribute.DAMAGE_BOOST
        ].set_multiplier(DamageTag.HYDRO, 15 + 20 + 5 + 1.5 + 0.9 + 3)

        # keys: 30
        self.doll.additive_modifiers.special_attributes[
            SpecialAttribute.DAMAGE_BOOST
        ].set_multiplier(DamageTag.PHASE, 30)

        # weapon: 14
        # raid stance: 1
        self.doll.additive_modifiers.special_attributes[
            SpecialAttribute.DAMAGE_BOOST
        ].set_multiplier(DamageTag.PASSIVE, 14 + 1)

        # imagoform: 10
        self.doll.additive_modifiers.special_attributes[
            SpecialAttribute.DAMAGE_BOOST
        ].set_multiplier(DamageTag.STABILITY_BROKEN, 10)

        # Sync Sinveiler now that real stats are in place.
        self.doll.refresh_sinveiler()

    @override
    def get_rotation_planner(self) -> None:
        with ui.card().classes("w-full h-full"):

            def update_all():
                self.damage_instances = self.rotation_planner.get_all_actions()
                self.stats_update_callback(None)  # type: ignore

            ui.button("Update", on_click=update_all).classes("w-full")
            self.rotation_planner = RotationPlanner(options_config=self.option_config)
            self.rotation_planner.set_data(sample_rotation)

    @override
    def get_model_assumptions(self) -> list[ModelAssumption]:
        return [
            ModelAssumption(
                name="Sinveiler Gear",
                description=(
                    "The current gear of Sinveiler. Select the gear to calculate damage with. "
                    "S+ Gear at V3+ fortification applies +30 to base potency for applicable skills."
                ),
            ),
        ]
