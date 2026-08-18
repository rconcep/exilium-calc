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
from core.dolls import nikketa

sample_rotation: dict[int, list[dict]] = {
    1: [
        {"name": "Judgment Strike", "has_fixed_key_3": False},
        {"name": "K9 Deployment"},
        {"name": "Counterattack (Kulich)"},
        {
            "name": "Righteous Verdict",
            "target_has_guilt": True,
            "confectance_index_spent": 0,
            "is_out_of_turn": True,
        },
        {"name": "Counterattack (Kulich)"},
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
        {"name": "Counterattack (Kulich)"},
        {
            "name": "Righteous Verdict",
            "target_has_guilt": True,
            "confectance_index_spent": 0,
            "is_out_of_turn": True,
        },
        {"name": "Counterattack (Kulich)"},
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
        {"name": "Counterattack (Kulich)"},
        {
            "name": "Righteous Verdict",
            "target_has_guilt": True,
            "confectance_index_spent": 0,
            "is_out_of_turn": True,
        },
        {"name": "Counterattack (Kulich)"},
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
        {"name": "Counterattack (Kulich)"},
        {
            "name": "Righteous Verdict",
            "target_has_guilt": True,
            "confectance_index_spent": 0,
            "is_out_of_turn": True,
        },
        {"name": "Counterattack (Kulich)"},
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
        {"name": "Counterattack (Kulich)"},
        {
            "name": "Righteous Verdict",
            "target_has_guilt": True,
            "confectance_index_spent": 0,
            "is_out_of_turn": True,
        },
        {"name": "Counterattack (Kulich)"},
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
        {"name": "Counterattack (Kulich)"},
        {
            "name": "Righteous Verdict",
            "target_has_guilt": True,
            "confectance_index_spent": 0,
            "is_out_of_turn": True,
        },
        {"name": "Counterattack (Kulich)"},
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
        {"name": "Counterattack (Kulich)"},
        {
            "name": "Righteous Verdict",
            "target_has_guilt": True,
            "confectance_index_spent": 0,
            "is_out_of_turn": True,
        },
        {"name": "Counterattack (Kulich)"},
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
            "Counterattack (Kulich)": {
                "fields": [],
                "function": self.doll.kulich_counterattack.execute,
            },
        }

        self.add_elemental_tile_actions_for_element(
            self.option_config,
            DamageTag.HYDRO,
        )

    @override
    def set_initial_values(self) -> None:
        self.doll.initial_stats.basic_attributes[StatType.ATTACK] = 4830
        self.doll.initial_stats.basic_attributes[StatType.CRIT_RATE] = 81
        self.doll.initial_stats.basic_attributes[StatType.CRIT_DAMAGE] = 154.5

        # Attachments, common keys, imagoform, specialized traits
        # Copied these from Robella

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
        ].set_multiplier(DamageTag.HYDRO, 10)

        # imagoform: 8
        # attack boost: 3.6
        # Support Imagoform (60): 3
        self.doll.multiplicative_modifiers.basic_attributes[StatType.ATTACK] = (
            8 + 3.6 + 3
        )

        # Sync Kulich's snapshot now that real stats are in place.
        self.doll.refresh_kulich()

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
                "name": "Clue",
                "stacks": 10,
                "nikketa_fortification_level": FortificationLevel.SEGMENT06,
            },
            {
                "name": "Justice",
                "stacks": 5,
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
            {
                "name": "Guilt",
                "nikketa_fortification_level": FortificationLevel.SEGMENT06,
            },
        ]

    @override
    def stats_update_callback(self, update: ui.number) -> None:  # type: ignore[override]
        # Keep Kulich's snapshot current before deepcopy is taken
        # for every damage calculation inside the parent's callback.
        self.doll.refresh_kulich()
        super().stats_update_callback(update)

    @override
    def get_model_assumptions(self) -> list[ModelAssumption]:
        return [
            ModelAssumption(
                icon="pets",
                description="Kulich is modeled as a summoned snapshot and refreshed when Nikketa stats change.",
            ),
            ModelAssumption(
                icon="balance",
                description="Kulich snapshot uses core stat ratios (Health 80%, ATK 80%, DEF 100%).",
            ),
            ModelAssumption(
                icon="key",
                description="Expansion Key - Justice is Always With You is active.",
                link_label="Dandegate",
                link_target="https://www.dandegate.net/dolls/nikketa/keys/expansion-key-justice-is-always-with-you",
            ),
            ModelAssumption(
                icon="key",
                description="Sample rotation assumes Fixed Key 1 - Righteous Doll is active.",
                link_label="Dandegate",
                link_target="https://www.dandegate.net/dolls/nikketa/keys/fixed-key-1-righteous-doll",
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
