﻿'''_2139.py

Coupling
'''


from typing import List

from mastapy._internal import constructor, conversion
from mastapy.system_model.part_model.couplings import (
    _2140, _2135, _2138, _2142,
    _2144, _2145, _2151, _2155,
    _2158, _2159, _2160, _2162,
    _2164
)
from mastapy._internal.cast_exception import CastException
from mastapy.system_model.part_model import _2038
from mastapy._internal.python_net import python_net_import

_COUPLING = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Couplings', 'Coupling')


__docformat__ = 'restructuredtext en'
__all__ = ('Coupling',)


class Coupling(_2038.SpecialisedAssembly):
    '''Coupling

    This is a mastapy class.
    '''

    TYPE = _COUPLING

    __hash__ = None

    def __init__(self, instance_to_wrap: 'Coupling.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def torsional_stiffness(self) -> 'float':
        '''float: 'TorsionalStiffness' is the original name of this property.'''

        return self.wrapped.TorsionalStiffness

    @torsional_stiffness.setter
    def torsional_stiffness(self, value: 'float'):
        self.wrapped.TorsionalStiffness = float(value) if value else 0.0

    @property
    def radial_stiffness(self) -> 'float':
        '''float: 'RadialStiffness' is the original name of this property.'''

        return self.wrapped.RadialStiffness

    @radial_stiffness.setter
    def radial_stiffness(self, value: 'float'):
        self.wrapped.RadialStiffness = float(value) if value else 0.0

    @property
    def axial_stiffness(self) -> 'float':
        '''float: 'AxialStiffness' is the original name of this property.'''

        return self.wrapped.AxialStiffness

    @axial_stiffness.setter
    def axial_stiffness(self, value: 'float'):
        self.wrapped.AxialStiffness = float(value) if value else 0.0

    @property
    def tilt_stiffness(self) -> 'float':
        '''float: 'TiltStiffness' is the original name of this property.'''

        return self.wrapped.TiltStiffness

    @tilt_stiffness.setter
    def tilt_stiffness(self, value: 'float'):
        self.wrapped.TiltStiffness = float(value) if value else 0.0

    @property
    def halves(self) -> 'List[_2140.CouplingHalf]':
        '''List[CouplingHalf]: 'Halves' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Halves, constructor.new(_2140.CouplingHalf))
        return value

    @property
    def half_a(self) -> '_2140.CouplingHalf':
        '''CouplingHalf: 'HalfA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2140.CouplingHalf)(self.wrapped.HalfA) if self.wrapped.HalfA else None

    @property
    def half_a_of_type_clutch_half(self) -> '_2135.ClutchHalf':
        '''ClutchHalf: 'HalfA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2135.ClutchHalf.TYPE not in self.wrapped.HalfA.__class__.__mro__:
            raise CastException('Failed to cast half_a to ClutchHalf. Expected: {}.'.format(self.wrapped.HalfA.__class__.__qualname__))

        return constructor.new(_2135.ClutchHalf)(self.wrapped.HalfA) if self.wrapped.HalfA else None

    @property
    def half_a_of_type_concept_coupling_half(self) -> '_2138.ConceptCouplingHalf':
        '''ConceptCouplingHalf: 'HalfA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2138.ConceptCouplingHalf.TYPE not in self.wrapped.HalfA.__class__.__mro__:
            raise CastException('Failed to cast half_a to ConceptCouplingHalf. Expected: {}.'.format(self.wrapped.HalfA.__class__.__qualname__))

        return constructor.new(_2138.ConceptCouplingHalf)(self.wrapped.HalfA) if self.wrapped.HalfA else None

    @property
    def half_a_of_type_cvt_pulley(self) -> '_2142.CVTPulley':
        '''CVTPulley: 'HalfA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2142.CVTPulley.TYPE not in self.wrapped.HalfA.__class__.__mro__:
            raise CastException('Failed to cast half_a to CVTPulley. Expected: {}.'.format(self.wrapped.HalfA.__class__.__qualname__))

        return constructor.new(_2142.CVTPulley)(self.wrapped.HalfA) if self.wrapped.HalfA else None

    @property
    def half_a_of_type_part_to_part_shear_coupling_half(self) -> '_2144.PartToPartShearCouplingHalf':
        '''PartToPartShearCouplingHalf: 'HalfA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2144.PartToPartShearCouplingHalf.TYPE not in self.wrapped.HalfA.__class__.__mro__:
            raise CastException('Failed to cast half_a to PartToPartShearCouplingHalf. Expected: {}.'.format(self.wrapped.HalfA.__class__.__qualname__))

        return constructor.new(_2144.PartToPartShearCouplingHalf)(self.wrapped.HalfA) if self.wrapped.HalfA else None

    @property
    def half_a_of_type_pulley(self) -> '_2145.Pulley':
        '''Pulley: 'HalfA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2145.Pulley.TYPE not in self.wrapped.HalfA.__class__.__mro__:
            raise CastException('Failed to cast half_a to Pulley. Expected: {}.'.format(self.wrapped.HalfA.__class__.__qualname__))

        return constructor.new(_2145.Pulley)(self.wrapped.HalfA) if self.wrapped.HalfA else None

    @property
    def half_a_of_type_rolling_ring(self) -> '_2151.RollingRing':
        '''RollingRing: 'HalfA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2151.RollingRing.TYPE not in self.wrapped.HalfA.__class__.__mro__:
            raise CastException('Failed to cast half_a to RollingRing. Expected: {}.'.format(self.wrapped.HalfA.__class__.__qualname__))

        return constructor.new(_2151.RollingRing)(self.wrapped.HalfA) if self.wrapped.HalfA else None

    @property
    def half_a_of_type_spring_damper_half(self) -> '_2155.SpringDamperHalf':
        '''SpringDamperHalf: 'HalfA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2155.SpringDamperHalf.TYPE not in self.wrapped.HalfA.__class__.__mro__:
            raise CastException('Failed to cast half_a to SpringDamperHalf. Expected: {}.'.format(self.wrapped.HalfA.__class__.__qualname__))

        return constructor.new(_2155.SpringDamperHalf)(self.wrapped.HalfA) if self.wrapped.HalfA else None

    @property
    def half_a_of_type_synchroniser_half(self) -> '_2158.SynchroniserHalf':
        '''SynchroniserHalf: 'HalfA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2158.SynchroniserHalf.TYPE not in self.wrapped.HalfA.__class__.__mro__:
            raise CastException('Failed to cast half_a to SynchroniserHalf. Expected: {}.'.format(self.wrapped.HalfA.__class__.__qualname__))

        return constructor.new(_2158.SynchroniserHalf)(self.wrapped.HalfA) if self.wrapped.HalfA else None

    @property
    def half_a_of_type_synchroniser_part(self) -> '_2159.SynchroniserPart':
        '''SynchroniserPart: 'HalfA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2159.SynchroniserPart.TYPE not in self.wrapped.HalfA.__class__.__mro__:
            raise CastException('Failed to cast half_a to SynchroniserPart. Expected: {}.'.format(self.wrapped.HalfA.__class__.__qualname__))

        return constructor.new(_2159.SynchroniserPart)(self.wrapped.HalfA) if self.wrapped.HalfA else None

    @property
    def half_a_of_type_synchroniser_sleeve(self) -> '_2160.SynchroniserSleeve':
        '''SynchroniserSleeve: 'HalfA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2160.SynchroniserSleeve.TYPE not in self.wrapped.HalfA.__class__.__mro__:
            raise CastException('Failed to cast half_a to SynchroniserSleeve. Expected: {}.'.format(self.wrapped.HalfA.__class__.__qualname__))

        return constructor.new(_2160.SynchroniserSleeve)(self.wrapped.HalfA) if self.wrapped.HalfA else None

    @property
    def half_a_of_type_torque_converter_pump(self) -> '_2162.TorqueConverterPump':
        '''TorqueConverterPump: 'HalfA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2162.TorqueConverterPump.TYPE not in self.wrapped.HalfA.__class__.__mro__:
            raise CastException('Failed to cast half_a to TorqueConverterPump. Expected: {}.'.format(self.wrapped.HalfA.__class__.__qualname__))

        return constructor.new(_2162.TorqueConverterPump)(self.wrapped.HalfA) if self.wrapped.HalfA else None

    @property
    def half_a_of_type_torque_converter_turbine(self) -> '_2164.TorqueConverterTurbine':
        '''TorqueConverterTurbine: 'HalfA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2164.TorqueConverterTurbine.TYPE not in self.wrapped.HalfA.__class__.__mro__:
            raise CastException('Failed to cast half_a to TorqueConverterTurbine. Expected: {}.'.format(self.wrapped.HalfA.__class__.__qualname__))

        return constructor.new(_2164.TorqueConverterTurbine)(self.wrapped.HalfA) if self.wrapped.HalfA else None

    @property
    def half_b(self) -> '_2140.CouplingHalf':
        '''CouplingHalf: 'HalfB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2140.CouplingHalf)(self.wrapped.HalfB) if self.wrapped.HalfB else None

    @property
    def half_b_of_type_clutch_half(self) -> '_2135.ClutchHalf':
        '''ClutchHalf: 'HalfB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2135.ClutchHalf.TYPE not in self.wrapped.HalfB.__class__.__mro__:
            raise CastException('Failed to cast half_b to ClutchHalf. Expected: {}.'.format(self.wrapped.HalfB.__class__.__qualname__))

        return constructor.new(_2135.ClutchHalf)(self.wrapped.HalfB) if self.wrapped.HalfB else None

    @property
    def half_b_of_type_concept_coupling_half(self) -> '_2138.ConceptCouplingHalf':
        '''ConceptCouplingHalf: 'HalfB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2138.ConceptCouplingHalf.TYPE not in self.wrapped.HalfB.__class__.__mro__:
            raise CastException('Failed to cast half_b to ConceptCouplingHalf. Expected: {}.'.format(self.wrapped.HalfB.__class__.__qualname__))

        return constructor.new(_2138.ConceptCouplingHalf)(self.wrapped.HalfB) if self.wrapped.HalfB else None

    @property
    def half_b_of_type_cvt_pulley(self) -> '_2142.CVTPulley':
        '''CVTPulley: 'HalfB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2142.CVTPulley.TYPE not in self.wrapped.HalfB.__class__.__mro__:
            raise CastException('Failed to cast half_b to CVTPulley. Expected: {}.'.format(self.wrapped.HalfB.__class__.__qualname__))

        return constructor.new(_2142.CVTPulley)(self.wrapped.HalfB) if self.wrapped.HalfB else None

    @property
    def half_b_of_type_part_to_part_shear_coupling_half(self) -> '_2144.PartToPartShearCouplingHalf':
        '''PartToPartShearCouplingHalf: 'HalfB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2144.PartToPartShearCouplingHalf.TYPE not in self.wrapped.HalfB.__class__.__mro__:
            raise CastException('Failed to cast half_b to PartToPartShearCouplingHalf. Expected: {}.'.format(self.wrapped.HalfB.__class__.__qualname__))

        return constructor.new(_2144.PartToPartShearCouplingHalf)(self.wrapped.HalfB) if self.wrapped.HalfB else None

    @property
    def half_b_of_type_pulley(self) -> '_2145.Pulley':
        '''Pulley: 'HalfB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2145.Pulley.TYPE not in self.wrapped.HalfB.__class__.__mro__:
            raise CastException('Failed to cast half_b to Pulley. Expected: {}.'.format(self.wrapped.HalfB.__class__.__qualname__))

        return constructor.new(_2145.Pulley)(self.wrapped.HalfB) if self.wrapped.HalfB else None

    @property
    def half_b_of_type_rolling_ring(self) -> '_2151.RollingRing':
        '''RollingRing: 'HalfB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2151.RollingRing.TYPE not in self.wrapped.HalfB.__class__.__mro__:
            raise CastException('Failed to cast half_b to RollingRing. Expected: {}.'.format(self.wrapped.HalfB.__class__.__qualname__))

        return constructor.new(_2151.RollingRing)(self.wrapped.HalfB) if self.wrapped.HalfB else None

    @property
    def half_b_of_type_spring_damper_half(self) -> '_2155.SpringDamperHalf':
        '''SpringDamperHalf: 'HalfB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2155.SpringDamperHalf.TYPE not in self.wrapped.HalfB.__class__.__mro__:
            raise CastException('Failed to cast half_b to SpringDamperHalf. Expected: {}.'.format(self.wrapped.HalfB.__class__.__qualname__))

        return constructor.new(_2155.SpringDamperHalf)(self.wrapped.HalfB) if self.wrapped.HalfB else None

    @property
    def half_b_of_type_synchroniser_half(self) -> '_2158.SynchroniserHalf':
        '''SynchroniserHalf: 'HalfB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2158.SynchroniserHalf.TYPE not in self.wrapped.HalfB.__class__.__mro__:
            raise CastException('Failed to cast half_b to SynchroniserHalf. Expected: {}.'.format(self.wrapped.HalfB.__class__.__qualname__))

        return constructor.new(_2158.SynchroniserHalf)(self.wrapped.HalfB) if self.wrapped.HalfB else None

    @property
    def half_b_of_type_synchroniser_part(self) -> '_2159.SynchroniserPart':
        '''SynchroniserPart: 'HalfB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2159.SynchroniserPart.TYPE not in self.wrapped.HalfB.__class__.__mro__:
            raise CastException('Failed to cast half_b to SynchroniserPart. Expected: {}.'.format(self.wrapped.HalfB.__class__.__qualname__))

        return constructor.new(_2159.SynchroniserPart)(self.wrapped.HalfB) if self.wrapped.HalfB else None

    @property
    def half_b_of_type_synchroniser_sleeve(self) -> '_2160.SynchroniserSleeve':
        '''SynchroniserSleeve: 'HalfB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2160.SynchroniserSleeve.TYPE not in self.wrapped.HalfB.__class__.__mro__:
            raise CastException('Failed to cast half_b to SynchroniserSleeve. Expected: {}.'.format(self.wrapped.HalfB.__class__.__qualname__))

        return constructor.new(_2160.SynchroniserSleeve)(self.wrapped.HalfB) if self.wrapped.HalfB else None

    @property
    def half_b_of_type_torque_converter_pump(self) -> '_2162.TorqueConverterPump':
        '''TorqueConverterPump: 'HalfB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2162.TorqueConverterPump.TYPE not in self.wrapped.HalfB.__class__.__mro__:
            raise CastException('Failed to cast half_b to TorqueConverterPump. Expected: {}.'.format(self.wrapped.HalfB.__class__.__qualname__))

        return constructor.new(_2162.TorqueConverterPump)(self.wrapped.HalfB) if self.wrapped.HalfB else None

    @property
    def half_b_of_type_torque_converter_turbine(self) -> '_2164.TorqueConverterTurbine':
        '''TorqueConverterTurbine: 'HalfB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2164.TorqueConverterTurbine.TYPE not in self.wrapped.HalfB.__class__.__mro__:
            raise CastException('Failed to cast half_b to TorqueConverterTurbine. Expected: {}.'.format(self.wrapped.HalfB.__class__.__qualname__))

        return constructor.new(_2164.TorqueConverterTurbine)(self.wrapped.HalfB) if self.wrapped.HalfB else None
