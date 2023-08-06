﻿'''_6191.py

CylindricalGearMeshCriticalSpeedAnalysis
'''


from typing import List

from mastapy.system_model.connections_and_sockets.gears import _1961
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _6458
from mastapy.system_model.analyses_and_results.critical_speed_analyses import _6202
from mastapy._internal.python_net import python_net_import

_CYLINDRICAL_GEAR_MESH_CRITICAL_SPEED_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.CriticalSpeedAnalyses', 'CylindricalGearMeshCriticalSpeedAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('CylindricalGearMeshCriticalSpeedAnalysis',)


class CylindricalGearMeshCriticalSpeedAnalysis(_6202.GearMeshCriticalSpeedAnalysis):
    '''CylindricalGearMeshCriticalSpeedAnalysis

    This is a mastapy class.
    '''

    TYPE = _CYLINDRICAL_GEAR_MESH_CRITICAL_SPEED_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'CylindricalGearMeshCriticalSpeedAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def connection_design(self) -> '_1961.CylindricalGearMesh':
        '''CylindricalGearMesh: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1961.CylindricalGearMesh)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def connection_load_case(self) -> '_6458.CylindricalGearMeshLoadCase':
        '''CylindricalGearMeshLoadCase: 'ConnectionLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6458.CylindricalGearMeshLoadCase)(self.wrapped.ConnectionLoadCase) if self.wrapped.ConnectionLoadCase else None

    @property
    def planetaries(self) -> 'List[CylindricalGearMeshCriticalSpeedAnalysis]':
        '''List[CylindricalGearMeshCriticalSpeedAnalysis]: 'Planetaries' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Planetaries, constructor.new(CylindricalGearMeshCriticalSpeedAnalysis))
        return value
