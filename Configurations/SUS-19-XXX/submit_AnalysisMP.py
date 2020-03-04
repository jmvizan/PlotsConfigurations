#!/usr/bin/env python
import os,sys
from datetime import datetime
import numpy as np

#write header to logfile
def logtitle(filename,sigset):
    if(os.path.exists(filename) is False):  print "creating log file"
    f = open(filename,"a")
    # Textual month, day and year
    now = datetime.now()
    d2  = now.strftime("%d %B, %Y, at %H:%M:%S")
    f.write(d2+"\nCALCULATING LIMITS FOR:\t "+ sigset+"\n")
    f.close()


#Create log file
def writetolog(filename,line):
    f = open(filename,"a")
    f.write(line+'\n')
    f.close()
    #print "line", line

     
def makeSubFile2(filename,folder,year,tag,sigset,fileset, doDC,writesigset):
    PWD = os.getenv('PWD')+'/'
    f = open(filename,"w+")
    jobsent= '$(' +sigset + ')'
    arguments = year+' '+tag+' '+jobsent+ ' ' +PWD+' '+fileset+' '+str(doDC)
    #print "creating "+filename+" \t ARGUMENTS:\n ",arguments, "\n"                       
    f.write("executable            = "+PWD+"run_AnalysisMP.py \n")
    f.write("arguments             = "+arguments+"\n")
    f.write("output                = "+folder+"/"+jobsent+".$(ClusterId).out\n")
    f.write("error                 = "+folder+"/"+jobsent+".$(ClusterId).err\n")
    f.write("log                   = "+folder+"/"+jobsent+".$(ClusterId).log\n")
    #f.write("+JobFlavour           = nextweek\n")
    f.write("+JobFlavour           = testmatch\n")
    #f.write("+JobFlavour           = tomorrow\n")
    f.write("queue "+sigset+' from '+folder+'/joblist.txt \n')
    f.close()



#Remove duplicated substrings in a string
def rreplace(s, old, new, occurrence):
    li = s.rsplit(old, occurrence)
    return new.join(li)

if len(sys.argv)<4:      
    print 'Please, specify year, tag and sigset values, in that order'
    sys.exit() 

#Take args
if sys.argv[1]=='-1':
    year='2016-2017-2018'
elif sys.argv[1]=='0':
    year='2016'
elif sys.argv[1]=='1':
    year='2017'
elif sys.argv[1]=='2':
    year='2018'
else:
    year=sys.argv[1]
if   sys.argv[2]== '0':                                                             
    tag='Preselection'                                                             
elif sys.argv[2]== '1':                                                            
    tag='ValidationRegions'                                                        
elif sys.argv[2]=='2':                                                             
    tag='StopSignalRegions'                                                        
else:                                                                              
    tag=sys.argv[2] 
sigset  = sys.argv[3]

doDC    = ' '
if(len(sys.argv)>4):
    if(sys.argv[4].lower()in ["dodatacards","dodc", "mkdc","makedatacards"]):
        doDC=sys.argv[4]
        fileset=sigset
    else:
        fileset=sys.argv[4]
        
    if(len(sys.argv)>5): 
        doDC    = sys.argv[5]
else: fileset=sigset
exec(open("signalMassPoints.py").read())


#Look for masspoints in the sigset
mpInSigset=[]
for model in signalMassPoints:
    print "Model:", model,"\tSignal set", sigset
    if model not in sigset:  continue
    for massPoint in signalMassPoints[model]:
        if(massPointInSignalSet(massPoint,sigset)):
            submitThis = True
	    rootname = './Limits/' + year + '/' + tag + '/' + massPoint + '/higgsCombine_' + tag + '_Blind.AsymptoticLimits.mH120.root'
            if os.path.isfile(rootname):  
                if os.path.getsize(rootname)>6500:
                    submitThis = False
	    if submitThis:
		print 'submmm', massPoint 
                mpInSigset.append(massPoint)
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
        if(firstsigset[j]!=thissigset[j]):
            if(j<len(thissigset)-1): diffmp='-'
            firstpart = (firstsigset[j]+'_').split('-')
            thispart  = (thissigset[j]+'_').split('-')
            writesigset[j]+=diffmp+'-'+thissigset[j]

#remove duplicate mS and similars            
try:
    nmS = writesigset[1].count('mS')
    nmX = writesigset[2].count('mX')
except IndexError:
    nmS=0
    nmX=0
    print "either no mS or mX specified"

    if(nmS>1):   writesigset[1] = rreplace(writesigset[1] , 'mS', '', nmS - 1)
    elif(nmX>1): writesigset[2] = rreplace(writesigset[2] , 'mX', '', nmX - 1)

#divide masspoints in sets of nMPs and send jobs
nMPs        = 1
lognm       = '_'.join(writesigset)
jobfolder   = "./Condor/"+year+'/'+tag
logfile     = jobfolder + '/'+lognm+".log"
subfilename = jobfolder + '/'+lognm+".sub"
flistname   = jobfolder+'/joblist.txt'

os.system("mkdir -p "+jobfolder)
logtitle(logfile,fileset)
logline =   "Input arguments:\t"+ year + ' ' + tag + ' ' + fileset + ' ' + doDC
logline+= "\nSample list    :\t" + flistname
logline+= "\nSubmission file:\t"+ subfilename
writetolog(logfile, logline)

jobs     = [sorted(mpInSigset)[x:x+nMPs] for x in xrange(0, len(mpInSigset), nMPs)]
flist    = open(flistname,"w+")
for ijob,job in enumerate(jobs):
    argsigset = ",".join(job)
    flist.write(argsigset+'\n')
    submit="condor_submit "+subfilename+" >>"+logfile
    print "sending job",str(ijob)+":", argsigset 
flist.close()
#Function to create sub file                                                         

makeSubFile2(subfilename,jobfolder, year, tag, 'MPs' , fileset,doDC,lognm)
commandtorun="condor_submit "+subfilename+">>"+logfile
os.system(commandtorun)
print "jobs sent:\n", commandtorun
writetolog(logfile,"----------------------------------")

print "LIMITS SENT\nlog file:\t"+logfile,"\nsub file:\t"+subfilename,"\njob list:\t"+flistname 

