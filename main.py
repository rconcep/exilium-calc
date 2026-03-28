from nicegui import app, ui

from gui.doll_calculator.dolls import (
    Robella,
    Voymastina,
    Lewis,
    MosinNagant,
    Tololo,
    Leva,
    Makiatto,
    Nikketa,
    Lainie,
)


def root():
    dark = ui.dark_mode()
    ui.page_title("Exilium-Calc")

    pages: dict[str, str] = {
        "Lainie": "/lainie",
        "Leva": "/leva",
        "Lewis": "/lewis",
        "Makiatto": "/makiatto",
        "Mosin-Nagant": "/mosin-nagant",
        "Nikketa": "/nikketa",
        "Robella": "/robella",
        "Voymastina": "/voymastina",
        "Tololo": "/tololo",
    }

    with ui.row().classes("w-full items-center"):
        ui.button("", icon="home", on_click=lambda: ui.navigate.to("/")).props("flat")
        ui.select(
            options=sorted(list(pages.keys())),
            label="Doll",
            with_input=True,
            new_value_mode=None,
            on_change=lambda t: ui.navigate.to(pages[t.value]),
        ).props("standout")

        # with ui.button(icon='menu'):
        #     with ui.menu() as menu:
        #         ui.menu_item('Home', lambda: ui.navigate.to('/'))
        #         ui.menu_item('Robella', lambda: ui.navigate.to('/robella'))
        #         ui.menu_item('Voymastina', lambda: ui.navigate.to('/voymastina'))
        #         ui.menu_item('Lewis', lambda: ui.navigate.to('/lewis'))

        ui.switch("Dark mode").bind_value(dark)

    ui.sub_pages(
        {
            "/": mainpage,
            "/lainie": Lainie().get_page,
            "/robella": Robella().get_page,
            "/voymastina": Voymastina().get_page,
            "/lewis": Lewis().get_page,
            "/mosin-nagant": MosinNagant().get_page,
            "/tololo": Tololo().get_page,
            "/leva": Leva().get_page,
            "/makiatto": Makiatto().get_page,
            "/nikketa": Nikketa().get_page,
        }
    )


def mainpage() -> None:
    ui.markdown(
        """# Welcome to Exilium-Calc!
Get started by selecting a Doll above.
                """
    )

    with ui.row():
        with ui.card().classes("w-150 h-150"):
            ui.markdown(
                """## Rotation Potency 
A tool used for simulating the effect of "increased damage" stats on rotations intended for informing gearing choices:

* Selecting between attachment sets
* Selecting Remolding Core Special Traits

This tool is not intended for comparing damage output between Dolls - it abstracts away many of the components of 
the damage calculation and instead focuses on "potency".

### What is "potency"?
The damage formula consists of several terms that are multiplied together:

* Base damage, as a function of Attack and the target's Defense
* Skill multiplier ("deals x% of attack")
* The sum of all applicable "increased damage" stats
* Critical damage multiplier, if the attack is a crit
* Increased damage taken effects on the target
* Bonus damage if phase weaknesses are exploited
* Damage reduction if the target has stability

We use the term "potency" to refer to the product of skill multiplier and the sum of all applicable "increased damage" stats. 
This is because these are the terms that are most relevant to gearing choices. The other terms are either constant across 
gearing choices (base damage, critical damage multiplier, increased damage taken effects) or are not relevant 
(phase weaknesses, stability).


            """,
            )

        with ui.card().classes("w-150 h-100"):
            ui.markdown(
                """## Damage Calculator
A tool used for calculating the damage dealt by a single action. Apply buffs to the Doll and debuffs to the target,
select a skill, and hit calculate to see the expected result. Note that all visible stats are applied - the attribute
tab is shared with all tools!
                        """
            )

    with ui.row():
        with ui.card().classes("w-150 h-100"):
            ui.label("Revision history").classes("text-lg")
            ui.separator()
            with ui.scroll_area().classes("w-full h-150"):
                with ui.timeline(side="right"):
                    ui.timeline_entry(
                        "Added feature to save/load Doll stats as JSON files",
                        title="Added save/load feature",
                        subtitle="March 26, 2026",
                    )
                    ui.timeline_entry(
                        "Implemented Nikketa; made backend changes to support summons",
                        title="",
                        subtitle="March 26, 2026",
                    )
                    ui.timeline_entry(
                        "Implemented Makiatto",
                        title="",
                        subtitle="March 23, 2026",
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
