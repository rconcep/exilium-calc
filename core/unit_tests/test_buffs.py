# from core.types import StatType, SpecialAttribute, DamageTag, FortificationLevel
from core.buffs import *


def test_RadiantRise():
    assert RadiantRise(FortificationLevel.SEGMENT00).value == 30
    assert RadiantRise(FortificationLevel.SEGMENT02).value == 50
