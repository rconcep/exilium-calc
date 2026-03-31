from nicegui import ui

from gui.templates.doll_calculator_page import DollCalculatorPage, ModelAssumption
from gui.templates.rotation_planner import RotationPlanner
from typing import Any, override
from core.types import DamageTag, FortificationLevel, SpecialAttribute, StatType
from core.dolls import faye


sample_rotation: dict[int, list[dict]] = {
    1: [
        {"name": "Ruinous Whirl", "has_fixed_key_2": True},
        {"name": "Axe Whirl"},
        {"name": "Gash", "stacks_of_gash": 8},
        {"name": "Axe Whirl"},
    ],
    2: [
        {"name": "No Survivors", "stacks_of_rend": 8},
        {"name": "Gash", "stacks_of_gash": 8},
        {"name": "Axe Whirl"},
        {"name": "Gash", "stacks_of_gash": 8},
        {"name": "Axe Whirl"},
    ],
    3: [
        {"name": "No Survivors", "stacks_of_rend": 8},
        {"name": "Gash", "stacks_of_gash": 8},
        {"name": "Axe Whirl"},
        {"name": "Gash", "stacks_of_gash": 8},
        {"name": "Axe Whirl"},
    ],
    4: [
        {"name": "No Survivors", "stacks_of_rend": 8},
        {"name": "Gash", "stacks_of_gash": 8},
        {"name": "Axe Whirl"},
        {"name": "Gash", "stacks_of_gash": 8},
        {"name": "Axe Whirl"},
    ],
    5: [
        {"name": "No Survivors", "stacks_of_rend": 8},
        {"name": "Gash", "stacks_of_gash": 8},
        {"name": "Axe Whirl"},
        {"name": "Gash", "stacks_of_gash": 8},
        {"name": "Axe Whirl"},
    ],
    6: [
        {"name": "No Survivors", "stacks_of_rend": 8},
        {"name": "Gash", "stacks_of_gash": 8},
        {"name": "Axe Whirl"},
        {"name": "Gash", "stacks_of_gash": 8},
        {"name": "Axe Whirl"},
    ],
    7: [
        {"name": "No Survivors", "stacks_of_rend": 8},
        {"name": "Gash", "stacks_of_gash": 8},
        {"name": "Axe Whirl"},
        {"name": "Gash", "stacks_of_gash": 8},
        {"name": "Axe Whirl"},
    ],
}


class Faye(DollCalculatorPage):
    """Page for Faye."""

    def __init__(self):
        super().__init__()

        self.doll: faye.Faye = faye.Faye()
        self.doll.set_fortification_level(FortificationLevel.SEGMENT06)
        self.doll_subtitle: str = """Mixed Damage / Ignores defense / Ignores obstructions

            Vanguard / Physical"""
        self.dandegate_link: str = "https://www.dandegate.net/dolls/faye"
        self.doll_portrait: str = "resources/faye.webp"

    @override
    def update_doll_abilities(self) -> None:
        self.option_config: dict[str, dict[str, Any]] = {
            "Practice Shot": {
                "fields": [],
                "function": self.doll.practice_shot.execute,
            },
            "Ruinous Whirl": {
                "fields": [
                    {
                        "key": "has_fixed_key_2",
                        "type": "checkbox",
                        "label": "Fixed Key 2 - All-In Slash",
                        "default": True,
                    },
                ],
                "function": self.doll.ruinous_whirl.execute,
            },
            "Fissioned Firelight": {
                "fields": [],
                "function": self.doll.fissioned_firelight.execute,
            },
            "No Survivors": {
                "fields": [
                    {
                        "key": "stacks_of_rend",
                        "type": "select",
                        "options": [n for n in range(0, 9)],
                        "label": "Rend Stacks",
                        "default": 8,
                    },
                ],
                "function": self.doll.no_survivors.execute,
            },
            "Tomahawk Throw": {
                "fields": [],
                "function": self.doll.tomahawk_throw.execute,
            },
            "Axe Whirl": {
                "fields": [],
                "function": self.doll.axe_whirl.execute,
            },
            "Gash": {
                "fields": [
                    {
                        "key": "stacks_of_gash",
                        "type": "select",
                        "options": [n for n in range(0, 9)],
                        "label": "Gash Stacks",
                        "default": 8,
                    },
                ],
                "function": self.doll.gash.execute,
            },
        }

    @override
    def set_initial_values(self) -> None:
        self.doll.initial_stats.basic_attributes[StatType.ATTACK] = 4025
        self.doll.initial_stats.basic_attributes[StatType.CRIT_RATE] = 68.8
        self.doll.initial_stats.basic_attributes[StatType.CRIT_DAMAGE] = 135.0

        # Preset build assumptions (attachments, keys, imagoform, and traits).
        # Targeting approximately 100 total damage boost from ALL + PHYSICAL.
        # ALL: 30 (weapon) + 20 (imagoform) + 22 (team/passive) = 72
        self.doll.additive_modifiers.special_attributes[
            SpecialAttribute.DAMAGE_BOOST
        ].set_multiplier(DamageTag.ALL, 72)

        # PHYSICAL: 20 (attachment set) + 8 (specialized traits) = 28
        self.doll.additive_modifiers.special_attributes[
            SpecialAttribute.DAMAGE_BOOST
        ].set_multiplier(DamageTag.PHYSICAL, 28)

        # Combined baseline: 72 + 28 = 100
        self.doll.multiplicative_modifiers.basic_attributes[StatType.ATTACK] = 8

    @override
    def get_model_assumptions(self) -> list[ModelAssumption]:
        return [
            ModelAssumption(
                icon="key",
                description="Expansion Key - Unstoppable Fighting Spirit is active.",
                link_label="Dandegate",
                link_target="https://www.dandegate.net/dolls/faye/keys/expansion-key-relentless-fighting-spirit",
            ),
            ModelAssumption(
                icon="rule",
                description="Assumes the target has maximum Gash and 8 Rend stacks unless specified by the action inputs.",
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
