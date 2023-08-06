﻿'''_3766.py

ConceptCouplingConnectionModalAnalysesAtStiffnesses
'''


from mastapy.system_model.connections_and_sockets.couplings import _1915
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6096
from mastapy.system_model.analyses_and_results.modal_analyses_at_stiffnesses_ns import _3777
from mastapy._internal.python_net import python_net_import

_CONCEPT_COUPLING_CONNECTION_MODAL_ANALYSES_AT_STIFFNESSES = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtStiffnessesNS', 'ConceptCouplingConnectionModalAnalysesAtStiffnesses')


__docformat__ = 'restructuredtext en'
__all__ = ('ConceptCouplingConnectionModalAnalysesAtStiffnesses',)


class ConceptCouplingConnectionModalAnalysesAtStiffnesses(_3777.CouplingConnectionModalAnalysesAtStiffnesses):
    '''ConceptCouplingConnectionModalAnalysesAtStiffnesses

    This is a mastapy class.
    '''

    TYPE = _CONCEPT_COUPLING_CONNECTION_MODAL_ANALYSES_AT_STIFFNESSES

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ConceptCouplingConnectionModalAnalysesAtStiffnesses.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def connection_design(self) -> '_1915.ConceptCouplingConnection':
        '''ConceptCouplingConnection: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1915.ConceptCouplingConnection)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def connection_load_case(self) -> '_6096.ConceptCouplingConnectionLoadCase':
        '''ConceptCouplingConnectionLoadCase: 'ConnectionLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6096.ConceptCouplingConnectionLoadCase)(self.wrapped.ConnectionLoadCase) if self.wrapped.ConnectionLoadCase else None
