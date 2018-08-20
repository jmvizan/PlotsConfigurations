#!/bin/bash

if [ $# -lt 1 ] ; then
    exit -1
fi

FOLDER="$1"

pushd $FOLDER

hadd -f -k 98_Others.root 15_VZ3V.root 09_TTW.root 11_HWW.root

popd
