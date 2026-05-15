from typing import Any, cast, override

from nicegui import ui

from core.dolls import phaetusa
from core.types import DamageTag, FortificationLevel, SpecialAttribute, StatType
from gui.templates.doll_calculator_page import DollCalculatorPage, ModelAssumption
from gui.templates.rotation_planner import RotationPlanner

sample_rotation: dict[int, list[dict[str, Any]]] = {
    1: [
        {
            "name": "Dual-Winged Descent",
            "has_bloodquenched": True,
        },
        {
            "name": "Lacerating Wound",
            "original_damage_instance_potency": 120,
        },
        {"name": "Support Action"},
        {
            "name": "Lacerating Wound",
            "original_damage_instance_potency": 120,
        },
        {"name": "Support Action"},
        {
            "name": "Lacerating Wound",
            "original_damage_instance_potency": 120,
        },
        {"name": "Support Action"},
        {
            "name": "Lacerating Wound",
            "original_damage_instance_potency": 120,
        },
    ],
    2: [
        {
            "name": "Dual-Winged Descent",
            "has_bloodquenched": False,
        },
        {
            "name": "Lacerating Wound",
            "original_damage_instance_potency": 120,
        },
        {"name": "Support Action"},
        {
            "name": "Lacerating Wound",
            "original_damage_instance_potency": 120,
        },
        {"name": "Support Action"},
        {
            "name": "Lacerating Wound",
            "original_damage_instance_potency": 120,
        },
        {"name": "Support Action"},
        {
            "name": "Lacerating Wound",
            "original_damage_instance_potency": 120,
        },
    ],
    3: [
        {
            "name": "Twofold Rapture",
            "has_bloodquenched": True,
            "stacks_of_blade_resonance": 3,
        },
        {
            "name": "Lacerating Wound",
            "original_damage_instance_potency": 920,
        },
        # Synchrony + Reversion
        {
            "name": "Twofold Rapture",
            "has_bloodquenched": True,
            "stacks_of_blade_resonance": 3,
        },
        {
            "name": "Lacerating Wound",
            "original_damage_instance_potency": 920,
        },
        {"name": "Support Action"},
        {
            "name": "Lacerating Wound",
            "original_damage_instance_potency": 120,
        },
        {"name": "Support Action"},
        {
            "name": "Lacerating Wound",
            "original_damage_instance_potency": 120,
        },
        {"name": "Support Action"},
        {
            "name": "Lacerating Wound",
            "original_damage_instance_potency": 120,
        },
    ],
    4: [
        {
            "name": "Dual-Winged Descent",
            "has_bloodquenched": False,
        },
        {
            "name": "Lacerating Wound",
            "original_damage_instance_potency": 120,
        },
        {"name": "Support Action"},
        {
            "name": "Lacerating Wound",
            "original_damage_instance_potency": 120,
        },
        {"name": "Support Action"},
        {
            "name": "Lacerating Wound",
            "original_damage_instance_potency": 120,
        },
        {"name": "Support Action"},
        {
            "name": "Lacerating Wound",
            "original_damage_instance_potency": 120,
        },
    ],
    5: [
        {
            "name": "Dual-Winged Descent",
            "has_bloodquenched": True,
        },
        {
            "name": "Lacerating Wound",
            "original_damage_instance_potency": 120,
        },
        {"name": "Support Action"},
        {
            "name": "Lacerating Wound",
            "original_damage_instance_potency": 120,
        },
        {"name": "Support Action"},
        {
            "name": "Lacerating Wound",
            "original_damage_instance_potency": 120,
        },
        {"name": "Support Action"},
        {
            "name": "Lacerating Wound",
            "original_damage_instance_potency": 120,
        },
    ],
    6: [
        {
            "name": "Dual-Winged Descent",
            "has_bloodquenched": False,
        },
        {
            "name": "Lacerating Wound",
            "original_damage_instance_potency": 120,
        },
        {"name": "Support Action"},
        {
            "name": "Lacerating Wound",
            "original_damage_instance_potency": 120,
        },
        {"name": "Support Action"},
        {
            "name": "Lacerating Wound",
            "original_damage_instance_potency": 120,
        },
        {"name": "Support Action"},
        {
            "name": "Lacerating Wound",
            "original_damage_instance_potency": 120,
        },
    ],
    7: [
        {
            "name": "Twofold Rapture",
            "has_bloodquenched": True,
            "stacks_of_blade_resonance": 3,
        },
        {
            "name": "Lacerating Wound",
            "original_damage_instance_potency": 920,
        },
        # Synchrony + Reversion
        {
            "name": "Twofold Rapture",
            "has_bloodquenched": True,
            "stacks_of_blade_resonance": 3,
        },
        {
            "name": "Lacerating Wound",
            "original_damage_instance_potency": 920,
        },
        {"name": "Support Action"},
        {
            "name": "Lacerating Wound",
            "original_damage_instance_potency": 120,
        },
        {"name": "Support Action"},
        {
            "name": "Lacerating Wound",
            "original_damage_instance_potency": 120,
        },
        {"name": "Support Action"},
        {
            "name": "Lacerating Wound",
            "original_damage_instance_potency": 120,
        },
    ],
}


class Phaetusa(DollCalculatorPage):
    """Page for Phaetusa."""

    def __init__(self):
        super().__init__()

        self.doll = phaetusa.Phaetusa()
        self.doll.set_fortification_level(FortificationLevel.SEGMENT06)
        self.doll_subtitle: str = """Team Support / Burst Damage

            Sentinel / Corrosion"""
        self.dandegate_link: str = "https://www.dandegate.net/dolls/phaetusa"
        self.doll_portrait: str = "resources/phaetusa.webp"

    @override
    def update_doll_abilities(self) -> None:
        doll = cast(phaetusa.Phaetusa, self.doll)

        self.option_config = {
            "One Strike, Two Cuts": {
                "fields": [
                    {
                        "key": "has_bloodquenched",
                        "type": "checkbox",
                        "label": "Bloodquenched active",
                        "default": False,
                    },
                ],
                "function": doll.one_strike_two_cuts.execute,
            },
            "Dual-Winged Descent": {
                "fields": [
                    {
                        "key": "has_bloodquenched",
                        "type": "checkbox",
                        "label": "Bloodquenched active",
                        "default": False,
                    },
                ],
                "function": doll.dual_winged_descent.execute,
            },
            "Twofold Rapture": {
                "fields": [
                    {
                        "key": "has_bloodquenched",
                        "type": "checkbox",
                        "label": "Bloodquenched active",
                        "default": True,
                    },
                    {
                        "key": "stacks_of_blade_resonance",
                        "type": "select",
                        "label": "Blade Resonance stacks",
                        "default": 3,
                        "options": [n for n in range(4)],
                    },
                ],
                "function": doll.twofold_rapture.execute,
            },
            "Support Action": {
                "fields": [],
                "function": doll.support_action.execute,
            },
            "Lacerating Wound": {
                "fields": [
                    {
                        "key": "original_damage_instance_potency",
                        "type": "number",
                        "label": "Original Damage Potency",
                        "default": 120,
                    },
                ],
                "function": doll.lacerating_wound.execute,
            },
        }

    @override
    def set_initial_values(self) -> None:
        doll = cast(phaetusa.Phaetusa, self.doll)

        doll.initial_stats.basic_attributes[StatType.ATTACK] = 4064
        doll.initial_stats.basic_attributes[StatType.CRIT_RATE] = 98.3
        doll.initial_stats.basic_attributes[StatType.CRIT_DAMAGE] = 188.3
        doll.initial_stats.basic_attributes[StatType.HEALTH] = 4343

        # Key: 7
        # Attachment: 12
        # Cause and Effect (Imprint): 2.5
        # Support Imagoform (Shoot): 4
        doll.additive_modifiers.special_attributes[
            SpecialAttribute.DAMAGE_BOOST
        ].set_multiplier(DamageTag.ALL, 25.5)

        # Attachment: 24
        # Imagoform (Embryo): 8
        doll.additive_modifiers.special_attributes[
            SpecialAttribute.DAMAGE_BOOST
        ].set_multiplier(DamageTag.MELEE, 32)

        # Cause and Effect: 15
        # Imagoform (Sprout): 5
        # Corrosion Boost: 1.1
        # Support Imagoform (Embryo): 3
        doll.additive_modifiers.special_attributes[
            SpecialAttribute.DAMAGE_BOOST
        ].set_multiplier(DamageTag.CORROSION, 24.1)

        # Key: 10
        doll.additive_modifiers.special_attributes[
            SpecialAttribute.DAMAGE_BOOST
        ].set_multiplier(DamageTag.PHASE, 10)

        # Key: 10
        # Cause and Effect (Trait): 5 + 5
        # Area Specialization: 3.5
        doll.additive_modifiers.special_attributes[
            SpecialAttribute.DAMAGE_BOOST
        ].set_multiplier(DamageTag.AREA_OF_EFFECT, 23.5)

        # Imagoform (Shoot): 10
        # Follow-Up Strike: 1
        doll.additive_modifiers.special_attributes[
            SpecialAttribute.DAMAGE_BOOST
        ].set_multiplier(DamageTag.STABILITY_BROKEN, 11)

        # Thronebreaker: 3.5
        doll.additive_modifiers.special_attributes[
            SpecialAttribute.DAMAGE_BOOST
        ].set_multiplier(DamageTag.BOSS, 3.5)

        # Fixed Key 3: 15
        self.doll.additive_modifiers.special_attributes[
            SpecialAttribute.DAMAGE_BOOST
        ].set_multiplier(DamageTag.ONLY_HIT_ONE_TARGET, 15)

        # smite boost: 2.4
        self.doll.additive_modifiers.special_attributes[
            SpecialAttribute.CRITICAL_DAMAGE
        ].set_multiplier(DamageTag.ALL, 2.4)

        # Area Smite: 3
        self.doll.additive_modifiers.special_attributes[
            SpecialAttribute.CRITICAL_DAMAGE
        ].set_multiplier(DamageTag.AREA_OF_EFFECT, 3)

        # Imagoform (Bud): 8
        # Attack Boost: 3.6
        # Support Imagoform (Blossom): 3
        doll.multiplicative_modifiers.basic_attributes[StatType.ATTACK] = 14.6

        # Ichor Conversion: 0.4%
        doll.additive_modifiers.basic_attributes[StatType.ATTACK] = (
            0.004 * doll.initial_stats.basic_attributes[StatType.HEALTH]
        )

    def get_default_damage_calculator_buffs(self) -> list[dict[str, Any]]:
        return [
            {
                "name": "Reversion (Phaetusa)",
                "phaetusa_fortification_level": FortificationLevel.SEGMENT06,
            },
            {
                "name": "Overwrite Trap (Phaetusa)",
                "uses_of_replication_trap": 6,
                "phaetusa_fortification_level": FortificationLevel.SEGMENT06,
            },
            {
                "name": "Dream Guardian",
            },
            {
                "name": "Nightmare Form",
                "mechty_fortification_level": FortificationLevel.SEGMENT06,
            },
        ]

    def get_default_damage_calculator_debuffs(self) -> list[dict[str, Any]]:
        return [
            {"name": "Radio Invitation: Defense Down"},
            {
                "name": "Corrosive Infusion (Klukai)",
                "stacks": 15,
                "klukai_fortification_level": FortificationLevel.SEGMENT06,
            },
            {"name": "Toxin Inundation"},
            {"name": "Acid Corrosion II"},
        ]

    @override
    def get_model_assumptions(self) -> list[ModelAssumption]:
        return [
            ModelAssumption(
                icon="content_cut",
                description="Lacerating Wound is modeled as 40% of the configured original potency.",
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
