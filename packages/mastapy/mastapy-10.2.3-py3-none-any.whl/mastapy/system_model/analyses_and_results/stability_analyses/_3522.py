﻿'''_3522.py

WormGearStabilityAnalysis
'''


from mastapy.system_model.part_model.gears import _2195
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6578
from mastapy.system_model.analyses_and_results.stability_analyses import _3455
from mastapy._internal.python_net import python_net_import

_WORM_GEAR_STABILITY_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StabilityAnalyses', 'WormGearStabilityAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('WormGearStabilityAnalysis',)


class WormGearStabilityAnalysis(_3455.GearStabilityAnalysis):
    '''WormGearStabilityAnalysis

    This is a mastapy class.
    '''

    TYPE = _WORM_GEAR_STABILITY_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'WormGearStabilityAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2195.WormGear':
        '''WormGear: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2195.WormGear)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_load_case(self) -> '_6578.WormGearLoadCase':
        '''WormGearLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6578.WormGearLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase else None
