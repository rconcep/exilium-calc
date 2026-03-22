from nicegui import ui

from gui.templates.doll_calculator_page import DollCalculatorPage
from gui.templates.rotation_planner import RotationPlanner
from typing import Any, override
from core.types import DamageTag, SpecialAttribute, StatType, FortificationLevel
from core.dolls import mosin_nagant


sample_rotation: dict[int, list[dict]] = {
    1: [
        {"name": "Support Action", "has_active_engagement": True},
        {"name": "Support Action", "has_active_engagement": True},
        {"name": "Support Action", "has_active_engagement": True},
        {"name": "Declaration of Victory", "has_active_engagement": True},
    ],
    2: [
        {"name": "Support Action", "has_active_engagement": True},
        {"name": "Support Action", "has_active_engagement": True},
        {"name": "Support Action", "has_active_engagement": True},
        {"name": "Declaration of Victory", "has_active_engagement": True},
    ],
    3: [
        {"name": "Support Action", "has_active_engagement": True},
        {"name": "Support Action", "has_active_engagement": True},
        {"name": "Support Action", "has_active_engagement": True},
        {"name": "Declaration of Victory", "has_active_engagement": True},
    ],
    4: [
        {"name": "Support Action", "has_active_engagement": True},
        {"name": "Support Action", "has_active_engagement": True},
        {"name": "Support Action", "has_active_engagement": True},
        {"name": "Declaration of Victory", "has_active_engagement": True},
    ],
    5: [
        {"name": "Support Action", "has_active_engagement": True},
        {"name": "Support Action", "has_active_engagement": True},
        {"name": "Support Action", "has_active_engagement": True},
        {"name": "Declaration of Victory", "has_active_engagement": True},
    ],
    6: [
        {"name": "Support Action", "has_active_engagement": True},
        {"name": "Support Action", "has_active_engagement": True},
        {"name": "Support Action", "has_active_engagement": True},
        {"name": "Declaration of Victory", "has_active_engagement": True},
    ],
    7: [
        {"name": "Support Action", "has_active_engagement": True},
        {"name": "Support Action", "has_active_engagement": True},
        {"name": "Support Action", "has_active_engagement": True},
        {"name": "Declaration of Victory", "has_active_engagement": True},
    ],
}


class MosinNagant(DollCalculatorPage):
    """Page for Mosin-Nagant"""

    def __init__(self):
        super().__init__()

        self.doll: mosin_nagant.MosinNagant = mosin_nagant.MosinNagant()
        self.doll.set_fortification_level(FortificationLevel.SEGMENT06)
        self.doll_subtitle: str = """Single Target Burst / Assist / Control

            Sentinel / Electric"""
        self.dandegate_link: str = "https://www.dandegate.net/dolls/mosin-nagant"
        self.doll_portrait: str = "resources/mosin-nagant.webp"

    @override
    def update_doll_abilities(self) -> None:
        self.option_config: dict[str, dict[str, Any]] = {
            "Patrol Time": {
                "fields": [
                    {
                        "key": "has_active_engagement",
                        "type": "checkbox",
                        "label": "Active Engagement",
                        "default": True,
                    }
                ],
                "function": self.doll.patrol_time.execute,
            },
            "Target Victory": {
                "fields": [
                    {
                        "key": "has_active_engagement",
                        "type": "checkbox",
                        "label": "Active Engagement",
                        "default": True,
                    }
                ],
                "function": self.doll.target_victory.execute,
            },
            "Declaration of Victory": {
                "fields": [
                    {
                        "key": "has_active_engagement",
                        "type": "checkbox",
                        "label": "Active Engagement",
                        "default": True,
                    }
                ],
                "function": self.doll.declaration_of_victory.execute,
            },
            "Support Action": {
                "fields": [
                    {
                        "key": "has_active_engagement",
                        "type": "checkbox",
                        "label": "Active Engagement",
                        "default": True,
                    }
                ],
                "function": self.doll.support_action.execute,
            },
        }

    @override
    def set_initial_values(self) -> None:
        self.doll.initial_stats.basic_attributes[StatType.ATTACK] = 3964
        self.doll.initial_stats.basic_attributes[StatType.CRIT_RATE] = 80.8
        self.doll.initial_stats.basic_attributes[StatType.CRIT_DAMAGE] = 177

        self.doll.additive_modifiers.special_attributes[
            SpecialAttribute.DAMAGE_BOOST
        ].set_multiplier(DamageTag.PHASE, 25)
        self.doll.additive_modifiers.special_attributes[
            SpecialAttribute.DAMAGE_BOOST
        ].set_multiplier(DamageTag.PASSIVE, 16.8)
        self.doll.additive_modifiers.special_attributes[
            SpecialAttribute.DAMAGE_BOOST
        ].set_multiplier(DamageTag.ELECTRIC, 5)
        self.doll.additive_modifiers.special_attributes[
            SpecialAttribute.DAMAGE_BOOST
        ].set_multiplier(DamageTag.SUPPORT_ACTION, 5)
        self.doll.additive_modifiers.special_attributes[
            SpecialAttribute.DAMAGE_BOOST
        ].set_multiplier(DamageTag.TARGETED, 3.5)

        self.doll.additive_modifiers.special_attributes[
            SpecialAttribute.CRITICAL_DAMAGE
        ].set_multiplier(DamageTag.PASSIVE, 6.8)
        self.doll.additive_modifiers.special_attributes[
            SpecialAttribute.CRITICAL_DAMAGE
        ].set_multiplier(DamageTag.ELECTRIC, 0.6)
        self.doll.additive_modifiers.special_attributes[
            SpecialAttribute.CRITICAL_DAMAGE
        ].set_multiplier(DamageTag.SUPPORT_ACTION, 5)
        self.doll.additive_modifiers.special_attributes[
            SpecialAttribute.CRITICAL_DAMAGE
        ].set_multiplier(DamageTag.TARGETED, 3)

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
