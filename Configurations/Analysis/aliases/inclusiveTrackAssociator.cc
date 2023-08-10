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

class InclusiveTrackAssociator : public multidraw::TTreeFunction {
public:
  InclusiveTrackAssociator(float ptcut = 5., float drcut = 999.);

  char const* getName() const override { return "InclusiveTrackAssociator"; }
  TTreeFunction* clone() const override { return new InclusiveTrackAssociator(ptcut_, drcut_); }
  
  void beginEvent(long long) override;
  unsigned getNdata() override { return inclusiveTrackAssociator.size(); }
  int getMultiplicity() override { return 1; }
  double evaluate(unsigned) override;

protected:
  void bindTree_(multidraw::FunctionLibrary&) override;

  IntArrayReader*    nJet{}; 
  LongArrayReader*   Jet_nFirstTrkInc{};
  LongArrayReader*   Jet_nLastTrkInc{};
  IntArrayReader*    nTrkInc{};
  DoubleArrayReader* TrkInc_pt{};
  DoubleArrayReader* TrkInc_eta{};
  DoubleArrayReader* TrkInc_phi{};

  std::vector<int> inclusiveTrackAssociator{};
  void setValues();

  float ptcut_{};
  float drcut_{};

};

void InclusiveTrackAssociator::beginEvent(long long _iEntry) {
  setValues();
}

InclusiveTrackAssociator::InclusiveTrackAssociator(float ptcut, float drcut) :
  TTreeFunction(),
  ptcut_{ptcut},
  drcut_{drcut}
{
}

double
InclusiveTrackAssociator::evaluate(unsigned iJ) {
  return inclusiveTrackAssociator[iJ];
}

void InclusiveTrackAssociator::bindTree_(multidraw::FunctionLibrary& _library) {
  _library.bindBranch(nJet,              "nJet");
  _library.bindBranch(Jet_nFirstTrkInc,  "Jet_nFirstTrkInc");
  _library.bindBranch(Jet_nLastTrkInc,   "Jet_nLastTrkInc");
  _library.bindBranch(nTrkInc,           "nTrkInc");
  _library.bindBranch(TrkInc_pt,         "TrkInc_pt");
  _library.bindBranch(TrkInc_eta,        "TrkInc_eta");
  _library.bindBranch(TrkInc_phi,        "TrkInc_phi");
}

void InclusiveTrackAssociator::setValues() {

  inclusiveTrackAssociator.clear();
  
  for (int itrk = 0; itrk<nTrkInc->At(0); itrk++) { 
   
    double associatedJet = -1.;

    for (int ijet = 0; ijet<nJet->At(0); ijet++) {
      
      long long firstJetTrk{Jet_nFirstTrkInc->At(ijet)};
      long long lastJetTrk{Jet_nLastTrkInc->At(ijet)};

      if (firstJetTrk>=0 && itrk>=firstJetTrk && lastJetTrk>=0 && itrk<lastJetTrk) {
        associatedJet = double(ijet);
      }

    }

    inclusiveTrackAssociator.push_back(associatedJet);

  }

}

 
