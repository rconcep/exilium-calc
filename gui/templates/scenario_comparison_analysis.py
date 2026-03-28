from __future__ import annotations

import copy
from typing import Any

from nicegui import ui

from core.types import Doll, StatType, DamageTag, SpecialAttribute
from core.combat import CombatSummary


def default_scenario_tag(tool: Any) -> DamageTag:
    """Returns a stable default tag for scenario controls."""
    return (
        DamageTag.ALL
        if DamageTag.ALL in tool.relevant_damage_tags
        else tool.relevant_damage_tags[0]
    )


def apply_scenario_component(
    doll: Doll,
    source: str,
    increment: float,
    stat: StatType,
    special_attribute: SpecialAttribute,
    tag: DamageTag,
) -> None:
    """Applies one increment component to a doll clone."""
    if source == "additive_special_attributes":
        doll.additive_modifiers.special_attributes[special_attribute].add_to_multiplier(
            tag, increment
        )
    elif source == "additive_modifiers":
        doll.additive_modifiers.basic_attributes[stat] += increment
    else:
        doll.initial_stats.basic_attributes[stat] += increment


def update_scenario_component_visibility(
    tool: Any, scenario_row: dict[str, Any], component_index: int
) -> None:
    """Shows only the relevant selectors for one scenario component."""
    source: str = scenario_row[f"source_{component_index}"].value
    show_basic: bool = source in ["initial_stats", "additive_modifiers"]
    show_special: bool = source == "additive_special_attributes"

    scenario_row[f"stat_{component_index}"].set_visibility(show_basic)
    scenario_row[f"special_attribute_{component_index}"].set_visibility(show_special)
    scenario_row[f"tag_{component_index}"].set_visibility(show_special)


def update_scenario_row_visibility(tool: Any, scenario_row: dict[str, Any]) -> None:
    """Shows only controls relevant to row mode and component source."""
    mode: str = scenario_row["mode"].value or "single"
    component_count: int = int(scenario_row["component_count"].value or 1)
    if mode != "combined":
        component_count = 1
        scenario_row["component_count"].value = 1

    scenario_row["component_count"].set_visibility(mode == "combined")
    scenario_row["add_component_btn"].set_visibility(mode == "combined")
    scenario_row["remove_component_btn"].set_visibility(mode == "combined")

    scenario_row["component_container_2"].set_visibility(component_count >= 2)
    scenario_row["component_container_3"].set_visibility(component_count >= 3)

    update_scenario_component_visibility(tool, scenario_row, 1)
    update_scenario_component_visibility(tool, scenario_row, 2)
    update_scenario_component_visibility(tool, scenario_row, 3)


def remove_scenario_row(tool: Any, scenario_row: dict[str, Any]) -> None:
    """Removes the specified scenario row."""
    if scenario_row in tool.delta_scenario_rows:
        tool.delta_scenario_rows.remove(scenario_row)
    scenario_row["container"].delete()
    update_scenario_comparison_chart(tool)


def add_component_to_scenario_row(tool: Any, scenario_row: dict[str, Any]) -> None:
    """Adds one component to a combined row up to 3."""
    current_count: int = int(scenario_row["component_count"].value or 1)
    scenario_row["component_count"].value = min(3, current_count + 1)
    update_scenario_row_visibility(tool, scenario_row)
    update_scenario_comparison_chart(tool)


def remove_component_from_scenario_row(tool: Any, scenario_row: dict[str, Any]) -> None:
    """Removes one component from a combined row down to 1."""
    current_count: int = int(scenario_row["component_count"].value or 1)
    scenario_row["component_count"].value = max(1, current_count - 1)
    update_scenario_row_visibility(tool, scenario_row)
    update_scenario_comparison_chart(tool)


def add_single_scenario_row(tool: Any, _event: Any = None) -> None:
    """Adds one single-component scenario row."""
    tag: DamageTag = default_scenario_tag(tool)
    create_scenario_row(
        tool,
        label=f"Scenario {tool.delta_scenario_next_index}",
        mode="single",
        component_1={
            "source": "initial_stats",
            "increment": 30,
            "stat": StatType.ATTACK,
            "special_attribute": SpecialAttribute.DAMAGE_BOOST,
            "tag": tag,
        },
        component_2={
            "source": "initial_stats",
            "increment": 0,
            "stat": StatType.HEALTH,
            "special_attribute": SpecialAttribute.DAMAGE_BOOST,
            "tag": tag,
        },
        component_3={
            "source": "additive_special_attributes",
            "increment": 0,
            "stat": StatType.ATTACK,
            "special_attribute": SpecialAttribute.DAMAGE_BOOST,
            "tag": tag,
        },
    )
    tool.delta_scenario_next_index += 1
    update_scenario_comparison_chart(tool)


def add_combined_scenario_row(tool: Any, _event: Any = None) -> None:
    """Adds one combined scenario row with three increment components."""
    tag: DamageTag = default_scenario_tag(tool)
    create_scenario_row(
        tool,
        label=f"Combined {tool.delta_scenario_next_index}",
        mode="combined",
        component_1={
            "source": "initial_stats",
            "increment": 30,
            "stat": StatType.ATTACK,
            "special_attribute": SpecialAttribute.DAMAGE_BOOST,
            "tag": tag,
        },
        component_2={
            "source": "initial_stats",
            "increment": 50,
            "stat": StatType.HEALTH,
            "special_attribute": SpecialAttribute.DAMAGE_BOOST,
            "tag": tag,
        },
        component_3={
            "source": "additive_special_attributes",
            "increment": 4,
            "stat": StatType.ATTACK,
            "special_attribute": SpecialAttribute.DAMAGE_BOOST,
            "tag": tag,
        },
    )
    tool.delta_scenario_next_index += 1
    update_scenario_comparison_chart(tool)


def create_scenario_row(
    tool: Any,
    label: str,
    mode: str,
    component_1: dict[str, Any],
    component_2: dict[str, Any],
    component_3: dict[str, Any],
) -> None:
    """Creates one editable scenario row for the comparison chart."""
    with tool.scenario_rows_container:
        row_container = ui.card().classes("w-full")

    with row_container:
        with ui.grid(columns=3).classes("w-full gap-2 items-end"):
            row_label = ui.input(label="Label", value=label).on(
                "update:model-value",
                lambda e: update_scenario_comparison_chart(tool, e),
            )
            row_mode = ui.select(
                options={"single": "Single", "combined": "Combined"},
                value=mode,
                label="Row mode",
            )
            row_component_count = ui.number(
                label="Components",
                value=3 if mode == "combined" else 1,
                min=1,
                max=3,
                precision=0,
            ).on(
                "update:model-value",
                lambda e: update_scenario_comparison_chart(tool, e),
            )

        with ui.row().classes("w-full gap-2"):
            add_component_btn = ui.button("Component", icon="add", color="secondary")
            remove_component_btn = ui.button(
                "Component", icon="remove", color="secondary"
            )
            remove_row_btn = ui.button("Remove Scenario", color="negative").props(
                "outline"
            )

        with ui.column().classes("w-full gap-2") as component_container_1:
            ui.label("Component 1").classes("text-caption text-bold")
            with ui.grid(columns=5).classes("w-full gap-2"):
                row_source_1 = ui.select(
                    options={
                        "initial_stats": "Initial Stats",
                        "additive_modifiers": "Additive Modifiers (Basic)",
                        "additive_special_attributes": "Additive Modifiers (Special)",
                    },
                    value=component_1["source"],
                    label="Source",
                )
                row_increment_1 = ui.number(
                    label="Increment",
                    value=component_1["increment"],
                    precision=2,
                ).on(
                    "update:model-value",
                    lambda e: update_scenario_comparison_chart(tool, e),
                )
                row_stat_1 = ui.select(
                    options=[stat_option for stat_option in StatType],
                    value=component_1["stat"],
                    label="Basic stat",
                ).on(
                    "update:model-value",
                    lambda e: update_scenario_comparison_chart(tool, e),
                )
                row_special_attribute_1 = ui.select(
                    options=[attribute for attribute in SpecialAttribute],
                    value=component_1["special_attribute"],
                    label="Special Attribute",
                ).on(
                    "update:model-value",
                    lambda e: update_scenario_comparison_chart(tool, e),
                )
                row_tag_1 = ui.select(
                    options=tool.relevant_damage_tags,
                    value=component_1["tag"],
                    label="Damage tag",
                ).on(
                    "update:model-value",
                    lambda e: update_scenario_comparison_chart(tool, e),
                )

        with ui.column().classes("w-full gap-2") as component_container_2:
            ui.label("Component 2").classes("text-caption text-bold")
            with ui.grid(columns=5).classes("w-full gap-2"):
                row_source_2 = ui.select(
                    options={
                        "initial_stats": "Initial Stats",
                        "additive_modifiers": "Additive Modifiers (Basic)",
                        "additive_special_attributes": "Additive Modifiers (Special)",
                    },
                    value=component_2["source"],
                    label="Source",
                )
                row_increment_2 = ui.number(
                    label="Increment",
                    value=component_2["increment"],
                    precision=2,
                ).on(
                    "update:model-value",
                    lambda e: update_scenario_comparison_chart(tool, e),
                )
                row_stat_2 = ui.select(
                    options=[stat_option for stat_option in StatType],
                    value=component_2["stat"],
                    label="Basic stat",
                ).on(
                    "update:model-value",
                    lambda e: update_scenario_comparison_chart(tool, e),
                )
                row_special_attribute_2 = ui.select(
                    options=[attribute for attribute in SpecialAttribute],
                    value=component_2["special_attribute"],
                    label="Special Attribute",
                ).on(
                    "update:model-value",
                    lambda e: update_scenario_comparison_chart(tool, e),
                )
                row_tag_2 = ui.select(
                    options=tool.relevant_damage_tags,
                    value=component_2["tag"],
                    label="Damage tag",
                ).on(
                    "update:model-value",
                    lambda e: update_scenario_comparison_chart(tool, e),
                )

        with ui.column().classes("w-full gap-2") as component_container_3:
            ui.label("Component 3").classes("text-caption text-bold")
            with ui.grid(columns=5).classes("w-full gap-2"):
                row_source_3 = ui.select(
                    options={
                        "initial_stats": "Initial Stats",
                        "additive_modifiers": "Additive Modifiers (Basic)",
                        "additive_special_attributes": "Additive Modifiers (Special)",
                    },
                    value=component_3["source"],
                    label="Source",
                )
                row_increment_3 = ui.number(
                    label="Increment",
                    value=component_3["increment"],
                    precision=2,
                ).on(
                    "update:model-value",
                    lambda e: update_scenario_comparison_chart(tool, e),
                )
                row_stat_3 = ui.select(
                    options=[stat_option for stat_option in StatType],
                    value=component_3["stat"],
                    label="Basic stat",
                ).on(
                    "update:model-value",
                    lambda e: update_scenario_comparison_chart(tool, e),
                )
                row_special_attribute_3 = ui.select(
                    options=[attribute for attribute in SpecialAttribute],
                    value=component_3["special_attribute"],
                    label="Special Attribute",
                ).on(
                    "update:model-value",
                    lambda e: update_scenario_comparison_chart(tool, e),
                )
                row_tag_3 = ui.select(
                    options=tool.relevant_damage_tags,
                    value=component_3["tag"],
                    label="Damage tag",
                ).on(
                    "update:model-value",
                    lambda e: update_scenario_comparison_chart(tool, e),
                )

    scenario_row: dict[str, Any] = {
        "container": row_container,
        "label": row_label,
        "mode": row_mode,
        "component_count": row_component_count,
        "add_component_btn": add_component_btn,
        "remove_component_btn": remove_component_btn,
        "remove_row_btn": remove_row_btn,
        "component_container_1": component_container_1,
        "component_container_2": component_container_2,
        "component_container_3": component_container_3,
        "source_1": row_source_1,
        "increment_1": row_increment_1,
        "stat_1": row_stat_1,
        "special_attribute_1": row_special_attribute_1,
        "tag_1": row_tag_1,
        "source_2": row_source_2,
        "increment_2": row_increment_2,
        "stat_2": row_stat_2,
        "special_attribute_2": row_special_attribute_2,
        "tag_2": row_tag_2,
        "source_3": row_source_3,
        "increment_3": row_increment_3,
        "stat_3": row_stat_3,
        "special_attribute_3": row_special_attribute_3,
        "tag_3": row_tag_3,
    }

    row_mode.on(
        "update:model-value",
        lambda _event, row=scenario_row: (
            update_scenario_row_visibility(tool, row),
            update_scenario_comparison_chart(tool),
        ),
    )

    row_component_count.on(
        "update:model-value",
        lambda _event, row=scenario_row: (
            update_scenario_row_visibility(tool, row),
            update_scenario_comparison_chart(tool),
        ),
    )

    row_source_1.on(
        "update:model-value",
        lambda _event, row=scenario_row: (
            update_scenario_component_visibility(tool, row, 1),
            update_scenario_comparison_chart(tool),
        ),
    )
    row_source_2.on(
        "update:model-value",
        lambda _event, row=scenario_row: (
            update_scenario_component_visibility(tool, row, 2),
            update_scenario_comparison_chart(tool),
        ),
    )
    row_source_3.on(
        "update:model-value",
        lambda _event, row=scenario_row: (
            update_scenario_component_visibility(tool, row, 3),
            update_scenario_comparison_chart(tool),
        ),
    )

    add_component_btn.on(
        "click",
        lambda _event, row=scenario_row: add_component_to_scenario_row(tool, row),
    )
    remove_component_btn.on(
        "click",
        lambda _event, row=scenario_row: remove_component_from_scenario_row(tool, row),
    )
    remove_row_btn.on(
        "click", lambda _event, row=scenario_row: remove_scenario_row(tool, row)
    )

    tool.delta_scenario_rows.append(scenario_row)
    update_scenario_row_visibility(tool, scenario_row)


def update_scenario_comparison_chart(tool: Any, _event: Any = None) -> None:
    """Updates one-point mixed-increment scenario comparison chart."""
    if not tool.last_action_type:
        tool.scenario_chart["data"] = []
        ui.update(tool.scenario_chart_plot)
        return

    base_expected_damage: float = tool.combat_summary.expected_damage
    if base_expected_damage <= 0:
        tool.scenario_chart["data"] = []
        ui.update(tool.scenario_chart_plot)
        return

    labels: list[str] = []
    deltas: list[float] = []
    marker_colors: list[str] = []
    text_values: list[str] = []

    for idx, scenario_row in enumerate(tool.delta_scenario_rows):
        label: str = scenario_row["label"].value or f"Scenario {idx + 1}"
        mode: str = scenario_row["mode"].value or "single"
        component_count: int = int(scenario_row["component_count"].value or 1)
        if mode == "single":
            component_indices: list[int] = [1]
        else:
            component_count = max(1, min(3, component_count))
            component_indices = list(range(1, component_count + 1))

        doll: Doll = copy.deepcopy(tool.doll)
        for component_idx in component_indices:
            source: str = (
                scenario_row[f"source_{component_idx}"].value or "initial_stats"
            )
            increment: float = float(
                scenario_row[f"increment_{component_idx}"].value or 0
            )
            stat: StatType = scenario_row[f"stat_{component_idx}"].value
            special_attribute: SpecialAttribute = scenario_row[
                f"special_attribute_{component_idx}"
            ].value
            tag: DamageTag = scenario_row[f"tag_{component_idx}"].value

            if increment == 0:
                continue

            apply_scenario_component(
                doll=doll,
                source=source,
                increment=increment,
                stat=stat,
                special_attribute=special_attribute,
                tag=tag,
            )

        summary: CombatSummary = tool._get_combat_summary_with_doll(doll)
        delta_pct: float = (
            (summary.expected_damage - base_expected_damage)
            / base_expected_damage
            * 100
        )

        labels.append(label)
        deltas.append(delta_pct)
        marker_colors.append("#2E7D32" if delta_pct >= 0 else "#C62828")
        text_values.append(f"{delta_pct:.2f}%")

    tool.scenario_chart["data"] = [
        {
            "type": "bar",
            "orientation": "h",
            "x": deltas,
            "y": labels,
            "text": text_values,
            "textposition": "auto",
            "marker": {"color": marker_colors},
            "hovertemplate": "%{y}: %{x:.2f}%<extra></extra>",
        }
    ]
    ui.update(tool.scenario_chart_plot)
