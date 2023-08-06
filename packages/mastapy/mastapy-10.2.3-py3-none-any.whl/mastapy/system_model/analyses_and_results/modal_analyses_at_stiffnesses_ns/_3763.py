﻿'''_3763.py

ClutchModalAnalysesAtStiffnesses
'''


from mastapy.system_model.part_model.couplings import _2134
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6093
from mastapy.system_model.analyses_and_results.modal_analyses_at_stiffnesses_ns import _3779
from mastapy._internal.python_net import python_net_import

_CLUTCH_MODAL_ANALYSES_AT_STIFFNESSES = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtStiffnessesNS', 'ClutchModalAnalysesAtStiffnesses')


__docformat__ = 'restructuredtext en'
__all__ = ('ClutchModalAnalysesAtStiffnesses',)


class ClutchModalAnalysesAtStiffnesses(_3779.CouplingModalAnalysesAtStiffnesses):
    '''ClutchModalAnalysesAtStiffnesses

    This is a mastapy class.
    '''

    TYPE = _CLUTCH_MODAL_ANALYSES_AT_STIFFNESSES

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ClutchModalAnalysesAtStiffnesses.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def assembly_design(self) -> '_2134.Clutch':
        '''Clutch: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2134.Clutch)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def assembly_load_case(self) -> '_6093.ClutchLoadCase':
        '''ClutchLoadCase: 'AssemblyLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6093.ClutchLoadCase)(self.wrapped.AssemblyLoadCase) if self.wrapped.AssemblyLoadCase else None
