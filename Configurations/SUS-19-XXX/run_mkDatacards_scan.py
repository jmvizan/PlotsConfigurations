#!/usr/bin/env python

import sys
import os

if len(sys.argv)<4:
    print 'Please, specify year, tag and sigset values!'
    sys.exit()

if sys.argv[1]==0:
    year='2016'
elif sys.argv[1]==1:
    year='2017'
elif sys.argv[1]==2:
    year='2018'
else:
    year=sys.argv[1]

if sys.argv[2]==0:
    tag='Preselection'
elif sys.argv[2]==1:
    tag='ValidationRegions'
elif sys.argv[2]==2:
    tag='SignalRegions'
else:
    tag=sys.argv[2]

sigset=sys.argv[3]

if len(sys.argv)==5:
    fileset=sys.argv[4]
else:
    fileset='SM-'+sigset

exec(open('./signalMassPoints.py').read())

for model in signalMassPoints:
    if model in sigset:
        for massPoint in signalMassPoints[model]:
            if massPointInSignalSet(massPoint, sigset):

                os.system('./run_mkDatacards.sh '+year+' '+tag+' '+massPoint+' '+fileset)
               


                
