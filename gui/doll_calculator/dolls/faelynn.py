from typing import Any, cast, override

from nicegui import ui

from core.buffs import MAX_TILE_ASCENSION_LEVEL
from core.dolls import faelynn
from core.types import DamageTag, FortificationLevel, SpecialAttribute, StatType
from gui.templates.doll_calculator_page import DollCalculatorPage, ModelAssumption
from gui.templates.rotation_planner import RotationPlanner

sample_rotation: dict[int, list[dict]] = {}


class Faelynn(DollCalculatorPage):
    """Page for Faelynn."""

    def __init__(self):
        super().__init__()

        self.doll = faelynn.Faelynn()
        self.doll.set_fortification_level(FortificationLevel.SEGMENT06)
        self.doll_subtitle: str = """Combo Attack / Tile

            Sentinel / Corrosion"""
        self.dandegate_link: str = "https://www.dandegate.net/dolls/faelynn"
        self.doll_portrait: str = "resources/faelynn.webp"

    @override
    def update_doll_abilities(self) -> None:
        doll = cast(faelynn.Faelynn, self.doll)

        hunters_tracking_stack_options: list[int] = [n for n in range(7)]
        targets_hit_options: list[int] = [n for n in range(1, 10)]

        self.option_config: dict[str, dict[str, Any]] = {
            "Cuspid Combo": {
                "fields": [],
                "function": doll.cuspid_combo.execute,
            },
            "Triple Maule": {
                "fields": [
                    {
                        "key": "stacks_of_hunters_tracking",
                        "type": "select",
                        "label": "Stacks of Hunter's Tracking",
                        "options": hunters_tracking_stack_options,
                        "default": 6,
                    },
                ],
                "function": doll.triple_maule.execute,
            },
            "Triple Maule (follow-up)": {
                "fields": [
                    {
                        "key": "number_of_targets_hit",
                        "type": "select",
                        "label": "Targets Hit",
                        "options": targets_hit_options,
                        "default": 1,
                    },
                    {
                        "key": "boss_was_hit",
                        "type": "checkbox",
                        "label": "Boss Hit",
                        "default": True,
                    },
                ],
                "function": doll.triple_maule_followup.execute,
            },
            "Scent Mark": {
                "fields": [],
                "function": doll.scent_mark.execute,
            },
            "Loyal Hunt": {
                "fields": [
                    {
                        "key": "stacks_of_hunters_tracking",
                        "type": "select",
                        "label": "Stacks of Hunter's Tracking",
                        "options": hunters_tracking_stack_options,
                        "default": 6,
                    },
                ],
                "function": doll.loyal_hunt.execute,
            },
            "Hunter's Instinct I": {
                "fields": [
                    {
                        "key": "stacks_of_hunters_tracking",
                        "type": "select",
                        "label": "Stacks of Hunter's Tracking",
                        "options": hunters_tracking_stack_options,
                        "default": 6,
                    },
                    {
                        "key": "number_of_targets_hit",
                        "type": "select",
                        "label": "Targets Hit",
                        "options": targets_hit_options,
                        "default": 1,
                    },
                ],
                "function": doll.hunters_instinct_i.execute,
            },
            "Hunter's Instinct II": {
                "fields": [
                    {
                        "key": "stacks_of_hunters_tracking",
                        "type": "select",
                        "label": "Stacks of Hunter's Tracking",
                        "options": hunters_tracking_stack_options,
                        "default": 6,
                    },
                    {
                        "key": "number_of_targets_hit",
                        "type": "select",
                        "label": "Targets Hit",
                        "options": targets_hit_options,
                        "default": 1,
                    },
                    {
                        "key": "has_collar_brand",
                        "type": "checkbox",
                        "label": "Collar Brand",
                        "default": True,
                    },
                ],
                "function": doll.hunters_instinct_ii.execute,
            },
            "Hunter's Instinct III": {
                "fields": [
                    {
                        "key": "stacks_of_hunters_tracking",
                        "type": "select",
                        "label": "Stacks of Hunter's Tracking",
                        "options": hunters_tracking_stack_options,
                        "default": 6,
                    },
                    {
                        "key": "number_of_targets_hit",
                        "type": "select",
                        "label": "Targets Hit",
                        "options": targets_hit_options,
                        "default": 1,
                    },
                    {
                        "key": "has_collar_brand",
                        "type": "checkbox",
                        "label": "Collar Brand",
                        "default": False,
                    },
                    {
                        "key": "target_tile_ascension_level",
                        "type": "select",
                        "label": "Target Tile Ascension Level",
                        "options": [n for n in range(0, MAX_TILE_ASCENSION_LEVEL + 1)],
                        "default": 3,
                    },
                ],
                "function": doll.hunters_instinct_iii.execute,
            },
        }

    @override
    def set_initial_values(self) -> None:
        doll = cast(faelynn.Faelynn, self.doll)

        # Initial stats copied from Nemesis: Gnosis pending Faelynn-specific values.
        doll.initial_stats.basic_attributes[StatType.ATTACK] = 4210
        doll.initial_stats.basic_attributes[StatType.CRIT_RATE] = 99
        doll.initial_stats.basic_attributes[StatType.CRIT_DAMAGE] = 175

        doll.additive_modifiers.special_attributes[
            SpecialAttribute.DAMAGE_BOOST
        ].set_multiplier(DamageTag.ALL, 7)

        doll.additive_modifiers.special_attributes[
            SpecialAttribute.DAMAGE_BOOST
        ].set_multiplier(DamageTag.CORROSION, 20)

        doll.additive_modifiers.special_attributes[
            SpecialAttribute.DAMAGE_BOOST
        ].set_multiplier(DamageTag.PHASE, 15)

        doll.additive_modifiers.special_attributes[
            SpecialAttribute.DAMAGE_BOOST
        ].set_multiplier(DamageTag.ULTIMATE, 12)

        doll.additive_modifiers.special_attributes[
            SpecialAttribute.DAMAGE_BOOST
        ].set_multiplier(DamageTag.PASSIVE, 8)

        doll.additive_modifiers.special_attributes[
            SpecialAttribute.CRITICAL_DAMAGE
        ].set_multiplier(DamageTag.ALL, 3)

        doll.multiplicative_modifiers.basic_attributes[StatType.ATTACK] = 11

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
            self.rotation_planner = RotationPlanner(options_config=self.option_config)
            self.rotation_planner.set_data(sample_rotation)
