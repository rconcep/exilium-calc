from nicegui import ui

from typing import final, Any
from abc import ABC, abstractmethod
from dataclasses import asdict
from decimal import Decimal, ROUND_DOWN

from core.types import *
from core.combat import DamageInstance, sum_damage_instances
from gui.templates.rotation_planner import RotationPlanner
from gui.styles.descriptions import get_tag_description, get_stat_description
from gui.styles.graphs import get_bar_chart_template, get_donut_chart_template


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

    def __init__(self):
        # Basic Tab
        self.initial_stats_number_inputs: dict[StatType, ui.number] = {}

        # Special Tab
        self.damage_boost_number_inputs: dict[DamageTag, ui.number] = {}
        self.critical_damage_number_inputs: dict[DamageTag, ui.number] = {}
        self.defense_ignore_number_inputs: dict[DamageTag, ui.number] = {}

        # Additive Modifier Tab
        self.additive_stat_modifier_number_inputs: dict[StatType, ui.number] = {}
        self.additive_mod_damage_boost_number_inputs: dict[DamageTag, ui.number] = {}
        self.additive_mod_critical_damage_number_inputs: dict[DamageTag, ui.number] = {}
        self.additive_mod_defense_ignore_number_inputs: dict[DamageTag, ui.number] = {}

        # Multiplicative Modifier Tab
        self.multiplicative_stat_modifier_number_inputs: dict[StatType, ui.number] = {}
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
        )

    @abstractmethod
    def revision_history(self) -> None:
        """Generates the revision history information."""
        pass

    @abstractmethod
    def get_rotation_planner(self) -> None:
        """Generates the Rotation Planner section."""
        pass

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
            )
            self.potency_bar_chart_plot = ui.plotly(
                self.potency_bar_chart_data
            ).classes("w-full h-100")
            self.damage_type_breakdown_table = ui.table(
                columns=DollCalculatorPage.damage_type_breakdown_table_columns,
                rows=[],
                pagination={"rowsPerPage": 5, "sortBy": "share", "descending": True},
            )
            self.donut_chart_plot_3 = ui.plotly(self.ability_donut_chart).classes(
                "w-full h-80"
            )

            self.update_potency_bar_chart()
            self.update_ability_breakdown_donut_chart()
            self.update_damage_type_breakdown_table()

    def stats_update_callback(self, update: ui.number) -> None:
        """Updates elements when Doll stats are modified."""
        for di in self.damage_instances:
            di.calculate_adjusted_potency(
                self.doll.get_effective_special_attribute(SpecialAttribute.DAMAGE_BOOST)
            )

        self.update_actions_table()
        self.update_potency_bar_chart()
        self.update_ability_breakdown_donut_chart()
        self.update_damage_type_breakdown_table()

    @abstractmethod
    def update_doll_abilities(self) -> None:
        """Update self.option_config references to Doll ability functions."""
        pass

    def doll_fortification_callback(self, update: ui.select) -> None:
        """Updates Doll abilities upon changing Fortification level."""
        self.doll.set_fortification_level(FortificationLevel(update.value))
        ui.notify(f"Changed fortification to V{update.value}", group=False)
        self.update_doll_abilities()
        self.rotation_planner.set_options_config(self.option_config)

        for di in self.damage_instances:
            di.calculate_adjusted_potency(
                self.doll.get_effective_special_attribute(SpecialAttribute.DAMAGE_BOOST)
            )

        self.actions_table_data: list[dict] = [
            asdict(di) for di in self.damage_instances
        ]
        self.stats_update_callback(None)

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
        pass

    def update_actions_table(self) -> None:
        """Updates the Actions Table."""
        new_rows = [asdict(di) for di in self.damage_instances]

        # Null out the tags key because Set isn't JSON serializable
        # and we don't display it anyway
        for row in new_rows:
            row["tags"] = ""
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
            grouped_damage_instances.setdefault(di.group_name, DamageInstance("", 0))
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
        new_rows: list[dict[Any]] = [
            asdict(sum_damage_instances(self.damage_instances, tag))
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

        with ui.row():
            with ui.card().classes("w-100 h-150"):
                self.doll_header()
                self.revision_history()

                with ui.grid(columns="50% auto").classes("w-full gap-0"):
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
                    )

            with ui.card().classes("w-75 h-150"):
                ui.image(self.doll_portrait)

            with ui.card().classes("w-150 h-150"):
                with ui.tabs().classes("w-full") as tabs:
                    basic_stats_tab = ui.tab("Basic").tooltip(
                        "Initial values of basic stats as seen in Refitting Room or Formation."
                    )
                    special_stats_tab = ui.tab("Special").tooltip(
                        "Conditionally applied stats from innate abilities."
                    )
                    additive_mods_tab = ui.tab("Additive Mods").tooltip(
                        '"Additive" modifiers from non-innate sources.'
                    )
                    multiplicative_mods_tab = ui.tab("Multiplicative Mods").tooltip(
                        '"Multiplicative" modifiers from non-innate sources.'
                    )
                with ui.tab_panels(tabs, value=basic_stats_tab).classes(
                    "w-full h-full"
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
                                                        precision=2,
                                                        suffix="%",
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
                                                    precision=2,
                                                    suffix="%",
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
                                                    precision=2,
                                                    suffix="%",
                                                )

                    with ui.tab_panel(additive_mods_tab):
                        with ui.scroll_area().classes("w-full h-full"):
                            with ui.expansion(
                                text="Help",
                            ).classes("w-full"):
                                ui.label(
                                    """Put additive modifiers from keys, attachment set 
                                        bonuses, remolding core, and in-combat buffs here."""
                                )
                                ui.label(
                                    """Note: Since these mods are additive with the 'Special' tab,
                                        it technically doesn't matter if they are put here or 
                                        in the 'Special' tab, but the values in the 'Special'
                                        tab are liable to dynamically change (e.g., when changing
                                        Fortification Level)."""
                                ).classes("italic")
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
                                                    value=0, min=0, precision=2
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
                                                    precision=2,
                                                    suffix="%",
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
                                                    precision=2,
                                                    suffix="%",
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
                                                    precision=2,
                                                    suffix="%",
                                                )

                    with ui.tab_panel(multiplicative_mods_tab):
                        with ui.scroll_area().classes("w-full h-full"):
                            with ui.expansion(
                                text="Help",
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
                                                    value=0, min=0, precision=2
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
                                                    precision=2,
                                                    suffix="%",
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
                                                    precision=2,
                                                    suffix="%",
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
                                                    precision=2,
                                                    suffix="%",
                                                )

        ui.separator().classes("w-330")

        self.set_initial_values()
        self.update_doll_abilities()
        self.rebind_doll()

        with ui.tabs().classes("") as tabs:
            basic_stats_tab = ui.tab("Rotation Potency")
            special_stats_tab = ui.tab("Damage Calculator")

        with ui.tab_panels(tabs, value=basic_stats_tab).classes("w-330 h-300"):
            with ui.tab_panel(basic_stats_tab).classes("w-full h-full"):
                with ui.grid(columns="25% auto").classes("w-full h-full"):
                    self.get_rotation_planner()
                    self.get_rotation_analysis()

            with ui.tab_panel(special_stats_tab).classes("w-full h-full"):
                from gui.templates.damage_calculator import DamageCalculator

                self.damage_calculator = DamageCalculator(self)

        self.damage_instances = self.rotation_planner.get_all_actions()
        self.stats_update_callback(None)
