from typing import Any, cast, override

from nicegui import ui

from core.dolls import asteria
from core.types import DamageTag, FortificationLevel, SpecialAttribute, StatType
from gui.templates.doll_calculator_page import DollCalculatorPage, ModelAssumption
from gui.templates.rotation_planner import RotationPlanner

sample_rotation: dict[int, list[dict[str, Any]]] = {
    1: [
        {
            "name": "Railgun Judgement",
            "has_fixed_key_6": False,
            "stacks_of_absolution": 0,
        },
        *[
            {"name": "Blade of Sin", "stacks_of_absolution": stacks}
            for stacks in range(0, 6)
        ],
    ],
    2: [
        {
            "name": "Demolition Reckoning",
        },
    ],
    3: [
        {
            "name": "Railgun Judgement",
            "has_fixed_key_6": False,
            "stacks_of_absolution": 6,
        },
    ],
    4: [
        {
            "name": "Demolition Reckoning",
        },
    ],
    5: [
        {
            "name": "Railgun Judgement",
            "has_fixed_key_6": False,
            "stacks_of_absolution": 6,
        },
    ],
    6: [
        {
            "name": "Demolition Reckoning",
        },
    ],
    7: [
        {
            "name": "Railgun Judgement",
            "has_fixed_key_6": False,
            "stacks_of_absolution": 6,
        },
    ],
}


class Asteria(DollCalculatorPage):
    """Page for Asteria."""

    def __init__(self):
        super().__init__()

        self.doll: asteria.Asteria = asteria.Asteria()
        self.doll.set_fortification_level(FortificationLevel.SEGMENT06)
        self.doll_subtitle: str = """Buff / Add Weakness / Lock-On

            Support / Physical"""
        self.dandegate_link: str = "https://www.dandegate.net/dolls/asteria"
        self.doll_portrait: str = "resources/asteria.webp"

    @override
    def update_doll_abilities(self) -> None:
        doll = cast(asteria.Asteria, self.doll)

        self.option_config: dict[str, dict[str, Any]] = {
            "Silent Trigger": {
                "fields": [],
                "function": doll.silent_trigger.execute,
            },
            "Demolition Reckoning": {
                "fields": [],
                "function": doll.demolition_reckoning.execute,
            },
            "Railgun Judgement": {
                "fields": [
                    {
                        "key": "has_fixed_key_6",
                        "type": "checkbox",
                        "label": "Fixed Key 6 - Relentless Pursuit",
                        "default": False,
                    },
                    {
                        "key": "stacks_of_absolution",
                        "type": "select",
                        "label": "Absolution Stacks",
                        "default": 6,
                        "options": [n for n in range(0, 7)],
                    },
                ],
                "function": doll.railgun_judgement.execute,
            },
            "Blade of Sin": {
                "fields": [
                    {
                        "key": "stacks_of_absolution",
                        "type": "select",
                        "label": "Absolution Stacks",
                        "default": 6,
                        "options": [n for n in range(0, 7)],
                    },
                ],
                "function": doll.blade_of_sin.execute,
            },
        }

    @override
    def set_initial_values(self) -> None:
        self.doll.initial_stats.basic_attributes[StatType.ATTACK] = 3800
        self.doll.initial_stats.basic_attributes[StatType.HEALTH] = 4833
        self.doll.initial_stats.basic_attributes[StatType.CRIT_RATE] = 95
        self.doll.initial_stats.basic_attributes[StatType.CRIT_DAMAGE] = 170.0

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
    def get_default_damage_calculator_buffs(self) -> list[dict[str, Any]]:
        return [
            {"name": "Attack Up II"},
            {"name": "Never Give Up (Yoohee)", "stacks": 4},
            {"name": "Graceful Spin (Yoohee)"},
            {"name": "Preshow Warmup (Yoohee)"},
        ]

    @override
    def get_default_damage_calculator_debuffs(self) -> list[dict[str, Any]]:
        return [
            {"name": "Defense Down III"},
            {
                "name": "Precognition Foresight (Lainie)",
                "lainie_fortification_level": FortificationLevel.SEGMENT03,
            },
            {
                "name": "Precognition Awareness (Simulacrum)",
                "lainie_fortification_level": FortificationLevel.SEGMENT03,
            },
        ]

    @override
    def get_model_assumptions(self) -> list[ModelAssumption]:
        return [
            ModelAssumption(
                icon="format_bold",
                description="Asteria's passive effect of adding ammo typing to non-ammo type Physical damage is applied to herself - adding Medium Ammo type to all of her actions except when Fixed Key 6 is equipped for Railgun Judgement.",
            ),
            ModelAssumption(
                icon="handshake",
                description="Blade of Sin triggers for the unit with Bond are not included in the sample rotation.",
            ),
            ModelAssumption(
                icon="label_important",
                description="The effect of adding all weapon weaknesses from Vindicator's Mark is not modeled explicitly. This should be modeled using the 'phase weaknesses exploited' parameters in the Target's state.",
            ),
            ModelAssumption(
                icon="label_important",
                description="The effect of taking additional fixed damage for V1+ Vindicator's Mark is not modeled. It's basically a 10% more damage dealt.",
            ),
            ModelAssumption(
                icon="crisis_alert",
                description="The stacking increased critical damage taken effect from Absolution is implemented as a generic increased damage taken effect (no critical damage condition).",
            ),
            ModelAssumption(
                icon="format_bold",
                description="The 80% attack increase when Asteria gains Crime and Punishment at V6 is not modeled - use a custom buff.",
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
