#include "LatinoAnalysis/MultiDraw/interface/TTreeFunction.h"
#include "LatinoAnalysis/MultiDraw/interface/FunctionLibrary.h"
#include <vector>
#include <map>

#include "TVector2.h"
#include "TString.h"
#include "TFile.h"
#include "TH2.h"
#include "TH2F.h"
#include "TGraph.h"
#include "Math/Vector4Dfwd.h"
#include "Math/GenVector/LorentzVector.h"
#include "Math/GenVector/PtEtaPhiM4D.h"

#include <iostream>

class MuonJetFinder : public multidraw::TTreeFunction {
public:
  MuonJetFinder(float ptCut, float drcut);

  char const* getName() const override { return "MuonJetFinder"; }
  TTreeFunction* clone() const override { return new MuonJetFinder(ptCut_, drCut_); }
  
  void beginEvent(long long) override;
  unsigned getNdata() override { return muonJetFinder.size(); }
  int getMultiplicity() override { return 1; }
  double evaluate(unsigned) override;

protected:
  void bindTree_(multidraw::FunctionLibrary&) override;
 
  IntArrayReader*    nPFMuon{};
  DoubleArrayReader* PFMuon_pt{};
  DoubleArrayReader* PFMuon_eta{};
  LongArrayReader*   PFMuon_GoodQuality{};
  LongArrayReader*   PFMuon_IdxJet{};

  float ptCut_;
  float drCut_;

  std::vector<double> muonJetFinder{};
  void setValues();

};

void MuonJetFinder::beginEvent(long long _iEntry) {
  setValues();
}

MuonJetFinder::MuonJetFinder(float ptCut, float drCut) :
  TTreeFunction(),
  ptCut_{ptCut},
  drCut_{drCut}
{
}

double
MuonJetFinder::evaluate(unsigned iJ) {
  return muonJetFinder[iJ];
}

void MuonJetFinder::bindTree_(multidraw::FunctionLibrary& _library) {
  _library.bindBranch(nPFMuon,              "nPFMuon");
  _library.bindBranch(PFMuon_pt,            "PFMuon_pt");
  _library.bindBranch(PFMuon_eta,           "PFMuon_eta");
  _library.bindBranch(PFMuon_GoodQuality,   "PFMuon_GoodQuality");
  _library.bindBranch(PFMuon_IdxJet,        "PFMuon_IdxJet");
}

void MuonJetFinder::setValues() {

  muonJetFinder.clear();

  int nGoodSoftMuon = 0, muonIndex = -1, muonJetIndex = -1;
  float ptMaxMuon = 0.;

  for (int imu = 0; imu<nPFMuon->At(0); imu++) {

    double    muPt{PFMuon_pt->At(imu)};
    double    muEta{PFMuon_eta->At(imu)}; 
    long long muQuality{PFMuon_GoodQuality->At(imu)};
    long long muJet{PFMuon_IdxJet->At(imu)};

    if (muQuality>=2 && muPt>5. && muEta>-2.4 && muEta<2.4 && muJet>=0) {
      if (muPt>ptMaxMuon) {
        muonIndex = imu;
        muonJetIndex = muJet;
        ptMaxMuon = muPt;
      }
      nGoodSoftMuon++;
    }

  }

  if (nGoodSoftMuon==1) {    
    muonJetFinder.push_back(muonIndex);
    muonJetFinder.push_back(muonJetIndex);
  } else {
    muonJetFinder.push_back(-1);
    muonJetFinder.push_back(-1);
  }

}


