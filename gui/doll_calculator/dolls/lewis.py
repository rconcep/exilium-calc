from nicegui import ui

from gui.templates.doll_calculator_page import DollCalculatorPage, ModelAssumption
from gui.templates.rotation_planner import RotationPlanner
from typing import Any, override
from core.types import DamageTag, SpecialAttribute, StatType, FortificationLevel
from core.dolls import lewis
from core.combat import Overburn

sample_rotation: dict[int, list[dict]] = {
    1: [
        # Holders' Actions
        {"name": "Volley Fire", "tin_soldier_rank": 2, "has_tin_soldiers_order": False},
        {"name": "Volley Fire", "tin_soldier_rank": 2, "has_tin_soldiers_order": False},
        # End of Holders' Actions
        {"name": "Volley Fire", "tin_soldier_rank": 2, "has_tin_soldiers_order": False},
        {"name": "Volley Fire", "tin_soldier_rank": 2, "has_tin_soldiers_order": False},
        {
            "name": "Surprising Funball",
        },
        {"name": "Surprising Funball (Fixed)"},
    ],
    2: [
        # Holders' Actions
        {"name": "Volley Fire", "tin_soldier_rank": 3, "has_tin_soldiers_order": True},
        {"name": "Volley Fire", "tin_soldier_rank": 3, "has_tin_soldiers_order": True},
        # End of Holders' Actions
        {"name": "Volley Fire", "tin_soldier_rank": 3, "has_tin_soldiers_order": False},
        {"name": "Volley Fire", "tin_soldier_rank": 3, "has_tin_soldiers_order": False},
        # Rank III - Toy Carnival triggers
        {"name": "Volley Fire", "tin_soldier_rank": 3, "has_tin_soldiers_order": False},
        {"name": "Volley Fire", "tin_soldier_rank": 3, "has_tin_soldiers_order": False},
        {
            "name": "Toy Carnival",
            "cumulative_tin_soldier_ranks": 6,
            "highest_rank_tin_soldier": 3,
        },
    ],
    3: [
        # Holders' Actions
        {"name": "Volley Fire", "tin_soldier_rank": 3, "has_tin_soldiers_order": False},
        {"name": "Volley Fire", "tin_soldier_rank": 3, "has_tin_soldiers_order": False},
        # End of Holders' Actions
        {"name": "Volley Fire", "tin_soldier_rank": 3, "has_tin_soldiers_order": False},
        {"name": "Volley Fire", "tin_soldier_rank": 3, "has_tin_soldiers_order": False},
        {
            "name": "Surprising Funball",
        },
        {"name": "Surprising Funball (Fixed)"},
    ],
    4: [
        # Holders' Actions
        {"name": "Volley Fire", "tin_soldier_rank": 3, "has_tin_soldiers_order": True},
        {"name": "Volley Fire", "tin_soldier_rank": 3, "has_tin_soldiers_order": True},
        # End of Holders' Actions
        {"name": "Volley Fire", "tin_soldier_rank": 3, "has_tin_soldiers_order": False},
        {"name": "Volley Fire", "tin_soldier_rank": 3, "has_tin_soldiers_order": False},
        # Rank III - Toy Carnival triggers
        {"name": "Volley Fire", "tin_soldier_rank": 3, "has_tin_soldiers_order": False},
        {"name": "Volley Fire", "tin_soldier_rank": 3, "has_tin_soldiers_order": False},
        {
            "name": "Toy Carnival",
            "cumulative_tin_soldier_ranks": 6,
            "highest_rank_tin_soldier": 3,
        },
    ],
    5: [
        # Holders' Actions
        {"name": "Volley Fire", "tin_soldier_rank": 3, "has_tin_soldiers_order": False},
        {"name": "Volley Fire", "tin_soldier_rank": 3, "has_tin_soldiers_order": False},
        # End of Holders' Actions
        {"name": "Volley Fire", "tin_soldier_rank": 3, "has_tin_soldiers_order": False},
        {"name": "Volley Fire", "tin_soldier_rank": 3, "has_tin_soldiers_order": False},
        {
            "name": "Surprising Funball",
        },
        {"name": "Surprising Funball (Fixed)"},
    ],
    6: [
        # Holders' Actions
        {"name": "Volley Fire", "tin_soldier_rank": 3, "has_tin_soldiers_order": True},
        {"name": "Volley Fire", "tin_soldier_rank": 3, "has_tin_soldiers_order": True},
        # End of Holders' Actions
        {"name": "Volley Fire", "tin_soldier_rank": 3, "has_tin_soldiers_order": False},
        {"name": "Volley Fire", "tin_soldier_rank": 3, "has_tin_soldiers_order": False},
        # Rank III - Toy Carnival triggers
        {"name": "Volley Fire", "tin_soldier_rank": 3, "has_tin_soldiers_order": False},
        {"name": "Volley Fire", "tin_soldier_rank": 3, "has_tin_soldiers_order": False},
        {
            "name": "Toy Carnival",
            "cumulative_tin_soldier_ranks": 6,
            "highest_rank_tin_soldier": 3,
        },
    ],
    7: [
        # Holders' Actions
        {"name": "Volley Fire", "tin_soldier_rank": 3, "has_tin_soldiers_order": False},
        {"name": "Volley Fire", "tin_soldier_rank": 3, "has_tin_soldiers_order": False},
        # End of Holders' Actions
        {"name": "Volley Fire", "tin_soldier_rank": 3, "has_tin_soldiers_order": False},
        {"name": "Volley Fire", "tin_soldier_rank": 3, "has_tin_soldiers_order": False},
        {
            "name": "Surprising Funball",
        },
        {"name": "Surprising Funball (Fixed)"},
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
        self.doll_portrait: str = "resources/lewis.webp"

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
            "Surprising Funball (Fixed)": {
                "fields": [],
                "function": self.doll.surprising_funball_fixed.execute,
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
            "Overburn": {
                "fields": [],
                "function": Overburn().execute,
            },
        }

    @override
    def set_initial_values(self) -> None:
        self.doll.initial_stats.basic_attributes[StatType.ATTACK] = 4280
        self.doll.initial_stats.basic_attributes[StatType.CRIT_RATE] = 68.7
        self.doll.initial_stats.basic_attributes[StatType.CRIT_DAMAGE] = 145.2

        # Attachments, common keys, imagoform, specialized traits
        # keys: 7
        # imagoform: 5
        # imagoform: 12
        # Vector imagoform: 4
        self.doll.additive_modifiers.special_attributes[
            SpecialAttribute.DAMAGE_BOOST
        ].set_multiplier(DamageTag.ALL, 7 + 5 + 12 + 4)

        # attachment: 15
        # keys: 10:
        self.doll.additive_modifiers.special_attributes[
            SpecialAttribute.DAMAGE_BOOST
        ].set_multiplier(DamageTag.PASSIVE, 15 + 10)

        # Toysmith: 25
        # burn boost: 1.4
        # imagoform: 5
        # Vector imagoform: 3
        # burn unity: 0.9
        self.doll.additive_modifiers.special_attributes[
            SpecialAttribute.DAMAGE_BOOST
        ].set_multiplier(DamageTag.BURN, 25 + 1.4 + 5 + 3 + 0.9)

        # keys: 7
        # raid stance: 1.8
        self.doll.additive_modifiers.special_attributes[
            SpecialAttribute.DAMAGE_BOOST
        ].set_multiplier(DamageTag.PASSIVE, 7 + 1.8)

        # pinpoint spec: 3.5
        self.doll.additive_modifiers.special_attributes[
            SpecialAttribute.DAMAGE_BOOST
        ].set_multiplier(DamageTag.TARGETED, 3.5)

        # keys: 10
        # imagoform: 10
        # follow-up strike: 0.5
        self.doll.additive_modifiers.special_attributes[
            SpecialAttribute.DAMAGE_BOOST
        ].set_multiplier(DamageTag.STABILITY_BROKEN, 10 + 10 + 0.5)

        # thronebreaker: 5.5
        self.doll.additive_modifiers.special_attributes[
            SpecialAttribute.DAMAGE_BOOST
        ].set_multiplier(DamageTag.BOSS, 5.5)

        # smite boost: 2.4
        # tin soldiers: 15
        self.doll.additive_modifiers.special_attributes[
            SpecialAttribute.CRITICAL_DAMAGE
        ].set_multiplier(DamageTag.ALL, 15 + 2.4)

        # burning smite: 0.4
        self.doll.additive_modifiers.special_attributes[
            SpecialAttribute.CRITICAL_DAMAGE
        ].set_multiplier(DamageTag.BURN, 0.4)

        # precision blow: 3
        self.doll.additive_modifiers.special_attributes[
            SpecialAttribute.CRITICAL_DAMAGE
        ].set_multiplier(DamageTag.TARGETED, 3)

        # Toysmith: 20
        self.doll.additive_modifiers.special_attributes[
            SpecialAttribute.DEFENSE_IGNORE
        ].set_multiplier(DamageTag.ALL, 20)

        # imagoform: 8
        # attack boost: 3.6
        # Vector imagoform: 3
        # attack unity: 1
        self.doll.multiplicative_modifiers.basic_attributes[StatType.ATTACK] = (
            8 + 3.6 + 3 + 1
        )

    def get_default_damage_calculator_buffs(self) -> list[dict[str, Any]]:
        return [
            {"name": "Blazing Assault II"},
            {
                "name": "Accelerant (Vector)",
                "vector_fortification_level": FortificationLevel.SEGMENT06,
                "number_of_burn_buffs": 3,
            },
            {
                "name": "Rank (Lewis)",
                "lewis_fortification_level": FortificationLevel.SEGMENT06,
                "rank": 3,
            },
            {
                "name": "Rank (Lewis)",
                "lewis_fortification_level": FortificationLevel.SEGMENT06,
                "rank": 3,
            },
        ]

    def get_default_damage_calculator_debuffs(self) -> list[dict[str, Any]]:
        return [
            {"name": "Defense Down II"},
            {
                "name": "Overheat Combustion",
                "vector_fortification_level": FortificationLevel.SEGMENT06,
            },
            {"name": "Conflagration"},
            {
                "name": "Smolder",
                "vector_fortification_level": FortificationLevel.SEGMENT06,
                "number_of_burn_debuffs": 4,
            },
        ]

    @override
    def get_model_assumptions(self) -> list[ModelAssumption]:
        return [
            ModelAssumption(
                icon="whatshot",
                description="Sample rotation assumes Tin Soldier holders are triggering Volley Fire.",
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
