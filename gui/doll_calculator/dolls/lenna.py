from nicegui import ui

from gui.templates.doll_calculator_page import DollCalculatorPage, ModelAssumption
from gui.templates.rotation_planner import RotationPlanner
from typing import Any, cast, override
from core.types import DamageTag, StatType, FortificationLevel, SpecialAttribute
from core.dolls import lenna


sample_rotation: dict[int, list[dict]] = {
    1: [
        {"name": "Leaping Pursuit", "confectance_index": 6},
        {
            "name": "Hunting Strategy",
            "confectance_index": 3,
            "follows_leaping_pursuit": True,
        },
    ],
    2: [
        {"name": "Leaping Pursuit", "confectance_index": 6},
        {
            "name": "Wild Extinction",
            "confectance_index": 3,
            "follows_leaping_pursuit": True,
        },
    ],
    3: [
        {"name": "Leaping Pursuit", "confectance_index": 6},
        {
            "name": "Wild Extinction",
            "confectance_index": 3,
            "follows_leaping_pursuit": True,
        },
    ],
    4: [
        {"name": "Leaping Pursuit", "confectance_index": 6},
        {
            "name": "Hunting Strategy",
            "confectance_index": 3,
            "follows_leaping_pursuit": True,
        },
    ],
    5: [
        {"name": "Leaping Pursuit", "confectance_index": 6},
        {
            "name": "Wild Extinction",
            "confectance_index": 3,
            "follows_leaping_pursuit": True,
        },
    ],
    6: [
        {"name": "Leaping Pursuit", "confectance_index": 6},
        {
            "name": "Wild Extinction",
            "confectance_index": 3,
            "follows_leaping_pursuit": True,
        },
    ],
    7: [
        {"name": "Leaping Pursuit", "confectance_index": 6},
        {
            "name": "Hunting Strategy",
            "confectance_index": 3,
            "follows_leaping_pursuit": True,
        },
    ],
}


class Lenna(DollCalculatorPage):
    """Page for Lenna."""

    def __init__(self):
        super().__init__()

        self.doll = lenna.Lenna()
        self.doll.set_fortification_level(FortificationLevel.SEGMENT06)
        self.doll_subtitle: str = """Crowd Control / Tile / Stealth

            Support / Electric"""
        self.dandegate_link: str = "https://www.dandegate.net/dolls/lenna"
        self.doll_portrait: str = "resources/lenna.webp"

    @override
    def update_doll_abilities(self) -> None:
        doll = cast(lenna.Lenna, self.doll)

        self.option_config: dict[str, dict[str, Any]] = {
            "Territory Awareness": {
                "fields": [
                    {
                        "key": "follows_leaping_pursuit",
                        "type": "checkbox",
                        "label": "Follows Leaping Pursuit",
                        "default": True,
                    },
                ],
                "function": doll.territory_awareness.execute,
            },
            "Wild Extinction": {
                "fields": [
                    {
                        "key": "confectance_index",
                        "type": "select",
                        "label": "Confectance Index",
                        "default": 3,
                        "options": [n for n in range(7)],
                    },
                    {
                        "key": "follows_leaping_pursuit",
                        "type": "checkbox",
                        "label": "Follows Leaping Pursuit",
                        "default": True,
                    },
                ],
                "function": doll.wild_extinction.execute,
            },
            "Leaping Pursuit": {
                "fields": [
                    {
                        "key": "confectance_index",
                        "type": "select",
                        "label": "Confectance Index",
                        "default": 3,
                        "options": [n for n in range(7)],
                    },
                ],
                "function": doll.leaping_pursuit.execute,
            },
            "Hunting Strategy": {
                "fields": [
                    {
                        "key": "confectance_index",
                        "type": "select",
                        "label": "Confectance Index",
                        "default": 3,
                        "options": [n for n in range(7)],
                    },
                    {
                        "key": "follows_leaping_pursuit",
                        "type": "checkbox",
                        "label": "Follows Leaping Pursuit",
                        "default": True,
                    },
                ],
                "function": doll.hunting_strategy.execute,
            },
        }

    @override
    def set_initial_values(self) -> None:
        self.doll.initial_stats.basic_attributes[StatType.ATTACK] = 4300
        self.doll.initial_stats.basic_attributes[StatType.CRIT_RATE] = 85
        self.doll.initial_stats.basic_attributes[StatType.CRIT_DAMAGE] = 170

        self.doll.additive_modifiers.special_attributes[
            SpecialAttribute.DAMAGE_BOOST
        ].set_multiplier(DamageTag.ALL, 35)
        self.doll.additive_modifiers.special_attributes[
            SpecialAttribute.DAMAGE_BOOST
        ].set_multiplier(DamageTag.ELECTRIC, 35)
        self.doll.additive_modifiers.special_attributes[
            SpecialAttribute.DAMAGE_BOOST
        ].set_multiplier(DamageTag.PHASE, 15)

        # Fixed Key 1 - Skillful Strategem
        self.doll.additive_modifiers.special_attributes[
            SpecialAttribute.DEFENSE_IGNORE
        ].set_multiplier(DamageTag.ALL, 15)

        self.doll.multiplicative_modifiers.basic_attributes[StatType.ATTACK] = 10

    def get_default_damage_calculator_buffs(self) -> list[dict[str, Any]]:
        return [
            {"name": "Attack Up II"},
            {
                "name": "Positive Charge",
                "target_has_negative_charge": True,
            },
            {
                "name": "Power Surge",
                "stacks": 3,
                "jiangyu_fortification_level": FortificationLevel.SEGMENT06,
                "target_voltage_sag_stacks": 3,
            },
        ]

    def get_default_damage_calculator_debuffs(self) -> list[dict[str, Any]]:
        return [
            {"name": "Defense Down II"},
            {
                "name": "Voltage Sag",
                "stacks": 3,
                "jiangyu_fortification_level": FortificationLevel.SEGMENT06,
            },
        ]

    @override
    def get_model_assumptions(self) -> list[ModelAssumption]:
        return [
            ModelAssumption(
                icon="key",
                description="Expansion Key - Lioness' Determination is active.",
                link_label="Dandegate",
                link_target="https://www.dandegate.net/dolls/lenna/keys/expansion-key-lioness-determination",
            ),
            ModelAssumption(
                icon="rule",
                description="When an action is marked as following Leaping Pursuit, the model assumes that Leaping Pursuit was enhanced by consuming Confectance Index.",
            ),
            ModelAssumption(
                icon="bolt",
                description="At V6, the Electric Arc buff has full uptime.",
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
