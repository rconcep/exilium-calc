from nicegui import ui

from gui.templates.doll_calculator_page import DollCalculatorPage, ModelAssumption
from gui.templates.rotation_planner import RotationPlanner
from typing import Any, cast, override
from core.types import DamageTag, FortificationLevel, SpecialAttribute, StatType
from core.dolls import liushih

_t1: list[dict[str, Any]] = [
    {"name": "Desperate Gambit"},
    {"name": "One Doll Cavalry"},
    {"name": "Gatling Cannon (Pegasus)", "stacks_of_marksmanship": 6},
    {"name": "Gatling Cannon (Pegasus)", "stacks_of_marksmanship": 6},
]

_t2: list[dict[str, Any]] = [
    {"name": "Desperate Gambit"},
    {"name": "Gatling Cannon (Pegasus)", "stacks_of_marksmanship": 12},
    {"name": "Gatling Cannon (Pegasus)", "stacks_of_marksmanship": 12},
    {"name": "Line Breaker", "stacks_of_marksmanship": 12},
    {"name": "Gatling Cannon (Pegasus)", "stacks_of_marksmanship": 12},
    {"name": "Gatling Cannon (Pegasus)", "stacks_of_marksmanship": 12},
]


sample_rotation: dict[int, list[dict]] = {
    1: _t1,
    2: _t2,
    3: _t2,
    4: _t2,
    5: _t2,
    6: _t2,
    7: _t2,
}


class Liushih(DollCalculatorPage):
    """Page for Liushih."""

    def __init__(self):
        super().__init__()

        self._liushih: liushih.Liushih = liushih.Liushih()
        self.doll = self._liushih
        self.doll.set_fortification_level(FortificationLevel.SEGMENT06)
        self.doll_subtitle: str = """Summon / Load Attack

            Sentinel / Hydro"""
        self.dandegate_link: str = "https://www.dandegate.net/dolls/liushih"
        self.doll_portrait: str = "resources/liushih.webp"

    @override
    def update_doll_abilities(self) -> None:
        doll = cast(liushih.Liushih, self.doll)

        self.option_config: dict[str, dict[str, Any]] = {
            "Line Breaker": {
                "fields": [
                    {
                        "key": "stacks_of_marksmanship",
                        "label": "Stacks of Marksmanship",
                        "type": "select",
                        "options": list(range(13)),
                        "default": 12,
                    }
                ],
                "function": doll.line_breaker.execute,
            },
            "Desperate Gambit": {
                "fields": [],
                "function": doll.desperate_gambit.execute,
            },
            "One Doll Cavalry": {
                "fields": [],
                "function": doll.one_doll_cavalry.execute,
            },
            "Gatling Cannon (Pegasus)": {
                "fields": [
                    {
                        "key": "stacks_of_marksmanship",
                        "label": "Stacks of Marksmanship",
                        "type": "select",
                        "options": list(range(13)),
                        "default": 12,
                    }
                ],
                "function": doll.gatling_cannon.execute,
            },
        }

        self.add_elemental_tile_actions_for_element(
            self.option_config,
            DamageTag.HYDRO,
        )

    @override
    def set_initial_values(self) -> None:
        # Using Springfield's stats as initial values
        self.doll.initial_stats.basic_attributes[StatType.ATTACK] = 600
        self.doll.initial_stats.basic_attributes[StatType.HEALTH] = 15700
        self.doll.initial_stats.basic_attributes[StatType.CRIT_RATE] = 90
        self.doll.initial_stats.basic_attributes[StatType.CRIT_DAMAGE] = 168

        # Radiance: 2.5
        # Key: 7
        # Key: 7
        # Imagoform Shoot: 4
        self.doll.additive_modifiers.special_attributes[
            SpecialAttribute.DAMAGE_BOOST
        ].set_multiplier(DamageTag.ALL, 20.5)

        # Shadow Runner: 20
        # Attachment: 20
        # Imagoform Embryo: 3
        # Imagoform Sprout: 5
        self.doll.additive_modifiers.special_attributes[
            SpecialAttribute.DAMAGE_BOOST
        ].set_multiplier(DamageTag.HYDRO, 48)

        # Key: 10
        self.doll.additive_modifiers.special_attributes[
            SpecialAttribute.DAMAGE_BOOST
        ].set_multiplier(DamageTag.PHASE, 10)

        # Imagoform Bud: 4
        # Attack Unity: 1
        # Fighting Spirit: 1.8
        self.doll.multiplicative_modifiers.basic_attributes[StatType.ATTACK] = 6.8

        # Ichor Conversion: 0.8% of initial max HP
        self.doll.additive_modifiers.basic_attributes[StatType.ATTACK] = (
            0.008 * self.doll.initial_stats.basic_attributes[StatType.HEALTH]
        )

        # Imagoform Bud: 4
        # Fighting Spirit: 1.8
        # HP Boost: 3.6
        # Radiance: 15
        self.doll.multiplicative_modifiers.basic_attributes[StatType.HEALTH] = 24.4

        # Ichor Resonance: 0.4% of initial Attack
        self.doll.additive_modifiers.basic_attributes[StatType.HEALTH] = (
            0.004 * self.doll.initial_stats.basic_attributes[StatType.ATTACK]
        )

        # Shadow Runner: 15
        self.doll.additive_modifiers.special_attributes[
            SpecialAttribute.CRITICAL_DAMAGE
        ].set_multiplier(DamageTag.BASIC, 15)

        # Sync Pegasus now that real stats are in place.
        self._liushih.refresh_pegasus()

    def get_default_damage_calculator_buffs(self) -> list[dict[str, Any]]:
        return [
            {"name": "Attack Up II"},
            {
                "name": "Overflowing Care",
                "springfield_fortification_level": FortificationLevel.SEGMENT06,
                "percent_excess_healing": 105,
            },
            {
                "name": "Deep-Rooted Bonds",
            },
            {
                "name": "Eagle's Vigilance (Taryz)",
                "springfield_fortification_level": FortificationLevel.SEGMENT06,
            },
            {
                "name": "Boldness",
                "liushih_fortification_level": FortificationLevel.SEGMENT06,
                "stacks": 6,
            },
            {
                "name": "Joint Ops (Liushih)",
                "liushih_fortification_level": FortificationLevel.SEGMENT06,
            },
        ]

    def get_default_damage_calculator_debuffs(self) -> list[dict[str, Any]]:
        return [
            {"name": "Defense Down II"},
            {
                "name": "False Intelligence",
                "springfield_fortification_level": FortificationLevel.SEGMENT06,
            },
            {
                "name": "Taryz",
                "springfield_fortification_level": FortificationLevel.SEGMENT06,
            },
            {
                "name": "Vulnerability Analysis",
                "springfield_fortification_level": FortificationLevel.SEGMENT06,
                "stacks": 3,
            },
            {"name": "Lock On (Liushih)"},
        ]

    @override
    def stats_update_callback(self, update: ui.number) -> None:  # type: ignore[override]
        # Keep Pegasus's snapshot current before deepcopy is taken
        # for every damage calculation inside the parent's callback.
        self._liushih.refresh_pegasus()
        super().stats_update_callback(update)

    @override
    def get_model_assumptions(self) -> list[ModelAssumption]:
        return [
            ModelAssumption(
                icon="people",
                description="Liushih's passive 'Shared Vengeance' increases the basic attack damage multiplier based on her initial attack but only in Damage Calculator.",
            ),
            ModelAssumption(
                icon="bedroom_baby",
                description="Pegasus inherits Liushih's stats at the time of summoning and is refreshed before each calculation.",
            ),
            ModelAssumption(
                icon="water_drop",
                description="Sample rotation relies on Springfield for Shared Telepathy support.",
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
