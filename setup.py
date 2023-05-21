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


import configparser
from distutils.command.install_data import install_data
from distutils.command.install_headers import install_headers
from setuptools import setup, Extension
from glob import glob
import json
import os
import platform
import subprocess
import sys

import numpy as np
from Cython.Build import cythonize


# Utility functions
# -----------------


def get_sources(dirname):
    """Get all cpp files and the cext.pyx file of a package"""
    # avoid accidental inclusion of in-place build files and inc files
    result = [
        fn for fn in glob("%s/*.cpp" % dirname) if not (("ext.cpp" in fn) or ("_inc.cpp" in fn))
    ]
    result.append("%s/cext.pyx" % dirname)
    return result


def get_depends(dirname):
    """Get all files that should trigger a recompilation of the C extension of a package"""
    result = glob("%s/*.h" % dirname)
    result += glob("%s/*.pxd" % dirname)
    return result


def get_headers():
    """Get all header-like files that need to be installed"""
    result = []
    for dn in ["horton_grid/"] + glob("horton_grid/*/"):
        result.extend(glob("%s/*.h" % dn))
    return result


class my_install_data(install_data):
    """Add a datadir.txt file that points to the root for the data files. It is
    otherwise impossible to figure out the location of these data files at
    runtime.
    """

    def run(self):
        # Do the normal install_data
        install_data.run(self)
        # Create the file datadir.txt. It's exact content is only known
        # at installation time. By default, it is the installation prefix
        # passed to setup.py, but one can override it using the env var
        # INSTALL_DIR, which may be useful for packaging, or any other
        # situation where the installed files are moved to a new location
        # afterwards.
        my_install_dir = os.getenv("INSTALL_DIR", self.install_dir)
        # Loop over all packages in this project and write the data_dir.txt
        # file only in the main package. Usualy, there is only one that matters.
        dist = self.distribution
        libdir = dist.command_obj["install_lib"].install_dir
        for name in dist.packages:
            # If a package contains a dot, e.g. horton.test, then don't write
            # the file data_dir.txt.
            if "." not in name:
                destination = os.path.join(libdir, name, "data_dir.txt")
                print("install_dir={}".format(my_install_dir))
                print("Creating {}".format(destination))
                if not self.dry_run:
                    with open(destination, "w") as f:
                        print(my_install_dir, file=f)


class my_install_headers(install_headers):
    def run(self):
        headers = self.distribution.headers
        if not headers:
            return

        self.mkpath(self.install_dir)
        for header in headers:
            dest = os.path.join(os.path.dirname(self.install_dir), header)
            dest_dn = os.path.dirname(dest)
            if not os.path.isdir(dest_dn):
                self.mkpath(dest_dn)
            (out, _) = self.copy_file(header, dest)
            self.outfiles.append(out)


# Print the Machine name on screen
# --------------------------------

print("PLATFORM={}".format(platform.platform()))


# Define extension modules
# ------------------------

ext_modules = [
    Extension(
        "horton_grid.cext",
        sources=get_sources("horton_grid"),
        depends=get_depends("horton_grid"),
        include_dirs=[np.get_include(), "."],
        extra_compile_args=["-std=c++11"],
        language="c++",
    ),
    Extension(
        "horton_grid.grid.cext",
        sources=get_sources("horton_grid/grid")
        + ["horton_grid/cell.cpp", "horton_grid/moments.cpp"],
        depends=get_depends("horton_grid/grid")
        + [
            "horton_grid/cell.pxd",
            "horton_grid/cell.h",
            "horton_grid/moments.pxd",
            "horton_grid/moments.h",
        ],
        include_dirs=[np.get_include(), "."],
        extra_compile_args=["-std=c++11"],
        language="c++",
    ),
]

for e in ext_modules:
    e.cython_directives = {"embedsignature": True}

# Call distutils setup
# --------------------

setup(
    name="horton-grid",
    version="2.3.0",
    description="HORTON: Helpful Open-source Research TOol for N-fermion systems.",
    author="Toon Verstraelen",
    author_email="Toon.Verstraelen@UGent.be",
    url="http://yingxingcheng.github.com/horton-grid/",
    scripts=glob("scripts/*.py"),
    package_dir={"horton_grid": "horton_grid"},
    packages=[
        "horton_grid",
        "horton_grid.test",
        "horton_grid.grid",
        "horton_grid.grid.test",
        "horton_grid.io",
        "horton_grid.io.test",
    ],
    cmdclass={
        "install_data": my_install_data,
        "install_headers": my_install_headers,
    },
    data_files=[
        ("share/horton_grid", glob("data/*.*")),
        ("share/horton_grid/test", glob("data/test/*.*")),
        ("share/horton_grid/basis", glob("data/basis/*.*")),
        ("share/horton_grid/grids", glob("data/grids/*.txt")),
    ]
    + [
        (
            "share/horton_grid/examples/%s" % os.path.basename(dn[:-1]),
            glob("%s/*.py" % dn) + glob("%s/README" % dn),
        )
        for dn in glob("data/examples/*/")
    ]
    + [
        ("include/horton_grid", glob("horton_grid/*.h")),
        ("include/horton_grid/grid", glob("horton_grid/grid/*.h")),
    ],
    package_data={
        "horton_grid": ["*.pxd"],
        "horton_grid.grid": ["*.pxd"],
    },
    ext_modules=cythonize(ext_modules),
    headers=get_headers(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Console",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: GNU General Public License (GPL)",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3",
        "Programming Language :: Cython",
        "Programming Language :: C++",
        "Topic :: Science/Engineering :: Molecular Science",
    ],
)
