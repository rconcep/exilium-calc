import pytest

from core.dolls.asteria import Asteria, BladeOfSinV6, RailgunJudgementV6
from core.types import DamageTag, FortificationLevel


def test_asteria_v6_upgrade_scales_railgun_and_blade_of_sin():
    doll = Asteria()
    doll.set_fortification_level(FortificationLevel.SEGMENT06)

    assert isinstance(doll.railgun_judgement, RailgunJudgementV6)
    assert isinstance(doll.blade_of_sin, BladeOfSinV6)

    railgun = doll.railgun_judgement.execute(
        has_fixed_key_6=True,
        stacks_of_absolution=8,
    )
    blade = doll.blade_of_sin.execute(stacks_of_absolution=5)

    assert railgun.base_potency == pytest.approx(600)
    assert DamageTag.MELEE in railgun.tags
    assert blade.base_potency == pytest.approx(350)
    assert DamageTag.MELEE in blade.tags


def test_asteria_low_fortification_keeps_base_railgun_potency():
    doll = Asteria()
    doll.set_fortification_level(FortificationLevel.SEGMENT00)

    railgun = doll.railgun_judgement.execute(
        has_fixed_key_6=False,
        stacks_of_absolution=6,
    )

    assert railgun.base_potency == pytest.approx(240)
    assert DamageTag.MELEE not in railgun.tags
