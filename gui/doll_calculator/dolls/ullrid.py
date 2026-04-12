from typing import Any, cast, override

from nicegui import ui

from core.dolls import ullrid
from core.types import DamageTag, FortificationLevel, SpecialAttribute, StatType
from gui.templates.doll_calculator_page import DollCalculatorPage, ModelAssumption
from gui.templates.rotation_planner import RotationPlanner


_rotation_turn: list[dict[str, Any]] = [
    {
        "name": "Blade Whirlwind",
        "attacking_same_target_within_one_action": True,
    },
    {
        "name": "Determined Pursuit",
    },
    {
        "name": "Lacerating Wound",
        "original_damage_instance_potency": 90,
    },
    {
        "name": "Blade Whirlwind",
        "attacking_same_target_within_one_action": True,
    },
    {
        "name": "Determined Pursuit",
    },
    {
        "name": "Lacerating Wound",
        "original_damage_instance_potency": 90,
    },
    {
        "name": "Blade Whirlwind",
        "attacking_same_target_within_one_action": True,
    },
    {
        "name": "Determined Pursuit",
    },
    {
        "name": "Lacerating Wound",
        "original_damage_instance_potency": 90,
    },
    {
        "name": "Hidden Pursuit",
        "stacks_of_hunters_talent": 6,
        "percent_target_missing_health": 0,
    },
    {
        "name": "Lacerating Wound",
        "original_damage_instance_potency": 180,
    },
    {
        "name": "Mark of Prey",
    },
]

sample_rotation: dict[int, list[dict[str, Any]]] = {
    turn: [dict(action) for action in _rotation_turn] for turn in range(1, 8)
}


class Ullrid(DollCalculatorPage):
    """Page for Ullrid."""

    def __init__(self):
        super().__init__()

        self.doll = ullrid.Ullrid()
        self.doll.set_fortification_level(FortificationLevel.SEGMENT06)
        self.doll_subtitle: str = """Melee Damage / Combo Attack / Stealth

            Vanguard / Physical"""
        self.dandegate_link: str = "https://www.dandegate.net/dolls/ullrid"
        self.doll_portrait: str = "resources/ullrid.webp"

    @override
    def update_doll_abilities(self) -> None:
        doll = cast(ullrid.Ullrid, self.doll)

        self.option_config: dict[str, dict[str, Any]] = {
            "Warning Shot": {
                "fields": [],
                "function": doll.warning_shot.execute,
            },
            "Hunter's Sight": {
                "fields": [],
                "function": doll.hunters_sight.execute,
            },
            "Blade Whirlwind": {
                "fields": [
                    {
                        "key": "attacking_same_target_within_one_action",
                        "type": "checkbox",
                        "label": "Same Target Within One Action",
                        "default": True,
                    },
                ],
                "function": doll.blade_whirlwind.execute,
            },
            "Determined Pursuit": {
                "fields": [],
                "function": doll.determined_pursuit.execute,
            },
            "Hidden Pursuit": {
                "fields": [
                    {
                        "key": "stacks_of_hunters_talent",
                        "type": "select",
                        "options": [n for n in range(0, 7)],
                        "label": "Hunter's Talent stacks",
                        "default": 6,
                    },
                    {
                        "key": "percent_target_missing_health",
                        "type": "number",
                        "label": "Target Missing Health (%)",
                        "default": 0,
                    },
                ],
                "function": doll.hidden_pursuit.execute,
            },
            "Mark of Prey": {
                "fields": [],
                "function": doll.mark_of_prey.execute,
            },
            "Lacerating Wound": {
                "fields": [
                    {
                        "key": "original_damage_instance_potency",
                        "type": "number",
                        "label": "Original Damage Potency",
                        "default": 90,
                    },
                ],
                "function": doll.lacerating_wound.execute,
            },
        }

    @override
    def set_initial_values(self) -> None:
        doll = cast(ullrid.Ullrid, self.doll)

        doll.initial_stats.basic_attributes[StatType.ATTACK] = 3000
        doll.initial_stats.basic_attributes[StatType.CRIT_RATE] = 115.6
        doll.initial_stats.basic_attributes[StatType.CRIT_DAMAGE] = 156.3

        # imagoform, common keys
        doll.additive_modifiers.special_attributes[
            SpecialAttribute.DAMAGE_BOOST
        ].set_multiplier(DamageTag.ALL, 29)

        # weapon, attachments
        doll.additive_modifiers.special_attributes[
            SpecialAttribute.DAMAGE_BOOST
        ].set_multiplier(DamageTag.PHYSICAL, 26.4)

        doll.additive_modifiers.special_attributes[
            SpecialAttribute.DAMAGE_BOOST
        ].set_multiplier(DamageTag.MELEE, 36)

        doll.additive_modifiers.special_attributes[
            SpecialAttribute.CRITICAL_DAMAGE
        ].set_multiplier(DamageTag.PHYSICAL, 0.4)

        doll.additive_modifiers.special_attributes[
            SpecialAttribute.CRITICAL_DAMAGE
        ].set_multiplier(DamageTag.BOSS, 3)

        doll.additive_modifiers.special_attributes[
            SpecialAttribute.CRITICAL_DAMAGE
        ].set_multiplier(DamageTag.TARGETED, 5)

        doll.additive_modifiers.special_attributes[
            SpecialAttribute.CRITICAL_DAMAGE
        ].set_multiplier(DamageTag.ALL, 2.4)

        # Fixed Key 2 - Predation: Ignore 30% of the target enemy's defense when there are no other
        # enemy units within 3 tiles of the target.
        doll.additive_modifiers.special_attributes[
            SpecialAttribute.DEFENSE_IGNORE
        ].set_multiplier(DamageTag.ALL, 30)

        doll.additive_modifiers.special_attributes[
            SpecialAttribute.DEFENSE_IGNORE
        ].set_multiplier(DamageTag.PHYSICAL, 10)

        doll.multiplicative_modifiers.basic_attributes[StatType.ATTACK] = 14.6

    def get_default_damage_calculator_buffs(self) -> list[dict[str, Any]]:
        return [
            {"name": "Attack Up II"},
            {"name": "Never Give Up (Yoohee)", "stacks": 4},
            {"name": "Graceful Spin (Yoohee)"},
            {"name": "Preshow Warmup (Yoohee)"},
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
        ]

    @override
    def get_model_assumptions(self) -> list[ModelAssumption]:
        return [
            ModelAssumption(
                icon="key",
                description="Expansion Key - Determined Pursuit (Tier 1/2) effects are active.",
                link_label="Dandegate",
                link_target="https://www.dandegate.net/dolls/ullrid/keys/expansion-key-determined-pursuit",
            ),
            ModelAssumption(
                icon="directions_run",
                description="The Attack boost for moving 2+ tiles for V5+ Optical Camouflage passive is active.",
            ),
            ModelAssumption(
                icon="content_cut",
                description="The Lacerating Wound effect is modeled as an attack with 40% of the specified potency.",
            ),
            ModelAssumption(
                icon="key",
                description="Sample rotation use Fixed Key 1 - Swift Action to enable the full combo each turn.",
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
