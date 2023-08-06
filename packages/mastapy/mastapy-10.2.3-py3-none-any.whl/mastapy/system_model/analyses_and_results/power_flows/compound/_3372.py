﻿'''_3372.py

BevelDifferentialGearCompoundPowerFlow
'''


from typing import List

from mastapy.system_model.part_model.gears import _2075
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.power_flows import _3248
from mastapy.system_model.analyses_and_results.power_flows.compound import _3377
from mastapy._internal.python_net import python_net_import

_BEVEL_DIFFERENTIAL_GEAR_COMPOUND_POWER_FLOW = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.PowerFlows.Compound', 'BevelDifferentialGearCompoundPowerFlow')


__docformat__ = 'restructuredtext en'
__all__ = ('BevelDifferentialGearCompoundPowerFlow',)


class BevelDifferentialGearCompoundPowerFlow(_3377.BevelGearCompoundPowerFlow):
    '''BevelDifferentialGearCompoundPowerFlow

    This is a mastapy class.
    '''

    TYPE = _BEVEL_DIFFERENTIAL_GEAR_COMPOUND_POWER_FLOW

    __hash__ = None

    def __init__(self, instance_to_wrap: 'BevelDifferentialGearCompoundPowerFlow.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2075.BevelDifferentialGear':
        '''BevelDifferentialGear: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2075.BevelDifferentialGear)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_3248.BevelDifferentialGearPowerFlow]':
        '''List[BevelDifferentialGearPowerFlow]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_3248.BevelDifferentialGearPowerFlow))
        return value

    @property
    def component_power_flow_load_cases(self) -> 'List[_3248.BevelDifferentialGearPowerFlow]':
        '''List[BevelDifferentialGearPowerFlow]: 'ComponentPowerFlowLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentPowerFlowLoadCases, constructor.new(_3248.BevelDifferentialGearPowerFlow))
        return value
