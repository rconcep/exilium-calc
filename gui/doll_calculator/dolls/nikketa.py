from nicegui import ui

from gui.templates.doll_calculator_page import DollCalculatorPage
from gui.templates.rotation_planner import RotationPlanner
from typing import Any, override
from core.types import (
    StatType,
    FortificationLevel,
    SpecialAttribute,
    DamageTag,
)
from core.dolls import nikketa


sample_rotation: dict[int, list[dict]] = {
    1: [
        {"name": "Judgment Strike", "has_fixed_key_3": False},
        {"name": "K9 Deployment"},
        {"name": "Kulich's Counterattack"},
        {
            "name": "Righteous Verdict",
            "target_has_guilt": True,
            "confectance_index_spent": 0,
            "is_out_of_turn": True,
        },
        {"name": "Kulich's Counterattack"},
        {
            "name": "Righteous Verdict",
            "target_has_guilt": True,
            "confectance_index_spent": 0,
            "is_out_of_turn": True,
        },
    ],
    2: [
        {"name": "Judgment Strike", "has_fixed_key_3": False},
        {
            "name": "Righteous Verdict",
            "target_has_guilt": True,
            "confectance_index_spent": 3,
            "is_out_of_turn": False,
        },
        {"name": "Kulich's Counterattack"},
        {
            "name": "Righteous Verdict",
            "target_has_guilt": True,
            "confectance_index_spent": 0,
            "is_out_of_turn": True,
        },
        {"name": "Kulich's Counterattack"},
        {
            "name": "Righteous Verdict",
            "target_has_guilt": True,
            "confectance_index_spent": 0,
            "is_out_of_turn": True,
        },
    ],
    3: [
        {"name": "Judgment Strike", "has_fixed_key_3": False},
        {
            "name": "Righteous Verdict",
            "target_has_guilt": True,
            "confectance_index_spent": 3,
            "is_out_of_turn": False,
        },
        # Justice = 5 Triggers additional cast
        {
            "name": "Righteous Verdict",
            "target_has_guilt": True,
            "confectance_index_spent": 0,
            "is_out_of_turn": False,
        },
        {"name": "Kulich's Counterattack"},
        {
            "name": "Righteous Verdict",
            "target_has_guilt": True,
            "confectance_index_spent": 0,
            "is_out_of_turn": True,
        },
        {"name": "Kulich's Counterattack"},
        {
            "name": "Righteous Verdict",
            "target_has_guilt": True,
            "confectance_index_spent": 0,
            "is_out_of_turn": True,
        },
    ],
    4: [
        {"name": "Judgment Strike", "has_fixed_key_3": False},
        {
            "name": "Righteous Verdict",
            "target_has_guilt": True,
            "confectance_index_spent": 3,
            "is_out_of_turn": False,
        },
        {"name": "Kulich's Counterattack"},
        {
            "name": "Righteous Verdict",
            "target_has_guilt": True,
            "confectance_index_spent": 0,
            "is_out_of_turn": True,
        },
        {"name": "Kulich's Counterattack"},
        {
            "name": "Righteous Verdict",
            "target_has_guilt": True,
            "confectance_index_spent": 0,
            "is_out_of_turn": True,
        },
    ],
    5: [
        {"name": "Judgment Strike", "has_fixed_key_3": False},
        {
            "name": "Righteous Verdict",
            "target_has_guilt": True,
            "confectance_index_spent": 3,
            "is_out_of_turn": False,
        },
        # Justice = 5 Triggers additional cast
        {
            "name": "Righteous Verdict",
            "target_has_guilt": True,
            "confectance_index_spent": 0,
            "is_out_of_turn": False,
        },
        {"name": "Kulich's Counterattack"},
        {
            "name": "Righteous Verdict",
            "target_has_guilt": True,
            "confectance_index_spent": 0,
            "is_out_of_turn": True,
        },
        {"name": "Kulich's Counterattack"},
        {
            "name": "Righteous Verdict",
            "target_has_guilt": True,
            "confectance_index_spent": 0,
            "is_out_of_turn": True,
        },
    ],
    6: [
        {"name": "Judgment Strike", "has_fixed_key_3": False},
        {
            "name": "Righteous Verdict",
            "target_has_guilt": True,
            "confectance_index_spent": 3,
            "is_out_of_turn": False,
        },
        {"name": "Kulich's Counterattack"},
        {
            "name": "Righteous Verdict",
            "target_has_guilt": True,
            "confectance_index_spent": 0,
            "is_out_of_turn": True,
        },
        {"name": "Kulich's Counterattack"},
        {
            "name": "Righteous Verdict",
            "target_has_guilt": True,
            "confectance_index_spent": 0,
            "is_out_of_turn": True,
        },
    ],
    7: [
        {"name": "Judgment Strike", "has_fixed_key_3": False},
        {
            "name": "Righteous Verdict",
            "target_has_guilt": True,
            "confectance_index_spent": 3,
            "is_out_of_turn": False,
        },
        {"name": "Kulich's Counterattack"},
        {
            "name": "Righteous Verdict",
            "target_has_guilt": True,
            "confectance_index_spent": 0,
            "is_out_of_turn": True,
        },
        {"name": "Kulich's Counterattack"},
        {
            "name": "Righteous Verdict",
            "target_has_guilt": True,
            "confectance_index_spent": 0,
            "is_out_of_turn": True,
        },
    ],
}


class Nikketa(DollCalculatorPage):
    """Page for Nikketa."""

    def __init__(self):
        super().__init__()

        self.doll: nikketa.Nikketa = nikketa.Nikketa()
        self.doll.set_fortification_level(FortificationLevel.SEGMENT06)
        self.doll_subtitle: str = """Sustained Damage / Summon / Pursuit

            Sentinel / Hydro"""
        self.dandegate_link: str = "https://www.dandegate.net/dolls/nikketa"
        self.doll_portrait: str = "resources/nikketa.webp"

    @override
    def update_doll_abilities(self) -> None:
        self.option_config: dict[str, dict[str, Any]] = {
            "Active Deterrence": {
                "fields": [],
                "function": self.doll.active_deterrence.execute,
            },
            "K9 Deployment": {
                "fields": [],
                "function": self.doll.k9_deployment.execute,
            },
            "Judgment Strike": {
                "fields": [
                    {
                        "key": "has_fixed_key_3",
                        "type": "checkbox",
                        "label": "Fixed Key 3 - Valiant Aura",
                        "default": False,
                    },
                ],
                "function": self.doll.judgment_strike.execute,
            },
            "Righteous Verdict": {
                "fields": [
                    {
                        "key": "target_has_guilt",
                        "type": "checkbox",
                        "label": "Target Has Guilt",
                        "default": True,
                    },
                    {
                        "key": "confectance_index_spent",
                        "type": "select",
                        "label": "Confectance Index Spent",
                        "default": 4,
                        "options": [n for n in range(7)],
                    },
                    {
                        "key": "is_out_of_turn",
                        "type": "checkbox",
                        "label": "From Counterattack",
                        "default": False,
                    },
                ],
                "function": self.doll.righteous_verdict.execute,
            },
            "Kulich's Counterattack": {
                "fields": [],
                "function": self.doll.kulich_counterattack.execute,
            },
        }

    @override
    def set_initial_values(self) -> None:
        self.doll.initial_stats.basic_attributes[StatType.ATTACK] = 4830
        self.doll.initial_stats.basic_attributes[StatType.CRIT_RATE] = 81
        self.doll.initial_stats.basic_attributes[StatType.CRIT_DAMAGE] = 154.5

        # Attachments, common keys, imagoform, specialized traits

        # imagoform: 5+12
        # CQC elite: 0.4
        # Alva 6P33: 10
        # Imagoform (Shoot): 4+3
        # Dushevnaya Expansion Key: 10
        # Dushevnaya Passive: 10
        self.doll.additive_modifiers.special_attributes[
            SpecialAttribute.DAMAGE_BOOST
        ].set_multiplier(DamageTag.ALL, 17 + 0.4 + 10 + 4 + 3 + 10 + 10)

        # weapon: 15
        # attachment: 20
        # imagoform: 5
        # freeze boost: 1.5
        # Alva Brumal Barrier: <Alva Attack>*2/1000*1.5 = 11.4 at 3800 attack
        # Alva Covering Mode: 20
        # Freeze Unity: 0.9
        # Dushevnaya Expansion Key: 15+10
        # Dushevnaya Eulogistic Verse: 10
        # Dushevnaya Passive: 10
        # Dushevnaya Imagoform (Bud): 3
        self.doll.additive_modifiers.special_attributes[
            SpecialAttribute.DAMAGE_BOOST
        ].set_multiplier(
            DamageTag.FREEZE, 15 + 20 + 5 + 1.5 + 11.4 + 20 + 0.9 + 15 + 10 + 10 + 3
        )

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

        # thronebreaker: 5
        self.doll.additive_modifiers.special_attributes[
            SpecialAttribute.DAMAGE_BOOST
        ].set_multiplier(DamageTag.BOSS, 5)

        # smite boost: 2.4
        self.doll.additive_modifiers.special_attributes[
            SpecialAttribute.CRITICAL_DAMAGE
        ].set_multiplier(DamageTag.ALL, 2.4)

        # ambush mastery: 0.2
        self.doll.additive_modifiers.special_attributes[
            SpecialAttribute.CRITICAL_DAMAGE
        ].set_multiplier(DamageTag.PASSIVE, 0.2)

        # Alva 6P33: 10
        self.doll.additive_modifiers.special_attributes[
            SpecialAttribute.CRITICAL_DAMAGE
        ].set_multiplier(DamageTag.FREEZE, 10)

        # imagoform: 8
        # attack boost: 3.6
        # Alva Imagoform: 3
        self.doll.multiplicative_modifiers.basic_attributes[StatType.ATTACK] = (
            8 + 3.6 + 3
        )

    @override
    def revision_history(self) -> None:
        with ui.timeline(side="right"):
            ui.timeline_entry("", title="Initial version", subtitle="March 25, 2026")

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
