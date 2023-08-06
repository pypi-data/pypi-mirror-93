﻿'''_4009.py

CoaxialConnectionModalAnalysesAtSpeeds
'''


from mastapy.system_model.connections_and_sockets import _1852
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6094
from mastapy.system_model.analyses_and_results.modal_analyses_at_speeds_ns import _4079
from mastapy._internal.python_net import python_net_import

_COAXIAL_CONNECTION_MODAL_ANALYSES_AT_SPEEDS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtSpeedsNS', 'CoaxialConnectionModalAnalysesAtSpeeds')


__docformat__ = 'restructuredtext en'
__all__ = ('CoaxialConnectionModalAnalysesAtSpeeds',)


class CoaxialConnectionModalAnalysesAtSpeeds(_4079.ShaftToMountableComponentConnectionModalAnalysesAtSpeeds):
    '''CoaxialConnectionModalAnalysesAtSpeeds

    This is a mastapy class.
    '''

    TYPE = _COAXIAL_CONNECTION_MODAL_ANALYSES_AT_SPEEDS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'CoaxialConnectionModalAnalysesAtSpeeds.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def connection_design(self) -> '_1852.CoaxialConnection':
        '''CoaxialConnection: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1852.CoaxialConnection)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def connection_load_case(self) -> '_6094.CoaxialConnectionLoadCase':
        '''CoaxialConnectionLoadCase: 'ConnectionLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6094.CoaxialConnectionLoadCase)(self.wrapped.ConnectionLoadCase) if self.wrapped.ConnectionLoadCase else None
