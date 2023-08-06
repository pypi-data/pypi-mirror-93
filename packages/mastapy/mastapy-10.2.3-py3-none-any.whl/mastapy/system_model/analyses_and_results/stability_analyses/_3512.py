﻿'''_3512.py

SynchroniserSleeveStabilityAnalysis
'''


from mastapy.system_model.part_model.couplings import _2249
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6565
from mastapy.system_model.analyses_and_results.stability_analyses import _3511
from mastapy._internal.python_net import python_net_import

_SYNCHRONISER_SLEEVE_STABILITY_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StabilityAnalyses', 'SynchroniserSleeveStabilityAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('SynchroniserSleeveStabilityAnalysis',)


class SynchroniserSleeveStabilityAnalysis(_3511.SynchroniserPartStabilityAnalysis):
    '''SynchroniserSleeveStabilityAnalysis

    This is a mastapy class.
    '''

    TYPE = _SYNCHRONISER_SLEEVE_STABILITY_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'SynchroniserSleeveStabilityAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2249.SynchroniserSleeve':
        '''SynchroniserSleeve: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2249.SynchroniserSleeve)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_load_case(self) -> '_6565.SynchroniserSleeveLoadCase':
        '''SynchroniserSleeveLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6565.SynchroniserSleeveLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase else None
