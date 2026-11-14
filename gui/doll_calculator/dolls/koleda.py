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

        # Driver configuration inputs
        self.driver_attack_input: ui.number | None = None
        self.driver_defense_input: ui.number | None = None
        self.driver_health_input: ui.number | None = None
        self.driver_crit_damage_input: ui.number | None = None

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
            "Kinetic Release (Koleda)": {
                "fields": [],
                "function": self.doll.koleda_kinetic_release.execute,
            },
            "Kinetic Release+ (Koleda)": {
                "fields": [],
                "function": self.doll.koleda_kinetic_release_plus.execute,
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

    def _sync_driver_stats(self) -> None:
        """Syncs driver input fields to the Koleda doll's driver stats."""
        if all(
            [
                self.driver_attack_input,
                self.driver_defense_input,
                self.driver_health_input,
                self.driver_crit_damage_input,
            ]
        ):
            self.doll.set_driver(
                attack=self.driver_attack_input.value,
                defense=self.driver_defense_input.value,
                health=self.driver_health_input.value,
                crit_damage=self.driver_crit_damage_input.value,
            )

    def _driver_update_callback(self, _: ui.number) -> None:  # type: ignore
        """Callback for driver stat changes."""
        self._sync_driver_stats()
        self.doll.refresh_sinveiler()
        self.stats_update_callback(None)  # type: ignore

    @override
    def stats_update_callback(self, update: ui.number) -> None:  # type: ignore[override]
        # Keep Sinveiler's snapshot current before deepcopy is taken
        # for every damage calculation inside the parent's callback.
        self.doll.refresh_sinveiler()
        super().stats_update_callback(update)

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
    def render_context_cards(self) -> None:
        """Renders Koleda-specific context card for driver configuration."""
        with ui.row().classes("w-full gap-4"):
            self.render_driver_configuration_tab()

    def render_driver_configuration_tab(self) -> None:
        """Renders the driver configuration tab UI with stat inputs."""
        with ui.card().classes("w-110 exilium-panel"):
            ui.label("Sinveiler: Let's Go For a Spin!").classes("text-bold text-lg")
            ui.label(
                "Specify the target of Out for a Spin! If none, leave stats at 0."
            ).classes("italic text-caption")

            with ui.list().props("bordered dense separator").classes("w-full"):
                ui.item_label("Driver Stats").props("header").classes("text-bold")
                ui.separator()

                with ui.item():
                    with ui.item_section().props("no-wrap"):
                        ui.item_label("Attack")
                    with ui.item_section().props("side"):
                        self.driver_attack_input = ui.number(
                            value=0,
                            min=0,
                            precision=1,
                            on_change=self._driver_update_callback,
                        )

                with ui.item():
                    with ui.item_section().props("no-wrap"):
                        ui.item_label("Defense")
                    with ui.item_section().props("side"):
                        self.driver_defense_input = ui.number(
                            value=0,
                            min=0,
                            precision=1,
                            on_change=self._driver_update_callback,
                        )

                with ui.item():
                    with ui.item_section().props("no-wrap"):
                        ui.item_label("Health")
                    with ui.item_section().props("side"):
                        self.driver_health_input = ui.number(
                            value=0,
                            min=0,
                            precision=1,
                            on_change=self._driver_update_callback,
                        )

                with ui.item():
                    with ui.item_section().props("no-wrap"):
                        ui.item_label("Crit Damage")
                    with ui.item_section().props("side"):
                        self.driver_crit_damage_input = ui.number(
                            value=0,
                            min=0,
                            precision=1,
                            on_change=self._driver_update_callback,
                        )

    @override
    def get_model_assumptions(self) -> list[ModelAssumption]:
        return [
            ModelAssumption(
                icon="car_crash",
                description="Sinveiler is modeled as a summoned snapshot of Koleda's stats and refreshed when Koleda stats change. Let's Go For a Spin! modifies Sinveiler's initial stats.",
            ),
        ]
