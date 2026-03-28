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
from core.combat import DamageInstance, CombatSummary
from core.buffs import Buff, Debuff, buffs_option_config, debuffs_option_config
from gui.templates.doll_calculator_page import DollCalculatorPage
from gui.templates.single_configurable_item_editor import SingleConfigurableItemEditor
from gui.templates.selectable_chips_editor import SelectableChipsEditor
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

        # self.bar_chart_plot: ui.plotly
        self.combat_summary: CombatSummary = CombatSummary()
        self.last_action_type: str | None = None
        self.last_action_kwargs: dict[str, Any] = {}

        self.delta_chart: dict[str, Any] = {
            "data": [],
            "layout": {
                "title": {"text": "Change in Expected Damage by Stat Increment"},
                "margin": {"l": 50, "r": 20, "t": 50, "b": 50},
                "plot_bgcolor": "#E5ECF6",
                "xaxis": {"title": {"text": "Stat increment"}, "gridcolor": "white"},
                "yaxis": {
                    "title": {"text": "Change in expected damage (%)"},
                    "gridcolor": "white",
                },
                "legend": {"orientation": "h", "y": -0.25},
            },
        }

        self.delta_chart_plot: ui.plotly
        self.delta_increment_input: ui.number
        self.delta_steps_input: ui.number
        self.delta_stats_selector: ui.select
        self.delta_stat_source_selector: ui.select
        self.delta_special_attribute_selector: ui.select
        self.delta_special_attribute_tag_selector: ui.select
        self.delta_multi_initial_stats_selector: ui.select
        self.delta_multi_additive_stats_selector: ui.select
        self.delta_multi_additive_special_selector: ui.select
        self.delta_basic_controls_container: ui.column
        self.delta_single_special_controls_container: ui.column
        self.delta_multi_controls_container: ui.column

        self.delta_special_combo_options: dict[str, str] = {
            f"{attribute.value}::{tag.value}": f"{attribute.value} [{tag.value}]"
            for attribute in SpecialAttribute
            for tag in self.relevant_damage_tags
        }

        self.results_labels: dict[str, ui.label] = {}

        with ui.row().classes("h-full"):
            with ui.column().classes("w-full"):
                with ui.row().classes("w-full"):
                    with ui.card().classes("w-115 h-180"):
                        self._attacker_section()
                    with ui.card().classes("w-80 h-180"):
                        self._results_section()
                    with ui.card().classes("w-115 h-180"):
                        self._target_section()

                with ui.card().classes("w-full"):
                    self._delta_section()

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

        self.last_action_type = data["type"]
        self.last_action_kwargs = keyword_args

        di: DamageInstance = combat_action(**keyword_args)

        stability_broken: bool = self.target_stability_broken.value
        phase_weaknesses_exploited: int = self.target_phase_weaknesses_exploited.value  # type: ignore

        self.combat_summary = di.damage_calculation_strategy.calculate_damage(
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

        self._update_expected_damage_delta_chart()

    def _update_expected_damage_delta_chart(self, _event: Any = None) -> None:
        """Updates expected damage deltas from basic stat increments."""
        if not self.last_action_type:
            self.delta_chart["data"] = []
            ui.update(self.delta_chart_plot)
            return

        increment: float = float(self.delta_increment_input.value or 0)
        steps: int = int(self.delta_steps_input.value or 0)
        x_values: list[float] = [increment * i for i in range(steps + 1)]
        stat_source: str = self.delta_stat_source_selector.value or "initial_stats"

        selected_multi_initial_stats: list[StatType] = (
            self.delta_multi_initial_stats_selector.value or []  # type: ignore
        )
        selected_multi_additive_stats: list[StatType] = (
            self.delta_multi_additive_stats_selector.value or []  # type: ignore
        )
        selected_multi_additive_special: list[str] = (
            self.delta_multi_additive_special_selector.value or []  # type: ignore
        )

        selected_stats: list[StatType] = self.delta_stats_selector.value or []  # type: ignore
        selected_special_attribute: SpecialAttribute | None = (
            self.delta_special_attribute_selector.value
        )
        selected_special_attribute_tag: DamageTag | None = (
            self.delta_special_attribute_tag_selector.value
        )

        if stat_source != "additive_special_attributes" and not selected_stats:
            self.delta_chart["data"] = []
            ui.update(self.delta_chart_plot)
            return

        if stat_source == "additive_special_attributes" and (
            selected_special_attribute is None or selected_special_attribute_tag is None
        ):
            self.delta_chart["data"] = []
            ui.update(self.delta_chart_plot)
            return

        base_expected_damage: float = self.combat_summary.expected_damage
        if base_expected_damage <= 0:
            self.delta_chart["data"] = []
            ui.update(self.delta_chart_plot)
            return

        traces: list[dict[str, Any]] = []

        if stat_source == "multi_series":
            if (
                not selected_multi_initial_stats
                and not selected_multi_additive_stats
                and not selected_multi_additive_special
            ):
                self.delta_chart["data"] = []
                ui.update(self.delta_chart_plot)
                return

            for stat in selected_multi_initial_stats:
                deltas: list[float] = []
                for stat_increment in x_values:
                    doll: Doll = copy.deepcopy(self.doll)
                    doll.initial_stats.basic_attributes[stat] += stat_increment
                    summary: CombatSummary = self._get_combat_summary_with_doll(doll)
                    deltas.append(
                        (summary.expected_damage - base_expected_damage)
                        / base_expected_damage
                        * 100
                    )

                traces.append(
                    {
                        "type": "scatter",
                        "mode": "lines+markers",
                        "name": f"{stat} (Initial)",
                        "x": x_values,
                        "y": deltas,
                        "hovertemplate": "%{x}: %{y:.2f}%<extra>%{fullData.name}</extra>",
                    }
                )

            for stat in selected_multi_additive_stats:
                deltas = []
                for stat_increment in x_values:
                    doll = copy.deepcopy(self.doll)
                    doll.additive_modifiers.basic_attributes[stat] += stat_increment
                    summary = self._get_combat_summary_with_doll(doll)
                    deltas.append(
                        (summary.expected_damage - base_expected_damage)
                        / base_expected_damage
                        * 100
                    )

                traces.append(
                    {
                        "type": "scatter",
                        "mode": "lines+markers",
                        "name": f"{stat} (Additive)",
                        "x": x_values,
                        "y": deltas,
                        "hovertemplate": "%{x}: %{y:.2f}%<extra>%{fullData.name}</extra>",
                    }
                )

            for special_combo in selected_multi_additive_special:
                special_attribute_value, tag_value = special_combo.split(
                    "::", maxsplit=1
                )
                selected_attribute: SpecialAttribute = SpecialAttribute(
                    special_attribute_value
                )
                selected_tag: DamageTag = DamageTag(tag_value)

                deltas = []
                for stat_increment in x_values:
                    doll = copy.deepcopy(self.doll)
                    doll.additive_modifiers.special_attributes[
                        selected_attribute
                    ].add_to_multiplier(selected_tag, stat_increment)

                    summary = self._get_combat_summary_with_doll(doll)
                    deltas.append(
                        (summary.expected_damage - base_expected_damage)
                        / base_expected_damage
                        * 100
                    )

                traces.append(
                    {
                        "type": "scatter",
                        "mode": "lines+markers",
                        "name": f"{selected_attribute} [{selected_tag}] (Additive)",
                        "x": x_values,
                        "y": deltas,
                        "hovertemplate": "%{x}: %{y:.2f}%<extra>%{fullData.name}</extra>",
                    }
                )
        elif stat_source == "additive_special_attributes":
            selected_special_attribute_typed: SpecialAttribute = (
                selected_special_attribute  # type: ignore
            )
            selected_special_attribute_tag_typed: DamageTag = (
                selected_special_attribute_tag  # type: ignore
            )
            deltas: list[float] = []

            for stat_increment in x_values:
                doll: Doll = copy.deepcopy(self.doll)
                doll.additive_modifiers.special_attributes[
                    selected_special_attribute_typed
                ].add_to_multiplier(
                    selected_special_attribute_tag_typed, stat_increment
                )

                summary: CombatSummary = self._get_combat_summary_with_doll(doll)
                deltas.append(
                    (summary.expected_damage - base_expected_damage)
                    / base_expected_damage
                    * 100
                )

            traces.append(
                {
                    "type": "scatter",
                    "mode": "lines+markers",
                    "name": f"{selected_special_attribute_typed} [{selected_special_attribute_tag_typed}] (Additive)",
                    "x": x_values,
                    "y": deltas,
                    "hovertemplate": "%{x}: %{y:.2f}%<extra>%{fullData.name}</extra>",
                }
            )
        else:
            for stat in selected_stats:
                deltas: list[float] = []

                for stat_increment in x_values:
                    doll: Doll = copy.deepcopy(self.doll)
                    if stat_source == "additive_modifiers":
                        doll.additive_modifiers.basic_attributes[stat] += stat_increment
                    else:
                        doll.initial_stats.basic_attributes[stat] += stat_increment

                    summary: CombatSummary = self._get_combat_summary_with_doll(doll)
                    deltas.append(
                        (summary.expected_damage - base_expected_damage)
                        / base_expected_damage
                        * 100
                    )

                traces.append(
                    {
                        "type": "scatter",
                        "mode": "lines+markers",
                        "name": f"{stat} ({'Additive' if stat_source == 'additive_modifiers' else 'Initial'})",
                        "x": x_values,
                        "y": deltas,
                        "hovertemplate": "%{x}: %{y:.2f}%<extra>%{fullData.name}</extra>",
                    }
                )

        self.delta_chart["data"] = traces
        ui.update(self.delta_chart_plot)

    def _on_delta_stat_source_changed(self, _event: Any = None) -> None:
        """Prefills common comparison traces when switching to multi-series."""
        stat_source: str = self.delta_stat_source_selector.value or "initial_stats"
        if stat_source == "multi_series":
            self.delta_multi_initial_stats_selector.value = []
            self.delta_multi_additive_stats_selector.value = []

            default_special_series: list[str] = []
            for attribute, tag in [
                (SpecialAttribute.DAMAGE_BOOST, DamageTag.ALL),
                (SpecialAttribute.CRITICAL_DAMAGE, DamageTag.ALL),
                (SpecialAttribute.DEFENSE_IGNORE, DamageTag.ALL),
            ]:
                key: str = f"{attribute.value}::{tag.value}"
                if key in self.delta_special_combo_options:
                    default_special_series.append(key)

            self.delta_multi_additive_special_selector.value = default_special_series

            if not default_special_series and self.delta_special_combo_options:
                first_special_combo: str = next(iter(self.delta_special_combo_options))
                self.delta_multi_additive_special_selector.value = [first_special_combo]

        self._update_delta_control_visibility()
        self._update_expected_damage_delta_chart()

    def _update_delta_control_visibility(self) -> None:
        """Shows only controls relevant to the currently selected increment source."""
        stat_source: str = self.delta_stat_source_selector.value or "initial_stats"

        show_basic_stats: bool = stat_source in ["initial_stats", "additive_modifiers"]
        show_single_special: bool = stat_source == "additive_special_attributes"
        show_multi: bool = stat_source == "multi_series"

        self.delta_basic_controls_container.set_visibility(show_basic_stats)
        self.delta_single_special_controls_container.set_visibility(show_single_special)
        self.delta_multi_controls_container.set_visibility(show_multi)

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

        stability_broken: bool = self.target_stability_broken.value
        phase_weaknesses_exploited: int = self.target_phase_weaknesses_exploited.value  # type: ignore

        return damage_instance.damage_calculation_strategy.calculate_damage(
            copy.deepcopy(doll),
            copy.deepcopy(self.target),
            damage_instance,
            is_stability_broken=stability_broken,
            phase_weaknesses_exploited=phase_weaknesses_exploited,
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

    def _delta_section(self):
        """Generates the Expected Damage Delta section."""
        ui.label("Stat Increment Analysis").props("header")
        ui.separator()

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
                    value="initial_stats",
                    label="Increment source",
                )
                .classes("w-full")
                .on("update:model-value", self._on_delta_stat_source_changed)
            )

        with ui.column().classes("w-full") as self.delta_basic_controls_container:
            self.delta_stats_selector = (
                ui.select(
                    options=[stat for stat in StatType],
                    value=[StatType.ATTACK, StatType.CRIT_RATE, StatType.CRIT_DAMAGE],
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
                    .on("update:model-value", self._update_expected_damage_delta_chart)
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
                    .on("update:model-value", self._update_expected_damage_delta_chart)
                )

        with ui.column().classes("w-full") as self.delta_multi_controls_container:
            with ui.grid(columns=2).classes("w-full gap-2"):
                self.delta_multi_initial_stats_selector = (
                    ui.select(
                        options=[stat for stat in StatType],
                        value=[StatType.ATTACK],
                        multiple=True,
                        with_input=False,
                        label="Initial stats (multi-series)",
                    )
                    .classes("w-full")
                    .on("update:model-value", self._update_expected_damage_delta_chart)
                )
                self.delta_multi_additive_stats_selector = (
                    ui.select(
                        options=[stat for stat in StatType],
                        value=[],
                        multiple=True,
                        with_input=False,
                        label="Additive modifiers (basic) (multi-series)",
                    )
                    .classes("w-full")
                    .on("update:model-value", self._update_expected_damage_delta_chart)
                )

            self.delta_multi_additive_special_selector = (
                ui.select(
                    options=self.delta_special_combo_options,
                    value=[],
                    multiple=True,
                    with_input=True,
                    label="Additive modifiers (special) (multi-series)",
                )
                .classes("w-full")
                .on("update:model-value", self._update_expected_damage_delta_chart)
            )

        self.delta_chart_plot = ui.plotly(self.delta_chart).classes("w-full h-90")
        self._update_delta_control_visibility()

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
