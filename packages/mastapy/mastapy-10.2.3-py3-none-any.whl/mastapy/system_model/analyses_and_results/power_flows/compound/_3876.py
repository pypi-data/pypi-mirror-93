﻿'''_3876.py

PartToPartShearCouplingHalfCompoundPowerFlow
'''


from typing import List

from mastapy.system_model.part_model.couplings import _2233
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.power_flows import _3743
from mastapy.system_model.analyses_and_results.power_flows.compound import _3833
from mastapy._internal.python_net import python_net_import

_PART_TO_PART_SHEAR_COUPLING_HALF_COMPOUND_POWER_FLOW = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.PowerFlows.Compound', 'PartToPartShearCouplingHalfCompoundPowerFlow')


__docformat__ = 'restructuredtext en'
__all__ = ('PartToPartShearCouplingHalfCompoundPowerFlow',)


class PartToPartShearCouplingHalfCompoundPowerFlow(_3833.CouplingHalfCompoundPowerFlow):
    '''PartToPartShearCouplingHalfCompoundPowerFlow

    This is a mastapy class.
    '''

    TYPE = _PART_TO_PART_SHEAR_COUPLING_HALF_COMPOUND_POWER_FLOW

    __hash__ = None

    def __init__(self, instance_to_wrap: 'PartToPartShearCouplingHalfCompoundPowerFlow.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2233.PartToPartShearCouplingHalf':
        '''PartToPartShearCouplingHalf: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2233.PartToPartShearCouplingHalf)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_3743.PartToPartShearCouplingHalfPowerFlow]':
        '''List[PartToPartShearCouplingHalfPowerFlow]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_3743.PartToPartShearCouplingHalfPowerFlow))
        return value

    @property
    def component_power_flow_load_cases(self) -> 'List[_3743.PartToPartShearCouplingHalfPowerFlow]':
        '''List[PartToPartShearCouplingHalfPowerFlow]: 'ComponentPowerFlowLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentPowerFlowLoadCases, constructor.new(_3743.PartToPartShearCouplingHalfPowerFlow))
        return value
