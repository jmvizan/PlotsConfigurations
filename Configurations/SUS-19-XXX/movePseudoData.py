import os,sys, ROOT
from datetime import datetime
import numpy as np
import submit_mkShapes
def confirm():
    answer = raw_input("Do you wish to continue? [Y/N] ").lower()
    if answer in ["no","n"]:
        print "aborting..."
        exit()
    return

def movePseudoData(fol_i,file_i, fol_f, file_f):
    

    print fol_i+file_i, os.path.isfile(fol_i+file_i)
    if os.path.isfile(fol_i+file_i):
        if os.path.isdir(fol_f) is False: os.system('mkdir -p '+fol_f)
        print "to", fol_f+file_f, os.path.isfile(fol_f+file_f)
        os.system('cp '+fol_i+file_i+' '+fol_f+file_f)
    else:
        print "looks like the input file is wrong"
 


lxshapes = 'pmatorra@lxplus.cern.ch:/eos/user/s/scodella/SUSY/ShapesV9'
if __name__ == '__main__':
    args=sys.argv
    if len(args)<3:
        print 'Please, specify year, tag and sigset values, in that order'
        sys.exit()

    if   args[1] == '-1':
        yearset = ['2016HIPM', '2016noHIPM','2017','2018']
    elif args[1] == '0':
        yearset = ['2016']
    elif args[1] == '0b':
        yearset = ['2016HIPM', '2016noHIPM']
    elif args[1] == '1':
        yearset = ['2017']
    elif args[1] == '2':
        yearset = ['2018']
    else:
        yearset = args[1].split('_')

    yearnm   = '-'.join(yearset)
    tags_ini = args[2]
    tags_fin = args[3]
    if len(args) ==3:
        version='ALL_DATA'
    elif len(args[4].split('_'))==1:
        version = '_ALL_'+args[4]
    else:
        version = '_'+args[4]
    doAll    = False
    doLxplus = False
    doMove   = False
    doMerge  = False
    if 'lxplus' in args[-1].lower(): doLxplus = True
    if 'merge'  in args[-1].lower(): doMerge  = True
    if 'move'   in args[-1].lower(): doMove   = True
    if args[-1].lower()=='all': 
        doAll    = True
        doLxplus = True
        doMove   = True
        doMerge  = True
    
    print "years", yearset
    print "tags_ini ", tags_ini
    if len(tags_ini.split('-'))>1 or len(yearset)>1: confirm()
    for idx, tag_ini in enumerate(tags_ini.split('-')):
        tag_fin = tags_fin.split('-')[idx]
        if "shapes" in args[-1].lower() or doAll:
            args_shapes = ['',args[1], tag_ini, '1', args[4]]
            print "Moving to submit_mkShapes.py with arguments:", args_shapes 
            submit_mkShapes.submit_shapes(args_shapes)

        for year in yearset:
            print tag_ini, year
            fol_i  = os.getcwd()+'/Shapes/'+year+'/'+tag_ini+'/'
            fol_f  = os.getcwd()+'/Shapes/'+year+'/'+tag_fin+'/'
            file_i = 'plots_'+year+tag_ini+version+'.root'#.replace('.root','.broot')
            file_f = 'plots_'+year+tag_fin+version+'.root'#.replace('.root','.broot')
            if '_ALL_' in version: 
                fol_i  +='Samples/'
                fol_f  +='Samples/'
            else:
                file_i  = file_i.replace(year,'')
                file_f  = file_f.replace(year,'')

            if doMove:
                movePseudoData(fol_i, file_i, fol_f, file_f)
                if doLxplus:
                    ssh_command = 'scp -r '+fol_f+file_f+' '+lxshapes+'/'+fol_f.split('Shapes/')[-1]
                    print ssh_command
                    os.system(ssh_command)
        if doMerge:
            arguments =  './mergeShapes.py --years=0b --tag='+tag_fin+' --sigset='+args[4]+' --outputDir=./Shapes/2016/'+tag_fin+'/ --skipLNN'
            print arguments
            os.system(arguments)
            print "here?"
            
        if doLxplus or doAll: 
            fol_merge   = os.getcwd()+'/Shapes/2016/'+tag_fin+'/'
            ssh_command = 'scp -r '+fol_merge+file_f+' '+lxshapes+'/'+fol_merge.split('Shapes/')[-1]
            print "this one", ssh_command
            os.system(ssh_command)
        
