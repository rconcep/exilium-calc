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
from core.dolls import mityl

# Sample rotation left blank for now.
sample_rotation: dict[int, list[dict]] = {}


class Mityl(DollCalculatorPage):
    """Page for Mityl."""

    def __init__(self):
        super().__init__()

        self.doll: mityl.Mityl = mityl.Mityl()
        self.doll.set_fortification_level(FortificationLevel.SEGMENT06)
        self.doll_subtitle: str = """AoE Damage / Agile Combat

            Sentinel / Hydro"""
        self.dandegate_link: str = "https://www.dandegate.net/dolls/mityl"
        self.doll_portrait: str = "resources/mityl.webp"

    @override
    def update_doll_abilities(self) -> None:
        self.option_config: dict[str, dict[str, Any]] = {
            "Assault Shot": {
                "fields": [],
                "function": self.doll.assault_shot.execute,
            },
            "Air Dash": {
                "fields": [
                    {
                        "key": "is_skill_reuse",
                        "type": "checkbox",
                        "label": "Second Use of Air Dash",
                        "default": False,
                    },
                ],
                "function": self.doll.air_dash.execute,
            },
            "Support Action (Self Hologram)": {
                "fields": [],
                "function": self.doll.support_action.execute,
            },
            "Aligned Resonance (Self Hologram)": {
                "fields": [],
                "function": self.doll.aligned_resonance.execute,
            },
            "Hologram Assault (Self Hologram)": {
                "fields": [],
                "function": self.doll.hologram_assault.execute,
            },
        }

        self.add_elemental_tile_actions_for_element(
            self.option_config,
            DamageTag.HYDRO,
        )

    @override
    def set_initial_values(self) -> None:
        # Base stats copied from Nikketa.
        self.doll.initial_stats.basic_attributes[StatType.ATTACK] = 4830
        self.doll.initial_stats.basic_attributes[StatType.CRIT_RATE] = 81
        self.doll.initial_stats.basic_attributes[StatType.CRIT_DAMAGE] = 154.5

        self.doll.additive_modifiers.special_attributes[
            SpecialAttribute.DAMAGE_BOOST
        ].set_multiplier(DamageTag.ALL, 17 + 0.4 + 10 + 4 + 3)

        self.doll.additive_modifiers.special_attributes[
            SpecialAttribute.DAMAGE_BOOST
        ].set_multiplier(DamageTag.HYDRO, 15 + 20 + 5 + 1.5 + 0.9 + 3)

        self.doll.additive_modifiers.special_attributes[
            SpecialAttribute.DAMAGE_BOOST
        ].set_multiplier(DamageTag.PHASE, 30)

        self.doll.additive_modifiers.special_attributes[
            SpecialAttribute.DAMAGE_BOOST
        ].set_multiplier(DamageTag.PASSIVE, 14 + 1)

        self.doll.additive_modifiers.special_attributes[
            SpecialAttribute.CRITICAL_DAMAGE
        ].set_multiplier(DamageTag.ALL, 2.4)

        self.doll.additive_modifiers.special_attributes[
            SpecialAttribute.CRITICAL_DAMAGE
        ].set_multiplier(DamageTag.HYDRO, 10)

        self.doll.multiplicative_modifiers.basic_attributes[StatType.ATTACK] = (
            8 + 3.6 + 3
        )

        # Sync Self Hologram's snapshot now that real stats are in place.
        self.doll.refresh_self_hologram()

    def get_default_damage_calculator_buffs(self) -> list[dict[str, Any]]:
        return [
            {"name": "Attack Up II"},
        ]

    def get_default_damage_calculator_debuffs(self) -> list[dict[str, Any]]:
        return [
            {"name": "Defense Down II"},
        ]

    @override
    def stats_update_callback(self, update: ui.number) -> None:  # type: ignore[override]
        # Keep Self Hologram's snapshot current before deepcopy is taken
        # for every damage calculation inside the parent's callback.
        self.doll.refresh_self_hologram()
        super().stats_update_callback(update)

    @override
    def get_model_assumptions(self) -> list[ModelAssumption]:
        return [
            ModelAssumption(
                icon="pets",
                description="Self Hologram is modeled as a summoned snapshot and refreshed when Mityl's stats change.",
            ),
            ModelAssumption(
                icon="balance",
                description="Self Hologram inherits Mityl's full initial stat snapshot (no stat ratio reduction).",
            ),
            ModelAssumption(
                icon="pets",
                description="Copy Holograms are not available.",
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
