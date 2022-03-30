#!/usr/bin/env python                                                                                                                        
import os,sys, ROOT
from datetime import datetime
import numpy as np
# ask for confirmation to run the commands                                                                                                   
def confirm():
    answer = raw_input("Do you wish to continue? [Y/N] ").lower()
    if answer in ["no","n"]:
        print "aborting..."
        exit()
    return

if __name__ == '__main__':
    args=sys.argv
    if len(args)<3:
        print 'Please, specify year, tag and sigset values, in that order'
        sys.exit()

    if   args[1] == '-1':
        yearset = ['2016HIPM', '2016noHIPM','2017','2018']
    elif args[1] == '0':
        yearset = ['2016']
    elif args[1] == '1':
        yearset = ['2017']
    elif args[1] == '2':
        yearset = ['2018']
    else:
        yearset = args[1].split('_')

    yearnm = '-'.join(yearset)
    tags   = args[2]
    rmtag  = args[3]

    print "years", yearset
    print "tags ", tags
    if len(tags.split('-'))>1 or len(yearset)>1: confirm()
    #c1 = ROOT.TCanvas( 'c1', 'Dynamic Filling Example', 200,10, 1600, 900 )
    for year in yearset:
        for tag in tags.split('-'):
            #Get the combined version
            print tag, year
            folder    = os.getcwd()+'/Shapes/'+year+'/'+tag+'/Samples/'
            infiles   = []
            infiles   = [f for f in  os.listdir(folder) if tag in f and year in f and "DATA" not in f and "_TChi" not in f and "_T2tt" not in f and "_EOY." not in f and 'EOYWJets' not in f]
            outfilenm = 'plots_'+year+tag+'_ALL_DATA.root'
            outfile   = ROOT.TFile(folder+outfilenm,"RECREATE","Final merged one");
            print "Files over which we are looping\n",infiles
            for infilenm in infiles:
                print "File:", infilenm
                sig_i  = infilenm.split('ALL')[1].split('.root')[0]
                infile = ROOT.TFile(folder+infilenm, "READ", infilenm)
                keys   = infile.GetListOfKeys()
                for key in keys:
                    keynm = key.GetTitle()
                    var   = 'mt2ll'
                    h1    =  infile.Get(keynm).Get(var).Get('histo'+sig_i)
                    fol_i = keynm+'/'+var
                    
                    if bool(outfile.FindObject(keynm)) is False:
                        dict_i = outfile.mkdir(fol_i)
                        outfile.cd(fol_i)
                        h2     = h1.Clone("histo_DATA")
                        h2.Write()
                        if 'SR1_NoJet_em' in keynm: print "first bin", h2.GetBinContent(3)
                        
                        
                    else:
                        outfile.cd(fol_i)
                        h4 = outfile.Get(keynm).Get(var).Get('histo_DATA')
                        h4.Add(h1)
                        if 'SR1_NoJet_em' in keynm: print "first bin", h4.GetBinContent(3)
                        h4.Write()
                    outfile.cd()
                    
            print "\nCalculating the uncertainty for the new data events..."
            print tag, year
            folder = os.getcwd()+'/Shapes/'+year+'/'+tag+'/Samples/'
            keys   = outfile.GetListOfKeys()
            var    = 'mt2ll'
            print keys
            for key in keys:

                keynm  = key.GetTitle()
                outfile.cd(keynm)
                h1  =  outfile.Get(keynm).Get('histo_DATA')
                
                for  i_bin in range(0, h1.GetNbinsX()+1):
                    i_content = h1.GetBinContent(i_bin)
                    h1.SetBinContent(i_bin, int(i_content))
                    h1.SetBinError(i_bin, np.sqrt(i_content))
                h1.Write()
                outfile.cd()
            print "\nFinal Root file in", folder+outfilenm
            newplace = folder.replace(rmtag,'') + outfilenm.replace(rmtag,'')
            print "Moving root file to "+ newplace
            #confirm()
            #os.system('rm '+newplace+outfilenm)
            #os.system('cp '+folder+outfilenm+' '+newplace)
            #print "check it works!" 
