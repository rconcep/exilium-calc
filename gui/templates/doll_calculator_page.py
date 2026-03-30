from nicegui import events, ui

import copy
import inspect
from typing import final, Any
from abc import ABC, abstractmethod
from dataclasses import asdict
from decimal import Decimal, ROUND_DOWN
from pydantic import BaseModel

from core.types import *
from core.stat_serializer import SerializationError, StatsSerializer
from core.combat import DamageInstance, sum_damage_instances
from gui.templates.rotation_planner import RotationPlanner
from gui.styles.descriptions import get_tag_description, get_stat_description
from gui.styles.graphs import get_bar_chart_template, get_donut_chart_template


class ModelAssumption(BaseModel):
    """Typed model for the assumptions list shown in each Doll page."""

    icon: str = "info"
    description: str
    link_label: str | None = None
    link_target: str | None = None


class DollCalculatorPage(ABC):
    """Template for each Doll's page."""

    actions_table_columns: list[dict] = [
        {
            "name": "action",
            "label": "Action",
            "field": "label",
            "required": True,
            "align": "left",
        },
        # {'name': 'tags', 'label': 'Tags', 'field': 'tags', 'required': True, 'align': 'left'},
        {
            "name": "potency",
            "label": "Potency",
            "field": "base_potency",
            "sortable": False,
        },
        {
            "name": "potency_adjusted",
            "label": "Potency (Effective)",
            "field": "adjusted_potency",
            "sortable": False,
        },
    ]

    damage_type_breakdown_table_columns: list[dict] = [
        {
            "name": "tag",
            "label": "Damage Type",
            "field": "tag",
            "required": True,
            "align": "left",
        },
        {"name": "share", "label": "%", "field": "share", "sortable": False},
    ]

    conditional_basic_stats_to_show: tuple[StatType, ...] = (
        StatType.ATTACK,
        StatType.CRIT_RATE,
    )

    def __init__(self):
        # Basic Tab
        self.initial_stats_number_inputs: dict[StatType, ui.number] = {}

        # Special Tab
        self.initial_conditional_stat_number_inputs: dict[
            StatType, dict[DamageTag, ui.number]
        ] = {stat: {} for stat in StatType}
        self.damage_boost_number_inputs: dict[DamageTag, ui.number] = {}
        self.critical_damage_number_inputs: dict[DamageTag, ui.number] = {}
        self.defense_ignore_number_inputs: dict[DamageTag, ui.number] = {}

        # Additive Modifier Tab
        self.additive_stat_modifier_number_inputs: dict[StatType, ui.number] = {}
        self.additive_conditional_stat_modifier_number_inputs: dict[
            StatType, dict[DamageTag, ui.number]
        ] = {stat: {} for stat in StatType}
        self.additive_mod_damage_boost_number_inputs: dict[DamageTag, ui.number] = {}
        self.additive_mod_critical_damage_number_inputs: dict[DamageTag, ui.number] = {}
        self.additive_mod_defense_ignore_number_inputs: dict[DamageTag, ui.number] = {}

        # Multiplicative Modifier Tab
        self.multiplicative_stat_modifier_number_inputs: dict[StatType, ui.number] = {}
        self.multiplicative_conditional_stat_modifier_number_inputs: dict[
            StatType, dict[DamageTag, ui.number]
        ] = {stat: {} for stat in StatType}
        self.multiplicative_mod_damage_boost_number_inputs: dict[
            DamageTag, ui.number
        ] = {}
        self.multiplicative_mod_critical_damage_number_inputs: dict[
            DamageTag, ui.number
        ] = {}
        self.multiplicative_mod_defense_ignore_number_inputs: dict[
            DamageTag, ui.number
        ] = {}

        self.damage_instances: list[DamageInstance] = []
        self.option_config: Dict[str, Dict[str, Any]] = dict()
        self.rotation_planner: RotationPlanner
        self.doll: Doll
        self.doll_subtitle: str
        self.dandegate_link: str
        self.doll_portrait: str = "resources/dinergate.png"
        self.relevant_damage_tags: list[DamageTag]

        self.potency_bar_chart_data: dict = get_bar_chart_template()
        self.potency_bar_chart_data["data"][0]["x"] = ["Base", "Effective"]
        self.potency_bar_chart_plot: ui.plotly
        self.ability_donut_chart: dict = get_donut_chart_template()
        self.damage_type_breakdown_table: ui.table
        self.actions_table_data: list[dict] = []
        self.actions_table: ui.table

    def doll_header(self) -> None:
        """Generates the Doll description."""
        ui.page_title(f"Exilium-Calc: {self.doll.name}")
        ui.markdown(
            f"""
            # {self.doll.name}
            {self.doll_subtitle}

            [Dandegate]({self.dandegate_link})
        """
        ).classes("exilium-character-copy")

    @abstractmethod
    def get_model_assumptions(self) -> list[ModelAssumption]:
        """Returns model assumptions shown in the left panel.

        Each item may provide:
        - icon: icon name for the avatar section
        - description: short assumption description
        - link_label: optional link text
        - link_target: optional external URL
        """
        ...

    def render_model_assumptions(self) -> None:
        """Renders model assumptions as a list with icon, description, and optional link."""
        assumptions = self.get_model_assumptions()

        with ui.list().props("bordered dense separator").classes("w-full"):
            ui.item_label("Model Assumptions").props("header").classes("text-bold")
            ui.separator()

            if not assumptions:
                with ui.item():
                    with ui.item_section().props("avatar"):
                        ui.icon("block")
                    with ui.item_section():
                        ui.item_label("None").props("no-wrap")
                return

            for assumption in assumptions:
                with ui.item():
                    with ui.item_section().props("avatar"):
                        ui.icon(assumption.icon)
                    with ui.item_section():
                        ui.item_label(assumption.description).props("no-wrap")
                    if assumption.link_target:
                        with ui.item_section().props("side"):
                            ui.link(
                                assumption.link_label or "Link",
                                target=assumption.link_target,
                                new_tab=True,
                            )

    @abstractmethod
    def get_rotation_planner(self) -> None:
        """Generates the Rotation Planner section."""
        ...

    def get_rotation_analysis(self) -> None:
        """Generates the Rotation Analysis section."""
        with ui.grid(columns="50% auto").classes("w-full h-150"):
            self.actions_table = ui.table(
                columns=DollCalculatorPage.actions_table_columns,
                rows=self.actions_table_data,
                row_key="action",
                pagination={
                    "rowsPerPage": 5,
                },
            ).classes("exilium-data-table")
            self.potency_bar_chart_plot = ui.plotly(
                self.potency_bar_chart_data
            ).classes("w-full h-100 exilium-plot")
            self.damage_type_breakdown_table = ui.table(
                columns=DollCalculatorPage.damage_type_breakdown_table_columns,
                rows=[],
                pagination={"rowsPerPage": 5, "sortBy": "share", "descending": True},
            ).classes("exilium-data-table")
            self.donut_chart_plot_3 = ui.plotly(self.ability_donut_chart).classes(
                "w-full h-80 exilium-plot"
            )

            self.update_potency_bar_chart()
            self.update_ability_breakdown_donut_chart()
            self.update_damage_type_breakdown_table()

    def stats_update_callback(self, update: ui.number) -> None:
        """Updates elements when Doll stats are modified."""
        for di in self.damage_instances:
            di.damage_calculation_strategy.do_adjust_potency(
                attacker=copy.deepcopy(self.doll),
                target=Unit(stats=StatSheet(basic_attributes={StatType.DEFENSE: -1})),
                damage_instance=di,
            )

        self.update_actions_table()
        self.update_potency_bar_chart()
        self.update_ability_breakdown_donut_chart()
        self.update_damage_type_breakdown_table()

    @abstractmethod
    def update_doll_abilities(self) -> None:
        """Update self.option_config references to Doll ability functions."""
        ...

    def doll_fortification_callback(self, update: ui.select) -> None:
        """Updates Doll abilities upon changing Fortification level."""
        self.doll.set_fortification_level(FortificationLevel(update.value))
        ui.notify(f"Changed fortification to V{update.value}", group=False)
        self.update_doll_abilities()
        self.rotation_planner.set_options_config(self.option_config)

        for di in self.damage_instances:
            di.damage_calculation_strategy.do_adjust_potency(
                attacker=copy.deepcopy(self.doll),
                target=Unit(stats=StatSheet(basic_attributes={StatType.DEFENSE: -1})),
                damage_instance=di,
            )

        self.actions_table_data: list[dict] = [
            {
                "label": di.label,
                "base_potency": di.base_potency,
                "adjusted_potency": di.adjusted_potency,
            }
            for di in self.damage_instances
        ]
        self.stats_update_callback(None)

    def export_stats_json(self) -> str:
        """Serialize the current doll stats to a JSON string."""
        return StatsSerializer.save_to_string(self.doll, doll_name=self.doll.name)

    def export_stats_filename(self) -> str:
        """Build a safe default filename for exported stats."""
        safe_name = "".join(
            character.lower() if character.isalnum() else "_"
            for character in self.doll.name.strip()
        ).strip("_")
        return f"{safe_name or 'doll'}_stats.json"

    def import_stats_from_unit(self, loaded: Unit) -> None:
        """Copy stats from a deserialized Unit into self.doll in-place.

        Mutates the existing dicts so that all bound UI inputs stay valid
        and automatically reflect the new values.
        """
        # Basic attributes
        for stat in StatType:
            self.doll.initial_stats.basic_attributes[stat] = (
                loaded.initial_stats.basic_attributes.get(stat, 0)
            )
            self.doll.additive_modifiers.basic_attributes[stat] = (
                loaded.additive_modifiers.basic_attributes.get(stat, 0)
            )
            self.doll.multiplicative_modifiers.basic_attributes[stat] = (
                loaded.multiplicative_modifiers.basic_attributes.get(stat, 0)
            )

            for tag in DamageTag:
                self.doll.initial_stats.conditional_basic_attributes[stat].multipliers[
                    tag
                ] = loaded.initial_stats.conditional_basic_attributes[
                    stat
                ].multipliers.get(
                    tag, 0
                )
                self.doll.additive_modifiers.conditional_basic_attributes[
                    stat
                ].multipliers[
                    tag
                ] = loaded.additive_modifiers.conditional_basic_attributes[
                    stat
                ].multipliers.get(
                    tag, 0
                )
                self.doll.multiplicative_modifiers.conditional_basic_attributes[
                    stat
                ].multipliers[
                    tag
                ] = loaded.multiplicative_modifiers.conditional_basic_attributes[
                    stat
                ].multipliers.get(
                    tag, 0
                )

        # Special attributes (all tags)
        for attr in SpecialAttribute:
            for tag in DamageTag:
                self.doll.initial_stats.special_attributes[attr].multipliers[tag] = (
                    loaded.initial_stats.special_attributes[attr].multipliers.get(
                        tag, 0
                    )
                )
                self.doll.additive_modifiers.special_attributes[attr].multipliers[
                    tag
                ] = loaded.additive_modifiers.special_attributes[attr].multipliers.get(
                    tag, 0
                )
                self.doll.multiplicative_modifiers.special_attributes[attr].multipliers[
                    tag
                ] = loaded.multiplicative_modifiers.special_attributes[
                    attr
                ].multipliers.get(
                    tag, 0
                )

    def rebind_doll(self) -> None:
        """Binds UI elements to new Doll's stats."""
        for stat in StatType:
            self.initial_stats_number_inputs[stat].bind_value(
                self.doll.initial_stats.basic_attributes, stat
            )
            self.initial_stats_number_inputs[stat].on(
                "change", self.stats_update_callback
            )

            self.additive_stat_modifier_number_inputs[stat].bind_value(
                self.doll.additive_modifiers.basic_attributes, stat
            )
            self.additive_stat_modifier_number_inputs[stat].on(
                "change", self.stats_update_callback
            )

            self.multiplicative_stat_modifier_number_inputs[stat].bind_value(
                self.doll.multiplicative_modifiers.basic_attributes, stat
            )
            self.multiplicative_stat_modifier_number_inputs[stat].on(
                "change", self.stats_update_callback
            )

        for stat in self.conditional_basic_stats_to_show:
            for tag in self.relevant_damage_tags:
                self.initial_conditional_stat_number_inputs[stat][tag].bind_value(
                    self.doll.initial_stats.conditional_basic_attributes[
                        stat
                    ].multipliers,
                    tag,
                )
                self.initial_conditional_stat_number_inputs[stat][tag].on(
                    "change", self.stats_update_callback
                )

                self.additive_conditional_stat_modifier_number_inputs[stat][
                    tag
                ].bind_value(
                    self.doll.additive_modifiers.conditional_basic_attributes[
                        stat
                    ].multipliers,
                    tag,
                )
                self.additive_conditional_stat_modifier_number_inputs[stat][tag].on(
                    "change", self.stats_update_callback
                )

                self.multiplicative_conditional_stat_modifier_number_inputs[stat][
                    tag
                ].bind_value(
                    self.doll.multiplicative_modifiers.conditional_basic_attributes[
                        stat
                    ].multipliers,
                    tag,
                )
                self.multiplicative_conditional_stat_modifier_number_inputs[stat][
                    tag
                ].on("change", self.stats_update_callback)

        for tag in self.relevant_damage_tags:
            self.damage_boost_number_inputs[tag].bind_value(
                self.doll.initial_stats.special_attributes[
                    SpecialAttribute.DAMAGE_BOOST
                ].multipliers,
                tag,
            )
            self.damage_boost_number_inputs[tag].on(
                "change", self.stats_update_callback
            )

            self.critical_damage_number_inputs[tag].bind_value(
                self.doll.initial_stats.special_attributes[
                    SpecialAttribute.CRITICAL_DAMAGE
                ].multipliers,
                tag,
            )
            self.critical_damage_number_inputs[tag].on(
                "change", self.stats_update_callback
            )

            self.defense_ignore_number_inputs[tag].bind_value(
                self.doll.initial_stats.special_attributes[
                    SpecialAttribute.DEFENSE_IGNORE
                ].multipliers,
                tag,
            )
            self.defense_ignore_number_inputs[tag].on(
                "change", self.stats_update_callback
            )

            self.additive_mod_damage_boost_number_inputs[tag].bind_value(
                self.doll.additive_modifiers.special_attributes[
                    SpecialAttribute.DAMAGE_BOOST
                ].multipliers,
                tag,
            )
            self.additive_mod_damage_boost_number_inputs[tag].on(
                "change", self.stats_update_callback
            )

            self.additive_mod_critical_damage_number_inputs[tag].bind_value(
                self.doll.additive_modifiers.special_attributes[
                    SpecialAttribute.CRITICAL_DAMAGE
                ].multipliers,
                tag,
            )
            self.additive_mod_critical_damage_number_inputs[tag].on(
                "change", self.stats_update_callback
            )

            self.additive_mod_defense_ignore_number_inputs[tag].bind_value(
                self.doll.additive_modifiers.special_attributes[
                    SpecialAttribute.DEFENSE_IGNORE
                ].multipliers,
                tag,
            )
            self.additive_mod_defense_ignore_number_inputs[tag].on(
                "change", self.stats_update_callback
            )

            self.multiplicative_mod_damage_boost_number_inputs[tag].bind_value(
                self.doll.multiplicative_modifiers.special_attributes[
                    SpecialAttribute.DAMAGE_BOOST
                ].multipliers,
                tag,
            )
            self.multiplicative_mod_damage_boost_number_inputs[tag].on(
                "change", self.stats_update_callback
            )

            self.multiplicative_mod_critical_damage_number_inputs[tag].bind_value(
                self.doll.multiplicative_modifiers.special_attributes[
                    SpecialAttribute.CRITICAL_DAMAGE
                ].multipliers,
                tag,
            )
            self.multiplicative_mod_critical_damage_number_inputs[tag].on(
                "change", self.stats_update_callback
            )

            self.multiplicative_mod_defense_ignore_number_inputs[tag].bind_value(
                self.doll.multiplicative_modifiers.special_attributes[
                    SpecialAttribute.DEFENSE_IGNORE
                ].multipliers,
                tag,
            )
            self.multiplicative_mod_defense_ignore_number_inputs[tag].on(
                "change", self.stats_update_callback
            )

    @abstractmethod
    def set_initial_values(self) -> None:
        """Initializes Doll's stats to specified values."""
        ...

    def update_actions_table(self) -> None:
        """Updates the Actions Table."""
        new_rows = [
            {
                "label": di.label,
                "base_potency": di.base_potency,
                "adjusted_potency": di.adjusted_potency,
            }
            for di in self.damage_instances
        ]

        for row in new_rows:
            row["adjusted_potency"] = Decimal(row["adjusted_potency"]).quantize(
                Decimal("0.01"), rounding=ROUND_DOWN
            )

        self.actions_table.rows[:] = new_rows
        self.actions_table.update()

    def update_potency_bar_chart(self) -> None:
        """Updates the bar chart showing potencies."""
        y = [
            sum([skill.base_potency for skill in self.damage_instances]),
            sum([skill.adjusted_potency for skill in self.damage_instances]),
        ]

        self.potency_bar_chart_data["data"][0]["y"] = y
        self.potency_bar_chart_data["data"][0]["text"] = [
            str(Decimal(val).quantize(Decimal("0.01"), rounding=ROUND_DOWN))
            for val in y
        ]

        ui.update(self.potency_bar_chart_plot)

    def update_ability_breakdown_donut_chart(self) -> None:
        """Updates the donut chart breaking down damage by label."""
        grouped_damage_instances: dict[str, DamageInstance] = dict()

        for di in self.damage_instances:
            grouped_damage_instances.setdefault(
                di.group_name, DamageInstance(label="", base_potency=0)
            )
            grouped_damage_instances[di.group_name].base_potency += di.base_potency
            grouped_damage_instances[
                di.group_name
            ].adjusted_potency += di.adjusted_potency

        labels: list[str] = list(grouped_damage_instances.keys())
        vals: list[float] = [
            x.adjusted_potency for x in grouped_damage_instances.values()
        ]

        self.ability_donut_chart["data"][0]["labels"] = labels
        self.ability_donut_chart["data"][0]["values"] = vals

        ui.update(self.donut_chart_plot_3)

    def update_damage_type_breakdown_table(self) -> None:
        """Updates the table breaking down damage by tag."""
        new_rows: list[dict[str, Any]] = [
            {
                "label": sum_damage_instances(self.damage_instances, tag).label,
                "base_potency": sum_damage_instances(
                    self.damage_instances, tag
                ).base_potency,
                "adjusted_potency": sum_damage_instances(
                    self.damage_instances, tag
                ).adjusted_potency,
                "tags": sum_damage_instances(self.damage_instances, tag).tags,
            }
            for tag in DamageTag
        ]

        total_adjusted_potency: float = sum(
            [skill.adjusted_potency for skill in self.damage_instances]
        )
        for row in new_rows:
            row["tag"] = next(iter(row["tags"]))
            row["tags"] = ""
            row["share"] = (
                (row["adjusted_potency"] / total_adjusted_potency * 100)
                if total_adjusted_potency != 0
                else 0
            )
            row["share"] = Decimal(row["share"]).quantize(
                Decimal("0.1"), rounding=ROUND_DOWN
            )

        self.damage_type_breakdown_table.rows[:] = new_rows
        self.damage_type_breakdown_table.update()

    @final
    def get_page(self) -> None:
        """Generates the Doll Calculator Page instance."""
        self.relevant_damage_tags = [
            tag for tag in DamageTag if tag not in self.doll.irrelevant_damage_tags
        ]

        with ui.row().classes("w-full exilium-dashboard"):
            with ui.card().classes("w-100 h-150 exilium-panel"):
                self.doll_header()
                with ui.scroll_area().classes("w-full h-full"):
                    self.render_model_assumptions()

                with ui.grid(columns="75% auto").classes("w-full gap-0"):
                    ui.select(
                        {
                            0: "Segment 00",
                            1: "Segment 01",
                            2: "Segment 02",
                            3: "Segment 03",
                            4: "Segment 04",
                            5: "Segment 05",
                            6: "Segment 06",
                        },
                        value=6,
                        label="Fortification",
                        multiple=False,
                        on_change=self.doll_fortification_callback,  # type: ignore
                    ).props("outlined")

            with ui.card().classes("w-75 h-150 exilium-panel exilium-portrait-panel"):
                ui.image(self.doll_portrait)

            with ui.card().classes("w-160 h-150 exilium-panel"):
                with ui.tabs().classes("w-full exilium-top-tabs") as tabs:
                    basic_stats_tab = ui.tab("Basic").tooltip(
                        "Initial values of basic stats as seen in Refitting Room or Formation."
                    )
                    special_stats_tab = ui.tab("Special").tooltip(
                        "Conditionally applied stats from innate abilities."
                    )
                    additive_mods_tab = ui.tab("Additive").tooltip(
                        '"Additive" modifiers from non-innate sources.'
                    )
                    multiplicative_mods_tab = ui.tab("Multiplicative").tooltip(
                        '"Multiplicative" modifiers from non-innate sources.'
                    )
                    save_load_tab = ui.tab("Load/Save").tooltip(
                        "Export a snapshot of the current stats or import from a file."
                    )
                with ui.tab_panels(tabs, value=basic_stats_tab).classes(
                    "w-full h-full exilium-tab-panels"
                ):
                    with ui.tab_panel(basic_stats_tab):
                        with ui.scroll_area().classes("w-full h-full"):
                            with ui.list().props("bordered dense separator").classes(
                                "w-full"
                            ):
                                ui.item_label(
                                    "Initial Values (Refitting Room/Formation)"
                                ).props("header").classes("text-bold")
                                ui.separator()
                                for stat in StatType:
                                    with ui.item():
                                        with ui.item_section().props("no-wrap"):
                                            ui.item_label(stat)
                                            ui.item_label(
                                                get_stat_description(stat)
                                            ).props("caption")
                                        with ui.item_section().props("side"):
                                            self.initial_stats_number_inputs[stat] = (
                                                ui.number(value=0, min=0, precision=2)
                                            )

                    with ui.tab_panel(special_stats_tab):
                        with ui.scroll_area().classes("w-full h-full"):
                            with ui.expansion(
                                text="Help",
                                icon="info",
                            ).classes("w-full"):
                                ui.label(
                                    """Put additive modifiers from innate abilities here.
                                    Expect these to be pre-populated and to dynamically
                                    change based on Fortification level and other factors.
                                    """
                                )
                                ui.label(
                                    """Prefer to use the 'Additive Mods' tab for that reason."""
                                ).classes("italic")
                                with ui.list().props("bordered dense separator"):
                                    ui.item_label("Examples").props("header").classes(
                                        "text-bold"
                                    )
                                    ui.separator()
                                    with ui.item():
                                        with ui.item_section():
                                            ui.item_label("Fixed Key")
                                        with ui.item_section():
                                            ui.item_label(
                                                "Leva Fixed Key 2 - Fox's Smile"
                                            ).props("caption")
                                        with ui.item_section():
                                            ui.item_label(
                                                "Damage dealt to enemy units in Stability Break is increased by 7%."
                                            ).props("caption")
                                    with ui.item():
                                        with ui.item_section():
                                            ui.item_label("Expansion Key")
                                        with ui.item_section():
                                            ui.item_label(
                                                "Leva Expansion Key - Electric Espionage"
                                            ).props("caption")
                                        with ui.item_section():
                                            ui.item_label(
                                                """"At the start of battle, Electric damage dealt by Leva
                                                is increased by 2% [...] for each Electric attributed
                                                Doll on the battlefield."""
                                            ).props("caption")
                                    with ui.item():
                                        with ui.item_section():
                                            ui.item_label("Passive Ability")
                                        with ui.item_section():
                                            ui.item_label("Fox's Scheme (Leva)").props(
                                                "caption"
                                            )
                                        with ui.item_section():
                                            ui.item_label(
                                                """If Leva has Positive Charge, Electric damage dealt 
                                                is increased by 10%."""
                                            ).props("caption")

                            ui.separator()

                            with ui.expansion(
                                text="Basic (Conditional)",
                                group="doll_stats",
                            ).classes("w-full"):
                                for stat in self.conditional_basic_stats_to_show:
                                    with ui.expansion(
                                        text=str(stat),
                                        group="initial_conditional_basic_stats",
                                    ).classes("w-full"):
                                        with ui.list().props(
                                            "bordered dense separator"
                                        ).classes("w-full"):
                                            for tag in self.relevant_damage_tags:
                                                with ui.item():
                                                    with ui.item_section().props(
                                                        "no-wrap"
                                                    ):
                                                        ui.item_label(tag)
                                                        ui.item_label(
                                                            get_tag_description(tag)
                                                        ).props("caption")
                                                    with ui.item_section().props(
                                                        "side"
                                                    ):
                                                        self.initial_conditional_stat_number_inputs[
                                                            stat
                                                        ][
                                                            tag
                                                        ] = ui.number(
                                                            value=0,
                                                            min=0,
                                                            suffix="%",
                                                            precision=1,
                                                            format="%.1f",
                                                        )

                            with ui.expansion(
                                text="Damage Boost (Increased Damage)",
                                group="doll_stats",
                            ).classes("w-full"):
                                with ui.list().props(
                                    "bordered dense separator"
                                ).classes("w-full"):
                                    for tag in self.relevant_damage_tags:
                                        with ui.item():
                                            with ui.item_section().props("no-wrap"):
                                                ui.item_label(tag)
                                                ui.item_label(
                                                    get_tag_description(tag)
                                                ).props("caption")
                                            with ui.item_section().props("side"):
                                                self.damage_boost_number_inputs[tag] = (
                                                    ui.number(
                                                        value=0,
                                                        min=0,
                                                        suffix="%",
                                                        precision=1,
                                                        format="%.1f",
                                                    )
                                                )

                            with ui.expansion(
                                text="Critical Damage", group="doll_stats"
                            ).classes("w-full"):
                                with ui.list().props(
                                    "bordered dense separator"
                                ).classes("w-full"):
                                    for tag in self.relevant_damage_tags:
                                        with ui.item():
                                            with ui.item_section().props("no-wrap"):
                                                ui.item_label(tag)
                                                ui.item_label(
                                                    get_tag_description(tag)
                                                ).props("caption")
                                            with ui.item_section().props("side"):
                                                self.critical_damage_number_inputs[
                                                    tag
                                                ] = ui.number(
                                                    value=0,
                                                    min=0,
                                                    suffix="%",
                                                    precision=1,
                                                    format="%.1f",
                                                )

                            with ui.expansion(
                                text="Defense Ignore", group="doll_stats"
                            ).classes("w-full"):
                                with ui.list().props(
                                    "bordered dense separator"
                                ).classes("w-full"):
                                    for tag in self.relevant_damage_tags:
                                        with ui.item():
                                            with ui.item_section().props("no-wrap"):
                                                ui.item_label(tag)
                                                ui.item_label(
                                                    get_tag_description(tag)
                                                ).props("caption")
                                            with ui.item_section().props("side"):
                                                self.defense_ignore_number_inputs[
                                                    tag
                                                ] = ui.number(
                                                    value=0,
                                                    min=0,
                                                    suffix="%",
                                                    precision=1,
                                                    format="%.1f",
                                                )

                    with ui.tab_panel(additive_mods_tab):
                        with ui.scroll_area().classes("w-full h-full"):
                            with ui.expansion(
                                text="Help",
                                icon="info",
                            ).classes("w-full"):
                                ui.label(
                                    """Put additive modifiers from keys, attachment set 
                                        bonuses, remolding core, and in-combat buffs here."""
                                )
                                ui.label(
                                    """Note: Since these mods are additive with the Special tab,
                                        it technically doesn't matter if they are put here or 
                                        in the Special tab, but the values in the Special
                                        tab are subject to dynamically change (e.g., when changing
                                        Fortification Level)."""
                                ).classes("text-caption exilium-subtle")
                                with ui.list().props("bordered dense separator"):
                                    ui.item_label("Examples").props("header").classes(
                                        "text-bold"
                                    )
                                    ui.separator()
                                    with ui.item():
                                        with ui.item_section():
                                            ui.item_label("Attachment Set")
                                        with ui.item_section():
                                            ui.item_label("Electric Boost").props(
                                                "caption"
                                            )
                                        with ui.item_section():
                                            ui.item_label(
                                                "When dealing Electric damage, the damage is increased by 20%."
                                            ).props("caption")
                                    with ui.item():
                                        with ui.item_section():
                                            ui.item_label("Weapon")
                                        with ui.item_section():
                                            ui.item_label("Leaping Tiger").props(
                                                "caption"
                                            )
                                        with ui.item_section():
                                            ui.item_label(
                                                "Phase damage dealt is increased by 10%. [...]."
                                            ).props("caption")
                                    with ui.item():
                                        with ui.item_section():
                                            ui.item_label("Common Key")
                                        with ui.item_section():
                                            ui.item_label(
                                                "Common Key - Endless Night"
                                            ).props("caption")
                                        with ui.item_section():
                                            ui.item_label(
                                                "When attacking enemies with debuffs, phase damage dealt is increased by 10%."
                                            ).props("caption")
                                    with ui.item():
                                        with ui.item_section():
                                            ui.item_label("Food buff")
                                        with ui.item_section():
                                            ui.item_label("Condiment: Rose Salt").props(
                                                "caption"
                                            )
                                        with ui.item_section():
                                            ui.item_label(
                                                "Attack is increased by 20 points."
                                            ).props("caption")
                                    with ui.item():
                                        with ui.item_section():
                                            ui.item_label("Remolding Core Imagoform")
                                        with ui.item_section():
                                            ui.item_label("Sprout (Jiangyu)").props(
                                                "caption"
                                            )
                                        with ui.item_section():
                                            ui.item_label(
                                                "Electric damage dealt is increased by 5%."
                                            ).props("caption")
                                    with ui.item():
                                        with ui.item_section():
                                            ui.item_label(
                                                "Remolding Core Specialized Trait"
                                            )
                                        with ui.item_section():
                                            ui.item_label(
                                                "Smite Boost (Vanguard)"
                                            ).props("caption")
                                        with ui.item_section():
                                            ui.item_label(
                                                "Critical damage is increased by 2.4%."
                                            ).props("caption")
                                    with ui.item():
                                        with ui.item_section():
                                            ui.item_label(
                                                "Remolding Core Specialized Trait"
                                            )
                                        with ui.item_section():
                                            ui.item_label(
                                                "Freeze Boost (Sentinel)"
                                            ).props("caption")
                                        with ui.item_section():
                                            ui.item_label(
                                                "Freeze damage dealt is increased by 1.4%."
                                            ).props("caption")

                            ui.separator()

                            with ui.expansion(
                                text="Basic",
                                group="additive_mods",
                            ).classes("w-full"):
                                with ui.list().props(
                                    "bordered dense separator"
                                ).classes("w-full"):
                                    for stat in StatType:
                                        with ui.item():
                                            with ui.item_section().props("no-wrap"):
                                                ui.item_label(stat)
                                                ui.item_label(
                                                    get_stat_description(stat)
                                                ).props("caption")
                                            with ui.item_section().props("side"):
                                                self.additive_stat_modifier_number_inputs[
                                                    stat
                                                ] = ui.number(
                                                    value=0,
                                                    min=0,
                                                    precision=1,
                                                    format="%.1f",
                                                )
                            with ui.expansion(
                                text="Basic (Conditional)",
                                group="additive_mods",
                            ).classes("w-full"):
                                for stat in self.conditional_basic_stats_to_show:
                                    with ui.expansion(
                                        text=str(stat),
                                        group="additive_conditional_basic_mods",
                                    ).classes("w-full"):
                                        with ui.list().props(
                                            "bordered dense separator"
                                        ).classes("w-full"):
                                            for tag in self.relevant_damage_tags:
                                                with ui.item():
                                                    with ui.item_section().props(
                                                        "no-wrap"
                                                    ):
                                                        ui.item_label(tag)
                                                        ui.item_label(
                                                            get_tag_description(tag)
                                                        ).props("caption")
                                                    with ui.item_section().props(
                                                        "side"
                                                    ):
                                                        self.additive_conditional_stat_modifier_number_inputs[
                                                            stat
                                                        ][
                                                            tag
                                                        ] = ui.number(
                                                            value=0,
                                                            min=0,
                                                            precision=1,
                                                            format="%.1f",
                                                        )

                            with ui.expansion(
                                text="Damage Boost (Increased Damage)",
                                group="additive_mods",
                            ).classes("w-full"):
                                with ui.list().props(
                                    "bordered dense separator"
                                ).classes("w-full"):
                                    for tag in self.relevant_damage_tags:
                                        with ui.item():
                                            with ui.item_section().props("no-wrap"):
                                                ui.item_label(tag)
                                                ui.item_label(
                                                    get_tag_description(tag)
                                                ).props("caption")
                                            with ui.item_section().props("side"):
                                                self.additive_mod_damage_boost_number_inputs[
                                                    tag
                                                ] = ui.number(
                                                    value=0,
                                                    min=0,
                                                    suffix="%",
                                                    precision=1,
                                                    format="%.1f",
                                                )

                            with ui.expansion(
                                text="Critical Damage", group="additive_mods"
                            ).classes("w-full"):
                                with ui.list().props(
                                    "bordered dense separator"
                                ).classes("w-full"):
                                    for tag in self.relevant_damage_tags:
                                        with ui.item():
                                            with ui.item_section().props("no-wrap"):
                                                ui.item_label(tag)
                                                ui.item_label(
                                                    get_tag_description(tag)
                                                ).props("caption")
                                            with ui.item_section().props("side"):
                                                self.additive_mod_critical_damage_number_inputs[
                                                    tag
                                                ] = ui.number(
                                                    value=0,
                                                    min=0,
                                                    suffix="%",
                                                    precision=1,
                                                    format="%.1f",
                                                )

                            with ui.expansion(
                                text="Defense Ignore", group="additive_mods"
                            ).classes("w-full"):
                                with ui.list().props(
                                    "bordered dense separator"
                                ).classes("w-full"):
                                    for tag in self.relevant_damage_tags:
                                        with ui.item():
                                            with ui.item_section().props("no-wrap"):
                                                ui.item_label(tag)
                                                ui.item_label(
                                                    get_tag_description(tag)
                                                ).props("caption")
                                            with ui.item_section().props("side"):
                                                self.additive_mod_defense_ignore_number_inputs[
                                                    tag
                                                ] = ui.number(
                                                    value=0,
                                                    min=0,
                                                    suffix="%",
                                                    precision=1,
                                                    format="%.1f",
                                                )

                    with ui.tab_panel(multiplicative_mods_tab):
                        with ui.scroll_area().classes("w-full h-full"):
                            with ui.expansion(
                                text="Help",
                                icon="info",
                            ).classes("w-full"):
                                ui.label(
                                    """Put multiplicative modifiers from remolding core 
                                        and in-combat buffs here. Currently, this is 
                                        limited to effects on basic stats like Attack.
                                        """
                                )
                                with ui.list().props("bordered dense separator"):
                                    ui.item_label("Examples").props("header").classes(
                                        "text-bold"
                                    )
                                    ui.separator()
                                    with ui.item():
                                        with ui.item_section():
                                            ui.item_label("Food buff")
                                        with ui.item_section():
                                            ui.item_label(
                                                "Condiment: Weijixian Soy Sauce"
                                            ).props("caption")
                                        with ui.item_section():
                                            ui.item_label(
                                                "Attack is increased by 0.8%, and defense is increased by 0.8%."
                                            ).props("caption")
                                    with ui.item():
                                        with ui.item_section():
                                            ui.item_label(
                                                "Remolding Core Specialized Trait"
                                            )
                                        with ui.item_section():
                                            ui.item_label(
                                                "Attack Boost (Sentinel)"
                                            ).props("caption")
                                        with ui.item_section():
                                            ui.item_label(
                                                "Attack is increased by 2%."
                                            ).props("caption")
                                    with ui.item():
                                        with ui.item_section():
                                            ui.item_label("Remolding Core Imagoform")
                                        with ui.item_section():
                                            ui.item_label(
                                                "Bud (Level 45) (Sentinel)"
                                            ).props("caption")
                                        with ui.item_section():
                                            ui.item_label(
                                                "Attack is increased by 8%."
                                            ).props("caption")

                            ui.separator()

                            with ui.expansion(
                                text="Basic",
                                group="multiplicative_mods",
                            ).classes("w-full"):
                                with ui.list().props(
                                    "bordered dense separator"
                                ).classes("w-full"):
                                    for stat in StatType:
                                        with ui.item():
                                            with ui.item_section().props("no-wrap"):
                                                ui.item_label(stat)
                                                ui.item_label(
                                                    get_stat_description(stat)
                                                ).props("caption")
                                            with ui.item_section().props("side"):
                                                self.multiplicative_stat_modifier_number_inputs[
                                                    stat
                                                ] = ui.number(
                                                    value=0,
                                                    min=0,
                                                    suffix="%",
                                                    precision=1,
                                                    format="%.1f",
                                                )
                            with ui.expansion(
                                text="Basic (Conditional)",
                                group="multiplicative_mods",
                            ).classes("w-full"):
                                for stat in self.conditional_basic_stats_to_show:
                                    with ui.expansion(
                                        text=str(stat),
                                        group="multiplicative_conditional_basic_mods",
                                    ).classes("w-full"):
                                        with ui.list().props(
                                            "bordered dense separator"
                                        ).classes("w-full"):
                                            for tag in self.relevant_damage_tags:
                                                with ui.item():
                                                    with ui.item_section().props(
                                                        "no-wrap"
                                                    ):
                                                        ui.item_label(tag)
                                                        ui.item_label(
                                                            get_tag_description(tag)
                                                        ).props("caption")
                                                    with ui.item_section().props(
                                                        "side"
                                                    ):
                                                        self.multiplicative_conditional_stat_modifier_number_inputs[
                                                            stat
                                                        ][
                                                            tag
                                                        ] = ui.number(
                                                            value=0,
                                                            min=0,
                                                            suffix="%",
                                                            precision=1,
                                                            format="%.1f",
                                                        )

                            with ui.expansion(
                                text="Damage Boost (Increased Damage)",
                                group="multiplicative_mods",
                            ).classes("w-full"):
                                with ui.list().props(
                                    "bordered dense separator"
                                ).classes("w-full"):
                                    for tag in self.relevant_damage_tags:
                                        with ui.item():
                                            with ui.item_section().props("no-wrap"):
                                                ui.item_label(tag)
                                                ui.item_label(
                                                    get_tag_description(tag)
                                                ).props("caption")
                                            with ui.item_section().props("side"):
                                                self.multiplicative_mod_damage_boost_number_inputs[
                                                    tag
                                                ] = ui.number(
                                                    value=0,
                                                    min=0,
                                                    suffix="%",
                                                    precision=1,
                                                    format="%.1f",
                                                )

                            with ui.expansion(
                                text="Critical Damage", group="multiplicative_mods"
                            ).classes("w-full"):
                                with ui.list().props(
                                    "bordered dense separator"
                                ).classes("w-full"):
                                    for tag in self.relevant_damage_tags:
                                        with ui.item():
                                            with ui.item_section().props("no-wrap"):
                                                ui.item_label(tag)
                                                ui.item_label(
                                                    get_tag_description(tag)
                                                ).props("caption")
                                            with ui.item_section().props("side"):
                                                self.multiplicative_mod_critical_damage_number_inputs[
                                                    tag
                                                ] = ui.number(
                                                    value=0,
                                                    min=0,
                                                    suffix="%",
                                                    precision=1,
                                                    format="%.1f",
                                                )

                            with ui.expansion(
                                text="Defense Ignore", group="multiplicative_mods"
                            ).classes("w-full"):
                                with ui.list().props(
                                    "bordered dense separator"
                                ).classes("w-full"):
                                    for tag in self.relevant_damage_tags:
                                        with ui.item():
                                            with ui.item_section().props("no-wrap"):
                                                ui.item_label(tag)
                                                ui.item_label(
                                                    get_tag_description(tag)
                                                ).props("caption")
                                            with ui.item_section().props("side"):
                                                self.multiplicative_mod_defense_ignore_number_inputs[
                                                    tag
                                                ] = ui.number(
                                                    value=0,
                                                    min=0,
                                                    suffix="%",
                                                    precision=1,
                                                    format="%.1f",
                                                )

                    with ui.tab_panel(save_load_tab):
                        with ui.scroll_area().classes("w-full h-full"):
                            ui.label("Export").classes("text-subtitle2 font-bold")
                            (
                                ui.label(
                                    "Download a JSON file with the current configuration. "
                                    "You can upload that file later to restore these stats."
                                ).classes("text-sm text-gray-500")
                            )

                            with ui.row().classes("gap-2"):

                                def _do_export() -> None:
                                    ui.download.content(
                                        self.export_stats_json(),
                                        self.export_stats_filename(),
                                        media_type="application/json",
                                    )

                                ui.button(
                                    "Download JSON",
                                    on_click=_do_export,
                                    icon="download",
                                ).props("color=primary unelevated")

                            ui.separator()
                            ui.label("Import").classes("text-subtitle2 font-bold")
                            ui.label(
                                "Upload a saved .json file to restore these stats."
                            ).classes("text-sm text-gray-500")

                            def _apply_import(json_string: str) -> None:
                                try:
                                    loaded_unit, metadata = (
                                        StatsSerializer.load_from_string(json_string)
                                    )
                                except SerializationError as exc:
                                    ui.notify(
                                        f"Invalid configuration JSON: {exc}",
                                        type="negative",
                                    )
                                    return
                                self.import_stats_from_unit(loaded_unit)
                                self.stats_update_callback(None)
                                doll_name = metadata.get("doll_name") or "unknown"
                                ui.notify(
                                    f"Imported stats for '{doll_name}'",
                                    type="positive",
                                )

                            async def _on_upload(
                                e: events.UploadEventArguments,
                            ) -> None:
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
                                            text_val = await _maybe_await(
                                                source.text(encoding="utf-8")
                                            )
                                            if isinstance(text_val, str):
                                                return text_val
                                        except TypeError:
                                            try:
                                                text_val = await _maybe_await(
                                                    source.text()
                                                )
                                                if isinstance(text_val, str):
                                                    return text_val
                                            except Exception:
                                                ...
                                        except Exception:
                                            ...

                                    if hasattr(source, "read"):
                                        raw = await _maybe_await(source.read())
                                        if isinstance(
                                            raw, (bytes, bytearray, memoryview)
                                        ):
                                            return bytes(raw).decode("utf-8")
                                        if isinstance(raw, str):
                                            return raw

                                    if hasattr(source, "getvalue"):
                                        raw = await _maybe_await(source.getvalue())
                                        if isinstance(
                                            raw, (bytes, bytearray, memoryview)
                                        ):
                                            return bytes(raw).decode("utf-8")
                                        if isinstance(raw, str):
                                            return raw

                                    return None

                                try:
                                    payload = None

                                    if hasattr(e, "content") and e.content is not None:
                                        payload = await _read_text(e.content)

                                    if (
                                        payload is None
                                        and hasattr(e, "file")
                                        and e.file is not None
                                    ):
                                        payload = await _read_text(e.file)

                                    if (
                                        payload is None
                                        and hasattr(e, "file")
                                        and e.file is not None
                                        and hasattr(e.file, "file")
                                    ):
                                        payload = await _read_text(e.file.file)

                                except UnicodeDecodeError:
                                    ui.notify(
                                        "File must be UTF-8 encoded JSON",
                                        type="negative",
                                    )
                                    return

                                if payload is None:
                                    ui.notify(
                                        "Could not read uploaded file",
                                        type="negative",
                                    )
                                    return

                                payload = (
                                    payload.lstrip("\ufeff") if payload else payload
                                )
                                if not payload or not payload.strip():
                                    ui.notify("Uploaded file is empty", type="negative")
                                    return
                                if payload.lstrip()[:1] not in {"{", "["}:
                                    ui.notify(
                                        "Upload did not contain JSON text",
                                        type="negative",
                                    )
                                    return
                                _apply_import(payload)

                            ui.upload(
                                label="Upload .json configuration",
                                on_upload=_on_upload,
                                auto_upload=True,
                            ).props("accept=.json outlined")

        ui.separator().classes("w-330 exilium-divider")

        self.set_initial_values()
        self.update_doll_abilities()
        self.rebind_doll()

        with ui.tabs().classes("w-fit exilium-main-tabs") as tabs:
            basic_stats_tab = ui.tab("Rotation Potency")
            special_stats_tab = ui.tab("Damage Calculator")

        with ui.tab_panels(tabs, value=basic_stats_tab).classes(
            "w-340 h-full exilium-tab-panels"
        ):
            with ui.tab_panel(basic_stats_tab).classes("w-full h-400"):
                with ui.grid(columns="25% auto").classes("w-full h-full"):
                    self.get_rotation_planner()
                    self.get_rotation_analysis()

            with ui.tab_panel(special_stats_tab).classes("w-full h-650"):
                from gui.templates.damage_calculator import DamageCalculator

                self.damage_calculator = DamageCalculator(self)

        self.damage_instances = self.rotation_planner.get_all_actions()
        self.stats_update_callback(None)
