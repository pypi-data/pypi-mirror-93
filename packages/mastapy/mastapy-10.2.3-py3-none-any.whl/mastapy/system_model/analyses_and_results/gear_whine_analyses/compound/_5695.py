﻿'''_5695.py

BearingCompoundGearWhineAnalysis
'''


from typing import List

from mastapy.system_model.part_model import _2004
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.gear_whine_analyses import _5280
from mastapy.system_model.analyses_and_results.gear_whine_analyses.compound import _5723
from mastapy._internal.python_net import python_net_import

_BEARING_COMPOUND_GEAR_WHINE_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.GearWhineAnalyses.Compound', 'BearingCompoundGearWhineAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('BearingCompoundGearWhineAnalysis',)


class BearingCompoundGearWhineAnalysis(_5723.ConnectorCompoundGearWhineAnalysis):
    '''BearingCompoundGearWhineAnalysis

    This is a mastapy class.
    '''

    TYPE = _BEARING_COMPOUND_GEAR_WHINE_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'BearingCompoundGearWhineAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2004.Bearing':
        '''Bearing: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2004.Bearing)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_5280.BearingGearWhineAnalysis]':
        '''List[BearingGearWhineAnalysis]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_5280.BearingGearWhineAnalysis))
        return value

    @property
    def component_gear_whine_analysis_load_cases(self) -> 'List[_5280.BearingGearWhineAnalysis]':
        '''List[BearingGearWhineAnalysis]: 'ComponentGearWhineAnalysisLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentGearWhineAnalysisLoadCases, constructor.new(_5280.BearingGearWhineAnalysis))
        return value

    @property
    def planetaries(self) -> 'List[BearingCompoundGearWhineAnalysis]':
        '''List[BearingCompoundGearWhineAnalysis]: 'Planetaries' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Planetaries, constructor.new(BearingCompoundGearWhineAnalysis))
        return value
