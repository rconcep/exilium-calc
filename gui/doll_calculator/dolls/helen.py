from nicegui import ui

from gui.templates.doll_calculator_page import DollCalculatorPage, ModelAssumption
from gui.templates.rotation_planner import RotationPlanner
from typing import Any, cast, override
from core.types import DamageTag, FortificationLevel, SpecialAttribute, StatType
from core.dolls import helen


sample_rotation: dict[int, list[dict]] = {
    1: [{"name": "Guardian", "stacks_icy_edge": 20}],
    2: [{"name": "Guardian", "stacks_icy_edge": 20}],
    3: [{"name": "Guardian", "stacks_icy_edge": 20}],
    4: [{"name": "Guardian", "stacks_icy_edge": 20}],
    5: [{"name": "Guardian", "stacks_icy_edge": 20}],
    6: [{"name": "Guardian", "stacks_icy_edge": 20}],
    7: [{"name": "Guardian", "stacks_icy_edge": 20}],
}


class Helen(DollCalculatorPage):
    """Page for Helen."""

    def __init__(self):
        super().__init__()

        self.doll = helen.Helen()
        self.doll.set_fortification_level(FortificationLevel.SEGMENT06)
        self.doll_subtitle: str = """Damage Distribution / Tile / Shield

            Bulwark / Freeze"""
        self.dandegate_link: str = "https://www.dandegate.net/dolls/helen"
        self.doll_portrait: str = "resources/helen.webp"

    @override
    def update_doll_abilities(self) -> None:
        doll = cast(helen.Helen, self.doll)
        self.option_config: dict[str, dict[str, Any]] = {
            "Guardian": {
                "fields": [
                    {
                        "key": "stacks_icy_edge",
                        "type": "number",
                        "label": "Icy Edge stacks",
                        "default": 20,
                    },
                ],
                "function": doll.guardian.execute,
            },
        }

    @override
    def set_initial_values(self) -> None:
        self.doll.initial_stats.basic_attributes[StatType.ATTACK] = 3000
        self.doll.initial_stats.basic_attributes[StatType.DEFENSE] = 2000
        self.doll.initial_stats.basic_attributes[StatType.CRIT_RATE] = 80.0
        self.doll.initial_stats.basic_attributes[StatType.CRIT_DAMAGE] = 150.0

        # Attachments, common keys, imagoform, specialized traits
        # attachment: 20
        # imagoform (sprout): 5
        self.doll.additive_modifiers.special_attributes[
            SpecialAttribute.DAMAGE_BOOST
        ].set_multiplier(DamageTag.FREEZE, 25)

        # Common Key: 10
        self.doll.additive_modifiers.special_attributes[
            SpecialAttribute.DAMAGE_BOOST
        ].set_multiplier(DamageTag.PHASE, 10)

        # Common Key: 10
        self.doll.additive_modifiers.special_attributes[
            SpecialAttribute.DAMAGE_BOOST
        ].set_multiplier(DamageTag.SHOTGUN_AMMO, 10)

        # imagoform: 12
        # onslaught stance: 1
        self.doll.additive_modifiers.special_attributes[
            SpecialAttribute.DAMAGE_BOOST
        ].set_multiplier(DamageTag.ALL, 13)

        # imagoform: 8
        self.doll.multiplicative_modifiers.basic_attributes[StatType.DEFENSE] = 8

        # imagoform: 4
        # attack boost: 3.6
        # attack unity: 1
        self.doll.multiplicative_modifiers.basic_attributes[StatType.ATTACK] = 8.6

    def get_default_damage_calculator_buffs(self) -> list[dict[str, Any]]:
        return [
            {"name": "Attack Up III"},
            {"name": "Defense Up III"},
            {"name": "Critical Damage Up II"},
            {
                "name": "Brumal Barrier (Alva)",
                "alva_fortification_level": FortificationLevel.SEGMENT05,
                "shield_size": 9000,
            },
            {
                "name": "Covering Mode (Alva)",
            },
            {
                "name": "Frostchill Drive (Helen)",
                "helen_fortification_level": FortificationLevel.SEGMENT05,
                "stacks": 3,
            },
        ]

    def get_default_damage_calculator_debuffs(self) -> list[dict[str, Any]]:
        return [
            {"name": "Defense Down II"},
            {
                "name": "Hypothermia",
                "alva_fortification_level": FortificationLevel.SEGMENT05,
            },
            {
                "name": "Frostbite",
            },
        ]

    @override
    def get_model_assumptions(self) -> list[ModelAssumption]:
        return [
            ModelAssumption(
                icon="shield",
                description="Helen's Defense-to-Attack conversion and Defense/HP passive boosts are applied during damage calculation.",
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
