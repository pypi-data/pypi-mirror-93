﻿'''_3777.py

SynchroniserHalfPowerFlow
'''


from mastapy.system_model.analyses_and_results.power_flows import _3682, _3778
from mastapy._internal import constructor
from mastapy.system_model.part_model.couplings import _2247
from mastapy.system_model.analyses_and_results.static_loads import _6562
from mastapy._internal.python_net import python_net_import

_SYNCHRONISER_HALF_POWER_FLOW = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.PowerFlows', 'SynchroniserHalfPowerFlow')


__docformat__ = 'restructuredtext en'
__all__ = ('SynchroniserHalfPowerFlow',)


class SynchroniserHalfPowerFlow(_3778.SynchroniserPartPowerFlow):
    '''SynchroniserHalfPowerFlow

    This is a mastapy class.
    '''

    TYPE = _SYNCHRONISER_HALF_POWER_FLOW

    __hash__ = None

    def __init__(self, instance_to_wrap: 'SynchroniserHalfPowerFlow.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def clutch_connection(self) -> '_3682.ClutchConnectionPowerFlow':
        '''ClutchConnectionPowerFlow: 'ClutchConnection' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_3682.ClutchConnectionPowerFlow)(self.wrapped.ClutchConnection) if self.wrapped.ClutchConnection else None

    @property
    def component_design(self) -> '_2247.SynchroniserHalf':
        '''SynchroniserHalf: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2247.SynchroniserHalf)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_load_case(self) -> '_6562.SynchroniserHalfLoadCase':
        '''SynchroniserHalfLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6562.SynchroniserHalfLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase else None
