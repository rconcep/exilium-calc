from nicegui import app, ui

from gui.doll_calculator.dolls.robella import Robella
from gui.doll_calculator.dolls.voymastina import Voymastina
from gui.doll_calculator.dolls.lewis import Lewis
from gui.doll_calculator.dolls.mosin_nagant import MosinNagant
from gui.doll_calculator.dolls.tololo import Tololo
from gui.doll_calculator.dolls.leva import Leva


def root():
    dark = ui.dark_mode()
    ui.page_title("Exilium-Calc")

    pages: dict[str, str] = {
        "Leva": "/leva",
        "Lewis": "/lewis",
        "Mosin-Nagant": "/mosin-nagant",
        "Robella": "/robella",
        "Voymastina": "/voymastina",
        "Tololo": "/tololo",
    }

    with ui.row().classes("w-full items-center"):
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
            "/robella": Robella().get_page,
            "/voymastina": Voymastina().get_page,
            "/lewis": Lewis().get_page,
            "/mosin-nagant": MosinNagant().get_page,
            "/tololo": Tololo().get_page,
            "/leva": Leva().get_page,
        }
    )


def mainpage() -> None:
    ui.markdown(
        """# Welcome to Exilium-Calc!
Get started by selecting a Doll above.
                """
    )

    with ui.row():
        with ui.card().classes("w-150 h-100"):
            ui.markdown(
                r"""## Rotation Potency 
A tool used for simulating the effect of 'increased damage' stats on rotations intended for informing gearing choices:

* Selecting between attachment sets
* Selecting Remolding Core Special Traits
* Not intended for comparing damage output between Dolls

### What is "potency"?
In the damage formula, there is a term that can be thought of as:
$$\text{potency} = \text{skill modifier in ATK%} \cdot \left( 1 + \sum \text{increased damage modifiers} \right)$$
which is multiplied by factors like ATK, critical damage multipliers, etc.
                        
Potency is used to abstract away the effects of those stats which tend to remain constant among gearing choices 
such as attachment sets. This term is borrowed from other games.
            """,
                # extras=[
                #     "latex",
                # ],
            )

        with ui.card().classes("w-150 h-100"):
            ui.markdown(
                """## Damage Calculator
A tool used for calculating the damage dealt by a single action. Apply buffs to the Doll and debuffs to the target,
select a skill, and hit calculate to see the expected result. Note that all visible stats are applied - the attribute
tab is shared with all tools!
                        """
            )


if __name__ in {"__main__", "__mp_main__"}:
    app.add_static_files(
        "/resources",
        "resources",
    )
    ui.run(
        root,
        reload=False,
        reconnect_timeout=300,
    )
