from __future__ import annotations

from decimal import Decimal, ROUND_DOWN
from typing import Any, Callable
import copy
import hashlib
import inspect
import json
from uuid import uuid4

from nicegui import events, ui

from core.buffs import Buff, Debuff, buffs_option_config, debuffs_option_config
from core.combat import (
    CombatSummary,
    DamageInstance,
    TargetCombatState,
    get_reportable_damage_tags,
)
from core.rotation_data_serializer import (
    RotationDataError,
    build_payload_from_planner_defaults,
    normalize_payload,
    payload_to_string,
    string_to_payload,
)
from core.types import DamageTag, Doll, SpecialAttribute, StatType, Unit, UnitLevel
from gui.styles.descriptions import get_stat_description
from gui.styles.graphs import get_bar_chart_template, get_donut_chart_template
from gui.templates.rotation_planner import RotationPlanner
from gui.templates.selectable_chips_editor import SelectableChipsEditor
import gui.templates.increment_sweep_analysis as sweep_analysis
import gui.templates.scenario_comparison_analysis as scenario_analysis


def get_relevant_target_stats() -> list[StatType]:
    """Returns the subset of StatType that is relevant to damage calculations."""
    return [StatType.HEALTH, StatType.DEFENSE, StatType.STABILITY_DAMAGE_REDUCTION]


class RotationSimulator:
    """Hybrid tool that combines Rotation Planner sequencing with Damage Calculator math."""

    tag_blacklist: list[DamageTag] = [
        DamageTag.ALL,
        DamageTag.EXPOSED,
        DamageTag.STABILITY_BROKEN,
        DamageTag.BOSS,
        DamageTag.HAS_MOVEMENT_DEBUFF,
        DamageTag.ONLY_HIT_ONE_TARGET,
        DamageTag.NEAR,
        DamageTag.FAR,
        DamageTag.ON_PHASE_TILE,
    ]

    def __init__(self, doll_calculator):
        self.doll_calculator = doll_calculator
        self.doll: Doll = self.doll_calculator.doll
        self.option_config: dict[str, dict[str, Any]] = (
            self.doll_calculator.option_config
        )
        self.relevant_damage_tags: list[DamageTag] = [
            tag for tag in DamageTag if tag not in self.doll.irrelevant_damage_tags
        ]

        self.target: Unit = Unit()
        self._initialize_target()

        self.combat_summary: CombatSummary = CombatSummary()
        self.last_action_type: str | None = "rotation"
        self.last_action_kwargs: dict[str, Any] = {}

        self.baseline_buffs_selector: SelectableChipsEditor
        self.baseline_debuffs_selector: SelectableChipsEditor
        self.baseline_phase_weaknesses: ui.select
        self.baseline_stability_broken: ui.switch
        self.baseline_unit_level: ui.select
        self.baseline_phase_tile_level: ui.select

        self.timeline_rows_container: ui.column
        self.timeline_rows: list[dict[str, Any]] = []

        self.total_expected_damage_label: ui.label
        self.simulation_status_label: ui.label
        self.simulation_spinner: ui.spinner
        self.simulate_button: ui.button
        self.timeline_result_table: ui.table
        self.tag_breakdown_table: ui.table

        self.delta_chart: dict[str, Any] = get_bar_chart_template()
        self.scenario_chart: dict[str, Any] = get_bar_chart_template()
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

        self.ability_donut_chart: dict[str, Any] = get_donut_chart_template()
        self.ability_donut_chart_plot: ui.plotly

        self._build_ui()

    def refresh_doll_state_from_calculator(self) -> None:
        """Refresh Doll-dependent references after calculator state changes."""
        self.doll = self.doll_calculator.doll
        self.option_config = self.doll_calculator.option_config
        self.relevant_damage_tags = [
            tag for tag in DamageTag if tag not in self.doll.irrelevant_damage_tags
        ]

        # Keep simulator planner actions in sync with updated ability configs.
        if hasattr(self, "rotation_planner") and self.rotation_planner is not None:
            self.rotation_planner.set_options_config(self.option_config)

    def _initialize_target(self) -> None:
        self.target.initial_stats.basic_attributes[StatType.DEFENSE] = 5000
        self.target.initial_stats.basic_attributes[StatType.HEALTH] = 11e6
        self.target.initial_stats.basic_attributes[
            StatType.STABILITY_DAMAGE_REDUCTION
        ] = 60

    def _build_ui(self) -> None:
        with ui.column().classes("w-full gap-4"):
            with ui.expansion(
                "Rotation + Baseline Setup",
                caption="Edit rotation actions and baseline combat state.",
                value=True,
                icon="tune",
            ).classes("w-full"):
                with ui.row().classes("w-full gap-4 items-start"):
                    with ui.card().classes("w-80 h-180 exilium-panel"):
                        ui.label("Rotation Actions").classes("text-h6")
                        ui.label(
                            "Build your sequence by turn, then click Sync Timeline. This will re-build the action timeline and erase any per-action modifications."
                        ).classes("text-caption exilium-subtle")
                        ui.separator()
                        self.rotation_planner = RotationPlanner(
                            options_config=self.option_config
                        )
                        with ui.row().classes("w-full justify-end"):
                            ui.button(
                                "Sync Timeline",
                                on_click=self.sync_timeline,
                                icon="timeline",
                            ).props("color=primary unelevated")

                    with ui.card().classes("w-230 h-180 exilium-panel"):
                        self._baseline_state_section()

            with ui.expansion(
                "Edit Action Timeline",
                caption="Per-action attacker/target modifications. Buff/debuff additions and removals are resolved in chronological order.",
                value=False,
                icon="timeline",
            ).classes("w-full"):
                with ui.card().classes("w-full exilium-panel"):
                    with ui.column().classes(
                        "w-full gap-3"
                    ) as self.timeline_rows_container:
                        ui.label(
                            "No timeline yet. Click Sync Timeline after defining actions."
                        ).classes("text-caption")

            with ui.row().classes("w-full gap-4 items-start"):
                with ui.card().classes("w-120 exilium-panel"):
                    self._summary_section()

                with ui.card().classes("w-120 exilium-panel"):
                    self._rotation_data_section()

            with ui.row().classes("w-full gap-4 items-start"):
                with ui.card().classes("w-160 exilium-panel"):
                    ui.label("Simulation Results").classes("text-h6")
                    ui.separator()
                    self.timeline_result_table = ui.table(
                        columns=[
                            {
                                "name": "turn",
                                "label": "Turn",
                                "field": "turn",
                                "align": "left",
                            },
                            {
                                "name": "action",
                                "label": "Action",
                                "field": "action",
                                "align": "left",
                            },
                            {
                                "name": "expected_damage",
                                "label": "Expected Damage",
                                "field": "expected_damage",
                                "align": "right",
                            },
                            {
                                "name": "critical_rate",
                                "label": "Crit Rate",
                                "field": "critical_rate",
                                "align": "right",
                            },
                        ],
                        rows=[],
                        row_key="index",
                        pagination={"rowsPerPage": 10},
                    ).classes("w-full exilium-data-table")

                with ui.card().classes("w-150 exilium-panel"):
                    ui.label("Damage Type Breakdown").classes("text-h6")
                    ui.separator()
                    self.tag_breakdown_table = ui.table(
                        columns=[
                            {
                                "name": "tag",
                                "label": "Damage Type",
                                "field": "tag",
                                "align": "left",
                            },
                            {
                                "name": "share",
                                "label": "%",
                                "field": "share",
                                "align": "right",
                            },
                            {
                                "name": "expected_damage",
                                "label": "Expected Damage",
                                "field": "expected_damage",
                                "align": "right",
                            },
                        ],
                        rows=[],
                        row_key="tag",
                        pagination={
                            "rowsPerPage": 8,
                            "sortBy": "share",
                            "descending": True,
                        },
                    ).classes("w-full exilium-data-table")
                    # ui.separator()
                    # ui.label("Damage by Action Group").classes("text-subtitle1")
                    self.ability_donut_chart_plot = ui.plotly(
                        self.ability_donut_chart
                    ).classes("w-full h-80 exilium-plot")

            self._delta_section()

    def _baseline_state_section(self) -> None:
        ui.label("Baseline Combat State").classes("text-h6")
        ui.label("Default Attacker and Target state used for each action.").classes(
            "text-caption exilium-subtle"
        )
        ui.separator()

        with ui.grid(columns=2).classes("w-full gap-3 items-start"):
            with ui.card().classes("w-full exilium-panel"):
                ui.label("Attacker").classes("text-subtitle2")
                ui.separator()
                self.baseline_buffs_selector = SelectableChipsEditor(
                    options=list(buffs_option_config.keys()),
                    option_config=buffs_option_config,
                    title="Buffs",
                    allow_duplicates=True,
                    button_text="Add Buff",
                    clear_button_text="Clear Buffs",
                )

            with ui.card().classes("w-full exilium-panel"):
                ui.label("Target").classes("text-subtitle2")
                ui.separator()
                with ui.grid(columns="70% auto").classes("w-full"):
                    self.baseline_phase_weaknesses = ui.select(
                        options=[0, 1, 2],
                        value=2,
                        label="Phase Weaknesses Exploited",
                    )
                    self.baseline_stability_broken = ui.switch(
                        "Stability Broken", value=True
                    )

                with ui.grid(columns=2).classes("w-full"):
                    self.baseline_unit_level = ui.select(
                        options=[level.value for level in UnitLevel],
                        value=UnitLevel.BOSS.value,
                        label="Level",
                    )
                    self.baseline_phase_tile_level = ui.select(
                        options=[0, 1, 2, 3],
                        value=0,
                        label="Phase Tile Level",
                    )

                with ui.expansion("Target Stats", value=False).classes("w-full"):
                    with ui.list().props("bordered dense separator").classes("w-full"):
                        for stat in get_relevant_target_stats():
                            with ui.item():
                                with ui.item_section().props("no-wrap"):
                                    ui.item_label(stat)
                                    ui.item_label(get_stat_description(stat)).props(
                                        "caption"
                                    )
                                with ui.item_section().props("side"):
                                    ui.number(value=0, min=0, precision=2).bind_value(
                                        self.target.initial_stats.basic_attributes,
                                        stat,
                                    )

                self.baseline_debuffs_selector = SelectableChipsEditor(
                    options=list(debuffs_option_config.keys()),
                    option_config=debuffs_option_config,
                    title="Debuffs",
                    allow_duplicates=True,
                    button_text="Add Debuff",
                    clear_button_text="Clear Debuffs",
                )

    def _summary_section(self) -> None:
        ui.label("Run Simulation").classes("text-h6")
        ui.separator()
        ui.label("You can edit any action and simulate again.").classes(
            "text-caption exilium-subtle"
        )

        with ui.list().props("bordered dense").classes("w-full"):
            with ui.item():
                with ui.item_section().props("no-wrap"):
                    ui.item_label("Total Expected Damage")
                with ui.item_section().props("side"):
                    self.total_expected_damage_label = ui.label("0")

        with ui.row().classes("w-full items-center gap-2 text-caption exilium-subtle"):
            self.simulation_spinner = ui.spinner(size="sm")
            self.simulation_spinner.set_visibility(False)
            self.simulation_status_label = ui.label("")

        with ui.row().classes("w-full justify-end"):
            self.simulate_button = ui.button(
                "Simulate",
                on_click=self.simulate,
                icon="play_arrow",
            ).props("color=primary unelevated")

    def _rotation_data_section(self) -> None:
        ui.label("Load/Save Rotation").classes("text-h6")
        ui.separator()

        ui.label("Export").classes("text-subtitle2 font-bold")
        ui.label("Download current baseline and timeline as JSON.").classes(
            "text-sm text-gray-500"
        )

        with ui.row().classes("gap-2"):

            def _do_export() -> None:
                ui.download.content(
                    self.export_rotation_json(),
                    self.export_rotation_filename(),
                    media_type="application/json",
                )

            ui.button("Download JSON", on_click=_do_export, icon="download").props(
                "color=primary unelevated"
            )

        ui.separator()
        ui.label("Import").classes("text-subtitle2 font-bold")
        ui.label("Upload a saved .json file to restore baseline and timeline.").classes(
            "text-sm text-gray-500"
        )

        def _apply_import(json_string: str) -> None:
            try:
                payload = string_to_payload(
                    json_string,
                    option_config=self.option_config,
                    expected_doll_name=self.doll.name,
                )
                self.apply_rotation_payload(payload)
            except RotationDataError as exc:
                ui.notify(f"Invalid rotation JSON: {exc}", type="negative")
                return
            ui.notify(f"Imported rotation for '{self.doll.name}'", type="positive")

        async def _on_upload(e: events.UploadEventArguments) -> None:
            async def _maybe_await(value):
                if inspect.isawaitable(value):
                    return await value
                return value

            async def _read_text(source) -> str | None:
                if source is None:
                    return None

                if hasattr(source, "seek"):
                    try:
                        await _maybe_await(source.seek(0))
                    except Exception:
                        ...

                if hasattr(source, "text"):
                    try:
                        text_val = await _maybe_await(source.text(encoding="utf-8"))
                        if isinstance(text_val, str):
                            return text_val
                    except TypeError:
                        try:
                            text_val = await _maybe_await(source.text())
                            if isinstance(text_val, str):
                                return text_val
                        except Exception:
                            ...
                    except Exception:
                        ...

                if hasattr(source, "read"):
                    raw = await _maybe_await(source.read())
                    if isinstance(raw, (bytes, bytearray, memoryview)):
                        return bytes(raw).decode("utf-8")
                    if isinstance(raw, str):
                        return raw

                if hasattr(source, "getvalue"):
                    raw = await _maybe_await(source.getvalue())
                    if isinstance(raw, (bytes, bytearray, memoryview)):
                        return bytes(raw).decode("utf-8")
                    if isinstance(raw, str):
                        return raw

                return None

            try:
                payload = None

                content_obj = getattr(e, "content", None)
                file_obj = getattr(e, "file", None)

                if content_obj is not None:
                    payload = await _read_text(content_obj)

                if payload is None and file_obj is not None:
                    payload = await _read_text(file_obj)

                nested_file_obj = getattr(file_obj, "file", None)
                if payload is None and nested_file_obj is not None:
                    payload = await _read_text(nested_file_obj)

            except UnicodeDecodeError:
                ui.notify("File must be UTF-8 encoded JSON", type="negative")
                return

            if payload is None:
                ui.notify("Could not read uploaded file", type="negative")
                return

            payload = payload.lstrip("\ufeff") if payload else payload
            if not payload or not payload.strip():
                ui.notify("Uploaded file is empty", type="negative")
                return

            if payload.lstrip()[:1] not in {"{", "["}:
                ui.notify("Upload did not contain JSON text", type="negative")
                return

            _apply_import(payload)

        ui.upload(
            label="Upload .json configuration",
            on_upload=_on_upload,
            auto_upload=True,
        ).props("accept=.json outlined")

    def export_rotation_filename(self) -> str:
        safe_name = "".join(
            character.lower() if character.isalnum() else "_"
            for character in self.doll.name.strip()
        ).strip("_")
        return f"{safe_name or 'doll'}_rotation.json"

    def export_rotation_json(self) -> str:
        payload = self._build_rotation_payload()
        return payload_to_string(payload)

    def _get_row_effect_data(
        self, row: dict[str, Any], selector_key: str
    ) -> list[dict[str, Any]]:
        if selector_key in row:
            return copy.deepcopy(row[selector_key].data)
        data_key = selector_key.replace("_selector", "_data")
        return copy.deepcopy(row.get(data_key, []))

    def _set_row_effect_data(
        self, row: dict[str, Any], selector_key: str, data: list[dict[str, Any]]
    ) -> None:
        if selector_key in row:
            row[selector_key].set_data(copy.deepcopy(data), notify=False)
            return
        data_key = selector_key.replace("_selector", "_data")
        row[data_key] = copy.deepcopy(data)

    def _get_row_override_value(self, row: dict[str, Any], override_key: str) -> str:
        if override_key in row:
            return str(row[override_key].value)
        value_key = f"{override_key}_value"
        return str(row.get(value_key, "Baseline"))

    def _set_row_override_value(
        self, row: dict[str, Any], override_key: str, value: str
    ) -> None:
        if override_key in row:
            row[override_key].value = str(value)
            return
        value_key = f"{override_key}_value"
        row[value_key] = str(value)

    def _build_rotation_payload(self) -> dict[str, Any]:
        planner_turns = self.rotation_planner.get_data()
        payload = build_payload_from_planner_defaults(
            doll_name=self.doll.name,
            planner_turns=planner_turns,
            baseline_buffs=copy.deepcopy(self.baseline_buffs_selector.data),
            baseline_debuffs=copy.deepcopy(self.baseline_debuffs_selector.data),
        )

        timeline_actions: list[dict[str, Any]] = []
        for row in self.timeline_rows:
            timeline_actions.append(
                {
                    "turn": row["turn"],
                    "action": copy.deepcopy(row["chip_data"]),
                    "attacker": {
                        "add_buffs": self._get_row_effect_data(
                            row, "add_buffs_selector"
                        ),
                        "remove_buffs": self._get_row_effect_data(
                            row, "remove_buffs_selector"
                        ),
                    },
                    "target": {
                        "add_debuffs": self._get_row_effect_data(
                            row, "add_debuffs_selector"
                        ),
                        "remove_debuffs": self._get_row_effect_data(
                            row, "remove_debuffs_selector"
                        ),
                        "phase_weaknesses_override": self._get_row_override_value(
                            row, "phase_weaknesses_override"
                        ),
                        "stability_override": self._get_row_override_value(
                            row, "stability_override"
                        ),
                        "unit_level_override": self._get_row_override_value(
                            row, "unit_level_override"
                        ),
                        "phase_tile_override": self._get_row_override_value(
                            row, "phase_tile_override"
                        ),
                    },
                }
            )

        payload["baseline"]["target"]["phase_weaknesses_exploited"] = int(
            self.baseline_phase_weaknesses.value or 0
        )
        payload["baseline"]["target"]["stability_broken"] = bool(
            self.baseline_stability_broken.value
        )
        payload["baseline"]["target"]["unit_level"] = str(
            self.baseline_unit_level.value
        )
        payload["baseline"]["target"]["phase_tile_level"] = int(
            self.baseline_phase_tile_level.value or 0
        )
        payload["baseline"]["target"]["basic_attributes"] = {
            stat.value: float(self.target.initial_stats.basic_attributes[stat])
            for stat in get_relevant_target_stats()
        }
        payload["timeline"]["actions"] = timeline_actions

        return normalize_payload(
            payload,
            option_config=self.option_config,
            expected_doll_name=self.doll.name,
        )

    def apply_rotation_payload(self, payload: dict[str, Any]) -> None:
        normalized_payload = normalize_payload(
            payload,
            option_config=self.option_config,
            expected_doll_name=self.doll.name,
        )

        baseline = normalized_payload["baseline"]
        baseline_attacker = baseline["attacker"]
        baseline_target = baseline["target"]

        self.baseline_buffs_selector.set_data(copy.deepcopy(baseline_attacker["buffs"]))
        self.baseline_debuffs_selector.set_data(
            copy.deepcopy(baseline_target["debuffs"])
        )

        self.baseline_phase_weaknesses.value = int(
            baseline_target["phase_weaknesses_exploited"]
        )
        self.baseline_stability_broken.value = bool(baseline_target["stability_broken"])
        self.baseline_unit_level.value = str(baseline_target["unit_level"])
        self.baseline_phase_tile_level.value = int(baseline_target["phase_tile_level"])

        basic_attributes = baseline_target["basic_attributes"]
        for stat in get_relevant_target_stats():
            self.target.initial_stats.basic_attributes[stat] = float(
                basic_attributes[stat.value]
            )

        turns_raw = normalized_payload["planner"]["turns"]
        planner_turns: dict[int, list[dict[str, Any]]] = {
            int(turn): copy.deepcopy(actions) for turn, actions in turns_raw.items()
        }
        self.rotation_planner.set_data(planner_turns)
        self.sync_timeline()

        timeline_actions = normalized_payload["timeline"]["actions"]
        if len(timeline_actions) != len(self.timeline_rows):
            raise RotationDataError(
                "Timeline row count does not match planner actions after sync"
            )

        for index, (timeline_action, row) in enumerate(
            zip(timeline_actions, self.timeline_rows),
            start=1,
        ):
            imported_action = timeline_action["action"]
            current_action = {
                "name": row["chip_data"]["name"],
            }
            for field in self.option_config[current_action["name"]]["fields"]:
                key = field["key"]
                current_action[key] = row["chip_data"][key]

            if imported_action != current_action:
                raise RotationDataError(
                    f"Timeline action mismatch at position {index}; sync planner state before importing"
                )

            self._set_row_effect_data(
                row,
                "add_buffs_selector",
                copy.deepcopy(timeline_action["attacker"]["add_buffs"]),
            )
            self._set_row_effect_data(
                row,
                "remove_buffs_selector",
                copy.deepcopy(timeline_action["attacker"]["remove_buffs"]),
            )
            self._set_row_effect_data(
                row,
                "add_debuffs_selector",
                copy.deepcopy(timeline_action["target"]["add_debuffs"]),
            )
            self._set_row_effect_data(
                row,
                "remove_debuffs_selector",
                copy.deepcopy(timeline_action["target"]["remove_debuffs"]),
            )

            self._set_row_override_value(
                row,
                "phase_weaknesses_override",
                str(timeline_action["target"]["phase_weaknesses_override"]),
            )
            self._set_row_override_value(
                row,
                "stability_override",
                str(timeline_action["target"]["stability_override"]),
            )
            self._set_row_override_value(
                row,
                "unit_level_override",
                str(timeline_action["target"]["unit_level_override"]),
            )
            self._set_row_override_value(
                row,
                "phase_tile_override",
                str(timeline_action["target"]["phase_tile_override"]),
            )

        self._refresh_all_removal_selectors()

    def _set_simulation_busy(self, busy: bool) -> None:
        self.simulation_spinner.set_visibility(busy)
        self.simulation_status_label.text = "Processing simulation..." if busy else ""
        if busy:
            self.simulate_button.disable()
        else:
            self.simulate_button.enable()

    def _delta_section(self) -> None:
        """Generates the sensitivity analysis section for the full rotation result."""
        self.delta_chart["layout"].update(
            {
                "title": {"text": "Change in Expected Damage by Stat Increment"},
                "margin": {"l": 50, "r": 20, "t": 50, "b": 50},
                "colorway": [
                    "#d5a34f",
                    "#65bbc4",
                    "#8fd6d0",
                    "#dfc27d",
                    "#7fa8ad",
                ],
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
                "legend": {
                    "orientation": "h",
                    "y": -0.55,
                    "x": 0,
                    "xanchor": "left",
                },
            }
        )
        self.scenario_chart["layout"].update(
            {
                "title": {"text": "Scenario Comparison (Single Increment)"},
                "margin": {"l": 250, "r": 20, "t": 50, "b": 65},
                "colorway": [
                    "#d5a34f",
                    "#65bbc4",
                    "#8fd6d0",
                    "#dfc27d",
                    "#7fa8ad",
                ],
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
            }
        )

        with ui.expansion(
            "Scenario Comparison",
            caption="Expected damage change for rotation-wide stat scenarios.",
            value=False,
            icon="analytics",
            group="rotation-sensitivity-analysis",
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

        with ui.expansion(
            "Stat Increment Analysis",
            caption="Expected damage as a function of rotation-wide stat changes.",
            value=False,
            icon="data_exploration",
            group="rotation-sensitivity-analysis",
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
                            value=self._default_scenario_tag(),
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
                    .on("update:model-value", self._update_expected_damage_delta_chart)
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
                    .on("update:model-value", self._update_expected_damage_delta_chart)
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
                    .on("update:model-value", self._update_expected_damage_delta_chart)
                )

            self.delta_chart_plot = ui.plotly(self.delta_chart).classes(
                "w-full h-100 exilium-plot"
            )

        self._update_delta_control_visibility()

    def _default_scenario_tag(self) -> DamageTag:
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
        scenario_analysis.apply_scenario_component(
            doll=doll,
            source=source,
            increment=increment,
            stat=stat,
            special_attribute=special_attribute,
            tag=tag,
        )

    def _update_scenario_component_visibility(
        self, scenario_row: dict[str, Any], component_index: int
    ) -> None:
        scenario_analysis.update_scenario_component_visibility(
            self, scenario_row, component_index
        )

    def _update_scenario_row_visibility(self, scenario_row: dict[str, Any]) -> None:
        scenario_analysis.update_scenario_row_visibility(self, scenario_row)

    def _remove_scenario_row(self, scenario_row: dict[str, Any]) -> None:
        scenario_analysis.remove_scenario_row(self, scenario_row)

    def _add_component_to_scenario_row(self, scenario_row: dict[str, Any]) -> None:
        scenario_analysis.add_component_to_scenario_row(self, scenario_row)

    def _remove_component_from_scenario_row(self, scenario_row: dict[str, Any]) -> None:
        scenario_analysis.remove_component_from_scenario_row(self, scenario_row)

    def _add_single_scenario_row(self, _event: Any = None) -> None:
        scenario_analysis.add_single_scenario_row(self, _event)

    def _add_combined_scenario_row(self, _event: Any = None) -> None:
        scenario_analysis.add_combined_scenario_row(self, _event)

    def _create_scenario_row(
        self,
        label: str,
        mode: str,
        component_1: dict[str, Any],
        component_2: dict[str, Any],
        component_3: dict[str, Any],
    ) -> None:
        scenario_analysis.create_scenario_row(
            self,
            label,
            mode,
            component_1,
            component_2,
            component_3,
        )

    def _update_scenario_comparison_chart(self, _event: Any = None) -> None:
        scenario_analysis.update_scenario_comparison_chart(self, _event)

    def _update_expected_damage_delta_chart(self, _event: Any = None) -> None:
        sweep_analysis.update_expected_damage_delta_chart(self, _event)

    def _on_delta_stat_source_changed(self, _event: Any = None) -> None:
        sweep_analysis.on_delta_stat_source_changed(self, _event)

    def _update_delta_control_visibility(self) -> None:
        sweep_analysis.update_delta_control_visibility(self)

    def _get_combat_summary_with_doll(self, doll: Doll) -> CombatSummary:
        summary: CombatSummary = CombatSummary()
        summary.expected_damage = self._calculate_rotation_expected_damage_with_doll(
            doll
        )
        return summary

    def _calculate_rotation_expected_damage_with_doll(self, doll: Doll) -> float:
        if not self.timeline_rows:
            return 0

        total_expected_damage: float = 0
        active_buffs_data: list[dict[str, Any]] = copy.deepcopy(
            self.baseline_buffs_selector.data
        )
        active_debuffs_data: list[dict[str, Any]] = copy.deepcopy(
            self.baseline_debuffs_selector.data
        )

        for row in self.timeline_rows:
            self._remove_matching_items(
                active_items=active_buffs_data,
                to_remove=self._get_row_effect_data(row, "remove_buffs_selector"),
            )
            self._remove_matching_items(
                active_items=active_debuffs_data,
                to_remove=self._get_row_effect_data(row, "remove_debuffs_selector"),
            )

            active_buffs_data.extend(
                self._get_row_effect_data(row, "add_buffs_selector")
            )
            active_debuffs_data.extend(
                self._get_row_effect_data(row, "add_debuffs_selector")
            )

            buffs_before: list[Buff] = self._create_buff_instances(active_buffs_data)
            debuffs_before: list[Debuff] = self._create_debuff_instances(
                active_debuffs_data
            )

            chip_data: dict[str, Any] = row["chip_data"]
            action_config: dict[str, Any] = self.option_config[chip_data["name"]]
            action_function: Callable = action_config["function"]

            keyword_args: dict[str, Any] = {}
            for field in action_config["fields"]:
                keyword_args[field["key"]] = chip_data[field["key"]]

            damage_instance: DamageInstance = action_function(**keyword_args)
            target_state: TargetCombatState = self._build_target_state(row)

            attacker: Doll = copy.deepcopy(doll)
            attacker.prepare_for_calculation()

            target: Unit = copy.deepcopy(self.target)

            combat_summary: CombatSummary = (
                damage_instance.damage_calculation_strategy.calculate_damage(
                    attacker,
                    target,
                    damage_instance,
                    target_combat_state=target_state,
                    buffs_before=buffs_before,
                    debuffs_before=debuffs_before,
                )
            )
            total_expected_damage += combat_summary.expected_damage

        return total_expected_damage

    def _build_target_state(self, timeline_row: dict[str, Any]) -> TargetCombatState:
        weaknesses_override: str = self._get_row_override_value(
            timeline_row, "phase_weaknesses_override"
        )
        stability_override: str = self._get_row_override_value(
            timeline_row, "stability_override"
        )
        unit_level_override: str = self._get_row_override_value(
            timeline_row, "unit_level_override"
        )
        phase_tile_override: str = self._get_row_override_value(
            timeline_row, "phase_tile_override"
        )

        if weaknesses_override == "Baseline":
            phase_weaknesses_exploited = self.baseline_phase_weaknesses.value
        else:
            phase_weaknesses_exploited = int(weaknesses_override)
        phase_weaknesses_exploited = int(phase_weaknesses_exploited or 0)

        if stability_override == "Baseline":
            is_stability_broken = bool(self.baseline_stability_broken.value)
        else:
            is_stability_broken = stability_override == "broken"

        if unit_level_override == "Baseline":
            unit_level = UnitLevel(self.baseline_unit_level.value)
        else:
            unit_level = UnitLevel(unit_level_override)

        if phase_tile_override == "Baseline":
            phase_tile_level = int(self.baseline_phase_tile_level.value or 0)
        else:
            phase_tile_level = int(phase_tile_override)

        return TargetCombatState(
            is_stability_broken=is_stability_broken,
            phase_weaknesses_exploited=phase_weaknesses_exploited,
            unit_level=unit_level,
            is_on_phase_tile=phase_tile_level > 0,
            phase_tile_ascension_level=phase_tile_level,
        )

    def _summarize_action_kwargs(self, chip_data: dict[str, Any]) -> str:
        field_labels: list[str] = []

        for field in self.option_config[chip_data["name"]]["fields"]:
            key: str = field["key"]
            label: str = field.get("label", key)
            field_labels.append(f"{label}: {chip_data[key]}")

        return " | ".join(field_labels)

    def _get_timeline_expansion_caption(self, chip_data: dict[str, Any]) -> str:
        """Returns a compact header summary for one timeline action."""
        summary_text = self._summarize_action_kwargs(chip_data)
        return summary_text if summary_text else "No action parameters"

    def _effect_signature(self, item: dict[str, Any]) -> tuple[tuple[str, str], ...]:
        """Returns a stable signature of user-configured fields for one chip item."""
        return tuple(
            sorted(
                (key, repr(value))
                for key, value in item.items()
                if not key.startswith("_")
            )
        )

    def _format_effect_instance_label(
        self,
        item: dict[str, Any],
        occurrence_index: int,
    ) -> str:
        label: str = item["name"]
        field_parts: list[str] = []

        option_config = (
            buffs_option_config
            if item.get("_effect_kind") == "buff"
            else debuffs_option_config
        )
        option_details = option_config.get(item["name"], {})
        for field in option_details.get("fields", []):
            key: str = field["key"]
            value = item.get(key)
            if value in (None, "", False):
                continue
            field_parts.append(f"{field.get('label', key)}: {value}")

        if field_parts:
            label = f"{label} ({', '.join(field_parts)})"

        return f"{label} [#{occurrence_index}]"

    def _build_effect_reference_key(
        self,
        item: dict[str, Any],
        effect_kind: str,
        occurrence_index: int,
    ) -> str:
        """Builds a deterministic key for one removable effect instance.

        The key is based on effect kind, stable item payload (excluding metadata),
        and occurrence index among identical signatures before a timeline row.
        """
        payload = {
            key: value
            for key, value in item.items()
            if not str(key).startswith("_")
        }
        signature_text = json.dumps(payload, sort_keys=True, default=str)
        digest = hashlib.sha1(signature_text.encode("utf-8")).hexdigest()[:12]
        return f"{effect_kind}:{payload.get('name', '')}:{occurrence_index}:{digest}"

    def _ensure_effect_item_metadata(
        self, item: dict[str, Any], effect_kind: str
    ) -> dict[str, Any]:
        option_config = (
            buffs_option_config if effect_kind == "buff" else debuffs_option_config
        )
        config = option_config.get(item.get("name"), {})
        item.setdefault("_instance_id", str(uuid4()))
        item["_effect_kind"] = effect_kind
        if "target_instance_id" in config:
            item.setdefault("_target_instance_id", config["target_instance_id"])
        return item

    def _clone_effect_item(
        self, item: dict[str, Any], effect_kind: str
    ) -> dict[str, Any]:
        cloned_item: dict[str, Any] = copy.deepcopy(item)
        return self._ensure_effect_item_metadata(cloned_item, effect_kind)

    def _get_available_effect_instances_before_row(
        self,
        row_index: int,
        effect_kind: str,
    ) -> list[dict[str, Any]]:
        active_items: list[dict[str, Any]] = []

        baseline_items = (
            self.baseline_buffs_selector.data
            if effect_kind == "buff"
            else self.baseline_debuffs_selector.data
        )
        active_items.extend(
            [self._clone_effect_item(item, effect_kind) for item in baseline_items]
        )

        for row in self.timeline_rows:
            if row["index"] >= row_index:
                break

            remove_selector_key = (
                "remove_buffs_selector"
                if effect_kind == "buff"
                else "remove_debuffs_selector"
            )
            add_selector_key = (
                "add_buffs_selector"
                if effect_kind == "buff"
                else "add_debuffs_selector"
            )

            self._remove_matching_items(
                active_items=active_items,
                to_remove=[
                    self._clone_effect_item(item, effect_kind)
                    for item in row[remove_selector_key].data
                ],
            )
            active_items.extend(
                [
                    self._clone_effect_item(item, effect_kind)
                    for item in row[add_selector_key].data
                ]
            )

        return active_items

    def _build_removal_selector_config(
        self,
        row_index: int,
        effect_kind: str,
    ) -> tuple[dict[str, str], dict[str, dict[str, Any]]]:
        available_items: list[dict[str, Any]] = (
            self._get_available_effect_instances_before_row(
                row_index=row_index,
                effect_kind=effect_kind,
            )
        )

        options: dict[str, str] = {}
        option_config: dict[str, dict[str, Any]] = {}
        signature_counts: dict[tuple[tuple[str, str], ...], int] = {}

        for item in available_items:
            item = self._ensure_effect_item_metadata(item, effect_kind)
            signature = self._effect_signature(item)
            signature_counts.setdefault(signature, 0)
            signature_counts[signature] += 1

            instance_id: str = item["_instance_id"]
            occurrence_index: int = signature_counts[signature]
            reference_key: str = self._build_effect_reference_key(
                item=item,
                effect_kind=effect_kind,
                occurrence_index=occurrence_index,
            )
            display_name: str = self._format_effect_instance_label(
                item=item,
                occurrence_index=occurrence_index,
            )

            options[reference_key] = display_name
            option_config[reference_key] = {
                "fields": [],
                "display_name": display_name,
                "target_instance_id": instance_id,
            }

        return options, option_config

    def _refresh_row_removal_selector(
        self, row: dict[str, Any], effect_kind: str
    ) -> None:
        options, option_config = self._build_removal_selector_config(
            row_index=row["index"],
            effect_kind=effect_kind,
        )

        selector_key = (
            "remove_buffs_selector"
            if effect_kind == "buff"
            else "remove_debuffs_selector"
        )
        selector: SelectableChipsEditor = row[selector_key]
        prior_data: list[dict[str, Any]] = copy.deepcopy(selector.data)
        filtered_data: list[dict[str, Any]] = [
            item for item in prior_data if item["name"] in option_config
        ]

        selector.set_options_and_config(options=options, option_config=option_config)
        selector.set_data(filtered_data, notify=False)

    def _refresh_row_removal_selector_with_available(
        self,
        row: dict[str, Any],
        effect_kind: str,
        available_items: list[dict[str, Any]],
    ) -> None:
        options: dict[str, str] = {}
        option_config: dict[str, dict[str, Any]] = {}
        signature_counts: dict[tuple[tuple[str, str], ...], int] = {}

        for item in available_items:
            item = self._ensure_effect_item_metadata(item, effect_kind)
            signature = self._effect_signature(item)
            signature_counts.setdefault(signature, 0)
            signature_counts[signature] += 1

            instance_id: str = item["_instance_id"]
            occurrence_index: int = signature_counts[signature]
            reference_key: str = self._build_effect_reference_key(
                item=item,
                effect_kind=effect_kind,
                occurrence_index=occurrence_index,
            )
            display_name: str = self._format_effect_instance_label(
                item=item,
                occurrence_index=occurrence_index,
            )

            options[reference_key] = display_name
            option_config[reference_key] = {
                "fields": [],
                "display_name": display_name,
                "target_instance_id": instance_id,
            }

        selector_key = (
            "remove_buffs_selector"
            if effect_kind == "buff"
            else "remove_debuffs_selector"
        )
        selector: SelectableChipsEditor = row[selector_key]
        prior_data: list[dict[str, Any]] = copy.deepcopy(selector.data)
        filtered_data: list[dict[str, Any]] = [
            item for item in prior_data if item["name"] in option_config
        ]

        selector.set_options_and_config(options=options, option_config=option_config)
        selector.set_data(filtered_data, notify=False)

    def _apply_row_effect_changes_to_active_items(
        self,
        active_items: list[dict[str, Any]],
        row: dict[str, Any],
        effect_kind: str,
    ) -> None:
        remove_selector_key = (
            "remove_buffs_selector"
            if effect_kind == "buff"
            else "remove_debuffs_selector"
        )
        add_selector_key = (
            "add_buffs_selector" if effect_kind == "buff" else "add_debuffs_selector"
        )

        self._remove_matching_items(
            active_items=active_items,
            to_remove=[
                self._clone_effect_item(item, effect_kind)
                for item in self._get_row_effect_data(row, remove_selector_key)
            ],
        )
        active_items.extend(
            [
                self._clone_effect_item(item, effect_kind)
                for item in self._get_row_effect_data(row, add_selector_key)
            ]
        )

    def _refresh_all_removal_selectors(self) -> None:
        if not self.timeline_rows:
            return

        for effect_kind in ("buff", "debuff"):
            baseline_items = (
                self.baseline_buffs_selector.data
                if effect_kind == "buff"
                else self.baseline_debuffs_selector.data
            )
            active_items: list[dict[str, Any]] = [
                self._clone_effect_item(item, effect_kind) for item in baseline_items
            ]

            for row in self.timeline_rows:
                # Refresh using incremental active state rather than rescanning prior rows.
                if row.get("details_initialized", False):
                    self._refresh_row_removal_selector_with_available(
                        row=row,
                        effect_kind=effect_kind,
                        available_items=active_items,
                    )
                self._apply_row_effect_changes_to_active_items(
                    active_items=active_items,
                    row=row,
                    effect_kind=effect_kind,
                )

    def _is_expansion_opened_event(self, event: events.GenericEventArguments) -> bool:
        args = getattr(event, "args", None)
        if isinstance(args, bool):
            return args
        if isinstance(args, dict) and "value" in args:
            return bool(args["value"])
        if isinstance(args, (list, tuple)) and args:
            return bool(args[0])
        # Fallback: initialize on first event if payload shape is unexpected.
        return True

    def _ensure_timeline_row_details_initialized(self, row: dict[str, Any]) -> None:
        if row.get("details_initialized", False):
            return

        details_container: ui.column = row["details_container"]
        details_container.clear()

        with details_container:
            with ui.grid(columns=2).classes("w-full gap-3 items-start"):
                with ui.card().classes("w-full exilium-panel"):
                    ui.label("Attacker").classes("text-subtitle2")
                    ui.separator()
                    with ui.grid(columns=2).classes("w-full gap-2"):
                        row["add_buffs_selector"] = SelectableChipsEditor(
                            options=list(buffs_option_config.keys()),
                            option_config=buffs_option_config,
                            title="Add buffs",
                            allow_duplicates=True,
                            button_text="Add",
                            clear_button_text="Clear",
                            chip_color="positive",
                            on_change=self._refresh_all_removal_selectors,
                        )
                        row["remove_buffs_selector"] = SelectableChipsEditor(
                            options={},
                            option_config={},
                            title="Remove buffs",
                            allow_duplicates=True,
                            button_text="Remove",
                            clear_button_text="Clear",
                            chip_color="negative",
                            on_change=self._refresh_all_removal_selectors,
                        )

                with ui.card().classes("w-full exilium-panel"):
                    ui.label("Target").classes("text-subtitle2")
                    ui.separator()
                    with ui.grid(columns=2).classes("w-full gap-2"):
                        row["add_debuffs_selector"] = SelectableChipsEditor(
                            options=list(debuffs_option_config.keys()),
                            option_config=debuffs_option_config,
                            title="Add debuffs",
                            allow_duplicates=True,
                            button_text="Add",
                            clear_button_text="Clear",
                            chip_color="positive",
                            on_change=self._refresh_all_removal_selectors,
                        )
                        row["remove_debuffs_selector"] = SelectableChipsEditor(
                            options={},
                            option_config={},
                            title="Remove debuffs",
                            allow_duplicates=True,
                            button_text="Remove",
                            clear_button_text="Clear",
                            chip_color="negative",
                            on_change=self._refresh_all_removal_selectors,
                        )

                    with ui.grid(columns=2).classes("w-full gap-2"):
                        row["phase_weaknesses_override"] = ui.select(
                            options={
                                "Baseline": "Baseline",
                                "0": "0",
                                "1": "1",
                                "2": "2",
                            },
                            value=self._get_row_override_value(
                                row, "phase_weaknesses_override"
                            ),
                            label="Phase Weaknesses Exploited",
                        )
                        row["stability_override"] = ui.select(
                            options={
                                "Baseline": "Baseline",
                                "broken": "Stability Broken",
                                "intact": "Stability Intact",
                            },
                            value=self._get_row_override_value(
                                row, "stability_override"
                            ),
                            label="Stability",
                        )
                        row["unit_level_override"] = ui.select(
                            options={
                                "Baseline": "Baseline",
                                UnitLevel.BOSS.value: UnitLevel.BOSS.value,
                                UnitLevel.ELITE.value: UnitLevel.ELITE.value,
                                UnitLevel.NORMAL.value: UnitLevel.NORMAL.value,
                            },
                            value=self._get_row_override_value(
                                row, "unit_level_override"
                            ),
                            label="Target Level",
                        )
                        row["phase_tile_override"] = ui.select(
                            options={
                                "Baseline": "Baseline",
                                "0": "Off",
                                "1": "I",
                                "2": "II",
                                "3": "III",
                            },
                            value=self._get_row_override_value(
                                row, "phase_tile_override"
                            ),
                            label="Phase Tile",
                        )

        # Seed controls from stored row state for rows that were not previously initialized.
        self._set_row_effect_data(
            row, "add_buffs_selector", row.get("add_buffs_data", [])
        )
        self._set_row_effect_data(
            row, "remove_buffs_selector", row.get("remove_buffs_data", [])
        )
        self._set_row_effect_data(
            row, "add_debuffs_selector", row.get("add_debuffs_data", [])
        )
        self._set_row_effect_data(
            row, "remove_debuffs_selector", row.get("remove_debuffs_data", [])
        )

        row["details_initialized"] = True
        self._refresh_all_removal_selectors()

    def _on_timeline_row_expansion_changed(
        self, row: dict[str, Any], event: events.GenericEventArguments
    ) -> None:
        if not self._is_expansion_opened_event(event):
            return
        self._ensure_timeline_row_details_initialized(row)

    def _create_buff_instances(self, buff_data: list[dict[str, Any]]) -> list[Buff]:
        buffs: list[Buff] = []

        for buff in buff_data:
            keyword_args: dict[str, Any] = {}
            constructor: Callable = buffs_option_config[buff["name"]]["function"]

            for field in buffs_option_config[buff["name"]]["fields"]:
                keyword_args[field["key"]] = buff[field["key"]]

            buff_instance: Buff | list[Buff] = constructor(**keyword_args)
            if isinstance(buff_instance, Buff):
                buffs.append(buff_instance)
            elif isinstance(buff_instance, list):
                buffs.extend(buff_instance)

        return buffs

    def _create_debuff_instances(
        self, debuff_data: list[dict[str, Any]]
    ) -> list[Debuff]:
        debuffs: list[Debuff] = []

        for debuff in debuff_data:
            keyword_args: dict[str, Any] = {}
            constructor: Callable = debuffs_option_config[debuff["name"]]["function"]

            for field in debuffs_option_config[debuff["name"]]["fields"]:
                keyword_args[field["key"]] = debuff[field["key"]]

            debuff_instance: Debuff | list[Debuff] = constructor(**keyword_args)
            if isinstance(debuff_instance, Debuff):
                debuffs.append(debuff_instance)
            elif isinstance(debuff_instance, list):
                debuffs.extend(debuff_instance)

        return debuffs

    def _remove_matching_items(
        self,
        active_items: list[dict[str, Any]],
        to_remove: list[dict[str, Any]],
    ) -> None:
        for remove_item in to_remove:
            target_instance_id = remove_item.get(
                "_target_instance_id", remove_item.get("_instance_id")
            )
            for idx, active_item in enumerate(active_items):
                if active_item.get("_instance_id") == target_instance_id:
                    active_items.pop(idx)
                    break

    def sync_timeline(self, _event: Any = None) -> None:
        """Build timeline rows from the current Rotation Planner actions."""
        self.timeline_rows.clear()
        self.timeline_rows_container.clear()

        flat_actions: list[tuple[int, dict[str, Any]]] = []
        for turn in range(1, 1 + RotationPlanner.NUMBER_OF_TURNS):
            editor = self.rotation_planner.editors.get(turn)
            if not editor:
                continue
            for chip in editor.data:
                flat_actions.append((turn, copy.deepcopy(chip)))

        if not flat_actions:
            with self.timeline_rows_container:
                ui.label("No actions selected in Rotation Actions.").classes(
                    "text-caption"
                )
            ui.notify("No actions to sync", type="warning")
            return

        with self.timeline_rows_container:
            for index, (turn, chip_data) in enumerate(flat_actions, start=1):
                row: dict[str, Any] = {
                    "index": index,
                    "turn": turn,
                    "chip_data": chip_data,
                    "add_buffs_data": [],
                    "remove_buffs_data": [],
                    "add_debuffs_data": [],
                    "remove_debuffs_data": [],
                    "phase_weaknesses_override_value": "Baseline",
                    "stability_override_value": "Baseline",
                    "unit_level_override_value": "Baseline",
                    "phase_tile_override_value": "Baseline",
                    "details_initialized": False,
                }

                with ui.expansion(
                    text=f"T{turn} - {chip_data['name']}",
                    caption=self._get_timeline_expansion_caption(chip_data),
                    value=index == 1,
                    group="rotation-simulator-timeline",
                    icon="tune",
                ) as expansion:
                    expansion.classes("w-full exilium-panel")
                    row["details_container"] = ui.column().classes("w-full")
                    with row["details_container"]:
                        ui.label(
                            "Expand this row to load action detail controls."
                        ).classes("text-caption exilium-subtle")
                    expansion.on(
                        "update:model-value",
                        lambda event, row=row: self._on_timeline_row_expansion_changed(
                            row=row,
                            event=event,
                        ),
                    )

                self.timeline_rows.append(row)

                if index == 1:
                    self._ensure_timeline_row_details_initialized(row)

            self._refresh_all_removal_selectors()

        ui.notify(f"Synced {len(self.timeline_rows)} action(s)", type="positive")

    def simulate(self, _event: Any = None) -> None:
        """Runs combat calculations for each timeline row and aggregates results."""
        if not self.timeline_rows:
            ui.notify("Sync timeline first", type="warning")
            return

        self._set_simulation_busy(True)
        ui.timer(
            0.05,
            self._start_simulation,
            once=True,
            immediate=False,
        )

    def _start_simulation(self) -> None:
        self.simulate_button.client.safe_invoke(self._run_simulation)

    async def _run_simulation(self) -> None:
        try:
            total_expected_damage: float = 0
            grouped_expected_damage: dict[str, float] = {}
            tag_expected_damage: dict[DamageTag, float] = {}
            action_rows: list[dict[str, Any]] = []

            active_buffs_data: list[dict[str, Any]] = copy.deepcopy(
                self.baseline_buffs_selector.data
            )
            active_debuffs_data: list[dict[str, Any]] = copy.deepcopy(
                self.baseline_debuffs_selector.data
            )

            for row in self.timeline_rows:
                self._remove_matching_items(
                    active_items=active_buffs_data,
                    to_remove=self._get_row_effect_data(row, "remove_buffs_selector"),
                )
                self._remove_matching_items(
                    active_items=active_debuffs_data,
                    to_remove=self._get_row_effect_data(row, "remove_debuffs_selector"),
                )
                active_buffs_data.extend(
                    self._get_row_effect_data(row, "add_buffs_selector")
                )
                active_debuffs_data.extend(
                    self._get_row_effect_data(row, "add_debuffs_selector")
                )

                buffs_before: list[Buff] = self._create_buff_instances(
                    active_buffs_data
                )
                debuffs_before: list[Debuff] = self._create_debuff_instances(
                    active_debuffs_data
                )

                chip_data: dict[str, Any] = row["chip_data"]
                action_config: dict[str, Any] = self.option_config[chip_data["name"]]
                action_function: Callable = action_config["function"]

                keyword_args: dict[str, Any] = {}
                for field in action_config["fields"]:
                    keyword_args[field["key"]] = chip_data[field["key"]]

                damage_instance: DamageInstance = action_function(**keyword_args)
                target_state: TargetCombatState = self._build_target_state(row)

                attacker: Doll = copy.deepcopy(self.doll)
                attacker.prepare_for_calculation()

                target: Unit = copy.deepcopy(self.target)

                combat_summary: CombatSummary = (
                    damage_instance.damage_calculation_strategy.calculate_damage(
                        attacker,
                        target,
                        damage_instance,
                        target_combat_state=target_state,
                        buffs_before=buffs_before,
                        debuffs_before=debuffs_before,
                    )
                )

                expected_damage: float = combat_summary.expected_damage
                total_expected_damage += expected_damage

                grouped_expected_damage.setdefault(
                    damage_instance.group_name or damage_instance.label,
                    0,
                )
                grouped_expected_damage[
                    damage_instance.group_name or damage_instance.label
                ] += expected_damage

                for tag in get_reportable_damage_tags(damage_instance):
                    if tag in self.tag_blacklist:
                        continue
                    if tag not in self.relevant_damage_tags:
                        continue
                    tag_expected_damage.setdefault(tag, 0)
                    tag_expected_damage[tag] += expected_damage

                action_rows.append(
                    {
                        "index": row["index"],
                        "turn": f"T{row['turn']}",
                        "action": chip_data["name"],
                        "expected_damage": str(
                            Decimal(expected_damage).quantize(
                                Decimal("0.01"),
                                rounding=ROUND_DOWN,
                            )
                        ),
                        "critical_rate": f"{Decimal(combat_summary.critical_rate * 100).quantize(Decimal('0.1'), rounding=ROUND_DOWN)}%",
                    }
                )

            self.total_expected_damage_label.text = str(
                Decimal(total_expected_damage).quantize(
                    Decimal("0.01"),
                    rounding=ROUND_DOWN,
                )
            )
            self.combat_summary.expected_damage = total_expected_damage

            self.timeline_result_table.rows[:] = action_rows
            self.timeline_result_table.update()

            tag_rows: list[dict[str, Any]] = []
            for tag, expected_damage in tag_expected_damage.items():
                share_pct: float = (
                    expected_damage / total_expected_damage * 100
                    if total_expected_damage > 0
                    else 0
                )
                tag_rows.append(
                    {
                        "tag": str(tag),
                        "share": str(
                            Decimal(share_pct).quantize(
                                Decimal("0.1"),
                                rounding=ROUND_DOWN,
                            )
                        ),
                        "expected_damage": str(
                            Decimal(expected_damage).quantize(
                                Decimal("0.01"),
                                rounding=ROUND_DOWN,
                            )
                        ),
                    }
                )

            self.tag_breakdown_table.rows[:] = sorted(
                tag_rows,
                key=lambda row_data: float(row_data["share"]),
                reverse=True,
            )
            self.tag_breakdown_table.update()

            self.ability_donut_chart["data"][0]["labels"] = list(
                grouped_expected_damage.keys()
            )
            self.ability_donut_chart["data"][0]["values"] = list(
                grouped_expected_damage.values()
            )
            ui.update(self.ability_donut_chart_plot)

            self._update_expected_damage_delta_chart()
            self._update_scenario_comparison_chart()

            ui.notify("Rotation simulation complete", type="positive", group=False)
        finally:
            self._set_simulation_busy(False)
