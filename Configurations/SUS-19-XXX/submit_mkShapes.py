#!/usr/bin/env python
import os,sys
from datetime import datetime
# ask for confirmation to run the commands
def confirm():
    answer = raw_input("Do you wish to continue? [Y/N] ").lower()
    if answer in ["no","n"]: 
        print "aborting..."
        exit()
    return 


def logtitle(filename,sigset):
    if(os.path.exists(filename) is False):  print "CREATING LOG FILE :"+filename
    f = open(filename,"a")
    # Textual month, day and year                                                                      
    now = datetime.now()
    d2  = now.strftime("%d %B, %Y, at %H:%M:%S")
    f.write(d2+"\nCALCULATING LIMITS FOR:\t "+ sigset+"\n")
    f.close()
def readsamples(sigset):
    with open(sigset) as sigfile:
        samples=sigfile.read().splitlines()
    return samples

if __name__ == '__main__':
    doDC=False
    args=sys.argv
    if len(args)<4:
        print 'Please, specify year, tag and sigset values, in that order'
        sys.exit()

    if   args[1] == '-1':
        yearset = ['2016','2017','2018']
    elif args[1] == '0':
        yearset = ['2016']
    elif args[1] == '1':
        yearset = ['2017']
    elif args[1] == '2':
        yearset = ['2018']
    else:
        yearset = args[1].split('_')

    if   args[2] == '0':
        tags = 'Preselection'
    elif args[2] == '1':
        tags = 'ValidationRegions'
    elif args[2] == '2':
        tags = 'StopSignalRegions'
    else:
        tags = args[2]
    
    #    tags=sys.argv[2]                                                                         
    lastarg = len(args)-1
    yearnm  = '-'.join(yearset)
    hadd    = args[3]
    sigset  = args[4]
    queue   = ''
    split   = ''
    rmlog   = None
    runopts = ['tomorrow','workday','cms_high','cms_med','cms_main']
    if 'rm' in args[lastarg]:
        args[lastarg] = ''
        rmlog = True
    elif args[lastarg] in  runopts:
        queue = args[lastarg]
        split = args[lastarg-1]
    else: split = args[lastarg]

    yearnm = '-'.join(yearset)
    hadd   = args[3]
    sigset = args[4]
    
    multi  = 'Multi'
    
    if '_notmulti' in tags.lower() : 
        multi = ''
        tags   = tags.split('_notmulti')[0]
        print "not running on multi"

    queue  = ''
    split  = ''
    rmlog  = None
    if 'rm' in args[len(args)-1]:
        args[len(args)-1] = ''
        rmlog = True
    if len(args)>5: 
        if args[5] in ['tomorrow','workday','cms_high','cms_med','cms_main']: 
            queue = args[5]
            if len(args)>6: 
                split = args[6]
        else:
            split  = args[5]
    
    if "amap" in split.lower(): split = "AsMuchAsPossible"
    
    script    = './run_mkShapes'+multi+'.sh'
    keepsplit = False
    allsam    = None
    bkgs      = ['ttbar','tW','ttW','VZ','VVV','WZ','ttZ','ZZ', 'DY', 'Higgs']
    bkgsend   = ['BackgroundsVetoDYVetottbar','Backgroundsttbar','BackgroundsDY','BackgroundsZZTo4L', 'BackgroundsEOY']
    smsend    = bkgsend+ ['Data']
    for signal in sigset.split('__'):
        print "sample:",signal
    if        len(sigset.split('__'))>1 : allsend = sigset.split('__')
    elif           '.' in sigset        : allsend = readsamples(sigset)
    elif 'backgrounds' in split.lower() : allsend = bkgsend
    elif          'SM' in split         : allsend = smsend
    elif        'plot' in args[-1].lower() : 
        allsend = ["SM"]
        script  = './run_mkPlot.sh'
        hadd    = '' 
    elif         'all' in split.lower() :
        if hadd == '1' and "SM-" not in sigset and sigset not in smsend+["SM","Backgrounds"]: sigset="SM-"+sigset
        if sigset.replace('Backgrounds','') in bkgs or sigset == 'Data': 
            print "please choose a valid signal"
            exit()
        elif "mc" in split.lower(): allsend = bkgsend
        elif hadd == '0' and sigset in ["SM", "Backgrounds"]:
            allsend = smsend
        else: allsend = smsend+[sigset]
    else: 
        allsend   = [sigset]
        keepsplit = True

    shapes_fol  = "./Shapes/log/"+yearnm+'/'
    allcomms    = []
    for tag in tags.split('_'):
        skipZZ4L = True
        if 'ZZValidationRegion' in tags or 'ttZ' in tags or 'WZValidationRegion' in tags or 'WZtoWWValidationRegion' in tags or 'FitCRWZ' in tags or 'FitCRZZ' in tags or ('FitCR' in tags and isDatacardOrPlot) or 'TheoryNormalizations' in tags: skipZZ4L = False
        #shapes_file = shapes_fol+tag+'_'+sigset+'.log'
        #os.system('mkdir -p '+shapes_fol)
        
        if rmlog:
            os.system('rm '+shapes_file)
            print "REMOVING FILE:\n", shapes_file
        #logtitle(shapes_file,tag+" "+sigset+" "+split)
        for samsend in allsend:
            if skipZZ4L and "ZZ" in samsend: 
                print "this should skip", samsend
                continue
            if hadd =='1' and 'Veto' in samsend: continue
            #if hadd =='0' and all_sam is True and  : continue
            if keepsplit is False:
                if samsend in smsend and 'Veto' not in samsend and 'EOY' not in samsend:
                    split = 'AsMuchAsPossible'
                else:
                    split = ''
            for year in yearset:
                command = script+" "+ year +" "+tag+" "+hadd+" "+samsend+" "+split
                allcomms.append(command)
    print "Commands to be ran:"
    for comm in allcomms:
        print comm
        
    if len(allcomms)>1: confirm()
    
    for comm in allcomms:
        print comm
        os.system(comm)#+" 2>&1 | tee -a "+shapes_file)

    #print "Shapes logfile in: \n"+shapes_file
