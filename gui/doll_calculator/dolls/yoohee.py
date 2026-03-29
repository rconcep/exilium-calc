from nicegui import ui

from gui.templates.doll_calculator_page import DollCalculatorPage, ModelAssumption
from gui.templates.rotation_planner import RotationPlanner
from typing import Any, override
from core.types import DamageTag, FortificationLevel, SpecialAttribute, StatType
from core.dolls import yoohee


sample_rotation: dict[int, list[dict]] = {
    1: [
        {
            "name": "Improv",
            "confectance_index_spent": 3,
            "stacks_fantastic_conception": 0,
            "has_fixed_key_1": True,
        },
        {
            "name": "Improv",
            "confectance_index_spent": 3,
            "stacks_fantastic_conception": 0,
            "has_fixed_key_1": True,
        },
    ],
    2: [
        {
            "name": "Improv",
            "confectance_index_spent": 3,
            "stacks_fantastic_conception": 3,
            "has_fixed_key_1": True,
        },
    ],
    3: [
        {
            "name": "Improv",
            "confectance_index_spent": 3,
            "stacks_fantastic_conception": 2,
            "has_fixed_key_1": True,
        },
        {
            "name": "Improv",
            "confectance_index_spent": 3,
            "stacks_fantastic_conception": 2,
            "has_fixed_key_1": True,
        },
    ],
    4: [
        {
            "name": "Improv",
            "confectance_index_spent": 3,
            "stacks_fantastic_conception": 3,
            "has_fixed_key_1": True,
        },
        {
            "name": "Improv",
            "confectance_index_spent": 3,
            "stacks_fantastic_conception": 3,
            "has_fixed_key_1": True,
        },
    ],
    5: [
        {
            "name": "Improv",
            "confectance_index_spent": 3,
            "stacks_fantastic_conception": 3,
            "has_fixed_key_1": True,
        },
    ],
    6: [
        {
            "name": "Improv",
            "confectance_index_spent": 3,
            "stacks_fantastic_conception": 2,
            "has_fixed_key_1": True,
        },
        {
            "name": "Improv",
            "confectance_index_spent": 3,
            "stacks_fantastic_conception": 2,
            "has_fixed_key_1": True,
        },
    ],
    7: [
        {
            "name": "Improv",
            "confectance_index_spent": 3,
            "stacks_fantastic_conception": 3,
            "has_fixed_key_1": True,
        },
        {
            "name": "Improv",
            "confectance_index_spent": 3,
            "stacks_fantastic_conception": 3,
            "has_fixed_key_1": True,
        },
    ],
}


class Yoohee(DollCalculatorPage):
    """Page for Yoohee."""

    def __init__(self):
        super().__init__()

        self.doll: yoohee.Yoohee = yoohee.Yoohee()
        self.doll.set_fortification_level(FortificationLevel.SEGMENT06)
        self.doll_subtitle: str = """Multi-Buff / Negative Defense

            Support / Physical"""
        self.dandegate_link: str = "https://www.dandegate.net/dolls/yoohee"
        self.doll_portrait: str = "resources/yoohee.webp"

    @override
    def update_doll_abilities(self) -> None:
        self.option_config = {
            "Rhythmic Pulse": {
                "fields": [],
                "function": self.doll.rhythmic_pulse.execute,
            },
            "Improv": {
                "fields": [
                    {
                        "key": "confectance_index_spent",
                        "type": "select",
                        "label": "Confectance Index Spent",
                        "default": 3,
                        "options": [n for n in range(1, 4)],
                    },
                    {
                        "key": "stacks_fantastic_conception",
                        "type": "select",
                        "label": "Fantastic Conception Stacks from Previous Turn",
                        "default": 3,
                        "options": [n for n in range(4)],
                    },
                    {
                        "key": "has_fixed_key_1",
                        "type": "checkbox",
                        "label": "Fixed Key 1 - Effort and Returns",
                        "default": True,
                    },
                ],
                "function": self.doll.improv.execute,
            },
            "Soul of Dance": {
                "fields": [],
                "function": self.doll.soul_of_dance.execute,
            },
        }

    @override
    def set_initial_values(self) -> None:
        self.doll.initial_stats.basic_attributes[StatType.ATTACK] = 4029
        self.doll.initial_stats.basic_attributes[StatType.HEALTH] = 4833
        self.doll.initial_stats.basic_attributes[StatType.CRIT_RATE] = 63.4
        self.doll.initial_stats.basic_attributes[StatType.CRIT_DAMAGE] = 145.0

        # Attachments, common keys, imagoform, specialized traits
        # attachment: 20
        # imagoform (sprout): 5
        # physical unity: 0.3
        self.doll.additive_modifiers.special_attributes[
            SpecialAttribute.DAMAGE_BOOST
        ].set_multiplier(DamageTag.PHYSICAL, 20 + 5 + 0.3)

        # Common Key: 10
        self.doll.additive_modifiers.special_attributes[
            SpecialAttribute.DAMAGE_BOOST
        ].set_multiplier(DamageTag.MEDIUM_AMMO, 10)

        # Common Key: 10
        # follow-up strike: 0.5
        self.doll.additive_modifiers.special_attributes[
            SpecialAttribute.DAMAGE_BOOST
        ].set_multiplier(DamageTag.STABILITY_BROKEN, 10 + 0.5)

        # onslaught stance: 1
        self.doll.additive_modifiers.special_attributes[
            SpecialAttribute.DAMAGE_BOOST
        ].set_multiplier(DamageTag.ACTIVE, 1)

        # imagoform: 12
        # CQC elite: 0.4
        # Support imagoform (Shoot): 4
        self.doll.additive_modifiers.special_attributes[
            SpecialAttribute.DAMAGE_BOOST
        ].set_multiplier(DamageTag.ALL, 12 + 0.4 + 4)

        # Yoohee imagoform: 5
        # Sparkling Centerstage: 10 + 20
        self.doll.additive_modifiers.special_attributes[
            SpecialAttribute.DEFENSE_IGNORE
        ].set_multiplier(DamageTag.PHYSICAL, 5 + 10 + 20)

        # imagoform (bud): 4
        # attack boost: 3.6
        # attack unity: 1
        # fighting spirit: 1
        self.doll.multiplicative_modifiers.basic_attributes[StatType.ATTACK] = (
            4 + 3.6 + 1 + 1
        )

        # ichor conversion: 0.8% of initial max HP
        self.doll.additive_modifiers.basic_attributes[StatType.ATTACK] = (
            0.008 * self.doll.initial_stats.basic_attributes[StatType.ATTACK]
        )

    @override
    def get_model_assumptions(self) -> list[ModelAssumption]:
        return [
            ModelAssumption(
                icon="groups",
                description="Expansion Key - Flawless Dance Moves team scaling is modeled at its 5-ally cap.",
                link_label="Dandegate",
                link_target="https://www.dandegate.net/dolls/yoohee/keys/expansion-key-perfect-dance",
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
