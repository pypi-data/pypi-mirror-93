﻿'''_6889.py

ClutchConnectionAdvancedSystemDeflection
'''


from typing import List

from mastapy.system_model.connections_and_sockets.couplings import _1992
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _6428
from mastapy.system_model.analyses_and_results.system_deflections import _2344
from mastapy.system_model.analyses_and_results.advanced_system_deflections import _6906
from mastapy._internal.python_net import python_net_import

_CLUTCH_CONNECTION_ADVANCED_SYSTEM_DEFLECTION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.AdvancedSystemDeflections', 'ClutchConnectionAdvancedSystemDeflection')


__docformat__ = 'restructuredtext en'
__all__ = ('ClutchConnectionAdvancedSystemDeflection',)


class ClutchConnectionAdvancedSystemDeflection(_6906.CouplingConnectionAdvancedSystemDeflection):
    '''ClutchConnectionAdvancedSystemDeflection

    This is a mastapy class.
    '''

    TYPE = _CLUTCH_CONNECTION_ADVANCED_SYSTEM_DEFLECTION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ClutchConnectionAdvancedSystemDeflection.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def connection_design(self) -> '_1992.ClutchConnection':
        '''ClutchConnection: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1992.ClutchConnection)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def connection_load_case(self) -> '_6428.ClutchConnectionLoadCase':
        '''ClutchConnectionLoadCase: 'ConnectionLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6428.ClutchConnectionLoadCase)(self.wrapped.ConnectionLoadCase) if self.wrapped.ConnectionLoadCase else None

    @property
    def connection_system_deflection_results(self) -> 'List[_2344.ClutchConnectionSystemDeflection]':
        '''List[ClutchConnectionSystemDeflection]: 'ConnectionSystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConnectionSystemDeflectionResults, constructor.new(_2344.ClutchConnectionSystemDeflection))
        return value
