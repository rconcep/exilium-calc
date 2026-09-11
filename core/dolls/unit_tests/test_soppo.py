from core.combat import DamageInstance
from core.dolls.soppo import *
from core.types import DamageTag, FortificationLevel


class TestSoppoSkills:
    def test_hunting_fang_freeze_and_burn_forms(self):
        freeze_hit: DamageInstance = HuntingFang().execute(in_feral_form=False)
        burn_hit: DamageInstance = HuntingFang().execute(in_feral_form=True)

        assert freeze_hit.base_potency == 80
        assert DamageTag.FREEZE in freeze_hit.tags
        assert DamageTag.BURN not in freeze_hit.tags

        assert burn_hit.base_potency == 80
        assert DamageTag.BURN in burn_hit.tags
        assert DamageTag.FREEZE not in burn_hit.tags

    def test_vicious_bite_v1_potency(self):
        hit: DamageInstance = ViciousBiteV1().execute(in_feral_form=False)

        assert hit.base_potency == 130
        assert DamageTag.AREA_OF_EFFECT in hit.tags

    def test_lunar_howl_v2_tile_tags(self):
        frost: DamageInstance = LunarHowlV2().execute(
            tile_target=LunarHowlTileTargetType.FROST
        )
        incineration: DamageInstance = LunarHowlV2().execute(
            tile_target=LunarHowlTileTargetType.INCINERATION
        )
        ashen_breath: DamageInstance = LunarHowlV2().execute(
            tile_target=LunarHowlTileTargetType.SMOLDERING_SUSPIRE
        )

        assert frost.base_potency == 80
        assert DamageTag.FREEZE in frost.tags
        assert DamageTag.BURN not in frost.tags

        assert incineration.base_potency == 80
        assert DamageTag.BURN in incineration.tags
        assert DamageTag.FREEZE not in incineration.tags

        assert ashen_breath.base_potency == 80
        assert DamageTag.BURN not in ashen_breath.tags
        assert DamageTag.FREEZE not in ashen_breath.tags

    def test_lunar_howl_form_swap_v3_scaling(self):
        base_hit: DamageInstance = LunarHowlFormSwapV3().execute(
            in_feral_form=True,
            num_targets=1,
            target_tile_ascension_level=1,
        )
        split_hit: DamageInstance = LunarHowlFormSwapV3().execute(
            in_feral_form=True,
            num_targets=2,
            target_tile_ascension_level=2,
        )

        assert base_hit.base_potency == 160
        assert split_hit.base_potency == 85

    def test_fatal_pounce_active_and_v5(self):
        active: DamageInstance = FatalPounceActive().execute(
            stacks_of_prey_mark=2,
            target_is_on_phase_tile=True,
            confectance_index=4,
        )
        active_v5: DamageInstance = FatalPounceActiveV5().execute(
            stacks_of_prey_mark=2,
            target_is_on_phase_tile=True,
            confectance_index=4,
        )

        assert active.base_potency == 110
        assert active_v5.base_potency == 170

    def test_fatal_pounce_passive_v5(self):
        passive_v5: DamageInstance = FatalPouncePassiveV5().execute()

        assert passive_v5.base_potency == 60
        assert DamageTag.PASSIVE in passive_v5.tags
        assert DamageTag.INTERCEPTION in passive_v5.tags


class TestSoppo:
    def test_set_to_v0(self):
        doll = Soppo()
        doll.set_to_v0()

        assert isinstance(doll.hunting_fang, HuntingFang)
        assert isinstance(doll.vicious_bite, ViciousBite)
        assert isinstance(doll.lunar_howl, LunarHowl)
        assert isinstance(doll.lunar_howl_form_swap, LunarHowlFormSwap)
        assert isinstance(doll.fatal_pounce_active, FatalPounceActive)
        assert isinstance(doll.fatal_pounce_passive, FatalPouncePassive)

    def test_set_to_v1_v2_v3_v5(self):
        doll = Soppo()

        doll.set_to_v1()
        assert isinstance(doll.vicious_bite, ViciousBiteV1)

        doll.set_to_v2()
        assert isinstance(doll.lunar_howl, LunarHowlV2)

        doll.set_to_v3()
        assert isinstance(doll.lunar_howl_form_swap, LunarHowlFormSwapV3)

        doll.set_to_v5()
        assert isinstance(doll.fatal_pounce_active, FatalPounceActiveV5)
        assert isinstance(doll.fatal_pounce_passive, FatalPouncePassiveV5)

    def test_set_fortification_level(self):
        doll = Soppo()

        doll.set_fortification_level(FortificationLevel.SEGMENT04)
        assert isinstance(doll.lunar_howl, LunarHowlV2)
        assert isinstance(doll.lunar_howl_form_swap, LunarHowlFormSwapV3)

        doll.set_fortification_level(FortificationLevel.SEGMENT06)
        assert doll.fortification_level == FortificationLevel.SEGMENT06
        assert isinstance(doll.fatal_pounce_active, FatalPounceActiveV5)
        assert isinstance(doll.fatal_pounce_passive, FatalPouncePassiveV5)
