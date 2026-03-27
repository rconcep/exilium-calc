from nicegui import ui

from gui.templates.selectable_chips_editor import SelectableChipsEditor
from typing import Any, Callable
from core.combat import DamageInstance


class RotationPlanner:
    """A tool for specifying Doll actions used for Rotation Analysis."""

    NUMBER_OF_TURNS: int = 7

    def __init__(self, options_config: dict[str, dict[str, Any]]):
        """
        Arguments:
        options_config -- data structure describing actions and their programmable fields
        """
        self.editors: dict[int, SelectableChipsEditor] = {}
        self.options_config: dict[str, dict[str, Any]] = options_config

        with ui.scroll_area().classes("w-full h-full"):
            for t in range(1, 1 + RotationPlanner.NUMBER_OF_TURNS):
                self.editors[t] = SelectableChipsEditor(
                    title=f"T{t}",
                    options=list(self.options_config.keys()),
                    option_config=self.options_config,
                )

                # Optional: debug views
                # with ui.expansion('Actions').classes('q-mt-md'):
                #     ui.label().bind_text_from(self.editors[t], 'data', backward=lambda v: f"{v}")
                ui.separator()

    def get_all_actions(self) -> list[DamageInstance]:
        """Returns a collection of all of the actions specified in the element."""
        all_combined_actions: list[DamageInstance] = []

        for turn_editor in self.editors.values():
            for chip in turn_editor.data:
                keyword_args: dict[str, Any] = {}
                chip_function: Callable = self.options_config[chip["name"]]["function"]

                for field in self.options_config[chip["name"]]["fields"]:
                    field_name: str = field["key"]
                    field_value: int = chip[field_name]
                    keyword_args[field_name] = field_value

                di: DamageInstance = chip_function(**keyword_args)
                all_combined_actions.append(di)

        return all_combined_actions

    def set_data(self, data: dict[int, list[dict]]):
        """Sets the data in the turn editors directly, e.g., for pre-populating a rotation."""
        for t, v in data.items():
            self.editors[t].set_data(v)

    def set_options_config(self, options_config: dict[str, dict[str, Any]]) -> None:
        """Sets the options config such as when changing Action implementations."""
        self.options_config = options_config
