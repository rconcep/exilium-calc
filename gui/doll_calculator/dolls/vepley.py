from nicegui import ui

from gui.templates.doll_calculator_page import DollCalculatorPage
from gui.templates.rotation_planner import RotationPlanner
from typing import Any, cast, override
from core.types import (
    StatType,
    FortificationLevel,
    SpecialAttribute,
    DamageTag,
)
from core.dolls import vepley


sample_rotation: dict[int, list[dict]] = {
    1: [
        {"name": "Infectious Enthusiasm"},
    ],
    2: [
        {"name": "Exclusive Stage"},
    ],
    3: [
        {"name": "All Out Performance"},
    ],
    4: [
        {"name": "Infectious Enthusiasm"},
    ],
    5: [
        {"name": "Exclusive Stage"},
    ],
    6: [
        {"name": "Infectious Enthusiasm"},
    ],
    7: [
        {"name": "Exclusive Stage"},
    ],
}


class Vepley(DollCalculatorPage):
    """Page for Vepley."""

    def __init__(self):
        super().__init__()

        self.doll = vepley.Vepley()
        self.doll.set_fortification_level(FortificationLevel.SEGMENT06)
        self.doll_subtitle: str = """Physical Damage / Defense Ignore / Movement Debuffs

            Vanguard / Physical"""
        self.dandegate_link: str = "https://www.dandegate.net/dolls/vepley"
        self.doll_portrait: str = "resources/vepley.webp"

    @override
    def update_doll_abilities(self) -> None:
        doll = cast(vepley.Vepley, self.doll)

        self.option_config: dict[str, dict[str, Any]] = {
            "Live Interaction": {
                "fields": [],
                "function": doll.live_interaction.execute,
            },
            "All Out Performance": {
                "fields": [],
                "function": doll.all_out_performance.execute,
            },
            "Exclusive Stage": {
                "fields": [],
                "function": doll.exclusive_stage.execute,
            },
            "Infectious Enthusiasm": {
                "fields": [],
                "function": doll.infectious_enthusiasm.execute,
            },
        }

    @override
    def set_initial_values(self) -> None:
        doll = cast(vepley.Vepley, self.doll)

        doll.initial_stats.basic_attributes[StatType.ATTACK] = 3960
        doll.initial_stats.basic_attributes[StatType.CRIT_RATE] = 78.6
        doll.initial_stats.basic_attributes[StatType.CRIT_DAMAGE] = 135.5

        # Attachments, common keys, imagoform, specialized traits
        # attachment: 12
        # imagoform: 12
        # Yoohee imagoform: 4
        doll.additive_modifiers.special_attributes[
            SpecialAttribute.DAMAGE_BOOST
        ].set_multiplier(DamageTag.ALL, 12 + 12 + 4)

        # imagoform: 5
        # physical boost: 1.4
        doll.additive_modifiers.special_attributes[
            SpecialAttribute.DAMAGE_BOOST
        ].set_multiplier(DamageTag.PHYSICAL, 5 + 1.4)

        # attachment: 36
        # keys: 10
        # imagoform: 8
        doll.additive_modifiers.special_attributes[
            SpecialAttribute.DAMAGE_BOOST
        ].set_multiplier(DamageTag.MELEE, 36 + 10 + 8)

        # keys: 7
        # raid stance: 3
        doll.additive_modifiers.special_attributes[
            SpecialAttribute.DAMAGE_BOOST
        ].set_multiplier(DamageTag.PASSIVE, 7 + 3)

        # keys: 10
        doll.additive_modifiers.special_attributes[
            SpecialAttribute.DAMAGE_BOOST
        ].set_multiplier(DamageTag.AREA_OF_EFFECT, 10)

        # imagoform: 10
        doll.additive_modifiers.special_attributes[
            SpecialAttribute.DAMAGE_BOOST
        ].set_multiplier(DamageTag.STABILITY_BROKEN, 10)

        # thronebreaker: 5.5
        doll.additive_modifiers.special_attributes[
            SpecialAttribute.DAMAGE_BOOST
        ].set_multiplier(DamageTag.BOSS, 5.5)

        # smite boost: 2.4
        doll.additive_modifiers.special_attributes[
            SpecialAttribute.CRITICAL_DAMAGE
        ].set_multiplier(DamageTag.ALL, 2.4)

        # physical smite: 0.4
        doll.additive_modifiers.special_attributes[
            SpecialAttribute.CRITICAL_DAMAGE
        ].set_multiplier(DamageTag.PHYSICAL, 0.4)

        # ambush mastery: 0.2
        doll.additive_modifiers.special_attributes[
            SpecialAttribute.CRITICAL_DAMAGE
        ].set_multiplier(DamageTag.PASSIVE, 0.2)

        # Yoohee Imagoform: 5
        # Yoohee Sparkling Centerstage: 10
        doll.additive_modifiers.special_attributes[
            SpecialAttribute.DEFENSE_IGNORE
        ].set_multiplier(DamageTag.PHYSICAL, 5 + 10)

        # imagoform: 8
        # attack boost: 3.6
        # Yoohee imagoform: 3
        doll.multiplicative_modifiers.basic_attributes[StatType.ATTACK] = 8 + 3.6 + 3

    @override
    def revision_history(self) -> None:
        with ui.timeline(side="right"):
            ui.timeline_entry("", title="Initial version", subtitle="March 28, 2026")

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
