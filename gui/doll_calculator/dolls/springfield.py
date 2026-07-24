from nicegui import ui

from gui.templates.doll_calculator_page import DollCalculatorPage, ModelAssumption
from gui.templates.rotation_planner import RotationPlanner
from typing import Any, cast, override
from core.types import DamageTag, FortificationLevel, SpecialAttribute, StatType
from core.dolls import springfield

_t1: list[dict[str, Any]] = [
    {"name": "Path of Protection"},
    {"name": "Peck (Elsin)", "stacks_of_inundance": 1, "target_has_taryz": True},
    {"name": "Peck (Elsin)", "stacks_of_inundance": 2, "target_has_taryz": True},
    {"name": "Peck (Elsin)", "stacks_of_inundance": 11, "target_has_taryz": True},
]

_t1.extend({"name": "Support Action (Taryz)"} for _ in range(4))
_t1.extend({"name": "Counterattack (Taryz)"} for _ in range(4))

_t2: list[dict[str, Any]] = [
    {"name": "Intel Manipulation"},
    {"name": "Peck (Elsin)", "stacks_of_inundance": 1, "target_has_taryz": True},
    {"name": "Peck (Elsin)", "stacks_of_inundance": 11, "target_has_taryz": True},
]

_t2.extend({"name": "Support Action (Taryz)"} for _ in range(4))
_t2.extend({"name": "Counterattack (Taryz)"} for _ in range(4))

_t3: list[dict[str, Any]] = [
    {"name": "Peck (Elsin)", "stacks_of_inundance": 1, "target_has_taryz": True},
    {"name": "Peck (Elsin)", "stacks_of_inundance": 11, "target_has_taryz": True},
]

_t3.extend({"name": "Support Action (Taryz)"} for _ in range(4))
_t3.extend({"name": "Counterattack (Taryz)"} for _ in range(4))

_t4: list[dict[str, Any]] = [
    {"name": "Path of Protection"},
    {"name": "Peck (Elsin)", "stacks_of_inundance": 1, "target_has_taryz": True},
    {"name": "Intel Manipulation"},
    {"name": "Peck (Elsin)", "stacks_of_inundance": 2, "target_has_taryz": True},
    {"name": "Peck (Elsin)", "stacks_of_inundance": 11, "target_has_taryz": True},
]

_t4.extend({"name": "Support Action (Taryz)"} for _ in range(4))
_t4.extend({"name": "Counterattack (Taryz)"} for _ in range(4))


sample_rotation: dict[int, list[dict]] = {
    1: _t1,
    2: _t2,
    3: _t3,
    4: _t4,
    5: _t3,
    6: _t2,
    7: _t1,
}


class Springfield(DollCalculatorPage):
    """Page for Springfield."""

    def __init__(self):
        super().__init__()

        self._springfield: springfield.Springfield = springfield.Springfield()
        self.doll = self._springfield
        self.doll.set_fortification_level(FortificationLevel.SEGMENT06)
        self.doll_subtitle: str = """Heal & Stability Regen / Summon / Overflow Damage

            Support / Hydro"""
        self.dandegate_link: str = "https://www.dandegate.net/dolls/springfield"
        self.doll_portrait: str = "resources/springfield.webp"

    @override
    def update_doll_abilities(self) -> None:
        doll = cast(springfield.Springfield, self.doll)

        self.option_config: dict[str, dict[str, Any]] = {
            "Gentle Approach": {
                "fields": [],
                "function": doll.gentle_approach.execute,
            },
            "Intel Manipulation": {
                "fields": [],
                "function": doll.intel_manipulation.execute,
            },
            "Path of Protection": {
                "fields": [],
                "function": doll.path_of_protection.execute,
            },
            "Support Action (Taryz)": {
                "fields": [],
                "function": doll.support_action.execute,
            },
            "Counterattack (Taryz)": {
                "fields": [],
                "function": doll.counterattack.execute,
            },
            "Peck (Elsin)": {
                "fields": [
                    {
                        "key": "stacks_of_inundance",
                        "label": "Stacks of Inundance",
                        "type": "number",
                        "default": 11,
                    },
                    {
                        "key": "target_has_taryz",
                        "label": "Target has Taryz",
                        "type": "checkbox",
                        "default": True,
                    },
                ],
                "function": doll.peck.execute,
            },
        }

    @override
    def set_initial_values(self) -> None:
        self.doll.initial_stats.basic_attributes[StatType.ATTACK] = 2545
        self.doll.initial_stats.basic_attributes[StatType.HEALTH] = 7971
        self.doll.initial_stats.basic_attributes[StatType.CRIT_RATE] = 91
        self.doll.initial_stats.basic_attributes[StatType.CRIT_DAMAGE] = 150

        # Radiance: 2.5
        # Key: 7
        # Key: 7
        # Imagoform Shoot: 4
        self.doll.additive_modifiers.special_attributes[
            SpecialAttribute.DAMAGE_BOOST
        ].set_multiplier(DamageTag.ALL, 20.5)

        # Radiance: 5
        # Attachment: 20
        # Imagoform Embryo: 3
        # Imagoform Sprout: 5
        self.doll.additive_modifiers.special_attributes[
            SpecialAttribute.DAMAGE_BOOST
        ].set_multiplier(DamageTag.HYDRO, 33)

        # Key: 10
        self.doll.additive_modifiers.special_attributes[
            SpecialAttribute.DAMAGE_BOOST
        ].set_multiplier(DamageTag.PHASE, 10)

        # Follow-up Strike: 0.5
        self.doll.additive_modifiers.special_attributes[
            SpecialAttribute.DAMAGE_BOOST
        ].set_multiplier(DamageTag.STABILITY_BROKEN, 0.5)

        # Imagoform Bud: 4
        # Attack Unity: 1
        # Fighting Spirit: 1.8
        self.doll.multiplicative_modifiers.basic_attributes[StatType.ATTACK] = 6.8

        # Ichor Conversion: 0.8% of initial max HP
        self.doll.additive_modifiers.basic_attributes[StatType.ATTACK] = (
            0.008 * self.doll.initial_stats.basic_attributes[StatType.HEALTH]
        )

        # Imagoform Bud: 4
        # Fighting Spirit: 1.8
        # HP Boost: 3.6
        # Radiance: 15
        self.doll.multiplicative_modifiers.basic_attributes[StatType.HEALTH] = 24.4

        # Ichor Resonance: 0.4% of initial Attack
        self.doll.additive_modifiers.basic_attributes[StatType.HEALTH] = (
            0.004 * self.doll.initial_stats.basic_attributes[StatType.ATTACK]
        )

        self._springfield.refresh_elsin()

    def get_default_damage_calculator_buffs(self) -> list[dict[str, Any]]:
        return [
            {"name": "Attack Up II"},
            {
                "name": "Overflowing Care",
                "springfield_fortification_level": FortificationLevel.SEGMENT06,
                "percent_excess_healing": 105,
            },
            {
                "name": "Deep-Rooted Bonds",
            },
            {
                "name": "Eagle's Vigilance (Taryz)",
                "springfield_fortification_level": FortificationLevel.SEGMENT06,
            },
            {
                "name": "Elsin",
            },
        ]

    def get_default_damage_calculator_debuffs(self) -> list[dict[str, Any]]:
        return [
            {"name": "Defense Down II"},
            {
                "name": "False Intelligence",
                "springfield_fortification_level": FortificationLevel.SEGMENT06,
            },
            {
                "name": "Taryz",
                "springfield_fortification_level": FortificationLevel.SEGMENT06,
            },
            {
                "name": "Vulnerability Analysis",
                "springfield_fortification_level": FortificationLevel.SEGMENT06,
                "stacks": 3,
            },
        ]

    @override
    def get_model_assumptions(self) -> list[ModelAssumption]:
        return [
            ModelAssumption(
                icon="flutter_dash",
                description="Taryz's attacks are set to 100 potency but uses the health scalars appropriately in Damage Calculator.",
            ),
            ModelAssumption(
                icon="flutter_dash",
                description="Using Eagle's Vigilance (Taryz) assumes Hydro damage is being dealt. It will only apply to out-of-turn (passive) attacks.",
            ),
            ModelAssumption(
                icon="water_drop",
                description="Using False Intelligence assumes the target is in Stability Break independently of the toggle in Damage Calculator.",
            ),
            ModelAssumption(
                icon="key",
                description="Expansion Key - Watching Each Other is active.",
                link_label="Dandegate",
                link_target="https://www.dandegate.net/dolls/springfield/keys/expansion-key-vigilant-bond",
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
