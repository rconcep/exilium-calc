import copy
from typing import Any
from uuid import uuid4
from nicegui import ui
from nicegui.events import ClickEventArguments


class SelectableChipsEditor:
    """
    Reusable component:
    - Button to open selection dialog
    - Selected items appear as clickable/removable chips
    - Each chip opens a customizable edit dialog
    - Clear All button to remove everything
    """

    def __init__(
        self,
        options: list[str] | dict[str, str],
        option_config: dict[str, dict[str, Any]],
        allow_duplicates: bool = True,
        title: str = "Select options",
        button_text: str = "",
        clear_button_text: str = "",
        button_icon: str = "add_circle",
        clear_button_icon: str = "delete_sweep",
        # chip_icon: str = "",
        chip_color: str = "primary",
        container_classes: str = "w-full gap-2 wrap q-mt-md",
        on_change: Any | None = None,
    ):
        self.allow_duplicates = allow_duplicates
        self.title = title
        self.button_text = button_text
        self.clear_button_text = clear_button_text
        self.button_icon = button_icon
        self.clear_button_icon = clear_button_icon
        # self.chip_icon = chip_icon
        self.chip_color = chip_color
        self.on_change = on_change

        self.options = options
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

        self.selected_items: list[dict[str, Any]] = []
        self.container = ui.row().classes(f"{container_classes} exilium-chipbar")
        self.selector: ui.select

        self._build_ui()
        self.refresh_chips()

    def _notify_change(self) -> None:
        if callable(self.on_change):
            self.on_change()

    def _ensure_item_metadata(self, item: dict[str, Any]) -> dict[str, Any]:
        config = self.get_config(item["name"])
        item.setdefault("_instance_id", str(uuid4()))
        item.setdefault("_display_name", config.get("display_name", item["name"]))
        return item

    def get_config(self, option_name: str) -> dict:
        return self.option_config.get(option_name, self.default_config)

    def create_new_item(self, option_name: str) -> dict:
        config = self.get_config(option_name)
        item = {"name": option_name}
        for field in config.get("fields", []):
            item[field["key"]] = field.get("default", "")
        return self._ensure_item_metadata(item)

    def open_edit_dialog(self, item: dict):
        config = self.get_config(item["name"])

        with ui.dialog(value=True).props("persistent") as dialog, ui.card().classes(
            "w-96 max-w-full exilium-panel"
        ):
            ui.label(f'{item["name"]}').classes("text-h6")
            ui.separator()

            field_elements = {}

            for field_def in config.get("fields", []):
                key = field_def["key"]
                ftype = field_def["type"]
                label = field_def.get("label", key.capitalize())
                value = item.get(key, field_def.get("default", ""))

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

                field_elements[key] = el

            def save_and_close(e: ClickEventArguments):
                for key, element in field_elements.items():
                    item[key] = element.value
                self._ensure_item_metadata(item)
                dialog.close()
                self.refresh_chips()
                self._notify_change()
                with e.client:
                    ui.notify(f'Updated {item["name"]}')

            with ui.row().classes("w-full justify-end gap-2 q-mt-md"):
                ui.button("Cancel", on_click=dialog.close).props("flat color=negative")
                ui.button("Save", on_click=save_and_close).props("color=primary")

    def refresh_chips(self):
        self.container.clear()
        with self.container:
            ui.label(f"{self.title}:").classes("text-subtitle2")
            for item in self.selected_items:
                self._ensure_item_metadata(item)
                chip = ui.chip(
                    text=item.get("_display_name", item["name"]),
                    # icon=self.chip_icon,
                    color=self.chip_color,
                    removable=True,
                ).props("dense clickable")

                summary = []
                config = self.get_config(item["name"])
                for f in config.get("fields", []):
                    if f["key"] != "comment" and item.get(f["key"]) not in (
                        None,
                        "",
                        False,
                    ):
                        summary.append(f"{f.get('label', f['key'])}: {item[f['key']]}")
                tooltip_text = " • ".join(summary)
                if not tooltip_text and item.get("comment"):
                    tooltip_text = (
                        item["comment"][:80] + "..."
                        if len(item["comment"]) > 80
                        else item["comment"]
                    )
                if tooltip_text:
                    chip.tooltip(tooltip_text)

                chip.on("click", lambda e, it=item: self.open_edit_dialog(it))

                def remove_this(e, it=item):
                    self.selected_items.remove(it)
                    self.refresh_chips()
                    self._notify_change()
                    with e.client:
                        ui.notify(f'Removed {it["name"]}')

                chip.on("remove", remove_this)

    def add_option(self, option_text: str):
        # new_item = self.create_new_item(option_text)
        # self.selected_items.append(new_item)
        # self.refresh_chips()
        # ui.notify(f'Added: {option_text}', group=False)
        if self.allow_duplicates or (
            not any(it["name"] == option_text for it in self.selected_items)
        ):
            new_item = self.create_new_item(option_text)
            self.selected_items.append(new_item)
            self.refresh_chips()
            self._notify_change()
            ui.notify(f"Added: {option_text}")
        else:
            ui.notify(f"{option_text} already selected", type="warning")

    def clear_all(self):
        if not self.selected_items:
            ui.notify("Nothing to clear", type="info")
            return
        self.selected_items.clear()
        self.refresh_chips()
        self._notify_change()
        ui.notify(f"Cleared all {self.title.lower()}", type="positive")

    def set_options_and_config(
        self,
        options: list[str] | dict[str, str],
        option_config: dict[str, dict[str, Any]],
    ) -> None:
        self.options = options
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
        self.selector.options = options
        self.selector.update()

    def _build_ui(self):
        # Selection dialog
        with ui.dialog(value=False).props(
            "persistent"
        ) as self.select_dialog, self.select_dialog:
            with ui.card().classes("w-96 exilium-panel"):
                ui.label(self.title).classes("text-h6")
                ui.separator()

                self.selector = (
                    ui.select(
                        options=self.options,
                        with_input=True,
                        new_value_mode=None,
                        on_change=lambda e: [
                            self.add_option(e.value),
                            self.select_dialog.close(),
                        ],
                    )
                    .props("filled")
                    .classes("w-full")
                )

                # ui.button(
                # self.button_text,
                # on_click=[self.add_option(selector.value), self.select_dialog.close()],
                # icon=self.button_icon
                # ).props('unelevated color=primary')

                # with ui.grid(columns=5).classes('w-full gap-3'):
                #     for opt in self.options:
                #         ui.button(
                #             opt,
                #             on_click=lambda e, t=opt: [self.add_option(t), self.select_dialog.close()]
                #         ).props('no-caps color=primary stretch')

        # Control buttons row
        with ui.row().classes("items-center gap-3 q-mt-md"):
            ui.button(
                self.button_text,
                on_click=self.select_dialog.open,
                icon=self.button_icon,
            ).props("unelevated color=primary")

            ui.button(
                self.clear_button_text,
                on_click=self.clear_all,
                icon=self.clear_button_icon,
            ).props("unelevated color=negative outline")

    # Public API
    @property
    def data(self) -> list[dict]:
        return self.selected_items

    def clear(self):
        self.clear_all()

    def set_data(self, data: list[dict], notify: bool = True):
        self.selected_items = [
            self._ensure_item_metadata(copy.deepcopy(item)) for item in data
        ]
        self.refresh_chips()
        if notify:
            self._notify_change()
