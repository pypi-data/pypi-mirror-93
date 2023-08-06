﻿'''_2386.py

BevelDifferentialGearCompoundSystemDeflection
'''


from typing import List

from mastapy.system_model.part_model.gears import _2075
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.system_deflections import _2240
from mastapy.system_model.analyses_and_results.system_deflections.compound import _2391
from mastapy._internal.python_net import python_net_import

_BEVEL_DIFFERENTIAL_GEAR_COMPOUND_SYSTEM_DEFLECTION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SystemDeflections.Compound', 'BevelDifferentialGearCompoundSystemDeflection')


__docformat__ = 'restructuredtext en'
__all__ = ('BevelDifferentialGearCompoundSystemDeflection',)


class BevelDifferentialGearCompoundSystemDeflection(_2391.BevelGearCompoundSystemDeflection):
    '''BevelDifferentialGearCompoundSystemDeflection

    This is a mastapy class.
    '''

    TYPE = _BEVEL_DIFFERENTIAL_GEAR_COMPOUND_SYSTEM_DEFLECTION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'BevelDifferentialGearCompoundSystemDeflection.TYPE'):
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
    def load_case_analyses_ready(self) -> 'List[_2240.BevelDifferentialGearSystemDeflection]':
        '''List[BevelDifferentialGearSystemDeflection]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_2240.BevelDifferentialGearSystemDeflection))
        return value

    @property
    def component_system_deflection_load_cases(self) -> 'List[_2240.BevelDifferentialGearSystemDeflection]':
        '''List[BevelDifferentialGearSystemDeflection]: 'ComponentSystemDeflectionLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentSystemDeflectionLoadCases, constructor.new(_2240.BevelDifferentialGearSystemDeflection))
        return value
