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

class GlobalLeptonWeightReader : public multidraw::TTreeFunction {
public:
  GlobalLeptonWeightReader(char const* fileNameMuo, char const* fileNameEle, char const* histName);

  char const* getName() const override { return "GlobalLeptonWeightReader"; }
  TTreeFunction* clone() const override { return new GlobalLeptonWeightReader(fileNameMuo_.Data(), fileNameEle_.Data(), histName_.Data()); }
  
  void beginEvent(long long) override;
  unsigned getNdata() override { return globalLeptonWeightReader.size(); }
  int getMultiplicity() override { return 1; }
  double evaluate(unsigned) override;

protected:
  void bindTree_(multidraw::FunctionLibrary&) override;
  
  FloatArrayReader* Lepton_pt{};
  FloatArrayReader* Lepton_eta{};
  IntArrayReader*   Lepton_pdgId{};
  IntArrayReader*   Lepton_electronIdx{};
  FloatArrayReader* Electron_deltaEtaSC{};

  std::vector<double> globalLeptonWeightReader{};
  void setValues();
  double GetBinContent4Weight(TH2* hist, double valx, double valy, double sys);

  TString fileNameMuo_{};
  TString fileNameEle_{};
  TString histName_{};

  TFile* rootFileMuo{};
  TFile* rootFileEle{};
  TH2F* histMuoGlobalLeptonWeightReader{};
  TH2F* histEleGlobalLeptonWeightReader{};   

};

void GlobalLeptonWeightReader::beginEvent(long long _iEntry) {
  setValues();
}

GlobalLeptonWeightReader::GlobalLeptonWeightReader(char const* fileNameMuo,  char const* fileNameEle, char const* histName) :
  TTreeFunction(),
  fileNameMuo_{fileNameMuo},
  fileNameEle_{fileNameEle},
  histName_{histName}
{
  rootFileMuo = new TFile(fileNameMuo_);
  rootFileEle = new TFile(fileNameEle_);
  histMuoGlobalLeptonWeightReader = (TH2F*)rootFileMuo->Get(histName_);
  histEleGlobalLeptonWeightReader = (TH2F*)rootFileEle->Get(histName_);
}

double
GlobalLeptonWeightReader::evaluate(unsigned iJ) {
  return globalLeptonWeightReader[iJ];
}

void GlobalLeptonWeightReader::bindTree_(multidraw::FunctionLibrary& _library) {
  _library.bindBranch(Lepton_pt, "Lepton_pt");
  _library.bindBranch(Lepton_eta, "Lepton_eta");
  _library.bindBranch(Lepton_pdgId, "Lepton_pdgId");
  _library.bindBranch(Lepton_electronIdx, "Lepton_electronIdx");
  _library.bindBranch(Electron_deltaEtaSC, "Electron_deltaEtaSC");
}

void GlobalLeptonWeightReader::setValues() {

  globalLeptonWeightReader.clear();
  float globalLeptonWeight = 1.;
  for (int ilep = 0; ilep<2; ilep++) {  
    double lepEta{Lepton_eta->At(ilep)}; //TODO will use scEta for electron 
    double lepPt{Lepton_pt->At(ilep)};
    int lepId{Lepton_pdgId->At(ilep)};
    if (lepId==11 || lepId==-11) { // How was abs in C++?
      globalLeptonWeight *= this->GetBinContent4Weight(histEleGlobalLeptonWeightReader, lepEta, lepPt, 0);
    } else {
      globalLeptonWeight *= this->GetBinContent4Weight(histMuoGlobalLeptonWeightReader, lepPt, lepEta, 0);
    }
  }
  globalLeptonWeightReader.push_back(globalLeptonWeight);

}

double GlobalLeptonWeightReader::GetBinContent4Weight(TH2* hist, double valx, double valy, double sys){

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
    


