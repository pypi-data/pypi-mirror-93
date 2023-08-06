﻿'''_3489.py

RootAssemblyStabilityAnalysis
'''


from mastapy.system_model.part_model import _2120
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.stability_analyses import _2284, _3401
from mastapy._internal.python_net import python_net_import

_ROOT_ASSEMBLY_STABILITY_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StabilityAnalyses', 'RootAssemblyStabilityAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('RootAssemblyStabilityAnalysis',)


class RootAssemblyStabilityAnalysis(_3401.AssemblyStabilityAnalysis):
    '''RootAssemblyStabilityAnalysis

    This is a mastapy class.
    '''

    TYPE = _ROOT_ASSEMBLY_STABILITY_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'RootAssemblyStabilityAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def assembly_design(self) -> '_2120.RootAssembly':
        '''RootAssembly: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2120.RootAssembly)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def stability_analysis_inputs(self) -> '_2284.StabilityAnalysis':
        '''StabilityAnalysis: 'StabilityAnalysisInputs' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2284.StabilityAnalysis)(self.wrapped.StabilityAnalysisInputs) if self.wrapped.StabilityAnalysisInputs else None
