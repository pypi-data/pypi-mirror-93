﻿'''_3629.py

BeltDriveCompoundParametricStudyTool
'''


from typing import List

from mastapy.system_model.part_model.couplings import _2132
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.parametric_study_tools import _3492
from mastapy.system_model.analyses_and_results.parametric_study_tools.compound import _3711
from mastapy._internal.python_net import python_net_import

_BELT_DRIVE_COMPOUND_PARAMETRIC_STUDY_TOOL = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ParametricStudyTools.Compound', 'BeltDriveCompoundParametricStudyTool')


__docformat__ = 'restructuredtext en'
__all__ = ('BeltDriveCompoundParametricStudyTool',)


class BeltDriveCompoundParametricStudyTool(_3711.SpecialisedAssemblyCompoundParametricStudyTool):
    '''BeltDriveCompoundParametricStudyTool

    This is a mastapy class.
    '''

    TYPE = _BELT_DRIVE_COMPOUND_PARAMETRIC_STUDY_TOOL

    __hash__ = None

    def __init__(self, instance_to_wrap: 'BeltDriveCompoundParametricStudyTool.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2132.BeltDrive':
        '''BeltDrive: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2132.BeltDrive)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def assembly_design(self) -> '_2132.BeltDrive':
        '''BeltDrive: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2132.BeltDrive)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_3492.BeltDriveParametricStudyTool]':
        '''List[BeltDriveParametricStudyTool]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_3492.BeltDriveParametricStudyTool))
        return value

    @property
    def assembly_parametric_study_tool_load_cases(self) -> 'List[_3492.BeltDriveParametricStudyTool]':
        '''List[BeltDriveParametricStudyTool]: 'AssemblyParametricStudyToolLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyParametricStudyToolLoadCases, constructor.new(_3492.BeltDriveParametricStudyTool))
        return value
