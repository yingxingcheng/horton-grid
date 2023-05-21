# -*- coding: utf-8 -*-
# HORTON: Helpful Open-source Research TOol for N-fermion systems.
# Copyright (C) 2011-2022 The HORTON Development Team
#
# This file is part of HORTON.
#
# HORTON is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 3
# of the License, or (at your option) any later version.
#
# HORTON is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, see <http://www.gnu.org/licenses/>
#
# --
#cython: language_level=3

cimport numpy as np

cimport horton_grid.grid.cubic_spline as cubic_spline
cimport horton_grid.grid.rtransform as rtransform
cimport horton_grid.grid.uniform as uniform


cdef class Extrapolation(object):
    cdef cubic_spline.Extrapolation* _this


cdef class ZeroExtrapolation(Extrapolation):
    pass


cdef class CuspExtrapolation(Extrapolation):
    pass


cdef class PowerExtrapolation(Extrapolation):
    pass


cdef class PotentialExtrapolation(Extrapolation):
    pass


cdef class CubicSpline(object):
    cdef cubic_spline.CubicSpline* _this
    cdef Extrapolation _extrapolation
    cdef RTransform _rtransform
    cdef np.ndarray _y
    cdef np.ndarray _dx
    cdef np.ndarray _dt


cdef class RTransform(object):
    cdef rtransform.RTransform* _this


cdef class IdentityRTransform(RTransform):
    pass


cdef class LinearRTransform(RTransform):
    pass


cdef class ExpRTransform(RTransform):
    pass


cdef class PowerRTransform(RTransform):
    pass


cdef class HyperbolicRTransform(RTransform):
    pass


cdef class UniformGrid:
    cdef uniform.UniformGrid* _this
