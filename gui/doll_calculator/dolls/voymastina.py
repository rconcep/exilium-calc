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
from core.dolls import voymastina


sample_rotation: dict[int, list[dict]] = {
    1: [
        {"name": "Eye of the White Mastiff (Passive)"},
        {"name": "Sirius Fall (Passive)", "has_fixed_key_4": True},
        {"name": "Pile Bunker (Passive)"},
        {"name": "Lock-On Attack"},
        {"name": "Sirius Fall (Active)", "has_fixed_key_4": True},
    ],
    2: [
        {"name": "Sirius Fall (Passive)", "has_fixed_key_4": True},
        {"name": "Pile Bunker (Passive)"},
        {"name": "Lock-On Attack"},
        {"name": "Pile Bunker (Active)", "has_activated_fixed_key_6": True},
    ],
    3: [
        {"name": "Sirius Fall (Passive)", "has_fixed_key_4": True},
        {"name": "Pile Bunker (Passive)"},
        {"name": "Lock-On Attack"},
        {"name": "Sirius Fall (Active)", "has_fixed_key_4": True},
    ],
    4: [
        {"name": "Eye of the White Mastiff (Passive)"},
        {"name": "Sirius Fall (Passive)", "has_fixed_key_4": True},
        {"name": "Pile Bunker (Passive)"},
        {"name": "Lock-On Attack"},
        {"name": "Pile Bunker (Active)", "has_activated_fixed_key_6": True},
    ],
    5: [
        {"name": "Sirius Fall (Passive)", "has_fixed_key_4": True},
        {"name": "Pile Bunker (Passive)"},
        {"name": "Lock-On Attack"},
        {"name": "Sirius Fall (Active)", "has_fixed_key_4": True},
    ],
    6: [
        {"name": "Sirius Fall (Passive)", "has_fixed_key_4": True},
        {"name": "Pile Bunker (Passive)"},
        {"name": "Lock-On Attack"},
        {"name": "Pile Bunker (Active)", "has_activated_fixed_key_6": True},
    ],
    7: [
        {"name": "Sirius Fall (Passive)", "has_fixed_key_4": True},
        {"name": "Pile Bunker (Passive)"},
        {"name": "Lock-On Attack"},
        {"name": "Sirius Fall (Active)", "has_fixed_key_4": True},
    ],
}


class Voymastina(DollCalculatorPage):
    """ """

    def __init__(self):
        super().__init__()

        self.doll: voymastina.Voymastina = voymastina.Voymastina()
        self.doll.set_fortification_level(FortificationLevel.SEGMENT06)
        self.doll_subtitle: str = """Melee Damage / Ignores defense / Assist

            Sentinel / Physical"""
        self.dandegate_link: str = "https://www.dandegate.net/dolls/voymastina"
        self.doll_portrait: str = "resources/voymastina.webp"

    @override
    def update_doll_abilities(self) -> None:
        self.option_config: dict[str, dict[str, Any]] = {
            "Dread Ultimatum": {
                "fields": [],
                "function": self.doll.dread_ultimatum.execute,
            },
            "Sirius Fall (Passive)": {
                "fields": [
                    {
                        "key": "has_fixed_key_4",
                        "type": "checkbox",
                        "label": "Fixed Key 4 - Solo Kill",
                        "default": True,
                    },
                ],
                "function": self.doll.sirius_fall_passive.execute,
            },
            "Sirius Fall (Active)": {
                "fields": [
                    {
                        "key": "has_fixed_key_4",
                        "type": "checkbox",
                        "label": "Fixed Key 4 - Solo Kill",
                        "default": True,
                    },
                ],
                "function": self.doll.sirius_fall_active.execute,
            },
            "Eye of the White Mastiff (Passive)": {
                "fields": [],
                "function": self.doll.eye_of_the_white_mastiff_passive.execute,
            },
            "Lock-On Attack": {
                "fields": [],
                "function": self.doll.lockon_attack.execute,
            },
            "Pile Bunker (Passive)": {
                "fields": [],
                "function": self.doll.pile_bunker_passive.execute,
            },
            "Pile Bunker (Active)": {
                "fields": [
                    {
                        "key": "has_activated_fixed_key_6",
                        "type": "checkbox",
                        "label": "Activated Fixed Key 6 - Scars Are Power",
                        "default": True,
                    },
                ],
                "function": self.doll.pile_bunker_active.execute,
            },
        }

    @override
    def set_initial_values(self) -> None:
        self.doll.initial_stats.basic_attributes[StatType.ATTACK] = 3960
        self.doll.initial_stats.basic_attributes[StatType.CRIT_RATE] = 78.6
        self.doll.initial_stats.basic_attributes[StatType.CRIT_DAMAGE] = 135.5

        # Attachments, common keys, imagoform, specialized traits
        # attachment: 12
        # imagoform: 12
        # Yoohee imagoform: 4
        self.doll.additive_modifiers.special_attributes[
            SpecialAttribute.DAMAGE_BOOST
        ].set_multiplier(DamageTag.ALL, 12 + 12 + 4)

        # imagoform: 5
        # physical boost: 1.4
        self.doll.additive_modifiers.special_attributes[
            SpecialAttribute.DAMAGE_BOOST
        ].set_multiplier(DamageTag.PHYSICAL, 5 + 1.4)

        # attachment: 36
        # keys: 10
        # imagoform: 8
        self.doll.additive_modifiers.special_attributes[
            SpecialAttribute.DAMAGE_BOOST
        ].set_multiplier(DamageTag.MELEE, 36 + 10 + 8)

        # keys: 7
        # raid stance: 3
        self.doll.additive_modifiers.special_attributes[
            SpecialAttribute.DAMAGE_BOOST
        ].set_multiplier(DamageTag.PASSIVE, 7 + 3)

        # keys: 10
        self.doll.additive_modifiers.special_attributes[
            SpecialAttribute.DAMAGE_BOOST
        ].set_multiplier(DamageTag.AREA_OF_EFFECT, 10)

        # imagoform: 10
        self.doll.additive_modifiers.special_attributes[
            SpecialAttribute.DAMAGE_BOOST
        ].set_multiplier(DamageTag.STABILITY_BROKEN, 10)

        # thronebreaker: 5.5
        self.doll.additive_modifiers.special_attributes[
            SpecialAttribute.DAMAGE_BOOST
        ].set_multiplier(DamageTag.BOSS, 5.5)

        # smite boost: 2.4
        self.doll.additive_modifiers.special_attributes[
            SpecialAttribute.CRITICAL_DAMAGE
        ].set_multiplier(DamageTag.ALL, 2.4)

        # physical smite: 0.4
        self.doll.additive_modifiers.special_attributes[
            SpecialAttribute.CRITICAL_DAMAGE
        ].set_multiplier(DamageTag.PHYSICAL, 0.4)

        # ambush mastery: 0.2
        self.doll.additive_modifiers.special_attributes[
            SpecialAttribute.CRITICAL_DAMAGE
        ].set_multiplier(DamageTag.PASSIVE, 0.2)

        # Yoohee Imagoform: 5
        # Yoohee Sparkling Centerstage: 10
        self.doll.additive_modifiers.special_attributes[
            SpecialAttribute.DEFENSE_IGNORE
        ].set_multiplier(DamageTag.PHYSICAL, 5 + 10)

        # imagoform: 8
        # attack boost: 3.6
        # Yoohee imagoform: 3
        self.doll.multiplicative_modifiers.basic_attributes[StatType.ATTACK] = (
            8 + 3.6 + 3
        )

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
            self.rotation_planner.set_data(sample_rotation)
