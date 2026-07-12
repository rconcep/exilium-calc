from __future__ import annotations

from decimal import Decimal, ROUND_DOWN
from typing import Any, Callable
import copy

from nicegui import ui

from core.buffs import Buff, Debuff, buffs_option_config, debuffs_option_config
from core.combat import CombatSummary, DamageInstance, TargetCombatState
from core.types import DamageTag, Doll, SpecialAttribute, StatType, Unit, UnitLevel
from gui.styles.descriptions import get_stat_description
from gui.styles.graphs import get_donut_chart_template
from gui.templates.rotation_planner import RotationPlanner
from gui.templates.selectable_chips_editor import SelectableChipsEditor


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

        self.baseline_buffs_selector: SelectableChipsEditor
        self.baseline_debuffs_selector: SelectableChipsEditor
        self.baseline_phase_weaknesses: ui.select
        self.baseline_stability_broken: ui.switch
        self.baseline_unit_level: ui.select
        self.baseline_phase_tile_level: ui.select

        self.timeline_rows_container: ui.column
        self.timeline_rows: list[dict[str, Any]] = []

        self.total_expected_damage_label: ui.label
        self.timeline_result_table: ui.table
        self.tag_breakdown_table: ui.table

        self.ability_donut_chart: dict[str, Any] = get_donut_chart_template()
        self.ability_donut_chart_plot: ui.plotly

        self._build_ui()

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

            with ui.card().classes("w-120 exilium-panel"):
                self._summary_section()

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

        with ui.row().classes("w-full justify-end"):
            ui.button(
                "Simulate",
                on_click=self.simulate,
                icon="play_arrow",
            ).props("color=primary unelevated")

    def _build_target_state(self, timeline_row: dict[str, Any]) -> TargetCombatState:
        weaknesses_override: str = timeline_row["phase_weaknesses_override"].value
        stability_override: str = timeline_row["stability_override"].value
        unit_level_override: str = timeline_row["unit_level_override"].value
        phase_tile_override: str = timeline_row["phase_tile_override"].value

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
        for field in option_config[item["name"]]["fields"]:
            key: str = field["key"]
            value = item.get(key)
            if value in (None, "", False):
                continue
            field_parts.append(f"{field.get('label', key)}: {value}")

        if field_parts:
            label = f"{label} ({', '.join(field_parts)})"

        return f"{label} [#{occurrence_index}]"

    def _clone_effect_item(
        self, item: dict[str, Any], effect_kind: str
    ) -> dict[str, Any]:
        cloned_item: dict[str, Any] = copy.deepcopy(item)
        cloned_item["_effect_kind"] = effect_kind
        return cloned_item

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
            signature = self._effect_signature(item)
            signature_counts.setdefault(signature, 0)
            signature_counts[signature] += 1

            instance_id: str = item["_instance_id"]
            display_name: str = self._format_effect_instance_label(
                item=item,
                occurrence_index=signature_counts[signature],
            )

            options[instance_id] = display_name
            option_config[instance_id] = {
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

    def _refresh_all_removal_selectors(self) -> None:
        if not self.timeline_rows:
            return

        for row in self.timeline_rows:
            self._refresh_row_removal_selector(row=row, effect_kind="buff")
            self._refresh_row_removal_selector(row=row, effect_kind="debuff")

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
                }

                with ui.expansion(
                    text=f"T{turn} - {chip_data['name']}",
                    caption=self._get_timeline_expansion_caption(chip_data),
                    value=index == 1,
                    group="rotation-simulator-timeline",
                    icon="tune",
                ).classes("w-full exilium-panel"):
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
                                    value="Baseline",
                                    label="Phase Weaknesses Exploited",
                                )
                                row["stability_override"] = ui.select(
                                    options={
                                        "Baseline": "Baseline",
                                        "broken": "Stability Broken",
                                        "intact": "Stability Intact",
                                    },
                                    value="Baseline",
                                    label="Stability",
                                )
                                row["unit_level_override"] = ui.select(
                                    options={
                                        "Baseline": "Baseline",
                                        UnitLevel.BOSS.value: UnitLevel.BOSS.value,
                                        UnitLevel.ELITE.value: UnitLevel.ELITE.value,
                                        UnitLevel.NORMAL.value: UnitLevel.NORMAL.value,
                                    },
                                    value="Baseline",
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
                                    value="Baseline",
                                    label="Phase Tile",
                                )

                self.timeline_rows.append(row)

            self._refresh_all_removal_selectors()

        ui.notify(f"Synced {len(self.timeline_rows)} action(s)", type="positive")

    def simulate(self, _event: Any = None) -> None:
        """Runs combat calculations for each timeline row and aggregates results."""
        if not self.timeline_rows:
            ui.notify("Sync timeline first", type="warning")
            return

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
                to_remove=copy.deepcopy(row["remove_buffs_selector"].data),
            )
            self._remove_matching_items(
                active_items=active_debuffs_data,
                to_remove=copy.deepcopy(row["remove_debuffs_selector"].data),
            )

            active_buffs_data.extend(copy.deepcopy(row["add_buffs_selector"].data))
            active_debuffs_data.extend(copy.deepcopy(row["add_debuffs_selector"].data))

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

            for tag in damage_instance.tags:
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

        ui.notify("Rotation simulation complete", type="positive", group=False)
