from core.dolls.vector import *

from core.combat import DamageInstance
from core.types import DamageTag, FortificationLevel, StatType


class TestVectorSkills:
    def test_depressive_mentality(self):
        depressive_mentality: DamageInstance = DepressiveMentality().execute()

        assert depressive_mentality.base_potency == 80
        assert DamageTag.ACTIVE in depressive_mentality.tags
        assert DamageTag.BASIC in depressive_mentality.tags
        assert DamageTag.LIGHT_AMMO in depressive_mentality.tags
        assert DamageTag.TARGETED in depressive_mentality.tags
        assert DamageTag.PHYSICAL in depressive_mentality.tags
        assert depressive_mentality.group_name == "Depressive Mentality"

    def test_dead_end_meltdown(self):
        dead_end_meltdown: DamageInstance = DeadEndMeltdown().execute()

        assert dead_end_meltdown.base_potency == 120
        assert DamageTag.ACTIVE in dead_end_meltdown.tags
        assert DamageTag.BURN in dead_end_meltdown.tags
        assert DamageTag.PHASE in dead_end_meltdown.tags
        assert DamageTag.TARGETED in dead_end_meltdown.tags
        assert DamageTag.LIGHT_AMMO in dead_end_meltdown.tags
        assert dead_end_meltdown.group_name == "Dead End Meltdown"

    def test_dead_end_meltdown_fixed(self):
        dead_end_meltdown_fixed: DamageInstance = DeadEndMeltdownFixed().execute()

        assert dead_end_meltdown_fixed.base_potency == 50
        assert dead_end_meltdown_fixed.group_name == "Dead End Meltdown (Fixed)"

    def test_dead_end_meltdown_v3(self):
        dead_end_meltdown_v3: DamageInstance = DeadEndMeltdownV3().execute()
        dead_end_meltdown_fixed_v3: DamageInstance = DeadEndMeltdownFixedV3().execute()

        assert dead_end_meltdown_v3.base_potency == 150
        assert dead_end_meltdown_fixed_v3.base_potency == 80

    def test_portent_of_doom(self):
        portent_of_doom: DamageInstance = PortentOfDoom().execute()

        assert portent_of_doom.base_potency == 100
        assert DamageTag.ACTIVE in portent_of_doom.tags
        assert DamageTag.BURN in portent_of_doom.tags
        assert DamageTag.PHASE in portent_of_doom.tags
        assert DamageTag.TARGETED in portent_of_doom.tags
        assert portent_of_doom.group_name == "Portent of Doom"

    def test_portent_of_doom_v4(self):
        portent_of_doom_v4: DamageInstance = PortentOfDoomV4().execute()

        assert portent_of_doom_v4.base_potency == 130

    def test_searing_finale(self):
        searing_finale: DamageInstance = SearingFinale().execute()

        assert searing_finale.base_potency == 60
        assert DamageTag.ACTIVE in searing_finale.tags
        assert DamageTag.BURN in searing_finale.tags
        assert DamageTag.PHASE in searing_finale.tags
        assert DamageTag.ULTIMATE in searing_finale.tags
        assert DamageTag.AREA_OF_EFFECT in searing_finale.tags
        assert searing_finale.group_name == "Searing Finale"

    def test_emergency_support(self):
        emergency_support: DamageInstance = EmergencySupport().execute()

        assert emergency_support.base_potency == 60
        assert DamageTag.PASSIVE in emergency_support.tags
        assert DamageTag.SUPPORT_ACTION in emergency_support.tags
        assert DamageTag.PHASE in emergency_support.tags
        assert DamageTag.BURN in emergency_support.tags
        assert DamageTag.LIGHT_AMMO in emergency_support.tags
        assert DamageTag.TARGETED in emergency_support.tags
        assert emergency_support.group_name == "Emergency Support"

    def test_overheat_combustion(self):
        overheat_combustion: DamageInstance = OverheatCombustion().execute()
        overheat_combustion_v5: DamageInstance = OverheatCombustionV5().execute()

        assert overheat_combustion.base_potency == 20
        assert overheat_combustion_v5.base_potency == 30
        assert overheat_combustion.group_name == "Overheat Combustion"


class TestVector:
    def test_set_to_v0(self):
        vector: Vector = Vector()
        vector.set_to_v0()

        assert isinstance(vector.depressive_mentality, DepressiveMentality)
        assert isinstance(vector.dead_end_meltdown, DeadEndMeltdown)
        assert isinstance(vector.dead_end_meltdown_fixed, DeadEndMeltdownFixed)
        assert isinstance(vector.portent_of_doom, PortentOfDoom)
        assert isinstance(vector.searing_finale, SearingFinale)
        assert isinstance(vector.emergency_support, EmergencySupport)
        assert isinstance(vector.overheat_combustion, OverheatCombustion)
        assert vector.multiplicative_modifiers.basic_attributes[StatType.ATTACK] == 10

    def test_set_to_v3(self):
        vector: Vector = Vector()
        vector.set_to_v3()

        assert isinstance(vector.dead_end_meltdown, DeadEndMeltdownV3)
        assert isinstance(vector.dead_end_meltdown_fixed, DeadEndMeltdownFixedV3)

    def test_set_to_v4(self):
        vector: Vector = Vector()
        vector.set_to_v4()

        assert isinstance(vector.portent_of_doom, PortentOfDoomV4)

    def test_set_to_v5(self):
        vector: Vector = Vector()
        vector.set_to_v5()

        assert isinstance(vector.overheat_combustion, OverheatCombustionV5)
        assert vector.multiplicative_modifiers.basic_attributes[StatType.ATTACK] == 20

    def test_set_to_v6(self):
        vector: Vector = Vector()
        vector.set_to_v6()

        assert isinstance(vector.overheat_combustion, OverheatCombustionV5)
        assert vector.multiplicative_modifiers.basic_attributes[StatType.ATTACK] == 20

    def test_set_to_fortification_level(self):
        vector: Vector = Vector()

        vector.set_fortification_level(FortificationLevel.SEGMENT00)
        assert isinstance(vector.portent_of_doom, PortentOfDoom)

        vector.set_fortification_level(FortificationLevel.SEGMENT03)
        assert isinstance(vector.dead_end_meltdown, DeadEndMeltdownV3)

        vector.set_fortification_level(FortificationLevel.SEGMENT04)
        assert isinstance(vector.portent_of_doom, PortentOfDoomV4)

        vector.set_fortification_level(FortificationLevel.SEGMENT05)
        assert isinstance(vector.overheat_combustion, OverheatCombustionV5)

        vector.set_fortification_level(FortificationLevel.SEGMENT06)
        assert vector.fortification_level == FortificationLevel.SEGMENT06
