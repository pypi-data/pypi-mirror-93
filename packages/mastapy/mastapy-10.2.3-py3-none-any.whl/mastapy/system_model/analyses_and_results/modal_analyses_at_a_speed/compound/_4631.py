'''_4631.py

AssemblyCompoundModalAnalysisAtASpeed
'''


from typing import List

from mastapy.system_model.part_model import _2021, _2058
from mastapy._internal import constructor, conversion
from mastapy._internal.cast_exception import CastException
from mastapy.system_model.analyses_and_results.modal_analyses_at_a_speed import _4509
from mastapy.system_model.analyses_and_results.modal_analyses_at_a_speed.compound import (
    _4632, _4634, _4637, _4643,
    _4644, _4645, _4650, _4655,
    _4665, _4669, _4675, _4676,
    _4683, _4684, _4691, _4694,
    _4695, _4696, _4698, _4700,
    _4705, _4706, _4707, _4714,
    _4709, _4713, _4719, _4720,
    _4725, _4728, _4731, _4735,
    _4739, _4743, _4746, _4626
)
from mastapy._internal.python_net import python_net_import

_ASSEMBLY_COMPOUND_MODAL_ANALYSIS_AT_A_SPEED = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtASpeed.Compound', 'AssemblyCompoundModalAnalysisAtASpeed')


__docformat__ = 'restructuredtext en'
__all__ = ('AssemblyCompoundModalAnalysisAtASpeed',)


class AssemblyCompoundModalAnalysisAtASpeed(_4626.AbstractAssemblyCompoundModalAnalysisAtASpeed):
    '''AssemblyCompoundModalAnalysisAtASpeed

    This is a mastapy class.
    '''

    TYPE = _ASSEMBLY_COMPOUND_MODAL_ANALYSIS_AT_A_SPEED

    __hash__ = None

    def __init__(self, instance_to_wrap: 'AssemblyCompoundModalAnalysisAtASpeed.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2021.Assembly':
        '''Assembly: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2021.Assembly.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to Assembly. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDesign.__class__)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def assembly_design(self) -> '_2021.Assembly':
        '''Assembly: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2021.Assembly.TYPE not in self.wrapped.AssemblyDesign.__class__.__mro__:
            raise CastException('Failed to cast assembly_design to Assembly. Expected: {}.'.format(self.wrapped.AssemblyDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.AssemblyDesign.__class__)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_4509.AssemblyModalAnalysisAtASpeed]':
        '''List[AssemblyModalAnalysisAtASpeed]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_4509.AssemblyModalAnalysisAtASpeed))
        return value

    @property
    def assembly_modal_analysis_at_a_speed_load_cases(self) -> 'List[_4509.AssemblyModalAnalysisAtASpeed]':
        '''List[AssemblyModalAnalysisAtASpeed]: 'AssemblyModalAnalysisAtASpeedLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyModalAnalysisAtASpeedLoadCases, constructor.new(_4509.AssemblyModalAnalysisAtASpeed))
        return value

    @property
    def bearings(self) -> 'List[_4632.BearingCompoundModalAnalysisAtASpeed]':
        '''List[BearingCompoundModalAnalysisAtASpeed]: 'Bearings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Bearings, constructor.new(_4632.BearingCompoundModalAnalysisAtASpeed))
        return value

    @property
    def belt_drives(self) -> 'List[_4634.BeltDriveCompoundModalAnalysisAtASpeed]':
        '''List[BeltDriveCompoundModalAnalysisAtASpeed]: 'BeltDrives' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BeltDrives, constructor.new(_4634.BeltDriveCompoundModalAnalysisAtASpeed))
        return value

    @property
    def bevel_differential_gear_sets(self) -> 'List[_4637.BevelDifferentialGearSetCompoundModalAnalysisAtASpeed]':
        '''List[BevelDifferentialGearSetCompoundModalAnalysisAtASpeed]: 'BevelDifferentialGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BevelDifferentialGearSets, constructor.new(_4637.BevelDifferentialGearSetCompoundModalAnalysisAtASpeed))
        return value

    @property
    def bolts(self) -> 'List[_4643.BoltCompoundModalAnalysisAtASpeed]':
        '''List[BoltCompoundModalAnalysisAtASpeed]: 'Bolts' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Bolts, constructor.new(_4643.BoltCompoundModalAnalysisAtASpeed))
        return value

    @property
    def bolted_joints(self) -> 'List[_4644.BoltedJointCompoundModalAnalysisAtASpeed]':
        '''List[BoltedJointCompoundModalAnalysisAtASpeed]: 'BoltedJoints' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BoltedJoints, constructor.new(_4644.BoltedJointCompoundModalAnalysisAtASpeed))
        return value

    @property
    def clutches(self) -> 'List[_4645.ClutchCompoundModalAnalysisAtASpeed]':
        '''List[ClutchCompoundModalAnalysisAtASpeed]: 'Clutches' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Clutches, constructor.new(_4645.ClutchCompoundModalAnalysisAtASpeed))
        return value

    @property
    def concept_couplings(self) -> 'List[_4650.ConceptCouplingCompoundModalAnalysisAtASpeed]':
        '''List[ConceptCouplingCompoundModalAnalysisAtASpeed]: 'ConceptCouplings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConceptCouplings, constructor.new(_4650.ConceptCouplingCompoundModalAnalysisAtASpeed))
        return value

    @property
    def concept_gear_sets(self) -> 'List[_4655.ConceptGearSetCompoundModalAnalysisAtASpeed]':
        '''List[ConceptGearSetCompoundModalAnalysisAtASpeed]: 'ConceptGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConceptGearSets, constructor.new(_4655.ConceptGearSetCompoundModalAnalysisAtASpeed))
        return value

    @property
    def cv_ts(self) -> 'List[_4665.CVTCompoundModalAnalysisAtASpeed]':
        '''List[CVTCompoundModalAnalysisAtASpeed]: 'CVTs' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CVTs, constructor.new(_4665.CVTCompoundModalAnalysisAtASpeed))
        return value

    @property
    def cylindrical_gear_sets(self) -> 'List[_4669.CylindricalGearSetCompoundModalAnalysisAtASpeed]':
        '''List[CylindricalGearSetCompoundModalAnalysisAtASpeed]: 'CylindricalGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CylindricalGearSets, constructor.new(_4669.CylindricalGearSetCompoundModalAnalysisAtASpeed))
        return value

    @property
    def face_gear_sets(self) -> 'List[_4675.FaceGearSetCompoundModalAnalysisAtASpeed]':
        '''List[FaceGearSetCompoundModalAnalysisAtASpeed]: 'FaceGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.FaceGearSets, constructor.new(_4675.FaceGearSetCompoundModalAnalysisAtASpeed))
        return value

    @property
    def flexible_pin_assemblies(self) -> 'List[_4676.FlexiblePinAssemblyCompoundModalAnalysisAtASpeed]':
        '''List[FlexiblePinAssemblyCompoundModalAnalysisAtASpeed]: 'FlexiblePinAssemblies' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.FlexiblePinAssemblies, constructor.new(_4676.FlexiblePinAssemblyCompoundModalAnalysisAtASpeed))
        return value

    @property
    def hypoid_gear_sets(self) -> 'List[_4683.HypoidGearSetCompoundModalAnalysisAtASpeed]':
        '''List[HypoidGearSetCompoundModalAnalysisAtASpeed]: 'HypoidGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.HypoidGearSets, constructor.new(_4683.HypoidGearSetCompoundModalAnalysisAtASpeed))
        return value

    @property
    def imported_fe_components(self) -> 'List[_4684.ImportedFEComponentCompoundModalAnalysisAtASpeed]':
        '''List[ImportedFEComponentCompoundModalAnalysisAtASpeed]: 'ImportedFEComponents' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ImportedFEComponents, constructor.new(_4684.ImportedFEComponentCompoundModalAnalysisAtASpeed))
        return value

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_sets(self) -> 'List[_4691.KlingelnbergCycloPalloidHypoidGearSetCompoundModalAnalysisAtASpeed]':
        '''List[KlingelnbergCycloPalloidHypoidGearSetCompoundModalAnalysisAtASpeed]: 'KlingelnbergCycloPalloidHypoidGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.KlingelnbergCycloPalloidHypoidGearSets, constructor.new(_4691.KlingelnbergCycloPalloidHypoidGearSetCompoundModalAnalysisAtASpeed))
        return value

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_sets(self) -> 'List[_4694.KlingelnbergCycloPalloidSpiralBevelGearSetCompoundModalAnalysisAtASpeed]':
        '''List[KlingelnbergCycloPalloidSpiralBevelGearSetCompoundModalAnalysisAtASpeed]: 'KlingelnbergCycloPalloidSpiralBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.KlingelnbergCycloPalloidSpiralBevelGearSets, constructor.new(_4694.KlingelnbergCycloPalloidSpiralBevelGearSetCompoundModalAnalysisAtASpeed))
        return value

    @property
    def mass_discs(self) -> 'List[_4695.MassDiscCompoundModalAnalysisAtASpeed]':
        '''List[MassDiscCompoundModalAnalysisAtASpeed]: 'MassDiscs' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.MassDiscs, constructor.new(_4695.MassDiscCompoundModalAnalysisAtASpeed))
        return value

    @property
    def measurement_components(self) -> 'List[_4696.MeasurementComponentCompoundModalAnalysisAtASpeed]':
        '''List[MeasurementComponentCompoundModalAnalysisAtASpeed]: 'MeasurementComponents' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.MeasurementComponents, constructor.new(_4696.MeasurementComponentCompoundModalAnalysisAtASpeed))
        return value

    @property
    def oil_seals(self) -> 'List[_4698.OilSealCompoundModalAnalysisAtASpeed]':
        '''List[OilSealCompoundModalAnalysisAtASpeed]: 'OilSeals' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.OilSeals, constructor.new(_4698.OilSealCompoundModalAnalysisAtASpeed))
        return value

    @property
    def part_to_part_shear_couplings(self) -> 'List[_4700.PartToPartShearCouplingCompoundModalAnalysisAtASpeed]':
        '''List[PartToPartShearCouplingCompoundModalAnalysisAtASpeed]: 'PartToPartShearCouplings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PartToPartShearCouplings, constructor.new(_4700.PartToPartShearCouplingCompoundModalAnalysisAtASpeed))
        return value

    @property
    def planet_carriers(self) -> 'List[_4705.PlanetCarrierCompoundModalAnalysisAtASpeed]':
        '''List[PlanetCarrierCompoundModalAnalysisAtASpeed]: 'PlanetCarriers' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PlanetCarriers, constructor.new(_4705.PlanetCarrierCompoundModalAnalysisAtASpeed))
        return value

    @property
    def point_loads(self) -> 'List[_4706.PointLoadCompoundModalAnalysisAtASpeed]':
        '''List[PointLoadCompoundModalAnalysisAtASpeed]: 'PointLoads' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PointLoads, constructor.new(_4706.PointLoadCompoundModalAnalysisAtASpeed))
        return value

    @property
    def power_loads(self) -> 'List[_4707.PowerLoadCompoundModalAnalysisAtASpeed]':
        '''List[PowerLoadCompoundModalAnalysisAtASpeed]: 'PowerLoads' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PowerLoads, constructor.new(_4707.PowerLoadCompoundModalAnalysisAtASpeed))
        return value

    @property
    def shaft_hub_connections(self) -> 'List[_4714.ShaftHubConnectionCompoundModalAnalysisAtASpeed]':
        '''List[ShaftHubConnectionCompoundModalAnalysisAtASpeed]: 'ShaftHubConnections' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ShaftHubConnections, constructor.new(_4714.ShaftHubConnectionCompoundModalAnalysisAtASpeed))
        return value

    @property
    def rolling_ring_assemblies(self) -> 'List[_4709.RollingRingAssemblyCompoundModalAnalysisAtASpeed]':
        '''List[RollingRingAssemblyCompoundModalAnalysisAtASpeed]: 'RollingRingAssemblies' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.RollingRingAssemblies, constructor.new(_4709.RollingRingAssemblyCompoundModalAnalysisAtASpeed))
        return value

    @property
    def shafts(self) -> 'List[_4713.ShaftCompoundModalAnalysisAtASpeed]':
        '''List[ShaftCompoundModalAnalysisAtASpeed]: 'Shafts' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Shafts, constructor.new(_4713.ShaftCompoundModalAnalysisAtASpeed))
        return value

    @property
    def spiral_bevel_gear_sets(self) -> 'List[_4719.SpiralBevelGearSetCompoundModalAnalysisAtASpeed]':
        '''List[SpiralBevelGearSetCompoundModalAnalysisAtASpeed]: 'SpiralBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.SpiralBevelGearSets, constructor.new(_4719.SpiralBevelGearSetCompoundModalAnalysisAtASpeed))
        return value

    @property
    def spring_dampers(self) -> 'List[_4720.SpringDamperCompoundModalAnalysisAtASpeed]':
        '''List[SpringDamperCompoundModalAnalysisAtASpeed]: 'SpringDampers' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.SpringDampers, constructor.new(_4720.SpringDamperCompoundModalAnalysisAtASpeed))
        return value

    @property
    def straight_bevel_diff_gear_sets(self) -> 'List[_4725.StraightBevelDiffGearSetCompoundModalAnalysisAtASpeed]':
        '''List[StraightBevelDiffGearSetCompoundModalAnalysisAtASpeed]: 'StraightBevelDiffGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.StraightBevelDiffGearSets, constructor.new(_4725.StraightBevelDiffGearSetCompoundModalAnalysisAtASpeed))
        return value

    @property
    def straight_bevel_gear_sets(self) -> 'List[_4728.StraightBevelGearSetCompoundModalAnalysisAtASpeed]':
        '''List[StraightBevelGearSetCompoundModalAnalysisAtASpeed]: 'StraightBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.StraightBevelGearSets, constructor.new(_4728.StraightBevelGearSetCompoundModalAnalysisAtASpeed))
        return value

    @property
    def synchronisers(self) -> 'List[_4731.SynchroniserCompoundModalAnalysisAtASpeed]':
        '''List[SynchroniserCompoundModalAnalysisAtASpeed]: 'Synchronisers' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Synchronisers, constructor.new(_4731.SynchroniserCompoundModalAnalysisAtASpeed))
        return value

    @property
    def torque_converters(self) -> 'List[_4735.TorqueConverterCompoundModalAnalysisAtASpeed]':
        '''List[TorqueConverterCompoundModalAnalysisAtASpeed]: 'TorqueConverters' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.TorqueConverters, constructor.new(_4735.TorqueConverterCompoundModalAnalysisAtASpeed))
        return value

    @property
    def unbalanced_masses(self) -> 'List[_4739.UnbalancedMassCompoundModalAnalysisAtASpeed]':
        '''List[UnbalancedMassCompoundModalAnalysisAtASpeed]: 'UnbalancedMasses' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.UnbalancedMasses, constructor.new(_4739.UnbalancedMassCompoundModalAnalysisAtASpeed))
        return value

    @property
    def worm_gear_sets(self) -> 'List[_4743.WormGearSetCompoundModalAnalysisAtASpeed]':
        '''List[WormGearSetCompoundModalAnalysisAtASpeed]: 'WormGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.WormGearSets, constructor.new(_4743.WormGearSetCompoundModalAnalysisAtASpeed))
        return value

    @property
    def zerol_bevel_gear_sets(self) -> 'List[_4746.ZerolBevelGearSetCompoundModalAnalysisAtASpeed]':
        '''List[ZerolBevelGearSetCompoundModalAnalysisAtASpeed]: 'ZerolBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ZerolBevelGearSets, constructor.new(_4746.ZerolBevelGearSetCompoundModalAnalysisAtASpeed))
        return value
