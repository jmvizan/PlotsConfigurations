import os, sys
from ROOT import TH1D, TH2D, TFile, TTree, TCanvas, gROOT, gStyle
import numpy as np


def getall(d, basepath="/"):
    "Generator function to recurse into a ROOT file/dir and yield (path, obj) pairs"
    for key in d.GetListOfKeys():
        kname = key.GetName()
        if key.IsFolder():
            # TODO: -> "yield from" in Py3
            for i in getall(d.Get(kname), basepath+kname+"/"):
                yield i
        else:
            yield basepath+kname, d.Get(kname)



inpfile=TFile ('../lxplus/plots_HighPtMissOptimisationRegion_SM-T2tt_mS-400to700.root', "READ")
wloc=os.environ['WWW']
optim=wloc+"/susy/optimisation/"
folder=inpfile.cd('VR1_Tag_sf')
#folder="VR1_Tag_sf"#/mt2ptmiss"
#unrolled=inpfile.Get(folder+"/histo_ttbar")
regions=["VR1_Tag_sf", "VR1_Tag_em", "VR1_Veto_em", "VR1_Veto_sf"]
folder="../Histograms/significance/"
os.system("mkdir -p "+folder)
gROOT.SetBatch(True)

for reg in regions:
    nMT2=100
    nptmiss=100
    signal1D= TH1D("signal1D"+reg, reg, 10000, 0, 10000)
    bkg1D   = TH1D("bkgs1D"+reg  , reg, 10000, 0, 10000)
    signal2D= TH2D("signal2D"+reg, reg, nMT2, 0, 1000, nptmiss, 0, 2000)
    bkg2D   = TH2D("bkgs2D"+reg  , reg, nMT2, 0, 1000, nptmiss, 0, 2000)
    signif2D= TH2D("signif2D"+reg, reg, nMT2, 0, 1000, nptmiss, 0, 2000)
    dmass=200
    mSmin=400
    mSmax=700
    signif2D.SetTitle("m_{T2ll} vs p_{T}^{miss} ("+reg+")")
    signif2D.SetYTitle("m_{T2ll} [GeV]")
    signif2D.SetXTitle("p_{T}^{miss} [GeV]")
    allhistos=getall(inpfile)# folder)
    for ihis, histloc in enumerate(allhistos):
        histnm=histloc[0]
        hsplit = histnm.split('mS')
        isSig =False
        if(reg not in histnm): continue
        #if ihis>3: break # continue

        if len(hsplit) >1:
            isSig=True
            mass=hsplit[1].replace('-','_').split('_')
            mS=int(mass[1])
            mX=int(mass[3])
            if(mS<mSmin or mS>mSmax):
                #print "mS not in ", mSmin, mSmax
                continue
            if(mS-mX<dmass):
                #print "histo not in mass range"
                continue
    
        histo=inpfile.Get(histnm)
        if(isSig is True): signal1D.Add(histo)
        else: bkg1D.Add(histo)



    nbin=signal1D.GetNbinsX()
    y=0
    x=0
    n=0
    for i in range(1,nbin):
        if (i % nMT2 is 0):
            x+=1
            y=0
        y+=1
        isig=signal1D.GetBinContent(i)
        ibkg=bkg1D.GetBinContent(i)
        #if ientry<0.01: continue
        if(isig>0):signal2D.SetBinContent(x,y,isig)
        if(ibkg>0): bkg2D.SetBinContent(x,y, ibkg)
        if(ibkg>25 and isig>5): signif2D.SetBinContent(x,y,isig/np.sqrt(ibkg))
        #print nbin, signal1D.GetBinContent(nbin)
        #break
    print signal1D.GetEntries()

    #exit()
    c1 = TCanvas( 'c1', 'Dynamic Filling Example', 200,10, 1600, 900 )
    #signal2D.Draw('colz')
    #bkg2D.Draw('colz')
    gStyle.SetPaintTextFormat("4.1f");
    signif2D.Draw('colz text')
    signif2D.GetYaxis().SetRangeUser(0,200);
    signif2D.GetXaxis().SetRangeUser(0,400);
    c1.SaveAs(folder+"mt2vsptmiss"+reg+'.png')
    #os.system("display "+regions[0]+".png")
    print signal1D.GetEntries()
    
os.system("cp "+optim+'/index.php '+folder)
os.system('cp -r '+folder+" "+ optim)
    #exit()
    
