from nicegui import app, ui
from typing import Callable

from gui.doll_calculator.dolls import (
    Alva,
    Basti,
    Daiyan,
    Dushevnaya,
    Faye,
    Belka,
    Cheyanne,
    Helen,
    Jiangyu,
    Klukai,
    Liushih,
    Loreley,
    Robella,
    Sextans,
    Soppo,
    Voymastina,
    Lewis,
    MosinNagant,
    OTs14,
    Tololo,
    Leva,
    Lenna,
    Lind,
    Makiatto,
    Mechty,
    Nikketa,
    Phaetusa,
    Qiuhua,
    Qiongjiu,
    Lainie,
    Sakura,
    Springfield,
    Ullrid,
    Yoohee,
    Vector,
    Vepley,
)
from gui.styles.theme import apply_exilium_theme

DOLL_PAGES: list[tuple[str, str, Callable[[], object]]] = [
    ("Alva", "/alva", Alva),
    ("Basti", "/basti", Basti),
    ("Belka", "/belka", Belka),
    ("Cheyanne", "/cheyanne", Cheyanne),
    ("Daiyan", "/daiyan", Daiyan),
    ("Dushevnaya", "/dushevnaya", Dushevnaya),
    ("Faye", "/faye", Faye),
    ("Helen", "/helen", Helen),
    ("Jiangyu", "/jiangyu", Jiangyu),
    ("Lainie", "/lainie", Lainie),
    ("Liushih", "/liushih", Liushih),
    ("Loreley", "/loreley", Loreley),
    ("Leva", "/leva", Leva),
    ("Lenna", "/lenna", Lenna),
    ("Lewis", "/lewis", Lewis),
    ("Lind", "/lind", Lind),
    ("Klukai", "/klukai", Klukai),
    ("Makiatto", "/makiatto", Makiatto),
    ("Mechty", "/mechty", Mechty),
    ("Mosin-Nagant", "/mosin-nagant", MosinNagant),
    ("Nikketa", "/nikketa", Nikketa),
    ("OTs-14", "/ots-14", OTs14),
    ("Phaetusa", "/phaetusa", Phaetusa),
    ("Qiuhua", "/qiuhua", Qiuhua),
    ("Qiongjiu", "/qiongjiu", Qiongjiu),
    ("Robella", "/robella", Robella),
    ("Sakura", "/sakura", Sakura),
    ("Soppo", "/soppo", Soppo),
    ("Sextans", "/sextans", Sextans),
    ("Springfield", "/springfield", Springfield),
    ("Voymastina", "/voymastina", Voymastina),
    ("Tololo", "/tololo", Tololo),
    ("Ullrid", "/ullrid", Ullrid),
    ("Vector", "/vector", Vector),
    ("Yoohee", "/yoohee", Yoohee),
    ("Vepley", "/vepley", Vepley),
]


def root():
    dark = ui.dark_mode()
    dark.enable()
    apply_exilium_theme()
    ui.page_title("Exilium-Calc")

    pages: dict[str, str] = {label: route for label, route, _factory in DOLL_PAGES}
    with ui.header(fixed=True, bordered=True).classes("exilium-topbar"):
        with ui.row().classes("w-full items-center gap-3 exilium-shell"):
            ui.button("", icon="home", on_click=lambda: ui.navigate.to("/")).props(
                "color=primary push"
            )
            ui.select(
                options=sorted(list(pages.keys())),
                label="Doll",
                with_input=True,
                new_value_mode=None,
                on_change=lambda t: ui.navigate.to(pages[t.value]),
            ).props("square outlined")

            ui.switch("Dark mode").bind_value(dark).props("color=white")

    def lazy_doll_page(route: str, factory: Callable[[], object]) -> Callable[[], None]:
        """Create a fresh Doll page instance for each navigation."""

        def render() -> None:
            factory().get_page()  # type: ignore[attr-defined]

        return render

    sub_page_routes: dict[str, Callable[[], None]] = {"/": mainpage}
    sub_page_routes.update(
        {route: lazy_doll_page(route, factory) for _label, route, factory in DOLL_PAGES}
    )

    ui.sub_pages(sub_page_routes)

    with ui.footer(bordered=True, fixed=False).classes("exilium-footer"):
        with ui.column().classes("w-full items-center q-py-sm"):
            with ui.row().classes("w-full justify-center items-center gap-1"):
                ui.label("Exilium-Calc © 2026 | ").classes("text-center")
                ui.link(
                    "Discord",
                    target="https://discord.com/users/132232400687071233",
                    new_tab=True,
                ).classes("text-center")
            ui.label(
                "Exilium-Calc is an unofficial fan-made project for Girls' Frontline 2: Exilium. Not affiliated with, endorsed by, or sponsored by MICA Team or Sunborn Network Technology Co., Ltd."
            ).classes("text-center text-caption exilium-subtle")


def mainpage() -> None:
    ui.markdown("""# Welcome to Exilium-Calc!
Get started by selecting a Doll above.
                """).classes("exilium-intro-copy exilium-shell")

    with ui.grid(columns=2).classes("w-full exilium-mainpage-row"):
        with ui.card().classes("w-150 h-150 exilium-panel"):
            ui.markdown(
                """## Rotation Potency 
A tool used for simulating the effect of "increased damage" stats on rotations intended for informing gearing choices:

* Selecting between attachment sets
* Selecting Remolding Core Special Traits

This tool is not intended for comparing damage output between Dolls - it abstracts away many of the components of 
the damage calculation and instead focuses on "potency".

### What is "potency"?
The damage formula consists of several terms that are multiplied together, including:

* Base damage, as a function of Attack/Health and the target's Defense
* Skill multiplier ("deals x% of attack")
* The sum of all applicable "increased damage" stats
* Critical damage multiplier, if the attack is a crit
* Increased damage taken effects on the target
* Bonus damage if phase weaknesses are exploited

We use the term "potency" to refer to the product of skill multiplier and the sum of all applicable "increased damage" stats.
The other terms are typically constant across gearing choices (base damage, critical damage, etc.).


            """,
            ).classes("exilium-intro-copy")

        with ui.card().classes("w-150 h-150 exilium-panel"):
            ui.markdown("""## Damage Calculator
A tool used for calculating the damage dealt by a single action. Apply buffs to the Doll and debuffs to the target,
select a skill, and hit calculate to see the expected result.

### Scenario Comparison
Trying to figure out if losing 3 levels of Freeze Boost for 3 levels of Freeze Smite in your Remolding Core is worth it? This feature 
allows you to compare the expected damage output of different scenarios by applying the respective stat changes to the Doll and 
comparing the resulting expected damage (for a specific action under specified conditions).

### Stat Increment Analysis
Should you add "increased damage" modifiers or "increased critical damage", given the Doll's current build? This feature 
allows you to see which stats provide the most marginal benefit to expected damage output by incrementally increasing 
each stat and observing the resulting change in expected damage.
                        """).classes("exilium-intro-copy")

        with ui.card().classes("w-150 h-150 exilium-panel"):
            ui.markdown("""## Rotation Simulator
A tool used to estimate the expected damage dealt to a single target after a sequence of actions ("rotation").
                        
* Configure the baseline stats of the Doll and the target, including buffs and debuffs. These conditions will be used in the action timeline unless overridden.
* Define the attacker's rotation then sync the timeline.
* Edit each action in the timeline as desired - are buffs or debuffs added or removed at this point?
* Run the simulation to see the results.
* Need to adjust the buff/debuff timings? Edit the Action Timeline and re-run the simulation.
* Need to modify the rotation? Edit the Rotation, re-sync the timeline, edit the Action Timeline, and re-run the simulation.
* Rotation data can be saved and loaded for sharing or future use.

Scenario Comparison and Stat Increment Analysis are also available in Rotation Simulator for sensitivity analysis.
                        """).classes("exilium-intro-copy")

    with ui.row().classes("w-full exilium-mainpage-row"):
        with ui.card().classes("w-200 h-100 exilium-panel"):
            ui.label("Revision history").classes("text-lg")
            ui.separator()
            with ui.scroll_area().classes("w-full h-150"):
                with ui.timeline(side="right"):
                    ui.timeline_entry(
                        "Added the Rotation Simulator tool - a union of the Rotation Potency and Damage Calculator tools for estimating the expected damage of a rotation in a single-target scenario. Added Springfield's expansion key. Fixed physical summons' stat inheritance behavior.",
                        title="Added Rotation Simulator",
                        subtitle="July 24, 2026",
                        icon="analytics",
                    )
                    ui.timeline_entry(
                        "Add Rank (Lewis) buff to represent buff from Tin Soldiers' rank; marked release of version 1.0.0.",
                        title="Release 1.0.0",
                        subtitle="July 9, 2026",
                        icon="publish",
                    )

                    ui.timeline_entry(
                        "Updated Loreley's localizations and sample rotation; implemented Klukai's expansion key.",
                        title="",
                        subtitle="June 26, 2026",
                        icon="translate",
                    )
                    ui.timeline_entry(
                        "Updated Loreley's localizations based on preview material and added to her Notes.",
                        title="",
                        subtitle="June 18, 2026",
                        icon="translate",
                    )
                    ui.timeline_entry(
                        "Added a tab for Doll Notes - quick reference for Dolls' utility, team and build tips, and upgrades at each fortification level. Updated Basti's localizations after GL release.",
                        title="Added Doll Notes",
                        subtitle="June 4, 2026",
                        icon="post_add",
                    )
                    ui.timeline_entry(
                        "Implemented Basti (preview). Fixed a bug in Rotation Potency where removing actions from one turn could cause actions to be removed from other turns as well due to shared references.",
                        title="",
                        subtitle="May 27, 2026",
                        icon="person_add",
                    )
                    ui.timeline_entry(
                        "Added Total Increased Damage to Damage Calculator results.",
                        title="",
                        subtitle="May 27, 2026",
                        icon="functions",
                    )
                    ui.timeline_entry(
                        "Changed Phaetusa's Bloodquenched buff behavior such that it does not get multiplied by Blade Resonance stack effect. Updated Phaetusa's sample rotation.",
                        title="",
                        subtitle="May 15, 2026",
                        icon="bloodtype",
                    )
                    ui.timeline_entry(
                        "Updated names of Phaetusa's actions and buffs to match GL translations.",
                        title="",
                        subtitle="May 9, 2026",
                        icon="translate",
                    )
                    ui.timeline_entry(
                        "Implemented Soppo (preview). Added 'on phase tile' as a damage tag; added phase tile level and unit level (type) to target in Damage Calculator. (Note: Buffs/debuffs/actions that take phase tile level as a parameter do not check the target's parameters and simply use their own parameters.)",
                        title="",
                        subtitle="May 2, 2026",
                        icon="person_add",
                    )
                    ui.timeline_entry(
                        "Implemented Sextans (preview).",
                        title="",
                        subtitle="April 28, 2026",
                        icon="person_add",
                    )
                    ui.timeline_entry(
                        "Updated Qiuhua with Expansion Key - Sizzling Stir-Fry. Updated Helen flavor text.",
                        title="",
                        subtitle="April 24, 2026",
                        icon="key",
                    )
                    ui.timeline_entry(
                        "Implemented Loreley (preview).",
                        title="",
                        subtitle="April 22, 2026",
                        icon="person_add",
                    )
                    ui.timeline_entry(
                        "Implemented Cheyanne (preview).",
                        title="",
                        subtitle="April 20, 2026",
                        icon="person_add",
                    )
                    ui.timeline_entry(
                        "Implemented Liushih (preview) and updated Helen's actions and buffs to GL translations.",
                        title="",
                        subtitle="April 17, 2026",
                        icon="person_add",
                    )
                    ui.timeline_entry(
                        "Implemented Phaetusa (preview) and Mechty.",
                        title="",
                        subtitle="April 16, 2026",
                        icon="person_add",
                    )
                    ui.timeline_entry(
                        "Implemented Helen (preview).",
                        title="",
                        subtitle="April 15, 2026",
                        icon="person_add",
                    )
                    ui.timeline_entry(
                        "Implemented Dushevnaya.",
                        title="",
                        subtitle="April 14, 2026",
                        icon="person_add",
                    )
                    ui.timeline_entry(
                        "Implemented Lenna and Belka.",
                        title="",
                        subtitle="April 13, 2026",
                        icon="person_add",
                    )
                    ui.timeline_entry(
                        "Implemented Daiyan and Ullrid.",
                        title="",
                        subtitle="April 11, 2026",
                        icon="person_add",
                    )
                    ui.timeline_entry(
                        "Implemented Springfield.",
                        title="",
                        subtitle="April 11, 2026",
                        icon="person_add",
                    )
                    ui.timeline_entry(
                        "Implemented Sakura and Vector.",
                        title="",
                        subtitle="April 10, 2026",
                        icon="person_add",
                    )
                    ui.timeline_entry(
                        "Implemented Alva and Lind. Tied stability broken modifiers to the actual Target state in Damage Calculator instead of assuming it's always True.",
                        title="",
                        subtitle="April 9, 2026",
                        icon="person_add",
                    )
                    ui.timeline_entry(
                        """Finally determined that the "damage multiplier" is a more like flat bonus damage and it does not interact with Attack at all.
                        This explains why its scaling is so weak. I was able to recover the 10% of Health scaling although some "slack" exists in the
                        regression analysis especially for high damage modifiers... so there's still a compensation bias term in the model. I may test
                        with V3 Lainie to see if the model holds up.
                        """,
                        title="Revised Lainie's Health-based scaling (for good?)",
                        subtitle="April 4, 2026",
                        icon="bug_report",
                    )
                    ui.timeline_entry(
                        """Revised Lainie's Health-based scaling after in-game testing. The skill multiplier is 
                        definitely not increased by 10% of Health and, based on linear regression analysis, exhibits severe diminishing returns when
                        damage increases (including Reversed Assault) and critical damage multipliers are high. I've only tested up to V1 Lainie so
                        for now the scaling isn't updated at higher fortification levels.
                        """,
                        title="Revised Lainie's Health-based scaling",
                        subtitle="April 3, 2026",
                        icon="bug_report",
                    )
                    ui.timeline_entry(
                        "Implemented Lind.",
                        title="",
                        subtitle="April 3, 2026",
                        icon="person_add",
                    )
                    ui.timeline_entry(
                        "Implemented Faye and Klukai; implemented Fixed damage; removed low-value tags from the damage type breakdown in Rotation Analysis.",
                        title="",
                        subtitle="April 1, 2026",
                        icon="person_add",
                    )
                    ui.timeline_entry(
                        "Implemented Qiuhua and Qiongjiu; added missing controls for initial, conditional basic stat modifiers.",
                        title="",
                        subtitle="March 29, 2026",
                        icon="person_add",
                    )
                    ui.timeline_entry(
                        "Implemented theming inspired by GFL2. Replaced revision history on each Doll page with modeling assumptions.",
                        title="Implemented Theme",
                        subtitle="March 29, 2026",
                        icon="palette",
                    )
                    ui.timeline_entry(
                        "Fixed an issue where conditional %DEF down was not being applied correctly for ignoring defense calculations.",
                        title="",
                        subtitle="March 28, 2026",
                        icon="bug_report",
                    )
                    ui.timeline_entry(
                        "Implemented Yoohee and Vepley; added support for conditional modifiers to Attack and Critical Rate",
                        title="",
                        subtitle="March 28, 2026",
                        icon="person_add",
                    )
                    ui.timeline_entry(
                        "Trying to decide which attachment or growth data to use? See which stat change combination increases damage more.",
                        title="Added Scenario Comparison to Damage Calculator",
                        subtitle="March 28, 2026",
                        icon="analytics",
                    )
                    ui.timeline_entry(
                        "Analyze relative change in expected damage by marginal changes in stats",
                        title="Added Stat Increment Analysis to Damage Calculator",
                        subtitle="March 28, 2026",
                        icon="analytics",
                    )
                    ui.timeline_entry(
                        "Implemented preview of Lainie (why does her scaling look insane?)",
                        title="",
                        subtitle="March 27, 2026",
                        icon="person_add",
                    )
                    ui.timeline_entry(
                        "Added feature to save/load Doll stats as JSON files",
                        title="Added save/load feature",
                        subtitle="March 26, 2026",
                        icon="save",
                    )
                    ui.timeline_entry(
                        "Implemented Nikketa; made backend changes to support summons",
                        title="",
                        subtitle="March 26, 2026",
                        icon="person_add",
                    )
                    ui.timeline_entry(
                        "Implemented Makiatto",
                        title="",
                        subtitle="March 23, 2026",
                        icon="person_add",
                    )
                    ui.timeline_entry(
                        "First deployment as a web app",
                        title="First deployment",
                        subtitle="March 22, 2026",
                        icon="rocket",
                    )
                    ui.timeline_entry(
                        "", title="Development begins", subtitle="March 3, 2026"
                    )


if __name__ in {"__main__", "__mp_main__"}:
    app.add_static_files(
        "/resources",
        "resources",
    )
    ui.run(
        root,
        # reload=False,
        reconnect_timeout=300,
    )
