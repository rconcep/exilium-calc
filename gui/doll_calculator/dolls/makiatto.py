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
from core.dolls import makiatto


sample_rotation: dict[int, list[dict]] = {
    1: [
        {
            "name": "Cold Precision Shot (1st)",
        },
        {
            "name": "Cold Precision Shot (2nd)",
            "first_hit_was_critical": True,
        },
        {"name": "Interception"},
        {"name": "Interception"},
        {"name": "Interception"},
        {"name": "Interception"},
    ],
    2: [
        {
            "name": "Cold Precision Shot (1st)",
        },
        {
            "name": "Cold Precision Shot (2nd)",
            "first_hit_was_critical": True,
        },
        {"name": "Interception"},
        {"name": "Interception"},
        {"name": "Interception"},
        {"name": "Interception"},
    ],
    3: [
        {
            "name": "Cold Precision Shot (1st)",
        },
        {
            "name": "Cold Precision Shot (2nd)",
            "first_hit_was_critical": True,
        },
    ],
    4: [
        {
            "name": "Cold Precision Shot (1st)",
        },
        {
            "name": "Cold Precision Shot (2nd)",
            "first_hit_was_critical": True,
        },
        {"name": "Interception"},
        {"name": "Interception"},
        {"name": "Interception"},
        {"name": "Interception"},
    ],
    5: [
        {
            "name": "Cold Precision Shot (1st)",
        },
        {
            "name": "Cold Precision Shot (2nd)",
            "first_hit_was_critical": True,
        },
        {"name": "Interception"},
        {"name": "Interception"},
        {"name": "Interception"},
        {"name": "Interception"},
    ],
    6: [
        {
            "name": "Cold Precision Shot (1st)",
        },
        {
            "name": "Cold Precision Shot (2nd)",
            "first_hit_was_critical": True,
        },
    ],
    7: [
        {
            "name": "Cold Precision Shot (1st)",
        },
        {
            "name": "Cold Precision Shot (2nd)",
            "first_hit_was_critical": True,
        },
        {"name": "Interception"},
        {"name": "Interception"},
        {"name": "Interception"},
        {"name": "Interception"},
    ],
}


class Makiatto(DollCalculatorPage):
    """Page for Makiatto."""

    def __init__(self):
        super().__init__()

        self.doll: makiatto.Makiatto = makiatto.Makiatto()
        self.doll.set_fortification_level(FortificationLevel.SEGMENT06)
        self.doll_subtitle: str = """Single Target Damage / First Strike

            Sentinel / Freeze"""
        self.dandegate_link: str = "https://www.dandegate.net/dolls/makiatto"
        self.doll_portrait: str = "resources/makiatto.webp"

    @override
    def update_doll_abilities(self) -> None:
        self.option_config: dict[str, dict[str, Any]] = {
            "Lone Wolf Territory": {
                "fields": [],
                "function": self.doll.lone_wolf_territory.execute,
            },
            "Cold Precision Shot (1st)": {
                "fields": [],
                "function": self.doll.cold_precision_shot_first.execute,
            },
            "Cold Precision Shot (2nd)": {
                "fields": [
                    {
                        "key": "first_hit_was_critical",
                        "type": "checkbox",
                        "label": "First hit was critical",
                        "default": True,
                    }
                ],
                "function": self.doll.cold_precision_shot_second.execute,
            },
            "Professional Tactics": {
                "fields": [],
                "function": self.doll.professional_tactics.execute,
            },
            "Interception": {
                "fields": [],
                "function": self.doll.interception.execute,
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
    def get_model_assumptions(self) -> list[ModelAssumption]:
        return [
            ModelAssumption(
                icon="ac_unit",
                description="Target is assumed to be Frigid for Battlefield Insight.",
            ),
            ModelAssumption(
                icon="track_changes",
                description="Cold Precision Shot second hit (for V1+) is calculated separately.",
            ),
            ModelAssumption(
                icon="key",
                description="Expansion Key - Sniper's Lock is active.",
                link_label="Dandegate",
                link_target="https://www.dandegate.net/dolls/makiatto/keys/expansion-key-sniper-s-lock",
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
