#!/bin/bash

echo "Creating datacards for " $1
./mkShapesFromHistos.py --pycfg=configuration.py --outputFileName=Shapes_$2_ --signalPoint=$1 #--fastsimMet='reco'
mkdir -p ./tempDatacards/MassPoint$1_$2
./mkDatacards.py        --pycfg=configuration.py --inputFile=./Shapes/Shapes_$2_$1.root --outputDirDatacard=./tempDatacards/MassPoint$1_$2
mkdir -p Datacards$2/MassPoint$1
rm  -r Datacards$2/MassPoint$1
mv ./tempDatacards/MassPoint$1_$2  Datacards$2/MassPoint$1
rm ./Shapes/Shapes_$2_$1.root


