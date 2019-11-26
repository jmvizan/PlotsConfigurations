import os,sys
from datetime import datetime
import numpy as np

#Function to create sub file
def makeSubFile(filename,year,tag,sigset):
    f = open(filename,"w+")
    arguments = year+' '+tag+' '+sigset
    print "creating "+filename+" \t ARGUMENTS:\n ",arguments, "\n"
    f.write("executable            = run_AnalysisMP.py \n")
    f.write("arguments             = "+arguments+"\n")
    f.write("output                = Condor/test/hello.$(ClusterId).$(ProcId).out\n")
    f.write("error                 = Condor/test/hello.$(ClusterId).$(ProcId).err\n")
    f.write("log                   = Condor/test/hello.$(ClusterId).log\n")
    f.write("+JobFlavour           = tomorrow\n")
    f.write("queue\n")
    f.close() 

#Create log file
def writetolog(filename,line,doheader):
    print filename.split('/')[1].split('.')[0].split(',')

    if(os.path.exists(filename) is False):
        print "creating file:"
        f = open(filename,"w+")
    else:
        f = open(filename,"a+")
    # Textual month, day and year
    if(doheader is True):
        now = datetime.now()
        d2  = now.strftime("%d %B, %Y, at %H:%M:%S")
        f.write(d2+"\nSUBMITTING FILES\n\n")
    f.write(line+'\n')
    f.close()
    print "line", line

#Remove specifical events
def rreplace(s, old, new, occurrence):
    li = s.rsplit(old, occurrence)
    return new.join(li)

if len(sys.argv)<4:      
    print 'Please, specify year, tag and sigset values, in that order'
    sys.exit() 

#Take args
year   = sys.argv[1]
tag    = sys.argv[2]
sigset = sys.argv[3]

exec(open("signalMassPoints.py").read())


#Look for masspoints in the sigset
mpInSigset=[]
for model in signalMassPoints:
    print "Model:", model,"\tSignal set", sigset
    if model not in sigset:  continue
    for massPoint in signalMassPoints[model]:
        if(massPointInSignalSet(massPoint,sigset)): mpInSigset.append(massPoint)
        if massPoint not in sigset: continue
        print "Mass Point:", massPoint

#Make a more human-readable logfile if necessary
sigsets     = sigset.split(',')
firstsigset = sigsets[0].split('_')
writesigset = firstsigset    
for i in range(0,len(sigsets)):
    if i is 0: continue
    diffmp = ''
    thissigset  = sigsets[i].split('_')    
    if(len(firstsigset) is not len(thissigset)): continue
    for j in range(0,len(thissigset)):
#        print firstsigset[j], thissigset[j]
        if(firstsigset[j]!=thissigset[j]):
            if(j<len(thissigset)-1): diffmp='-'
            firstpart = (firstsigset[j]+'_').split('-')
            thispart  = (thissigset[j]+'_').split('-')
            writesigset[j]+=diffmp+'-'+thissigset[j]

#remove duplicate mS and similars            
nmS = writesigset[1].count('mS')
nmX = writesigset[2].count('mX')
if(nmS>1):   writesigset[1] = rreplace(writesigset[1] , 'mS', '', nmS - 1)
elif(nmX>1): writesigset[2] = rreplace(writesigset[2] , 'mX', '', nmX - 1)
    
print writesigset
lognm   = '_'.join(writesigset)
logfile = "Condor/"+lognm+".log"



#divide masspoints in sets of four and send jobs
nchunk      = 4
chunks      = [sorted(mpInSigset)[x:x+nchunk] for x in xrange(0, len(mpInSigset), nchunk)]
doheader    = True
subfilename ="Condor/submitMPtemp.sub"
for i in chunks:
    doheader  = False
    argsigset = ",".join(i)
    line      = "\nMPs: "+argsigset
    writetolog(logfile, line,doheader)
    makeSubFile(subfilename, year, tag, argsigset)
    submit="condor_submit "+subfilename+" >>"+logfile
    print submit
    os.system(submit)

writetolog(logfile,"----------------------------------" ,doheader)

print "\nCODE SHOULD BE SENT, MORE INFO IN LOG FILE:\n--> ", logfile
    
