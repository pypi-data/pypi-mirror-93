'''_6540.py

RollingRingLoadCase
'''


from mastapy.system_model.part_model.couplings import _2240
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6447
from mastapy._internal.python_net import python_net_import

_ROLLING_RING_LOAD_CASE = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads', 'RollingRingLoadCase')


__docformat__ = 'restructuredtext en'
__all__ = ('RollingRingLoadCase',)


class RollingRingLoadCase(_6447.CouplingHalfLoadCase):
    '''RollingRingLoadCase

    This is a mastapy class.
    '''

    TYPE = _ROLLING_RING_LOAD_CASE

    __hash__ = None

    def __init__(self, instance_to_wrap: 'RollingRingLoadCase.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2240.RollingRing':
        '''RollingRing: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2240.RollingRing)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None
