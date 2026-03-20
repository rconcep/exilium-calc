from typing import Any, Optional, Callable
from nicegui import ui


class SingleConfigurableItemEditor:
    """
    Reusable single-item editor widget:
    - Dropdown to choose item type (from option_config keys)
    - Shows editable fields directly in a card (no modal dialog)
    - One active configuration at a time
    - Uses the same option_config format as previous widgets
    """

    def __init__(
        self,
        option_config: dict[str, dict[str, Any]],
        title: str = "Configuration",
        subtitle: str = "Select type and edit settings below",
        selector_label: str = "Configuration Type",
        card_classes: str = "w-full max-w-2xl q-mt-md",
        save_callback: Optional[Callable[[dict], None]] = None,
    ):
        self.option_config = option_config
        self.default_config = option_config.get(
            "default",
            {
                "fields": [
                    {
                        "key": "comment",
                        "type": "textarea",
                        "label": "Notes",
                        "default": "",
                    }
                ]
            },
        )

        self.title = title
        self.subtitle = subtitle
        self.selector_label = selector_label
        self.card_classes = card_classes
        self.save_callback = save_callback

        # Current state
        self.current_type: Optional[str] = None
        self.current_data: dict[str, Any] = {}
        self.field_elements: dict[str, Any] = {}

        self._build_ui()

    def get_config(self, item_type: str) -> dict:
        return self.option_config.get(item_type, self.default_config)

    def reset_to_defaults(self, item_type: str):
        config = self.get_config(item_type)
        self.current_data = {"type": item_type}
        for field in config.get("fields", []):
            self.current_data[field["key"]] = field.get("default", "")
        self._refresh_form()

    def _refresh_form(self):
        """Update UI fields from current_data"""
        for key, element in self.field_elements.items():
            if key in self.current_data:
                element.value = self.current_data[key]

    def _save_current(self):
        """Collect values from UI elements into current_data"""
        for key, element in self.field_elements.items():
            self.current_data[key] = element.value

        if self.save_callback:
            self.save_callback(self.current_data.copy())

        # ui.notify(f'Saved {self.current_type} configuration', type='positive')

    def _on_type_change(self, e):
        new_type = e.value
        if new_type == self.current_type:
            return

        self.current_type = new_type
        self.reset_to_defaults(new_type)
        self.card.visible = bool(new_type)
        ui.notify(f"Switched to {new_type}")

    def _build_ui(self):
        if self.title != "":
            ui.label(self.title).classes("text-h5 q-mt-xl")
        if self.subtitle != "":
            ui.label(self.subtitle).classes("text-subtitle2 q-mb-md")

        # Type selector
        type_select = (
            ui.select(
                options=list(self.option_config.keys()),
                label=self.selector_label,
                value=None,
            )
            .classes("w-full")
            .props("outlined dense")
        )
        type_select.on_value_change(self._on_type_change)

        # Main card (hidden until type selected)
        self.card = ui.card().classes(self.card_classes).props("flat bordered")
        self.card.visible = False

        with self.card:
            ui.label().bind_text_from(
                self, "current_type", lambda t: f'{t or "Select a type"}'
            ).classes("text-h6")
            ui.separator()

            self.field_elements.clear()

            # We'll rebuild fields dynamically when type changes
            def rebuild_fields():
                # Clear previous fields
                self.card.clear()
                with self.card:
                    ui.label().bind_text_from(
                        self, "current_type", lambda t: f'{t or "Select a type"}'
                    ).classes("text-h6")
                    ui.separator()

                    self.field_elements.clear()

                    if not self.current_type:
                        return

                    config = self.get_config(self.current_type)

                    for field_def in config.get("fields", []):
                        key = field_def["key"]
                        ftype = field_def["type"]
                        label = field_def.get("label", key.capitalize())
                        value = self.current_data.get(key, field_def.get("default", ""))

                        if ftype == "textarea":
                            el = (
                                ui.textarea(
                                    label=label,
                                    value=value,
                                    placeholder=field_def.get("placeholder", ""),
                                )
                                .classes("w-full")
                                .props("autogrow outlined")
                            )
                        elif ftype == "select":
                            el = (
                                ui.select(
                                    options=field_def.get("options", []),
                                    label=label,
                                    value=value,
                                )
                                .classes("w-full")
                                .props("outlined dense")
                            )
                        elif ftype == "checkbox":
                            el = ui.checkbox(text=label, value=value).classes("w-full")
                        elif ftype == "number":
                            el = (
                                ui.number(label=label, value=value)
                                .classes("w-full")
                                .props("outlined dense")
                            )
                        else:
                            el = (
                                ui.input(label=label, value=value)
                                .classes("w-full")
                                .props("outlined dense")
                            )

                        self.field_elements[key] = el

                    with ui.row().classes("w-full justify-end gap-3 q-mt-lg"):
                        # ui.button('Reset to Defaults', on_click=lambda: self.reset_to_defaults(self.current_type))\
                        #     .props('flat color=negative')
                        ui.button("Calculate", on_click=self._save_current).props(
                            "color=primary unelevated"
                        )

            # Bind rebuild when type changes (after reset)
            type_select.on_value_change(lambda e: rebuild_fields())

    # Public API
    @property
    def data(self) -> Optional[dict]:
        """Get current configuration (after save)"""
        if not self.current_type:
            return None
        return self.current_data.copy()

    def set_data(self, data: dict):
        """Load existing configuration"""
        if not data or "type" not in data:
            return
        self.current_type = data["type"]
        self.current_data = data.copy()
        # Update dropdown
        # (assuming the select element is accessible - in real app you might store reference)
        # For simplicity we just reset form
        self._refresh_form()
        self.card.visible = True
        ui.notify(f"Loaded {self.current_type} configuration")
