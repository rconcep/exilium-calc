from __future__ import annotations

from gui.templates.rotation_simulator import RotationSimulator


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
