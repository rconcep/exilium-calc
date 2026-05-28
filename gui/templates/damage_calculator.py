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
from core.types import UnitLevel
from core.combat import DamageInstance, CombatSummary, TargetCombatState
from core.buffs import Buff, Debuff, buffs_option_config, debuffs_option_config
from gui.templates.doll_calculator_page import DollCalculatorPage
from gui.templates.single_configurable_item_editor import SingleConfigurableItemEditor
from gui.templates.selectable_chips_editor import SelectableChipsEditor
import gui.templates.increment_sweep_analysis as sweep_analysis
import gui.templates.scenario_comparison_analysis as scenario_analysis
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
        self.relevant_damage_tags: list[DamageTag] = [
            tag for tag in DamageTag if tag not in self.doll.irrelevant_damage_tags
        ]

        self.buffs_selector: SelectableChipsEditor
        self.debuffs_selector: SelectableChipsEditor

        self.initialize_target()

        self.target_phase_weaknesses_exploited: ui.select
        self.target_stability_broken: ui.switch
        self.target_unit_level: ui.select
        self.target_phase_tile_level: ui.select

        # self.bar_chart_plot: ui.plotly
        self.combat_summary: CombatSummary = CombatSummary()
        self.last_action_type: str | None = None
        self.last_action_kwargs: dict[str, Any] = {}

        self.delta_chart: dict[str, Any] = {
            "data": [],
            "layout": {
                "title": {"text": "Change in Expected Damage by Stat Increment"},
                "margin": {"l": 50, "r": 20, "t": 50, "b": 50},
                "paper_bgcolor": "rgba(0,0,0,0)",
                "plot_bgcolor": "rgba(10,24,30,0.9)",
                "font": {"color": "#eef4ef", "family": "Inter, sans-serif"},
                "title_font": {"family": "Josefin Sans, sans-serif", "size": 18},
                "colorway": ["#d5a34f", "#65bbc4", "#8fd6d0", "#dfc27d", "#7fa8ad"],
                "xaxis": {
                    "title": {"text": "Stat increment"},
                    "gridcolor": "rgba(143,214,208,0.08)",
                    "linecolor": "rgba(143,214,208,0.24)",
                },
                "yaxis": {
                    "title": {"text": "Change in expected damage (%)"},
                    "gridcolor": "rgba(143,214,208,0.08)",
                    "linecolor": "rgba(143,214,208,0.24)",
                },
                "legend": {"orientation": "h", "y": -0.55, "x": 0, "xanchor": "left"},
            },
        }
        self.scenario_chart: dict[str, Any] = {
            "data": [],
            "layout": {
                "title": {"text": "Scenario Comparison (Single Increment)"},
                "margin": {"l": 250, "r": 20, "t": 50, "b": 65},
                "paper_bgcolor": "rgba(0,0,0,0)",
                "plot_bgcolor": "rgba(10,24,30,0.9)",
                "font": {"color": "#eef4ef", "family": "Inter, sans-serif"},
                "title_font": {"family": "Josefin Sans, sans-serif", "size": 18},
                "colorway": ["#d5a34f", "#65bbc4", "#8fd6d0", "#dfc27d", "#7fa8ad"],
                "xaxis": {
                    "title": {"text": "Change in expected damage (%)"},
                    "gridcolor": "rgba(143,214,208,0.08)",
                    "linecolor": "rgba(143,214,208,0.24)",
                },
                "yaxis": {
                    "gridcolor": "rgba(143,214,208,0.08)",
                    "linecolor": "rgba(143,214,208,0.24)",
                },
                "showlegend": False,
            },
        }

        self.delta_chart_plot: ui.plotly
        self.scenario_chart_plot: ui.plotly
        self.delta_increment_input: ui.number
        self.delta_steps_input: ui.number
        self.delta_stats_selector: ui.select
        self.delta_stat_source_selector: ui.select
        self.delta_special_attribute_selector: ui.select
        self.delta_special_attribute_tag_selector: ui.select
        self.delta_multi_initial_stats_selector: ui.select
        self.delta_multi_additive_stats_selector: ui.select
        self.delta_multi_additive_special_selector: ui.select
        self.delta_multi_additive_conditional_basic_stats_selector: ui.select
        self.delta_multi_multiplicative_stats_selector: ui.select
        self.delta_multi_multiplicative_conditional_basic_stats_selector: ui.select
        self.delta_basic_controls_container: ui.column
        self.delta_single_special_controls_container: ui.column
        self.delta_multi_controls_container: ui.column
        self.scenario_rows_container: ui.column
        self.delta_scenario_rows: list[dict[str, Any]] = []
        self.delta_scenario_next_index: int = 1

        self.delta_special_combo_options: dict[str, str] = {
            f"{attribute.value}::{tag.value}": f"{attribute.value} [{tag.value}]"
            for attribute in SpecialAttribute
            for tag in self.relevant_damage_tags
        }

        conditional_basic_stats_to_show: tuple[StatType, ...] = (
            StatType.ATTACK,
            StatType.CRIT_RATE,
        )
        self.delta_conditional_basic_combo_options: dict[str, str] = {
            f"{stat.value}::{tag.value}": f"{stat.value} [{tag.value}]"
            for stat in conditional_basic_stats_to_show
            for tag in self.relevant_damage_tags
        }

        self.results_labels: dict[str, ui.label] = {}

        with ui.row().classes("h-full w-full"):
            with ui.column().classes("w-full gap-6"):
                with ui.row().classes("w-full gap-6 items-start"):
                    with ui.card().classes("w-120 h-180 exilium-panel"):
                        self._attacker_section()
                    with ui.card().classes("w-80 h-180 exilium-panel"):
                        self._results_section()
                    with ui.card().classes("w-120 h-180 exilium-panel"):
                        self._target_section()

                with ui.card().classes("w-full exilium-panel"):
                    self._delta_section()

    def initialize_target(self):
        """Sets the target to initial values."""
        self.target.initial_stats.basic_attributes[StatType.DEFENSE] = 5000
        self.target.initial_stats.basic_attributes[StatType.HEALTH] = 11e6
        self.target.initial_stats.basic_attributes[
            StatType.STABILITY_DAMAGE_REDUCTION
        ] = 60

    def _build_target_combat_state(self) -> TargetCombatState:
        """Builds TargetCombatState from current target UI controls."""
        stability_broken: bool = self.target_stability_broken.value
        phase_weaknesses_exploited: int = self.target_phase_weaknesses_exploited.value  # type: ignore
        phase_tile_level: int = self.target_phase_tile_level.value  # type: ignore

        return TargetCombatState(
            is_stability_broken=stability_broken,
            phase_weaknesses_exploited=phase_weaknesses_exploited,
            unit_level=UnitLevel(self.target_unit_level.value),  # type: ignore
            is_on_phase_tile=phase_tile_level > 0,
            phase_tile_ascension_level=phase_tile_level,
        )

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

        self.last_action_type = data["type"]
        self.last_action_kwargs = keyword_args

        di: DamageInstance = combat_action(**keyword_args)
        target_combat_state: TargetCombatState = self._build_target_combat_state()

        self.combat_summary = di.damage_calculation_strategy.calculate_damage(
            copy.deepcopy(self.doll),
            copy.deepcopy(self.target),
            di,
            target_combat_state=target_combat_state,
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
                Decimal(self.combat_summary.critical_rate * 100).quantize(
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
            # + "%"
        )
        self.results_labels["total_increased_damage_pct"].text = (
            str(
                Decimal(self.combat_summary.total_increased_damage_pct).quantize(
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

        self._update_expected_damage_delta_chart()
        self._update_scenario_comparison_chart()

    def _update_expected_damage_delta_chart(self, _event: Any = None) -> None:
        """Updates expected damage deltas from basic stat increments."""
        return sweep_analysis.update_expected_damage_delta_chart(self, _event)

    def _default_scenario_tag(self) -> DamageTag:
        """Returns a stable default tag for scenario controls."""
        return scenario_analysis.default_scenario_tag(self)

    def _apply_scenario_component(
        self,
        doll: Doll,
        source: str,
        increment: float,
        stat: StatType,
        special_attribute: SpecialAttribute,
        tag: DamageTag,
    ) -> None:
        """Applies one increment component to a doll clone."""
        return scenario_analysis.apply_scenario_component(
            doll, source, increment, stat, special_attribute, tag
        )

    def _update_scenario_component_visibility(
        self, scenario_row: dict[str, Any], component_index: int
    ) -> None:
        """Shows only the relevant selectors for one scenario component."""
        return scenario_analysis.update_scenario_component_visibility(
            self, scenario_row, component_index
        )

    def _update_scenario_row_visibility(self, scenario_row: dict[str, Any]) -> None:
        """Shows only controls relevant to row mode and component source."""
        return scenario_analysis.update_scenario_row_visibility(self, scenario_row)

    def _remove_scenario_row(self, scenario_row: dict[str, Any]) -> None:
        """Removes the specified scenario row."""
        return scenario_analysis.remove_scenario_row(self, scenario_row)

    def _add_component_to_scenario_row(self, scenario_row: dict[str, Any]) -> None:
        """Adds one component to a combined row up to 3."""
        return scenario_analysis.add_component_to_scenario_row(self, scenario_row)

    def _remove_component_from_scenario_row(self, scenario_row: dict[str, Any]) -> None:
        """Removes one component from a combined row down to 1."""
        return scenario_analysis.remove_component_from_scenario_row(self, scenario_row)

    def _add_single_scenario_row(self, _event: Any = None) -> None:
        """Adds one single-component scenario row."""
        return scenario_analysis.add_single_scenario_row(self, _event)

    def _add_combined_scenario_row(self, _event: Any = None) -> None:
        """Adds one combined scenario row with three increment components."""
        return scenario_analysis.add_combined_scenario_row(self, _event)

    def _create_scenario_row(
        self,
        label: str,
        mode: str,
        component_1: dict[str, Any],
        component_2: dict[str, Any],
        component_3: dict[str, Any],
    ) -> None:
        """Creates one editable scenario row for the comparison chart."""
        return scenario_analysis.create_scenario_row(
            self,
            label,
            mode,
            component_1,
            component_2,
            component_3,
        )

    def _update_scenario_comparison_chart(self, _event: Any = None) -> None:
        """Updates one-point mixed-increment scenario comparison chart."""
        return scenario_analysis.update_scenario_comparison_chart(self, _event)

    def _on_delta_stat_source_changed(self, _event: Any = None) -> None:
        """Prefills common comparison traces when switching to multi-series."""
        return sweep_analysis.on_delta_stat_source_changed(self, _event)

    def _update_delta_control_visibility(self) -> None:
        """Shows only controls relevant to the currently selected increment source."""
        return sweep_analysis.update_delta_control_visibility(self)

    def _get_combat_summary_with_doll(self, doll: Doll) -> CombatSummary:
        """Runs the active action for doll and returns a combat summary."""
        if not self.last_action_type:
            return CombatSummary()

        doll.prepare_for_calculation()

        action_config: dict[str, Any] = self.doll_calculator.option_config[
            self.last_action_type
        ]
        combat_action: Callable = action_config["function"]
        damage_instance: DamageInstance = combat_action(**self.last_action_kwargs)
        target_combat_state: TargetCombatState = self._build_target_combat_state()

        return damage_instance.damage_calculation_strategy.calculate_damage(
            copy.deepcopy(doll),
            copy.deepcopy(self.target),
            damage_instance,
            target_combat_state=target_combat_state,
            buffs_before=self.get_all_buffs(),
            debuffs_before=self.get_all_debuffs(),
        )

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
        # self.bar_chart_plot = ui.plotly(self.bar_chart).classes("w-full h-80")

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
                    ui.item_label("Total Increased Damage")
                with ui.item_section().props("side"):
                    self.results_labels["total_increased_damage_pct"] = ui.label()

            with ui.item():
                with ui.item_section().props(""):
                    ui.item_label("Effective Potency")
                with ui.item_section().props("side"):
                    self.results_labels["effective_damage_multiplier"] = ui.label()

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
                    ui.item_label("Negative Defense")
                    ui.item_label("Defense ignore beyond 100%").props("caption")
                with ui.item_section().props("side"):
                    self.results_labels["negative_defense"] = ui.label()

    def _delta_section(self):
        """Generates the Expected Damage Delta section."""

        ### Incremental Scenario Comparison (top, open by default)
        with ui.expansion(
            "Scenario Comparison",
            caption="Expected damage change for specific stat change scenarios",
            value=True,
            icon="analytics",
            group="stat-increment-analysis",
        ).classes("w-full"):
            with ui.row().classes("w-full gap-2"):
                ui.button("Add Scenario", on_click=self._add_single_scenario_row)
                ui.button(
                    "Add Combined Scenario", on_click=self._add_combined_scenario_row
                )

            with ui.column().classes("w-full gap-2") as self.scenario_rows_container:
                pass

            default_tag: DamageTag = self._default_scenario_tag()
            self._create_scenario_row(
                label="Crit Dmg for Dmg Boost",
                mode="combined",
                component_1={
                    "source": "additive_special_attributes",
                    "increment": -0.8,
                    "stat": StatType.CRIT_DAMAGE,
                    "special_attribute": SpecialAttribute.CRITICAL_DAMAGE,
                    "tag": default_tag,
                },
                component_2={
                    "source": "additive_special_attributes",
                    "increment": 2,
                    "stat": StatType.HEALTH,
                    "special_attribute": SpecialAttribute.DAMAGE_BOOST,
                    "tag": default_tag,
                },
                component_3={
                    "source": "additive_special_attributes",
                    "increment": 0,
                    "stat": StatType.ATTACK,
                    "special_attribute": SpecialAttribute.DAMAGE_BOOST,
                    "tag": default_tag,
                },
            )
            self._create_scenario_row(
                label="+0.4 Crit Dmg",
                mode="combined",
                component_1={
                    "source": "additive_special_attributes",
                    "increment": 0.4,
                    "stat": StatType.CRIT_DAMAGE,
                    "special_attribute": SpecialAttribute.CRITICAL_DAMAGE,
                    "tag": default_tag,
                },
                component_2={
                    "source": "initial_stats",
                    "increment": 0,
                    "stat": StatType.ATTACK,
                    "special_attribute": SpecialAttribute.DAMAGE_BOOST,
                    "tag": default_tag,
                },
                component_3={
                    "source": "additive_special_attributes",
                    "increment": 0,
                    "stat": StatType.ATTACK,
                    "special_attribute": SpecialAttribute.DAMAGE_BOOST,
                    "tag": default_tag,
                },
            )
            self._create_scenario_row(
                label="+2 Additive Damage Boost [All]",
                mode="single",
                component_1={
                    "source": "additive_special_attributes",
                    "increment": 2,
                    "stat": StatType.ATTACK,
                    "special_attribute": SpecialAttribute.DAMAGE_BOOST,
                    "tag": default_tag,
                },
                component_2={
                    "source": "initial_stats",
                    "increment": 0,
                    "stat": StatType.HEALTH,
                    "special_attribute": SpecialAttribute.DAMAGE_BOOST,
                    "tag": default_tag,
                },
                component_3={
                    "source": "initial_stats",
                    "increment": 0,
                    "stat": StatType.ATTACK,
                    "special_attribute": SpecialAttribute.DAMAGE_BOOST,
                    "tag": default_tag,
                },
            )
            self.delta_scenario_next_index = 4

            self.scenario_chart_plot = ui.plotly(self.scenario_chart).classes(
                "w-full h-100 exilium-plot"
            )

        ### Sweep (below, closed by default)
        with ui.expansion(
            "Stat Increment Analysis",
            caption="Expected damage as a function of stats",
            value=False,
            icon="data_exploration",
            group="stat-increment-analysis",
        ).classes("w-full"):
            with ui.grid(columns=3).classes("w-full gap-2"):
                self.delta_increment_input = ui.number(
                    value=0.4,
                    min=0,
                    precision=2,
                    label="Increment per step",
                ).on("update:model-value", self._update_expected_damage_delta_chart)
                self.delta_steps_input = ui.number(
                    value=10,
                    min=1,
                    precision=0,
                    label="Number of steps",
                ).on("update:model-value", self._update_expected_damage_delta_chart)
                self.delta_stat_source_selector = (
                    ui.select(
                        options={
                            "initial_stats": "Initial Stats",
                            "additive_modifiers": "Additive Modifiers (Basic)",
                            "additive_special_attributes": "Additive Modifiers (Special)",
                            "multi_series": "Custom Multi-Series",
                        },
                        value="multi_series",
                        label="Increment source",
                    )
                    .classes("w-full")
                    .on("update:model-value", self._on_delta_stat_source_changed)
                )

            with ui.column().classes("w-full") as self.delta_basic_controls_container:
                self.delta_stats_selector = (
                    ui.select(
                        options=[stat for stat in StatType],
                        value=[
                            StatType.ATTACK,
                            StatType.CRIT_RATE,
                            StatType.CRIT_DAMAGE,
                        ],
                        multiple=True,
                        with_input=False,
                        label="Stats to vary",
                    )
                    .classes("w-full")
                    .on("update:model-value", self._update_expected_damage_delta_chart)
                )

            with ui.column().classes(
                "w-full"
            ) as self.delta_single_special_controls_container:
                with ui.grid(columns=2).classes("w-full gap-2"):
                    self.delta_special_attribute_selector = (
                        ui.select(
                            options=[attribute for attribute in SpecialAttribute],
                            value=SpecialAttribute.DAMAGE_BOOST,
                            label="Special attribute",
                        )
                        .classes("w-full")
                        .on(
                            "update:model-value",
                            self._update_expected_damage_delta_chart,
                        )
                    )
                    self.delta_special_attribute_tag_selector = (
                        ui.select(
                            options=self.relevant_damage_tags,
                            value=(
                                DamageTag.ALL
                                if DamageTag.ALL in self.relevant_damage_tags
                                else self.relevant_damage_tags[0]
                            ),
                            label="Special attribute tag",
                        )
                        .classes("w-full")
                        .on(
                            "update:model-value",
                            self._update_expected_damage_delta_chart,
                        )
                    )

            with ui.column().classes("w-full") as self.delta_multi_controls_container:
                with ui.grid(columns=2).classes("w-full gap-2"):
                    self.delta_multi_initial_stats_selector = (
                        ui.select(
                            options=[stat for stat in StatType],
                            value=[],
                            multiple=True,
                            with_input=False,
                            label="Initial stats (multi-series)",
                        )
                        .props(
                            "use-chips options-selected-class=exilium-multiselect-selected"
                        )
                        .classes("w-full")
                        .on(
                            "update:model-value",
                            self._update_expected_damage_delta_chart,
                        )
                    )
                    self.delta_multi_additive_stats_selector = (
                        ui.select(
                            options=[stat for stat in StatType],
                            value=[],
                            multiple=True,
                            with_input=False,
                            label="Additive modifiers (basic) (multi-series)",
                        )
                        .props(
                            "use-chips options-selected-class=exilium-multiselect-selected"
                        )
                        .classes("w-full")
                        .on(
                            "update:model-value",
                            self._update_expected_damage_delta_chart,
                        )
                    )

                self.delta_multi_additive_special_selector = (
                    ui.select(
                        options=self.delta_special_combo_options,
                        value=[
                            f"{SpecialAttribute.DAMAGE_BOOST.value}::{DamageTag.ALL.value}",
                            f"{SpecialAttribute.CRITICAL_DAMAGE.value}::{DamageTag.ALL.value}",
                            f"{SpecialAttribute.DEFENSE_IGNORE.value}::{DamageTag.ALL.value}",
                        ],
                        multiple=True,
                        with_input=True,
                        label="Additive modifiers (special) (multi-series)",
                    )
                    .props(
                        "use-chips options-selected-class=exilium-multiselect-selected"
                    )
                    .classes("w-full")
                    .on("update:model-value", self._update_expected_damage_delta_chart)
                )

                self.delta_multi_additive_conditional_basic_stats_selector = (
                    ui.select(
                        options=self.delta_conditional_basic_combo_options,
                        value=[],
                        multiple=True,
                        with_input=False,
                        label="Additive modifiers (basic conditional) (multi-series)",
                    )
                    .props(
                        "use-chips options-selected-class=exilium-multiselect-selected"
                    )
                    .classes("w-full")
                    .on(
                        "update:model-value",
                        self._update_expected_damage_delta_chart,
                    )
                )

                self.delta_multi_multiplicative_stats_selector = (
                    ui.select(
                        options=[stat for stat in StatType],
                        value=[],
                        multiple=True,
                        with_input=False,
                        label="Multiplicative modifiers (basic) (multi-series)",
                    )
                    .props(
                        "use-chips options-selected-class=exilium-multiselect-selected"
                    )
                    .classes("w-full")
                    .on(
                        "update:model-value",
                        self._update_expected_damage_delta_chart,
                    )
                )

                self.delta_multi_multiplicative_conditional_basic_stats_selector = (
                    ui.select(
                        options=self.delta_conditional_basic_combo_options,
                        value=[],
                        multiple=True,
                        with_input=False,
                        label="Multiplicative modifiers (basic conditional) (multi-series)",
                    )
                    .props(
                        "use-chips options-selected-class=exilium-multiselect-selected"
                    )
                    .classes("w-full")
                    .on(
                        "update:model-value",
                        self._update_expected_damage_delta_chart,
                    )
                )

            self.delta_chart_plot = ui.plotly(self.delta_chart).classes(
                "w-full h-100 exilium-plot"
            )

        self._update_delta_control_visibility()

    def _target_section(self):
        """Generates the elements in the Target section."""
        ui.label("Target").props("header")
        ui.separator()
        with ui.grid(columns="65% auto").classes("w-full"):
            self.target_phase_weaknesses_exploited = ui.select(
                options=[0, 1, 2], value=2, label="Phase Weaknesses Exploited"
            )
            self.target_stability_broken = ui.switch("Stability Broken", value=True)

        with ui.grid(columns=2).classes("w-full"):
            self.target_unit_level = ui.select(
                options=[level.value for level in UnitLevel],
                value=UnitLevel.BOSS.value,
                label="Level",
            )
            self.target_phase_tile_level = ui.select(
                options=[0, 1, 2, 3], value=0, label="Phase Tile Level"
            )

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
                    for tag in self.relevant_damage_tags:
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
