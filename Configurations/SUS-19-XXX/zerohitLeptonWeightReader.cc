#include "LatinoAnalysis/MultiDraw/interface/TTreeFunction.h"
#include "LatinoAnalysis/MultiDraw/interface/FunctionLibrary.h"

#include <vector>
#include <map>

#include "TVector2.h"
#include "TString.h"
#include "TFile.h"
#include "TH2.h"
#include "TH2F.h"
#include "Math/Vector4Dfwd.h"
#include "Math/GenVector/LorentzVector.h"
#include "Math/GenVector/PtEtaPhiM4D.h"

#include <iostream>

class ZeroHitLeptonWeightReader : public multidraw::TTreeFunction {
public:
  ZeroHitLeptonWeightReader(char const* fileName, char const* histName);

  char const* getName() const override { return "ZeroHitLeptonWeightReader"; }
  TTreeFunction* clone() const override { return new ZeroHitLeptonWeightReader(fileName_.Data(), histName_.Data()); }
  
  void beginEvent(long long) override;
  unsigned getNdata() override { return zerohitLeptonWeightReader.size(); }
  int getMultiplicity() override { return 1; }
  double evaluate(unsigned) override;

protected:
  void bindTree_(multidraw::FunctionLibrary&) override;
  
  FloatArrayReader* Lepton_pt{};
  FloatArrayReader* Lepton_eta{};
  IntArrayReader*   Lepton_pdgId{};
  IntArrayReader*   Lepton_electronIdx{};
  FloatArrayReader* Electron_deltaEtaSC{};

  std::vector<double> zerohitLeptonWeightReader{};
  void setValues();
  double GetBinContent4Weight(TH2* hist, double valx, double valy, double sys);

  TString fileName_{};
  TString histName_{};

  TFile* rootFile{};
  TH2F* histZeroHitLeptonWeightReader{};

};

void ZeroHitLeptonWeightReader::beginEvent(long long _iEntry) {
  setValues();
}

ZeroHitLeptonWeightReader::ZeroHitLeptonWeightReader(char const* fileName, char const* histName) :
  TTreeFunction(),
  fileName_{fileName},
  histName_{histName}
{
  rootFile = new TFile(fileName_);
  histZeroHitLeptonWeightReader = (TH2F*)rootFile->Get(histName_);
}

double
ZeroHitLeptonWeightReader::evaluate(unsigned iJ) {
  return zerohitLeptonWeightReader[iJ];
}

void ZeroHitLeptonWeightReader::bindTree_(multidraw::FunctionLibrary& _library) {
  _library.bindBranch(Lepton_pt, "Lepton_pt");
  _library.bindBranch(Lepton_eta, "Lepton_eta");
  _library.bindBranch(Lepton_pdgId, "Lepton_pdgId");
  _library.bindBranch(Lepton_electronIdx, "Lepton_electronIdx");
  _library.bindBranch(Electron_deltaEtaSC, "Electron_deltaEtaSC");
}

void ZeroHitLeptonWeightReader::setValues() {

  zerohitLeptonWeightReader.clear();
  float zerohitLeptonWeight = 1.;
  for (int ilep = 0; ilep<2; ilep++) {  
    double lepEta{Lepton_eta->At(ilep)}; //TODO will use scEta for electron 
    double lepPt{Lepton_pt->At(ilep)};
    int lepEleIdx{Lepton_electronIdx->At(ilep)};    
    int lepId{Lepton_pdgId->At(ilep)};
    if (lepEleIdx>=0 && (lepId==11 || lepId==-11)) { // How was abs in C++?
      double lepDeltaEta=Electron_deltaEtaSC->At(lepEleIdx);
      double lepSCEta=lepEta+lepDeltaEta;
      zerohitLeptonWeight *= this->GetBinContent4Weight(histZeroHitLeptonWeightReader, lepSCEta, lepPt, 0);
    }
  }
  zerohitLeptonWeightReader.push_back(zerohitLeptonWeight);

}

double ZeroHitLeptonWeightReader::GetBinContent4Weight(TH2* hist, double valx, double valy, double sys){

  double xmin=hist->GetXaxis()->GetXmin();
  double xmax=hist->GetXaxis()->GetXmax();
  double ymin=hist->GetYaxis()->GetXmin();
  double ymax=hist->GetYaxis()->GetXmax();
  if(xmin>=0) valx=fabs(valx);
  if(valx<xmin) valx=xmin+0.001;
  if(valx>xmax) valx=xmax-0.001;
  if(ymin>=0) valy=fabs(valy);
  if(valy<ymin) valy=ymin+0.001;
  if(valy>ymax) valy=ymax-0.001;
  float weight = hist->GetBinContent(hist->FindBin(valx,valy));
  if (sys!=0) {
    weight += sys*hist->GetBinError(hist->FindBin(valx,valy));
  }
  return weight;
}
    


