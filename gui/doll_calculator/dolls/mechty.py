from typing import Any, cast, override

from nicegui import ui

from core.dolls import mechty
from core.types import DamageTag, FortificationLevel, SpecialAttribute, StatType
from gui.templates.doll_calculator_page import DollCalculatorPage, ModelAssumption
from gui.templates.rotation_planner import RotationPlanner


_t1 = [
    {
        "name": "Dreamquake",
    },
    {
        "name": "Bedtime Warmup",
        "in_turbo_mode": True,
        "enhanced_by_dreamquake": True,
        "is_sleepwalking": True,
    },
    {
        "name": "Dreamquake",
    },
]

_t2 = [
    {
        "name": "Bedtime Warmup",
        "in_turbo_mode": True,
        "enhanced_by_dreamquake": False,
        "is_sleepwalking": True,
    },
    {
        "name": "Dreamquake",
    },
    {
        "name": "Bedtime Warmup",
        "in_turbo_mode": True,
        "enhanced_by_dreamquake": True,
        "is_sleepwalking": True,
    },
]

sample_rotation: dict[int, list[dict]] = {
    1: _t1,
    2: _t2,
    3: _t1,
    4: _t2,
    5: _t1,
    6: _t2,
    7: _t1,
}


class Mechty(DollCalculatorPage):
    """Page for Mechty."""

    def __init__(self):
        super().__init__()

        self.doll = mechty.Mechty()
        self.doll.set_fortification_level(FortificationLevel.SEGMENT06)
        self.doll_subtitle: str = """Damage Boost / Tile / Basic Attack Enhancement

            Support / Corrosion"""
        self.dandegate_link: str = "https://www.dandegate.net/dolls/mechty"
        self.doll_portrait: str = "resources/mechty.webp"

    @override
    def update_doll_abilities(self) -> None:
        doll = cast(mechty.Mechty, self.doll)

        self.option_config: dict[str, dict[str, Any]] = {
            "Bedtime Warmup": {
                "fields": [
                    {
                        "key": "in_turbo_mode",
                        "type": "checkbox",
                        "label": "Turbo Mode",
                        "default": True,
                    },
                    {
                        "key": "enhanced_by_dreamquake",
                        "type": "checkbox",
                        "label": "Enhanced by Dreamquake",
                        "default": True,
                    },
                    {
                        "key": "is_sleepwalking",
                        "type": "checkbox",
                        "label": "Sleepwalking",
                        "default": True,
                    },
                ],
                "function": doll.bedtime_warmup.execute,
            },
            "Dreamquake": {
                "fields": [],
                "function": doll.dreamquake.execute,
            },
        }

    @override
    def set_initial_values(self) -> None:
        doll = cast(mechty.Mechty, self.doll)

        doll.initial_stats.basic_attributes[StatType.ATTACK] = 3800
        doll.initial_stats.basic_attributes[StatType.CRIT_RATE] = 75
        doll.initial_stats.basic_attributes[StatType.CRIT_DAMAGE] = 150

        doll.additive_modifiers.special_attributes[
            SpecialAttribute.DAMAGE_BOOST
        ].set_multiplier(DamageTag.ALL, 22)
        doll.additive_modifiers.special_attributes[
            SpecialAttribute.DAMAGE_BOOST
        ].set_multiplier(DamageTag.CORROSION, 26)
        doll.additive_modifiers.special_attributes[
            SpecialAttribute.DAMAGE_BOOST
        ].set_multiplier(DamageTag.PHASE, 15)

        doll.multiplicative_modifiers.basic_attributes[StatType.ATTACK] = 8

    def get_default_damage_calculator_buffs(self) -> list[dict[str, Any]]:
        return [
            {"name": "Attack Up II"},
            {
                "name": "Dream Guardian",
            },
            {
                "name": "Nightmare Form",
                "mechty_fortification_level": FortificationLevel.SEGMENT06,
            },
            {
                "name": "Patch Mode (Mechty)",
                "mechty_fortification_level": FortificationLevel.SEGMENT06,
            },
            {
                "name": "Turbo Mode (Mechty)",
                "mechty_fortification_level": FortificationLevel.SEGMENT06,
            },
            {
                "name": "Sleep Aid Kit (Mechty)",
                "mechty_fortification_level": FortificationLevel.SEGMENT06,
                "stacks": 3,
            },
            {"name": "Dreamscape Exhilaration (Mechty)", "stacks": 6},
        ]

    def get_default_damage_calculator_debuffs(self) -> list[dict[str, Any]]:
        return [
            {"name": "Defense Down II"},
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
                icon="key",
                description="Expansion Key - Sleepberserking Syndrome is active.",
                link_label="Dandegate",
                link_target="https://www.dandegate.net/dolls/mechty/keys/expansion-key-sleepberserking-syndrome",
            ),
            ModelAssumption(
                icon="hotel",
                description="Sample rotation assumes Mechty is Sleepwalking with three stacks of Sleep Aid Kit each turn.",
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
