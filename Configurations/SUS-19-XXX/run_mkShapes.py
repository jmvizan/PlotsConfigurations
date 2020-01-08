import sys
import os
args=sys.argv

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
if len(args)==2 or args[2]=='0' or args[2]=='shapes':
    batch     = True
    queue     = 'tomorrow'
    dohadd    = False
    keepinput = False
else:
    batch     = True
    queue     = ''
    dohadd    = True
    keepinput = True
if len(args)<4:
    sigset='SM'
    if tag=='btagefficiencies': sigset='Backgrounds'
    split='Samples'
else:
    sigset=args[3]
    if len(args)<5: split='Samples'
    else:           split=args[4]
shapefolder="Shapes/"+ yearset+'/'+split
#os.system("mkdir -p "+shapefolder  )
batch=False
batchstr=' '
if batch is True:
    batchstr+='--doBatch=True --batchQueue='+queue
batchstr+= "--batchSplit="+split+" --doHadd="+str(dohadd)

if( dohadd is False):
    os.system("mkShapes.py --pycfg=configuration.py --tag="+yearset+tag+" --sigset="+sigset+ " --treeName=Events --ooutputDir=."+shapefolder+' '+batchstr)
else:
    os.system("mkShapes.py --pycfg=configuration.py --tag="+yearset+tag+" --sigset="+sigset+ " --treeName=Events --outputDir="+shapefolder+" --doNotCleanup")
    os.system("mv "+shapefolder+'/plots_'+yearset+tag+'.root ./Shapes/'+yearset+'/plots_'+tag+sigset+".root")
