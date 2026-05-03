from typing import Any, cast, override

from nicegui import ui

from core.dolls import soppo
from core.types import DamageTag, FortificationLevel, SpecialAttribute, StatType
from gui.templates.doll_calculator_page import DollCalculatorPage, ModelAssumption
from gui.templates.rotation_planner import RotationPlanner


_t1: list[dict[str, Any]] = [
    {
        "name": "Ferocious Bite",
        "in_feral_form": False,
    },
    {
        "name": "Predator's Pursuit",
        "in_feral_form": False,
    },
    {
        "name": "Midnight Howl",
        "tile_target": soppo.MidnightHowlTileTargetType.FROST,
        "in_feral_form": False,
    },
    {
        "name": "Predator's Pursuit",
        "in_feral_form": True,
    },
    {
        "name": "Predator's Pursuit",
        "in_feral_form": True,
    },
    {
        "name": "Deadly Pounce (Passive)",
    },
]


_t2: list[dict[str, Any]] = [
    {
        "name": "Midnight Howl",
        "tile_target": soppo.MidnightHowlTileTargetType.FROST,
        "in_feral_form": True,
    },
    {
        "name": "Midnight Howl",
        "tile_target": soppo.MidnightHowlTileTargetType.INCINERATION,
        "in_feral_form": True,
    },
    {
        "name": "Midnight Howl (Form Swap)",
        "in_feral_form": True,
        "num_targets": 1,
        "target_tile_ascension_level": 1,
    },
    {"name": "Predator's Pursuit", "in_feral_form": True},
    {
        "name": "Deadly Pounce",
        "stacks_of_prey_mark": 10,
        "target_is_on_phase_tile": True,
        "confectance_index": 4,
    },
    {"name": "Deadly Pounce (Passive)"},
]

_t3: list[dict[str, Any]] = [
    {"name": "Ferocious Bite", "in_feral_form": False},
    {"name": "Predator's Pursuit", "in_feral_form": False},
    {
        "name": "Midnight Howl",
        "tile_target": soppo.MidnightHowlTileTargetType.FROST,
        "in_feral_form": False,
    },
    {
        "name": "Midnight Howl",
        "tile_target": soppo.MidnightHowlTileTargetType.INCINERATION,
        "in_feral_form": False,
    },
    {"name": "Predator's Pursuit", "in_feral_form": True},
    {
        "name": "Deadly Pounce",
        "stacks_of_prey_mark": 9,
        "target_is_on_phase_tile": True,
        "confectance_index": 4,
    },
    {"name": "Deadly Pounce (Passive)"},
]

sample_rotation: dict[int, list[dict[str, Any]]] = {
    1: _t1,
    2: _t2,
    3: _t3,
    4: _t3,
    5: _t3,
    6: _t3,
    7: _t3,
}


class Soppo(DollCalculatorPage):
    """Page for Soppo."""

    def __init__(self):
        super().__init__()

        self.doll = soppo.Soppo()
        self.doll.set_fortification_level(FortificationLevel.SEGMENT06)
        self.doll_subtitle: str = """Element Swap / Tile Interaction / Interception

            Sentinel / Freeze"""
        self.dandegate_link: str = "https://www.dandegate.net/dolls/soppo"
        self.doll_portrait: str = "resources/soppo.webp"

    @override
    def update_doll_abilities(self) -> None:
        doll = cast(soppo.Soppo, self.doll)

        self.option_config: dict[str, dict[str, Any]] = {
            "Predator's Pursuit": {
                "fields": [
                    {
                        "key": "in_feral_form",
                        "type": "checkbox",
                        "label": "In Feral Form",
                        "default": False,
                    }
                ],
                "function": doll.predators_pursuit.execute,
            },
            "Ferocious Bite": {
                "fields": [
                    {
                        "key": "in_feral_form",
                        "type": "checkbox",
                        "label": "In Feral Form",
                        "default": False,
                    }
                ],
                "function": doll.ferocious_bite.execute,
            },
            "Midnight Howl": {
                "fields": [
                    {
                        "key": "tile_target",
                        "type": "select",
                        "label": "Target Tile",
                        "default": soppo.MidnightHowlTileTargetType.FROST,
                        "options": [
                            soppo.MidnightHowlTileTargetType.FROST,
                            soppo.MidnightHowlTileTargetType.INCINERATION,
                            # soppo.MidnightHowlTileTargetType.ASHEN_BREATH,
                        ],
                    },
                    {
                        "key": "in_feral_form",
                        "type": "checkbox",
                        "label": "In Feral Form",
                        "default": False,
                    },
                ],
                "function": doll.midnight_howl.execute,
            },
            "Midnight Howl (Form Swap)": {
                "fields": [
                    {
                        "key": "in_feral_form",
                        "type": "checkbox",
                        "label": "In Feral Form",
                        "default": True,
                    },
                    {
                        "key": "num_targets",
                        "type": "number",
                        "label": "Targets Hit",
                        "default": 1,
                    },
                    {
                        "key": "target_tile_ascension_level",
                        "type": "select",
                        "label": "Tile Ascension Level",
                        "default": 1,
                        "options": [n for n in range(0, 4)],
                    },
                ],
                "function": doll.midnight_howl_form_swap.execute,
            },
            "Deadly Pounce": {
                "fields": [
                    {
                        "key": "stacks_of_prey_mark",
                        "type": "number",
                        "label": "Prey Mark Stacks",
                        "default": 9,
                    },
                    {
                        "key": "target_is_on_phase_tile",
                        "type": "checkbox",
                        "label": "Target on Phase Tile",
                        "default": True,
                    },
                    {
                        "key": "confectance_index",
                        "type": "select",
                        "label": "Confectance Index",
                        "default": 4,
                        "options": [n for n in range(7)],
                    },
                ],
                "function": doll.deadly_pounce_active.execute,
            },
            "Deadly Pounce (Passive)": {
                "fields": [],
                "function": doll.deadly_pounce_passive.execute,
            },
        }

    @override
    def set_initial_values(self) -> None:
        doll = cast(soppo.Soppo, self.doll)

        self.doll.initial_stats.basic_attributes[StatType.ATTACK] = 4830
        self.doll.initial_stats.basic_attributes[StatType.CRIT_RATE] = 81
        self.doll.initial_stats.basic_attributes[StatType.CRIT_DAMAGE] = 154.5

        # Attachments, common keys, imagoform, specialized traits

        # imagoform: 5+12
        # CQC elite: 0.4
        # Alva 6P33: 10
        # Imagoform (Shoot): 4+3
        # Dushevnaya Expansion Key: 10
        # Dushevnaya Passive: 10
        self.doll.additive_modifiers.special_attributes[
            SpecialAttribute.DAMAGE_BOOST
        ].set_multiplier(DamageTag.ALL, 17 + 0.4 + 10 + 4 + 3 + 10 + 10)

        # weapon: 15
        # attachment: 20
        # imagoform: 5
        # freeze boost: 1.5
        # Alva Brumal Barrier: <Alva Attack>*2/1000*1.5 = 11.4 at 3800 attack
        # Alva Covering Mode: 20
        # Freeze Unity: 0.9
        # Dushevnaya Expansion Key: 15+10
        # Dushevnaya Eulogistic Verse: 10
        # Dushevnaya Passive: 10
        # Dushevnaya Imagoform (Bud): 3
        self.doll.additive_modifiers.special_attributes[
            SpecialAttribute.DAMAGE_BOOST
        ].set_multiplier(
            DamageTag.FREEZE, 15 + 20 + 5 + 1.5 + 11.4 + 20 + 0.9 + 15 + 10 + 10 + 3
        )

        # keys: 30
        self.doll.additive_modifiers.special_attributes[
            SpecialAttribute.DAMAGE_BOOST
        ].set_multiplier(DamageTag.PHASE, 30)

        # weapon: 14
        # raid stance: 1
        self.doll.additive_modifiers.special_attributes[
            SpecialAttribute.DAMAGE_BOOST
        ].set_multiplier(DamageTag.PASSIVE, 14 + 1)

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

        # Alva 6P33: 10
        self.doll.additive_modifiers.special_attributes[
            SpecialAttribute.CRITICAL_DAMAGE
        ].set_multiplier(DamageTag.FREEZE, 10)

        # imagoform: 8
        # attack boost: 3.6
        # Alva Imagoform: 3
        self.doll.multiplicative_modifiers.basic_attributes[StatType.ATTACK] = (
            8 + 3.6 + 3
        )

    def get_default_damage_calculator_buffs(self) -> list[dict[str, Any]]:
        return [
            {"name": "Blazing Assault II"},
            {"name": "Frost Strike"},
            {
                "name": "Brumal Barrier (Alva)",
                "alva_fortification_level": FortificationLevel.SEGMENT05,
                "shield_size": 9000,
            },
            {"name": "Unity: Enhanced", "robella_initial_attack": 4800},
            {"name": "Feral Factor (Soppo)", "stacks": 20},
            {
                "name": "Feral Factor I (Soppo)",
                "soppo_fortification_level": FortificationLevel.SEGMENT06,
                "tile_level": 1,
                "stacks_of_feral_factor": 20,
            },
            {
                "name": "Feral Factor II (Soppo)",
                "soppo_fortification_level": FortificationLevel.SEGMENT06,
                "number_of_freeze_and_burn_buffs": 5,
                "stacks_of_feral_factor": 20,
            },
            {
                "name": "Feral Factor III (Soppo)",
                "soppo_fortification_level": FortificationLevel.SEGMENT06,
                "tile_level": 1,
                "stacks_of_feral_factor": 20,
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
                icon="info",
                description="Ashen Breath should be modeled as two Midnight Howl actions (one Frost tile and one Incineration tile).",
            ),
            ModelAssumption(
                icon="rule",
                description="The conditions for the passive's effect of increased damage based on having at least 3 Burn or Freeze allies is automatically satisfied. The requirement of the target having a Burn/Freeze debuff is ignored.",
            ),
        ]

    @override
    def get_rotation_planner(self) -> None:
        with ui.card().classes("w-full h-full"):

            def update_all() -> None:
                self.damage_instances = self.rotation_planner.get_all_actions()
                self.stats_update_callback(None)  # type: ignore[arg-type]

            ui.button("Update", on_click=update_all).classes("w-full")
            self.rotation_planner = RotationPlanner(options_config=self.option_config)
            self.rotation_planner.set_data(sample_rotation)
