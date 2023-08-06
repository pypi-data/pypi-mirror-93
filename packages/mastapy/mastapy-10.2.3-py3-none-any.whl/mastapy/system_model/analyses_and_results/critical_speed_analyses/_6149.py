'''_6149.py

BearingCriticalSpeedAnalysis
'''


from typing import List

from mastapy.system_model.part_model import _2087
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _6415
from mastapy.system_model.analyses_and_results.critical_speed_analyses import _6177
from mastapy._internal.python_net import python_net_import

_BEARING_CRITICAL_SPEED_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.CriticalSpeedAnalyses', 'BearingCriticalSpeedAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('BearingCriticalSpeedAnalysis',)


class BearingCriticalSpeedAnalysis(_6177.ConnectorCriticalSpeedAnalysis):
    '''BearingCriticalSpeedAnalysis

    This is a mastapy class.
    '''

    TYPE = _BEARING_CRITICAL_SPEED_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'BearingCriticalSpeedAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2087.Bearing':
        '''Bearing: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2087.Bearing)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_load_case(self) -> '_6415.BearingLoadCase':
        '''BearingLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6415.BearingLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase else None

    @property
    def planetaries(self) -> 'List[BearingCriticalSpeedAnalysis]':
        '''List[BearingCriticalSpeedAnalysis]: 'Planetaries' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Planetaries, constructor.new(BearingCriticalSpeedAnalysis))
        return value
