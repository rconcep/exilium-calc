import copy
from typing import Any

from core.types import Doll, StatType, DamageTag, SpecialAttribute
from core.combat import CombatSummary


def update_expected_damage_delta_chart(tool: Any, _event: Any = None) -> None:
    """Updates expected damage deltas from configured sweep controls."""
    if not tool.last_action_type:
        tool.delta_chart["data"] = []
        ui_update(tool)
        return

    increment: float = float(tool.delta_increment_input.value or 0)
    steps: int = int(tool.delta_steps_input.value or 0)
    x_values: list[float] = [increment * i for i in range(steps + 1)]
    stat_source: str = tool.delta_stat_source_selector.value or "initial_stats"

    selected_multi_initial_stats: list[StatType] = (
        tool.delta_multi_initial_stats_selector.value or []
    )
    selected_multi_additive_stats: list[StatType] = (
        tool.delta_multi_additive_stats_selector.value or []
    )
    selected_multi_additive_special: list[str] = (
        tool.delta_multi_additive_special_selector.value or []
    )

    selected_stats: list[StatType] = tool.delta_stats_selector.value or []
    selected_special_attribute: SpecialAttribute | None = (
        tool.delta_special_attribute_selector.value
    )
    selected_special_attribute_tag: DamageTag | None = (
        tool.delta_special_attribute_tag_selector.value
    )

    if stat_source != "additive_special_attributes" and not selected_stats:
        tool.delta_chart["data"] = []
        ui_update(tool)
        return

    if stat_source == "additive_special_attributes" and (
        selected_special_attribute is None or selected_special_attribute_tag is None
    ):
        tool.delta_chart["data"] = []
        ui_update(tool)
        return

    base_expected_damage: float = tool.combat_summary.expected_damage
    if base_expected_damage <= 0:
        tool.delta_chart["data"] = []
        ui_update(tool)
        return

    traces: list[dict[str, Any]] = []

    if stat_source == "multi_series":
        if (
            not selected_multi_initial_stats
            and not selected_multi_additive_stats
            and not selected_multi_additive_special
        ):
            tool.delta_chart["data"] = []
            ui_update(tool)
            return

        for stat in selected_multi_initial_stats:
            deltas: list[float] = []
            for stat_increment in x_values:
                doll: Doll = copy.deepcopy(tool.doll)
                doll.initial_stats.basic_attributes[stat] += stat_increment
                summary: CombatSummary = tool._get_combat_summary_with_doll(doll)
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
                doll = copy.deepcopy(tool.doll)
                doll.additive_modifiers.basic_attributes[stat] += stat_increment
                summary = tool._get_combat_summary_with_doll(doll)
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
            special_attribute_value, tag_value = special_combo.split("::", maxsplit=1)
            selected_attribute: SpecialAttribute = SpecialAttribute(
                special_attribute_value
            )
            selected_tag: DamageTag = DamageTag(tag_value)

            deltas = []
            for stat_increment in x_values:
                doll = copy.deepcopy(tool.doll)
                doll.additive_modifiers.special_attributes[
                    selected_attribute
                ].add_to_multiplier(selected_tag, stat_increment)

                summary = tool._get_combat_summary_with_doll(doll)
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
        selected_special_attribute_typed: SpecialAttribute = selected_special_attribute  # type: ignore
        selected_special_attribute_tag_typed: DamageTag = selected_special_attribute_tag  # type: ignore
        deltas: list[float] = []

        for stat_increment in x_values:
            doll: Doll = copy.deepcopy(tool.doll)
            doll.additive_modifiers.special_attributes[
                selected_special_attribute_typed
            ].add_to_multiplier(selected_special_attribute_tag_typed, stat_increment)

            summary: CombatSummary = tool._get_combat_summary_with_doll(doll)
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
                doll: Doll = copy.deepcopy(tool.doll)
                if stat_source == "additive_modifiers":
                    doll.additive_modifiers.basic_attributes[stat] += stat_increment
                else:
                    doll.initial_stats.basic_attributes[stat] += stat_increment

                summary: CombatSummary = tool._get_combat_summary_with_doll(doll)
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

    tool.delta_chart["data"] = traces
    ui_update(tool)


def on_delta_stat_source_changed(tool: Any, _event: Any = None) -> None:
    """Prefills common comparison traces when switching to multi-series."""
    stat_source: str = tool.delta_stat_source_selector.value or "initial_stats"
    if stat_source == "multi_series":
        tool.delta_multi_initial_stats_selector.value = []
        tool.delta_multi_additive_stats_selector.value = []

        default_special_series: list[str] = []
        for attribute, tag in [
            (SpecialAttribute.DAMAGE_BOOST, DamageTag.ALL),
            (SpecialAttribute.CRITICAL_DAMAGE, DamageTag.ALL),
            (SpecialAttribute.DEFENSE_IGNORE, DamageTag.ALL),
        ]:
            key: str = f"{attribute.value}::{tag.value}"
            if key in tool.delta_special_combo_options:
                default_special_series.append(key)

        tool.delta_multi_additive_special_selector.value = default_special_series

        if not default_special_series and tool.delta_special_combo_options:
            first_special_combo: str = next(iter(tool.delta_special_combo_options))
            tool.delta_multi_additive_special_selector.value = [first_special_combo]

    update_delta_control_visibility(tool)
    update_expected_damage_delta_chart(tool)


def update_delta_control_visibility(tool: Any) -> None:
    """Shows only controls relevant to the currently selected increment source."""
    stat_source: str = tool.delta_stat_source_selector.value or "initial_stats"

    show_basic_stats: bool = stat_source in ["initial_stats", "additive_modifiers"]
    show_single_special: bool = stat_source == "additive_special_attributes"
    show_multi: bool = stat_source == "multi_series"

    tool.delta_basic_controls_container.set_visibility(show_basic_stats)
    tool.delta_single_special_controls_container.set_visibility(show_single_special)
    tool.delta_multi_controls_container.set_visibility(show_multi)


def ui_update(tool: Any) -> None:
    """Updates sweep chart widget."""
    from nicegui import ui

    ui.update(tool.delta_chart_plot)
