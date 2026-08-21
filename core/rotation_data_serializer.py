from __future__ import annotations

import json
from enum import Enum
from typing import Any

from core.rotation_name_aliases import canonical_action_name, canonical_effect_name
from core.types import StatType, UnitLevel


class RotationDataError(ValueError):
    """Raised when rotation data import validation fails."""


CURRENT_VERSION: int = 1
NUMBER_OF_TURNS: int = 7

DEFAULT_BASELINE_TARGET: dict[str, Any] = {
    "phase_weaknesses_exploited": 2,
    "stability_broken": True,
    "unit_level": UnitLevel.BOSS.value,
    "phase_tile_level": 0,
    "basic_attributes": {
        StatType.DEFENSE.value: 5000,
        StatType.HEALTH.value: 11e6,
        StatType.STABILITY_DAMAGE_REDUCTION.value: 60,
    },
}

DEFAULT_TARGET_OVERRIDES: dict[str, str] = {
    "phase_weaknesses_override": "Baseline",
    "stability_override": "Baseline",
    "unit_level_override": "Baseline",
    "phase_tile_override": "Baseline",
}


def _to_json_compatible(value: Any) -> Any:
    if isinstance(value, Enum):
        return value.value
    if isinstance(value, dict):
        return {
            str(key): _to_json_compatible(val)
            for key, val in value.items()
            if not str(key).startswith("_")
        }
    if isinstance(value, list):
        return [_to_json_compatible(item) for item in value]
    return value


def payload_to_string(payload: dict[str, Any]) -> str:
    """Serializes a normalized payload to pretty JSON."""
    return json.dumps(_to_json_compatible(payload), indent=2, ensure_ascii=False)


def string_to_payload(
    json_string: str,
    option_config: dict[str, dict[str, Any]],
    expected_doll_name: str | None = None,
) -> dict[str, Any]:
    """Deserializes and validates rotation JSON into normalized payload."""
    try:
        raw_payload = json.loads(json_string)
    except json.JSONDecodeError as exc:
        raise RotationDataError(f"Invalid JSON: {exc}") from exc

    return normalize_payload(raw_payload, option_config, expected_doll_name)


def build_payload_from_planner_defaults(
    doll_name: str,
    planner_turns: dict[int, list[dict[str, Any]]],
    baseline_buffs: list[dict[str, Any]],
    baseline_debuffs: list[dict[str, Any]],
) -> dict[str, Any]:
    """Builds a valid baseline payload from planner turns and baseline effects."""
    timeline_actions: list[dict[str, Any]] = []
    for turn in range(1, NUMBER_OF_TURNS + 1):
        for action in planner_turns.get(turn, []):
            timeline_actions.append(
                {
                    "turn": turn,
                    "action": _to_json_compatible(action),
                    "attacker": {"add_buffs": [], "remove_buffs": []},
                    "target": {
                        "add_debuffs": [],
                        "remove_debuffs": [],
                        **DEFAULT_TARGET_OVERRIDES,
                    },
                }
            )

    return {
        "metadata": {
            "version": CURRENT_VERSION,
            "doll_name": doll_name,
        },
        "baseline": {
            "attacker": {
                "buffs": _to_json_compatible(baseline_buffs),
            },
            "target": {
                "debuffs": _to_json_compatible(baseline_debuffs),
                **DEFAULT_BASELINE_TARGET,
            },
        },
        "planner": {
            "turns": {
                str(turn): _to_json_compatible(planner_turns.get(turn, []))
                for turn in range(1, NUMBER_OF_TURNS + 1)
            }
        },
        "timeline": {
            "actions": timeline_actions,
        },
    }


def _normalize_effect_chip(chip_raw: Any, context: str) -> dict[str, Any]:
    if not isinstance(chip_raw, dict):
        raise RotationDataError(f"{context} must contain object items")

    chip = {
        k: _to_json_compatible(v)
        for k, v in chip_raw.items()
        if not str(k).startswith("_")
    }
    name = chip.get("name")
    if not isinstance(name, str) or not name:
        raise RotationDataError(f"{context} item is missing a valid 'name'")

    chip["name"] = canonical_effect_name(name)

    return chip


def _normalize_action_chip(
    chip_raw: Any,
    option_config: dict[str, dict[str, Any]],
    context: str,
) -> dict[str, Any]:
    chip = _normalize_effect_chip(chip_raw, context)
    action_name = canonical_action_name(chip["name"])
    chip["name"] = action_name

    if action_name not in option_config:
        raise RotationDataError(
            f"{context} action '{action_name}' does not exist for this doll"
        )

    expected_fields: list[str] = [
        field["key"] for field in option_config[action_name].get("fields", [])
    ]
    actual_fields: set[str] = {key for key in chip.keys() if key != "name"}
    missing = sorted(set(expected_fields) - actual_fields)
    extra = sorted(actual_fields - set(expected_fields))
    if missing or extra:
        details: list[str] = []
        if missing:
            details.append(f"missing fields: {missing}")
        if extra:
            details.append(f"unexpected fields: {extra}")
        detail_text = "; ".join(details)
        raise RotationDataError(
            f"{context} action '{action_name}' parameters are incompatible with the current definition ({detail_text})"
        )

    normalized: dict[str, Any] = {"name": action_name}
    for field_key in expected_fields:
        normalized[field_key] = chip[field_key]
    return normalized


def _normalize_planner_turns(
    turns_raw: Any,
    option_config: dict[str, dict[str, Any]],
) -> dict[int, list[dict[str, Any]]]:
    if not isinstance(turns_raw, dict):
        raise RotationDataError("planner.turns must be an object")

    normalized: dict[int, list[dict[str, Any]]] = {}

    for key in turns_raw.keys():
        try:
            turn = int(key)
        except (TypeError, ValueError) as exc:
            raise RotationDataError(
                f"planner.turns key '{key}' is not an integer"
            ) from exc

        if turn < 1 or turn > NUMBER_OF_TURNS:
            raise RotationDataError(
                f"planner.turns key '{turn}' is out of range (1..{NUMBER_OF_TURNS})"
            )

    for turn in range(1, NUMBER_OF_TURNS + 1):
        turn_entries = turns_raw.get(turn, turns_raw.get(str(turn), []))
        if turn_entries is None:
            turn_entries = []
        if not isinstance(turn_entries, list):
            raise RotationDataError(f"planner.turns[{turn}] must be a list")

        normalized[turn] = [
            _normalize_action_chip(
                entry,
                option_config=option_config,
                context=f"planner.turns[{turn}]",
            )
            for entry in turn_entries
        ]

    return normalized


def _normalize_baseline(baseline_raw: Any) -> dict[str, Any]:
    if not isinstance(baseline_raw, dict):
        baseline_raw = {}

    attacker_raw = baseline_raw.get("attacker", {})
    if not isinstance(attacker_raw, dict):
        attacker_raw = {}
    target_raw = baseline_raw.get("target", {})
    if not isinstance(target_raw, dict):
        target_raw = {}

    buffs_raw = attacker_raw.get("buffs", [])
    if not isinstance(buffs_raw, list):
        raise RotationDataError("baseline.attacker.buffs must be a list")

    debuffs_raw = target_raw.get("debuffs", [])
    if not isinstance(debuffs_raw, list):
        raise RotationDataError("baseline.target.debuffs must be a list")

    basic_raw = target_raw.get("basic_attributes", {})
    if not isinstance(basic_raw, dict):
        basic_raw = {}

    default_basic = DEFAULT_BASELINE_TARGET["basic_attributes"]
    basic_attributes: dict[str, float] = {}
    for key, default_value in default_basic.items():
        value = basic_raw.get(key, default_value)
        try:
            basic_attributes[key] = float(value)
        except (TypeError, ValueError) as exc:
            raise RotationDataError(
                f"baseline.target.basic_attributes.{key} must be numeric"
            ) from exc

    try:
        phase_weaknesses_exploited = int(
            target_raw.get(
                "phase_weaknesses_exploited",
                DEFAULT_BASELINE_TARGET["phase_weaknesses_exploited"],
            )
        )
    except (TypeError, ValueError) as exc:
        raise RotationDataError(
            "baseline.target.phase_weaknesses_exploited must be an integer"
        ) from exc

    stability_broken = bool(
        target_raw.get("stability_broken", DEFAULT_BASELINE_TARGET["stability_broken"])
    )

    unit_level = str(
        target_raw.get("unit_level", DEFAULT_BASELINE_TARGET["unit_level"])
    )
    if unit_level not in {level.value for level in UnitLevel}:
        raise RotationDataError(f"baseline.target.unit_level '{unit_level}' is invalid")

    try:
        phase_tile_level = int(
            target_raw.get(
                "phase_tile_level", DEFAULT_BASELINE_TARGET["phase_tile_level"]
            )
        )
    except (TypeError, ValueError) as exc:
        raise RotationDataError(
            "baseline.target.phase_tile_level must be an integer"
        ) from exc

    return {
        "attacker": {
            "buffs": [
                _normalize_effect_chip(item, "baseline.attacker.buffs")
                for item in buffs_raw
            ]
        },
        "target": {
            "debuffs": [
                _normalize_effect_chip(item, "baseline.target.debuffs")
                for item in debuffs_raw
            ],
            "phase_weaknesses_exploited": phase_weaknesses_exploited,
            "stability_broken": stability_broken,
            "unit_level": unit_level,
            "phase_tile_level": phase_tile_level,
            "basic_attributes": basic_attributes,
        },
    }


def _normalize_timeline(
    timeline_raw: Any,
    option_config: dict[str, dict[str, Any]],
) -> dict[str, Any]:
    if not isinstance(timeline_raw, dict):
        timeline_raw = {}

    actions_raw = timeline_raw.get("actions", [])
    if not isinstance(actions_raw, list):
        raise RotationDataError("timeline.actions must be a list")

    normalized_actions: list[dict[str, Any]] = []
    for index, action_row in enumerate(actions_raw, start=1):
        context = f"timeline.actions[{index}]"
        if not isinstance(action_row, dict):
            raise RotationDataError(f"{context} must be an object")

        turn_raw = action_row.get("turn")
        try:
            turn = int(turn_raw)
        except (TypeError, ValueError) as exc:
            raise RotationDataError(f"{context}.turn must be an integer") from exc

        if turn < 1 or turn > NUMBER_OF_TURNS:
            raise RotationDataError(
                f"{context}.turn must be between 1 and {NUMBER_OF_TURNS}"
            )

        action_chip = _normalize_action_chip(
            action_row.get("action", {}),
            option_config,
            context=f"{context}.action",
        )

        attacker_raw = action_row.get("attacker", {})
        if not isinstance(attacker_raw, dict):
            attacker_raw = {}

        target_raw = action_row.get("target", {})
        if not isinstance(target_raw, dict):
            target_raw = {}

        add_buffs_raw = attacker_raw.get("add_buffs", [])
        remove_buffs_raw = attacker_raw.get("remove_buffs", [])
        add_debuffs_raw = target_raw.get("add_debuffs", [])
        remove_debuffs_raw = target_raw.get("remove_debuffs", [])
        if not isinstance(add_buffs_raw, list):
            raise RotationDataError(f"{context}.attacker.add_buffs must be a list")
        if not isinstance(remove_buffs_raw, list):
            raise RotationDataError(f"{context}.attacker.remove_buffs must be a list")
        if not isinstance(add_debuffs_raw, list):
            raise RotationDataError(f"{context}.target.add_debuffs must be a list")
        if not isinstance(remove_debuffs_raw, list):
            raise RotationDataError(f"{context}.target.remove_debuffs must be a list")

        phase_weaknesses_override = str(
            target_raw.get(
                "phase_weaknesses_override",
                DEFAULT_TARGET_OVERRIDES["phase_weaknesses_override"],
            )
        )
        stability_override = str(
            target_raw.get(
                "stability_override", DEFAULT_TARGET_OVERRIDES["stability_override"]
            )
        )
        unit_level_override = str(
            target_raw.get(
                "unit_level_override", DEFAULT_TARGET_OVERRIDES["unit_level_override"]
            )
        )
        phase_tile_override = str(
            target_raw.get(
                "phase_tile_override", DEFAULT_TARGET_OVERRIDES["phase_tile_override"]
            )
        )

        normalized_actions.append(
            {
                "turn": turn,
                "action": action_chip,
                "attacker": {
                    "add_buffs": [
                        _normalize_effect_chip(item, f"{context}.attacker.add_buffs")
                        for item in add_buffs_raw
                    ],
                    "remove_buffs": [
                        _normalize_effect_chip(item, f"{context}.attacker.remove_buffs")
                        for item in remove_buffs_raw
                    ],
                },
                "target": {
                    "add_debuffs": [
                        _normalize_effect_chip(item, f"{context}.target.add_debuffs")
                        for item in add_debuffs_raw
                    ],
                    "remove_debuffs": [
                        _normalize_effect_chip(item, f"{context}.target.remove_debuffs")
                        for item in remove_debuffs_raw
                    ],
                    "phase_weaknesses_override": phase_weaknesses_override,
                    "stability_override": stability_override,
                    "unit_level_override": unit_level_override,
                    "phase_tile_override": phase_tile_override,
                },
            }
        )

    return {"actions": normalized_actions}


def normalize_payload(
    payload_raw: Any,
    option_config: dict[str, dict[str, Any]],
    expected_doll_name: str | None = None,
) -> dict[str, Any]:
    """Validates and normalizes rotation data payload."""
    if not isinstance(payload_raw, dict):
        raise RotationDataError("Rotation data must be a JSON object")

    metadata_raw = payload_raw.get("metadata", {})
    if not isinstance(metadata_raw, dict):
        metadata_raw = {}

    version_raw = metadata_raw.get("version", CURRENT_VERSION)
    try:
        version = int(version_raw)
    except (TypeError, ValueError) as exc:
        raise RotationDataError("metadata.version must be an integer") from exc

    doll_name = str(metadata_raw.get("doll_name", "")).strip()
    if not doll_name:
        raise RotationDataError("metadata.doll_name is required")

    if expected_doll_name and doll_name != expected_doll_name:
        raise RotationDataError(
            f"Rotation data is for doll '{doll_name}', not '{expected_doll_name}'"
        )

    planner_raw = payload_raw.get("planner", {})
    if not isinstance(planner_raw, dict):
        planner_raw = {}

    turns_raw = planner_raw.get("turns", {})
    normalized_turns = _normalize_planner_turns(turns_raw, option_config)
    normalized_baseline = _normalize_baseline(payload_raw.get("baseline", {}))
    normalized_timeline = _normalize_timeline(
        payload_raw.get("timeline", {}), option_config
    )

    return {
        "metadata": {
            "version": version,
            "doll_name": doll_name,
        },
        "baseline": normalized_baseline,
        "planner": {
            "turns": {str(turn): actions for turn, actions in normalized_turns.items()}
        },
        "timeline": normalized_timeline,
    }
