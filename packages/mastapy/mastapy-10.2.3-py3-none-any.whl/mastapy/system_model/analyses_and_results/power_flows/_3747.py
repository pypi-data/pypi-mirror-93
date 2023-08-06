﻿'''_3747.py

PlanetCarrierPowerFlow
'''


from mastapy.system_model.part_model import _2115
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6528
from mastapy.system_model.analyses_and_results.power_flows import _3739
from mastapy._internal.python_net import python_net_import

_PLANET_CARRIER_POWER_FLOW = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.PowerFlows', 'PlanetCarrierPowerFlow')


__docformat__ = 'restructuredtext en'
__all__ = ('PlanetCarrierPowerFlow',)


class PlanetCarrierPowerFlow(_3739.MountableComponentPowerFlow):
    '''PlanetCarrierPowerFlow

    This is a mastapy class.
    '''

    TYPE = _PLANET_CARRIER_POWER_FLOW

    __hash__ = None

    def __init__(self, instance_to_wrap: 'PlanetCarrierPowerFlow.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2115.PlanetCarrier':
        '''PlanetCarrier: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2115.PlanetCarrier)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_load_case(self) -> '_6528.PlanetCarrierLoadCase':
        '''PlanetCarrierLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6528.PlanetCarrierLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase else None
