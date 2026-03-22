from nicegui import ui

from decimal import Decimal, ROUND_DOWN, ROUND_UP
from typing import Any, Callable
import copy
from core.types import (
    Doll,
    Unit,
    StatType,
    DamageTag,
    SpecialAttribute,
)
from core.combat import DamageInstance, CombatSummary, calculate_damage
from core.buffs import Buff, Debuff, buffs_option_config, debuffs_option_config
from gui.templates.doll_calculator_page import DollCalculatorPage
from gui.templates.single_configurable_item_editor import SingleConfigurableItemEditor
from gui.templates.selectable_chips_editor import SelectableChipsEditor
from gui.styles.graphs import get_bar_chart_template
from gui.styles.descriptions import get_tag_description, get_stat_description


def get_relevant_target_stats() -> list[StatType]:
    """Returns the subset of StatType that is relevant to damage calculations."""
    return [StatType.HEALTH, StatType.DEFENSE, StatType.STABILITY_DAMAGE_REDUCTION]


class DamageCalculator:
    """A tool for simulating a Doll's action against a specified target."""

    def __init__(self, doll_calculator: DollCalculatorPage):
        """
        Arguments:
        doll_calculator -- The DollCalculatorPage this instance resides on - for referring to the Doll used in calculations.
        """
        self.doll_calculator: DollCalculatorPage = doll_calculator
        self.doll: Doll = self.doll_calculator.doll
        self.target: Unit = Unit()

        self.buffs_selector: SelectableChipsEditor
        self.debuffs_selector: SelectableChipsEditor

        self.initialize_target()

        self.target_phase_weaknesses_exploited: ui.select
        self.target_stability_broken: ui.switch

        self.bar_chart_plot: ui.plotly
        self.combat_summary: CombatSummary = CombatSummary()

        self.bar_chart: dict = get_bar_chart_template()
        self.bar_chart["data"][0]["x"] = ["normal", "expected", "crit"]
        self.bar_chart["layout"]["title"]["text"] = "Damage"

        self.results_labels: dict[str, ui.label] = {}

        with ui.row().classes("h-full"):
            with ui.card().classes("w-115 h-full"):
                self._attacker_section()
            with ui.card().classes("w-80 h-200"):
                self._results_section()
            with ui.card().classes("w-115 h-full"):
                self._target_section()

    def initialize_target(self):
        """Sets the target to initial values."""
        self.target.initial_stats.basic_attributes[StatType.DEFENSE] = 5000
        self.target.initial_stats.basic_attributes[StatType.HEALTH] = 11e6
        self.target.initial_stats.basic_attributes[
            StatType.STABILITY_DAMAGE_REDUCTION
        ] = 60

    def calculate(self, data):
        """Performs the combat calculation according to currently defined values
        and updates elements for displaying calculation results.
        """
        ui.notify("Calculating", type="info", group=False)

        keyword_args: dict[str, Any] = {}
        option_config: dict[str, Any] = self.doll_calculator.option_config
        combat_action: Callable = option_config[data["type"]]["function"]

        for field in option_config[data["type"]]["fields"]:
            field_name: str = field["key"]
            field_value: int = data[field_name]
            keyword_args[field_name] = field_value

        di: DamageInstance = combat_action(**keyword_args)

        stability_broken: bool = self.target_stability_broken.value
        phase_weaknesses_exploited: int = self.target_phase_weaknesses_exploited.value  # type: ignore

        self.combat_summary = calculate_damage(
            copy.deepcopy(self.doll),
            copy.deepcopy(self.target),
            di,
            is_stability_broken=stability_broken,
            phase_weaknesses_exploited=phase_weaknesses_exploited,
            buffs_before=self.get_all_buffs(),
            debuffs_before=self.get_all_debuffs(),
        )

        self._update_results_card()

    def _update_results_card(self) -> None:
        """Updates the text and graphics on the results panel."""
        self.results_labels["non_critical_damage"].text = Decimal(
            self.combat_summary.non_critical_damage
        ).quantize(Decimal("0.01"), rounding=ROUND_DOWN)
        self.results_labels["expected_damage"].text = Decimal(
            self.combat_summary.expected_damage
        ).quantize(Decimal("0.01"), rounding=ROUND_DOWN)
        self.results_labels["critical_damage"].text = Decimal(
            self.combat_summary.critical_damage
        ).quantize(Decimal("0.01"), rounding=ROUND_DOWN)
        self.results_labels["critical_rate"].text = (
            str(
                Decimal(self.combat_summary.effective_critical_rate * 100).quantize(
                    Decimal("0.01"), rounding=ROUND_DOWN
                )
            )
            + "%"
        )
        self.results_labels["critical_damage_multiplier"].text = (
            str(
                Decimal(
                    self.combat_summary.effective_critical_damage_multiplier * 100
                ).quantize(Decimal("0.01"), rounding=ROUND_DOWN)
            )
            + "%"
        )
        self.results_labels["effective_attack"].text = Decimal(
            self.combat_summary.effective_attack
        ).quantize(Decimal("0"), rounding=ROUND_UP)
        self.results_labels["effective_defense"].text = Decimal(
            self.combat_summary.effective_defense
        ).quantize(Decimal("0"), rounding=ROUND_UP)
        self.results_labels["effective_damage_multiplier"].text = (
            str(
                Decimal(self.combat_summary.effective_damage_multiplier * 100).quantize(
                    Decimal("0.01"), rounding=ROUND_DOWN
                )
            )
            + "%"
        )
        self.results_labels["negative_defense"].text = (
            str(
                Decimal(self.combat_summary.negative_defense).quantize(
                    Decimal("0.01"), rounding=ROUND_DOWN
                )
            )
            + "%"
        )

        y: list[float] = [
            self.combat_summary.non_critical_damage,
            self.combat_summary.expected_damage,
            self.combat_summary.critical_damage,
        ]

        self.bar_chart["data"][0]["y"] = y
        self.bar_chart["data"][0]["text"] = [
            str(Decimal(val).quantize(Decimal("0.1"), rounding=ROUND_DOWN)) for val in y
        ]

        ui.update(self.bar_chart_plot)

    def get_all_buffs(self) -> list[Buff]:
        """Returns all of the buffs specified in the buff_selector."""
        all_buffs: list[Buff] = []

        for buff in self.buffs_selector.data:
            keyword_args: dict[str, Any] = {}
            buff_constructor: Callable = buffs_option_config[buff["name"]]["function"]

            for field in buffs_option_config[buff["name"]]["fields"]:
                field_name: str = field["key"]
                field_value: int = buff[field_name]
                keyword_args[field_name] = field_value

            buff_instance: Buff | list[Buff] = buff_constructor(**keyword_args)
            if isinstance(buff_instance, Buff):
                all_buffs.append(buff_instance)
            elif isinstance(buff_instance, list):
                all_buffs += buff_instance

        return all_buffs

    def get_all_debuffs(self) -> list[Debuff]:
        """Returns all of the debuffs specified in the debuff_selector."""
        all_debuffs: list[Debuff] = []

        for debuff in self.debuffs_selector.data:
            keyword_args: dict[str, Any] = {}
            debuff_constructor: Callable = debuffs_option_config[debuff["name"]][
                "function"
            ]

            for field in debuffs_option_config[debuff["name"]]["fields"]:
                field_name: str = field["key"]
                field_value: int = debuff[field_name]
                keyword_args[field_name] = field_value

            debuff_instance: Debuff | list[Debuff] = debuff_constructor(**keyword_args)
            if isinstance(debuff_instance, Debuff):
                all_debuffs.append(debuff_instance)
            elif isinstance(debuff_instance, list):
                all_debuffs += debuff_instance

        return all_debuffs

    def _attacker_section(self):
        """Generates the elements in the Attacker section."""
        ui.label("Attacker").props("header")
        ui.separator()

        editor = SingleConfigurableItemEditor(
            option_config=self.doll_calculator.option_config,
            title="",
            subtitle="",
            selector_label="Attack Skills",
            save_callback=self.calculate,
        )

        self.buffs_selector: SelectableChipsEditor = SelectableChipsEditor(
            options=list(buffs_option_config.keys()),
            option_config=buffs_option_config,
            title="Buffs",
            allow_duplicates=True,
        )

    def _results_section(self):
        """Generates the elements in the Results section."""
        self.bar_chart_plot = ui.plotly(self.bar_chart).classes("w-full h-80")

        with ui.list().props("bordered dense separator").classes("w-full"):
            ui.item_label("Combat Results").props("header").classes("text-bold")
            ui.separator()

            with ui.item():
                with ui.item_section().props(""):
                    ui.item_label("Damage")
                with ui.item_section().props("side"):
                    self.results_labels["non_critical_damage"] = ui.label()

            with ui.item():
                with ui.item_section().props(""):
                    ui.item_label("Expected Damage")
                    ui.item_label("Average").props("caption")
                with ui.item_section().props("side"):
                    self.results_labels["expected_damage"] = ui.label()

            with ui.item():
                with ui.item_section().props(""):
                    ui.item_label("Critical Damage")
                with ui.item_section().props("side"):
                    self.results_labels["critical_damage"] = ui.label()

            with ui.item():
                with ui.item_section().props(""):
                    ui.item_label("Critical Rate")
                with ui.item_section().props("side"):
                    self.results_labels["critical_rate"] = ui.label()

            with ui.item():
                with ui.item_section().props(""):
                    ui.item_label("Critical Damage Multiplier")
                with ui.item_section().props("side"):
                    self.results_labels["critical_damage_multiplier"] = ui.label()

            with ui.item():
                with ui.item_section().props(""):
                    ui.item_label("Effective Attack")
                with ui.item_section().props("side"):
                    self.results_labels["effective_attack"] = ui.label()

            with ui.item():
                with ui.item_section().props(""):
                    ui.item_label("Effective Defense")
                with ui.item_section().props("side"):
                    self.results_labels["effective_defense"] = ui.label()

            with ui.item():
                with ui.item_section().props(""):
                    ui.item_label("Effective Potency")
                    # ui.item_label('description').props('caption')
                with ui.item_section().props("side"):
                    self.results_labels["effective_damage_multiplier"] = ui.label()

            with ui.item():
                with ui.item_section().props(""):
                    ui.item_label("Negative Defense")
                    ui.item_label("Defense ignore beyond 100%").props("caption")
                with ui.item_section().props("side"):
                    self.results_labels["negative_defense"] = ui.label()

    def _target_section(self):
        """Generates the elements in the Target section."""
        ui.label("Target").props("header")
        ui.separator()
        with ui.grid(columns="55% auto").classes("w-full"):
            self.target_phase_weaknesses_exploited = ui.select(
                options=[0, 1, 2], value=2, label="Phase Weaknesses Exploited"
            )
            self.target_stability_broken = ui.switch("Stability Broken", value=True)

        self.debuffs_selector: SelectableChipsEditor = SelectableChipsEditor(
            options=list(debuffs_option_config.keys()),
            option_config=debuffs_option_config,
            title="Debuffs",
            allow_duplicates=True,
        )

        with ui.scroll_area().classes("w-full h-full"):
            with ui.list().props("bordered dense separator").classes("w-full"):
                ui.separator()
                for stat in get_relevant_target_stats():
                    with ui.item():
                        with ui.item_section().props(""):
                            ui.item_label(stat)
                            ui.item_label(get_stat_description(stat)).props("caption")
                        with ui.item_section().props("side"):
                            ui.number(value=0, min=0, precision=2).bind_value(
                                self.target.initial_stats.basic_attributes, stat
                            )

            with ui.expansion(text="Increased Damage Taken", group="target").classes(
                "w-full"
            ):
                with ui.list().props("bordered dense separator").classes("w-full"):
                    for tag in DamageTag:
                        with ui.item():
                            with ui.item_section().props("no-wrap"):
                                ui.item_label(tag)
                                ui.item_label(get_tag_description(tag)).props("caption")
                            with ui.item_section().props("side"):
                                ui.number(value=0, min=0, precision=2).bind_value(
                                    self.target.initial_stats.special_attributes[
                                        SpecialAttribute.INCREASE_DAMAGE_TAKEN
                                    ].multipliers,
                                    tag,
                                )
