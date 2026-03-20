from nicegui import ui

from gui.templates.doll_calculator_page import DollCalculatorPage
from gui.templates.rotation_planner import RotationPlanner
from typing import Any, override
from core.types import DamageTag, SpecialAttribute, StatType, FortificationLevel
from core.dolls import lewis


sample_rotation: dict[int, list[dict]] = {
    1: [
        {
            "name": "Surprising Funball",
        },
        {"name": "Volley Fire", "tin_soldier_rank": 2, "has_tin_soldiers_order": True},
        {"name": "Volley Fire", "tin_soldier_rank": 2, "has_tin_soldiers_order": True},
        {"name": "Volley Fire", "tin_soldier_rank": 2, "has_tin_soldiers_order": False},
        {"name": "Volley Fire", "tin_soldier_rank": 2, "has_tin_soldiers_order": False},
    ],
    2: [
        {"name": "Volley Fire", "tin_soldier_rank": 3, "has_tin_soldiers_order": False},
        {
            "name": "Toy Carnival",
            "cumulative_tin_soldier_ranks": 6,
            "highest_rank_tin_soldier": 3,
        },
        {"name": "Volley Fire", "tin_soldier_rank": 3, "has_tin_soldiers_order": False},
        {"name": "Volley Fire", "tin_soldier_rank": 3, "has_tin_soldiers_order": False},
        {"name": "Volley Fire", "tin_soldier_rank": 3, "has_tin_soldiers_order": False},
        {"name": "Volley Fire", "tin_soldier_rank": 3, "has_tin_soldiers_order": False},
    ],
    3: [
        {
            "name": "Surprising Funball",
        },
        {"name": "Volley Fire", "tin_soldier_rank": 3, "has_tin_soldiers_order": True},
        {"name": "Volley Fire", "tin_soldier_rank": 3, "has_tin_soldiers_order": True},
        {"name": "Volley Fire", "tin_soldier_rank": 3, "has_tin_soldiers_order": False},
        {"name": "Volley Fire", "tin_soldier_rank": 3, "has_tin_soldiers_order": False},
    ],
    4: [
        {"name": "Volley Fire", "tin_soldier_rank": 3, "has_tin_soldiers_order": False},
        {
            "name": "Toy Carnival",
            "cumulative_tin_soldier_ranks": 6,
            "highest_rank_tin_soldier": 3,
        },
        {"name": "Volley Fire", "tin_soldier_rank": 3, "has_tin_soldiers_order": False},
        {"name": "Volley Fire", "tin_soldier_rank": 3, "has_tin_soldiers_order": False},
        {"name": "Volley Fire", "tin_soldier_rank": 3, "has_tin_soldiers_order": False},
        {"name": "Volley Fire", "tin_soldier_rank": 3, "has_tin_soldiers_order": False},
    ],
    5: [
        {
            "name": "Surprising Funball",
        },
        {"name": "Volley Fire", "tin_soldier_rank": 3, "has_tin_soldiers_order": True},
        {"name": "Volley Fire", "tin_soldier_rank": 3, "has_tin_soldiers_order": True},
        {"name": "Volley Fire", "tin_soldier_rank": 3, "has_tin_soldiers_order": False},
        {"name": "Volley Fire", "tin_soldier_rank": 3, "has_tin_soldiers_order": False},
    ],
    6: [
        {"name": "Volley Fire", "tin_soldier_rank": 3, "has_tin_soldiers_order": False},
        {
            "name": "Toy Carnival",
            "cumulative_tin_soldier_ranks": 6,
            "highest_rank_tin_soldier": 3,
        },
        {"name": "Volley Fire", "tin_soldier_rank": 3, "has_tin_soldiers_order": False},
        {"name": "Volley Fire", "tin_soldier_rank": 3, "has_tin_soldiers_order": False},
        {"name": "Volley Fire", "tin_soldier_rank": 3, "has_tin_soldiers_order": False},
        {"name": "Volley Fire", "tin_soldier_rank": 3, "has_tin_soldiers_order": False},
    ],
    7: [
        {
            "name": "Surprising Funball",
        },
        {"name": "Volley Fire", "tin_soldier_rank": 3, "has_tin_soldiers_order": True},
        {"name": "Volley Fire", "tin_soldier_rank": 3, "has_tin_soldiers_order": True},
        {"name": "Volley Fire", "tin_soldier_rank": 3, "has_tin_soldiers_order": False},
        {"name": "Volley Fire", "tin_soldier_rank": 3, "has_tin_soldiers_order": False},
    ],
}


class Lewis(DollCalculatorPage):
    """Page for Lewis."""

    def __init__(self):
        super().__init__()

        self.doll: lewis.Lewis = lewis.Lewis()
        self.doll.set_fortification_level(FortificationLevel.SEGMENT06)
        self.doll_subtitle: str = """Single Target Burst / Summon

            Sentinel / Burn"""
        self.dandegate_link: str = "https://www.dandegate.net/dolls/lewis"
        self.doll_portrait: str = (
            "resources/lewis.webp"
        )

    @override
    def update_doll_abilities(self) -> None:
        self.option_config: dict[str, dict[str, Any]] = {
            "Playtime": {"fields": [], "function": self.doll.playtime.execute},
            "Bad Guy Cleanup": {
                "fields": [],
                "function": self.doll.bad_guy_cleanup.execute,
            },
            "Surprising Funball": {
                "fields": [],
                "function": self.doll.surprising_funball.execute,
            },
            "Toy Carnival": {
                "fields": [
                    {
                        "key": "cumulative_tin_soldier_ranks",
                        "type": "number",
                        "label": "Sum of all Tin Soldier Ranks",
                        "default": 6,
                    },
                    {
                        "key": "highest_rank_tin_soldier",
                        "type": "number",
                        "label": "Highest Rank Tin Soldier",
                        "default": 3,
                    },
                ],
                "function": self.doll.toy_carnival.execute,
            },
            "Volley Fire": {
                "fields": [
                    {
                        "key": "tin_soldier_rank",
                        "type": "number",
                        "label": "Rank of Tin Soldier",
                        "default": 3,
                    },
                    {
                        "key": "has_tin_soldiers_order",
                        "type": "checkbox",
                        "label": "Tin Soldier's Order",
                        "default": True,
                    },
                ],
                "function": self.doll.volley_fire.execute,
            },
        }

    @override
    def set_initial_values(self) -> None:
        self.doll.initial_stats.special_attributes[
            SpecialAttribute.DAMAGE_BOOST
        ].set_multiplier(
            DamageTag.BURN, 30
        )  # Embers
        self.doll.initial_stats.basic_attributes[StatType.ATTACK] = 5429
        self.doll.initial_stats.basic_attributes[StatType.CRIT_RATE] = 78.9
        self.doll.initial_stats.basic_attributes[StatType.CRIT_DAMAGE] = 156.9

        self.doll.additive_modifiers.basic_attributes[StatType.CRIT_DAMAGE] = 20

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
