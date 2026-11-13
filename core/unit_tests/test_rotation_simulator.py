from __future__ import annotations

from gui.templates.rotation_simulator import RotationSimulator
from core.rotation_data_serializer import string_to_payload


class _DummySelectableChipsEditor:
    def __init__(self):
        self.data = []
        self.options = {}
        self.option_config = {}

    def set_options_and_config(self, options, option_config):
        self.options = options
        self.option_config = option_config

    def set_data(self, data, notify=False):
        self.data = data


def test_refresh_row_removal_selector_with_available_handles_missing_instance_id():
    sim = RotationSimulator.__new__(RotationSimulator)
    row = {"remove_debuffs_selector": _DummySelectableChipsEditor()}

    available_items = [
        {"name": "Confagration", "stack": 1},
        {"name": "Defense Down I", "stack": 2},
    ]

    sim._refresh_row_removal_selector_with_available(
        row=row,
        effect_kind="debuff",
        available_items=available_items,
    )

    assert all("_instance_id" in item for item in available_items)
    assert row["remove_debuffs_selector"].data == []

    legacy_item = {"name": "Legacy Debuff Value", "stack": 99}
    label = sim._format_effect_instance_label(
        sim._ensure_effect_item_metadata(legacy_item, "debuff"),
        occurrence_index=1,
    )
    assert label.endswith("[ #1 ]") is False
    assert "Legacy Debuff Value" in label


def test_rotation_data_normalizes_legacy_ots14_names():
        payload = string_to_payload(
                """
                {
                    "metadata": {"version": 1, "doll_name": "OTs-14"},
                    "baseline": {
                        "attacker": {"buffs": [{"name": "Demolition Mode (OTs-14)"}]},
                        "target": {"debuffs": [{"name": "Reconstruction: Burn (OTs-14)"}]}
                    },
                    "planner": {
                        "turns": {"1": [{"name": "Combat Instinct"}]}
                    },
                    "timeline": {
                        "actions": [{
                            "turn": 1,
                            "action": {"name": "Critical Splash", "previous_uses": 1},
                            "attacker": {
                                "add_buffs": [{"name": "Cover Mode (OTs-14)"}],
                                "remove_buffs": []
                            },
                            "target": {
                                "add_debuffs": [],
                                "remove_debuffs": [{"name": "Reconstruction: Electric (OTs-14)"}]
                            }
                        }]
                    }
                }
                """,
                option_config={
                        "Shooting Instinct": {"fields": []},
                        "Critical Blast": {
                                "fields": [{"key": "previous_uses"}],
                        },
                },
        )

        assert payload["planner"]["turns"]["1"][0]["name"] == "Shooting Instinct"
        assert payload["timeline"]["actions"][0]["action"]["name"] == "Critical Blast"
        assert (
                payload["baseline"]["attacker"]["buffs"][0]["name"]
                == "Demolition Order (OTs-14)"
        )
        assert (
                payload["timeline"]["actions"][0]["attacker"]["add_buffs"][0]["name"]
                == "Cover Order (OTs-14)"
        )
        assert (
                payload["baseline"]["target"]["debuffs"][0]["name"]
                == "Reconfiguration - Burn (OTs-14)"
        )


def test_rotation_data_normalizes_legacy_welrod_names():
    option_config = {
        "Hushed Erasure": {"fields": []},
        "Subjective Sanction": {"fields": []},
        "Judgement Blast": {
            "fields": [
                {"key": "instances_of_damage_taken"},
                {"key": "number_of_targets_hit"},
            ]
        },
        "Iniquity's Retribution": {
            "fields": [{"key": "detectives_immunity_accumulated_damage"}]
        },
        "Case Controller": {
            "fields": [{"key": "detectives_immunity_accumulated_damage"}]
        },
    }
    payload = string_to_payload(
        """
        {
            "metadata": {"version": 1, "doll_name": "Welrod"},
            "baseline": {
                "attacker": {"buffs": [{"name": "Deductive Obsession (Welrod)"}]},
                "target": {"debuffs": [{"name": "Case Detective (Welrod)"}]}
            },
            "planner": {
                "turns": {
                    "1": [
                        {"name": "Silent Takedown"},
                        {"name": "Conviction and Punishment"},
                        {
                            "name": "Hour of Reckoning",
                            "instances_of_damage_taken": 1,
                            "number_of_targets_hit": 2
                        },
                        {
                            "name": "Crime Backlash",
                            "detectives_immunity_accumulated_damage": 1000
                        },
                        {
                            "name": "Case Detective",
                            "detectives_immunity_accumulated_damage": 1000
                        }
                    ]
                }
            },
            "timeline": {
                "actions": [
                    {
                        "turn": 1,
                        "action": {"name": "Silent Takedown"},
                        "attacker": {
                            "add_buffs": [{"name": "Deductive Obsession (Welrod)"}],
                            "remove_buffs": []
                        },
                        "target": {
                            "add_debuffs": [{"name": "Case Detective (Welrod)"}],
                            "remove_debuffs": []
                        }
                    }
                ]
            }
        }
        """,
        option_config=option_config,
    )

    actions = payload["planner"]["turns"]["1"]
    assert [action["name"] for action in actions] == [
        "Hushed Erasure",
        "Subjective Sanction",
        "Judgement Blast",
        "Iniquity's Retribution",
        "Case Controller",
    ]
    assert (
        payload["baseline"]["attacker"]["buffs"][0]["name"]
        == "Deduction Obsession (Welrod)"
    )
    assert (
        payload["baseline"]["target"]["debuffs"][0]["name"]
        == "Case Controller (Welrod)"
    )
    timeline_action = payload["timeline"]["actions"][0]
    assert timeline_action["action"]["name"] == "Hushed Erasure"
    assert (
        timeline_action["attacker"]["add_buffs"][0]["name"]
        == "Deduction Obsession (Welrod)"
    )
    assert (
        timeline_action["target"]["add_debuffs"][0]["name"]
        == "Case Controller (Welrod)"
    )


def test_rotation_data_normalizes_legacy_faelynn_names_and_fields():
    stack_field = {"key": "stacks_of_hunt_tracking"}
    option_config = {
        "Burst Fang": {"fields": []},
        "Triple Maul": {"fields": [stack_field]},
        "Triple Maul (follow-up)": {
            "fields": [
                {"key": "number_of_targets_hit"},
                {"key": "boss_was_hit"},
            ]
        },
        "Scent Trail": {"fields": []},
        "Loyal Dash": {"fields": [stack_field]},
        "Pursuit Instinct I": {
            "fields": [stack_field, {"key": "number_of_targets_hit"}]
        },
        "Pursuit Instinct II": {
            "fields": [
                stack_field,
                {"key": "number_of_targets_hit"},
                {"key": "has_collar_brand"},
            ]
        },
        "Pursuit Instinct III": {
            "fields": [
                stack_field,
                {"key": "number_of_targets_hit"},
                {"key": "has_collar_brand"},
                {"key": "target_tile_ascension_level"},
            ]
        },
    }
    payload = string_to_payload(
        """
        {
            "metadata": {"version": 1, "doll_name": "Faelynn"},
            "baseline": {
                "attacker": {
                    "buffs": [
                        {"name": "Hunter's Tracking (Faelynn)"},
                        {"name": "Roving Bloodlust (Faelynn)"}
                    ]
                },
                "target": {"debuffs": [{"name": "Scent Mark (Faelynn)"}]}
            },
            "planner": {
                "turns": {
                    "1": [
                        {"name": "Cuspid Combo"},
                        {"name": "Triple Maule", "stacks_of_hunters_tracking": 2},
                        {
                            "name": "Triple Maule (follow-up)",
                            "number_of_targets_hit": 4,
                            "boss_was_hit": false
                        },
                        {"name": "Scent Mark"},
                        {"name": "Loyal Hunt", "stacks_of_hunters_tracking": 3},
                        {
                            "name": "Hunter's Instinct I",
                            "stacks_of_hunters_tracking": 1,
                            "number_of_targets_hit": 2
                        },
                        {
                            "name": "Hunter's Instinct II",
                            "stacks_of_hunters_tracking": 2,
                            "number_of_targets_hit": 1,
                            "has_collar_brand": true
                        },
                        {
                            "name": "Hunter's Instinct III",
                            "stacks_of_hunters_tracking": 3,
                            "number_of_targets_hit": 2,
                            "has_collar_brand": false,
                            "target_tile_ascension_level": 1
                        }
                    ]
                }
            },
            "timeline": {
                "actions": [{
                    "turn": 1,
                    "action": {
                        "name": "Hunter's Instinct I",
                        "stacks_of_hunters_tracking": 1,
                        "number_of_targets_hit": 1
                    },
                    "attacker": {
                        "add_buffs": [
                            {"name": "Hunter's Tracking (Faelynn)"},
                            {"name": "Roving Bloodlust (Faelynn)"}
                        ],
                        "remove_buffs": []
                    },
                    "target": {
                        "add_debuffs": [{"name": "Scent Mark (Faelynn)"}],
                        "remove_debuffs": []
                    }
                }]
            }
        }
        """,
        option_config=option_config,
    )

    actions = payload["planner"]["turns"]["1"]
    assert [action["name"] for action in actions] == [
        "Burst Fang",
        "Triple Maul",
        "Triple Maul (follow-up)",
        "Scent Trail",
        "Loyal Dash",
        "Pursuit Instinct I",
        "Pursuit Instinct II",
        "Pursuit Instinct III",
    ]
    assert actions[1]["stacks_of_hunt_tracking"] == 2
    assert actions[4]["stacks_of_hunt_tracking"] == 3
    assert actions[7]["stacks_of_hunt_tracking"] == 3
    assert [
        buff["name"] for buff in payload["baseline"]["attacker"]["buffs"]
    ] == ["Hunt Tracking (Faelynn)", "Roving Ferocity (Faelynn)"]
    assert (
        payload["baseline"]["target"]["debuffs"][0]["name"]
        == "Scent Trail (Faelynn)"
    )
    timeline_action = payload["timeline"]["actions"][0]
    assert timeline_action["action"]["name"] == "Pursuit Instinct I"
    assert timeline_action["action"]["stacks_of_hunt_tracking"] == 1
    assert [
        buff["name"] for buff in timeline_action["attacker"]["add_buffs"]
    ] == ["Hunt Tracking (Faelynn)", "Roving Ferocity (Faelynn)"]
    assert (
        timeline_action["target"]["add_debuffs"][0]["name"]
        == "Scent Trail (Faelynn)"
    )
