from typing import Any, cast, override

from nicegui import ui

from core.dolls import soppo
from core.types import DamageTag, FortificationLevel, SpecialAttribute, StatType
from gui.templates.doll_calculator_page import DollCalculatorPage, ModelAssumption
from gui.templates.rotation_planner import RotationPlanner


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
            "Hunting Fang": {
                "fields": [
                    {
                        "key": "in_feral_form",
                        "type": "checkbox",
                        "label": "In Mad Dog Mode",
                        "default": False,
                    }
                ],
                "function": doll.hunting_fang.execute,
            },
            "Vicious Bite": {
                "fields": [
                    {
                        "key": "in_feral_form",
                        "type": "checkbox",
                        "label": "In Mad Dog Mode",
                        "default": False,
                    }
                ],
                "function": doll.vicious_bite.execute,
            },
            "Lunar Howl": {
                "fields": [
                    {
                        "key": "tile_target",
                        "type": "select",
                        "label": "Target Tile",
                        "default": soppo.LunarHowlTileTargetType.FROST,
                        "options": [
                            soppo.LunarHowlTileTargetType.FROST,
                            soppo.LunarHowlTileTargetType.INCINERATION,
                            # soppo.LunarHowlTileTargetType.SMOLDERING_SUSPIRE,
                        ],
                    },
                    {
                        "key": "in_feral_form",
                        "type": "checkbox",
                        "label": "In Mad Dog Mode",
                        "default": False,
                    },
                ],
                "function": doll.lunar_howl.execute,
            },
            "Lunar Howl (Form Swap)": {
                "fields": [
                    {
                        "key": "in_feral_form",
                        "type": "checkbox",
                        "label": "In Mad Dog Mode",
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
                "function": doll.lunar_howl_form_swap.execute,
            },
            "Fatal Pounce": {
                "fields": [
                    {
                        "key": "stacks_of_prey_mark",
                        "type": "number",
                        "label": "Hunting Mark Stacks",
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
                "function": doll.fatal_pounce_active.execute,
            },
            "Fatal Pounce (Passive)": {
                "fields": [],
                "function": doll.fatal_pounce_passive.execute,
            },
        }

        self.add_elemental_tile_actions_for_element(
            self.option_config,
            DamageTag.FREEZE,
        )
        self.add_elemental_tile_actions_for_element(
            self.option_config,
            DamageTag.BURN,
        )

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

    @override
    def get_model_assumptions(self) -> list[ModelAssumption]:
        return [
            ModelAssumption(
                icon="info",
                description="Landing on a Smoldering Suspire tile for Lunar Howl should be modeled as two Lunar Howl actions (one Frost tile and one Incineration tile).",
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
