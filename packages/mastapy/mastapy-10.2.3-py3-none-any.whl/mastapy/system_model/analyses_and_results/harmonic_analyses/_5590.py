﻿'''_5590.py

ConceptGearSetHarmonicAnalysis
'''


from typing import List

from mastapy.system_model.part_model.gears import _2166
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _6438
from mastapy.system_model.analyses_and_results.system_deflections import _2354
from mastapy.system_model.analyses_and_results.harmonic_analyses import _5588, _5589, _5634
from mastapy._internal.python_net import python_net_import

_CONCEPT_GEAR_SET_HARMONIC_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.HarmonicAnalyses', 'ConceptGearSetHarmonicAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('ConceptGearSetHarmonicAnalysis',)


class ConceptGearSetHarmonicAnalysis(_5634.GearSetHarmonicAnalysis):
    '''ConceptGearSetHarmonicAnalysis

    This is a mastapy class.
    '''

    TYPE = _CONCEPT_GEAR_SET_HARMONIC_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ConceptGearSetHarmonicAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def assembly_design(self) -> '_2166.ConceptGearSet':
        '''ConceptGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2166.ConceptGearSet)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def assembly_load_case(self) -> '_6438.ConceptGearSetLoadCase':
        '''ConceptGearSetLoadCase: 'AssemblyLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6438.ConceptGearSetLoadCase)(self.wrapped.AssemblyLoadCase) if self.wrapped.AssemblyLoadCase else None

    @property
    def system_deflection_results(self) -> '_2354.ConceptGearSetSystemDeflection':
        '''ConceptGearSetSystemDeflection: 'SystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2354.ConceptGearSetSystemDeflection)(self.wrapped.SystemDeflectionResults) if self.wrapped.SystemDeflectionResults else None

    @property
    def gears_harmonic_analysis(self) -> 'List[_5588.ConceptGearHarmonicAnalysis]':
        '''List[ConceptGearHarmonicAnalysis]: 'GearsHarmonicAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.GearsHarmonicAnalysis, constructor.new(_5588.ConceptGearHarmonicAnalysis))
        return value

    @property
    def concept_gears_harmonic_analysis(self) -> 'List[_5588.ConceptGearHarmonicAnalysis]':
        '''List[ConceptGearHarmonicAnalysis]: 'ConceptGearsHarmonicAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConceptGearsHarmonicAnalysis, constructor.new(_5588.ConceptGearHarmonicAnalysis))
        return value

    @property
    def meshes_harmonic_analysis(self) -> 'List[_5589.ConceptGearMeshHarmonicAnalysis]':
        '''List[ConceptGearMeshHarmonicAnalysis]: 'MeshesHarmonicAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.MeshesHarmonicAnalysis, constructor.new(_5589.ConceptGearMeshHarmonicAnalysis))
        return value

    @property
    def concept_meshes_harmonic_analysis(self) -> 'List[_5589.ConceptGearMeshHarmonicAnalysis]':
        '''List[ConceptGearMeshHarmonicAnalysis]: 'ConceptMeshesHarmonicAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConceptMeshesHarmonicAnalysis, constructor.new(_5589.ConceptGearMeshHarmonicAnalysis))
        return value
