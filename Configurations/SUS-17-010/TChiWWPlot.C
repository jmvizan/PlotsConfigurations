#include "TCanvas.h"
#include "TH1D.h"
#include "TH2D.h"
#include "TString.h"
#include "TFile.h"
#include <TROOT.h>
#include <TStyle.h>
#include <TLegend.h>
#include <TLatex.h>

#include "TCanvas.h"
#include "TFile.h"
#include "TFrame.h"
#include "TH1.h"
#include "THStack.h"
#include "TInterpreter.h"
#include "TLatex.h"
#include "TLegend.h"
#include "TLine.h"
#include "TGraphAsymmErrors.h"
#include "TMath.h"
#include "TPaletteAxis.h"
#include "TROOT.h"
#include "TString.h"
#include "TStyle.h"
#include "TSystem.h"
#include "TTree.h"

#include "SUSYCrossSections.C"

TString LSP = "#lower[-0.12]{#tilde{#chi}}#lower[0.2]{#scale[0.85]{^{0}}}#kern[-1.3]{#scale[0.85]{_{1}}}";
TString CHR = "#lower[-0.12]{#tilde{#chi}}#lower[0.2]{#scale[0.85]{^{#pm}}}#kern[-1.3]{#scale[0.85]{_{1}}}";

//const int nPoints = 11; float offset1 = 10., offset2 = 10.;
//int massPoint[nPoints] = {100, 125, 150, 175, 200, 225, 250, 275, 300, 325, 350};
//const int nPoints = 19; float offset1 = 10., offset2 = 10.;
//int massPoint[nPoints] = {100, 125, 150, 175, 200, 225, 250, 275, 300, 325, 350, 375, 400, 425, 450, 475, 500, 525, 550};
//const int nPoints = 27; float offset1 = 10., offset2 = 10.;
//int massPoint[nPoints] = {100, 125, 138, 150, 163, 175, 188, 200, 213, 225, 238, 250, 263, 275, 288, 300, 325, 338, 350, 375, 400, 425, 450, 475, 500, 525, 550}; float offset1 = 10., offset2 = 10.;
//const int nPoints = 28;
//int massPoint[nPoints] = {100, 113, 125, 138, 150, 163, 175, 188, 200, 213, 225, 238, 250, 263, 275, 288, 300, 325, 338, 350, 375, 400, 425, 450, 475, 500, 525, 550}; float offset1 = 10., offset2 = 10.;
//const int nPoints = 9;
//int massPoint[nPoints] = {100, 113, 138, 163, 188, 213, 238, 263, 338}; float offset1 = 10., offset2 = 10.;
const int nPoints = 22; float offset1 = 10., offset2 = 10.;
int massPoint[nPoints] = {100, 113, 125, 138, 150, 163, 175, 200, 225, 250, 275, 300, 325, 350, 375, 400, 425, 450, 475, 500, 525, 550};
//const int nPoints = 21; float offset1 = 10., offset2 = 10.;
//int massPoint[nPoints] = {100, 113, 125, 138, 150, 175, 200, 225, 250, 275, 300, 325, 350, 375, 400, 425, 450, 475, 500, 525, 550};
//const int nPoints = 20; float offset1 = 13., offset2 = 10.;
//int massPoint[nPoints] = {113, 125, 138, 150, 175, 200, 225, 250, 275, 300, 325, 350, 375, 400, 425, 450, 475, 500, 525, 550};
//const int nPoints = 21; float offset1 = 13., offset2 = 10.;
//int massPoint[nPoints] = {113, 125, 138, 150, 163, 175, 200, 225, 250, 275, 300, 325, 350, 375, 400, 425, 450, 475, 500, 525, 550};

void DrawLatex(Font_t      tfont,
	       Float_t     x,
	       Float_t     y,
	       Float_t     tsize,
	       Short_t     align,
	       const char* text,
	       Bool_t      setndc = true)
{
  TLatex* tl = new TLatex(x, y, text);

  tl->SetNDC      (setndc);
  tl->SetTextAlign( align);
  tl->SetTextFont ( tfont);
  tl->SetTextSize ( tsize);

  tl->Draw("same");
}

void TChiWWPlot(TString LimitFlag = "TChiWWNoTopPt", int Smooth = 0) {

  TString LimitDirectory = "Datacards" + LimitFlag + "/";

  //float offset = 0.;//12.5/2.;
  //int nhPoints = (massPoint[nPoints-1]-massPoint[0]+2.*offset)/offset;
  TH1F *Frame = new TH1F("Frame", "", 10000, massPoint[0]-offset1, massPoint[nPoints-1]+offset2);
  //TH1F *ExpLimit0 = new TH1F("ExpLimit0", "", nhPoints, massPoint[0]-offset, massPoint[nPoints-1]+offset);
  //TH1F *ExpLmtUp1 = new TH1F("ExpLmtUp1", "", nhPoints, massPoint[0]-offset, massPoint[nPoints-1]+offset);
  //TH1F *ExpLmtUp2 = new TH1F("ExpLmtUp2", "", nhPoints, massPoint[0]-offset, massPoint[nPoints-1]+offset);
  //TH1F *ExpLmtDo1 = new TH1F("ExpLmtDo1", "", nhPoints, massPoint[0]-offset, massPoint[nPoints-1]+offset);
  //TH1F *ExpLmtDo2 = new TH1F("ExpLmtDo2", "", nhPoints, massPoint[0]-offset, massPoint[nPoints-1]+offset);
  //TH1F *ObsLimit0 = new TH1F("ObsLimit0", "", nhPoints, massPoint[0]-offset, massPoint[nPoints-1]+offset);
  //TH1F *CrossSec1 = new TH1F("CrossSec1", "", nhPoints, massPoint[0]-offset, massPoint[nPoints-1]+offset);
  //TH1F *CrossSec2 = new TH1F("CrossSec2", "", nhPoints, massPoint[0]-offset, massPoint[nPoints-1]+offset);

  
  TGraph *ExpLimit0 = new TGraph;
  TGraphErrors *ExpLmtUp1 = new TGraphErrors;
  TGraphErrors *ExpLmtDo1 = new TGraphErrors;
  TGraphErrors *ExpLmtUp2 = new TGraphErrors;
  TGraphErrors *ExpLmtDo2 = new TGraphErrors;
  TGraph *ObsLimit0 = new TGraph;
  TGraph *ObsLimit0new = new TGraph;
  TGraph *CrossSec2 = new TGraph;
  TGraphErrors *CrossSec1 = new TGraphErrors;

  float minY = 999., maxY = 0.;

  for (int mp = 0; mp<nPoints; mp++) {
    
    TString inputFileName = LimitDirectory + "MassPointChiWW_Xm";
    inputFileName += massPoint[mp]; 
    inputFileName += "_Xm1/datacardFinal.root";
    if (massPoint[mp]%5!=0) {
      inputFileName.ReplaceAll("NoTopPt", "_mChi1");
      inputFileName.ReplaceAll("tChiWW", "tChiWW_mChi1");
      if (massPoint[mp]==113) inputFileName.ReplaceAll("MassPointChiWW_mChi1", "MassPointChiWW_mChi1bis");
    }
    if (massPoint[mp]==100) inputFileName.ReplaceAll("MassPointChiWW", "MassPointChiWW_mChi1ter");
    TFile *inputFile = TFile::Open(inputFileName, "read");
    
    TTree *fChain = (TTree*) inputFile->Get("limit");
      
    float _quantileExpected; Double_t _limit;
    fChain->SetBranchAddress("quantileExpected", &_quantileExpected);
    fChain->SetBranchAddress("limit",            &_limit);
    
    int _nentries = fChain->GetEntries();
    
    if (_nentries==0) {
      cout << " Warning: file " << inputFileName << " not written " << endl;
      continue;
    }
      
    GetSUSYCrossSection(1.*massPoint[mp], "TChi");
   
    //CrossSec1->SetBinContent(mp+1, CrossSection);
    //CrossSec1->SetBinError(mp+1, CrossSectionUncertainty);
    CrossSec1->SetPoint(mp, massPoint[mp], CrossSection);
    CrossSec1->SetPointError(mp, 0., CrossSectionUncertainty);
    //CrossSec2->SetBinContent(mp+1, CrossSection);
    CrossSec2->SetPoint(mp, massPoint[mp], CrossSection);
    //CrossSec2->SetBinError(mp+1, CrossSectionUncertainty);

    float xSec = 1., xSecUp1 = -1., xSecUp2 = -1., xSecDo1 = 1., xSecDo2 = -1.;

    for (Long64_t jentry=0; jentry<_nentries; jentry++) {
      
      fChain->GetEntry(jentry);

      if (_quantileExpected==-1) {
	//ObsLimit0->SetBinContent(mp+1, _limit*CrossSection);
	ObsLimit0->SetPoint(mp, massPoint[mp], _limit*CrossSection);
	if (massPoint[mp]%5!=0 || (massPoint[mp]==100 && nPoints!=19)) ObsLimit0new->SetPoint(mp, massPoint[mp], _limit*CrossSection);
      } else if (_quantileExpected==0.5)  { 
	xSec = _limit*CrossSection; 
	//ExpLimit0->SetBinContent(mp+1, _limit*CrossSection);
	ExpLimit0->SetPoint(mp, massPoint[mp], _limit*CrossSection);
	//ExpLmtUp1->SetBinContent(mp+1, _limit*CrossSection);
	//ExpLmtUp2->SetBinContent(mp+1, _limit*CrossSection);
      } else if (_quantileExpected>0.02 && _quantileExpected<0.03) {
	xSecDo2 = _limit*CrossSection;
	if (xSecDo2<minY) minY = xSecDo2;
      } else if (_quantileExpected>0.15 && _quantileExpected<0.17) {
	xSecDo1 = _limit*CrossSection;
      } else if (_quantileExpected>0.83 && _quantileExpected<0.85) {
	xSecUp1 = _limit*CrossSection;
      } else if (_quantileExpected>0.97 && _quantileExpected<0.98) {
	xSecUp2 = _limit*CrossSection;
	if (xSecUp2>maxY) maxY = xSecUp2;
      } 
      
    }

    if (xSecUp2>0. && xSecDo2>0.) {
      //ExpLmtUp2->SetBinContent(mp+1, (xSec+xSecUp2)/2.);
      //ExpLmtUp2->SetBinError(mp+1, fabs(xSec-xSecUp2)/2.);
      //ExpLmtDo2->SetBinContent(mp+1, (xSec+xSecDo2)/2.);
      //ExpLmtDo2->SetBinError(mp+1, fabs(xSec-xSecDo2)/2.);
      ExpLmtUp2->SetPoint(mp, massPoint[mp], (xSec+xSecUp2)/2.);
      ExpLmtUp2->SetPointError(mp, 0., fabs(xSec-xSecUp2)/2.);
      ExpLmtDo2->SetPoint(mp, massPoint[mp], (xSec+xSecDo2)/2.);
      ExpLmtDo2->SetPointError(mp, 0., fabs(xSec-xSecDo2)/2.);
    }

    if (xSecUp1>0. && xSecDo1>0.) {
      //ExpLmtUp1->SetBinContent(mp+1, (xSec+xSecUp1)/2.);
      //ExpLmtUp1->SetBinError(mp+1, fabs(xSec-xSecUp1)/2.);
      //ExpLmtDo1->SetBinContent(mp+1, (xSec+xSecDo1)/2.);
      //ExpLmtDo1->SetBinError(mp+1, fabs(xSec-xSecDo1)/2.);
      ExpLmtUp1->SetPoint(mp, massPoint[mp], (xSec+xSecUp1)/2.);
      ExpLmtUp1->SetPointError(mp, 0., fabs(xSec-xSecUp1)/2.);
      ExpLmtDo1->SetPoint(mp, massPoint[mp], (xSec+xSecDo1)/2.);
      ExpLmtDo1->SetPointError(mp, 0., fabs(xSec-xSecDo1)/2.);
    }

  }
  
  TCanvas *CanvasTChiWW = new TCanvas("CanvasTChiWW", "", 600, 600);// ? la Kirill, it was --> "TChiWW", "", 900, 600); 
  CanvasTChiWW->Divide(1, 1);
  
  //CanvasTChiWW->cd(1);
  
  TPad *PadTChiWW = (TPad*)CanvasTChiWW->GetPad(1);
  
  PadTChiWW->cd();
  
  // Run2015B Setting
  gStyle->SetOptFit(0);
  gStyle->SetOptStat(0);
  gStyle->SetOptTitle(0);
  
  CanvasTChiWW->Range(0,0,1,1);
  CanvasTChiWW->SetFillColor(10);
  CanvasTChiWW->SetBorderMode(0);
  CanvasTChiWW->SetBorderSize(2);
  CanvasTChiWW->SetTickx(1);
  CanvasTChiWW->SetTicky(1);
  CanvasTChiWW->SetLeftMargin(0.16);
  CanvasTChiWW->SetRightMargin(0.02);
  CanvasTChiWW->SetTopMargin(0.05);
  CanvasTChiWW->SetBottomMargin(0.13);
  CanvasTChiWW->SetFrameFillColor(0);
  CanvasTChiWW->SetFrameFillStyle(0);
  CanvasTChiWW->SetFrameBorderMode(0);
  
  PadTChiWW->SetFillColor(0);
  PadTChiWW->SetBorderMode(0);
  PadTChiWW->SetBorderSize(2);
  //PadTChiWW->SetGridy();
  PadTChiWW->SetLogy();
  PadTChiWW->SetTickx(1);
  PadTChiWW->SetTicky(1);
  PadTChiWW->SetLeftMargin(0.16);
  PadTChiWW->SetRightMargin(0.02);
  //PadTChiWW->SetTopMargin(0.05);
  //PadTChiWW->SetBottomMargin(0.31);
  PadTChiWW->SetTopMargin(0.065);
  PadTChiWW->SetBottomMargin(0.13);
  PadTChiWW->SetFrameFillStyle(0);
  PadTChiWW->SetFrameBorderMode(0);
  PadTChiWW->SetFrameFillStyle(0);
  PadTChiWW->SetFrameBorderMode(0);
  PadTChiWW->Draw();
  // End Run2015B Setting 

  Frame->SetXTitle("m_{"+CHR+"} [GeV]");
  Frame->SetYTitle("95% CL upper limit on #sigma(pp#rightarrow "+LSP+LSP+") [pb]");
    
  Frame->SetMinimum(minY*0.25);
  Frame->SetMaximum(maxY*1.25);

  Frame->GetXaxis()->SetLabelFont(42);
  Frame->GetYaxis()->SetLabelFont(42);
  Frame->GetXaxis()->SetTitleFont(42);
  Frame->GetYaxis()->SetTitleFont(42);
      
  Frame->SetTitle("");
  
  Frame->GetYaxis()->SetTitleSize(0.05);
  Frame->GetYaxis()->SetLabelSize(0.05);
  Frame->GetXaxis()->SetTitleSize(0.05);
  Frame->GetXaxis()->SetLabelSize(0.05);
  Frame->GetXaxis()->SetTitleOffset(1.2);
  Frame->GetYaxis()->SetTitleOffset(1.3);

  Frame->Draw();
  /*
  ExpLmtUp2->GetXaxis()->SetLabelFont(42);
  ExpLmtUp2->GetYaxis()->SetLabelFont(42);
  ExpLmtUp2->GetXaxis()->SetTitleFont(42);
  ExpLmtUp2->GetYaxis()->SetTitleFont(42);
      
  ExpLmtUp2->SetTitle("");
  
  ExpLmtUp2->GetYaxis()->SetTitleSize(0.05);
  ExpLmtUp2->GetYaxis()->SetLabelSize(0.05);
  ExpLmtUp2->GetXaxis()->SetTitleSize(0.05);
  ExpLmtUp2->GetXaxis()->SetLabelSize(0.05);
  ExpLmtUp2->GetXaxis()->SetTitleOffset(1.2);
  ExpLmtUp2->GetYaxis()->SetTitleOffset(1.3);
  */
  //ExpLmtUp2->GetXaxis()->SetRangeUser(1.*massPoint[0], 1.*massPoint[nPoints-1]);

  ExpLmtUp2->SetFillStyle(1001);
  ExpLmtUp1->SetFillStyle(1001);
  ExpLmtUp2->SetFillColor(kOrange);
  ExpLmtUp1->SetFillColor(kGreen+1);

  ExpLmtDo2->SetFillStyle(1001);
  ExpLmtDo1->SetFillStyle(1001);
  ExpLmtDo2->SetFillColor(kOrange);
  ExpLmtDo1->SetFillColor(kGreen+1);

  //ExpLmtUp2->SetMinimum(minY*0.25);

  TString ErrorOption = Smooth==2 ? "e4" : "e3";
  TString LimitOption = Smooth==2 ? "C"  : "l";

  ExpLmtUp2->Draw(ErrorOption);
  ExpLmtDo2->Draw(ErrorOption+"same");
  ExpLmtUp1->Draw(ErrorOption+"same");
  ExpLmtDo1->Draw(ErrorOption+"same");

  ExpLimit0->SetLineColor(4);
  ExpLimit0->SetLineStyle(2);
  ExpLimit0->SetLineWidth(2);
  ExpLimit0->Draw(LimitOption+"same");

  CrossSec2->SetLineColor(kPink+6);
  CrossSec1->SetFillColor(kPink+6);
  CrossSec1->SetFillStyle(3353);
  CrossSec2->SetLineWidth(2);
  CrossSec1->Draw(ErrorOption+"same");
  CrossSec2->Draw(LimitOption+"same");

  ObsLimit0->SetMarkerStyle(20);
  ObsLimit0->SetMarkerSize(0.7);
  ObsLimit0->SetLineColor(1);
  ObsLimit0->SetLineStyle(1);
  ObsLimit0->SetLineWidth(2);
  TString LimitOptionObserved = Smooth==1 ? "C"  : "l";
  ObsLimit0->Draw(LimitOptionObserved+"psame");

  ObsLimit0new->SetMarkerStyle(20);
  ObsLimit0new->SetMarkerColor(2);
  ObsLimit0new->SetMarkerSize(0.7);
  ObsLimit0new->Draw("psame");

  
  TLegend  *leg_fit = new TLegend(0.52, 0.63, 0.82, 0.81);
  leg_fit->SetFillColor(kWhite); leg_fit->SetBorderSize(0.);
  leg_fit->SetTextColor(1); leg_fit->SetTextSize(0.035);
  leg_fit->SetTextFont(42); 
  leg_fit->SetHeader("95% CL upper limits");
  //leg_fit->SetHeader(CHR+" #rightarrow "+LSP+"W,   m_{"+LSP+"} = 1 GeV"); //leg_fit->SetMargin(0.2); 
  //leg_fit->AddEntry((TObject*)0, " ", "");
  leg_fit->AddEntry(ObsLimit0, " Observed", "pe");
  leg_fit->AddEntry(ExpLimit0, " Median expected", "l");
  leg_fit->AddEntry(ExpLmtUp1, " 68% expected", "f");
  leg_fit->AddEntry(ExpLmtUp2, " 95% expected", "f");
  //leg_fit->AddEntry(CrossSec1, " Theoretical cross section", "lf");

  TLegend  *leg_fitT = new TLegend(0.52, 0.85, 0.82, 0.90);
  leg_fitT->SetFillColor(kWhite); leg_fitT->SetBorderSize(0.);
  leg_fitT->SetTextColor(1); leg_fitT->SetTextSize(0.035);
  leg_fitT->SetTextFont(42); 
  CrossSec1->SetLineColor(kPink+6);
  CrossSec1->SetLineWidth(2);
  leg_fitT->AddEntry(CrossSec1, " " +CHR+" #rightarrow "+LSP+"W,  m_{"+LSP+"} = 1 GeV", "lf");

  leg_fit->Draw();
  leg_fitT->Draw();

  DrawLatex(61, 0.190,   0.945, 0.050, 11, "CMS");
  DrawLatex(52, 0.300, 0.945, 0.030, 11, "Preliminary");
  DrawLatex(42, 0.940, 0.945, 0.050, 31, Form("%.1f fb^{-1} (13TeV)", 35.9));

}
