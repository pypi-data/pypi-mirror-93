﻿'''_5990.py

SynchroniserDynamicAnalysis
'''


from mastapy.system_model.part_model.couplings import _2245
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6563
from mastapy.system_model.analyses_and_results.dynamic_analyses import _5975
from mastapy._internal.python_net import python_net_import

_SYNCHRONISER_DYNAMIC_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.DynamicAnalyses', 'SynchroniserDynamicAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('SynchroniserDynamicAnalysis',)


class SynchroniserDynamicAnalysis(_5975.SpecialisedAssemblyDynamicAnalysis):
    '''SynchroniserDynamicAnalysis

    This is a mastapy class.
    '''

    TYPE = _SYNCHRONISER_DYNAMIC_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'SynchroniserDynamicAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def assembly_design(self) -> '_2245.Synchroniser':
        '''Synchroniser: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2245.Synchroniser)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def assembly_load_case(self) -> '_6563.SynchroniserLoadCase':
        '''SynchroniserLoadCase: 'AssemblyLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6563.SynchroniserLoadCase)(self.wrapped.AssemblyLoadCase) if self.wrapped.AssemblyLoadCase else None
