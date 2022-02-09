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
    #sigset = args[3]

    #c1 = ROOT.TCanvas( 'c1', 'Dynamic Filling Example', 200,10, 1600, 900 )
    for year in yearset:
        for tag in tags.split('-'):
            #Get the combined version
            print tag, year
            folder    = os.getcwd()+'/Shapes/'+year+'/'+tag+'/Samples/'
            infiles   = []
            infiles   = [f for f in  os.listdir(folder) if tag in f and year in f and "DATA" not in f and "_TChi" not in f and "_T2tt" not in f]
            outfilenm = 'plots_'+year+tag+'_ALL_DATA.root'
            outfile   = ROOT.TFile(folder+outfilenm,"RECREATE","Final merged one");
            print "Files over which we are looping\n",infiles
            #exit()
            #infiles  = [infiles[0]]
            for infilenm in infiles:
                print "File:", infilenm
                sig_i  = infilenm.split('ALL')[1].split('.root')[0]
                infile = ROOT.TFile(folder+infilenm, "READ", infilenm)
                keys   = infile.GetListOfKeys()
                for key in keys:
                    #key    = keys[0]
                    keynm  = key.GetTitle()
                    #keynm  = "SR2_Veto_sf"
                    print "Folder:", key.GetTitle()
                    var = 'mt2ll'
                    h1  =  infile.Get(keynm).Get(var).Get('histo'+sig_i)
                    fol_i = keynm+'/'+var
                    
                    if bool(outfile.FindObject(keynm)) is False:
                        print "FIRST ITERATION:", keynm
                        dict_i = outfile.mkdir(fol_i)
                        outfile.cd(fol_i)
                        #print "ee", outfile.ls()
                        h2 = h1.Clone("histo_DATA")
                        h2.Write()
                        #outfile.cd()
                        print "done"
                    else:
                        print "yey", keynm
                        outfile.cd(fol_i)
                        h4 = outfile.Get(keynm).Get(var).Get('histo_DATA')
                        h4.Add(h1)
                        #print h4
                        #h4.Draw()
                        #c1.SaveAs(keynm+sig_i+'.png')
                        h4.Write()
                    outfile.cd()
                    
            print "DONE WITH THE FIRST PART"
            print tag, year
            folder  = os.getcwd()+'/Shapes/'+year+'/'+tag+'/Samples/'
            #outfile  = ROOT.TFile(folder+'plots_'+year+tag+'_ALL_DATA.root', "UPDATE")
            print outfile.ls()
            keys   = outfile.GetListOfKeys()
            var    = 'mt2ll'
            print keys
            for key in keys:

                keynm  = key.GetTitle()
                print "FOL_I", keynm
                outfile.cd(keynm)
                #print outfile.ls()                                                     
                h1  =  outfile.Get(keynm).Get('histo_DATA')
                #h1_err = h1.Clone('histo_DATA_err')

                for  i_bin in range(0, h1.GetNbinsX()+1):
                    #print np.sqrt(h1.GetBinContent(i_bin))                            
                    h1.SetBinError(i_bin, np.sqrt(h1.GetBinContent(i_bin)))
                h1.Write()
                #print h1.GetEntries()                                                 
                outfile.cd()
            print "Final Root file in", folder+outfilenm
