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
    print filename.split('/')[1].split('.')[0].split(',')

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
            #print "sigset", sigset

        if massPoint not in sigset: continue
        print "Mass Point:", massPoint




#sortMP=sorted(includedMP)
nchunk=4
chunks = [sorted(mpInSigset)[x:x+nchunk] for x in xrange(0, len(mpInSigset), nchunk)]
doheader=True
logfile="Condor/"+sigset+".log"
subfilename="Condor/submitMPtemp.sub"
lastmp=''
#for mp in sigset.split(','):
#    print compare(mp,lastmp)
#    lastmp=mp
sigsets=sigset.split(',')
inc=''#sigsets[0][0]+'-'
i=0
'''
for l in sigsets[0]:
    inc+=l
    dash=True
    #print l, sigsets[1][i]
    for othermp in sigsets[1:]:
        l2= othermp[i]
        print l,l2.isdigit(), othermp
        if(l is not l2 and l2.isdigit() is False):
            if(dash is True): inc+='-'
            inc+=l2
        dash=False
    i+=

writefp=True
print inc, sigsets[1].split('_'),"\n-------------------\n"#.split('-')
for i in range(0,len(sigsets)):
    if i is 0: 
        if(len(sigsets) is 0): inc=sigsets[0]
        continue
    firstsigset = sigsets[0].split('_')
    thissigset  = sigsets[i].split('_')
    if(len(firstsigset) is not len(thissigset)): continue
    for j in range(0,len(thissigset)):
        
        #for part in sigsets[i].split('_'):
        #if
        firstdashpart = (firstsigset[j]+'_').split('-')
        thisdashpart  = (thissigset[j]+'_').split('-')
        print firstdashpart, len(firstdashpart)
        if(len(firstdashpart) is not len (thisdashpart)): continue
        for k in range(0,len(thisdashpart)):
            firstpart=firstdashpart[k]
            thispart=thisdashpart[k]
            if(k <len(firstdashpart)-1): 
                firstpart+='-'
                thispart +='-'
            print"first-->", firstpart
            if(writefp is True): 
                inc+=firstpart
            if(thispart!= firstpart):
                inc+=thispart
                writefp=False
            elif(thispart ==firstpart): writefp=True
            
            #print "--------> ",inc
        #print firstpart,thispart
    #print sigsets[i].split('_')

print 'INC\n'+inc+'\n'

#if any(entry.startswith('John:') in entry for entry in sigset.split(',')): print "e"
print sigset, sigset[0].replace(sigset[1],"")

'''
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

