﻿'''_3422.py

ConceptCouplingStabilityAnalysis
'''


from mastapy.system_model.part_model.couplings import _2225
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6435
from mastapy.system_model.analyses_and_results.stability_analyses import _3433
from mastapy._internal.python_net import python_net_import

_CONCEPT_COUPLING_STABILITY_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StabilityAnalyses', 'ConceptCouplingStabilityAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('ConceptCouplingStabilityAnalysis',)


class ConceptCouplingStabilityAnalysis(_3433.CouplingStabilityAnalysis):
    '''ConceptCouplingStabilityAnalysis

    This is a mastapy class.
    '''

    TYPE = _CONCEPT_COUPLING_STABILITY_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ConceptCouplingStabilityAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def assembly_design(self) -> '_2225.ConceptCoupling':
        '''ConceptCoupling: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2225.ConceptCoupling)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def assembly_load_case(self) -> '_6435.ConceptCouplingLoadCase':
        '''ConceptCouplingLoadCase: 'AssemblyLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6435.ConceptCouplingLoadCase)(self.wrapped.AssemblyLoadCase) if self.wrapped.AssemblyLoadCase else None
