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

class BTagWeightNtag : public multidraw::TTreeFunction {
public:
  BTagWeightNtag(char const* btagdisc, char const* btagalgo, double cut, double etaMax);

  char const* getName() const override { return "BTagWeightNtag"; }
  TTreeFunction* clone() const override { return new BTagWeightNtag(btagdisc_.Data(), btagalgo_.Data(), cut_, etaMax_); }
  
  void beginEvent(long long) override;
  unsigned getNdata() override { return btagWeightNtag.size(); }
  int getMultiplicity() override { return 1; }
  double evaluate(unsigned) override;

protected:
  void bindTree_(multidraw::FunctionLibrary&) override;
 
  IntArrayReader*   nCleanJet{};
  FloatArrayReader* CleanJet_pt{};
  FloatArrayReader* CleanJet_eta{};
  IntArrayReader*   CleanJet_jetIdx{};
  FloatArrayReader* JetBTagDiscriminant{};
  FloatArrayReader* JetBTagSF{};
  FloatArrayReader* Weight1Tag{}; 
 
  std::vector<double> btagWeightNtag{};
  void setValues();

  TString btagdisc_{};
  TString btagalgo_{};
  double cut_;
  double etaMax_;

  TFile* rootFile{};
  TH2F*  kinematicWeightsHisto{};

};

void BTagWeightNtag::beginEvent(long long _iEntry) {
  setValues();
}

BTagWeightNtag::BTagWeightNtag(char const* btagdisc, char const* btagalgo, double cut, double etaMax) :
  TTreeFunction(),
  btagdisc_{btagdisc},
  btagalgo_{btagalgo},
  cut_{cut},
  etaMax_{etaMax}
{
}

double
BTagWeightNtag::evaluate(unsigned iJ) {
  return btagWeightNtag[iJ];
}

void BTagWeightNtag::bindTree_(multidraw::FunctionLibrary& _library) {
  _library.bindBranch(nCleanJet,           "nCleanJet");
  _library.bindBranch(CleanJet_pt,         "CleanJet_pt");
  _library.bindBranch(CleanJet_eta,        "CleanJet_eta");
  _library.bindBranch(CleanJet_jetIdx,     "CleanJet_jetIdx");
  _library.bindBranch(JetBTagDiscriminant, "Jet_"+btagdisc_);
  _library.bindBranch(JetBTagSF,           "Jet_btagSF_"+btagalgo_);
  _library.bindBranch(Weight1Tag,          "btagWeight_1tag_"+btagalgo_+"_1c");
}

void BTagWeightNtag::setValues() {

  btagWeightNtag.clear();

  float weight1tag{Weight1Tag->At(0)};

  btagWeightNtag.push_back(1.-weight1tag);
  btagWeightNtag.push_back(weight1tag); 

  double ntagWeightExac1 = 0.;

  for (int ijet = 0; ijet<nCleanJet->At(0); ijet++) { 

    float JetPt{CleanJet_pt->At(ijet)};
    float JetEta{CleanJet_eta->At(ijet)};
    int   JetIdx{CleanJet_jetIdx->At(ijet)};
    float JetDisc{JetBTagDiscriminant->At(JetIdx)}; 

    if (JetPt>=20. && fabs(JetEta)<etaMax_ && JetDisc>=cut_) {

      float ntagWeightExac1jet{JetBTagSF->At(JetIdx)};

      for (int ijet2 = 0; ijet2<nCleanJet->At(0); ijet2++) {
        if (ijet2!=ijet) {

          float Jet2Pt{CleanJet_pt->At(ijet2)};
          float Jet2Eta{CleanJet_eta->At(ijet2)};
          int   Jet2Idx{CleanJet_jetIdx->At(ijet2)};
          float Jet2Disc{JetBTagDiscriminant->At(Jet2Idx)};   

          if (Jet2Pt>=20. && fabs(Jet2Eta)<etaMax_ && Jet2Disc>=cut_) {

            float Jet2SF{JetBTagSF->At(Jet2Idx)};
            ntagWeightExac1jet *= (1.-Jet2SF);

          }

        }

      }

      ntagWeightExac1 += ntagWeightExac1jet;    

    }

  }

  btagWeightNtag.push_back(weight1tag-ntagWeightExac1);

  double ntagWeightExac2 = 0.;

  for (int ijet = 0; ijet<nCleanJet->At(0); ijet++) {

    float JetPt{CleanJet_pt->At(ijet)};
    float JetEta{CleanJet_eta->At(ijet)};
    int   JetIdx{CleanJet_jetIdx->At(ijet)};
    float JetDisc{JetBTagDiscriminant->At(JetIdx)};

    if (JetPt>=20. && fabs(JetEta)<etaMax_ && JetDisc>=cut_) {

      for (int jjet = ijet+1; jjet<nCleanJet->At(0); jjet++) {

        float JJetPt{CleanJet_pt->At(jjet)};
        float JJetEta{CleanJet_eta->At(jjet)};
        int   JJetIdx{CleanJet_jetIdx->At(jjet)};
        float JJetDisc{JetBTagDiscriminant->At(JJetIdx)};

        if (JJetPt>=20. && fabs(JJetEta)<etaMax_ && JJetDisc>=cut_) {

          float ntagWeightExac2jet{JetBTagSF->At(JetIdx)};
          ntagWeightExac2jet *= JetBTagSF->At(JJetIdx);

          for (int ijet2 = 0; ijet2<nCleanJet->At(0); ijet2++) {
            if (ijet2!=ijet && ijet2!=jjet) {

              float Jet2Pt{CleanJet_pt->At(ijet2)};
              float Jet2Eta{CleanJet_eta->At(ijet2)};
              int   Jet2Idx{CleanJet_jetIdx->At(ijet2)};
              float Jet2Disc{JetBTagDiscriminant->At(Jet2Idx)};

              if (Jet2Pt>=20. && fabs(Jet2Eta)<etaMax_ && Jet2Disc>=cut_) {

                float Jet2SF{JetBTagSF->At(Jet2Idx)};
                ntagWeightExac2jet *= (1.-Jet2SF);

              }

            }

          }

          ntagWeightExac2 += ntagWeightExac2jet;

        }

      }

    }

  }

  btagWeightNtag.push_back(weight1tag-ntagWeightExac1-ntagWeightExac2);

}

 
