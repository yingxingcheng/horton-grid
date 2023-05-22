#!/usr/bin/env python
# -*- coding: utf-8 -*-
# HORTON-GRID: GRID for Helpful Open-source Research TOol for N-fermion systems.
# Copyright (C) 2011-2023 The HORTON-GRID Development Team
#
# This file is part of HORTON-GRID
#
# HORTON-GRID is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 3
# of the License, or (at your option) any later version.
#
# HORTON-GRID is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, see <http://www.gnu.org/licenses/>
#
# --


import numpy as np

from setuptools import setup, Extension, find_packages
from setuptools.command.build_ext import build_ext


# Read requirements.txt, ignore comments
with open("requirements.txt") as f:
    requirements = []
    for line in f:
        if line[0] != "#":
            requirements.append(line.strip())

ext_modules = [
    Extension(
        "horton_grid.cext",
        sources=[
            "horton_grid/cext.pyx",
            # "horton_grid/cext.cpp",
            "horton_grid/cell.cpp",
            "horton_grid/moments.cpp",
            "horton_grid/nucpot.cpp",
        ],
        depends=[
            # headers
            "horton_grid/cext.h",
            "horton_grid/cell.h",
            "horton_grid/nucpot.h",
            "horton_grid/moments.h",
            # pxd
            "horton_grid/nucpot.pxd",
            "horton_grid/moments.pxd",
            "horton_grid/cell.pxd",
            "horton_grid/cext.pxd",
        ],
        include_dirs=[
            np.get_include(),
            "horton_grid",
        ],
        language="c++",
        extra_compile_args=["-std=c++11"],  # example compiler arguments
    ),
    Extension(
        "horton_grid.grid.cext",
        sources=[
            "horton_grid/grid/cext.pyx",
            "horton_grid/grid/becke.cpp",
            "horton_grid/grid/cubic_spline.cpp",
            "horton_grid/grid/evaluate.cpp",
            "horton_grid/grid/lebedev_laikov.cpp",
            "horton_grid/grid/ode2.cpp",
            "horton_grid/grid/rtransform.cpp",
            "horton_grid/grid/uniform.cpp",
            "horton_grid/grid/utils.cpp",
        ],
        depends=[
            "horton_grid/grid/cext.h",
            "horton_grid/grid/cext.pxd",
            "horton_grid/grid/becke.h",
            "horton_grid/grid/becke.pxd",
            "horton_grid/grid/cubic_spline.h",
            "horton_grid/grid/cubic_spline.pxd",
            "horton_grid/grid/evaluate.h",
            "horton_grid/grid/evaluate.pxd",
            "horton_grid/grid/lebedev_laikov.h",
            "horton_grid/grid/lebedev_laikov.pxd",
            "horton_grid/grid/ode2.h",
            "horton_grid/grid/ode2.pxd",
            "horton_grid/grid/rtransform.h",
            "horton_grid/grid/rtransform.pxd",
            "horton_grid/grid/uniform.h",
            "horton_grid/grid/uniform.pxd",
            "horton_grid/grid/utils.h",
            "horton_grid/grid/utils.pxd",
        ]
        + [
            "horton_grid/cell.pxd",
            "horton_grid/cell.h",
            "horton_grid/moments.pxd",
            "horton_grid/moments.h",
        ],
        include_dirs=[
            np.get_include(),
            "horton_grid",
            "horton_grid/grid",
        ],
        language="c++",
        extra_compile_args=["-std=c++11"],
    ),
]

for e in ext_modules:
    e.cython_directives = {"embedsignature": True}

if __name__ == "__main__":
    setup(
        name="horton_grid",
        version="2.3.0",
        author="Your Name",
        author_email="your.email@domain.com",
        url="https://github.com/yourusername/horton_grid",
        description="A detailed description of your project",
        long_description="README",
        long_description_content_type="text/markdown",
        license="Your License",
        classifiers=[
            "Development Status :: 3 - Alpha",
            "Intended Audience :: Science/Research",
            "License :: OSI Approved :: MIT License",
            "Programming Language :: Python :: 3",
            "Programming Language :: Python :: 3.10",
        ],
        packages=find_packages(),
        package_data={
            "horton_grid": ["data/*.*", "data/grids/*.*", "data/test/*.*", "data/examples/*.py"],
        },
        include_package_data=True,
        python_requires=">=3.10",
        install_requires=requirements,
        ext_modules=ext_modules,
        cmdclass={"build_ext": build_ext},
    )
