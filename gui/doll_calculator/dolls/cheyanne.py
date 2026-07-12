from nicegui import ui

from gui.templates.doll_calculator_page import DollCalculatorPage, ModelAssumption
from gui.templates.rotation_planner import RotationPlanner
from typing import Any, cast, override
from core.types import FortificationLevel, StatType, SpecialAttribute, DamageTag
from core.dolls import cheyanne

_t1: list[dict[str, Any]] = [
    {"name": "Focused Pursuit", "analysis_score": 100},
    {"name": "Deliberate Action", "analysis_score": 100},
    {"name": "Deliberate Action", "analysis_score": 100},
]

_t3: list[dict[str, Any]] = [
    {
        "name": "Heavenpierce",
        "target_has_bullseye": True,
        "few_enemies_with_low_analysis_score": True,
        "stacks_of_prepared_stance": 3,
    },
    {"name": "Deliberate Action", "analysis_score": 100},
    {"name": "Deliberate Action", "analysis_score": 100},
]

sample_rotation: dict[int, list[dict]] = {
    1: _t1,
    2: _t1,
    3: _t1,
    4: _t3,
    5: _t3,
    6: _t1,
    7: _t3,
}


class Cheyanne(DollCalculatorPage):
    """Page for Cheyanne."""

    def __init__(self):
        super().__init__()

        self.doll = cheyanne.Cheyanne()
        self.doll.set_fortification_level(FortificationLevel.SEGMENT06)
        self.doll_subtitle: str = """Burst Damage / Debuff

            Sentinel / Physical"""
        self.dandegate_link: str = "https://www.dandegate.net/dolls/cheyanne"
        self.doll_portrait: str = "resources/cheyanne.webp"

    @override
    def update_doll_abilities(self) -> None:
        doll = cast(cheyanne.Cheyanne, self.doll)

        self.option_config: dict[str, dict[str, Any]] = {
            "Definitely Not 360 NoScope": {
                "fields": [
                    {
                        "key": "analysis_score",
                        "type": "number",
                        "label": "Target Analysis Score",
                        "default": 100,
                    },
                ],
                "function": doll.definitely_not_360_noscope.execute,
            },
            "Focused Pursuit": {
                "fields": [
                    {
                        "key": "analysis_score",
                        "type": "number",
                        "label": "Target Analysis Score",
                        "default": 100,
                    },
                ],
                "function": doll.focused_pursuit.execute,
            },
            "Heavenpierce": {
                "fields": [
                    {
                        "key": "target_has_bullseye",
                        "type": "checkbox",
                        "label": "Target has Bullseye",
                        "default": True,
                    },
                    {
                        "key": "few_enemies_with_low_analysis_score",
                        "type": "checkbox",
                        "label": "<= 3 enemies below 50% Analysis Score",
                        "default": True,
                    },
                    {
                        "key": "stacks_of_prepared_stance",
                        "type": "select",
                        "options": [n for n in range(0, 4)],
                        "label": "Prepared Stance Stacks",
                        "default": 3,
                    },
                ],
                "function": doll.heavenpierce.execute,
            },
            "Deliberate Action": {
                "fields": [
                    {
                        "key": "analysis_score",
                        "type": "number",
                        "label": "Target Analysis Score",
                        "default": 100,
                    },
                ],
                "function": doll.deliberate_action.execute,
            },
        }

    @override
    def set_initial_values(self) -> None:
        self.doll.initial_stats.basic_attributes[StatType.ATTACK] = 4700

        # Base + Universal Keys + Weapon Attachment
        self.doll.initial_stats.basic_attributes[StatType.CRIT_RATE] = 80

        # Base + Universal Keys + Signature Weapon + Weapon Attachment
        self.doll.initial_stats.basic_attributes[StatType.CRIT_DAMAGE] = 120 + 20 + 15
        self.doll.initial_stats.basic_attributes[StatType.HEALTH] = 4400

        # Attachments, common keys, imagoform, specialized traits

        # imagoform: 12
        # CQC elite: 0.4
        # Imagoform (Shoot): 4+3
        self.doll.additive_modifiers.special_attributes[
            SpecialAttribute.DAMAGE_BOOST
        ].set_multiplier(DamageTag.ALL, 12 + 0.4 + 4 + 3)

        # attachment: 20
        # imagoform: 5
        # physical boost: 1.5
        # physical Unity: 0.9
        # Imagoform (Bud): 3
        self.doll.additive_modifiers.special_attributes[
            SpecialAttribute.DAMAGE_BOOST
        ].set_multiplier(DamageTag.PHYSICAL, 20 + 5 + 1.5 + 0.9 + 3)

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

        # imagoform: 8
        # attack boost: 3.6
        # Support Imagoform: 3
        self.doll.multiplicative_modifiers.basic_attributes[StatType.ATTACK] = (
            8 + 3.6 + 3
        )

        # Night-Wayfaring Cardamom: 10
        # Yoohee Sparkling Centerstage: 10
        self.doll.additive_modifiers.special_attributes[
            SpecialAttribute.DEFENSE_IGNORE
        ].set_multiplier(DamageTag.PHYSICAL, 10 + 10)

    def get_default_damage_calculator_buffs(self) -> list[dict[str, Any]]:
        return [
            {"name": "Attack Up II"},
            {"name": "Never Give Up (Yoohee)", "stacks": 4},
            {"name": "Graceful Spin (Yoohee)"},
            {"name": "Preshow Warmup (Yoohee)"},
            {"name": "Mimosa's Calyx (Cheyanne)"},
            {
                "name": "Sense of Security (Cheyanne)",
                "stacks": 3,
                "cheyanne_fortification_level": FortificationLevel.SEGMENT06,
            },
        ]

    def get_default_damage_calculator_debuffs(self) -> list[dict[str, Any]]:
        return [
            {"name": "Defense Down II"},
            {
                "name": "Precognition Foresight (Lainie)",
                "lainie_fortification_level": FortificationLevel.SEGMENT03,
            },
            {
                "name": "Precognition Awareness (Simulacrum)",
                "lainie_fortification_level": FortificationLevel.SEGMENT03,
            },
            {
                "name": "Bullseye (Cheyanne)",
                "cheyanne_fortification_level": FortificationLevel.SEGMENT06,
            },
        ]

    @override
    def get_model_assumptions(self) -> list[ModelAssumption]:
        return [
            ModelAssumption(
                icon="flight",
                description="The 20% increased damage against flying targets is not included by default.",
            ),
            ModelAssumption(
                icon="key",
                description="Sample rotation assumes Fixed Key 6 - Total Focus is active to ensure all activations of Deliberate Action.",
                link_label="Dandegate",
                link_target="https://www.dandegate.net/dolls/cheyanne/keys/fixed-key-6-full-attention",
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
