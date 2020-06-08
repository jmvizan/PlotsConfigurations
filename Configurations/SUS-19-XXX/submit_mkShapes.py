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
    if(os.path.exists(filename) is False):  print "CREATING LOG FILE\n:"+filename
    f = open(filename,"a")
    # Textual month, day and year                                                                      
    now = datetime.now()
    d2  = now.strftime("%d %B, %Y, at %H:%M:%S")
    f.write(d2+"\nCALCULATING LIMITS FOR:\t "+ sigset+"\n")
    f.close()


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
        yearset = args[1].split('-')

    if   args[2] == '0':
        tag = 'Preselection'
    elif args[2] == '1':
        tag = 'ValidationRegions'
    elif args[2] == '2':
        tag = 'StopSignalRegions'
    else:
        tag = args[2]

    #    tag=sys.argv[2]                                                                         
    yearnm = '-'.join(yearset)
    hadd   = args[3]
    sigset = args[4]
    queue  = ''
    split  = ''
    rmlog  = None
    if 'rm' in args[len(args)-1]:
        args[len(args)-1] = ''
        rmlog = True

    if len(args)>5: 
        if args[5] in ['tomorrow','workday','gridui_sort']: 
            queue = args[5]
            if len(args)>6: 
                split = args[6]
        else:
            split  = args[5]
    
    keepsplit = False
    allsam  = None
    bkgs    = ['ttbar','tW','ttW','VZ','VVV','WZ','ttZ','ZZ', 'DY']
    bkgsend = ['BackgroundsVetoDYVetottbar','Backgroundsttbar','BackgroundsDY']
    smsend  = bkgsend+ ['Data']
    if 'backgrounds' in split.lower(): allsend = bkgsend
    elif        'sm' in split.lower(): allsend = smsend
    elif       'all' in split.lower(): 
        all_sam = True
        if sigset in bkgs or sigset == 'Data': 
            print "please choose a valid signal"
            exit()
        else:
            allsend = smsend+[sigset]
    else: 
        allsend   = [sigset]
        keepsplit = True

    shapes_fol  = "./Shapes/"+yearnm+'/log/'
    shapes_file = shapes_fol+tag+'_'+sigset+'.log'
    os.system('mkdir -p '+shapes_fol)
    allcomms= []

    if rmlog:
        os.system('rm '+shapes_file)
        print "REMOVING FILE:\n", shapes_file
    logtitle(shapes_file,tag+" "+sigset+" "+split)
    for samsend in allsend:
        if keepsplit is False:
            if samsend in smsend and 'Veto' not in samsend:
                split = 'AsMuchAsPossible'
            else:
                split = ''
        for year in yearset:
            command = "./run_mkShapes.sh "+ year +" "+tag+" "+hadd+" "+samsend+" "+split
            allcomms.append(command)
    print "Commands to be run:"
    for comm in allcomms:
        print comm
        
    if len(allsend)>1: confirm()
    
    #exit()
    for comm in allcomms:
        print comm
        os.system(comm+" 2>&1 | tee -a "+shapes_file)

    print "Shapes logfile in: \n"+shapes_file
