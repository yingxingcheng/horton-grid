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
            "src/horton_grid/cext.pyx",
            # "horton_grid/cext.cpp",
            "src/horton_grid/cell.cpp",
            "src/horton_grid/moments.cpp",
            "src/horton_grid/nucpot.cpp",
        ],
        depends=[
            # headers
            "src/horton_grid/cext.h",
            "src/horton_grid/cell.h",
            "src/horton_grid/nucpot.h",
            "src/horton_grid/moments.h",
            # pxd
            "src/horton_grid/nucpot.pxd",
            "src/horton_grid/moments.pxd",
            "src/horton_grid/cell.pxd",
            "src/horton_grid/cext.pxd",
        ],
        include_dirs=[
            np.get_include(),
            "src/horton_grid",
        ],
        language="c++",
        extra_compile_args=["-std=c++11"],  # example compiler arguments
    ),
    Extension(
        "horton_grid.grid.cext",
        sources=[
            "src/horton_grid/grid/cext.pyx",
            "src/horton_grid/grid/becke.cpp",
            "src/horton_grid/grid/cubic_spline.cpp",
            "src/horton_grid/grid/evaluate.cpp",
            "src/horton_grid/grid/lebedev_laikov.cpp",
            "src/horton_grid/grid/ode2.cpp",
            "src/horton_grid/grid/rtransform.cpp",
            "src/horton_grid/grid/uniform.cpp",
            "src/horton_grid/grid/utils.cpp",
        ],
        depends=[
            "src/horton_grid/grid/cext.h",
            "src/horton_grid/grid/cext.pxd",
            "src/horton_grid/grid/becke.h",
            "src/horton_grid/grid/becke.pxd",
            "src/horton_grid/grid/cubic_spline.h",
            "src/horton_grid/grid/cubic_spline.pxd",
            "src/horton_grid/grid/evaluate.h",
            "src/horton_grid/grid/evaluate.pxd",
            "src/horton_grid/grid/lebedev_laikov.h",
            "src/horton_grid/grid/lebedev_laikov.pxd",
            "src/horton_grid/grid/ode2.h",
            "src/horton_grid/grid/ode2.pxd",
            "src/horton_grid/grid/rtransform.h",
            "src/horton_grid/grid/rtransform.pxd",
            "src/horton_grid/grid/uniform.h",
            "src/horton_grid/grid/uniform.pxd",
            "src/horton_grid/grid/utils.h",
            "src/horton_grid/grid/utils.pxd",
        ]
        + [
            "src/horton_grid/cell.pxd",
            "src/horton_grid/cell.h",
            "src/horton_grid/moments.pxd",
            "src/horton_grid/moments.h",
        ],
        include_dirs=[
            np.get_include(),
            "src/horton_grid",
            "src/horton_grid/grid",
        ],
        language="c++",
        extra_compile_args=["-std=c++11"],
    ),
]

for e in ext_modules:
    e.cython_directives = {"embedsignature": True}

if __name__ == "__main__":
    setup(
        # name="horton_grid",
        # version="2.3.0",
        # author=["YingXing Cheng", "Toon Verstraelen"],
        # author_email=["yingxing.cheng@ugent.be", "toon.verstraelen@ugent.be"],
        # url="https://github.com/yingxingcheng/horton_grid",
        # description="A detailed description of your project",
        # long_description="README",
        # long_description_content_type="text/markdown",
        # license="Your License",
        # classifiers=[
        #     "Development Status :: 3 - Alpha",
        #     "Intended Audience :: Science/Research",
        #     "License :: OSI Approved :: MIT License",
        #     "Programming Language :: Python :: 3",
        #     "Programming Language :: Python :: 3.10",
        # ],
        package_dir={"": "src"},
        packages=find_packages("src"),
        package_data={
            "horton_grid": [
                "data/*.*",
                "data/grids/*.*",
                "data/test/*.*",
                "data/examples/*.py",
            ],
        },
        include_package_data=True,
        # python_requires=">=3.10",
        # install_requires=requirements,
        ext_modules=ext_modules,
        cmdclass={"build_ext": build_ext},
    )
