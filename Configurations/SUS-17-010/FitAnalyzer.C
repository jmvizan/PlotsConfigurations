#include "TCanvas.h"
#include "TH1D.h"
#include "TH2D.h"
#include "TString.h"
#include "TFile.h"
#include <TROOT.h>
#include <TStyle.h>
#include <TLegend.h>
#include <TLatex.h>

#include "../../../AnalysisCMS/include/CutsStop.h"

const int nChannels = 3;
TString Channel[nChannels] = {"em", "ee", "mm"};

TString DataSampleName = "01_PseudoDataSmeared";
const int nBackgroundSamples = 7;
TString BackgroundSampleName[nBackgroundSamples] = {"04_TTTo2L2Nu", "05_ST", "06_WW", "03_VZ", "07_Zjets", "09_TTW", "10_TTZ"};

bool VRForChannel = false;
TString FitDirectory = "shapes_fit_b";
bool VR1FitSplitChannels = false;

void VR1Fit(TString FitFileName, TString ShapeFileName, TString OutputDirectory, TString FitRegion) {

  TFile *FitFile    = new TFile(FitFileName, "read");
  TFile *ShapeVRFile  = new TFile(ShapeFileName, "read");
  TFile *ShapeFile  = new TFile("./Shapes/ShapesBackgrounds.root", "read"); // -> Use root file for whatever mass point

  int nBins = 7; float LowEdgeHisto = 0., HighEdgeHisto = 140.;

  TH1F *DataHisto[nChannels+1], *BkgHisto[nChannels+1];
  for (int ch = 0; ch<nChannels; ch++) {
    
    DataHisto[ch]    = new TH1F("Data_"  + Channel[ch], "", nBins, LowEdgeHisto, HighEdgeHisto);
    BkgHisto[ch]     = new TH1F("Bkg_"   + Channel[ch], "", nBins, LowEdgeHisto, HighEdgeHisto);

    if (ch==nChannels-1) {
      DataHisto[nChannels]    = new TH1F("Data_all",  "", nBins, LowEdgeHisto, HighEdgeHisto);
      BkgHisto[nChannels]     = new TH1F("Bkg_all",   "", nBins, LowEdgeHisto, HighEdgeHisto);
    }

  }

  TString VRName  = "VR1_" + FitRegion;

  for (int ch = 0; ch<nChannels; ch++) {

    TString Bin = "";
    if (!FitFileName.Contains("Tag")) Bin = FitRegion + "_";
    TString DataHistoName = VRName + "_" + Channel[ch] + "/MT2ll/histo_" + DataSampleName;
    TH1F *ThisDataHisto = (TH1F*) ShapeVRFile->Get(DataHistoName);
    DataHisto[ch]->Add(ThisDataHisto);
    
    for (int bkg = 0; bkg<nBackgroundSamples; bkg++) {

      TString BackHistoName = FitDirectory + "/" + Bin + Channel[ch] + "/" + BackgroundSampleName[bkg];
      TH1F *FitBackHisto = (TH1F*) FitFile->Get(BackHistoName);
      TH1F *ThisBackHisto = new TH1F("Fit_" + BackgroundSampleName[bkg] + "_" + Channel[ch], "", nBins, LowEdgeHisto, HighEdgeHisto);
      for (int ib = 1; ib<=nBins; ib++) {

	ThisBackHisto->SetBinContent(ib, FitBackHisto->GetBinContent(ib));
	ThisBackHisto->SetBinError(ib, FitBackHisto->GetBinError(ib));

      }

      if (FitRegion=="Tag" && bkg<2) BkgHisto[ch]->Add(ThisBackHisto);
      else if (FitRegion=="NoTag" && bkg==2) BkgHisto[ch]->Add(ThisBackHisto);
      else DataHisto[ch]->Add(ThisBackHisto, -1.);

    }

    DataHisto[nChannels]->Add(DataHisto[ch]);
    BkgHisto[nChannels]->Add(BkgHisto[ch]);

  }

  TString OutputFileName = OutputDirectory + "/VR1" + FitRegion + "Fit.root";
  if (!FitFileName.Contains("Tag") && FitRegion=="Tag") OutputFileName.ReplaceAll(".root", "_step2.root");
  TFile *OutputFile = new TFile(OutputFileName, "recreate");
  
  for (int ch = 0; ch<nChannels+1; ch++) {

    DataHisto[ch]->Write();
    BkgHisto[ch]->Write();
    DataHisto[ch]->Divide(BkgHisto[ch]);
    TString HistoName = DataHisto[ch]->GetName();
    HistoName.ReplaceAll("Data", "Ratio");
    DataHisto[ch]->SetName(HistoName);
    DataHisto[ch]->Write();

  }

  for (int ct = 0; ct<ncut; ct++) {

    TString SRName = scut[ct];
    SRName.ReplaceAll("Stop/02_", "");
    
    if (!SRName.Contains("VR1") && !SRName.Contains("SR")) continue;
    //if (SRName!="VR1_NoTag" && !SRName.Contains("SR")) continue;
    //if (SRName=="VR1_NoTag" && FitRegion=="NoTag") continue;
    
    for (int ch = 0; ch<nChannels; ch++) {
    
      TString CutName = SRName + "_" + Channel[ch];

      OutputFile->mkdir(CutName);
      OutputFile->cd(CutName);

      for (int tbg = 0; tbg<=2; tbg++) {

	if (FitRegion=="Tag" && tbg==2) continue;
	if (FitRegion=="NoTag" && tbg<2) continue;
	
	TString HistoName = "histo_" + BackgroundSampleName[tbg];
	TH1F *ThisHisto;
	if (!SRName.Contains("SR")) ThisHisto = (TH1F*) ShapeVRFile->Get(CutName + "/MT2ll/" + HistoName);
	else ThisHisto = (TH1F*) ShapeFile->Get(CutName + "/MT2ll/" + HistoName);
	ThisHisto->Write();
	
	TString SystematicName = tbg<2 ? "_TopMT2llShape" : "_WWMT2llShape";

	HistoName += SystematicName;
	if (VRForChannel) HistoName += ("_" + Channel[ch]); 
	ThisHisto->SetName(HistoName + "Down");
	ThisHisto->Write();
	if (VRForChannel) ThisHisto->Multiply(DataHisto[ch]); 
	else ThisHisto->Multiply(DataHisto[nChannels]); 
	ThisHisto->SetName(HistoName + "Up");
	ThisHisto->Write();

      }
      
    }

  }

  OutputFile->Close();
  
}

void FitAnalyzer(TString Action) {
  
  if (Action.Contains("FitVR1Tag"))  
    VR1Fit("./Datacards/ValidationRegions/mlfitVR1Tag.root", "./Shapes/ShapesVR1.root", "./Datacards", "Tag");
  
  if (Action.Contains("FitVR1NoTag"))
    VR1Fit("./Datacards/ValidationRegions/mlfitVR1NoTag.root", "./Shapes/ShapesVR1.root", "./Datacards", "NoTag");
  
  if (Action=="FitVR1") {
    VR1Fit("./Datacards/ValidationRegions/mlfitVR1.root", "./Shapes/ShapesVR1.root", "./Datacards", "NoTag");
    VR1Fit("./Datacards/ValidationRegions/mlfitVR1.root", "./Shapes/ShapesVR1.root", "./Datacards", "Tag");
  }

}
