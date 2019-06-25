#!/usr/bin/env python

import sys
import os

if len(sys.argv)<3:
    print 'Please, specify tag and sigset values!'
    sys.exit()

if sys.argv[1]==0:
    tag='Preselection'
elif sys.argv[1]==1:
    tag='ValidationRegions'
elif sys.argv[1]==2:
    tag='SignalRegions'
else:
    tag=sys.argv[1]

sigset=sys.argv[2]

if len(sys.argv)==4:
    fileset=sys.argv[3]
else:
    fileset='SM-'+sigset

exec(open('./signalMassPoints.py').read())

for model in signalMassPoints:
    if model in sigset:
        for massPoint in signalMassPoints[model]:
            if sigset in massPoint:

                os.system('./run_mkDatacards.sh '+tag+' '+massPoint+' '+fileset)
               


                
