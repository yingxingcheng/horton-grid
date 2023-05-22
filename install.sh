#!/bin/bash
#
if [ -d build ];then
    rm -rf build
fi

./setup.py install --single-version-externally-managed --record=record.txt
