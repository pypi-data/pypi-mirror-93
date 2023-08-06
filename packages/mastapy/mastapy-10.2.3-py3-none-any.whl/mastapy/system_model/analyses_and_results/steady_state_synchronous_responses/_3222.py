﻿'''_3222.py

RingPinsSteadyStateSynchronousResponse
'''


from mastapy.system_model.part_model.cycloidal import _2214
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6536
from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses import _3210
from mastapy._internal.python_net import python_net_import

_RING_PINS_STEADY_STATE_SYNCHRONOUS_RESPONSE = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SteadyStateSynchronousResponses', 'RingPinsSteadyStateSynchronousResponse')


__docformat__ = 'restructuredtext en'
__all__ = ('RingPinsSteadyStateSynchronousResponse',)


class RingPinsSteadyStateSynchronousResponse(_3210.MountableComponentSteadyStateSynchronousResponse):
    '''RingPinsSteadyStateSynchronousResponse

    This is a mastapy class.
    '''

    TYPE = _RING_PINS_STEADY_STATE_SYNCHRONOUS_RESPONSE

    __hash__ = None

    def __init__(self, instance_to_wrap: 'RingPinsSteadyStateSynchronousResponse.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2214.RingPins':
        '''RingPins: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2214.RingPins)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_load_case(self) -> '_6536.RingPinsLoadCase':
        '''RingPinsLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6536.RingPinsLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase else None
