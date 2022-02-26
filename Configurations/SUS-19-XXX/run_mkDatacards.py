#!/usr/bin/env python

import sys
import os

if len(sys.argv)<4:
    print 'Please, specify year, tag and sigset values!'
    sys.exit()

if sys.argv[1]=='-1':
    yearset='2016-2017-2018'
elif sys.argv[1]=='0':
    yearset='2016'
elif sys.argv[1]=='1':
    yearset='2017'
elif sys.argv[1]=='2':
    yearset='2018'
else:
    yearset=sys.argv[1]

if   sys.argv[2]== '0':
    tag='Preselection'                                                                         
elif sys.argv[2]== '1':
    tag='ValidationRegions'                                                                    
elif sys.argv[2]=='2':
    tag='StopSignalRegions'                                                                    
else: 
    tag=sys.argv[2]

sigset=sys.argv[3]

if len(sys.argv)==5:
    fileset=sys.argv[4]
else:
    fileset=sigset
if 'SM-' not in fileset:
    fileset = 'SM-' + fileset

exec(open('./signalMassPoints.py').read())

years = yearset.split('-')

inputtag = tag.split('_')[0]

for year in years:
    os.system('mkdir -p ./Datacards/'+year+'/'+tag)
    #print "this is signset", sigset,signalMassPoints
    if "wjets" in sigset.lower(): 
        massPoint = 'EOYWJets'
        os.system('mkDatacards.py --pycfg=configuration.py --tag='+year+tag+' --sigset=SM-'+massPoint+' --outputDirDatacard=./Datacards/'+year+'/'+tag+'/\
        '+massPoint+' --inputFile=./Shapes/'+year+'/'+inputtag+'/plots_'+inputtag+'_'+fileset+'.root')
    else:
        for model in signalMassPoints:
            print "model", model, sigset
            if model in sigset:
                for massPoint in signalMassPoints[model]:
                    if massPointInSignalSet(massPoint, sigset):
                        os.system('mkDatacards.py --pycfg=configuration.py --tag='+year+tag+' --sigset=SM-'+massPoint+' --outputDirDatacard=./Datacards/'+year+'/'+tag+'/'+massPoint+' --inputFile=./Shapes/'+year+'/'+inputtag+'/plots_'+inputtag+'_'+fileset+'.root') 
