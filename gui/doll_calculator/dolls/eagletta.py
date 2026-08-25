from nicegui import ui

from gui.templates.doll_calculator_page import DollCalculatorPage, ModelAssumption
from gui.templates.rotation_planner import RotationPlanner
from typing import Any, cast, override
from core.types import (
    StatType,
    FortificationLevel,
    SpecialAttribute,
    DamageTag,
)
from core.dolls import eagletta


class Eagletta(DollCalculatorPage):
    """Page for Eagletta."""

    def __init__(self):
        super().__init__()

        self.doll: eagletta.Eagletta = eagletta.Eagletta()
        self.doll.set_fortification_level(FortificationLevel.SEGMENT06)
        self.doll_subtitle: str = """Burst Damage / Stance Switching

            Sentinel / Freeze"""
        self.dandegate_link: str = "https://www.dandegate.net/dolls/eagletta"
        self.doll_portrait: str = "resources/eagletta.webp"

    @override
    def update_doll_abilities(self) -> None:
        self.option_config: dict[str, dict[str, Any]] = {
            "Rending Talons": {
                "fields": [
                    {
                        "key": "feathers_of_war_expended",
                        "type": "select",
                        "options": [n for n in range(0, 8)],
                        "label": "Feathers of War expended this round",
                        "default": 7,
                    },
                ],
                "function": self.doll.rending_talons.execute,
            },
            "Swift Eagle Strike": {
                "fields": [],
                "function": self.doll.swift_eagle_strike.execute,
            },
            "Stoop Strike": {
                "fields": [],
                "function": self.doll.stoop_strike.execute,
            },
            "Featherstorm Feast": {
                "fields": [
                    {
                        "key": "feathers_of_war_expended",
                        "type": "select",
                        "options": [n for n in range(0, 8)],
                        "label": "Feathers of War expended this round",
                        "default": 7,
                    },
                    {
                        "key": "triggered_by_swift_eagle_strike",
                        "type": "checkbox",
                        "label": "Triggered by Swift Eagle Strike",
                        "default": False,
                    },
                ],
                "function": self.doll.featherstorm_feast.execute,
            },
            "Predation": {
                "fields": [
                    {
                        "key": "in_heavy_talons_stance",
                        "type": "checkbox",
                        "label": "In Heavy Talons Stance",
                        "default": True,
                    },
                    {
                        "key": "feathers_of_war_expended",
                        "type": "select",
                        "options": [n for n in range(0, 8)],
                        "label": "Feathers of War expended this round",
                        "default": 7,
                    },
                ],
                "function": self.doll.predation.execute,
            },
        }

        self.add_elemental_tile_actions_for_element(
            self.option_config,
            DamageTag.FREEZE,
        )

    @override
    def set_initial_values(self) -> None:
        doll = cast(eagletta.Eagletta, self.doll)

        doll.initial_stats.basic_attributes[StatType.ATTACK] = 4300
        doll.initial_stats.basic_attributes[StatType.CRIT_RATE] = 99
        doll.initial_stats.basic_attributes[StatType.CRIT_DAMAGE] = 175

        # Attachments, common keys, imagoform, specialized traits

        # imagoform: 5+12
        # CQC elite: 0.4
        # Alva 6P33: 10
        # Imagoform (Shoot): 4+3
        doll.additive_modifiers.special_attributes[
            SpecialAttribute.DAMAGE_BOOST
        ].set_multiplier(DamageTag.ALL, 17 + 0.4 + 10 + 4 + 3)

        # weapon: 20
        # attachment: 20
        # imagoform: 5
        # freeze boost: 1.5
        # Alva Brumal Barrier: <Alva Attack>*2/500*1.5 = 22.8 at 3800 attack
        # Alva Covering Mode: 20
        # Freeze Unity: 0.9
        doll.additive_modifiers.special_attributes[
            SpecialAttribute.DAMAGE_BOOST
        ].set_multiplier(DamageTag.FREEZE, 20 + 20 + 5 + 1.5 + 22.8 + 20 + 0.9)

        # keys: 30
        doll.additive_modifiers.special_attributes[
            SpecialAttribute.DAMAGE_BOOST
        ].set_multiplier(DamageTag.PHASE, 30)

        # imagoform: 10
        doll.additive_modifiers.special_attributes[
            SpecialAttribute.DAMAGE_BOOST
        ].set_multiplier(DamageTag.STABILITY_BROKEN, 10)

        # thronebreaker: 5
        doll.additive_modifiers.special_attributes[
            SpecialAttribute.DAMAGE_BOOST
        ].set_multiplier(DamageTag.BOSS, 5)

        # smite boost: 2.4
        doll.additive_modifiers.special_attributes[
            SpecialAttribute.CRITICAL_DAMAGE
        ].set_multiplier(DamageTag.ALL, 2.4)

        # ambush mastery: 0.2
        doll.additive_modifiers.special_attributes[
            SpecialAttribute.CRITICAL_DAMAGE
        ].set_multiplier(DamageTag.PASSIVE, 0.2)

        # Alva 6P33: 10
        # Silver-Winged Pistis: 10
        doll.additive_modifiers.special_attributes[
            SpecialAttribute.CRITICAL_DAMAGE
        ].set_multiplier(DamageTag.FREEZE, 10 + 10)

        # Silver-Winged Pistis: 5
        doll.additive_modifiers.special_attributes[
            SpecialAttribute.DEFENSE_IGNORE
        ].set_multiplier(DamageTag.ON_PHASE_TILE, 5)

        # imagoform: 8
        # attack boost: 3.6
        # Alva Imagoform: 3
        doll.multiplicative_modifiers.basic_attributes[StatType.ATTACK] = 8 + 3.6 + 3

    @override
    def get_model_assumptions(self) -> list[ModelAssumption]:
        return []

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
