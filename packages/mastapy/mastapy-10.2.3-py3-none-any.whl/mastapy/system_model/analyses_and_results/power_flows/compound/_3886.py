﻿'''_3886.py

RollingRingCompoundPowerFlow
'''


from typing import List

from mastapy.system_model.part_model.couplings import _2240
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.power_flows import _3757
from mastapy.system_model.analyses_and_results.power_flows.compound import _3833
from mastapy._internal.python_net import python_net_import

_ROLLING_RING_COMPOUND_POWER_FLOW = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.PowerFlows.Compound', 'RollingRingCompoundPowerFlow')


__docformat__ = 'restructuredtext en'
__all__ = ('RollingRingCompoundPowerFlow',)


class RollingRingCompoundPowerFlow(_3833.CouplingHalfCompoundPowerFlow):
    '''RollingRingCompoundPowerFlow

    This is a mastapy class.
    '''

    TYPE = _ROLLING_RING_COMPOUND_POWER_FLOW

    __hash__ = None

    def __init__(self, instance_to_wrap: 'RollingRingCompoundPowerFlow.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2240.RollingRing':
        '''RollingRing: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2240.RollingRing)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_3757.RollingRingPowerFlow]':
        '''List[RollingRingPowerFlow]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_3757.RollingRingPowerFlow))
        return value

    @property
    def component_power_flow_load_cases(self) -> 'List[_3757.RollingRingPowerFlow]':
        '''List[RollingRingPowerFlow]: 'ComponentPowerFlowLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentPowerFlowLoadCases, constructor.new(_3757.RollingRingPowerFlow))
        return value
