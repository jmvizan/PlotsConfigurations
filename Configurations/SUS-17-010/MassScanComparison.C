#include "TCanvas.h"
#include "TH1D.h"
#include "TH2D.h"
#include "TString.h"
#include "TFile.h"
#include <TROOT.h>
#include <TStyle.h>
#include <TLegend.h>
#include <TLatex.h>

void MassScanComparison(TString Type = "", TString Reference = "" , TString Version = "", TString Signal = "") {

  TH2F *MassLimit;
  if (Signal=="" || Signal.Contains("T2tt")) {
    //MassLimit = new TH2F("MassLimit", "", 9, 287.5, 512.5, 13, 112.5, 437.5);
    //MassLimit = new TH2F("MassLimit", "", 17, 187.5, 612.5, 18, 87.5, 537.5);
    MassLimit = new TH2F("MassLimit", "", 42, 162.5, 1212.5, 32,  12.5, 812.5);
  } else if (Signal.Contains("T2bW")) {
    MassLimit = new TH2F("MassLimit",    "", 21, 187.5,  712.5, 26, -12.5, 637.5);
  } else if (Signal.Contains("TChiWW")) {
    MassLimit = new TH2F("MassLimit",    "", 11,  87.5,  362.5, 55,  -2.5, 272.5);
  } else if (Signal.Contains("TChiSlep")) {
    //MassLimit = new TH2F("MassLimit",    "", 29,  87.5,  812.5, 25, -12.5, 612.5);
    MassLimit = new TH2F("MassLimit",    "", 37 ,  87.5,  1012.5, 25, -12.5, 612.5);
  }
  ifstream InFile; InFile.open("./MassPointList" + Signal + ".txt");

  float CentralQuantile = -1.;
  if (Type!="") CentralQuantile = 0.5;
  //if (Type=="Do") CentralQuantile = 0.16;
  //if (Type=="Up") CentralQuantile = 0.84;
  if (Type.Contains("Blind")) Type = "Blind";
  else if (Type!="Expected") Type = "";

  while (InFile) {

    TString MassPoint;
    InFile >> MassPoint;
   
    if (!MassPoint.Contains("#") && MassPoint!="") {
      
      //MassPoint.ReplaceAll("tt", "tt_isr"); 
      TString RootFileName1 = "./Datacards" + Reference + "/MassPoint" + MassPoint + "/datacardFinal" + Type + ".root"; // 1 = Den
      TString RootFileName2 = "./Datacards" + Version   + "/MassPoint" + MassPoint + "/datacardFinal" + Type + ".root"; // 2 = Num

      TFile *RootFile1 = TFile::Open(RootFileName1, "read");
      TFile *RootFile2 = TFile::Open(RootFileName2, "read");

      //MassPoint.ReplaceAll("tt_isr", "");

      if (!RootFile1) continue;
      if (!RootFile2) continue;

      TTree *fChain1 = (TTree*) RootFile1->Get("limit");
      TTree *fChain2 = (TTree*) RootFile2->Get("limit");

      if (!fChain1 || !fChain2) { 
	cout << "Warning: " << MassPoint << " ";
	if (!fChain1) cout << Reference;
	if (!fChain2) cout << Version;
	cout << " does not have chain" << endl;
	RootFile1->Close();
	RootFile2->Close();
	continue;
      }

      Float_t _quantileExpected1; Double_t _limit1;
      fChain1->SetBranchAddress("quantileExpected", &_quantileExpected1);
      fChain1->SetBranchAddress("limit",            &_limit1);
      
      Float_t _quantileExpected2; Double_t _limit2;
      fChain2->SetBranchAddress("quantileExpected", &_quantileExpected2);
      fChain2->SetBranchAddress("limit",            &_limit2);
      
      int _nentries1     = fChain1->GetEntries();
      int _nentries2     = fChain2->GetEntries();

      if (_nentries1==0 || _nentries2==0) {
	cout << "Warning: " << MassPoint << " ";
	if (_nentries1==0 ) cout << Reference;
	if (_nentries2==0 ) cout << Version;
	cout << " has no entries" << endl;
	RootFile1->Close();
	RootFile2->Close();
	continue;
      }

      float pointlimit1, pointlimit2;

      for (Long64_t jentry=0; jentry<_nentries1;jentry++) {

	fChain1->GetEntry(jentry);
	fChain2->GetEntry(jentry);

	if (_quantileExpected1==CentralQuantile) pointlimit1 = _limit1;
	if (_quantileExpected2==CentralQuantile) pointlimit2 = _limit2;

      }

      TString StopMass = MassPoint;
      StopMass.Replace(0, StopMass.First("_")+1, "");
      if (Signal.Contains("T2tt")) StopMass.Replace(0, StopMass.First("_")+1, "");
      TString XMass = StopMass;
      StopMass.Replace(StopMass.First("_"), 10000,"");
      StopMass.ReplaceAll("Sm", "");
      StopMass.ReplaceAll("Xm", "");
      XMass.Replace(0, XMass.First("_")+1, "");
      XMass.ReplaceAll("Xm", "");
 
      if (Signal.Contains("T2") && (StopMass.Atoi())%5!=0) continue;

      if (pointlimit2/pointlimit1<5.){
	float RoundPrecision = (Signal.Contains("T2")) ? 1000. : 100.;
	float _limitratio = pointlimit2/pointlimit1;
	int _ilimitratio = round(RoundPrecision*_limitratio);
	float _flimitratio = _ilimitratio/RoundPrecision;
	MassLimit->Fill(StopMass.Atoi(), XMass.Atoi(), _flimitratio);
      }
      
      RootFile1->Close();
      RootFile2->Close();

    }

  }

  gStyle->SetOptStat(0);
  MassLimit->SetXTitle("M_{#tilde t} [GeV]");
  if (Signal.Contains("TChi")) MassLimit->SetXTitle("M_{#tilde #Chi^{#pm}_{1}} [GeV]");
  MassLimit->SetYTitle("M_{#tilde #Chi^{0}_{1}} [GeV]");
  MassLimit->Draw("TEXT");//COLZ");

}
