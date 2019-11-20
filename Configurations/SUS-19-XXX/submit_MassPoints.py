import os,sys
from datetime import datetime
import numpy as np
if len(sys.argv)<4:      
    print 'Please, specify year, tag and sigset values, in that order'
    sys.exit() 
def makeSubFile(filename,year,tag,sigset):
    f= open(filename,"w+")
    arguments=year+' '+tag+' '+sigset
    print "creating "+filename+" \t ARGUMENTS:\n ",arguments, "\n"
    f.write("executable            = run_AnalysisMP.py \n")
    f.write("arguments             = "+arguments+"\n")
    f.write("output                = Condor/test/hello.$(ClusterId).$(ProcId).out\n")
    f.write("error                 = Condor/test/hello.$(ClusterId).$(ProcId).err\n")
    f.write("log                   = Condor/test/hello.$(ClusterId).log\n")
    f.write("+JobFlavour           = tomorrow\n")
    f.write("queue\n")
    f.close() 

def writetolog(filename,line,doheader):
    if(os.path.exists(filename) is False):
        print "creating file:"
        f= open(filename,"w+")
    else:
        f= open(filename,"a+")
    # Textual month, day and year
    if(doheader is True):
        now = datetime.now()
        d2 = now.strftime("%d %B, %Y, at %H:%M:%S")
        f.write(d2+"\nSUBMITTING FILES\n\n")
    f.write(line+'\n')
    f.close()
    print "line", line
#Take args
year  = sys.argv[1]
tag   = sys.argv[2]
sigset= sys.argv[3]

exec(open("signalMassPoints.py").read())



mpInSigset=[]
for model in signalMassPoints:
    print "Model:", model,"\tSignal set", sigset
    if model not in sigset:  continue
    for massPoint in signalMassPoints[model]:
        if(massPointInSignalSet(massPoint,sigset)): mpInSigset.append(massPoint)
            #            print "this", sigset, massPoint
'''
        if massPoint not in sigset: continue
        print "Mass Point:", massPoint
'''
#sortMP=sorted(includedMP)
nchunk=4
chunks = [sorted(mpInSigset)[x:x+nchunk] for x in xrange(0, len(mpInSigset), nchunk)]
doheader=True
logfile="Condor/"+sigset+".log"
subfilename="submitMPtemp.sub"
for i in chunks:
    argsigset= ",".join(i)
    line="\nMPs: "+argsigset
    writetolog(logfile, line,doheader)
    doheader=False
    makeSubFile(subfilename, year, tag, argsigset)
    submit="condor_submit "+subfilename+" >>"+logfile
    print submit
    os.system(submit)

writetolog(logfile,"----------------------------------" ,doheader)

print "\nCODE SHOULD BE SENT, MORE INFO IN LOG FILE:\n--> ", logfile
    #os.system("cat "+filename)
    #continue
#print smp.massPointInSignalSet('t2tt','5')
