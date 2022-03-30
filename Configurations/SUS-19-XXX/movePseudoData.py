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

    yearnm  = '-'.join(yearset)
    tags    = args[2]
    if len(args) ==3:
        version='ALL_DATA'
    elif len(args[3].split('_'))==1:
        version = '_ALL_'+args[3]
    else:
        version = '_'+args[3]
    doAll = False
    if args[-1].lower()=='all': doAll = True
    if "shapes" in args[-1].lower() or args[-1].lower()=='all':
        args_shapes = ['',args[1], args[2].replace('WWSF','').replace('PseudoData',''), '1', args[3]]
        print "Moving to submit_mkShapes.py with arguments:", args_shapes 
        submit_mkShapes.submit_shapes(args_shapes)
    print "years", yearset
    print "tags ", tags
    if len(tags.split('-'))>1 or len(yearset)>1: confirm()
    for tag in tags.split('-'):
        for year in yearset:
            print tag, year
            fol_f  = os.getcwd()+'/Shapes/'+year+'/'+tag+'/'
            file_f = 'plots_'+year+tag+version+'.root'#.replace('.root','.broot')
            if '_ALL_' in version: 
                fol_f  +='Samples/'
            else:
                file_f  = file_f.replace(year,'')
                print "have i changed?", file_f
            fol_i  = fol_f.replace('WWSF','').replace('PseudoData','')
            file_i = file_f.replace('WWSF','').replace('PseudoData','')#.replace('b.root','.root')
            
            print fol_i+file_i, os.path.isfile(fol_i+file_i)
            print "to", fol_f+file_f, os.path.isfile(fol_f+file_f)
            if os.path.isfile(fol_i+file_i):
                os.system('cp '+fol_i+file_i+' '+fol_f+file_f)
            else:
                print "looks like the wrong file"
            if 'lxplus' in args[-1].lower() or doAll:
                ssh_command = 'scp -r '+fol_f+file_f+' '+lxshapes+'/'+fol_f.split('Shapes/')[-1]
                print ssh_command
                os.system(ssh_command)
        if 'merge' in args[-1].lower() or doAll:
            arguments= './mergeShapes.py --years=0b --tag='+tag+' --sigset='+args[3]+' --outputDir=./Shapes/2016/'+tags+'/ --skipLNN'
            print arguments
            if 'lxplus' in args[-1] or doAll: 
                fol_merge   = os.getcwd()+'/Shapes/2016/'+tag+'/'
                ssh_command = 'scp -r '+fol_merge+file_f+' '+lxshapes+'/'+fol_merge.split('Shapes/')[-1]
                print "this one", ssh_command
                os.system(ssh_command)
        
