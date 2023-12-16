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

class FastsimLeptonWeightReader : public multidraw::TTreeFunction {
public:
  FastsimLeptonWeightReader(char const* fileName, char const* histNameMuo, char const* histNameEle);

  char const* getName() const override { return "FastsimLeptonWeightReader"; }
  TTreeFunction* clone() const override { return new FastsimLeptonWeightReader(fileName_.Data(), histNameMuo_.Data(), histNameEle_.Data()); }
  
  void beginEvent(long long) override;
  unsigned getNdata() override { return fastsimLeptonWeightReader.size(); }
  int getMultiplicity() override { return 1; }
  double evaluate(unsigned) override;

protected:
  void bindTree_(multidraw::FunctionLibrary&) override;
  
  FloatArrayReader* Lepton_pt{};
  FloatArrayReader* Lepton_eta{};
  IntArrayReader*   Lepton_pdgId{};
  IntArrayReader*   Lepton_electronIdx{};
  FloatArrayReader* Electron_deltaEtaSC{};

  std::vector<double> fastsimLeptonWeightReader{};
  void setValues();
  double GetBinContent4Weight(TH2* hist, double valx, double valy, double sys);

  TString fileName_{};
  TString histNameMuo_{};
  TString histNameEle_{};

  TFile* rootFile{};
  TH2F* histMuoFastsimLeptonWeightReader{};
  TH2F* histEleFastsimLeptonWeightReader{};   

};

void FastsimLeptonWeightReader::beginEvent(long long _iEntry) {
  setValues();
}

FastsimLeptonWeightReader::FastsimLeptonWeightReader(char const* fileName, char const* histNameMuo, char const* histNameEle) :
  TTreeFunction(),
  fileName_{fileName},
  histNameMuo_{histNameMuo},
  histNameEle_{histNameEle}
{
  rootFile = new TFile(fileName_);
  histMuoFastsimLeptonWeightReader = (TH2F*)rootFile->Get(histNameMuo_);
  histEleFastsimLeptonWeightReader = (TH2F*)rootFile->Get(histNameEle_);
}

double
FastsimLeptonWeightReader::evaluate(unsigned iJ) {
  return fastsimLeptonWeightReader[iJ];
}

void FastsimLeptonWeightReader::bindTree_(multidraw::FunctionLibrary& _library) {
  _library.bindBranch(Lepton_pt, "Lepton_pt");
  _library.bindBranch(Lepton_eta, "Lepton_eta");
  _library.bindBranch(Lepton_pdgId, "Lepton_pdgId");
  _library.bindBranch(Lepton_electronIdx, "Lepton_electronIdx");
  _library.bindBranch(Electron_deltaEtaSC, "Electron_deltaEtaSC");
}

void FastsimLeptonWeightReader::setValues() {

  fastsimLeptonWeightReader.clear();
  float fastsimLeptonWeight = 1.;
  for (int ilep = 0; ilep<2; ilep++) {  
    double lepEta{Lepton_eta->At(ilep)}; //TODO will use scEta for electron 
    double lepPt{Lepton_pt->At(ilep)};
    int lepId{Lepton_pdgId->At(ilep)};
    if (lepId==11 || lepId==-11) { // How was abs in C++?
      fastsimLeptonWeight *= this->GetBinContent4Weight(histEleFastsimLeptonWeightReader, lepEta, lepPt, 0);
    } else {
      fastsimLeptonWeight *= this->GetBinContent4Weight(histMuoFastsimLeptonWeightReader, lepPt, lepEta, 0);
    }
  }
  fastsimLeptonWeightReader.push_back(fastsimLeptonWeight);

}

double FastsimLeptonWeightReader::GetBinContent4Weight(TH2* hist, double valx, double valy, double sys){

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
    


