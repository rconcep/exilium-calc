from nicegui import ui

from gui.templates.doll_calculator_page import DollCalculatorPage, ModelAssumption
from gui.templates.rotation_planner import RotationPlanner
from typing import Any, override
from core.types import FortificationLevel, StatType, Unit, SpecialAttribute, DamageTag
from core.dolls import lainie


sample_rotation: dict[int, list[dict]] = {
    1: [
        # Summon Simulacrum
        {
            "name": "Offense Simulation (Simulacrum)",
            "number_of_additional_targets": 1,
            "hit_same_target_as_combat_algorithm": True,
        },
        {
            "name": "Combat Algorithm",
            "target_has_nonpositive_defense": True,
        },
    ],
    2: [
        {
            "name": "Offense Simulation (Simulacrum)",
            "number_of_additional_targets": 1,
            "hit_same_target_as_combat_algorithm": True,
        },
        {
            "name": "Combat Algorithm",
            "target_has_nonpositive_defense": True,
        },
    ],
    3: [
        {
            "name": "Offense Simulation (Simulacrum)",
            "number_of_additional_targets": 1,
            "hit_same_target_as_combat_algorithm": True,
        },
        {
            "name": "Combat Algorithm",
            "target_has_nonpositive_defense": True,
        },
    ],
    4: [
        {
            "name": "Offense Simulation (Simulacrum)",
            "number_of_additional_targets": 1,
            "hit_same_target_as_combat_algorithm": True,
        },
        {
            "name": "Combat Algorithm",
            "target_has_nonpositive_defense": True,
        },
    ],
    5: [
        {
            "name": "Offense Simulation (Simulacrum)",
            "number_of_additional_targets": 1,
            "hit_same_target_as_combat_algorithm": True,
        },
        {
            "name": "Combat Algorithm",
            "target_has_nonpositive_defense": True,
        },
    ],
    6: [
        {
            "name": "Offense Simulation (Simulacrum)",
            "number_of_additional_targets": 1,
            "hit_same_target_as_combat_algorithm": True,
        },
        {
            "name": "Combat Algorithm",
            "target_has_nonpositive_defense": True,
        },
    ],
    7: [
        {
            "name": "Offense Simulation (Simulacrum)",
            "number_of_additional_targets": 1,
            "hit_same_target_as_combat_algorithm": True,
        },
        {
            "name": "Combat Algorithm",
            "target_has_nonpositive_defense": True,
        },
    ],
}


class Lainie(DollCalculatorPage):
    """Page for Lainie."""

    def __init__(self):
        super().__init__()

        self._lainie: lainie.Lainie = lainie.Lainie()
        self.doll = self._lainie
        self.doll.set_fortification_level(FortificationLevel.SEGMENT06)
        self.doll_subtitle: str = """Summon Damage / Defense Ignore

            Sentinel / Physical"""
        self.dandegate_link: str = "https://www.dandegate.net/dolls/lainie"
        self.doll_portrait: str = "resources/lainie.webp"

    @override
    def update_doll_abilities(self) -> None:
        self.option_config: dict[str, dict[str, Any]] = {
            "Victory Protocol": {
                "fields": [],
                "function": self._lainie.victory_protocol.execute,
            },
            "Combat Algorithm": {
                "fields": [
                    {
                        "key": "target_has_nonpositive_defense",
                        "type": "checkbox",
                        "label": "Target Defense ≤ 0",
                        "default": True,
                    },
                ],
                "function": self._lainie.combat_algorithm.execute,
            },
            "Computational Crush": {
                "fields": [],
                "function": self._lainie.computational_crush.execute,
            },
            "Perplexed Reflex (Simulacrum)": {
                "fields": [],
                "function": self._lainie.perplexed_reflex.execute,
            },
            "Offense Simulation (Simulacrum)": {
                "fields": [
                    {
                        "key": "number_of_additional_targets",
                        "type": "number",
                        "label": "Number of additional targets (beyond the first)",
                        "default": 1,
                    },
                    {
                        "key": "hit_same_target_as_combat_algorithm",
                        "type": "checkbox",
                        "label": "Hit same target as Combat Algorithm",
                        "default": True,
                    },
                ],
                "function": self._lainie.offense_simulation.execute,
            },
            "Hashrate Overclock (Simulacrum)": {
                "fields": [],
                "function": self._lainie.hashrate_overclock.execute,
            },
        }

    @override
    def set_initial_values(self) -> None:
        self.doll.initial_stats.basic_attributes[StatType.ATTACK] = 3900

        # Base + Universal Keys + Weapon Attachment
        self.doll.initial_stats.basic_attributes[StatType.CRIT_RATE] = 20 + 15 + 30

        # Base + Universal Keys + Signature Weapon + Weapon Attachment
        self.doll.initial_stats.basic_attributes[StatType.CRIT_DAMAGE] = (
            120 + 20 + 25 + 15
        )
        self.doll.initial_stats.basic_attributes[StatType.HEALTH] = 5200

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

        # imagoform: 8
        self.doll.additive_modifiers.special_attributes[
            SpecialAttribute.DAMAGE_BOOST
        ].set_multiplier(DamageTag.PHYSICAL_SUMMON, 8)

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

        # Project Helios: 20 + 15
        # Yoohee Sparkling Centerstage: 10
        self.doll.additive_modifiers.special_attributes[
            SpecialAttribute.DEFENSE_IGNORE
        ].set_multiplier(DamageTag.PHYSICAL, 20 + 15 + 10)

        # Sync the Simulacrum now that real stats are in place.
        self._lainie.refresh_simulacrum()

    @override
    def stats_update_callback(self, update: ui.number) -> None:  # type: ignore[override]
        # Keep the Simulacrum's snapshot current before deepcopy is taken
        # for every damage calculation inside the parent's callback.
        self._lainie.refresh_simulacrum()
        super().stats_update_callback(update)

    @override
    def get_model_assumptions(self) -> list[ModelAssumption]:
        return [
            ModelAssumption(
                icon="group_add",
                description="Simulacrum is modeled as a live snapshot of Lainie's current stats and is refreshed on stat updates.",
            ),
            ModelAssumption(
                icon="key",
                description="Expansion Key - Algorithmic Stack is active.",
                link_label="Dandegate",
                link_target="https://www.dandegate.net/dolls/lainie/keys/expansion-key-superimposed-algorithm",
            ),
            ModelAssumption(
                icon="group_work",
                description="Combat Algorithm: Checking the Defense <= 0 condition implies it was triggered by Offense Simulation.",
            ),
            ModelAssumption(
                icon="group_work",
                description="Offense Simulation: Unchecking the 'hit same target...' condition implies it was triggered by Combat Algorithm.",
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
