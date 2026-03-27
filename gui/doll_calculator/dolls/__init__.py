"""GUI doll calculator pages.

This package re-exports doll page classes for convenient imports:
        from gui.doll_calculator.dolls import Leva, Robella
"""

from .leva import Leva
from .lewis import Lewis
from .makiatto import Makiatto
from .mosin_nagant import MosinNagant
from .nikketa import Nikketa
from .robella import Robella
from .tololo import Tololo
from .voymastina import Voymastina

__all__ = [
    "Leva",
    "Lewis",
    "Makiatto",
    "MosinNagant",
    "Nikketa",
    "Robella",
    "Tololo",
    "Voymastina",
]
