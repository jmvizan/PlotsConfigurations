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

class LeptonL2TWeightReader : public multidraw::TTreeFunction {
public:
  LeptonL2TWeightReader(char const* fileName, char const* muoWP, char const* eleWP);

  char const* getName() const override { return "LeptonL2TWeightReader"; }
  TTreeFunction* clone() const override { return new LeptonL2TWeightReader(fileName_.Data(), muoWP_.Data(), eleWP_.Data()); }
  
  void beginEvent(long long) override;
  unsigned getNdata() override { return leptonL2TWeightReader.size(); }
  int getMultiplicity() override { return 1; }
  double evaluate(unsigned) override;

protected:
  void bindTree_(multidraw::FunctionLibrary&) override;
  
  FloatArrayReader* Lepton_pt{};
  FloatArrayReader* Lepton_eta{};
  IntArrayReader*   Lepton_isTightMuo{};
  IntArrayReader*   Lepton_isTightEle{};
  IntArrayReader*   Lepton_pdgId{};

  std::vector<double> leptonL2TWeightReader{};
  void setValues();
  double GetBinContent4Weight(TH2* hist, double valx, double valy, double sys);

  TString fileName_{};
  TString muoWP_{};
  TString eleWP_{};

  TFile* rootFile{};
  TH2F* histMuoL2TWeightReader{};
  TH2F* histEleL2TWeightReader{};   
  
};

void LeptonL2TWeightReader::beginEvent(long long _iEntry) {
  setValues();
}

LeptonL2TWeightReader::LeptonL2TWeightReader(char const* fileName, char const* muoWP, char const* eleWP) :
  TTreeFunction(),
  fileName_{fileName},
  muoWP_{muoWP},
  eleWP_{eleWP}
{
  rootFile = new TFile(fileName_);
  histMuoL2TWeightReader = (TH2F*)rootFile->Get("MuonLoose2TightRate");
  histEleL2TWeightReader = (TH2F*)rootFile->Get("ElectronLoose2TightRate"); 
}

double
LeptonL2TWeightReader::evaluate(unsigned iJ) {
  return leptonL2TWeightReader[iJ];
}

void LeptonL2TWeightReader::bindTree_(multidraw::FunctionLibrary& _library) {
  _library.bindBranch(Lepton_pt, "Lepton_pt");
  _library.bindBranch(Lepton_eta, "Lepton_eta");
  _library.bindBranch(Lepton_isTightMuo, "Lepton_isTightMuon_"+muoWP_);
  _library.bindBranch(Lepton_isTightEle, "Lepton_isTightElectron_"+eleWP_);
  _library.bindBranch(Lepton_pdgId, "Lepton_pdgId");
}

void LeptonL2TWeightReader::setValues() {

  leptonL2TWeightReader.clear();

  float leptonL2TWeight = 1.;
  int nLnoT = 0;
  for (int ilep = 0; ilep<2; ilep++) {
    double lepEta{Lepton_eta->At(ilep)};
    double lepPt{Lepton_pt->At(ilep)};
    int isTightMuo{Lepton_isTightMuo->At(ilep)};
    int isTightEle{Lepton_isTightEle->At(ilep)};
    int lepId{Lepton_pdgId->At(ilep)};
    if ((lepId==11 || lepId==-11) && isTightEle==0) { // How was abs in C++?
      leptonL2TWeight *= this->GetBinContent4Weight(histEleL2TWeightReader, lepPt, lepEta, 0);
      nLnoT += 1;
    } else if ((lepId==13 || lepId==-13) && isTightMuo==0) {
      leptonL2TWeight *= this->GetBinContent4Weight(histMuoL2TWeightReader, lepPt, lepEta, 0);
      nLnoT += 1;
    }
  }
  if (nLnoT!=1) {  
      std::cout << "LeptonL2TWeightReader Error: " << nLnoT << " loose no-tight leptons found in the event!" << std::endl;
  } else if (leptonL2TWeight<=0.) {
      std::cout << "LeptonL2TWeightReader Error: leptonL2TWeight = " << leptonL2TWeight << "!" << std::endl;
  }

  leptonL2TWeightReader.push_back(leptonL2TWeight);

}

double LeptonL2TWeightReader::GetBinContent4Weight(TH2* hist, double valx, double valy, double sys){
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
    


