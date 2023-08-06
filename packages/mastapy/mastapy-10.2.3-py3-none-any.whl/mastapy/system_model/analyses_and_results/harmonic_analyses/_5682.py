﻿'''_5682.py

SpiralBevelGearSetHarmonicAnalysis
'''


from typing import List

from mastapy.system_model.part_model.gears import _2188
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _6549
from mastapy.system_model.analyses_and_results.system_deflections import _2439
from mastapy.system_model.analyses_and_results.harmonic_analyses import _5680, _5681, _5576
from mastapy._internal.python_net import python_net_import

_SPIRAL_BEVEL_GEAR_SET_HARMONIC_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.HarmonicAnalyses', 'SpiralBevelGearSetHarmonicAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('SpiralBevelGearSetHarmonicAnalysis',)


class SpiralBevelGearSetHarmonicAnalysis(_5576.BevelGearSetHarmonicAnalysis):
    '''SpiralBevelGearSetHarmonicAnalysis

    This is a mastapy class.
    '''

    TYPE = _SPIRAL_BEVEL_GEAR_SET_HARMONIC_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'SpiralBevelGearSetHarmonicAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def assembly_design(self) -> '_2188.SpiralBevelGearSet':
        '''SpiralBevelGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2188.SpiralBevelGearSet)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def assembly_load_case(self) -> '_6549.SpiralBevelGearSetLoadCase':
        '''SpiralBevelGearSetLoadCase: 'AssemblyLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6549.SpiralBevelGearSetLoadCase)(self.wrapped.AssemblyLoadCase) if self.wrapped.AssemblyLoadCase else None

    @property
    def system_deflection_results(self) -> '_2439.SpiralBevelGearSetSystemDeflection':
        '''SpiralBevelGearSetSystemDeflection: 'SystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2439.SpiralBevelGearSetSystemDeflection)(self.wrapped.SystemDeflectionResults) if self.wrapped.SystemDeflectionResults else None

    @property
    def gears_harmonic_analysis(self) -> 'List[_5680.SpiralBevelGearHarmonicAnalysis]':
        '''List[SpiralBevelGearHarmonicAnalysis]: 'GearsHarmonicAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.GearsHarmonicAnalysis, constructor.new(_5680.SpiralBevelGearHarmonicAnalysis))
        return value

    @property
    def spiral_bevel_gears_harmonic_analysis(self) -> 'List[_5680.SpiralBevelGearHarmonicAnalysis]':
        '''List[SpiralBevelGearHarmonicAnalysis]: 'SpiralBevelGearsHarmonicAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.SpiralBevelGearsHarmonicAnalysis, constructor.new(_5680.SpiralBevelGearHarmonicAnalysis))
        return value

    @property
    def meshes_harmonic_analysis(self) -> 'List[_5681.SpiralBevelGearMeshHarmonicAnalysis]':
        '''List[SpiralBevelGearMeshHarmonicAnalysis]: 'MeshesHarmonicAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.MeshesHarmonicAnalysis, constructor.new(_5681.SpiralBevelGearMeshHarmonicAnalysis))
        return value

    @property
    def spiral_bevel_meshes_harmonic_analysis(self) -> 'List[_5681.SpiralBevelGearMeshHarmonicAnalysis]':
        '''List[SpiralBevelGearMeshHarmonicAnalysis]: 'SpiralBevelMeshesHarmonicAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.SpiralBevelMeshesHarmonicAnalysis, constructor.new(_5681.SpiralBevelGearMeshHarmonicAnalysis))
        return value
