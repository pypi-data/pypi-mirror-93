﻿'''_6155.py

BevelDifferentialPlanetGearCriticalSpeedAnalysis
'''


from mastapy.system_model.part_model.gears import _2161
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.critical_speed_analyses import _6152
from mastapy._internal.python_net import python_net_import

_BEVEL_DIFFERENTIAL_PLANET_GEAR_CRITICAL_SPEED_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.CriticalSpeedAnalyses', 'BevelDifferentialPlanetGearCriticalSpeedAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('BevelDifferentialPlanetGearCriticalSpeedAnalysis',)


class BevelDifferentialPlanetGearCriticalSpeedAnalysis(_6152.BevelDifferentialGearCriticalSpeedAnalysis):
    '''BevelDifferentialPlanetGearCriticalSpeedAnalysis

    This is a mastapy class.
    '''

    TYPE = _BEVEL_DIFFERENTIAL_PLANET_GEAR_CRITICAL_SPEED_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'BevelDifferentialPlanetGearCriticalSpeedAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2161.BevelDifferentialPlanetGear':
        '''BevelDifferentialPlanetGear: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2161.BevelDifferentialPlanetGear)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None
