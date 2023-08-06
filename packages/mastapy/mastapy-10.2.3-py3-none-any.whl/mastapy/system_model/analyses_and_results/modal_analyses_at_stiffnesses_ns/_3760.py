﻿'''_3760.py

BoltModalAnalysesAtStiffnesses
'''


from mastapy.system_model.part_model import _2006
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6090
from mastapy.system_model.analyses_and_results.modal_analyses_at_stiffnesses_ns import _3765
from mastapy._internal.python_net import python_net_import

_BOLT_MODAL_ANALYSES_AT_STIFFNESSES = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtStiffnessesNS', 'BoltModalAnalysesAtStiffnesses')


__docformat__ = 'restructuredtext en'
__all__ = ('BoltModalAnalysesAtStiffnesses',)


class BoltModalAnalysesAtStiffnesses(_3765.ComponentModalAnalysesAtStiffnesses):
    '''BoltModalAnalysesAtStiffnesses

    This is a mastapy class.
    '''

    TYPE = _BOLT_MODAL_ANALYSES_AT_STIFFNESSES

    __hash__ = None

    def __init__(self, instance_to_wrap: 'BoltModalAnalysesAtStiffnesses.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2006.Bolt':
        '''Bolt: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2006.Bolt)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_load_case(self) -> '_6090.BoltLoadCase':
        '''BoltLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6090.BoltLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase else None
