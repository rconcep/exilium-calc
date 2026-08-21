from typing import Any, cast, override

from nicegui import ui

from core.dolls import nemesis_gnosis
from core.types import DamageTag, FortificationLevel, SpecialAttribute, StatType
from gui.templates.doll_calculator_page import DollCalculatorPage, ModelAssumption
from gui.templates.rotation_planner import RotationPlanner

_calamity_resonance: dict = {"name": "Calamity Resonance"}
_fates_reprise: dict = {
    "name": "Fate's Reprise",
    "confectance_index_consumed": 6,
    "has_fifth_prophecy": True,
    "has_sixth_prophecy": False,
}
_support_action: dict = {"name": "Support Action", "has_judicial_privilege": True}

sample_rotation: dict[int, list[dict]] = {
    1: [
        _calamity_resonance,
        _fates_reprise,
        _support_action,
        _support_action,
        _support_action,
    ],
    2: [_fates_reprise, _support_action, _support_action, _support_action],
    3: [
        _calamity_resonance,
        _fates_reprise,
        _support_action,
        _support_action,
        _support_action,
    ],
    4: [_fates_reprise, _support_action, _support_action, _support_action],
    5: [
        _calamity_resonance,
        _fates_reprise,
        _support_action,
        _support_action,
        _support_action,
    ],
    6: [_fates_reprise, _support_action, _support_action, _support_action],
    7: [
        _calamity_resonance,
        _fates_reprise,
        _support_action,
        _support_action,
        _support_action,
    ],
}


class NemesisGnosis(DollCalculatorPage):
    """Page for Nemesis: Gnosis."""

    def __init__(self):
        super().__init__()

        self.doll = nemesis_gnosis.NemesisGnosis()
        self.doll.set_fortification_level(FortificationLevel.SEGMENT06)
        self.doll_subtitle: str = """Burst Damage / Prophecy Stacking

            Sentinel / Corrosion"""
        self.dandegate_link: str = "https://www.dandegate.net/dolls/nemesis-gnosis"
        self.doll_portrait: str = "resources/nemesis_gnosis.webp"

    @override
    def update_doll_abilities(self) -> None:
        doll = cast(nemesis_gnosis.NemesisGnosis, self.doll)

        self.option_config: dict[str, dict[str, Any]] = {
            "Starfall": {
                "fields": [],
                "function": doll.starfall.execute,
            },
            "Calamity Resonance": {
                "fields": [],
                "function": doll.calamity_resonance.execute,
            },
            "Prismatic Refraction": {
                "fields": [
                    {
                        "key": "has_first_prophecy",
                        "type": "checkbox",
                        "label": "First Prophecy: Resonance",
                        "default": True,
                    },
                    {
                        "key": "has_second_prophecy",
                        "type": "checkbox",
                        "label": "Second Prophecy: Solitude",
                        "default": True,
                    },
                    {
                        "key": "has_no_allies_nearby",
                        "type": "checkbox",
                        "label": "No Allies Within 4 Tiles",
                        "default": True,
                    },
                ],
                "function": doll.prismatic_refraction.execute,
            },
            "Fate's Reprise": {
                "fields": [
                    {
                        "key": "confectance_index_consumed",
                        "type": "select",
                        "label": "Confectance Index Consumed",
                        "options": [n for n in range(7)],
                        "default": 6,
                    },
                    {
                        "key": "has_fifth_prophecy",
                        "type": "checkbox",
                        "label": "Fifth Prophecy: Star Trail",
                        "default": True,
                    },
                    {
                        "key": "has_sixth_prophecy",
                        "type": "checkbox",
                        "label": "Sixth Prophecy: Event Horizon",
                        "default": True,
                    },
                ],
                "function": doll.fates_reprise.execute,
            },
            "Support Action": {
                "fields": [
                    {
                        "key": "has_judicial_privilege",
                        "type": "checkbox",
                        "label": "Judicial Privilege",
                        "default": True,
                    },
                ],
                "function": doll.support_action.execute,
            },
            "Third Prophecy": {
                "fields": [
                    {
                        "key": "triggered_out_of_turn",
                        "type": "checkbox",
                        "label": "Triggered Out of Turn",
                        "default": False,
                    },
                ],
                "function": doll.third_prophecy.execute,
            },
        }

    @override
    def set_initial_values(self) -> None:
        doll = cast(nemesis_gnosis.NemesisGnosis, self.doll)

        doll.initial_stats.basic_attributes[StatType.ATTACK] = 4210
        doll.initial_stats.basic_attributes[StatType.CRIT_RATE] = 99
        doll.initial_stats.basic_attributes[StatType.CRIT_DAMAGE] = 175

        # Attachments, common keys, imagoform, specialized traits
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

    def get_default_damage_calculator_buffs(self) -> list[dict[str, Any]]:
        return [
            {"name": "Attack Up II"},
        ]

    def get_default_damage_calculator_debuffs(self) -> list[dict[str, Any]]:
        return [
            {"name": "Defense Down II"},
        ]

    @override
    def get_model_assumptions(self) -> list[ModelAssumption]:
        return [
            ModelAssumption(
                icon="diversity_3",
                description="The damage dealt increase to Paradeus units is not modeled.",
            ),
            ModelAssumption(
                icon="cruelty_free",
                description="Sample rotation data assumes a single target, Boss target scenario: First Prophecy, Fourth Prophecy, and Fifth Prophecy active.",
            ),
        ]

    @override
    def get_rotation_planner(self) -> None:
        with ui.card().classes("w-full h-full"):

            def update_all():
                self.damage_instances = self.rotation_planner.get_all_actions()
                self.stats_update_callback(None)  # type: ignore

            ui.button("Update", on_click=update_all).classes("w-full")
            self.rotation_planner = RotationPlanner(options_config=self.option_config)
            self.rotation_planner.set_data(sample_rotation)
